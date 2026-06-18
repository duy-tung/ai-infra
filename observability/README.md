# Shared observability stack

One stack to watch all three agents: **traces** (OpenTelemetry → Jaeger) and
**metrics** (Prometheus → Grafana), with a Pushgateway for the one-shot CLI runs.

```
agent --OTLP--> otel-collector ──> Jaeger                (traces)
                               └─> spanmetrics ──> Prometheus   (RED metrics per span)
agent --push--> pushgateway ─────────────────────> Prometheus   (per-run cost/findings/latency)
Grafana <── Prometheus + Jaeger
```

## Run

```bash
docker compose -f observability/docker-compose.yml up -d

# fintech-guard: traces + pushed metrics
git diff main | python -m fintech_guard.cli --otel --metrics-push http://localhost:9091 --llm

# incident-triage
python -m incident_triage.cli --incident incident.json --otel --metrics-push http://localhost:9091 --llm

# agent-workbench
python -m agent_workbench.cli --otel --metrics-push http://localhost:9091 --workdir .sandbox "..."
```

| UI | URL |
|----|-----|
| Grafana (dashboard "AI agents") | http://localhost:3000 (anonymous admin) |
| Prometheus | http://localhost:9090 |
| Jaeger | http://localhost:16686 |

```bash
docker compose -f observability/docker-compose.yml down
```

## What you see

- **Grafana dashboard** (`grafana/dashboards/ai-agents.json`): total LLM cost,
  LLM call count, guard reviews, triage runs, findings by severity, triage
  outcomes, and span call-rate (from the collector's spanmetrics connector).
- **Jaeger**: per-run traces — `guard.review` / `triage.run` / `agent.run` with
  child `chat <model>` spans carrying token + `cost_usd` attributes.

## Metric names

Pushed by the agents (Pushgateway → Prometheus):
`fintech_guard_reviews_total`, `fintech_guard_findings_total`,
`fintech_guard_cost_usd_total`, `incident_triage_runs_total`,
`incident_triage_cost_usd_total`, `agent_*` (agent-workbench), plus
`*_llm_calls_total` and the `*_seconds` latency histograms.

Derived from spans (spanmetrics): `agent_calls_total{span_name=...}` and
`agent_duration_milliseconds_*`. (Exact spanmetrics names vary by collector
version — adjust the dashboard's span panel if needed.)

## Notes

- Config-only; not run-verified here (no Docker daemon in the build env). Image
  tags are pinned — bump as needed.
- One-shot CLIs are batch jobs, so metrics go through a **Pushgateway** (the
  standard pattern) rather than being scraped directly. Cost lives both as a
  pushed counter and as a `cost_usd` attribute on the `chat` span in Jaeger.
- `agent-workbench/observability/` is a smaller traces-only stack for using that
  project standalone; this root stack is the unified cross-project demo.
