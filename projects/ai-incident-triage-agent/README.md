# ai-incident-triage-agent

> **Status: ✅ runnable starter.** The deterministic correlation core and the
> offline eval are implemented and tested (23 unit tests; 3 incident fixtures at
> top-1 = 100%). The LLM hypothesis layer is wired and testable with a scripted
> client (real runs need `ANTHROPIC_API_KEY`). Portfolio project #2; reuses the
> workflow shape from [`../fintech-backend-guard-agent/`](../fintech-backend-guard-agent/).

An incident-triage assistant for **Go / Postgres services**. Given an alert and
the surrounding telemetry, it proposes a root cause, the blast radius, a rollback
suggestion, and the queries to run next — turning a 2am page into a head start.

## Why this project

It moves you toward **Observability Platform / SRE-for-AI / Developer
Productivity / AI Platform** roles. It's the second leg of the "Agent Control
Plane" narrative and shows you can apply agents to operations, not just code review.

## Quickstart

```bash
cd projects/ai-incident-triage-agent
python -m pip install -e ".[dev]"

make test     # 23 unit tests (offline, no API key)
make eval     # grade suspect-deploy correlation over fixture incidents (offline)

# triage an incident bundle — deterministic correlation, no API key
python -m incident_triage.cli --incident evals/fixtures/deploy_caused_errors.json
# add the LLM hypothesis layer (needs ANTHROPIC_API_KEY)
python -m incident_triage.cli --incident incident.json --llm
# JSON for a bot / dashboard
python -m incident_triage.cli --incident incident.json --json
# emit OpenTelemetry spans (triage + LLM call with token/cost) — needs ".[otel]" + an OTLP endpoint
python -m incident_triage.cli --incident incident.json --llm --otel
```

The incident bundle is a single JSON file (alert + deploys + logs + optional
metrics/diff/runbook/owners) — so the whole pipeline runs with no live backends.

## What's implemented vs. ahead

| Piece | Module | Status |
|-------|--------|--------|
| Incident bundle model + ISO time parsing | `models.py` | ✅ |
| Error-log signature clustering | `signatures.py` | ✅ normalizes ids/numbers/uuids |
| Deterministic correlator | `correlate.py` | ✅ suspect deploys, blast radius, timeline, rollback, owner, queries, confidence |
| LLM hypothesis generator (structured output) | `hypotheses.py` | ✅ (fake-client tested; real runs need a key) |
| Report (markdown / JSON) | `report.py` | ✅ read-only / advisory |
| Pipeline (workflow) + CLI | `pipeline.py`, `cli.py` | ✅ |
| Offline eval (top-1 / top-3 accuracy) | `evals/` | ✅ 3 fixtures |
| OpenTelemetry tracing + cost | `tracing.py` | ✅ `triage.run` → `chat <model>` spans (tokens + USD); `--otel` |
| Live connectors (Loki/Tempo/Prometheus/GitHub), metric-shift detection, dashboard | — | 🔜 next |

Like the guard, it's a **workflow**, not an agent loop, and **read-only**: it
proposes a rollback candidate and queries; a human acts.

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

## What I learned

> _Draft — personalize before publishing._

- **Most of incident triage is correlation, and correlation is deterministic.**
  Lining up alert time ↔ deploy time ↔ error onset gets you most of the way to a
  hypothesis with no model; the LLM adds value only on the ambiguous cases.
- **Read-only is a feature, not a limitation.** Making the agent incapable of
  acting removes the scariest failure mode in incident response and makes it
  something on-call will actually trust.
- **Normalize before you cluster.** Raw error lines never group; normalized
  signatures (ids/numbers/uuids stripped) do — and the normalization doubles as
  light PII reduction before text reaches the model.
- **Send the model a summary, not raw logs** — cheaper, and it limits PII egress.

## Failure modes

- Correlation isn't causation — the top suspect is a *candidate* surfaced with a
  confidence score, not a verdict.
- Signature normalization can over- or under-cluster.
- With no deploy in the window it reports low confidence rather than inventing a
  culprit (covered by the `no_recent_deploy` fixture).

---

> ⚠️ When public: anonymize / use synthetic telemetry only.
