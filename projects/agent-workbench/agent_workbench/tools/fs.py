"""Filesystem tools: read and write files, jailed to a working directory.

The path jail is the important part. The model proposes a path; we resolve it
against the workdir and refuse anything that escapes (``..``, absolute paths
outside the root, symlink games). This is a security boundary, not a
convenience — never trust a path that came from the model.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import Tool, ToolResult

MAX_READ_BYTES = 200_000  # don't blow up the context window on a huge file


def resolve_in_root(root: Path, candidate: str) -> Path:
    """Resolve `candidate` under `root`, raising if it escapes the jail."""
    root = root.resolve()
    target = (root / candidate).resolve()
    if root != target and root not in target.parents:
        raise PermissionError(f"path escapes workdir: {candidate!r}")
    return target


class ReadFileTool(Tool):
    name = "read_file"
    description = (
        "Read a UTF-8 text file from the working directory. Returns the file "
        "contents. Use this to inspect code, config, or data before acting."
    )
    mutating = False
    parallel_safe = True

    def __init__(self, workdir: Path) -> None:
        self.workdir = Path(workdir)

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the file, relative to the working directory.",
                }
            },
            "required": ["path"],
        }

    def run(self, path: str) -> ToolResult:
        try:
            target = resolve_in_root(self.workdir, path)
        except PermissionError as exc:
            return ToolResult(content=str(exc), is_error=True)
        if not target.is_file():
            return ToolResult(content=f"not a file: {path}", is_error=True)
        data = target.read_bytes()
        if len(data) > MAX_READ_BYTES:
            return ToolResult(
                content=f"file too large ({len(data)} bytes; limit {MAX_READ_BYTES})",
                is_error=True,
            )
        return ToolResult(content=data.decode("utf-8", errors="replace"))


class WriteFileTool(Tool):
    name = "write_file"
    description = (
        "Write (create or overwrite) a UTF-8 text file in the working directory. "
        "Creates parent directories as needed. This changes state, so it is "
        "gated by the permission policy."
    )
    mutating = True
    parallel_safe = False

    def __init__(self, workdir: Path) -> None:
        self.workdir = Path(workdir)

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to write, relative to the working directory.",
                },
                "content": {"type": "string", "description": "Full file contents to write."},
            },
            "required": ["path", "content"],
        }

    def run(self, path: str, content: str) -> ToolResult:
        try:
            target = resolve_in_root(self.workdir, path)
        except PermissionError as exc:
            return ToolResult(content=str(exc), is_error=True)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return ToolResult(content=f"wrote {len(content)} bytes to {path}")
