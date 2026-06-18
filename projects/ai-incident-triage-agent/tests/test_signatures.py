from incident_triage.models import LogLine
from incident_triage.signatures import extract_signatures, normalize


def test_normalize_numbers():
    assert normalize("user 123 not found") == "user <n> not found"


def test_normalize_uuid():
    out = normalize("ctx 550e8400-e29b-41d4-a716-446655440000 failed")
    assert "<uuid>" in out and "550e8400" not in out


def test_normalize_hex():
    assert "<hex>" in normalize("addr 0xdeadbeef invalid")


def _log(at, msg, level="error", service="payments"):
    return LogLine.from_dict({"at": at, "level": level, "service": service, "message": msg})


def test_extract_clusters_by_signature():
    logs = [
        _log("2026-06-18T10:00:00Z", "balance mismatch for account 1"),
        _log("2026-06-18T10:00:05Z", "balance mismatch for account 2"),
        _log("2026-06-18T10:00:10Z", "connection refused"),
    ]
    sigs = extract_signatures(logs)
    assert sigs[0].count == 2  # the two 'balance mismatch' lines collapse
    assert "balance mismatch for account <n>" == sigs[0].pattern
    assert sigs[0].services == {"payments"}


def test_extract_ignores_non_errors():
    logs = [_log("2026-06-18T10:00:00Z", "all good", level="info")]
    assert extract_signatures(logs) == []
