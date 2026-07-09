# 06 — Execution Strategy

How the program is executed with Claude Code, parallel subagents, and reusable artifacts — and where automation is deliberately *not* trusted.

---

## 1. Session model

- **One repository per session (or per worktree).** Each implementation session is started with the matching standalone prompt from `portfolio-planning/prompts/`. Prompts are self-contained: they embed the contract summaries, ownership rules, task seeds, and the deviation policy, so a session does not need this planning repo checked out.
- **Autonomous mode (optional):** `prompts/06-implementation-loop.md` is a master orchestration prompt (user-requested addition) that drives all six repositories to I8 as a self-pacing Claude Fable 5 loop — dispatching the repo prompts to subagents, enforcing gates G1–G10 and the human-review rules below, hard-blocking on GPU spend and OSS postings, and persisting recovery state in `program-state.md`. It requires this planning repo to be present (it is the one prompt that is deliberately not self-contained).
- **First session per repo runs the planning tasks** (`*-T001`): create/refresh the `docs/` set before any implementation.
- **Cross-repo work happens only at integration milestones**, driven from `inference-lab` with pinned released artifacts — never by editing two repos in one session to "make it work".

## 2. Where to use subagents and automation aggressively

| Use | Examples |
|---|---|
| Mechanical generation | schema ↔ example fixtures, table-driven tests, dashboard JSON from the metrics vocabulary, runbook skeletons |
| Parallel independent tasks | tasks marked `Par:yes` within one repo; doc bootstraps; fixture suites |
| Fresh-context verification | contract conformance review, ADR red-teaming, benchmark-report audit against the validity checklist |
| Source-reading scaffolds | vLLM/llama.cpp path walkthroughs producing sequence diagrams for the study track |
| Repetitive experiment execution | seeded benchmark reruns, fault-scenario replays, report regeneration |

## 3. Where speed is explicitly not evidence

Architecture reviews, controlled experiments, debugging sessions, upstream source reading, and verification gates are **mandatory thinking work**. Rules:

- A generated test suite proves nothing until its failure modes have been reviewed (a test that cannot fail is not evidence).
- Benchmark numbers are only claimable through the G4-approved pipeline (manifests, pooled percentiles, validity block).
- Every ADR gets human review; subagents may draft and red-team, not approve.
- GPU sessions are never unattended-automated beyond auto-stop safeguards.

## 4. Verification methodology (applies to every task)

1. Each task ships with its verification command/procedure (see register) — run it, capture output, link it in the evidence location (`inference-lab` for cross-repo, repo `docs/` for local).
2. `go test -race` clean is the floor for all Go concurrency work.
3. Contract conformance = fixtures from the pinned bundle version, run in CI.
4. Claims discipline: tests failed → say so; step skipped → say so; no "should work".
5. Fresh-context verifier subagents audit at wave exits: scope drift, boundary violations (gateway/engine), unsupported claims, dependency violations.

## 5. Deviation policy (embedded in every prompt)

> Keep `docs/implementation-notes.md`. When repository evidence forces a deviation from the approved plan, choose the conservative reversible option, record the evidence, decision, consequences, and follow-up under `Deviations`, and continue. Pause only when the deviation changes public contracts, repository ownership, security posture, or milestone scope.

## 6. Reusable artifacts to build once

- Contract validation kit (SC-T008) reused in four CIs.
- Mock backend image (IG) reused by inferbench CI, inferops smoke tests, and demos.
- Benchmark report template + validity checklist (IB-T006) reused for every report.
- Fault-scenario scripts + observation checklists (IO-T006/T007) reused across campaigns and regression re-runs.
- GPU session runbook: hypothesis template + manifest capture + auto-stop + budget alert (first used at IG-T014, reused for every session).
- Pins file + compatibility matrix (`inference-lab`) as the single source of "what is proven together".

## 7. Human-review plan

Single reviewer. Mandatory reviews: contract releases; G2/G4/G5/G8 evidence; ADRs; GPU session plans; OSS submissions; consolidation triggers; anything touching the §5 pause list. Batched at wave exits. Expected review artifacts are always: a short summary, the evidence links, and the specific question to decide — never raw logs.

Optional comprehension check (from the Fable field-guide "quiz" pattern): before accepting a major wave exit, the user may ask the session for a change report with a short quiz over what was built and why; acceptance waits until the reviewer passes it. Use sparingly — it is a reviewer aid, not a gate.

## 7a. Session conduct (Claude Fable 5)

Every standalone prompt embeds a shared "Working style (Claude Fable 5)" block derived from the two prompting guides supplied by the user (Anthropic platform guide "Prompting Claude Fable 5", 2026-07; Thariq's "A Field Guide to Fable"). Its rules: session-start blind-spot pass with user interviews limited to architecture-changing ambiguities; act-when-informed (no re-deriving settled decisions); simplest-thing scope discipline (no unrequested features/refactors/abstractions; validate at system boundaries only); pause only for destructive/irreversible actions, real scope changes, or user-only input, and never end a turn on a promise; progress claims audited against session tool results; parallel subagent delegation with fresh-context verifier subagents at milestone gates; final messages that lead with the outcome and read standalone. Prompts deliberately remain prescriptive about *what* to build (contracts, tasks, acceptance criteria) and brief about *how* to behave — per the platform guide, over-prescribing behavior degrades Fable output, while well-specified problems get first-shot correctness.

## 8. Evidence and honesty rules (program-wide)

- Never fabricate repository state, tests, benchmarks, hardware, costs, or maintainer activity.
- Numbers carry provenance (measured / source-reported / assumed) and dates; volatile data (GPU prices, engine metric names, upstream repo layouts) is re-verified at use time.
- Failed or invalid runs are recorded as such; "invalidate, don't publish" applies to benchmarks.
- The OSS log records real interactions only; planned-but-not-sent communications are marked as drafts.
