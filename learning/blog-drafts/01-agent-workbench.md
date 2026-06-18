# agent-workbench — a minimal coding-agent harness you can actually read

> **Draft — personalize before publishing.**

I wanted to understand agents from the inside, so I built the smallest harness
that still has the pieces a real agent platform needs: an agent loop, a tool
registry, a permission gate, tracing with cost, an eval runner — and later MCP,
OpenTelemetry, a cost governor, redaction, and a hash-chained audit log. It's
deliberately small enough to read in an afternoon.

## The loop, by hand

The core is a **manual agentic loop**: call the model, and while it asks for
tools, run them (through the permission gate), feed the results back, and call
again — until it's done or hits a turn cap. I drive it manually instead of using
the SDK's tool runner because that's the whole point of a workbench: I want to
gate, log, time, and cost-account every single tool call.

Two things I got wrong first and fixed:
- You must append the assistant turn — text, thinking, and `tool_use` blocks —
  back into the message history *verbatim* before adding tool results. The API
  requires the `tool_use`/`tool_result` pairing, and thinking blocks have to be
  replayed unchanged on the same model.
- Unknown tools and tool exceptions must become *results*, not crashes, so the
  model can recover and the loop keeps going.

## Tools, jailed

`read_file` / `write_file` / `run_shell` are registered in a `ToolRegistry`
that exposes schemas and dispatches by name. Every path is resolved under a
working directory and anything that escapes (`..`, absolute paths) is refused —
you never trust a path that came from the model. The shell tool runs behind a
`Sandbox` abstraction: local by default, or an ephemeral Docker container with
networking off for untrusted runs.

## Permission, policy, audit

Mutating tools go through a permission gate (`ask` / `auto` / `readonly`), or a
**policy-as-code** gate loaded from YAML (per-tool allow/ask/deny plus path and
command denylists). Every mutating action and the decision that gated it is
written to an **append-only, hash-chained audit log** — change or drop a record
and `verify()` detects the broken chain. That's the fintech audit-trail pattern
in miniature.

## MCP, both directions

The harness can expose its tools as an **MCP server** (any MCP client can use
them) and consume a remote MCP server through a **bridge** that adapts remote
tools into the same `Tool` interface. The interesting part was bridging the
synchronous agent loop to the async MCP client: a background event loop holds
the `ClientSession` open, and tool calls are submitted with
`run_coroutine_threadsafe`. Remote tools are treated as mutating by default.

## Eval, tracing, cost

A fixture-based eval runner runs the agent in a throwaway sandbox and grades
deterministically — no LLM-as-judge, so the regression suite is reproducible. A
JSONL tracer records every LLM and tool call with token usage and USD cost; an
optional OpenTelemetry tracer emits the same data as GenAI-convention spans into
Jaeger. A cost governor caps dollars/tokens/tool-calls per run and kills the run
when exceeded.

## What I'd build next

Parallel-safe tool scheduling (the registry already marks tools parallel-safe),
a long-running service form with a live `/metrics` endpoint, and semantic
caching. The architecture is intentionally additive — each of those slots in
without a rewrite.

**Repo:** `projects/agent-workbench` · 60 tests, all offline.
