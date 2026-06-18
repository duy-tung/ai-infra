"""The guard pipeline: diff -> static checks -> (optional) LLM review -> report.

This is a code-orchestrated **workflow**, not an open-ended agent loop — PR
review is well-specified, so we control the steps and only call the model for
the judgment-heavy part. The deterministic path runs with no API key, which is
what makes the eval suite offline and reproducible.
"""

from __future__ import annotations

import time
from contextlib import nullcontext
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
    def __init__(self, reviewer=None, threshold: Severity = Severity.HIGH, advisory: bool = True,
                 otel=None, metrics=None) -> None:
        self.reviewer = reviewer
        self.threshold = threshold
        self.advisory = advisory
        self.otel = otel        # optional OpenTelemetry tracer
        self.metrics = metrics  # optional Prometheus metrics

    def review_diff(self, diff_text: str, migration_sql: str | None = None) -> GuardReport:
        from .report import merge_findings

        started = time.monotonic()
        files = parse_unified_diff(diff_text)
        if migration_sql:
            files.append(
                FileDiff(path="migration.sql",
                         added=[(i + 1, line) for i, line in enumerate(migration_sql.splitlines())])
            )

        ctx = self.otel.review_span(len(files)) if self.otel else nullcontext()
        with ctx:
            static = run_static_checks(files)

            llm: list[Finding] = []
            used_llm = False
            if self.reviewer is not None:
                context = diff_text
                if migration_sql:
                    context += "\n\n-- migration.sql --\n" + migration_sql
                t0 = time.monotonic()
                llm = self.reviewer.review(context, already_flagged=[f.category for f in static])
                used_llm = True
                usage = getattr(self.reviewer, "last_usage", {}) or {}
                model = getattr(self.reviewer, "model", "")
                in_tok, out_tok = usage.get("input_tokens", 0), usage.get("output_tokens", 0)
                if self.otel:
                    self.otel.llm_span(model, in_tok, out_tok, time.monotonic() - t0)
                if self.metrics:
                    self.metrics.record_llm(model, in_tok, out_tok)

            merged = merge_findings(static, llm)
            g = gate(merged, self.threshold, self.advisory)
            report = GuardReport(merged, g, time.monotonic() - started, used_llm)
            verdict = "block" if g.blocked else ("advisory" if g.advisory else "pass")
            if self.otel:
                self.otel.set_result(verdict, report.counts, used_llm)
            if self.metrics:
                self.metrics.record_review(verdict, report.counts, report.duration_s)
            return report
