"""MCP server exposing the workbench's tools over the Model Context Protocol.

Why: once your tools speak MCP, *any* MCP client can use them — Claude Desktop,
the MCP Inspector, another agent, or this workbench's own bridge
(`mcp_bridge.py`). The same read/write/shell logic that the in-process registry
uses is exposed here, so there's one implementation and one security boundary
(the path jail in `tools/fs.py` / `tools/shell.py`).

Run it (stdio transport):

    AGENT_MCP_WORKDIR=/path/to/repo python -m agent_workbench.mcp_server
    # or
    python -m agent_workbench.mcp_server --workdir /path/to/repo

The working directory is the jail: every path the client sends is resolved
under it and anything that escapes is refused. See MCP_SECURITY.md for the
threat model. The `mcp` package is required: pip install -e ".[mcp]"
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

from .tools.fs import ReadFileTool, WriteFileTool
from .tools.shell import ShellTool


def build_server(workdir: Path) -> Any:
    """Build a FastMCP server whose tools are jailed to `workdir`.

    Kept as a function (not module-level) so it's importable and testable
    without starting the stdio loop."""
    from mcp.server.fastmcp import FastMCP

    workdir = Path(workdir).resolve()
    read_tool = ReadFileTool(workdir)
    write_tool = WriteFileTool(workdir)
    shell_tool = ShellTool(workdir)

    server = FastMCP("agent-workbench-tools")

    @server.tool()
    def read_file(path: str) -> str:
        """Read a UTF-8 text file from the working directory."""
        result = read_tool.run(path=path)
        if result.is_error:
            raise ValueError(result.content)
        return result.content

    @server.tool()
    def write_file(path: str, content: str) -> str:
        """Create or overwrite a UTF-8 text file in the working directory."""
        result = write_tool.run(path=path, content=content)
        if result.is_error:
            raise ValueError(result.content)
        return result.content

    @server.tool()
    def run_shell(command: str) -> str:
        """Run a shell command in the working directory; returns stdout/stderr/exit code."""
        result = shell_tool.run(command=command)
        # A non-zero exit is still a useful result for the model, not a protocol
        # error — return the body either way; the text carries the exit code.
        return result.content

    return server


def _resolve_workdir(argv: list[str] | None) -> Path:
    parser = argparse.ArgumentParser(description="MCP server exposing workbench tools.")
    parser.add_argument(
        "--workdir",
        default=os.environ.get("AGENT_MCP_WORKDIR", "."),
        help="Directory the tools are jailed to (env: AGENT_MCP_WORKDIR; default: cwd).",
    )
    args = parser.parse_args(argv)
    return Path(args.workdir).expanduser().resolve()


def main(argv: list[str] | None = None) -> None:
    workdir = _resolve_workdir(argv)
    workdir.mkdir(parents=True, exist_ok=True)
    server = build_server(workdir)
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
