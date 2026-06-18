"""Root-cause hypotheses.

The deterministic correlator gives one strong baseline hypothesis (the suspect
deploy). The LLM reads the same correlated evidence — the suspect deploys, the
*normalized* error signatures, the timeline, the diff, and the runbook — and
proposes additional ranked hypotheses. Both are the same `Hypothesis` shape and
get merged + ranked for the report.

The agent is **read-only**: hypotheses and suggested queries are advisory; the
agent never runs a query or a rollback itself. We send the LLM the normalized
correlation summary (error signatures already have ids/numbers stripped), not
raw log lines — limiting what leaves the process.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any

from .correlate import Correlation
from .models import IncidentBundle

DEFAULT_MODEL = os.environ.get("TRIAGE_MODEL", "claude-opus-4-8")
DEFAULT_EFFORT = os.environ.get("TRIAGE_EFFORT", "high")


@dataclass
class Hypothesis:
    root_cause: str
    confidence: float
    evidence: str = ""
    suggested_queries: list[str] = field(default_factory=list)
    source: str = "heuristic"  # "heuristic" | "llm"

    def to_dict(self) -> dict:
        return {
            "root_cause": self.root_cause,
            "confidence": round(self.confidence, 2),
            "evidence": self.evidence,
            "suggested_queries": self.suggested_queries,
            "source": self.source,
        }


def baseline_hypothesis(correlation: Correlation) -> Hypothesis | None:
    """The deterministic suspect-deploy hypothesis, if there is a suspect."""
    suspect = correlation.top_suspect
    if suspect is None:
        return None
    sig = correlation.error_signatures[0].pattern if correlation.error_signatures else "errors"
    return Hypothesis(
        root_cause=f"Recent deploy {suspect.id or suspect.sha} to {suspect.service} introduced the failure.",
        confidence=correlation.confidence,
        evidence=(
            f"Deployed {int(correlation.suspect_deploys[0].seconds_before_alert)}s before the alert; "
            f"dominant error signature: '{sig}'."
        ),
        suggested_queries=correlation.queries,
        source="heuristic",
    )


def _summarize(correlation: Correlation, bundle: IncidentBundle) -> str:
    lines = [
        f"Alert: {bundle.alert.name} on {bundle.alert.service} "
        f"({bundle.alert.metric}={bundle.alert.value}, threshold={bundle.alert.threshold}) "
        f"at {bundle.alert.fired_at.isoformat()}",
        "",
        "Suspect deploys (closest first):",
    ]
    for s in correlation.suspect_deploys[:5]:
        lines.append(f"  - {s.deploy.id or s.deploy.sha} {s.deploy.service} "
                     f"({int(s.seconds_before_alert)}s before, score {s.score}): {s.deploy.summary}")
    lines.append("")
    lines.append("Top error signatures (normalized):")
    for sig in correlation.error_signatures[:5]:
        lines.append(f"  - x{sig.count} '{sig.pattern}' in {sorted(sig.services)}")
    lines.append("")
    lines.append("Blast radius (services with errors): " + ", ".join(sorted(correlation.blast_radius)))
    lines.append("Timeline:")
    for e in correlation.timeline:
        lines.append(f"  {e.at} [{e.kind}] {e.description}")
    if bundle.runbook:
        lines.append("\nRunbook:\n" + bundle.runbook)
    if bundle.diff:
        lines.append("\nSuspect diff:\n" + bundle.diff)
    return "\n".join(lines)


SYSTEM = """\
You are an on-call SRE doing incident triage for Go/Postgres backend services.
Given correlated evidence, propose RANKED root-cause hypotheses. For each: a
concrete root cause, the evidence for it, a confidence (0-1), and 1-3 read-only
queries to confirm it (logs/metrics/DB — never mutations). Prefer the simplest
explanation that fits the timeline. Do not suggest any action that changes state."""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "hypotheses": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "root_cause": {"type": "string"},
                    "confidence": {"type": "number"},
                    "evidence": {"type": "string"},
                    "suggested_queries": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["root_cause", "confidence", "evidence", "suggested_queries"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["hypotheses"],
    "additionalProperties": False,
}


class HypothesisGenerator:
    def __init__(self, client: Any | None = None, model: str = DEFAULT_MODEL, effort: str = DEFAULT_EFFORT) -> None:
        self._client = client
        self.model = model
        self.effort = effort

    def _ensure_client(self) -> Any:
        if self._client is None:
            try:
                import anthropic
            except ImportError as exc:  # pragma: no cover - depends on env
                raise RuntimeError("the 'anthropic' package is required for the LLM generator (pip install anthropic)") from exc
            self._client = anthropic.Anthropic()
        return self._client

    def generate(self, correlation: Correlation, bundle: IncidentBundle) -> list[Hypothesis]:
        client = self._ensure_client()
        summary = _summarize(correlation, bundle)
        response = client.messages.create(
            model=self.model,
            max_tokens=16000,
            system=SYSTEM,
            output_config={"format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}, "effort": self.effort},
            messages=[{"role": "user", "content": f"Incident evidence:\n\n{summary}"}],
        )
        return self._parse(response)

    @staticmethod
    def _parse(response: Any) -> list[Hypothesis]:
        text = next((b.text for b in response.content if getattr(b, "type", None) == "text"), None)
        if not text:
            return []
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return []
        out: list[Hypothesis] = []
        for item in data.get("hypotheses", []):
            out.append(Hypothesis(
                root_cause=item.get("root_cause", ""),
                confidence=float(item.get("confidence", 0.5)),
                evidence=item.get("evidence", ""),
                suggested_queries=list(item.get("suggested_queries", [])),
                source="llm",
            ))
        return out


def merge_hypotheses(baseline: Hypothesis | None, llm: list[Hypothesis]) -> list[Hypothesis]:
    combined = ([baseline] if baseline else []) + llm
    return sorted(combined, key=lambda h: -h.confidence)
