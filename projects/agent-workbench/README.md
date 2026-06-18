# agent-workbench

A minimal, readable **coding-agent harness** — the core machinery every agent
platform needs, with nothing you can't read in an afternoon:

- an **agent loop** (the model calls tools until the task is done),
- a **tool registry** (read file, write file, run shell),
- a **permission gate** (human-in-the-loop / policy control over mutating actions),
- **tracing + cost accounting** (JSONL trace per run, token and USD totals),
- a **fixture-based eval runner** (run the agent against tasks, grade the outcome).

It is intentionally small and dependency-light so you can see exactly how an
agent works, then extend it. It is the Sprint 1 / Month 0–30 artifact of the
[ai-infra learning plan](../../learning/02-roadmap-12-months.md) — the
foundation the fintech PR-review agent and incident-triage agent build on.

> Built with the Anthropic Python SDK against Claude (Opus 4.8 by default;
> configurable to Sonnet 4.6 / Haiku 4.5 for cheaper loops).

## Architecture

```
                 task (string)
                      │
                      ▼
            ┌──────────────────┐        ┌──────────────────────┐
            │    Agent loop    │ ─────▶ │  Anthropic Messages   │
            │  (agent.py)      │ ◀───── │  API (Claude)         │
            └────────┬─────────┘        └──────────────────────┘
                     │ tool_use
                     ▼
            ┌──────────────────┐   check   ┌──────────────────┐
            │ Permission gate  │ ◀──────── │  Tool registry   │
            │ (permissions.py) │           │  (registry.py)   │
            └────────┬─────────┘           └────────┬─────────┘
              allow  │ deny                          │
                     ▼                               ▼
            ┌──────────────────┐           read_file / write_file / run_shell
            │   Tracer (JSONL) │◀──── every LLM call + tool call + totals
            │  (tracing.py)    │
            └──────────────────┘
```

