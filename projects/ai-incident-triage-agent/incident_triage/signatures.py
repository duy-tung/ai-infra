"""Error-log signature extraction.

Raw error lines are noisy — the same bug shows up as "user 4821 not found",
"user 9930 not found", ... Normalizing the variable bits (ids, numbers, hex,
uuids) collapses those into one signature you can count and rank. The dominant
signature around the alert is the strongest deterministic clue to what broke.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime

from .models import LogLine

_UUID = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")
_HEX = re.compile(r"\b0x[0-9a-fA-F]+\b|\b[0-9a-fA-F]{12,}\b")
_NUM = re.compile(r"\b\d+\b")
_QUOTED = re.compile(r"'[^']*'|\"[^\"]*\"")
_WS = re.compile(r"\s+")


def normalize(message: str) -> str:
    s = _UUID.sub("<uuid>", message)
    s = _HEX.sub("<hex>", s)
    s = _QUOTED.sub("<str>", s)
    s = _NUM.sub("<n>", s)
    return _WS.sub(" ", s).strip()


@dataclass
class Signature:
    pattern: str
    count: int
    first_at: datetime
    last_at: datetime
    example: str
    services: set[str]


def extract_signatures(logs: list[LogLine], level: str = "error") -> list[Signature]:
    """Cluster error logs by normalized message; return signatures by count desc."""
    buckets: dict[str, Signature] = {}
    for line in logs:
        if line.level != level:
            continue
        pat = normalize(line.message)
        sig = buckets.get(pat)
        if sig is None:
            buckets[pat] = Signature(
                pattern=pat, count=1, first_at=line.at, last_at=line.at,
                example=line.message, services={line.service} if line.service else set(),
            )
        else:
            sig.count += 1
            sig.first_at = min(sig.first_at, line.at)
            sig.last_at = max(sig.last_at, line.at)
            if line.service:
                sig.services.add(line.service)
    return sorted(buckets.values(), key=lambda s: (-s.count, s.first_at))
