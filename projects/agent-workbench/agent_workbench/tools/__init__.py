"""Built-in tools and a helper to assemble a default registry."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from .base import Tool, ToolResult
from .fs import ReadFileTool, WriteFileTool
from .registry import ToolRegistry
from .shell import ShellTool

if TYPE_CHECKING:
    from ..sandbox import Sandbox

__all__ = [
    "Tool",
    "ToolResult",
    "ToolRegistry",
    "ReadFileTool",
    "WriteFileTool",
    "ShellTool",
    "default_registry",
]


def default_registry(workdir: Path, shell_runner: "Sandbox | None" = None) -> ToolRegistry:
    """A registry with the standard read/write/shell tools, all jailed to workdir.

    Pass `shell_runner` (e.g. a DockerSandbox) to change where run_shell executes;
    default is the local host."""
    registry = ToolRegistry()
    registry.register(ReadFileTool(workdir))
    registry.register(WriteFileTool(workdir))
    registry.register(ShellTool(workdir, runner=shell_runner))
    return registry
