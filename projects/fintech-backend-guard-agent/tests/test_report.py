from fintech_guard.findings import Finding, Severity
from fintech_guard.report import gate, merge_findings, severity_counts, to_json, to_markdown


def test_merge_dedupes_static_wins_on_tie():
    static = [Finding("pii_secret", Severity.CRITICAL, "static", file="a.py", line=1, source="static")]
    llm = [Finding("pii_secret", Severity.MEDIUM, "llm", file="a.py", line=1, source="llm", confidence=0.5)]
    merged = merge_findings(static, llm)
    assert len(merged) == 1
    assert merged[0].source == "static" and merged[0].severity is Severity.CRITICAL


def test_merge_keeps_higher_severity():
    static = [Finding("x", Severity.LOW, "s", file="a", line=1)]
    llm = [Finding("x", Severity.HIGH, "l", file="a", line=1, source="llm")]
    merged = merge_findings(static, llm)
    assert merged[0].severity is Severity.HIGH


def test_severity_counts():
    f = [Finding("a", Severity.HIGH, "m"), Finding("b", Severity.HIGH, "m"), Finding("c", Severity.LOW, "m")]
    counts = severity_counts(f)
    assert counts["high"] == 2 and counts["low"] == 1


def test_gate_advisory_never_blocks_but_reports_would_block():
    f = [Finding("x", Severity.CRITICAL, "m")]
    g = gate(f, threshold=Severity.HIGH, advisory=True)
    assert g.blocked is False and g.would_block is True


def test_gate_enforce_blocks_at_threshold():
    f = [Finding("x", Severity.HIGH, "m")]
    g = gate(f, threshold=Severity.HIGH, advisory=False)
    assert g.blocked is True


def test_gate_enforce_passes_below_threshold():
    f = [Finding("x", Severity.MEDIUM, "m")]
    g = gate(f, threshold=Severity.HIGH, advisory=False)
    assert g.blocked is False


def test_render_markdown_and_json():
    f = [Finding("money_float", Severity.HIGH, "float used", file="w.go", line=3, suggestion="use cents")]
    g = gate(f, advisory=True)
    md = to_markdown(f, g)
    assert "money_float" in md and "use cents" in md
    import json
    data = json.loads(to_json(f, g))
    assert data["counts"]["high"] == 1 and data["findings"][0]["category"] == "money_float"
