"""OTel tracing test — uses an in-memory exporter, no collector needed.

Skipped automatically if opentelemetry isn't installed (pip install -e ".[otel]").
"""

from pathlib import Path
from types import SimpleNamespace

import pytest

pytest.importorskip("opentelemetry")

from opentelemetry import trace  # noqa: E402
from opentelemetry.sdk.trace import TracerProvider  # noqa: E402
from opentelemetry.sdk.trace.export import SimpleSpanProcessor  # noqa: E402
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (  # noqa: E402
    InMemorySpanExporter,
)

from agent_workbench.agent import Agent  # noqa: E402
from agent_workbench.config import Settings  # noqa: E402
from agent_workbench.permissions import PermissionGate  # noqa: E402
from agent_workbench.tools import default_registry  # noqa: E402
from agent_workbench.tracing_otel import OtelTracer  # noqa: E402


def _usage():
    return SimpleNamespace(
        input_tokens=100, output_tokens=20,
        cache_read_input_tokens=0, cache_creation_input_tokens=0,
    )


class ScriptedLLM:
    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = 0

    def create(self, system, messages, tools):
        resp = self._responses[self.calls]
        self.calls += 1
        return resp


def test_otel_emits_run_llm_and_tool_spans(tmp_path: Path):
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    tracer = trace.get_tracer("test", tracer_provider=provider)

    workdir = tmp_path / "work"
    workdir.mkdir()
    settings = Settings(model="claude-opus-4-8", trace_dir=tmp_path / "traces")
    otel = OtelTracer(settings, tracer=tracer)

    responses = [
        SimpleNamespace(
            stop_reason="tool_use", usage=_usage(),
            content=[SimpleNamespace(type="tool_use", name="write_file", id="t1",
                                     input={"path": "out.txt", "content": "hi"})],
        ),
        SimpleNamespace(
            stop_reason="end_turn", usage=_usage(),
            content=[SimpleNamespace(type="text", text="done")],
        ),
    ]

    agent = Agent(settings, default_registry(workdir), PermissionGate(mode="auto"),
                  llm=ScriptedLLM(responses), verbose=False, otel=otel)
    result = agent.run("write hi to out.txt")
    assert result.status == "completed"

    spans = {s.name: s for s in exporter.get_finished_spans()}
    assert "agent.run" in spans
    assert "chat claude-opus-4-8" in spans
    assert "execute_tool write_file" in spans

    chat = spans["chat claude-opus-4-8"]
    assert chat.attributes["gen_ai.usage.input_tokens"] == 100
    assert chat.attributes["gen_ai.system"] == "anthropic"
    assert "gen_ai.usage.cost_usd" in chat.attributes

    root = spans["agent.run"]
    assert root.attributes["agent.status"] == "completed"
