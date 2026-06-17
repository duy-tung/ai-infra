"""Built-in tools and a helper to assemble a default registry."""

from __future__ import annotations

from pathlib import Path

from .base import Tool, ToolResult
from .fs import ReadFileTool, WriteFileTool
from .registry import ToolRegistry
from .shell import ShellTool

__all__ = [
    "Tool",
    "ToolResult",
    "ToolRegistry",
    "ReadFileTool",
    "WriteFileTool",
    "ShellTool",
    "default_registry",
]


def default_registry(workdir: Path) -> ToolRegistry:
    """A registry with the standard read/write/shell tools, all jailed to workdir."""
    registry = ToolRegistry()
    registry.register(ReadFileTool(workdir))
    registry.register(WriteFileTool(workdir))
    registry.register(ShellTool(workdir))
    return registry
