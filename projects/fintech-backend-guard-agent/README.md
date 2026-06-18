# fintech-backend-guard-agent

> **Status: ✅ runnable starter.** The deterministic static-check core and the
> offline eval are implemented and tested (31 unit tests; 7 eval fixtures at
> precision/recall = 1.00). The LLM reviewer layer is wired and testable with a
> scripted client (real runs need `ANTHROPIC_API_KEY`). Sprint 4 of the plan;
> pairs with the hardening patterns from [`../agent-workbench/`](../agent-workbench/).

An AI agent that reviews a backend pull request **for fintech-specific risk** —
not code style. It reads the diff, migrations, tests, and service context, then
flags the failure modes that actually cause incidents and money loss in payment
systems, with a severity and a suggested fix.

## Why this project

A generic "AI code reviewer" is a commodity. A reviewer that understands
**idempotency, ledgers, reconciliation, and migration lock risk** is a moat —
it pairs AI-infrastructure skill with fintech domain knowledge. That combination
is what a "type 3" engineer offers. See
[`../../learning/00-goal-and-target-roles.md`](../../learning/00-goal-and-target-roles.md).

## Quickstart

```bash
cd projects/fintech-backend-guard-agent
python -m pip install -e ".[dev]"

make test          # 31 unit tests (offline, no API key)
make eval          # static-check eval over fixture PRs (offline)

# review a diff — static checks only, no API key
git diff main | python -m fintech_guard.cli
# enforce a merge gate (exit 1 if any finding >= threshold)
git diff main | python -m fintech_guard.cli --enforce --threshold high
# add the LLM reviewer (needs ANTHROPIC_API_KEY)
git diff main | python -m fintech_guard.cli --llm
# JSON for a bot / CI
python -m fintech_guard.cli --diff pr.diff --json
```

## What's implemented vs. ahead

| Piece | Module | Status |
|-------|--------|--------|
| Diff parser | `diff.py` | ✅ |
| Static checks (risk taxonomy) | `checks.py` | ✅ money_float, migration locks, idempotency, secrets/PII, error-swallow, audit |
| Secret/PII detection + pre-LLM scrubbing | `redaction.py` | ✅ |
| LLM reviewer (structured output) | `reviewer.py` | ✅ (fake-client tested; real runs need a key) |
| Merge + severity gate + report (md/json) | `report.py` | ✅ advisory by default |
| Pipeline (workflow) | `pipeline.py` | ✅ |
| CLI | `cli.py` | ✅ |
| Offline eval (precision/recall) | `evals/` | ✅ 7 fixtures |
| PR comment bot, OTel/metrics, more checks, sandboxed test-run | — | 🔜 next |

It's a **workflow**, not an agent loop: PR review is well-specified, so the code
orchestrates the steps and only calls the model for the judgment-heavy part. The
deterministic path runs with no API key — which is what makes the eval offline.

## What it checks (the risk taxonomy)

- **Idempotency** — does a retried request double-process? (missing idempotency key)
- **Retry → double charge** — retries on a non-idempotent payment path.
- **Transaction boundary** — work that should be atomic split across transactions.
- **Decimal / money precision** — float used for money; rounding errors.
- **Ledger imbalance** — debits/credits that don't sum to zero.
- **Reconciliation gap** — a state with no reconciliation/settlement path.
- **SQL migration lock risk** — migrations that take long locks on hot tables.
- **Audit log** — state-changing action with no audit trail.
- **PII / secrets** — PII logged, secrets committed.
- **Missing metric / span** — critical path with no observability.
- **Rollback plan** — change with no safe rollback.
- **Test coverage for failure cases** — happy path only; no failure/timeout tests.

## Architecture

```
Git diff
  → Context loader        (diff + migration SQL + service ownership + test output + logs/traces)
  → Fintech risk classifier   (rule-based pre-filter + LLM)
  → Static checks         (deterministic: precision, migration lock, idempotency-key presence, …)
  → LLM reviewer          (structured output: finding + severity + rationale + suggested patch)
  → Test / eval runner    (run the PR's tests in a sandbox)
  → Human approval gate   (advisory-only at first; never auto-blocks merge initially)
  → Report                (severity-ranked findings + suggested patches + confidence)
```

Reuses from `agent-workbench`: the agent loop, tool registry, permission gate,
sandbox runner, tracing/cost, and the eval-runner pattern.

## Tech stack

- **Go** for the backend service (matches the fintech profile) — diff ingestion, report API.
- **Python** for the agent / eval harness / LLM tooling (Anthropic SDK).
- **Postgres** to store runs, findings, and eval results.
- **OpenTelemetry + Prometheus/Grafana** for observability.
- **GitHub Actions** (run on PR) + **Docker Compose** for local stack.
- Optional **MCP server** to expose repo/test tools.

## Evaluation methodology

- 30–50 fixture PRs in `evals/fixtures/` — at least one per risk category, each
  with the expected findings (severity + category).
- Deterministic grading: did the agent flag the seeded risk? Track **precision**
  and **recall** per category, plus **false positives**.
- Regression: every real miss becomes a new fixture.

## KPIs to measure (and put on your CV)

review precision · false-positive rate · bugs caught · cost per PR · median
review latency · % PRs auto-classified to the right risk · time saved · escaped
bugs after adopting the checklist.

## Build order (v1 → hardened)

1. Context loader (diff + migration + test output).
2. Static checks (the deterministic subset — cheap wins, no LLM).
3. LLM reviewer with a severity rubric (structured output).
4. Eval set + grading.
5. Report + human approval gate (advisory-only).
6. Dashboard (runs, pass/fail, cost, latency, risk categories).
7. PR comment bot + OTel spans + Prometheus metrics + canary mode.

## Required README sections (fill when building)

What I learned · Production considerations · Failure modes · Security model ·
Evaluation methodology · Architecture diagram · Demo.

---

> ⚠️ When public: **anonymize everything** tied to your employer. Use synthetic
> fixtures only — never real fintech data.
