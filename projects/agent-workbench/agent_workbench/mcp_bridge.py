"""MCP client bridge: load tools from an MCP server into the agent's registry.

This is the other half of the MCP story. `mcp_server.py` *exposes* tools; this
module *consumes* an MCP server and adapts its tools into the workbench's `Tool`
interface, so the existing (synchronous) agent loop, permission gate, and
tracing all work unchanged against remote tools.

The MCP client is async; the agent loop is sync. We bridge that by running the
MCP `ClientSession` on a dedicated background event loop and submitting each
tool call to it with `run_coroutine_threadsafe`. The session is opened once and
kept alive for the life of the provider.

    from mcp_bridge import MCPToolProvider
    with MCPToolProvider("python", ["-m", "agent_workbench.mcp_server"],
                         env={**os.environ, "AGENT_MCP_WORKDIR": workdir}) as provider:
        for tool in provider.tools:
            registry.register(tool)
        agent.run("...")

Security note: MCP tools are treated as **mutating** (gated by the permission
policy) because the bridge can't know what a remote tool does. See MCP_SECURITY.md.
"""

from __future__ import annotations

import asyncio
import threading
from typing import Any

from .tools.base import Tool, ToolResult


class MCPTool(Tool):
    """Adapts one MCP tool into the workbench `Tool` interface."""

    mutating = True  # unknown remote behavior → gate it
    parallel_safe = False

    def __init__(self, name: str, description: str, input_schema: dict[str, Any], provider: "MCPToolProvider") -> None:
        self.name = name
        self.description = description
        self._schema = input_schema
        self._provider = provider

    @property
    def input_schema(self) -> dict[str, Any]:
        return self._schema

    def run(self, **kwargs: Any) -> ToolResult:
        return self._provider.call(self.name, kwargs)


class MCPToolProvider:
    """Connects to an MCP server over stdio and exposes its tools as `Tool`s."""

    def __init__(
        self,
        command: str,
        args: list[str] | None = None,
        env: dict[str, str] | None = None,
        init_timeout: float = 20.0,
        call_timeout: float = 60.0,
    ) -> None:
        self.command = command
        self.args = args or []
        self.env = env
        self.init_timeout = init_timeout
        self.call_timeout = call_timeout
        self.tools: list[MCPTool] = []
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None
        self._session: Any = None
        self._stop: asyncio.Event | None = None
        self._ready = threading.Event()
        self._error: BaseException | None = None

    def __enter__(self) -> "MCPToolProvider":
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        if not self._ready.wait(self.init_timeout):
            raise TimeoutError("MCP server did not initialize in time")
        if self._error is not None:
            raise self._error
        return self

    def __exit__(self, *exc: Any) -> bool:
        if self._loop is not None and self._stop is not None:
            self._loop.call_soon_threadsafe(self._stop.set)
        if self._thread is not None:
            self._thread.join(timeout=10)
        return False

    # --- background loop ---------------------------------------------------
    def _run_loop(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_until_complete(self._serve())
        finally:
            self._loop.close()

    async def _serve(self) -> None:
        from mcp import ClientSession
        from mcp.client.stdio import StdioServerParameters, stdio_client

        params = StdioServerParameters(command=self.command, args=self.args, env=self.env)
        try:
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    self._session = session
                    self._stop = asyncio.Event()
                    listed = await session.list_tools()
                    self.tools = [
                        MCPTool(t.name, t.description or "", t.inputSchema, self)
                        for t in listed.tools
                    ]
                    self._ready.set()
                    await self._stop.wait()
        except BaseException as exc:  # noqa: BLE001 - report init/teardown failures to __enter__
            self._error = exc
            self._ready.set()

    # --- sync tool dispatch -------------------------------------------------
    def call(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        if self._loop is None or self._session is None:
            return ToolResult("MCP session not ready", is_error=True)
        future = asyncio.run_coroutine_threadsafe(self._call(name, arguments), self._loop)
        try:
            return future.result(timeout=self.call_timeout)
        except Exception as exc:  # noqa: BLE001 - surface call failures as tool errors
            return ToolResult(f"MCP call failed: {exc}", is_error=True)

    async def _call(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        result = await self._session.call_tool(name, arguments)
        parts = [getattr(b, "text", "") for b in result.content if getattr(b, "text", None) is not None]
        return ToolResult("\n".join(parts), is_error=bool(getattr(result, "isError", False)))
