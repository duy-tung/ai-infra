# Observability stack

A local OpenTelemetry → Jaeger stack to view agent traces. Pairs with the
`OtelTracer` in `agent_workbench/tracing_otel.py`.

```
agent  ──OTLP gRPC :4317──▶  otel-collector  ──OTLP──▶  jaeger (UI :16686)
```

## Run

```bash
# from projects/agent-workbench
pip install -e ".[otel]"

docker compose -f observability/docker-compose.yml up -d

# run the agent with OTel on (exports to localhost:4317 by default)
export ANTHROPIC_API_KEY=sk-ant-...
python -m agent_workbench.cli --otel --workdir .sandbox --permission-mode auto \
    "create greet.py that prints hello, then run it"

# open the UI and find service "agent-workbench"
open http://localhost:16686

docker compose -f observability/docker-compose.yml down
```

## What you'll see

One trace per run:

```
agent.run                       (root — task, status, total cost)
├── chat claude-opus-4-8        (gen_ai.usage.input_tokens / output_tokens / cost_usd, finish reason)
├── execute_tool write_file     (gen_ai.tool.name, agent.tool.permission; ERROR status on failure)
└── chat claude-opus-4-8
```

Attributes follow the OpenTelemetry **GenAI semantic conventions**
(`gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.*`, `gen_ai.operation.name`,
`gen_ai.tool.name`) plus a custom `gen_ai.usage.cost_usd`.

## Configuration

- Endpoint: set `OTEL_EXPORTER_OTLP_ENDPOINT` (default `http://localhost:4317`).
- The collector (`otel-collector-config.yaml`) is the natural place to add
  sampling, PII redaction, or a second exporter — that's the "AI gateway"
  pattern from Phase 17.

## Why a collector (not export straight to Jaeger)

Jaeger all-in-one *can* receive OTLP directly, but routing through a collector
mirrors production: one gateway you control for sampling, redaction, resource
enrichment, and fan-out — without touching app code.
