"""OpenTelemetry tracing + cost for a guard run.

Mirrors the agent-workbench OTel spine so all three projects emit the same
GenAI-convention spans. One run looks like:

    guard.review                 (root — files changed, verdict, counts)
    └── chat <model>             (only when --llm; tokens + cost attributes)

The `opentelemetry` packages are imported lazily (optional extra: ".[otel]").
Tests inject an in-memory tracer; production builds an OTLP exporter from
OTEL_EXPORTER_OTLP_ENDPOINT (default http://localhost:4317).

In a real monorepo this and the agent-workbench tracer would be one shared lib;
kept local so this repo is self-contained.
"""

from __future__ import annotations

import os
import time
from contextlib import contextmanager
from typing import Any, Iterator

# USD per 1,000,000 tokens (cached pricing).
PRICING = {
    "claude-opus-4-8": {"input": 5.00, "output": 25.00},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    "claude-haiku-4-5": {"input": 1.00, "output": 5.00},
}
GENAI_SYSTEM = "anthropic"


def cost_of(model: str, input_tokens: int, output_tokens: int) -> float:
    p = PRICING.get(model, {"input": 0.0, "output": 0.0})
    return input_tokens * p["input"] / 1_000_000 + output_tokens * p["output"] / 1_000_000


def build_tracer(service_name: str, endpoint: str | None = None) -> tuple[Any, Any]:
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    endpoint = endpoint or os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
    return trace.get_tracer("fintech_guard", tracer_provider=provider), provider


class OtelTracer:
    def __init__(self, service_name: str = "fintech-guard", tracer: Any | None = None,
                 provider: Any | None = None, endpoint: str | None = None) -> None:
        self._owns_provider = tracer is None
        if tracer is None:
            tracer, provider = build_tracer(service_name, endpoint)
        self._tracer = tracer
        self._provider = provider
        self._root: Any | None = None
        from opentelemetry.trace import Status, StatusCode

        self._Status = Status
        self._StatusCode = StatusCode

    @contextmanager
    def review_span(self, files_changed: int) -> Iterator[Any]:
        with self._tracer.start_as_current_span("guard.review") as span:
            span.set_attribute("gen_ai.operation.name", "review")
            span.set_attribute("gen_ai.system", GENAI_SYSTEM)
            span.set_attribute("guard.files_changed", files_changed)
            self._root = span
            try:
                yield span
            finally:
                self._root = None
                if self._owns_provider and self._provider is not None:
                    self._provider.force_flush()

    def llm_span(self, model: str, input_tokens: int, output_tokens: int, latency_s: float) -> None:
        end_ns = time.time_ns()
        span = self._tracer.start_span(f"chat {model}", start_time=end_ns - int(latency_s * 1e9))
        span.set_attribute("gen_ai.operation.name", "chat")
        span.set_attribute("gen_ai.system", GENAI_SYSTEM)
        span.set_attribute("gen_ai.request.model", model)
        span.set_attribute("gen_ai.usage.input_tokens", input_tokens)
        span.set_attribute("gen_ai.usage.output_tokens", output_tokens)
        span.set_attribute("gen_ai.usage.cost_usd", round(cost_of(model, input_tokens, output_tokens), 6))
        span.end(end_time=end_ns)

    def set_result(self, verdict: str, counts: dict[str, int], used_llm: bool) -> None:
        if self._root is None:
            return
        self._root.set_attribute("guard.verdict", verdict)
        self._root.set_attribute("guard.used_llm", used_llm)
        for sev, n in counts.items():
            if n:
                self._root.set_attribute(f"guard.findings.{sev}", n)
