# Building an Agent Control Plane — a backend engineer's path into AI infrastructure

> **Draft — personalize before publishing.** Written in the first person as a
> starting point; replace with your own voice, numbers, and story.

Most "AI engineer" content is about *using* models — better prompts, RAG, a
chatbot. I wanted to learn the layer underneath: the **platform, evaluation,
observability, and safety machinery that lets agents work inside a real codebase
with control, measurement, rollback, and audit.** Coming from fintech backend
(Go/Postgres), that framing also plays to a moat: an agent that understands
*idempotency, ledgers, migrations, and audit trails* is worth more than a
generic code reviewer.

So instead of taking a 500-lesson course linearly, I used it as a menu and built
three small, runnable repos that together form one story — an **Agent Control
Plane for AI-native software engineering**:

1. **agent-workbench** — a minimal coding-agent harness: agent loop, tool
   registry, permission/policy gate, sandbox, eval runner, tracing, MCP, a cost
   governor, redaction, and a tamper-evident audit log.
2. **fintech-backend-guard-agent** — a PR-review agent that flags *fintech
   risk* (idempotency, money precision, migration locks, ledger/audit gaps,
   secrets) and posts a sticky PR comment.
3. **ai-incident-triage-agent** — a read-only assistant that correlates an alert
   with recent deploys and errors to propose a ranked root cause, blast radius,
   rollback candidate, and timeline.

## The pattern that ties them together: deterministic core + optional LLM layer

The single most useful decision was to **not** make everything an agent. PR
review and incident triage are well-specified problems, so I built them as
**workflows**: a deterministic core does the structured work, and the LLM is
called only for the judgment-heavy part.

That split pays off three ways:

- **Evals run offline.** The deterministic path needs no API key, so the eval
  suite is reproducible, free, and CI-able. fintech-guard grades 33 fixture PRs
  across 14 risk categories; incident-triage grades top-1/top-3 suspect-deploy
  accuracy — all without a network call.
- **Cost is bounded by design.** The LLM is one step, not an open loop.
- **The model does what only it can.** Pattern-matchable risks are caught
  precisely by code; the fuzzy ones (a transaction boundary split across two
  writes) go to the model.

I only reached for a real agent *loop* in the harness itself, where the task is
genuinely open-ended.

## What I learned

**Evals catch a different class of bug than unit tests.** While expanding the
guard's eval set from 7 to 33 fixtures, two real bugs surfaced that every unit
test had missed:
- A regex matched `account` but not `accounts` — the `\b` word boundary breaks
  on the plural `s`, so ledger writes to `accounts`/`transactions` were silently
  dropped.
- A case-insensitive `POST` pattern (meant to detect HTTP handlers) matched the
  word "post" inside `audit.record("post")`, producing a false "missing
  idempotency" finding.
Both only appear when you grade a *broad* set of realistic inputs. Unit tests
encode what you already thought of; evals encode what the system should do, and
the gap between those is where bugs live.

**Driving the agent loop by hand is worth it.** In the harness I use a manual
agentic loop instead of the SDK's tool runner, specifically so I can gate, log,
time, and cost-account *every* tool call. A subtle requirement: you must replay
the assistant turn — including thinking blocks — back to the API verbatim before
sending tool results, or the pairing breaks.

**Bridging sync and async is a real design problem.** The agent loop is
synchronous; the MCP client is async. I run the MCP `ClientSession` on a
dedicated background event loop and submit each tool call with
`run_coroutine_threadsafe`, opening the session once and keeping it alive — so
the sync loop, permission gate, and tracing all work unchanged against remote
tools.

**Safety is layered, and most of it is boring code.** Path jails, a permission
gate (ask/auto/readonly) backed by policy-as-code, a hash-chained audit log that
detects tampering, PII/secrets redaction before anything hits disk or the model,
a cost governor with a kill switch, and read-only-by-default for the incident
agent. None of it is glamorous; all of it is what makes agents safe to point at
a real system.

**Observability is the same shape everywhere.** All three repos emit
OpenTelemetry GenAI-convention spans with token and USD cost on every model
call. Starting with plain JSONL traces and graduating to OTel meant I could
build evals and cost accounting before standing up a collector.

## Failure modes I designed for

- Runaway loops → a hard turn cap + a cost governor that kills the run.
- Heuristic false positives/negatives in the guard → advisory-by-default gate, a
  clean-PR fixture set as a precision guard, and an LLM layer for the fuzzy
  cases.
- Correlation ≠ causation in triage → it proposes a *candidate*; a human acts.
- Secrets/PII in diffs and logs → redaction before egress and before disk.

## Where it goes next

Prometheus metrics + a Grafana dashboard across the three; live telemetry
connectors for the incident agent; richer fixtures from real (anonymized)
incidents and PRs; and running the LLM layers end-to-end against production-like
traffic in advisory mode.

The throughline: I'm not trying to know all of AI. I'm trying to be the person
on a fintech backend team who can make AI-assisted delivery **safe, measured,
and reversible** — and these three repos are the evidence.
