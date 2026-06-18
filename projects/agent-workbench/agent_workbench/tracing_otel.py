"""OpenTelemetry GenAI tracing for agent runs.

This is the same observability spine as the JSONL `Tracer`, but emitted as OTel
spans following the GenAI semantic conventions — so the data lands in Jaeger /
Tempo / any OTLP backend and sits next to the rest of your service traces.

Shape of a run:

    agent.run                       (root span — one per task)
    ├── chat claude-opus-4-8        (one per LLM call; token + cost attributes)
    ├── execute_tool write_file     (one per tool call; permission + error status)
    └── ...

The `anthropic` / `opentelemetry` packages are imported lazily so the rest of
the harness works without them. Install with:  pip install -e ".[otel]"

Tests inject an in-memory tracer; production builds an OTLP exporter from
OTEL_EXPORTER_OTLP_ENDPOINT (default http://localhost:4317).
"""

from __future__ import annotations

import os
import time
from contextlib import contextmanager
from typing import Any, Iterator

from .config import Settings
from .tracing import RunTotals, Usage

GENAI_SYSTEM = "anthropic"


def build_tracer(service_name: str, endpoint: str | None = None) -> tuple[Any, Any]:
    """Build a real OTLP-exporting tracer. Returns (tracer, provider).

    The provider is returned so the caller can flush/shutdown it at the end of a
    short-lived process (otherwise batched spans may never be exported)."""
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    endpoint = endpoint or os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
    tracer = trace.get_tracer("agent_workbench", tracer_provider=provider)
    return tracer, provider


class OtelTracer:
    """Emits OTel spans for a run. Mirrors the events the JSONL Tracer records,
    so the agent can drive both side by side."""

    def __init__(
        self,
        settings: Settings,
        service_name: str = "agent-workbench",
        tracer: Any | None = None,
        provider: Any | None = None,
        endpoint: str | None = None,
    ) -> None:
        self.settings = settings
        self._owns_provider = tracer is None
        if tracer is None:
            tracer, provider = build_tracer(service_name, endpoint)
        self._tracer = tracer
        self._provider = provider
        self._root: Any | None = None
        # status/error helpers are pulled in lazily to avoid a hard import.
        from opentelemetry.trace import Status, StatusCode

        self._Status = Status
        self._StatusCode = StatusCode

    @contextmanager
    def run_span(self, task: str) -> Iterator[Any]:
        with self._tracer.start_as_current_span("agent.run") as span:
            span.set_attribute("gen_ai.operation.name", "agent")
            span.set_attribute("gen_ai.system", GENAI_SYSTEM)
            span.set_attribute("gen_ai.request.model", self.settings.model)
            span.set_attribute("agent.task", task[:500])
            self._root = span
            try:
                yield span
            finally:
                self._root = None

    def _child(self, name: str, latency_s: float) -> Any:
        """Create a child span whose timing reflects an operation that already
        completed `latency_s` seconds ago (we measured it, then record it)."""
        end_ns = time.time_ns()
        start_ns = end_ns - int(latency_s * 1e9)
        span = self._tracer.start_span(name, start_time=start_ns)
        return span, end_ns

    def llm_call(self, usage: Usage, stop_reason: str | None, latency_s: float, cost_usd: float) -> None:
        span, end_ns = self._child(f"chat {self.settings.model}", latency_s)
        span.set_attribute("gen_ai.operation.name", "chat")
        span.set_attribute("gen_ai.system", GENAI_SYSTEM)
        span.set_attribute("gen_ai.request.model", self.settings.model)
        span.set_attribute("gen_ai.usage.input_tokens", usage.input_tokens)
        span.set_attribute("gen_ai.usage.output_tokens", usage.output_tokens)
        span.set_attribute("gen_ai.usage.cache_read_input_tokens", usage.cache_read_input_tokens)
        span.set_attribute("gen_ai.usage.cost_usd", round(cost_usd, 6))
        if stop_reason:
            span.set_attribute("gen_ai.response.finish_reasons", [stop_reason])
        span.end(end_time=end_ns)

    def tool_call(
        self,
        name: str,
        decision: str,
        is_error: bool,
        latency_s: float,
    ) -> None:
        span, end_ns = self._child(f"execute_tool {name}", latency_s)
        span.set_attribute("gen_ai.operation.name", "execute_tool")
        span.set_attribute("gen_ai.tool.name", name)
        span.set_attribute("agent.tool.permission", decision)
        if is_error:
            span.set_status(self._Status(self._StatusCode.ERROR))
        span.end(end_time=end_ns)

    def run_end(self, status: str, totals: RunTotals) -> None:
        # Set final attributes on the still-active root span, then flush.
        if self._root is not None:
            self._root.set_attribute("agent.status", status)
            self._root.set_attribute("gen_ai.usage.cost_usd", round(totals.cost_usd, 6))
            self._root.set_attribute("agent.llm_calls", totals.llm_calls)
            self._root.set_attribute("agent.tool_calls", totals.tool_calls)
            if status == "error":
                self._root.set_status(self._Status(self._StatusCode.ERROR))
        if self._owns_provider and self._provider is not None:
            # Flush batched spans before a short-lived process exits.
            self._provider.force_flush()
