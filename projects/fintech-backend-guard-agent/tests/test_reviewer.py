import json
from types import SimpleNamespace

from fintech_guard.findings import Severity
from fintech_guard.reviewer import LLMReviewer


def _client_returning(text: str):
    resp = SimpleNamespace(content=[SimpleNamespace(type="text", text=text)])
    return SimpleNamespace(messages=SimpleNamespace(create=lambda **kw: resp))


def test_parses_structured_findings():
    payload = json.dumps({"findings": [
        {"category": "txn_boundary", "severity": "high", "message": "split write",
         "file": "pay.py", "line": 12, "suggestion": "wrap in a tx", "confidence": 0.8},
    ]})
    reviewer = LLMReviewer(client=_client_returning(payload))
    findings = reviewer.review("diff")
    assert len(findings) == 1
    f = findings[0]
    assert f.category == "txn_boundary" and f.severity is Severity.HIGH
    assert f.source == "llm" and f.confidence == 0.8


def test_malformed_json_yields_no_findings():
    reviewer = LLMReviewer(client=_client_returning("not json"))
    assert reviewer.review("diff") == []


def test_unknown_severity_falls_back_to_info():
    payload = json.dumps({"findings": [{"category": "x", "severity": "spicy",
                                        "message": "m", "suggestion": "s", "confidence": 0.3}]})
    reviewer = LLMReviewer(client=_client_returning(payload))
    assert reviewer.review("diff")[0].severity is Severity.INFO


def test_diff_is_scrubbed_before_send():
    captured = {}

    def create(**kw):
        captured["messages"] = kw["messages"]
        return SimpleNamespace(content=[SimpleNamespace(type="text", text='{"findings": []}')])

    client = SimpleNamespace(messages=SimpleNamespace(create=create))
    reviewer = LLMReviewer(client=client)
    reviewer.review('API_KEY = "sk-abcdefghijklmnopqrstuvwxyz0123"')
    sent = captured["messages"][0]["content"]
    assert "sk-abcdefghijklmnopqrstuvwxyz0123" not in sent
    assert "[REDACTED" in sent
