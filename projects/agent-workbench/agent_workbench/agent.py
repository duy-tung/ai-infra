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
from contextlib import nullcontext
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from .config import Settings
from .llm import LLMClient
from .permissions import Decision, PermissionGate, PermissionRequest
from .tools.registry import ToolRegistry
from .tracing import RunTotals, Tracer, Usage

if TYPE_CHECKING:  # all optional — imported for type hints only
    from .audit import AuditLog
    from .governor import Governor
    from .metrics import Metrics
    from .redaction import Redactor
    from .tracing_otel import OtelTracer

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
        otel: "OtelTracer | None" = None,
        governor: "Governor | None" = None,
        audit: "AuditLog | None" = None,
        metrics: "Metrics | None" = None,
        redactor: "Redactor | None" = None,
    ) -> None:
        self.settings = settings
        self.registry = registry
        self.gate = gate
        self.llm = llm or LLMClient(settings)
        self.verbose = verbose
        # All optional (default None = behavior unchanged):
        self.otel = otel            # OpenTelemetry spans
        self.governor = governor    # cost/token/tool-call budget + kill switch
        self.audit = audit          # append-only hash-chained audit log
        self.metrics = metrics      # Prometheus metrics
        self.redactor = redactor    # PII/secrets scrubbing on the trace
        self._budget_reason = ""

    def _log(self, text: str) -> None:
        if self.verbose:
            sys.stderr.write(text + "\n")

    def run(self, task: str) -> AgentResult:
        tracer = Tracer(self.settings, redactor=self.redactor)
        tracer.run_start(task)
        tools = self.registry.api_schemas()
        messages: list[dict[str, Any]] = [{"role": "user", "content": task}]
        final_text = ""
        status = "max_turns"

        # Wrap the whole run in an OTel root span when enabled (no-op otherwise).
        run_ctx = self.otel.run_span(task) if self.otel else nullcontext()
        with run_ctx:
            try:
                for _turn in range(self.settings.max_turns):
                    started = time.monotonic()
                    response = self.llm.create(SYSTEM_PROMPT, messages, tools)
                    latency = time.monotonic() - started
                    stop_reason = getattr(response, "stop_reason", None)
                    usage = _usage_from_response(response)
                    cost = tracer.llm_call(usage, stop_reason, latency)
                    if self.otel:
                        self.otel.llm_call(usage, stop_reason, latency, cost)
                    if self.metrics:
                        self.metrics.record_llm(latency, cost)
                    if self._over_budget(tracer):
                        status, final_text = "budget_exceeded", self._budget_reason
                        break

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
                    if self._over_budget(tracer):
                        status, final_text = "budget_exceeded", self._budget_reason
                        break
            except Exception as exc:  # noqa: BLE001 - surface the failure, don't crash the harness
                status = "error"
                final_text = f"agent error: {exc}"
                self._log(f"[error] {exc}")

            if self.metrics:
                self.metrics.record_run(status)
            tracer.run_end(status, final_text)
            if self.otel:
                self.otel.run_end(status, tracer.totals)
        self._log(
            f"\n[done] status={status} turns_used calls={tracer.totals.llm_calls} "
            f"tool_calls={tracer.totals.tool_calls} cost=${tracer.totals.cost_usd:.4f} "
            f"trace={tracer.path}"
        )
        return AgentResult(status, final_text, tracer.totals, str(tracer.path))

    def _over_budget(self, tracer: Tracer) -> bool:
        """Ask the governor whether the run has blown its budget (kill switch)."""
        if not self.governor:
            return False
        status = self.governor.check(tracer.totals)
        if status.exceeded:
            self._budget_reason = f"stopped: {status.reason}"
            self._log(f"[governor] {status.reason}")
            return True
        return False

    def _audit_target(self, tool_input: dict[str, Any]) -> str:
        text = ", ".join(f"{k}={str(v)[:80]}" for k, v in tool_input.items())
        return self.redactor.redact(text) if self.redactor else text

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
        if self.otel:
            self.otel.tool_call(name=name, decision=decision.value, is_error=is_error, latency_s=latency)
        if self.metrics:
            self.metrics.record_tool(name, is_error, latency)
        if self.audit and mutating:
            # Audit every state-changing action and the decision that gated it.
            self.audit.record(
                action=name,
                target=self._audit_target(tool_input),
                decision=decision.value,
                reason=reason,
                extra={"is_error": is_error},
            )
        return {
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": result_content,
            "is_error": is_error,
        }
