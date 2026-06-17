"""Tool registry.

The registry is the agent's tool surface: register tools once, then hand the
schemas to the model and dispatch calls by name. Keeping this in one place is
what lets the harness gate, log, and (later) parallelize tool calls uniformly.
"""

from __future__ import annotations

from typing import Any

from .base import Tool, ToolResult


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def names(self) -> list[str]:
        return sorted(self._tools)

    def api_schemas(self) -> list[dict[str, Any]]:
        """Tool definitions in the order the API will see them. Sorted by name so
        the prompt prefix is byte-stable across runs (good for prompt caching)."""
        return [self._tools[name].to_api_schema() for name in self.names()]

    def execute(self, name: str, tool_input: dict[str, Any]) -> ToolResult:
        tool = self._tools.get(name)
        if tool is None:
            return ToolResult(content=f"unknown tool: {name}", is_error=True)
        try:
            return tool.run(**tool_input)
        except TypeError as exc:
            # Bad arguments from the model — tell it what went wrong so it can retry.
            return ToolResult(content=f"invalid arguments for {name}: {exc}", is_error=True)
        except Exception as exc:  # noqa: BLE001 - last-resort guard; tools shouldn't raise
            return ToolResult(content=f"{name} failed: {exc}", is_error=True)
