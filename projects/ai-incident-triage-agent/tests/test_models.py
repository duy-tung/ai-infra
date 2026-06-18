from datetime import timezone

from incident_triage.models import IncidentBundle, parse_ts


def test_parse_ts_z_suffix():
    dt = parse_ts("2026-06-18T10:00:00Z")
    assert dt.tzinfo is not None and dt.utcoffset().total_seconds() == 0


def test_parse_ts_naive_assumed_utc():
    dt = parse_ts("2026-06-18T10:00:00")
    assert dt.tzinfo == timezone.utc


def test_bundle_from_dict():
    b = IncidentBundle.from_dict({
        "alert": {"service": "payments", "fired_at": "2026-06-18T10:00:00Z", "metric": "error_rate"},
        "deploys": [{"id": "D1", "service": "payments", "at": "2026-06-18T09:58:00Z"}],
        "logs": [{"at": "2026-06-18T09:59:00Z", "level": "error", "service": "payments", "message": "boom"}],
        "owners": {"payments": "team-pay"},
    })
    assert b.alert.service == "payments"
    assert len(b.deploys) == 1 and b.deploys[0].id == "D1"
    assert b.logs[0].level == "error"
    assert b.owners["payments"] == "team-pay"
