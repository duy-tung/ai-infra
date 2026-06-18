"""Merge, gate, and render findings.

- `merge_findings` de-dupes static + LLM findings (static wins on a tie — it's
  higher precision).
- `gate` decides whether the PR should be blocked. Default is **advisory**: it
  computes what *would* block but never returns blocked=True, matching the
  "roll out advisory-only first" plan. Flip `advisory=False` to enforce.
- `to_markdown` / `to_json` render a PR comment or a machine-readable artifact.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from .findings import Finding, Severity, rank, sort_findings

_EMOJI = {
    Severity.CRITICAL: "🛑",
    Severity.HIGH: "🔴",
    Severity.MEDIUM: "🟠",
    Severity.LOW: "🟡",
    Severity.INFO: "⚪",
}


def merge_findings(static: list[Finding], llm: list[Finding]) -> list[Finding]:
    by_key: dict[tuple, Finding] = {}
    for f in [*static, *llm]:  # static first so it wins ties on identical key
        existing = by_key.get(f.key())
        if existing is None or rank(f.severity) > rank(existing.severity):
            by_key[f.key()] = f
    return sort_findings(list(by_key.values()))


def severity_counts(findings: list[Finding]) -> dict[str, int]:
    counts = {s.value: 0 for s in Severity}
    for f in findings:
        counts[f.severity.value] += 1
    return counts


@dataclass
class GateResult:
    blocked: bool
    would_block: bool      # what enforcement *would* decide (useful in advisory mode)
    threshold: Severity
    advisory: bool
    reason: str


def gate(findings: list[Finding], threshold: Severity = Severity.HIGH, advisory: bool = True) -> GateResult:
    worst = [f for f in findings if rank(f.severity) >= rank(threshold)]
    would_block = bool(worst)
    reason = (
        f"{len(worst)} finding(s) at or above {threshold.value}" if would_block else "no blocking findings"
    )
    return GateResult(
        blocked=False if advisory else would_block,
        would_block=would_block,
        threshold=threshold,
        advisory=advisory,
        reason=reason,
    )


def to_markdown(findings: list[Finding], gate_result: GateResult, meta: dict | None = None) -> str:
    counts = severity_counts(findings)
    lines = ["# Fintech Backend Guard — review", ""]
    verdict = "ADVISORY" if gate_result.advisory else ("BLOCK" if gate_result.blocked else "PASS")
    lines.append(f"**Verdict:** {verdict} — {gate_result.reason} (threshold: {gate_result.threshold.value})")
    summary = ", ".join(f"{k}: {v}" for k, v in counts.items() if v)
    lines.append(f"**Findings:** {summary or 'none'}")
    if meta:
        lines.append("**Meta:** " + ", ".join(f"{k}={v}" for k, v in meta.items()))
    lines.append("")
    if not findings:
        lines.append("_No risks flagged._")
        return "\n".join(lines)
    for f in findings:
        loc = f"`{f.file}`" + (f":{f.line}" if f.line else "")
        lines.append(f"### {_EMOJI[f.severity]} {f.severity.value.upper()} · {f.category} ({f.source}, conf {f.confidence:.2f})")
        lines.append(f"- {loc}")
        lines.append(f"- {f.message}")
        if f.suggestion:
            lines.append(f"- **Fix:** {f.suggestion}")
        lines.append("")
    return "\n".join(lines)


def to_json(findings: list[Finding], gate_result: GateResult, meta: dict | None = None) -> str:
    return json.dumps(
        {
            "verdict": "block" if gate_result.blocked else ("advisory" if gate_result.advisory else "pass"),
            "would_block": gate_result.would_block,
            "threshold": gate_result.threshold.value,
            "counts": severity_counts(findings),
            "findings": [f.to_dict() for f in findings],
            "meta": meta or {},
        },
        indent=2,
        ensure_ascii=False,
    )
