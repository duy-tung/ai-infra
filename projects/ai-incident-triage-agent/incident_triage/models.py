"""Incident data model.

The agent reasons over an *incident bundle*: the alert that fired plus the
telemetry around it (recent deploys, error logs, optional metric series, the
suspect diff, a runbook, service ownership). Everything is parsed from one JSON
file so the deterministic core and the eval suite run with no live backends.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def parse_ts(value: Any) -> datetime:
    """Parse an ISO-8601 timestamp into a timezone-aware datetime (UTC if naive)."""
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    s = str(value).strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


@dataclass
class Alert:
    name: str
    service: str
    fired_at: datetime
    metric: str = ""
    value: float | None = None
    threshold: float | None = None

    @classmethod
    def from_dict(cls, d: dict) -> "Alert":
        return cls(
            name=d.get("name", "alert"),
            service=d.get("service", ""),
            fired_at=parse_ts(d["fired_at"]),
            metric=d.get("metric", ""),
            value=d.get("value"),
            threshold=d.get("threshold"),
        )


@dataclass
class Deploy:
    id: str
    service: str
    at: datetime
    sha: str = ""
    summary: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "Deploy":
        return cls(
            id=d.get("id", ""),
            service=d.get("service", ""),
            at=parse_ts(d["at"]),
            sha=d.get("sha", ""),
            summary=d.get("summary", ""),
        )


@dataclass
class LogLine:
    at: datetime
    level: str
    service: str
    message: str

    @classmethod
    def from_dict(cls, d: dict) -> "LogLine":
        return cls(
            at=parse_ts(d["at"]),
            level=d.get("level", "info").lower(),
            service=d.get("service", ""),
            message=d.get("message", ""),
        )


@dataclass
class MetricSeries:
    name: str
    points: list[tuple[datetime, float]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> "MetricSeries":
        pts = [(parse_ts(p["at"]), float(p["value"])) for p in d.get("series", [])]
        return cls(name=d.get("name", ""), points=sorted(pts))


@dataclass
class IncidentBundle:
    alert: Alert
    deploys: list[Deploy] = field(default_factory=list)
    logs: list[LogLine] = field(default_factory=list)
    metrics: list[MetricSeries] = field(default_factory=list)
    diff: str = ""
    runbook: str = ""
    owners: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict) -> "IncidentBundle":
        return cls(
            alert=Alert.from_dict(d["alert"]),
            deploys=[Deploy.from_dict(x) for x in d.get("deploys", [])],
            logs=[LogLine.from_dict(x) for x in d.get("logs", [])],
            metrics=[MetricSeries.from_dict(x) for x in d.get("metrics", [])],
            diff=d.get("diff", ""),
            runbook=d.get("runbook", ""),
            owners=dict(d.get("owners", {})),
        )
