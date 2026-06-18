from incident_triage.correlate import correlate
from incident_triage.models import IncidentBundle

BUNDLE = {
    "alert": {"name": "HighErrorRate", "service": "payments", "fired_at": "2026-06-18T10:00:00Z",
              "metric": "error_rate", "value": 0.4, "threshold": 0.05},
    "deploys": [
        {"id": "D1", "service": "search", "at": "2026-06-18T09:10:00Z", "summary": "ranking"},
        {"id": "D2", "service": "payments", "at": "2026-06-18T09:58:00Z", "summary": "float balance"}
    ],
    "logs": [
        {"at": "2026-06-18T09:59:00Z", "level": "error", "service": "payments", "message": "balance mismatch 1"},
        {"at": "2026-06-18T09:59:30Z", "level": "error", "service": "payments", "message": "balance mismatch 2"}
    ],
    "owners": {"payments": "team-payments"},
}


def _bundle(d=BUNDLE):
    return IncidentBundle.from_dict(d)


def test_closest_same_service_deploy_is_top_suspect():
    c = correlate(_bundle())
    assert c.top_suspect.id == "D2"
    assert c.rollback.id == "D2"


def test_owner_resolved():
    assert correlate(_bundle()).owner == "team-payments"


def test_blast_radius_from_error_logs():
    assert correlate(_bundle()).blast_radius == {"payments"}


def test_timeline_is_time_sorted_and_has_alert():
    tl = correlate(_bundle()).timeline
    ats = [e.at for e in tl]
    assert ats == sorted(ats)
    assert any(e.kind == "alert" for e in tl)


def test_no_deploy_in_window_yields_no_suspect():
    d = dict(BUNDLE, deploys=[{"id": "OLD", "service": "payments", "at": "2026-06-18T08:00:00Z"}])
    c = correlate(_bundle(d))
    assert c.suspect_deploys == []
    assert c.top_suspect is None and c.rollback is None


def test_confidence_in_range():
    c = correlate(_bundle())
    assert 0.0 < c.confidence <= 0.99
