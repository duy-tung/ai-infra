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
| IL-T003 Scenario B + I3 (llama.cpp, real Qwen2.5-1.5B) | evidence complete (Sonnet finisher: reused the terminated agent's completed phases + re-ran cancel/checks/validate on idle box; (a) PASS 40/40+25/25; (b) PASS report #0, 3 arms, validity blocks incl. negative-overhead disclaimer; (c) DEVIATION — 21-vs-20 cancel-log census unreproduced, recorded open; (d) PASS failover 142s outage zero client failures; pins 13 entries validator green) | /home/user/inference-lab/evidence/i3 | inference-lab@4f5f3c1 |
| I3 milestone verification | **ACCEPTED by verifier AND user 2026-07-11** — all numbers re-derived exactly; deviation (cancel-log census) judged honest; 2 cosmetic nits fixed (inference-lab@b49093f); acceptance recorded in pins (proven_at [I3], milestone_evidence.I3) | verifier report (task a150717) + evidence/i3 | inference-lab@61132b2 |

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
- Wave 2: **EXITED 2026-07-11** — I2 and I3 both accepted (user review after fresh-context verification). G3 (local loop) = satisfied by I2+I3 acceptance.
- Wave 3: **EXITED 2026-07-11 on its wave-gate wording** (overload evidence produced: typed sheds + protected/accounted goodput; sweep/replay proven on mock with bracketed knee; OSS primary target built locally + reproduction ready). Open user decisions carried (AskUserQuestion UI failing — queued in chat): G5 resolution (recommend re-baseline per A9 after 2 honest REFUTEDs + mechanism analysis), RQ-13 ADRs, G4 ack.
- Wave 4: **active (CPU path per G6 decision)** — dispatched: IG-T012+T013 (routing + reliability, Sonnet), k8s env-prep probe (kind-vs-k3s + registry reality, Sonnet). Next: IG-T016 release → IO-T002 cluster baseline → IO-T003/T004 → IL-T004 (I4 CPU-fallback variant). Deferred pending GPU: IG-T014, IB-T011/T012.
- (superseded) Wave 3 was: active. Done+verified 2026-07-11: IG-T007 (infergate@102096c, revocation 74ms/1.0s vs 5s bound, no hot-path DB reads proven); IB-T008 (inferbench@e92d2df, bracketed knee at 21.12 rps found by unmodified detector, replay determinism, A/B mode, + seed-override bug found/fixed); IB-T009 (inferbench@2959d7c, hypothesis-gated experiment framework, 6 typed refusals demoed); IL-T010 (inference-lab@fff6f72, llm-d-router built + tested, #1625 fairness_id unbounded-cardinality reproduced — 5000 series demo, draft comment prepared). IG-T008 done (infergate@1dfbbc8 — settle variance 0.0000%, DB-outage backlog drained 765ms, idempotent ledger; orchestrator re-ran usage+quota race tests green) and IG-T009 done (infergate@977a9ea — RPM/TPM buckets, live 429+Retry-After verified; non-blocking open item: pre-settle headroom reading 58/208 not root-caused; also fixed a pre-existing cross-package DB test-isolation race). IG-T010 done (infergate@8ec9215 — bounded queues + global budget + typed 503 sheds, queue metrics real; H3 accepted-TTFT protection variance honestly attributed to tiny mock TTFT, D3) and IG-T011 done (infergate@6827d8c — WRR exact 30:10, aging ~20ms promotion, noisy-neighbor p95 shift 0.0-4.6% vs <15% target; orchestrator re-ran admission race tests green). IB-T010 done (inferbench@6a3fb53; orchestrator re-verified kit 31/31 valid): **benchmark report #1 published**. E1 gateway overhead: CONFIRMED on mock (paired p95 +2.21ms, p99 +2.81ms vs 10/20ms SLO), INCONCLUSIVE on llama.cpp at ms scale (real-engine variance dominates — honest). E2 admission value at 5x: **REFUTED on strict ≤20% accepted-TTFT criterion** (+25.16%, CI [+19.4,+31.1]%), root-caused (perpetually-full shallow queue adds one queue transit); companion criteria held (2067/2067 typed sheds + Retry-After, no starvation in declared scope). Deviations disclosed (discarded rebooted run, probe-only capacity, elevated gate thresholds).
**G5 verdict (Opus fresh-context, 2026-07-11): FAILED-FIRST-ATTEMPT on criterion 1 only** — every number reproduced to the digit (25.165% degradation, CI, shed typing 100%, time-to-shed p99 2.034ms); integrity clean (config pre-declared, no tuning-to-pass, discard procedural); criteria 2+3 verified PASS (incl. IG-T011's multi-tenant fairness evidence 0-4.6%); re-baseline explicitly rejected (fix is a documented knob). Root cause triple-confirmed (measured queue-wait, off-arm control, code). Now running: **E2b** (Sonnet) — prescribed single-variable re-run: queue caps 3→1, budget+deadline held; if E2b also fails, gate review-pauses to user (second failure same cause).
IG-T015 done docs-only during the benchmark (infergate@b424770, no CPU contention): ADR-0001 revocation consistency (bounded-staleness, measured 1.011s/74ms vs 5s bound), ADR-0006 tenant-config consistency (corrected an inaccurate prior-draft claim about admin CAS — honest gap note), ADR-0007 multi-gateway N-replica design (consensus-not-needed argument; ledger exactly-once via request_id PK). Review-queued (RQ-13, user review is the stop condition) — these three ADRs join the Wave-3 exit batch. **G4 PASSED 2026-07-11** (Opus fresh-context adversarial audit: all 5 bypass attacks refused — no validity-less reports, averaging inexpressible, gated latency withheld, hypothesis-less/combinatorial experiments refused pre-traffic, undisclosed closed-loop impossible; knee re-derived exactly from raw; sample report byte-reproducible; ADR-0002 params match code. 2 non-blocking notes: gate-threshold is a disclosed knob; contracts_bundle_version exempt from single-variable diff — glance if cross-bundle comparisons arise. Evidence queued for user review batch). Remaining Wave 3: IG-T010/T011, IB-T010 (G5), IL-T011 (user posts the #1625 comment — KI-3).
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
| RQ-11 | OSS target re-point | — | **approved 2026-07-11: llm-d-router primary, GAIE secondary, semconv-genai for the OTel track** |
| RQ-12 | Semconv pin staleness (observation): gen_ai.* deprecated out of core semconv at v1.42.0; gen_ai.system renamed gen_ai.provider.name at v1.37.0; our v1.34.0 pin is explicit + reverify-flagged, so nothing is broken — decide at a later infergate task whether to bump before v1.0.0 contract freeze (SC-T010). | nothing now; SC-T010 checklist item | queued 2026-07-11 |
| RQ-6 | inferops ADR-0001 | — | **accepted 2026-07-10** (inferops@7ca8870) |
| RQ-7 | fleetlab ADR-0001 | — | **accepted 2026-07-10** (fleetlab@da01bb4) |
| RQ-8 | SC compatibility policy + ADRs | — | **accepted 2026-07-10** (part of release review) |

### Wave 4 (CPU path; GPU items deferred per G6 decision)

| Task | Status | Evidence | Commit |
|---|---|---|---|
| IG-T012 routing (health+pressure+P2C) | done (orchestrator re-ran route tests race-green; shift measured 23-29ms vs bounds) | /home/user/infergate/internal/route | infergate@a99ba71 |
| IG-T013 reliability (retry budget/breaker/timeouts) | done (zero-post-first-token-retry invariant proven structurally + live 20x; breaker mid-stream-blind verified) | /home/user/infergate/internal/reliability | infergate@5aa528e |
| IG-T016 release v0.1.0 | done (digest-pinned images smoke-tested from release; Contract-5 descriptors kit-valid; consumption-without-checkout documented; tag local + release/v0.1.0 branch pushed per KI-1; also fixed missing mock capability descriptor gap) | /home/user/infergate RELEASES.md + deploy/ | infergate@49236a3 |
| IG-T014 vLLM adapter | deferred (G6: no GPU) | — | — |
| IB-T007 calibration vs reference | todo (CPU variant vs llama.cpp reference) | — | — |
| IO-T002+ ops track | **blocked-on-user (RQ-14)**: container lacks CAP_SYS_RESOURCE — NO k8s pod can run (proven at runc level, kind/k3s/minikube alike; k3s API server itself fine; Docker Hub/quay pulls DO work — earlier curl-probe belief corrected). Options: (a) compose-based ops + k3s API-validation pivot (recommended), (b) user-provided k8s machine, (c) defer ops wave. Probe report: /home/user/tools/k8s-env-probe-report.md | — | — |
| FL-T002 ingestion + validation | done (orchestrator re-ran 103 pytest green; real corpus ingests: 8 workloads, 48 manifests, ~13.4k events, 10 results; 2 refusals = the documented truncated aborted-session files, correctly refused; provenance refusals typed) | /home/user/fleetlab/fleetlab/ingest | fleetlab@2f01c10 |
| FL-T003 core models | done (Little's law exact on real traces; token-rate rel=1e-6 vs real result; KV formula vs fixture exact; KV-vs-measured-memory honestly PENDING — no isolated KV measurement exists in evidence) | /home/user/fleetlab/fleetlab/models + docs/notes/model-validation.md | fleetlab@9f02bf4 |
| FL-T004 goodput profiles + G8 holdout | done (re-fit on corrected corpus incl. ib-t008 sweep: **capacity holdout WITHIN STATED ERROR** — interior +0.7%/-0.4%, hard points ±7% at ≈1.05σ, both directions; latency fitted for sweep config with characterized extrapolation miss + functional-form analysis; agent also caught a 7.46% scheduled-rate bias and fitted empirical rates; ib-t010 2-point results stand alongside as the thin-corpus limitation; orchestrator verified commit scope + 168 tests green; G8 evidence queued for user review) | /home/user/fleetlab/reports/holdout-validation.md §2b | fleetlab@b02d6e3 |
| FL-T006+T008 autoscaling signals + cost model | in-progress (subagent) | — | — |
| FL-T005 dynamics | done (G/G/c core validated vs 5 analytic limits; cold-start MEASURED from i3 logs: warm 1.94s / cold 91.34s; scale-lag honestly assumed-flagged; headroom hypothesis supported 8.5x) | /home/user/fleetlab/fleetlab/dynamics + reports | fleetlab@dd57e88 |

## 5. Budget ledger

GPU spend: $0. **G6 DECISION (user, 2026-07-11): no GPU rental for now** — Wave 4+ GPU-dependent portions run the documented CPU fallbacks (05 §5): llama.cpp + Qwen2.5-1.5B is the measured engine baseline; I4 runs as the llama.cpp-backed variant with the charter §7 repositioning note; IG-T014/IB-T011/IB-T012 defer until GPU access exists (envelope $150–250 remains approved if that changes). Never-cut list unaffected — cancellation correctness, fault-injection, valid benchmarking, contract validation, and the I6 loop all close on CPU.

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
- (2026-07-11) Orchestrator lesson: a corpus/fact error in MY dispatch brief (wrong evidence path for the sweep) propagated into an agent's "missing data" finding — agents correctly refuse to invent, but the orchestrator must cite evidence paths from verified tool results, not memory. Cross-check dispatch briefs against ls/grep before sending.
- (2026-07-11) KI-2: besides timed session-limit windows, a Fable-5 usage-credit cap can terminate subagents ("run /usage-credits or switch models") — finishing-type work relaunches fine on Sonnet with a self-contained from-disk prompt; heavy design/verification work should wait for credits or explicit user say-so.
- (2026-07-11) KI-3: this session's GitHub access is scoped to the user's seven repos — writes to third-party repos (llm-d) are denied at the access layer, so ALL upstream OSS posting must be done by the user manually from the prepared drafts. User approved the #1625 comment; posting handed to user (draft: inference-lab/oss/drafts/2026-07-11-llm-d-router-1625-comment.md; pre-post live check done 2026-07-11: #1625 open+unassigned, #1909 still defers fairness_id).
- (2026-07-11) KI-4: very long tool inputs are being truncated mid-text this session (two Agent prompts + one heredoc cut off) — keep Agent prompts moderate, split big file edits into multiple Edit calls, and always re-check what was actually sent/landed.

## 8. Deviations index

- None yet. Each repo keeps `docs/implementation-notes.md` § Deviations; links accumulate here.
