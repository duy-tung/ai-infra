"""LLM reviewer — the fuzzy layer the static checks can't cover.

Static checks catch known patterns precisely. The LLM reads the diff for the
risks that need judgment: a transaction boundary split across two writes, a
reconciliation path that's silently missing, a retry that isn't safe. It returns
the same `Finding` shape via structured output, so everything downstream is
uniform.

Design choices that matter:
- The diff is **scrubbed** (redaction.scrub) before it leaves the process — no
  PII/secret goes to the API.
- We use structured outputs (`output_config.format`) for a guaranteed JSON shape.
- For code review, we ask the model to **report everything with a confidence +
  severity** and let the gate filter — recent models follow "be conservative"
  instructions literally, which silently drops findings.
- The Anthropic client is injectable, so tests run with a scripted fake (no API).
"""

from __future__ import annotations

import json
import os
from typing import Any

from . import redaction
from .findings import Finding, Severity

DEFAULT_MODEL = os.environ.get("GUARD_MODEL", "claude-opus-4-8")
DEFAULT_EFFORT = os.environ.get("GUARD_EFFORT", "high")

RISK_TAXONOMY = """\
idempotency, retry-induced double charge, transaction boundary/atomicity,
decimal/money precision and rounding, ledger imbalance (debits != credits),
missing reconciliation/settlement path, SQL migration lock risk, missing audit
trail, PII/secrets exposure, missing metric/span on a critical path, missing
rollback plan, and missing tests for failure/timeout cases."""

SYSTEM = f"""\
You are a senior fintech backend reviewer. Review the diff for RISK, not style.
Focus on: {RISK_TAXONOMY}

Report EVERY issue you find, including low-confidence and low-severity ones — a
separate gate filters by severity later, so your job is coverage, not filtering.
For each finding include a confidence (0-1) and a severity. Do not report pure
style/naming nits. Be concrete about the fix."""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "severity": {"type": "string", "enum": ["critical", "high", "medium", "low", "info"]},
                    "message": {"type": "string"},
                    "file": {"type": "string"},
                    "line": {"type": ["integer", "null"]},
                    "suggestion": {"type": "string"},
                    "confidence": {"type": "number"},
                },
                "required": ["category", "severity", "message", "suggestion", "confidence"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["findings"],
    "additionalProperties": False,
}


class LLMReviewer:
    def __init__(self, client: Any | None = None, model: str = DEFAULT_MODEL, effort: str = DEFAULT_EFFORT) -> None:
        self._client = client
        self.model = model
        self.effort = effort

    def _ensure_client(self) -> Any:
        if self._client is None:
            try:
                import anthropic
            except ImportError as exc:  # pragma: no cover - depends on env
                raise RuntimeError("the 'anthropic' package is required for the LLM reviewer (pip install anthropic)") from exc
            self._client = anthropic.Anthropic()
        return self._client

    def review(self, diff_text: str, already_flagged: list[str] | None = None) -> list[Finding]:
        client = self._ensure_client()
        safe_diff = redaction.scrub(diff_text)
        note = ""
        if already_flagged:
            note = ("\nStatic analysis already flagged these categories; focus on risks beyond them: "
                    + ", ".join(sorted(set(already_flagged))) + ".")
        response = client.messages.create(
            model=self.model,
            max_tokens=16000,
            system=SYSTEM,
            output_config={"format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}, "effort": self.effort},
            messages=[{"role": "user", "content": f"Review this diff.{note}\n\n```diff\n{safe_diff}\n```"}],
        )
        return self._parse(response)

    @staticmethod
    def _parse(response: Any) -> list[Finding]:
        text = next((b.text for b in response.content if getattr(b, "type", None) == "text"), None)
        if not text:
            return []
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return []
        findings: list[Finding] = []
        for item in data.get("findings", []):
            try:
                sev = Severity(item["severity"])
            except (KeyError, ValueError):
                sev = Severity.INFO
            findings.append(Finding(
                category=item.get("category", "llm_finding"),
                severity=sev,
                message=item.get("message", ""),
                file=item.get("file", ""),
                line=item.get("line"),
                suggestion=item.get("suggestion", ""),
                confidence=float(item.get("confidence", 0.5)),
                source="llm",
            ))
        return findings
