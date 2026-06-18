"""Secret / PII detection + scrubbing.

Two jobs:
1. `find(text)` — used by the `pii_secret` static check to flag secrets/PII a PR
   introduces (committing a key or logging a card is itself a finding).
2. `scrub(text)` — used before sending a diff to the LLM reviewer, so we don't
   ship a customer's PII or a live credential to a third party.

This mirrors the redactor in the agent-workbench harness. In a real monorepo it
would be one shared library; kept local here so this repo is self-contained.
"""

from __future__ import annotations

import re

EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
AWS_KEY = re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")
JWT = re.compile(r"\beyJ[\w-]+\.[\w-]+\.[\w-]+\b")
PRIVATE_KEY = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")
PREFIXED_TOKEN = re.compile(
    r"\b(?:sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,})\b"
)
ASSIGNED_SECRET = re.compile(
    r"(?i)\b(?:api[_-]?key|secret|password|passwd|token|access[_-]?key)\b\s*[:=]\s*['\"][^'\"]{6,}['\"]"
)

# (kind, pattern, is_secret) — secrets are CRITICAL, PII (email) is HIGH.
PATTERNS = [
    ("private_key", PRIVATE_KEY, True),
    ("aws_key", AWS_KEY, True),
    ("jwt", JWT, True),
    ("api_token", PREFIXED_TOKEN, True),
    ("hardcoded_secret", ASSIGNED_SECRET, True),
    ("email_pii", EMAIL, False),
]


def find(text: str) -> list[tuple[str, bool]]:
    """Return [(kind, is_secret), ...] for every match in `text`."""
    hits: list[tuple[str, bool]] = []
    for kind, pattern, is_secret in PATTERNS:
        if pattern.search(text):
            hits.append((kind, is_secret))
    return hits


def scrub(text: str) -> str:
    out = text
    for kind, pattern, _ in PATTERNS:
        out = pattern.sub(f"[REDACTED:{kind}]", out)
    return out
