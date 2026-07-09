# Program State — inference-systems portfolio

Orchestrator state file. Rewritten every iteration; recoverable from this file + git alone.
Last updated: iteration 3 (IG-T002/T004 + SC-T006/T007 done; v0.2.0 tagged; IG-T003 dispatched), 2026-07-09.

## Environment (blind-spot pass, iteration 0 — re-verify on container restart)

- Container: 4 vCPU, 15 GiB RAM, ~30 GiB free disk, linux/amd64, **no GPU** (GPU work is rented, Wave 4+, behind G6).
- Toolchain (measured 2026-07-09): go 1.24.7 · Python 3.11.15 / pip 24.0 · node v22.22.2 · GNU Make 4.3 · jq 1.7 · git 2.43.0 · docker 29.3.1 + compose v5.1.1.
- **Docker daemon is not auto-started.** `sudo dockerd &` works; must be restarted after any container restart.
- kind / kubectl / kustomize / k3s: **not installed** — install at Wave 4 (IO-T002); network permitting.
- Network: outbound HTTPS via agent proxy. Verified working: Go module proxy (go get succeeded). PyPI assumed working (not yet exercised). GitHub API via MCP tools only (no `gh` CLI).
- Remote repos: session GitHub scope is `duy-tung/ai-infra` only. Creating six GitHub repos = external-resource hard block → review-queued (RQ-1). Components are **local-only git repos** until decided.
- Unknown unknowns logged: llama.cpp availability via proxy (Wave 2); model download (HuggingFace GGUF) via proxy (Wave 2); kind image pulls via proxy (Wave 4); GPU rental provider access from this environment (Wave 4, G6); container ephemerality — local component repos live only in this container until remotes exist (mitigation: RQ-1 decision, or bundle backups).

## Workspace layout

Planning repo: `/home/user/ai-infra` (branch `claude/inference-systems-orchestration-77l8wk`).
Components (side-by-side local git repos, branch `main`): `/home/user/serving-contracts`, `/home/user/infergate`, `/home/user/inferbench`, `/home/user/fleetlab`, `/home/user/inferops`, `/home/user/inference-lab`.

## Wave & gate status

- **Current wave: 1** (contracts core + gateway spine).
- Gates G1–G10: none passed. Milestones I1–I8: none accepted.

## Task board (Wave 1 scope; full register in portfolio-planning/05 §8)

| Task | Status | Evidence / commit |
|---|---|---|
| SC-T001 policy+docs bootstrap | done (verifier PASS) | serving-contracts `8a4de1f` |
| SC-T002 inference API contract | done (verifier PASS: exact field subset, 10 error classes, 36 fixtures) | serving-contracts `116d903` |
| SC-T003 benchmark data schemas | done (verifier PASS: pooled-percentile/shed-adjacent/validity-block enforced structurally) | serving-contracts `d604a72` |
| SC-T004 backend-capability schema | done (verifier PASS) | serving-contracts `f2d1b2d` |
| SC-T005 metrics vocabulary | done (verifier PASS: 11/11 metrics match Contract 2; semconv v1.36.0 pinned) | serving-contracts `15edc81` |
| SC-T008 consumer compatibility kit | done (verifier PASS: 65 checks green, negative tests exit 1) | serving-contracts `8173098` |
| SC-T009 release v0.1.0 | done — tag `v0.1.0` created after RELEASE-READY audit; release notes in docs/releases/v0.1.0.md; review queued (RQ-3); deviation D1 recorded in SC implementation-notes | serving-contracts `6619185` + tag |
| SC-T006 deployment+fault contracts | done (orchestrator re-ran validator: 103 checks green; 12 fault scenarios FS-01..12; grace>max-stream structural) | serving-contracts `f219e05` |
| SC-T007 fleet schemas | done (provenance-mandatory quantities; Scenario E worked example chain) | serving-contracts `f8a21a7`; released as tag `v0.2.0` |
| IL-T001 inference-lab skeleton | done (verified iter 0: pins validator green, 15-doc set present, clean tree) | inference-lab `4fb1036` |
| IG-T001 infergate docs bootstrap | done (verified iter 0: 15 docs + 7 ADRs, clean tree) | infergate `60458ac` |
| IG-T002 gateway skeleton + mock | done (orchestrator re-ran: vet clean, race tests ok, CONFORMANCE PASS; auth/permission/rate_limited deferred to IG-T007/T009 by design) | infergate `3d089cb`,`27969ae`,`1cd4431` |
| IG-T004 config snapshots + drain | done (reload under traffic 5421 req / 0 fail; publish 2.1ms vs 5s budget; e2e drain test green) | infergate `9f83e0a` |
| IG-T003 SSE relay + cancellation | in-progress (agent dispatched iter 3; G2 gate follows) | — |
| IB-T001 inferbench docs bootstrap | done (verified iter 2: 15 docs + 5 ADRs, pin v0.1.0 recorded, clean tree) | inferbench `b5cf196` |
| All other tasks | todo | — |

## Pins

- contracts bundle: **v0.2.0** latest (additive MINOR: Contracts 5–7); infergate + inference-lab pin **v0.1.0** (sufficient for Contracts 1–4 consumers until IO/FL wire in). I1 not yet run (consumers not wired).
- engine pins (from plan, re-verify at use): vLLM v0.24.x; llama.cpp by commit at IG-T005; OTel GenAI semconv pinned at SC-T005.

## Review queue

| ID | Question | Blocks | Status |
|---|---|---|---|
| RQ-1 | Remote hosting: create six GitHub repos (`serving-contracts`, `infergate`, `inferbench`, `fleetlab`, `inferops`, `inference-lab`) under your account? Needed for durability (this container is ephemeral) and for OSS-visible portfolio. | Nothing immediately; durability risk grows each wave | open (surfaced iter 0) |
| RQ-3 | Wave-1 exit review batch (non-blocking, queue-and-continue): infergate boundary doc (`infergate/docs/architecture.md` §1 + ADR-0001), inference-lab skeleton structure, and (when released) contracts v0.1.0 release notes. | Nothing — deviation policy allows continuing; feedback folded in when received | open (accumulating until Wave 1 exit) |
| RQ-2 | Confirm four planning defaults (13 §7): six-repo strategy (default: yes), GPU budget envelope (default $150–250, alerts 50%/80%), OSS primary target (default: Gateway API Inference Extension), career overlay excluded (default: yes). | GPU spend (Wave 4) blocks on budget; rest proceed on defaults | open — defaults applied provisionally (surfaced iter 0) |

## Budget ledger (GPU)

Envelope: $150–250 (default, unconfirmed — RQ-2). Spent: $0. Sessions used: 0 of ≤6 target.

## Lessons

- L1: Docker daemon must be started manually (`sudo dockerd &`) after container restart — check before any compose/scenario work.
- L2: Component repos are local-only; commit early and often, and treat container loss as a real risk until RQ-1 is decided.
- L3: Deterministic hashing in the mock needed a splitmix64 finalizer (raw FNV-64a clustered badly on short IDs) — reuse that pattern for any seeded determinism elsewhere.

## Deviations index

- none yet (each repo keeps docs/implementation-notes.md §Deviations).
