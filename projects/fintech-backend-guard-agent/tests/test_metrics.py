"""Prometheus metrics test — skips if prometheus_client isn't installed."""

import pytest

pytest.importorskip("prometheus_client")

from fintech_guard.metrics import Metrics  # noqa: E402
from fintech_guard.pipeline import Guard  # noqa: E402

RISKY = "+++ b/wallet.go\n@@ -0,0 +1,1 @@\n+    Balance float64\n"


def test_records_review_and_findings():
    m = Metrics()
    m.record_review("advisory", {"high": 1, "low": 0}, duration_s=0.2)
    text = m.render().decode("utf-8")
    assert 'fintech_guard_reviews_total{verdict="advisory"} 1.0' in text
    assert 'fintech_guard_findings_total{severity="high"} 1.0' in text


def test_records_llm_cost():
    m = Metrics()
    m.record_llm("claude-opus-4-8", 1_000_000, 0)  # $5 input
    text = m.render().decode("utf-8")
    assert "fintech_guard_llm_calls_total 1.0" in text
    assert "fintech_guard_cost_usd_total 5.0" in text


def test_pipeline_records_review_metric():
    m = Metrics()
    Guard(reviewer=None, metrics=m).review_diff(RISKY)
    text = m.render().decode("utf-8")
    # money_float is HIGH; advisory verdict by default
    assert 'fintech_guard_reviews_total{verdict="advisory"} 1.0' in text
    assert 'fintech_guard_findings_total{severity="high"} 1.0' in text


def test_write_textfile(tmp_path):
    m = Metrics()
    m.record_review("pass", {}, 0.1)
    out = tmp_path / "guard.prom"
    m.write_textfile(str(out))
    assert "fintech_guard_reviews_total" in out.read_text(encoding="utf-8")
