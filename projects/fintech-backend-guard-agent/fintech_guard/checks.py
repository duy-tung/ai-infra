"""Deterministic static checks — the fintech risk taxonomy.

These run with no LLM: pure pattern matching over the lines a PR adds. They're
cheap, fast, reproducible, and high-precision on the risks they target — exactly
the kind of finding you want to gate a merge on. The LLM reviewer (reviewer.py)
covers the fuzzier risks these can't catch.

Each check returns Findings. Heuristics are intentionally conservative; tune the
patterns and severities against your codebase's conventions.
"""

from __future__ import annotations

import re

from . import redaction
from .diff import FileDiff
from .findings import Finding, Severity

# --- vocabularies -----------------------------------------------------------
MONEY = re.compile(r"(?i)\b(amount|price|balance|total|subtotal|fee|cost|money|payment|refund|charge|tax|salary|wage|interest|principal)\b")
FLOAT_TYPE = re.compile(r"(?i)(\bfloat(32|64)?\b|\bdouble\b|:\s*float\b|\bfloat\s*\()")
PAYMENT = re.compile(r"(?i)\b(charge|payment|transfer|capture|debit|withdraw|payout|refund|settle)\b")
HANDLER = re.compile(r"(?i)(\bdef\b|\bfunc\b|@app\.route|@router|\.post\(|HandlerFunc|POST\b)")
LEDGER = re.compile(r"(?i)\b(ledger|account|transaction|balance|entry|journal|posting|wallet)\b")
DB_WRITE = re.compile(r"(?i)(insert\s+into|update\s+\w|delete\s+from|\.save\(|\.create\(|\.update\(|\.insert\()")


def _add(findings, **kw):
    findings.append(Finding(**kw))


def check_money_float(files: list[FileDiff]) -> list[Finding]:
    out: list[Finding] = []
    for fd in files:
        if fd.is_sql():
            continue
        for lineno, text in fd.added:
            if MONEY.search(text) and FLOAT_TYPE.search(text):
                _add(out, category="money_float", severity=Severity.HIGH, file=fd.path, line=lineno,
                     message="Floating-point type used for a monetary value — rounding errors will corrupt balances.",
                     suggestion="Use integer minor units (cents) or a fixed-precision Decimal type for money.")
    return out


def check_migration_lock(files: list[FileDiff]) -> list[Finding]:
    out: list[Finding] = []
    for fd in files:
        if not fd.is_sql():
            continue
        for lineno, text in fd.added:
            low = text.lower()
            if "add column" in low and "not null" in low and "default" not in low:
                _add(out, category="migration_not_null", severity=Severity.HIGH, file=fd.path, line=lineno,
                     message="Adding a NOT NULL column without a DEFAULT rewrites the table under an exclusive lock.",
                     suggestion="Add the column nullable (or with a default), backfill, then add the NOT NULL constraint.")
            if "create index" in low and "concurrently" not in low:
                _add(out, category="migration_index_lock", severity=Severity.MEDIUM, file=fd.path, line=lineno,
                     message="CREATE INDEX without CONCURRENTLY locks writes on the table for the duration.",
                     suggestion="Use CREATE INDEX CONCURRENTLY (outside a transaction).")
            if re.search(r"alter\s+column\s+.+\s+type", low):
                _add(out, category="migration_type_change", severity=Severity.HIGH, file=fd.path, line=lineno,
                     message="Altering a column type can rewrite the table and take a long lock.",
                     suggestion="Add a new column, dual-write/backfill, then swap — avoid in-place type changes on hot tables.")
            if "lock table" in low:
                _add(out, category="migration_lock_table", severity=Severity.MEDIUM, file=fd.path, line=lineno,
                     message="Explicit LOCK TABLE blocks concurrent access.",
                     suggestion="Confirm the lock scope/duration is acceptable; prefer lock-free migration patterns.")
    return out


def check_missing_idempotency(files: list[FileDiff]) -> list[Finding]:
    out: list[Finding] = []
    for fd in files:
        if fd.is_sql():
            continue
        text = fd.added_text
        # File-level: a handler is defined AND the file deals with payments,
        # but nothing mentions idempotency. (Keyword + handler often land on
        # different lines — the def names the func, the call does the charge.)
        has_handler = any(HANDLER.search(t) for _, t in fd.added)
        has_payment = bool(PAYMENT.search(text))
        if has_handler and has_payment and "idempoten" not in text.lower():
            line = next((ln for ln, t in fd.added if HANDLER.search(t)), None)
            _add(out, category="missing_idempotency", severity=Severity.MEDIUM, file=fd.path, line=line,
                 confidence=0.6,
                 message="New payment/charge handler with no visible idempotency key — a retry could double-charge.",
                 suggestion="Require an idempotency key and dedupe on it before performing the side effect.")
    return out


def check_secret_pii(files: list[FileDiff]) -> list[Finding]:
    out: list[Finding] = []
    for fd in files:
        for lineno, text in fd.added:
            hits = redaction.find(text)
            if not hits:
                continue
            worst_secret = any(is_secret for _, is_secret in hits)
            kinds = ", ".join(kind for kind, _ in hits)
            _add(out,
                 category="pii_secret",
                 severity=Severity.CRITICAL if worst_secret else Severity.HIGH,
                 file=fd.path, line=lineno,
                 message=f"Possible secret/PII introduced in the diff ({kinds}).",
                 suggestion="Remove the value, rotate it if it was real, and load it from a secret manager / env.")
    return out


def check_error_swallow(files: list[FileDiff]) -> list[Finding]:
    out: list[Finding] = []
    single = re.compile(r"(?i)except[^:]*:\s*pass\s*$")
    empty_catch = re.compile(r"catch\s*\([^)]*\)\s*\{\s*\}")
    go_ignore = re.compile(r"\b_\s*=\s*err\b")
    for fd in files:
        added = fd.added
        for i, (lineno, text) in enumerate(added):
            stripped = text.strip()
            hit = (
                single.search(text)
                or empty_catch.search(text)
                or go_ignore.search(text)
                or (stripped == "pass" and i > 0 and added[i - 1][1].strip().startswith("except"))
            )
            if hit:
                _add(out, category="error_swallow", severity=Severity.MEDIUM, file=fd.path, line=lineno,
                     message="Error is silently swallowed — failures on a financial path must not be ignored.",
                     suggestion="Log the error, fail closed, and propagate so the caller can retry/compensate.")
    return out


def check_missing_audit(files: list[FileDiff]) -> list[Finding]:
    out: list[Finding] = []
    for fd in files:
        writes_ledger = any(DB_WRITE.search(t) and LEDGER.search(t) for _, t in fd.added)
        mentions_audit = "audit" in fd.added_text.lower()
        if writes_ledger and not mentions_audit:
            line = next((ln for ln, t in fd.added if DB_WRITE.search(t) and LEDGER.search(t)), None)
            _add(out, category="missing_audit", severity=Severity.MEDIUM, file=fd.path, line=line,
                 confidence=0.6,
                 message="Write to a ledger/account/transaction with no audit-trail entry nearby.",
                 suggestion="Record an append-only audit entry (actor, action, before/after) for state-changing writes.")
    return out


CHECKS = [
    check_money_float,
    check_migration_lock,
    check_missing_idempotency,
    check_secret_pii,
    check_error_swallow,
    check_missing_audit,
]


def run_static_checks(files: list[FileDiff]) -> list[Finding]:
    findings: list[Finding] = []
    for check in CHECKS:
        findings.extend(check(files))
    return findings
