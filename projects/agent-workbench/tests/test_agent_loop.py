"""End-to-end test of the agent loop with a scripted fake LLM.

No network, no API key: we feed the loop a canned sequence of responses (call a
tool, then finish) and assert the harness wired tool calls, permissions, and
tracing together correctly. This is the cheapest possible regression test for
the loop itself.
"""

from pathlib import Path
from types import SimpleNamespace

from agent_workbench.agent import Agent
from agent_workbench.config import Settings
from agent_workbench.permissions import PermissionGate
from agent_workbench.tools import default_registry


def _usage():
    return SimpleNamespace(
        input_tokens=100,
        output_tokens=20,
        cache_read_input_tokens=0,
        cache_creation_input_tokens=0,
    )


class ScriptedLLM:
    """Returns pre-baked responses in order, ignoring the actual prompt."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = 0

    def create(self, system, messages, tools):
        resp = self._responses[self.calls]
        self.calls += 1
        return resp


def test_loop_runs_tool_then_completes(tmp_path: Path):
    workdir = tmp_path / "work"
    workdir.mkdir()
    trace_dir = tmp_path / "traces"

    responses = [
        SimpleNamespace(
            stop_reason="tool_use",
            usage=_usage(),
            content=[
                SimpleNamespace(
                    type="tool_use",
                    name="write_file",
                    id="tool_1",
                    input={"path": "out.txt", "content": "hello world"},
                )
            ],
        ),
        SimpleNamespace(
            stop_reason="end_turn",
            usage=_usage(),
            content=[SimpleNamespace(type="text", text="Done — wrote out.txt.")],
        ),
    ]

    settings = Settings(model="claude-opus-4-8", trace_dir=trace_dir)
    registry = default_registry(workdir)
    gate = PermissionGate(mode="auto")
    agent = Agent(settings, registry, gate, llm=ScriptedLLM(responses), verbose=False)

    result = agent.run("write hello world to out.txt")

    assert result.status == "completed"
    assert "Done" in result.final_text
    assert (workdir / "out.txt").read_text() == "hello world"
    assert result.totals.llm_calls == 2
    assert result.totals.tool_calls == 1
    assert result.totals.cost_usd > 0


def test_readonly_mode_blocks_write(tmp_path: Path):
    workdir = tmp_path / "work"
    workdir.mkdir()

    responses = [
        SimpleNamespace(
            stop_reason="tool_use",
            usage=_usage(),
            content=[
                SimpleNamespace(
                    type="tool_use",
                    name="write_file",
                    id="tool_1",
                    input={"path": "out.txt", "content": "nope"},
                )
            ],
        ),
        SimpleNamespace(
            stop_reason="end_turn",
            usage=_usage(),
            content=[SimpleNamespace(type="text", text="I was blocked from writing.")],
        ),
    ]

    settings = Settings(trace_dir=tmp_path / "traces")
    registry = default_registry(workdir)
    gate = PermissionGate(mode="readonly")
    agent = Agent(settings, registry, gate, llm=ScriptedLLM(responses), verbose=False)

    result = agent.run("try to write a file")

    assert result.status == "completed"
    assert not (workdir / "out.txt").exists()  # the write was denied by the gate
