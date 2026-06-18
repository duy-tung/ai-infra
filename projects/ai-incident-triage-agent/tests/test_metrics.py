"""Prometheus metrics test — skips if prometheus_client isn't installed."""

import pytest

pytest.importorskip("prometheus_client")

from incident_triage.metrics import Metrics  # noqa: E402
from incident_triage.models import IncidentBundle  # noqa: E402
from incident_triage.pipeline import Triage  # noqa: E402

BUNDLE = {
    "alert": {"service": "payments", "fired_at": "2026-06-18T10:00:00Z", "metric": "error_rate", "value": 0.4},
    "deploys": [{"id": "D2", "service": "payments", "at": "2026-06-18T09:58:00Z", "summary": "x"}],
    "logs": [{"at": "2026-06-18T09:59:00Z", "level": "error", "service": "payments", "message": "boom 1"}],
}


def test_records_triage_outcome():
    m = Metrics()
    m.record_triage(has_suspect=True, top_confidence=0.8, duration_s=0.1)
    text = m.render().decode("utf-8")
    assert 'incident_triage_runs_total{outcome="has_suspect"} 1.0' in text


def test_records_llm_cost():
    m = Metrics()
    m.record_llm("claude-opus-4-8", 0, 1_000_000)  # $25 output
    text = m.render().decode("utf-8")
    assert "incident_triage_llm_calls_total 1.0" in text
    assert "incident_triage_cost_usd_total 25.0" in text


def test_pipeline_records_metric():
    m = Metrics()
    Triage(generator=None, metrics=m).triage(IncidentBundle.from_dict(BUNDLE))
    text = m.render().decode("utf-8")
    assert 'incident_triage_runs_total{outcome="has_suspect"} 1.0' in text
