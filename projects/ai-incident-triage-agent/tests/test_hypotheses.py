import json
from types import SimpleNamespace

from incident_triage.correlate import correlate
from incident_triage.hypotheses import (
    Hypothesis,
    HypothesisGenerator,
    baseline_hypothesis,
    merge_hypotheses,
)
from incident_triage.models import IncidentBundle

BUNDLE = {
    "alert": {"service": "payments", "fired_at": "2026-06-18T10:00:00Z", "metric": "error_rate", "value": 0.4},
    "deploys": [{"id": "D2", "service": "payments", "at": "2026-06-18T09:58:00Z", "summary": "float balance"}],
    "logs": [{"at": "2026-06-18T09:59:00Z", "level": "error", "service": "payments", "message": "balance mismatch 1"}],
}


def _corr():
    return correlate(IncidentBundle.from_dict(BUNDLE))


def test_baseline_hypothesis_points_at_suspect():
    h = baseline_hypothesis(_corr())
    assert h is not None and "D2" in h.root_cause and h.source == "heuristic"


def test_baseline_none_without_suspect():
    d = dict(BUNDLE, deploys=[])
    assert baseline_hypothesis(correlate(IncidentBundle.from_dict(d))) is None


def _client_returning(text):
    resp = SimpleNamespace(content=[SimpleNamespace(type="text", text=text)])
    return SimpleNamespace(messages=SimpleNamespace(create=lambda **kw: resp))


def test_generator_parses_structured_hypotheses():
    payload = json.dumps({"hypotheses": [
        {"root_cause": "float rounding in balance", "confidence": 0.7,
         "evidence": "diff switches to float64", "suggested_queries": ["check ledger sums"]},
    ]})
    gen = HypothesisGenerator(client=_client_returning(payload))
    hyps = gen.generate(_corr(), IncidentBundle.from_dict(BUNDLE))
    assert len(hyps) == 1 and hyps[0].source == "llm" and hyps[0].confidence == 0.7


def test_merge_orders_by_confidence():
    base = Hypothesis("baseline", 0.6, source="heuristic")
    llm = [Hypothesis("a", 0.9, source="llm"), Hypothesis("b", 0.3, source="llm")]
    merged = merge_hypotheses(base, llm)
    assert [h.confidence for h in merged] == [0.9, 0.6, 0.3]
