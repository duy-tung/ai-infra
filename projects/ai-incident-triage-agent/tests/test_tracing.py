"""OTel tracing test — in-memory exporter. Skips if opentelemetry absent."""

import pytest

pytest.importorskip("opentelemetry")

from opentelemetry import trace  # noqa: E402
from opentelemetry.sdk.trace import TracerProvider  # noqa: E402
from opentelemetry.sdk.trace.export import SimpleSpanProcessor  # noqa: E402
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (  # noqa: E402
    InMemorySpanExporter,
)

from incident_triage.models import IncidentBundle  # noqa: E402
from incident_triage.pipeline import Triage  # noqa: E402
from incident_triage.tracing import OtelTracer, cost_of  # noqa: E402

BUNDLE = {
    "alert": {"service": "payments", "fired_at": "2026-06-18T10:00:00Z", "metric": "error_rate", "value": 0.4},
    "deploys": [{"id": "D2", "service": "payments", "at": "2026-06-18T09:58:00Z", "summary": "float balance"}],
    "logs": [{"at": "2026-06-18T09:59:00Z", "level": "error", "service": "payments", "message": "balance mismatch 1"}],
}


def _tracer():
    exp = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exp))
    return trace.get_tracer("test", tracer_provider=provider), exp


class FakeGenerator:
    model = "claude-opus-4-8"

    def __init__(self):
        self.last_usage = {"input_tokens": 2000, "output_tokens": 300}

    def generate(self, correlation, bundle):
        return []


def test_cost_of():
    assert round(cost_of("claude-opus-4-8", 1_000_000, 1_000_000), 2) == 30.00


def test_static_only_emits_triage_span():
    tracer, exp = _tracer()
    Triage(generator=None, otel=OtelTracer(tracer=tracer)).triage(IncidentBundle.from_dict(BUNDLE))
    root = next(s for s in exp.get_finished_spans() if s.name == "triage.run")
    assert root.attributes["incident.service"] == "payments"
    assert root.attributes["triage.suspect_deploys"] == 1
    assert root.attributes["triage.used_llm"] is False


def test_llm_emits_chat_span_with_cost():
    tracer, exp = _tracer()
    Triage(generator=FakeGenerator(), otel=OtelTracer(tracer=tracer)).triage(IncidentBundle.from_dict(BUNDLE))
    spans = {s.name: s for s in exp.get_finished_spans()}
    assert "triage.run" in spans and "chat claude-opus-4-8" in spans
    assert spans["chat claude-opus-4-8"].attributes["gen_ai.usage.input_tokens"] == 2000
    assert spans["chat claude-opus-4-8"].attributes["gen_ai.usage.cost_usd"] > 0
    assert spans["triage.run"].attributes["triage.used_llm"] is True
