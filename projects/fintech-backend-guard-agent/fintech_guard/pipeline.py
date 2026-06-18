"""The guard pipeline: diff -> static checks -> (optional) LLM review -> report.

This is a code-orchestrated **workflow**, not an open-ended agent loop — PR
review is well-specified, so we control the steps and only call the model for
the judgment-heavy part. The deterministic path runs with no API key, which is
what makes the eval suite offline and reproducible.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from .checks import run_static_checks
from .diff import FileDiff, parse_unified_diff
from .findings import Finding, Severity
from .report import GateResult, gate, severity_counts, to_json, to_markdown


@dataclass
class GuardReport:
    findings: list[Finding]
    gate_result: GateResult
    duration_s: float
    used_llm: bool

    @property
    def counts(self) -> dict[str, int]:
        return severity_counts(self.findings)

    def markdown(self) -> str:
        return to_markdown(self.findings, self.gate_result, self._meta())

    def json(self) -> str:
        return to_json(self.findings, self.gate_result, self._meta())

    def _meta(self) -> dict:
        return {"duration_s": round(self.duration_s, 3), "used_llm": self.used_llm}


class Guard:
    def __init__(self, reviewer=None, threshold: Severity = Severity.HIGH, advisory: bool = True) -> None:
        self.reviewer = reviewer
        self.threshold = threshold
        self.advisory = advisory

    def review_diff(self, diff_text: str, migration_sql: str | None = None) -> GuardReport:
        started = time.monotonic()
        files = parse_unified_diff(diff_text)
        if migration_sql:
            files.append(
                FileDiff(path="migration.sql",
                         added=[(i + 1, line) for i, line in enumerate(migration_sql.splitlines())])
            )

        static = run_static_checks(files)

        llm: list[Finding] = []
        used_llm = False
        if self.reviewer is not None:
            context = diff_text
            if migration_sql:
                context += "\n\n-- migration.sql --\n" + migration_sql
            llm = self.reviewer.review(context, already_flagged=[f.category for f in static])
            used_llm = True

        from .report import merge_findings

        merged = merge_findings(static, llm)
        g = gate(merged, self.threshold, self.advisory)
        return GuardReport(merged, g, time.monotonic() - started, used_llm)
