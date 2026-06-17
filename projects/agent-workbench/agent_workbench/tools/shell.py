"""Shell tool: run a command inside the working directory.

This is the broadest, most dangerous tool — a shell can do almost anything.
That is exactly why it is `mutating` and goes through the permission gate, and
why it runs with a timeout, captures output, and stays in the workdir. A
command denylist blocks the obviously destructive patterns as defense in depth;
the real safety boundary is the permission gate plus running in a sandbox.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from .base import Tool, ToolResult

DEFAULT_TIMEOUT = 30  # seconds
MAX_OUTPUT_CHARS = 20_000

# Obvious foot-guns. This is not a security boundary on its own — a determined
# command can evade a substring denylist — it's a cheap tripwire. Run the agent
# in a throwaway sandbox for anything real.
DENYLIST = ("rm -rf /", "rm -rf ~", "mkfs", ":(){", "dd if=", "> /dev/sda")


class ShellTool(Tool):
    name = "run_shell"
    description = (
        "Run a shell command in the working directory and return stdout, stderr, "
        "and the exit code. Use for builds, tests, git, and inspection. This "
        "changes state, so it is gated by the permission policy."
    )
    mutating = True
    parallel_safe = False

    def __init__(self, workdir: Path, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.workdir = Path(workdir)
        self.timeout = timeout

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The shell command to run."}
            },
            "required": ["command"],
        }

    def run(self, command: str) -> ToolResult:
        lowered = command.lower()
        if any(bad in lowered for bad in DENYLIST):
            return ToolResult(content=f"command blocked by denylist: {command!r}", is_error=True)
        try:
            proc = subprocess.run(
                command,
                shell=True,
                cwd=str(self.workdir),
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
        except subprocess.TimeoutExpired:
            return ToolResult(content=f"command timed out after {self.timeout}s", is_error=True)

        out = (proc.stdout or "")[:MAX_OUTPUT_CHARS]
        err = (proc.stderr or "")[:MAX_OUTPUT_CHARS]
        body = f"exit_code: {proc.returncode}\n--- stdout ---\n{out}\n--- stderr ---\n{err}"
        return ToolResult(content=body, is_error=proc.returncode != 0)
