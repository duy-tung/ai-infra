# Program State — Inference Systems Portfolio

Orchestrator loop state. Committed every iteration. Any iteration must be recoverable from this file + git evidence alone. A task is **done** only when its verification evidence exists — never trust a prior iteration's claim without evidence.

- **Iteration:** 0 (bootstrap)
- **Last updated:** 2026-07-10 (session start)
- **Current wave:** 1 (Contracts core + gateway spine) — entry condition met (plan approved by user goal directive)
- **Workspace:** six sibling repos at `/home/user/{serving-contracts,infergate,inferbench,fleetlab,inferops,inference-lab}`, each `git init -b main`, no remotes yet.

---

## 1. Task board

Status values: todo / in-progress / blocked-on(X) / review-queued / done. Evidence = link or path; done requires evidence.

### Wave 1 (active)

| Task | Status | Evidence | Commit |
|---|---|---|---|
| SC-T001 docs+policy bootstrap | in-progress (subagent) | — | — |
| SC-T002 inference API contract | todo (dep SC-T001) | — | — |
| SC-T003 benchmark data schemas | todo (dep SC-T001) | — | — |
| SC-T004 backend-capability schema | todo (dep SC-T001) | — | — |
| SC-T005 metrics vocabulary | todo (dep SC-T001) | — | — |
| SC-T008 consumer compat kit | todo (dep SC-T002/T003) | — | — |
| SC-T009 release v0.1.0 | todo (dep SC-T002–T005,T008) | — | — |
| IG-T001 docs bootstrap | in-progress (subagent) | — | — |
| IG-T002 skeleton+mock+non-stream | todo (dep SC-T002, IG-T001) | — | — |
| IG-T004 config snapshots+drain | todo (dep IG-T002) | — | — |
| IL-T001 skeleton (pins/scenarios) | in-progress (subagent) | — | — |

### Bootstrap-pulled-forward (per goal §2: initialize every repo with *-T001)

| Task | Status | Evidence | Commit |
|---|---|---|---|
| IB-T001 docs bootstrap | in-progress (subagent) | — | — |
| FL-T001 docs bootstrap | in-progress (subagent) | — | — |
| IO-T001 docs bootstrap + tooling ADR | in-progress (subagent) | — | — |

All other register tasks (05 §8): todo, gated by wave order.

## 2. Wave & gate status

- Wave 1: **active**. Exit gate: contracts v0.1.0 released; gateway serves non-streaming completions from mock; consumer fixture validation green (I1 partial).
- G1–G10: none passed. I1–I8: none accepted.

## 3. Pins

Nothing pinned yet (mirrors inference-lab pins file once IL-T001 lands). Planning repo HEAD at bootstrap: `74acaf7`.

## 4. Review queue

| Item | Question | Blocks | State |
|---|---|---|---|
| RQ-1 | Six-repo strategy | — | **answered 2026-07-10: six repos** |
| RQ-2 | GPU budget envelope | G6/Wave 4 GPU work | **answered 2026-07-10: $150–250, alerts 50%/80%, ≤6 sessions, per-session approval** |
| RQ-3 | OSS primary target | IL-T010 (Wave 3) | **answered 2026-07-10: GAIE primary, OTel GenAI semconv secondary, vLLM fallback** |
| RQ-4 | Remote hosting: user approved creating 6 public GitHub repos, but the GitHub integration returned 403 (cannot create repos). **User action needed:** create empty repos duy-tung/{serving-contracts,infergate,inferbench,fleetlab,inferops,inference-lab} (public, no README) and say "repos created" — orchestrator then adds them via add_repo and pushes. | durable component hosting (work is container-local until then) | waiting-on-user since 2026-07-10 |
| RQ-5 | Career-overlay exclusion (13 §7.4) | nothing | default applied (excluded); user may override |

## 5. Budget ledger

GPU spend: $0. Envelope: default $150–250 (unconfirmed). Alerts at 50%/80%. Additional environment constraint: no GPU rental access from this remote container — GPU sessions will need user-provided access or CPU fallback (05 §5).

## 6. Environment blind-spot register (iteration-0 pass, all facts measured 2026-07-10)

| Fact | Status | Impact / mitigation |
|---|---|---|
| Go 1.24.7, Python 3.11.15, Node 22, make, jq, cargo | present | covers SC/IG/IB/FL toolchains |
| Docker 29.3.1 + compose v5.1.1 | daemon NOT auto-started; `dockerd` starts cleanly on demand (verified) | start dockerd per session; record in runbooks |
| kubectl / kind / k3s / helm | absent | install at Wave 4 (kind via `go install`, kubectl via dl.k8s.io — reachability unverified, re-check at IO-T001/T002) |
| Network: proxy-mediated; pypi/proxy.golang.org/npm open; ghcr.io+docker.io reachable (401 = auth, OK) | verified | module/image pulls should work |
| huggingface.co | **blocked** (proxy CONNECT 403, policy) | GGUF download for IG-T005/I3 needs alternative (ollama registry, mirror, or user-side allowlist) — re-test at Wave 2; queue if still blocked |
| Third-party GitHub clones (llama.cpp tested) | work via git proxy | llama.cpp build from source viable |
| GPU access | none in this environment | G6 will present options: user-provided remote GPU, or documented CPU fallback (llama.cpp) per 05 §5 |
| Disk: 30G avail; RAM 15G; 4 cores | adequate for CPU waves | kind + models may be tight — monitor |
| gh CLI | absent | GitHub via MCP tools only; session repo scope currently duy-tung/ai-infra only |

## 7. Lessons

- (2026-07-10) Remote-branch `claude/impl-infer-status-check-8mjyak` had been deleted on GitHub while the local clone still showed a stale tracking ref — always `fetch --prune` before reasoning about remote state.
- (2026-07-10) dockerd must be started manually in this container (`nohup dockerd &`); it initializes in ~6s.

## 8. Deviations index

- None yet. Each repo keeps `docs/implementation-notes.md` § Deviations; links accumulate here.
