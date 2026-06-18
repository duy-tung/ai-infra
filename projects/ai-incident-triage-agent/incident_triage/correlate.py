"""Deterministic correlation — the heart of the triage, no LLM required.

Given the incident bundle, line up the alert with what changed and what broke:

- **Suspect deploys**: deploys shortly before the alert, ranked by time
  proximity (and a bonus when the deploy is to the alerting service).
- **Error signatures**: the dominant normalized error around the alert window.
- **Blast radius**: which services show errors in the window.
- **Timeline**: deploys + alert + first error, time-ordered.
- **Rollback**: the top suspect deploy (advisory — this agent never acts).
- **Owner**, **suggested queries**, and a **confidence** score.

This is the reproducible spine; the LLM hypothesis layer builds on top of it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta

from .models import Deploy, IncidentBundle
from .signatures import Signature, extract_signatures


@dataclass
class SuspectDeploy:
    deploy: Deploy
    seconds_before_alert: float
    score: float


@dataclass
class TimelineEvent:
    at: str           # ISO string for rendering
    kind: str         # deploy | alert | error
    description: str


@dataclass
class Correlation:
    suspect_deploys: list[SuspectDeploy]
    error_signatures: list[Signature]
    timeline: list[TimelineEvent]
    blast_radius: set[str]
    rollback: Deploy | None
    owner: str | None
    queries: list[str]
    confidence: float

    @property
    def top_suspect(self) -> Deploy | None:
        return self.suspect_deploys[0].deploy if self.suspect_deploys else None


def correlate(bundle: IncidentBundle, window_minutes: int = 60) -> Correlation:
    alert = bundle.alert
    window = timedelta(minutes=window_minutes)

    # --- suspect deploys: before the alert, within the window, closest first ---
    suspects: list[SuspectDeploy] = []
    for dep in bundle.deploys:
        gap = (alert.fired_at - dep.at).total_seconds()
        if 0 <= gap <= window.total_seconds():
            proximity = 1.0 - gap / window.total_seconds()      # 1.0 == fired right after deploy
            same_service = 0.25 if dep.service == alert.service else 0.0
            suspects.append(SuspectDeploy(dep, gap, round(min(proximity + same_service, 1.0), 3)))
    suspects.sort(key=lambda s: (-s.score, s.seconds_before_alert))

    # --- error signatures + blast radius within the window around the alert ---
    lo = alert.fired_at - window
    windowed = [l for l in bundle.logs if l.at >= lo]
    signatures = extract_signatures(windowed, level="error")
    blast = {l.service for l in windowed if l.level == "error" and l.service}

    rollback = suspects[0].deploy if suspects else None
    owner = bundle.owners.get(alert.service) or (
        bundle.owners.get(rollback.service) if rollback else None
    )

    # --- timeline ---
    events: list[TimelineEvent] = []
    for s in suspects:
        events.append(TimelineEvent(s.deploy.at.isoformat(), "deploy",
                                    f"deploy {s.deploy.id or s.deploy.sha} -> {s.deploy.service}: {s.deploy.summary}"))
    if signatures:
        top = signatures[0]
        events.append(TimelineEvent(top.first_at.isoformat(), "error",
                                    f"first '{top.pattern}' (x{top.count})"))
    events.append(TimelineEvent(alert.fired_at.isoformat(), "alert",
                                f"{alert.name} on {alert.service} ({alert.metric}={alert.value})"))
    events.sort(key=lambda e: e.at)

    # --- suggested (read-only) queries ---
    queries = _suggested_queries(bundle, rollback, signatures)

    # --- confidence: proximity of the top suspect + does the error postdate it? ---
    confidence = _confidence(suspects, signatures, rollback)

    return Correlation(
        suspect_deploys=suspects,
        error_signatures=signatures,
        timeline=events,
        blast_radius=blast,
        rollback=rollback,
        owner=owner,
        queries=queries,
        confidence=confidence,
    )


def _suggested_queries(bundle: IncidentBundle, rollback: Deploy | None, signatures: list[Signature]) -> list[str]:
    a = bundle.alert
    qs = [
        f"logs: service={a.service} level=error since={a.fired_at.isoformat()}",
        f"metric: {a.metric or 'error_rate'} for {a.service} around {a.fired_at.isoformat()}",
    ]
    if rollback:
        qs.append(f"deploy diff: {rollback.id or rollback.sha} ({rollback.service})")
        qs.append(f"compare error_rate for {rollback.service} before/after {rollback.at.isoformat()}")
    if signatures:
        qs.append(f"logs matching: \"{signatures[0].example}\"")
    return qs


def _confidence(suspects, signatures, rollback) -> float:
    if not suspects:
        return 0.1
    score = suspects[0].score * 0.7
    # Boost if the dominant error first appeared *after* the suspect deploy.
    if signatures and rollback and signatures[0].first_at >= rollback.at:
        score += 0.25
    # Small penalty if several deploys are plausible (ambiguity).
    if len(suspects) > 1 and suspects[1].score >= suspects[0].score - 0.1:
        score -= 0.1
    return round(max(0.1, min(score, 0.99)), 3)
