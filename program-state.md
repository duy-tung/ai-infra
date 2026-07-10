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
| SC-T001 docs+policy bootstrap | done (21 files; policy review queued RQ-8) | /home/user/serving-contracts/docs, compatibility | serving-contracts@e4b93ba |
| SC-T002 inference API contract | done (spec valid: redocly 0 errors + openapi-spec-validator OK re-run by orchestrator; 17 positive + 14 negative fixtures, 81/81 checks) | /home/user/serving-contracts/openapi, examples/api | serving-contracts@40e2127 |
| SC-T003 benchmark data schemas | done (orchestrator re-validated: 5 schemas meta-valid, 8 workloads valid) | /home/user/serving-contracts/schemas, examples | serving-contracts@2df86b1 |
| SC-T004 backend-capability schema | done (3 descriptors re-validated) | examples/capabilities | serving-contracts@f933c43 |
| SC-T005 metrics vocabulary | done (agent cross-check: 11/11 Contract-2 metrics exact; semconv pinned v1.34.0 flagged re-verify) | /home/user/serving-contracts/metrics | serving-contracts@80f2507 |
| SC-T008 consumer compat kit | done (selftest independently re-run: GREEN, 32/32 pos, 20/20 neg) | /home/user/serving-contracts/kit | serving-contracts@6e92e1e |
| SC-T009 release v0.1.0 | done (user review passed 2026-07-10; tag v0.1.0 cut at 2df9f81; Apache-2.0 + github $id applied; post-review validation green) | RELEASES.md + tag v0.1.0 | serving-contracts@2df9f81 |
| IG-T001 docs bootstrap | done (15 docs + 7 ADRs verified present; boundary section + ADRs join Wave-1-exit review batch) | /home/user/infergate/docs | infergate@a8bb988 |
| IG-T002 skeleton+mock+non-stream | done (orchestrator re-ran go vet + go test -race: all green; 45 tests/62 subtests; conformance vs kit fixtures green, streaming skipped per scope) | /home/user/infergate | infergate@a5a2c02 |
| IG-T004 config snapshots+drain | in-progress (subagent) | — | — |
| IL-T001 skeleton (pins/scenarios) | done (39 files; pins validator independently re-run green; structure review joins Wave-1-exit batch) | /home/user/inference-lab (pins/, scenarios/, docs/) | inference-lab@6a219e2 |

### Wave 2 (overlap-started: contracts stable + verified, tag review pending)

| Task | Status | Evidence | Commit |
|---|---|---|---|
| IG-T003 SSE relay + cancellation (G2) | done-pending-G2-verify (orchestrator re-ran vet + race suite: all green; agent evidence: 100 streams no mixing, cancel release 122-321µs vs 100ms bound, 10-run 260/260; fresh-context G2 verifier dispatched) | /home/user/infergate docs/implementation-notes.md | infergate@08a529c |
| G2 gate verification | **PASSED 2026-07-10** — fresh-context verifier re-ran all evidence (10x race-clean, cancel release 124-630µs vs 100ms bound) + 5 adversarial fake-upstream probes all correct (EOF-without-DONE, zero-chunk-DONE, double-DONE, oversized event, death-after-usage). Non-blocking: slow-client stall test deferred to scenario-4 work (bound exists in code). Evidence queued for user review (batch, Wave-2 exit). | verifier report (task a394e35) | infergate@08a529c |
| IG-T006 observability per contract | done (orchestrator re-ran telemetry+gateway race tests green; 11 canonical metrics conformance-tested against vendored contract; span sequence verified live; OTel v1.40.0 justified dep; ADRs flipped Accepted + LICENSE) | /home/user/infergate/internal/telemetry + docs/implementation-notes.md | infergate@294c711 |
| llama.cpp build + tiny-GGUF fallback probe (IG-T005 prep) | done — llama.cpp @8f114a9 built (CPU, 5m27s); 8.9MB tiny GGUF (real 32k SPM vocab + random 2-layer weights) serves at 750-2100 t/s; SSE + [DONE] + usage chunk correct; mid-stream disconnect frees slot ~53ms; /metrics shape recorded; trap documented (http.client sock.close is a false-negative for cancel tests — use raw shutdown()). IG-T005 correctness can proceed on tiny model; real 1-3B GGUF still wanted for I3 measurement realism (RQ-10). | /home/user/tools/llamacpp-probe-report.md | n/a (scratch) |
| IB-T002 open-loop generator + raw events | **done** (CO re-review passed; all verification evidence green) | /home/user/inferbench + docs/evidence/ib-t002 | inferbench@2828f12 |
| IB-T002 CO-safety review (stop condition) | **FAILED 2026-07-10** — verifier demonstrated hidden connect-time queueing (latency clock starts at wire-write, not scheduled send; watchdog blind to dial/TLS/write window; 2s hidden per request in probe, run still reported VALID). Send-schedule half PASSED. Fix plan below. | verifier report (task afc43a0f) | — |
| IB-T003 workload suite v1 | done (orchestrator re-verified: 8/8 kit-valid, race tests green; 5 runnable workloads dry-ran 574/574 ok; 3 deferred features show typed refusals; contracts re-pinned v0.1.0) | /home/user/inferbench/workloads + docs/evidence/ib-t003 | inferbench@05ab858 |

