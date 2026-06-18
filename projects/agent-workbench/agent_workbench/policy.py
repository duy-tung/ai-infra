"""Policy-as-code permission gate.

The `PermissionGate` hardcodes one mode for the whole run. A `PolicyGate` reads
rules from data (a dict or a YAML file) instead — per-tool actions plus path and
command denylists — so security policy lives in version control next to the
code, can be reviewed, and can differ per environment. It implements the same
`.check(request) -> (Decision, reason)` interface, so it drops straight into the
agent in place of `PermissionGate`.

Example policy (YAML):

    default: ask              # action for tools not listed below
    tools:
      read_file: allow
      write_file: ask
      run_shell: ask
    deny_paths:               # fnmatch globs — matched against the tool's `path`
      - "*.env"
      - "*secrets*"
      - "*/.git/*"
    deny_commands:            # regex — matched against run_shell's `command`
      - "rm\\s+-rf"
      - "curl.*\\|\\s*sh"

Resolution order: a deny_paths / deny_commands hit always wins (DENY); otherwise
the per-tool action (or `default`) applies. `allow`/`deny` are decided
immediately; `ask` prompts a human (same as PermissionGate's ask mode).
"""

from __future__ import annotations

import fnmatch
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Callable

from .permissions import Decision, PermissionRequest, _short


@dataclass
class Policy:
    default: str = "ask"  # allow | ask | deny
    tools: dict[str, str] = field(default_factory=dict)
    deny_paths: list[str] = field(default_factory=list)
    deny_commands: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        for action in [self.default, *self.tools.values()]:
            if action not in {"allow", "ask", "deny"}:
                raise ValueError(f"invalid policy action: {action!r}")
        self._command_res = [re.compile(p) for p in self.deny_commands]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Policy":
        return cls(
            default=data.get("default", "ask"),
            tools=dict(data.get("tools", {})),
            deny_paths=list(data.get("deny_paths", [])),
            deny_commands=list(data.get("deny_commands", [])),
        )

    @classmethod
    def from_yaml(cls, path: str) -> "Policy":
        try:
            import yaml
        except ImportError as exc:  # pragma: no cover - depends on env
            raise RuntimeError("PyYAML is required to load a policy from YAML (pip install pyyaml)") from exc
        with open(path, encoding="utf-8") as fh:
            return cls.from_dict(yaml.safe_load(fh) or {})

    def denied_by_rule(self, tool_input: dict[str, Any]) -> str | None:
        """Return a reason string if a path/command denylist rule matches, else None."""
        path = tool_input.get("path")
        if isinstance(path, str):
            for pattern in self.deny_paths:
                if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(path.split("/")[-1], pattern):
                    return f"path {path!r} matches deny rule {pattern!r}"
        command = tool_input.get("command")
        if isinstance(command, str):
            for rx in self._command_res:
                if rx.search(command):
                    return f"command matches deny rule {rx.pattern!r}"
        return None

    def action_for(self, tool_name: str) -> str:
        return self.tools.get(tool_name, self.default)


@dataclass
class PolicyGate:
    policy: Policy
    prompt_fn: Callable[[str], str] = input  # injectable for tests / non-tty

    def check(self, request: PermissionRequest) -> tuple[Decision, str]:
        rule = self.policy.denied_by_rule(request.tool_input)
        if rule is not None:
            return Decision.DENY, rule
        action = self.policy.action_for(request.tool_name)
        if action == "allow":
            return Decision.ALLOW, "policy: allow"
        if action == "deny":
            return Decision.DENY, "policy: deny"
        return self._prompt(request)  # action == "ask"

    def _prompt(self, request: PermissionRequest) -> tuple[Decision, str]:
        summary = ", ".join(f"{k}={_short(v)}" for k, v in request.tool_input.items())
        sys.stderr.write(f"\n[policy] {request.tool_name}({summary})\n")
        answer = self.prompt_fn("[policy] allow this action? [y/N] ").strip().lower()
        if answer in {"y", "yes"}:
            return Decision.ALLOW, "policy: approved by human"
        return Decision.DENY, "policy: denied by human"
