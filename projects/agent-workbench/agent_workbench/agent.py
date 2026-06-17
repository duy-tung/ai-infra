"""The agent loop.

This is the heart of the workbench and the thing worth understanding deeply: a
manual agentic loop. We call the model, and as long as it asks for tools, we
run them (through the permission gate), feed the results back, and call again —
until the model is done or we hit the turn limit. Everything else in this
package (registry, permissions, tracing) plugs into this loop.

We drive the loop manually rather than using the SDK's tool runner so we can
gate, log, and time every tool call — which is the whole point of a workbench.
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from typing import Any

from .config import Settings
from .llm import LLMClient
from .permissions import Decision, PermissionGate, PermissionRequest
from .tools.registry import ToolRegistry
from .tracing import RunTotals, Tracer, Usage

SYSTEM_PROMPT = (
    "You are a focused coding agent operating inside a sandboxed working "
    "directory. You have tools to read files, write files, and run shell "
    "commands. Plan briefly, use tools to gather facts before acting, and "
    "verify your work (e.g. read a file back, run a test) before declaring "
    "the task done. Keep responses concise."
)


@dataclass
class AgentResult:
    status: str  # completed | max_turns | error
    final_text: str
    totals: RunTotals
    trace_path: str


def _usage_from_response(response: Any) -> Usage:
    u = getattr(response, "usage", None)
    if u is None:
        return Usage()
    return Usage(
        input_tokens=getattr(u, "input_tokens", 0) or 0,
        output_tokens=getattr(u, "output_tokens", 0) or 0,
        cache_read_input_tokens=getattr(u, "cache_read_input_tokens", 0) or 0,
        cache_creation_input_tokens=getattr(u, "cache_creation_input_tokens", 0) or 0,
    )


class Agent:
    def __init__(
        self,
        settings: Settings,
        registry: ToolRegistry,
        gate: PermissionGate,
        llm: LLMClient | None = None,
        verbose: bool = True,
    ) -> None:
        self.settings = settings
        self.registry = registry
        self.gate = gate
        self.llm = llm or LLMClient(settings)
        self.verbose = verbose

    def _log(self, text: str) -> None:
        if self.verbose:
            sys.stderr.write(text + "\n")

    def run(self, task: str) -> AgentResult:
        tracer = Tracer(self.settings)
        tracer.run_start(task)
        tools = self.registry.api_schemas()
        messages: list[dict[str, Any]] = [{"role": "user", "content": task}]
        final_text = ""
        status = "max_turns"

        try:
            for _turn in range(self.settings.max_turns):
                started = time.monotonic()
                response = self.llm.create(SYSTEM_PROMPT, messages, tools)
                latency = time.monotonic() - started
                stop_reason = getattr(response, "stop_reason", None)
                tracer.llm_call(_usage_from_response(response), stop_reason, latency)

                tool_uses = []
                for block in response.content:
                    btype = getattr(block, "type", None)
                    if btype == "text":
                        final_text = block.text
                        self._log(f"\n[agent] {block.text}")
                    elif btype == "thinking":
                        thinking = getattr(block, "thinking", "")
                        if thinking:
                            self._log(f"[thinking] {thinking}")
                    elif btype == "tool_use":
                        tool_uses.append(block)

                if stop_reason == "end_turn":
                    status = "completed"
                    break

                if stop_reason == "pause_turn":
                    # Server-side tool loop paused; re-send to let it resume.
                    messages.append({"role": "assistant", "content": response.content})
                    continue

                # Preserve the assistant turn verbatim (thinking + tool_use blocks)
                # before adding our tool results — the API requires the pairing.
                messages.append({"role": "assistant", "content": response.content})
                tool_results = [self._handle_tool(tracer, b) for b in tool_uses]
                messages.append({"role": "user", "content": tool_results})
        except Exception as exc:  # noqa: BLE001 - surface the failure, don't crash the harness
            status = "error"
            final_text = f"agent error: {exc}"
            self._log(f"[error] {exc}")

        tracer.run_end(status, final_text)
        self._log(
            f"\n[done] status={status} turns_used calls={tracer.totals.llm_calls} "
            f"tool_calls={tracer.totals.tool_calls} cost=${tracer.totals.cost_usd:.4f} "
            f"trace={tracer.path}"
        )
        return AgentResult(status, final_text, tracer.totals, str(tracer.path))

    def _handle_tool(self, tracer: Tracer, block: Any) -> dict[str, Any]:
        name = block.name
        tool_input = dict(block.input)
        tool = self.registry.get(name)
        mutating = tool.mutating if tool else True  # unknown tools treated as unsafe

        decision, reason = self.gate.check(
            PermissionRequest(tool_name=name, tool_input=tool_input, mutating=mutating)
        )

        started = time.monotonic()
        if decision is Decision.DENY:
            result_content = f"permission denied: {reason}"
            is_error = True
            self._log(f"[tool] {name} DENIED ({reason})")
        else:
            result = self.registry.execute(name, tool_input)
            result_content = result.content
            is_error = result.is_error
            self._log(f"[tool] {name} -> {'error' if is_error else 'ok'}")
        latency = time.monotonic() - started

        tracer.tool_call(
            name=name,
            tool_input=tool_input,
            decision=decision.value,
            reason=reason,
            result_preview=result_content,
            is_error=is_error,
            latency_s=latency,
        )
        return {
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": result_content,
            "is_error": is_error,
        }
