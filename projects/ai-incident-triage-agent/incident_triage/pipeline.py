"""Triage pipeline: bundle -> correlate -> (optional) LLM hypotheses -> report.

A read-only workflow. The deterministic correlation runs with no API key (so the
eval is offline); the LLM hypothesis generator is an optional layer on top.
"""

from __future__ import annotations

import time
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
    def __init__(self, generator: HypothesisGenerator | None = None, window_minutes: int = 60) -> None:
        self.generator = generator
        self.window_minutes = window_minutes

    def triage(self, bundle: IncidentBundle) -> TriageReport:
        started = time.monotonic()
        correlation = correlate(bundle, window_minutes=self.window_minutes)
        baseline = baseline_hypothesis(correlation)

        llm: list[Hypothesis] = []
        used_llm = False
        if self.generator is not None:
            llm = self.generator.generate(correlation, bundle)
            used_llm = True

        hypotheses = merge_hypotheses(baseline, llm)
        return TriageReport(correlation, hypotheses, time.monotonic() - started, used_llm)
