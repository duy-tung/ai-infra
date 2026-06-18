"""PII / secrets redaction.

Traces and audit logs capture tool inputs and outputs verbatim — which is
exactly where a leaked secret or a customer's PII ends up. This redactor scrubs
the obvious classes before anything is written to disk. It's a defense layer,
not a guarantee: pattern-based redaction misses novel formats, so the real rule
stays "don't point the agent at secrets you can't afford to log."

Two strategies:
1. Named patterns (email, credit card w/ Luhn, AWS key, JWT, common token
   prefixes, private-key headers) — high precision.
2. A conservative high-entropy fallback for long opaque tokens that don't match
   a named pattern.

Replacements look like ``[REDACTED:credit_card]`` so logs stay readable.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

# --- named patterns ---------------------------------------------------------
EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
AWS_KEY = re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")
JWT = re.compile(r"\beyJ[\w-]+\.[\w-]+\.[\w-]+\b")
PRIVATE_KEY = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.DOTALL)
# Common secret/token prefixes: sk-..., ghp_..., xoxb-..., Bearer <token>, slack, etc.
PREFIXED_TOKEN = re.compile(
    r"\b(?:sk-[A-Za-z0-9_-]{16,}"
    r"|gh[pousr]_[A-Za-z0-9]{20,}"
    r"|xox[baprs]-[A-Za-z0-9-]{10,})\b"
)
BEARER = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._-]{16,}")
# Candidate digit runs for credit cards (13-19 digits, optional spaces/dashes).
CC_CANDIDATE = re.compile(r"\b(?:\d[ -]?){13,19}\b")
# Opaque token candidate for the entropy fallback.
TOKEN_CANDIDATE = re.compile(r"\b[A-Za-z0-9+/=_-]{24,}\b")

NAMED = [
    ("private_key", PRIVATE_KEY),
    ("jwt", JWT),
    ("aws_key", AWS_KEY),
    ("api_token", PREFIXED_TOKEN),
    ("bearer_token", BEARER),
    ("email", EMAIL),
]


def luhn_valid(digits: str) -> bool:
    """Luhn checksum — used to confirm a digit run is plausibly a card number,
    cutting false positives on things like long IDs."""
    nums = [int(c) for c in digits if c.isdigit()]
    if not 13 <= len(nums) <= 19:
        return False
    total, parity = 0, len(nums) % 2
    for i, n in enumerate(nums):
        if i % 2 == parity:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    counts: dict[str, int] = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    n = len(s)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


@dataclass
class Redactor:
    entropy_threshold: float = 4.0
    min_entropy_len: int = 24
    _placeholder: str = field(default="[REDACTED:{kind}]", init=False)

    def redact(self, text: str | None) -> str | None:
        if not text:
            return text
        out = text
        for kind, pattern in NAMED:
            out = pattern.sub(self._placeholder.format(kind=kind), out)
        out = self._redact_credit_cards(out)
        out = self._redact_high_entropy(out)
        return out

    def _redact_credit_cards(self, text: str) -> str:
        def repl(m: re.Match[str]) -> str:
            return "[REDACTED:credit_card]" if luhn_valid(m.group(0)) else m.group(0)

        return CC_CANDIDATE.sub(repl, text)

    def _redact_high_entropy(self, text: str) -> str:
        def repl(m: re.Match[str]) -> str:
            tok = m.group(0)
            if len(tok) >= self.min_entropy_len and shannon_entropy(tok) >= self.entropy_threshold:
                return "[REDACTED:secret]"
            return tok

        return TOKEN_CANDIDATE.sub(repl, text)
