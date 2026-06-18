import json

from incident_triage.hypotheses import Hypothesis
from incident_triage.models import IncidentBundle
from incident_triage.pipeline import Triage

BUNDLE = {
    "alert": {"service": "payments", "fired_at": "2026-06-18T10:00:00Z", "metric": "error_rate", "value": 0.4},
    "deploys": [{"id": "D2", "service": "payments", "at": "2026-06-18T09:58:00Z", "summary": "float balance"}],
    "logs": [{"at": "2026-06-18T09:59:00Z", "level": "error", "service": "payments", "message": "balance mismatch 1"}],
    "owners": {"payments": "team-payments"},
}


class FakeGenerator:
    def __init__(self, hyps):
        self._hyps = hyps

    def generate(self, correlation, bundle):
        return self._hyps


def _bundle():
    return IncidentBundle.from_dict(BUNDLE)


def test_static_only_triage_uses_baseline():
    report = Triage(generator=None).triage(_bundle())
    assert report.used_llm is False
    assert report.top is not None and report.top.source == "heuristic"
    assert "D2" in report.top.root_cause


def test_triage_merges_llm_hypotheses():
    high = Hypothesis("connection pool exhausted", 0.95, source="llm")
    report = Triage(generator=FakeGenerator([high])).triage(_bundle())
    assert report.used_llm is True
    assert report.top.confidence == 0.95  # llm hypothesis outranks baseline


def test_markdown_is_read_only_and_has_rollback():
    md = Triage(generator=None).triage(_bundle()).markdown()
    assert "read-only" in md.lower()
    assert "Rollback candidate (advisory)" in md
    assert "team-payments" in md


def test_json_shape():
    data = json.loads(Triage(generator=None).triage(_bundle()).json())
    assert data["rollback_candidate"]["id"] == "D2"
    assert data["owner"] == "team-payments"
    assert data["hypotheses"] and "root_cause" in data["hypotheses"][0]