### Bootstrap-pulled-forward (per goal §2: initialize every repo with *-T001)

| Task | Status | Evidence | Commit |
|---|---|---|---|
| IB-T001 docs bootstrap | done (15 docs + 4 ADRs verified present; ADRs join Wave-1-exit review batch) | /home/user/inferbench/docs | inferbench@f65f15d |
| FL-T001 docs bootstrap | done (15 docs + ADR-0001 verified present; ADR review queued) | /home/user/fleetlab/docs | fleetlab@adf7122 |
| IO-T001 docs bootstrap + tooling ADR | done (15 docs + ADR-0001 verified present; ADR review queued) | /home/user/inferops/docs | inferops@2c25196 |

| SC-T006 deployment+fault contracts | done (orchestrator re-ran selftest GREEN 52/52+28/28; git diff v0.1.0 over old surface empty = strictly additive; 12/12 scenarios) | schemas + examples/{deployment,faults} | serving-contracts@a69da9a |
| SC-T007 fleet schemas | done (same verification; provenance structural; Scenario E expressible end-to-end) | schemas + examples/{fleet,capacity} | serving-contracts@0daabd7 |
| SC v0.2.0 prep + raw-event CO amendment | done (orchestrator verified scheduled_send_ts required=True; selftest 52/52+29/29 GREEN; migration note written; tag review-queued) | RELEASES.md v0.2.0 entry | serving-contracts@8d81492 |
| IB-T002 CO re-review | **PASSED 2026-07-10** — verifier's original 2s-dial attack now fully surfaces (TTFT 2.002-2.014s recorded, hidden=0.000s) or trips typed wire abort (41/60 sent, ABORT); never-sent-request probe produces honest error events, nothing understated. Non-blocking notes: send_slip should be absent when send never completed (handed to IB-T004); IB-T005 analyzer MUST gate latency quotes on error/shed rate. IB-T002 stop condition met. | verifier re-report (task afc43a0f) | inferbench@2828f12 |
| IB-T004 streaming client correctness | in-progress (subagent; incl. cancellation + slow-client profiles, mock calibration, ib-t003 evidence regen) | — | — |

All other register tasks (05 §8): todo, gated by wave order.

## 2. Wave & gate status

- Wave 1: **EXITED 2026-07-10.** Contracts v0.1.0 released (reviewed + tagged); gateway serves non-streaming from mock (verified); infergate conformance green vs fixtures (I1 partial — inferbench wires the kit at IB-T002, fleetlab/inferops at their first consuming tasks). G1 = partially satisfied (fixtures validate + first consumer green); full I1 needs all four consumers.
- Wave 2: **active**. G2 PASSED (fresh-context verified). IG-T003 done. IB-T002 awaiting measurement fix + re-review. SC v0.2.0 prepared (incl. raw-event CO fix + migration note), tag review-queued.
- G1–G10: none passed. I1–I8: none accepted.

## 3. Pins

Mirrors /home/user/inference-lab/pins/pins.yaml (validator green):
- contracts-bundle: serving-contracts **v0.1.0** (tag at 2df9f81, local-only until remotes exist), pinned 2026-07-10.

## 4. Review queue

