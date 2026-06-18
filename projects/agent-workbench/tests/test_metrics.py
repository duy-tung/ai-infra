"""Metrics test — skipped if prometheus_client isn't installed (pip install -e ".[metrics]")."""

import pytest

pytest.importorskip("prometheus_client")

from agent_workbench.metrics import Metrics  # noqa: E402


def test_metrics_record_and_render():
    m = Metrics()
    m.record_llm(latency_s=0.5, cost_usd=0.01)
    m.record_tool("write_file", is_error=False, latency_s=0.02)
    m.record_tool("run_shell", is_error=True, latency_s=0.03)
    m.record_run("completed")

    text = m.render().decode("utf-8")
    assert "agent_llm_calls_total 1.0" in text
    assert 'agent_tool_calls_total{outcome="ok",tool="write_file"} 1.0' in text
    assert 'agent_tool_calls_total{outcome="error",tool="run_shell"} 1.0' in text
    assert 'agent_runs_total{status="completed"} 1.0' in text
    assert "agent_cost_usd_total 0.01" in text


def test_write_textfile(tmp_path):
    m = Metrics()
    m.record_run("completed")
    out = tmp_path / "agent.prom"
    m.write_textfile(str(out))
    assert "agent_runs_total" in out.read_text(encoding="utf-8")
