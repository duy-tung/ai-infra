# ai-incident-triage-agent

> **Status: 🔜 specification — not yet implemented.** Portfolio project #2
> (Month 6–9). Reuses the harness from [`../agent-workbench/`](../agent-workbench/)
> and the observability/production work from
> [Sprint 3](../../learning/sprints/sprint-3-production-infra.md).

An incident-triage assistant for **Go / Postgres services**. Given an alert and
the surrounding telemetry, it proposes a root cause, the blast radius, a rollback
suggestion, and the queries to run next — turning a 2am page into a head start.

## Why this project

It moves you toward **Observability Platform / SRE-for-AI / Developer
Productivity / AI Platform** roles. It's the second leg of the "Agent Control
Plane" narrative and shows you can apply agents to operations, not just code review.

## Input

alert · logs · traces · recent deploys · Git diff (of the suspect deploy) ·
runbook · DB metrics · SLO dashboard.

## Output

- Suspected **root cause** (ranked hypotheses with evidence).
- **Blast radius** (which services/users affected).
- **Rollback suggestion** (which deploy to revert, how).
- **Queries to run** (logs/DB/metrics) to confirm.
- **Service owner** to page.
- **Confidence score** per hypothesis.
- **Incident timeline** (deploys + alerts + metric shifts).

## Architecture

```
Alert
  → Telemetry loader     (logs + traces + DB metrics + SLO + recent deploys + diff)
  → Correlator           (align metric shift ↔ deploy time ↔ diff)
  → Hypothesis generator (LLM: ranked root-cause hypotheses + evidence)
  → Evidence checker      (run suggested queries in a read-only sandbox)
  → Report               (root cause · blast radius · rollback · queries · owner · confidence · timeline)
```

Reuses from `agent-workbench`: agent loop, tool registry (read-only tools for
querying logs/metrics), permission gate (read-only mode by default!), tracing/cost, eval runner.

## Tech stack

- **Go** for the service + collectors.
- **Python** for the agent / eval harness.
- **Postgres** for runs + incident records.
- **OpenTelemetry + Prometheus/Grafana** (also the *source* of telemetry it reasons over).
- **Docker Compose** local stack with a sample Go/Postgres service to break on purpose.

## Evaluation methodology

- Fixture incidents: a recorded telemetry bundle + the known root cause.
- Grade: did the top hypothesis match the real root cause? (top-1 / top-3 accuracy)
- Track false root-cause rate and mean time-to-hypothesis.

## KPIs

top-1 / top-3 root-cause accuracy · mean time-to-first-hypothesis · cost per
incident · % incidents with correct rollback suggestion · operator time saved.

## Security model

**Read-only by default.** This agent reasons over telemetry; it must not mutate
prod. Permission gate runs in `readonly` mode; any suggested query/rollback is
*advisory* and executed only by a human. PII scrubbing on all ingested logs.

## Required README sections (fill when building)

What I learned · Production considerations · Failure modes · Security model ·
Evaluation methodology · Architecture diagram · Demo.

---

> ⚠️ When public: anonymize / use synthetic telemetry only.