| Item | Question | Blocks | State |
|---|---|---|---|
| RQ-1 | Six-repo strategy | — | **answered 2026-07-10: six repos** |
| RQ-2 | GPU budget envelope | G6/Wave 4 GPU work | **answered 2026-07-10: $150–250, alerts 50%/80%, ≤6 sessions, per-session approval** |
| RQ-3 | OSS primary target | IL-T010 (Wave 3) | **answered 2026-07-10: GAIE primary, OTel GenAI semconv secondary, vLLM fallback** |
| RQ-4 | Remote hosting: user approved creating 6 public GitHub repos, but the GitHub integration returned 403 (cannot create repos). **User action needed:** create empty repos duy-tung/{serving-contracts,infergate,inferbench,fleetlab,inferops,inference-lab} (public, no README) and say "repos created" — orchestrator then adds them via add_repo and pushes. | durable component hosting (work is container-local until then) | waiting-on-user since 2026-07-10 |
| RQ-5 | Career-overlay exclusion (13 §7.4) | nothing | default applied (excluded); user may override |
| RQ-10 | Network allowlist: add huggingface.co to this environment's network policy (claude.ai/code environment settings) so IG-T005/I3 can download a small GGUF (1–3B). Alternatives exist but are worse (see blind-spot register). | IG-T005/I3 (Wave 2, soon) | waiting-on-user since 2026-07-10 |
| RQ-9 | Wave-1 exit review | — | **passed 2026-07-10: v0.1.0 approved+tagged; Apache-2.0 license all repos; $id -> github.com/duy-tung path; ALL queued ADRs accepted** (infergate/inferbench ADR status-line flips deferred until their active agents land — avoid concurrent-commit conflicts) |
| RQ-6 | inferops ADR-0001 | — | **accepted 2026-07-10** (inferops@7ca8870) |
| RQ-7 | fleetlab ADR-0001 | — | **accepted 2026-07-10** (fleetlab@da01bb4) |
| RQ-8 | SC compatibility policy + ADRs | — | **accepted 2026-07-10** (part of release review) |

## 5. Budget ledger

GPU spend: $0. Envelope: $150–250 (user-confirmed 2026-07-10). Alerts at 50%/80%. Additional environment constraint: no GPU rental access from this remote container — GPU sessions will need user-provided access or CPU fallback (05 §5).

## 6. Environment blind-spot register (iteration-0 pass, all facts measured 2026-07-10)

| Fact | Status | Impact / mitigation |
|---|---|---|
| Go 1.24.7, Python 3.11.15, Node 22, make, jq, cargo | present | covers SC/IG/IB/FL toolchains |
| Docker 29.3.1 + compose v5.1.1 | daemon NOT auto-started; `dockerd` starts cleanly on demand (verified) | start dockerd per session; record in runbooks |
| kubectl / kind / k3s / helm | absent | install at Wave 4 (kind via `go install`, kubectl via dl.k8s.io — reachability unverified, re-check at IO-T001/T002) |
| Network: proxy-mediated; pypi/proxy.golang.org/npm open; ghcr.io+docker.io reachable (401 = auth, OK) | verified | module/image pulls should work |
| huggingface.co, registry.ollama.ai, hf-mirror.com, modelscope.cn | **all blocked** (proxy CONNECT 403, policy; re-tested 2026-07-10) | objects.githubusercontent.com reachable — GitHub release assets downloadable. Plan for IG-T005/I3: (a) user adds huggingface.co to the environment network allowlist (RQ-10, preferred), else (b) GGUF from a GitHub-hosted mirror repo/release asset, else (c) author a tiny GGUF via pypi `gguf` for correctness-only testing (benchmark validity then needs a real model later) |
| Third-party GitHub clones (llama.cpp tested) | work via git proxy | llama.cpp build from source viable |
| GPU access | none in this environment | G6 will present options: user-provided remote GPU, or documented CPU fallback (llama.cpp) per 05 §5 |
| Disk: 30G avail; RAM 15G; 4 cores | adequate for CPU waves | kind + models may be tight — monitor |
| gh CLI | absent | GitHub via MCP tools only; session repo scope currently duy-tung/ai-infra only |

## 7. Lessons

- (2026-07-10) Remote-branch `claude/impl-infer-status-check-8mjyak` had been deleted on GitHub while the local clone still showed a stale tracking ref — always `fetch --prune` before reasoning about remote state.
- (2026-07-10) dockerd must be started manually in this container (`nohup dockerd &`); it initializes in ~6s.
- (2026-07-10) A heredoc quoting bug silently skipped a pins.yaml edit while the commit (with a message claiming the pin) still went through — always re-run the relevant validator/check AFTER the edit and BEFORE committing; caught because the validator printed "0 artifact entries".
- (2026-07-10) Session token limits can kill all background subagents mid-task simultaneously (windows observed resetting 3:50am and 9am UTC); partial work survives on disk and agents resume via their transcript with a "continue from disk state" message — schedule the fallback heartbeat AFTER the reset time when a limit hit is known.
- (2026-07-10) The Agent tool can transiently fail when its safety classifier model is unavailable — retry later; read-only work continues meanwhile.

## 8. Deviations index

- None yet. Each repo keeps `docs/implementation-notes.md` § Deviations; links accumulate here.
