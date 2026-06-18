"""Render the triage as a markdown summary or JSON artifact.

Everything here is advisory and read-only: a rollback *candidate*, queries to
*run yourself*, an owner to *page*. The agent proposes; a human acts.
"""

from __future__ import annotations

import json

from .correlate import Correlation
from .hypotheses import Hypothesis


def to_markdown(correlation: Correlation, hypotheses: list[Hypothesis], meta: dict | None = None) -> str:
    top = hypotheses[0] if hypotheses else None
    lines = ["# Incident triage (advisory · read-only)", ""]
    if top:
        lines.append(f"**Most likely root cause** (confidence {top.confidence:.0%}, {top.source}): {top.root_cause}")
        if top.evidence:
            lines.append(f"> {top.evidence}")
    else:
        lines.append("_No root-cause hypothesis — insufficient correlation._")
    lines.append("")

    if correlation.rollback:
        rb = correlation.rollback
        lines.append(f"**Rollback candidate (advisory):** deploy `{rb.id or rb.sha}` → {rb.service} "
                     f"(deployed {rb.at.isoformat()})")
    if correlation.owner:
        lines.append(f"**Page:** {correlation.owner}")
    if correlation.blast_radius:
        lines.append(f"**Blast radius:** {', '.join(sorted(correlation.blast_radius))}")
    lines.append("")

    if len(hypotheses) > 1:
        lines.append("## Ranked hypotheses")
        for i, h in enumerate(hypotheses, 1):
            lines.append(f"{i}. ({h.confidence:.0%}, {h.source}) {h.root_cause}")
            if h.evidence:
                lines.append(f"   - evidence: {h.evidence}")
        lines.append("")

    queries = top.suggested_queries if top and top.suggested_queries else correlation.queries
    if queries:
        lines.append("## Queries to run (read-only)")
        for q in queries:
            lines.append(f"- `{q}`")
        lines.append("")

    lines.append("## Timeline")
    for e in correlation.timeline:
        lines.append(f"- {e.at} **[{e.kind}]** {e.description}")
    if meta:
        lines.append("")
        lines.append("_" + ", ".join(f"{k}={v}" for k, v in meta.items()) + "_")
    return "\n".join(lines)


def to_json(correlation: Correlation, hypotheses: list[Hypothesis], meta: dict | None = None) -> str:
    return json.dumps(
        {
            "root_cause": hypotheses[0].root_cause if hypotheses else None,
            "confidence": round(hypotheses[0].confidence, 2) if hypotheses else 0.0,
            "hypotheses": [h.to_dict() for h in hypotheses],
            "rollback_candidate": (
                {"id": correlation.rollback.id, "sha": correlation.rollback.sha,
                 "service": correlation.rollback.service, "at": correlation.rollback.at.isoformat()}
                if correlation.rollback else None
            ),
            "owner": correlation.owner,
            "blast_radius": sorted(correlation.blast_radius),
            "suspect_deploys": [
                {"id": s.deploy.id, "service": s.deploy.service,
                 "seconds_before_alert": int(s.seconds_before_alert), "score": s.score}
                for s in correlation.suspect_deploys
            ],
            "error_signatures": [
                {"pattern": sig.pattern, "count": sig.count, "services": sorted(sig.services)}
                for sig in correlation.error_signatures[:10]
            ],
            "queries": correlation.queries,
            "timeline": [{"at": e.at, "kind": e.kind, "description": e.description} for e in correlation.timeline],
            "meta": meta or {},
        },
        indent=2,
        ensure_ascii=False,
    )
