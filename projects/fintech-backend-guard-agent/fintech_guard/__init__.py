"""fintech_guard — an AI PR-review agent for fintech backends.

Reviews a diff for fintech *risk* (idempotency, money precision, migration
locks, ledger/audit gaps, secrets/PII) rather than style. A deterministic
static-check core (no LLM) plus an optional LLM reviewer, merged into a
severity-gated report.

Read order: findings -> diff -> checks -> reviewer -> report -> pipeline.
"""

from .findings import Finding, Severity
from .pipeline import Guard, GuardReport
from .reviewer import LLMReviewer

__all__ = ["Finding", "Severity", "Guard", "GuardReport", "LLMReviewer"]
