# Program State — inference-systems portfolio

Orchestrator state file. Rewritten every iteration; recoverable from this file + git alone.
Last updated: iteration 0 (bootstrap), 2026-07-09.

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
| SC-T001 policy+docs bootstrap | in-progress (agent dispatched iter 0) | — |
| SC-T002 inference API contract | in-progress | — |
| SC-T003 benchmark data schemas | in-progress | — |
| SC-T004 backend-capability schema | in-progress | — |
| SC-T005 metrics vocabulary | in-progress | — |
| SC-T008 consumer compatibility kit | in-progress | — |
| SC-T009 release v0.1.0 | todo (needs SC-T002–T005,T008 verified) | — |
| IL-T001 inference-lab skeleton | in-progress (agent dispatched iter 0) | — |
| IG-T001 infergate docs bootstrap | in-progress (agent dispatched iter 0) | — |
| IG-T002 gateway skeleton + mock | todo (needs SC-T002) | — |
| IG-T004 config snapshots + drain | todo (needs IG-T002) | — |
| All other tasks | todo | — |

## Pins

- contracts bundle: none released yet (target v0.1.0 at SC-T009).
- engine pins (from plan, re-verify at use): vLLM v0.24.x; llama.cpp by commit at IG-T005; OTel GenAI semconv pinned at SC-T005.

## Review queue

| ID | Question | Blocks | Status |
|---|---|---|---|
| RQ-1 | Remote hosting: create six GitHub repos (`serving-contracts`, `infergate`, `inferbench`, `fleetlab`, `inferops`, `inference-lab`) under your account? Needed for durability (this container is ephemeral) and for OSS-visible portfolio. | Nothing immediately; durability risk grows each wave | open (surfaced iter 0) |
| RQ-2 | Confirm four planning defaults (13 §7): six-repo strategy (default: yes), GPU budget envelope (default $150–250, alerts 50%/80%), OSS primary target (default: Gateway API Inference Extension), career overlay excluded (default: yes). | GPU spend (Wave 4) blocks on budget; rest proceed on defaults | open — defaults applied provisionally (surfaced iter 0) |

## Budget ledger (GPU)

Envelope: $150–250 (default, unconfirmed — RQ-2). Spent: $0. Sessions used: 0 of ≤6 target.

## Lessons

- L1: Docker daemon must be started manually (`sudo dockerd &`) after container restart — check before any compose/scenario work.
- L2: Component repos are local-only; commit early and often, and treat container loss as a real risk until RQ-1 is decided.

## Deviations index

- none yet (each repo keeps docs/implementation-notes.md §Deviations).
