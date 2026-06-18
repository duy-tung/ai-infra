"""OTel tracing test — in-memory exporter, no collector. Skips if opentelemetry absent."""

import pytest

pytest.importorskip("opentelemetry")

from opentelemetry import trace  # noqa: E402
from opentelemetry.sdk.trace import TracerProvider  # noqa: E402
from opentelemetry.sdk.trace.export import SimpleSpanProcessor  # noqa: E402
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (  # noqa: E402
    InMemorySpanExporter,
)

from fintech_guard.pipeline import Guard  # noqa: E402
from fintech_guard.tracing import OtelTracer, cost_of  # noqa: E402

RISKY = "+++ b/wallet.go\n@@ -0,0 +1,1 @@\n+    Balance float64\n"


def _tracer():
    exp = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exp))
    return trace.get_tracer("test", tracer_provider=provider), exp


class FakeReviewer:
    model = "claude-opus-4-8"

    def __init__(self):
        self.last_usage = {"input_tokens": 1000, "output_tokens": 200}

    def review(self, text, already_flagged=None):
        return []


def test_cost_of():
    # 1M in @ $5 + 1M out @ $25 = $30
    assert round(cost_of("claude-opus-4-8", 1_000_000, 1_000_000), 2) == 30.00


def test_static_only_emits_review_span():
    tracer, exp = _tracer()
    Guard(reviewer=None, otel=OtelTracer(tracer=tracer)).review_diff(RISKY)
    names = [s.name for s in exp.get_finished_spans()]
    assert "guard.review" in names
    root = next(s for s in exp.get_finished_spans() if s.name == "guard.review")
    assert root.attributes["guard.verdict"] == "advisory"
    assert root.attributes["guard.findings.high"] == 1


def test_llm_review_emits_chat_span_with_cost():
    tracer, exp = _tracer()
    guard = Guard(reviewer=FakeReviewer(), otel=OtelTracer(tracer=tracer))
    guard.review_diff(RISKY)
    spans = {s.name: s for s in exp.get_finished_spans()}
    assert "guard.review" in spans and "chat claude-opus-4-8" in spans
    chat = spans["chat claude-opus-4-8"]
    assert chat.attributes["gen_ai.usage.input_tokens"] == 1000
    assert chat.attributes["gen_ai.usage.cost_usd"] > 0
    assert spans["guard.review"].attributes["guard.used_llm"] is True
