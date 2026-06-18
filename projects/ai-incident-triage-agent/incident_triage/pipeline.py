"""Triage pipeline: bundle -> correlate -> (optional) LLM hypotheses -> report.

A read-only workflow. The deterministic correlation runs with no API key (so the
eval is offline); the LLM hypothesis generator is an optional layer on top.
"""

from __future__ import annotations

import time
from contextlib import nullcontext
from dataclasses import dataclass

from .correlate import Correlation, correlate
from .hypotheses import Hypothesis, HypothesisGenerator, baseline_hypothesis, merge_hypotheses
from .models import IncidentBundle
from .report import to_json, to_markdown


@dataclass
class TriageReport:
    correlation: Correlation
    hypotheses: list[Hypothesis]
    duration_s: float
    used_llm: bool

    @property
    def top(self) -> Hypothesis | None:
        return self.hypotheses[0] if self.hypotheses else None

    def markdown(self) -> str:
        return to_markdown(self.correlation, self.hypotheses, self._meta())

    def json(self) -> str:
        return to_json(self.correlation, self.hypotheses, self._meta())

    def _meta(self) -> dict:
        return {"duration_s": round(self.duration_s, 3), "used_llm": self.used_llm,
                "confidence": self.top.confidence if self.top else 0.0}


class Triage:
    def __init__(self, generator: HypothesisGenerator | None = None, window_minutes: int = 60, otel=None) -> None:
        self.generator = generator
        self.window_minutes = window_minutes
        self.otel = otel  # optional OpenTelemetry tracer

    def triage(self, bundle: IncidentBundle) -> TriageReport:
        started = time.monotonic()
        ctx = self.otel.triage_span(bundle.alert.service) if self.otel else nullcontext()
        with ctx:
            correlation = correlate(bundle, window_minutes=self.window_minutes)
            baseline = baseline_hypothesis(correlation)

            llm: list[Hypothesis] = []
            used_llm = False
            if self.generator is not None:
                t0 = time.monotonic()
                llm = self.generator.generate(correlation, bundle)
                used_llm = True
                if self.otel:
                    usage = getattr(self.generator, "last_usage", {}) or {}
                    self.otel.llm_span(getattr(self.generator, "model", ""),
                                       usage.get("input_tokens", 0), usage.get("output_tokens", 0),
                                       time.monotonic() - t0)

            hypotheses = merge_hypotheses(baseline, llm)
            report = TriageReport(correlation, hypotheses, time.monotonic() - started, used_llm)
            if self.otel:
                top_conf = report.top.confidence if report.top else 0.0
                self.otel.set_result(len(correlation.suspect_deploys), top_conf, used_llm)
            return report
