"""Sprint 3 integration: governor kill switch + audit log through the agent loop."""

from pathlib import Path
from types import SimpleNamespace

from agent_workbench.agent import Agent
from agent_workbench.audit import verify
from agent_workbench.audit import AuditLog
from agent_workbench.config import Settings
from agent_workbench.governor import Budget, Governor
from agent_workbench.permissions import PermissionGate
from agent_workbench.tools import default_registry


def _usage():
    return SimpleNamespace(input_tokens=100, output_tokens=20,
                           cache_read_input_tokens=0, cache_creation_input_tokens=0)


class ScriptedLLM:
    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = 0

    def create(self, system, messages, tools):
        # Repeat the last response if the loop asks for more (shouldn't, with a budget).
        resp = self._responses[min(self.calls, len(self._responses) - 1)]
        self.calls += 1
        return resp


def _tool_use(tool_id="t1"):
    return SimpleNamespace(
        stop_reason="tool_use", usage=_usage(),
        content=[SimpleNamespace(type="tool_use", name="write_file", id=tool_id,
                                 input={"path": "out.txt", "content": "hi"})],
    )


def _end(text="done"):
    return SimpleNamespace(stop_reason="end_turn", usage=_usage(),
                           content=[SimpleNamespace(type="text", text=text)])


def test_governor_kills_run_over_cost(tmp_path: Path):
    workdir = tmp_path / "work"; workdir.mkdir()
    settings = Settings(trace_dir=tmp_path / "traces")
    # One LLM call costs ~ $0.001 (100 in @ $5/1M + 20 out @ $25/1M); budget is below that.
    governor = Governor(Budget(max_usd=0.0001))
    agent = Agent(settings, default_registry(workdir), PermissionGate(mode="auto"),
                  llm=ScriptedLLM([_tool_use(), _end()]), verbose=False, governor=governor)

    result = agent.run("write hi to out.txt")
    assert result.status == "budget_exceeded"
    assert "cost" in result.final_text
    # The run was killed after the first LLM call, before the tool executed.
    assert not (workdir / "out.txt").exists()


def test_audit_log_records_mutating_tool(tmp_path: Path):
    workdir = tmp_path / "work"; workdir.mkdir()
    audit_path = tmp_path / "audit.jsonl"
    settings = Settings(trace_dir=tmp_path / "traces")
    agent = Agent(settings, default_registry(workdir), PermissionGate(mode="auto"),
                  llm=ScriptedLLM([_tool_use(), _end()]), verbose=False,
                  audit=AuditLog(audit_path))

    result = agent.run("write hi to out.txt")
    assert result.status == "completed"
    assert (workdir / "out.txt").read_text() == "hi"

    ok, msg = verify(audit_path)
    assert ok, msg
    body = audit_path.read_text(encoding="utf-8")
    assert "write_file" in body
    assert '"decision": "allow"' in body
