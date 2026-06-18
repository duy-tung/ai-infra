"""Findings — the unit of output for the guard.

A Finding is one risk the agent flags: what it is, how bad, where, and how to
fix. Both the deterministic static checks and the LLM reviewer produce Findings,
so the report and the gate treat them uniformly. `source` and `confidence` let
you tell a high-precision static hit from a lower-confidence LLM suggestion.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


# Higher = worse. Used for ranking and the merge gate.
_RANK = {
    Severity.CRITICAL: 4,
    Severity.HIGH: 3,
    Severity.MEDIUM: 2,
    Severity.LOW: 1,
    Severity.INFO: 0,
}


def rank(sev: Severity) -> int:
    return _RANK[sev]


@dataclass
class Finding:
    category: str          # e.g. "money_float", "migration_lock"
    severity: Severity
    message: str
    file: str = ""
    line: int | None = None
    suggestion: str = ""
    confidence: float = 1.0   # static checks = 1.0; LLM findings usually < 1.0
    source: str = "static"    # "static" | "llm"

    def key(self) -> tuple:
        """Identity for de-duplication (category + location)."""
        return (self.category, self.file, self.line)

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "severity": self.severity.value,
            "message": self.message,
            "file": self.file,
            "line": self.line,
            "suggestion": self.suggestion,
            "confidence": round(self.confidence, 2),
            "source": self.source,
        }


def sort_findings(findings: list[Finding]) -> list[Finding]:
    """Worst first; ties broken by file/line for stable output."""
    return sorted(findings, key=lambda f: (-rank(f.severity), f.file, f.line or 0))