The loop is **manual on purpose** (not the SDK's auto tool runner): driving it
ourselves is what lets the harness gate, time, and log every single tool call —
which is the whole point of a workbench.

## Quickstart

```bash
cd projects/agent-workbench
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"          # or: pip install -r requirements.txt

# 1) Run the offline unit tests (no API key needed — uses a scripted fake LLM)
make test

# 2) Set your key and run the agent on a real task
cp .env.example .env             # then edit ANTHROPIC_API_KEY
export ANTHROPIC_API_KEY=sk-ant-...
python -m agent_workbench.cli --workdir .sandbox \
    "create greet.py that prints hello, then run it"

# 3) Run the eval suite (calls the API)
make eval
```

By default the agent runs in `--permission-mode ask`, so it pauses for your
approval before any file write or shell command.

## How the loop works

Each turn (`agent.py`):

1. Send the conversation + tool schemas to Claude.
2. Record token usage and cost in the trace.
3. If `stop_reason == "end_turn"` → done.
4. Otherwise, for each `tool_use` block: ask the **permission gate**, run the
   tool through the **registry** (or return a "denied" result), and feed the
   results back as a `tool_result`.
5. Repeat, up to `AGENT_MAX_TURNS`.

The assistant turn (including thinking and `tool_use` blocks) is appended to the
message history **verbatim** before tool results — the API requires that pairing.

## The moving parts (read in this order)

| File | Responsibility |
|------|----------------|
| `config.py` | Model, pricing table, effort/thinking, trace dir — all tunable via env. |
| `tools/base.py` | The `Tool` contract: schema + `run`, plus `mutating` / `parallel_safe`. |
| `tools/registry.py` | Register tools, expose schemas, dispatch calls by name. |
| `tools/fs.py`, `tools/shell.py` | The built-in tools, **jailed to a working directory**. |
| `permissions.py` | The gate: `ask` / `auto` / `readonly`, allowlist, path jail. |
| `tracing.py` | JSONL events + token/cost accounting. |
| `llm.py` | Thin Anthropic SDK wrapper (adaptive thinking, effort, tools). |
| `agent.py` | The loop that ties it all together (optionally drives OTel). |
| `evals/runner.py` | Run fixtures in a sandbox, grade with deterministic checks. |
| `routing.py` | LLM routing layer — pick model by task (Sprint 2). |
| `mcp_server.py` | Expose the tools over MCP (Sprint 2). |
| `mcp_bridge.py` | Consume a remote MCP server as `Tool`s (Sprint 2). |
| `tracing_otel.py` | OpenTelemetry GenAI spans alongside the JSONL trace (Sprint 2). |
| `governor.py` | Cost/token/tool-call budget + kill switch (Sprint 3). |
| `redaction.py` | PII/secrets scrubbing on traces + audit (Sprint 3). |
| `policy.py` | Policy-as-code permission gate from YAML (Sprint 3). |
| `audit.py` | Append-only, hash-chained audit log (Sprint 3). |
| `metrics.py` | Prometheus metrics (Sprint 3). |
| `sandbox.py` | Local / Docker execution backends for `run_shell` (Sprint 3). |

## Evaluation methodology

Evals live in `agent_workbench/evals/`. Each fixture is a task plus checks on
the outcome (file exists / file contains / final answer contains). The runner
executes the agent in a **throwaway temp directory** with permissions on `auto`,
then grades deterministically — **no LLM-as-judge**, so results are reproducible
and free to verify. This is the seed of eval-driven development: add a fixture
for every behavior you care about, and you'll know when a prompt change breaks
something. See [`evals/README.md`](agent_workbench/evals/README.md).

## Security model

- **Path jail.** `read_file` / `write_file` resolve paths against the working
  directory and refuse anything that escapes it (`..`, absolute paths, symlink
  tricks). Never trust a path that came from the model.
- **Permission gate.** Mutating tools (`write_file`, `run_shell`) require
  approval in `ask` mode; read-only tools run freely. Policy lives in one place,
  separate from the model and the tools.
- **Shell denylist + timeout.** `run_shell` blocks obvious foot-guns and times
  out — a tripwire, not a real boundary. Run the agent in a disposable sandbox
  (container/VM) for anything untrusted; `--permission-mode auto` should only be
  used there.
- **Secrets.** The API key comes from the environment, never code. Traces store
  tool inputs/outputs — don't point the agent at secrets you don't want logged.

## Failure modes (known + by design)

- **Runaway loops** → bounded by `AGENT_MAX_TURNS`; status reports `max_turns`.
- **Model asks for an unknown tool** → registry returns an error result; the
  model can recover. Unknown tools are treated as *mutating* (unsafe) by the gate.
- **Tool raises** → caught by the registry and returned as an error result, not
  a crash, so the loop keeps going.
- **No API key / SDK missing** → the loop errors cleanly; offline unit tests
  still pass (they use a fake LLM).
- **Cost blindness** → every run prints and logs USD cost; watch it.

## Sprint 2 additions — MCP + OpenTelemetry + routing

The starter has grown the first production-shaped layers:

- **MCP server** (`mcp_server.py`): expose the tools over the Model Context
  Protocol so any MCP client can use them. `make mcp-server` (or plug into
  Claude Desktop / the MCP Inspector). Same path-jail security boundary.
- **MCP client bridge** (`mcp_bridge.py`): consume a remote MCP server and adapt
  its tools into the workbench `Tool` interface — the sync agent loop drives an
  async MCP session on a background event loop. Remote tools are gated as
  mutating by default. Round-trip is covered by an integration test.
- **OpenTelemetry GenAI tracing** (`tracing_otel.py`): run with `--otel` to emit
  spans (`agent.run` → `chat <model>` → `execute_tool <name>`) with GenAI
  semantic-convention attributes (tokens, cost, finish reason, tool name). View
  in Jaeger via [`observability/`](observability/) (`make otel-up`).
- **LLM routing** (`routing.py`): `--route` picks the model from the task
  (cheap → Haiku, balanced → Sonnet, heavy/agentic → Opus) to cut cost.

Security model for MCP (both directions) is written up in [`MCP_SECURITY.md`](MCP_SECURITY.md).

```bash
make otel-up                       # start collector + Jaeger
python -m agent_workbench.cli --route --otel --workdir .sandbox --permission-mode auto \
    "refactor greet.py to take a name argument, then run it"
open http://localhost:16686        # see the trace
```

## Sprint 3 additions — production hardening

The harness now has the governance/security/observability backbone a "type 3"
engineer is expected to build:

- **Cost governor + kill switch** (`governor.py`): per-run budget on dollars,
  tokens, and tool calls. The loop checks it after every LLM/tool call and stops
  with status `budget_exceeded`. `--max-usd`, `--max-tool-calls`.
- **PII / secrets redaction** (`redaction.py`): scrub emails, cards (Luhn),
  AWS/JWT/`sk-`/`ghp_` tokens, private keys, and high-entropy secrets from the
  trace and audit log before they hit disk. `--redact`.
- **Policy-as-code gate** (`policy.py` + `policy.example.yaml`): per-tool
  allow/ask/deny plus path and command denylists, from a reviewable YAML file —
  drop-in for the simple permission gate. `--policy policy.example.yaml`.
- **Audit log** (`audit.py`): append-only, **hash-chained** record of every
  mutating action + the decision that gated it. `verify()` detects tampering —
  the fintech audit-trail pattern in miniature. `--audit audit.jsonl`.
- **Prometheus metrics** (`metrics.py`): run/LLM/tool counters, cost counter,
  latency histograms. `--metrics-file agent.prom` (textfile-collector pattern).
- **Sandboxed execution** (`sandbox.py`): run `run_shell` in an ephemeral Docker
  container with networking off, instead of on the host. `--sandbox docker`.
- **Prompt caching** (`config.py` / `llm.py`): the stable system+tools prefix is
  cached so turns 2+ in a run read it at ~0.1x. `AGENT_CACHE=0` to disable.

```bash
# hardened run: budget cap, redaction, audit, policy-as-code, sandbox
python -m agent_workbench.cli \
    --policy policy.example.yaml --redact --audit audit.jsonl \
    --max-usd 0.50 --sandbox docker \
    --workdir .sandbox "refactor greet.py to take a name and run it"
```

## Production considerations (what's still ahead)

This is a learning starter. Still on the roadmap: parallel-safe tool scheduling,
a long-running service form with a live `/metrics` endpoint + Grafana
dashboards, semantic caching, rollback/compensating actions, and wiring the
audit log into an append-only store. The code is structured so each slots in
without a rewrite — see the per-sprint guides in `../../learning/sprints/`.

## What I learned

_(Fill this in as you build — it's the highest-signal part of a portfolio repo.)_
Examples to write up: why the assistant turn must be replayed verbatim with
thinking blocks; how token/cost accounting maps to `usage`; why deterministic
eval checks beat LLM-as-judge for a regression suite; where the permission gate
belongs in the architecture.
