from fintech_guard.findings import Finding, Severity
from fintech_guard.pipeline import Guard

RISKY_DIFF = (
    "diff --git a/wallet.go b/wallet.go\n"
    "--- a/wallet.go\n+++ b/wallet.go\n@@ -0,0 +1,3 @@\n"
    "+type Wallet struct {\n+\tBalance float64\n+}\n"
)


class FakeReviewer:
    def __init__(self, findings):
        self._findings = findings
        self.seen_flagged = None

    def review(self, text, already_flagged=None):
        self.seen_flagged = already_flagged
        return self._findings


def test_static_only_pipeline_flags_money_float():
    report = Guard(reviewer=None).review_diff(RISKY_DIFF)
    cats = {f.category for f in report.findings}
    assert "money_float" in cats
    assert report.used_llm is False
    assert report.gate_result.would_block is True  # HIGH severity


def test_pipeline_merges_llm_findings_and_passes_context():
    llm_finding = Finding("txn_boundary", Severity.MEDIUM, "split write", file="wallet.go", line=2, source="llm")
    reviewer = FakeReviewer([llm_finding])
    report = Guard(reviewer=reviewer).review_diff(RISKY_DIFF)
    cats = {f.category for f in report.findings}
    assert {"money_float", "txn_boundary"} <= cats
    assert report.used_llm is True
    # static categories are passed to the reviewer so it can focus elsewhere
    assert "money_float" in (reviewer.seen_flagged or [])


def test_migration_sql_param_is_reviewed():
    report = Guard(reviewer=None).review_diff(
        "diff --git a/x.py b/x.py\n+++ b/x.py\n@@ -0,0 +1,1 @@\n+x = 1\n",
        migration_sql="CREATE INDEX idx ON tx (a);",
    )
    assert "migration_index_lock" in {f.category for f in report.findings}


def test_advisory_does_not_block():
    report = Guard(reviewer=None, advisory=True).review_diff(RISKY_DIFF)
    assert report.gate_result.blocked is False


def test_enforce_blocks_on_high():
    report = Guard(reviewer=None, advisory=False, threshold=Severity.HIGH).review_diff(RISKY_DIFF)
    assert report.gate_result.blocked is True
