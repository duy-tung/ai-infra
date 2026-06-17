"""Permission gate.

Before the harness runs a mutating tool, it asks the gate. The gate is where
your safety policy lives, separate from both the model and the tools. Three
modes cover the common cases:

- ``ask``   : prompt a human for each mutating call (default for interactive use).
- ``auto``  : allow everything (use only inside a throwaway sandbox / evals).
- ``readonly``: deny every mutating call (dry-run / inspection mode).

Read-only tools are never gated. An optional allowlist lets you pre-approve
specific tools even in ``ask`` mode.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class Decision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass
class PermissionRequest:
    tool_name: str
    tool_input: dict[str, Any]
    mutating: bool


@dataclass
class PermissionGate:
    mode: str = "ask"  # ask | auto | readonly
    allowlist: set[str] = field(default_factory=set)
    # Injected so tests (and non-tty contexts) can drive the prompt deterministically.
    prompt_fn: Callable[[str], str] = input

    def __post_init__(self) -> None:
        if self.mode not in {"ask", "auto", "readonly"}:
            raise ValueError(f"unknown permission mode: {self.mode}")

    def check(self, request: PermissionRequest) -> tuple[Decision, str]:
        """Return (decision, reason). Reason is logged in the trace."""
        if not request.mutating:
            return Decision.ALLOW, "read-only tool"
        if request.tool_name in self.allowlist:
            return Decision.ALLOW, "allowlisted"
        if self.mode == "auto":
            return Decision.ALLOW, "auto mode"
        if self.mode == "readonly":
            return Decision.DENY, "readonly mode: mutating tool denied"
        # ask mode
        return self._prompt(request)

    def _prompt(self, request: PermissionRequest) -> tuple[Decision, str]:
        # Render the action so the human can make an informed call.
        summary = ", ".join(f"{k}={_short(v)}" for k, v in request.tool_input.items())
        sys.stderr.write(f"\n[permission] {request.tool_name}({summary})\n")
        answer = self.prompt_fn("[permission] allow this action? [y/N] ").strip().lower()
        if answer in {"y", "yes"}:
            return Decision.ALLOW, "approved by human"
        return Decision.DENY, "denied by human"


def _short(value: Any, limit: int = 80) -> str:
    text = str(value).replace("\n", "\\n")
    return text if len(text) <= limit else text[:limit] + "…"
