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
| IG-T004 config snapshots+drain | done (orchestrator re-ran config+gateway race tests green; reload-under-traffic 60 streams x 27 publishes zero-drop; drain verified live; publish latency ~200µs vs 5s bound) | /home/user/infergate/internal/config + docs | infergate@5d69aeb |
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

| IG-T005 llama.cpp adapter | done (orchestrator re-verified: backend tests race-green incl. real-engine suite; descriptor kit-valid 1/1; 3-point cancel on real llama-server — mid-stream slot release 1.25-5.24ms, pre-first-token 0.77-2.19s at decode-batch granularity (real-engine finding, R14 material); failover demo clean; D2 tiny-GGUF deviation standing) | /home/user/infergate/internal/backend/llamacpp | infergate@74f2372 |
| IB-T005 analysis core (Python) | done (orchestrator re-ran: 70/70 pytest green, 7/7 result files kit-valid; pooling guard structural; error-gate makes quoting latency impossible above 5% error+shed; contract observations queued: nullable latency tables + CI fields for a future MINOR) | /home/user/inferbench/analysis + docs/evidence/ib-t005 | inferbench@10b2e61 |
| IB-T006 report generator + validity block (G4 artifact) | done (orchestrator re-ran: 103/103 pytest green; refusal-first rendering — reports cannot render without validity block/hypothesis/shed-adjacent goodput; withheld-latency case rendered honestly; G4 stays open until IB-T009 joins) | /home/user/inferbench/analysis + docs/evidence/ib-t006 | inferbench@69a5abc |
| IL-T003 Scenario B + I3 (llama.cpp, real Qwen2.5-1.5B) | in-progress (subagent) | — | — |

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
| IB-T004 streaming client correctness | done (orchestrator re-verified: client+run race tests green, kit check 7/7 valid; calibration 28/28 within tolerance, TTFT Δp50 ≈ +2.9ms; 3-point cancellation two-sided vs mock; slow-client 9.2x e2e effect; contract proposals logged for metrics.md §4 wording + nullable send_ts) | /home/user/inferbench docs/evidence/ib-t004 | inferbench@caa5074 |
| IL-T002 Scenario A + I2 evidence | evidence complete (154 concurrent streams 2736/2736 ok, 0 integrity violations; 3-point cancel deltas ≤0.72ms; TTFT agreement +1.9ms within declared 25ms; 7801 full-sequence traces, conservation exact; PostgreSQL deviation D-001 recorded honestly; deviations D-002/D-003: registry CDNs blocked → host-compiled scratch images + ocb-built collector) | /home/user/inference-lab/evidence/i2 | inference-lab@d0a858c |
| I2 milestone verification | **ACCEPTED (subject to user review) 2026-07-11** — fresh-context verifier reproduced every checklist number from raw artifacts (independent DP pairing matched greedy results; conservation exact; archive byte-identical to run output; live smoke re-compose byte-identical to archived transcript); PostgreSQL deviation D-001 judged legitimate (milestone-spec inconsistency); 2 wording nits fixed at inference-lab@e11b9c9 | verifier report (task a9929d1) | inference-lab@d0a858c |

All other register tasks (05 §8): todo, gated by wave order.

## 2. Wave & gate status

- Wave 1: **EXITED 2026-07-10.** Contracts v0.1.0 released (reviewed + tagged); gateway serves non-streaming from mock (verified); infergate conformance green vs fixtures (I1 partial — inferbench wires the kit at IB-T002, fleetlab/inferops at their first consuming tasks). G1 = partially satisfied (fixtures validate + first consumer green); full I1 needs all four consumers.
- Wave 2: **active — I2 ACCEPTED by user 2026-07-11** (G2 acknowledged; v0.2.0 released + tagged). Wave-2 exit needs I3 (IL-T003 running with the real Qwen2.5-1.5B GGUF).
- User actions RESOLVED 2026-07-11: six GitHub repos live (all mains pushed; KI-1 tag workaround = release/<version> branches); huggingface.co allowlisted (real model downloaded, sha256 to be pinned at I3).
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
| RQ-4 | Remote hosting | — | **RESOLVED 2026-07-11: user created the six repos; all six pushed (main verified on remote). Tag pushes are silently dropped by the session git proxy (known issue KI-1) — release/v0.1.0 branch pushed as the pinnable ref workaround; annotated tags remain authoritative locally.** |
| RQ-5 | Career-overlay exclusion (13 §7.4) | nothing | default applied (excluded); user may override |
| RQ-10 | HF network allowlist | — | **RESOLVED 2026-07-11: huggingface.co returns 200; real 1-3B GGUF download unblocked for I3 (clears deviation D2's perf-realism limitation)** |
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
- (2026-07-11) KI-1: the session git proxy pushes branches fine but silently drops tag refs ("Everything up-to-date" while the remote has no tags) — push release/<version> branches as pinnable refs; annotated tags stay authoritative in local history and get pushed when hosting is direct.

## 8. Deviations index

- None yet. Each repo keeps `docs/implementation-notes.md` § Deviations; links accumulate here.
