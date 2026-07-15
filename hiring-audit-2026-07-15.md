# Evidence-Backed Hiring Audit — Backend Engineer → AI Infrastructure / Platform Engineer

**Audit date:** 2026-07-15
**Scope:** the six-repository `inference-systems` portfolio under `github.com/duy-tung`
**Method:** two independent reviewer passes (hiring manager; skeptical staff engineer), reconciled only at the end. Full clones with complete history; code-path tracing from `main()` down; all test suites re-run in this environment; headline numbers recomputed from raw archived events wherever raw data is published; GitHub Actions state checked via API; live job-description sample for market calibration.

Labels: **[VERIFIED]** = checked directly against code, raw evidence, recomputation, or live GitHub state. **[INFERENCE]** = judgment from verified facts. **[UNVERIFIED]** = claim exists in documents but cannot be independently checked from published artifacts.

---

## 0. Executive verdict

- **Best-fit role family today: B — Inference Reliability / Release / Developer-Productivity Engineering** (mid-level shortlist-credible), with **A — AI Platform / Model-Serving Platform** close behind if framed as "serving-platform mechanics on CPU, single host."
- The portfolio is **methodologically excellent and substrate-poor**. The benchmark methodology, negative-result discipline, and contract-first architecture are genuinely rare and survive adversarial recomputation. But **no GPU, no vLLM, no scheduled Kubernetes pod, no running autoscaling controller, no multi-node system, and no production traffic exist anywhere in the evidence.** Role families C and D score accordingly low; no amount of methodology compensates for the missing substrate.
- **Most damaging gap:** everything runs one level below what every sampled job description asks for — CPU llama.cpp instead of GPU vLLM; Docker Compose plus API-server-validated manifests instead of a real Kubernetes scheduler.
- **Ownership risk:** 105 of 106 commits across the six repos are *authored by* `Claude <noreply@anthropic.com>`, all within a 72-hour window, ~43k LOC. The work is defensible in interviews only with deliberate preparation (§6) and honest disclosure.
- **Blunt bottom line (§9.6):** the portfolio makes the *platform/reliability* half of the transition credible at mid-level. It does not yet make "AI Infrastructure Engineer" defensible in the GPU/runtime sense. Two vertical slices — one scripted GPU+vLLM session and one real cluster that actually schedules the existing manifests — would change the picture more than everything else combined (§8).

---

## 1. Snapshot and claim-integrity audit

### 1.1 Snapshot manifest [VERIFIED 2026-07-15]

| Repo | main HEAD (current-head scope) | Release refs on GitHub | Commits | Last commit (UTC) |
|---|---|---|---|---|
| serving-contracts | `507208b` | `release/v0.1.0`=`2df9f81`, `release/v0.2.0`=`484b449`, `release/v1.0.0`=`507208b` (= main) | 16 | 2026-07-12 00:12 |
| infergate | `f362ceb` | `release/v0.1.0`=`49236a3` | 33 | 2026-07-11 23:06 |
| inferbench | `62c2704` | none | 13 | 2026-07-11 23:08 |
| fleetlab | `dd05e7d` | none | 18 | 2026-07-11 22:21 |
| inferops | `c695425` | none | 13 | 2026-07-12 02:56 |
| inference-lab | `bb0c253` | `release/v1.0.0`=`bb0c253` (= main) | 26 | 2026-07-12 05:23 |

**Published-release scope.** `inference-lab@v1.0.0` is claimed as an annotated tag on `b940f5c` (`FINAL-REPORT.md:3`). **No tag of any kind exists on any of the six GitHub remotes** [VERIFIED via full tag fetch]. The program's own log (ai-infra `program-state.md`, KI-1) records the session git proxy silently dropping tag pushes; `release/<version>` branches were pushed as substitutes. Consequences:

1. "v1.0.0" is **not publicly verifiable as a tag**. The only public pinnable ref, `release/v1.0.0`, points at `bb0c253` — **two commits past** the claimed tag commit `b940f5c` (it includes `FINAL-REPORT.md` itself plus the acceptance-note commit). The release scope is recoverable but fuzzy at the edge.
2. serving-contracts' claimed tag commits are recoverable (`release/v1.0.0` = `507208b` matches), but the annotated tag objects cited in `pins/pins.yaml` (e.g. `64c3205…`) are not public.
3. **All milestone-pinned component commits named in `pins/pins.yaml` exist in public history** (infergate `5d69aeb`/`74f2372`/`49236a3`; inferbench `caa5074`/`69a5abc`/`6a3fb53`/`cc404a6`/`62c2704`; fleetlab `dd05e7d`; inferops `135dd34`…`db30279`/`f5fdd86`/`89871a6`/`a07fd2f`) [VERIFIED].
4. serving-contracts' own compatibility policy tells consumers to "pin an annotated tag `vX.Y.Z`" — a policy-vs-reality gap the repo itself flags (`RELEASES.md:14-15`).

**Current-HEAD vs published pins.** infergate main is 3 commits past released v0.1.0 (delta: IG-T017 stale-health experiment, IG-T018 crash-recovery test, ADR finalization) — all evidenced at HEAD, none claimed retroactively for v0.1.0. `inference-lab/compatibility/matrix.md`'s drift table states this accurately [VERIFIED]. No case was found of post-release work being used to validate a v1.0.0-scope claim.

### 1.2 CI claims [VERIFIED]

- **infergate is the only repo with CI**, and it is real: `.github/workflows/ci.yml` runs gofmt, `go vet`, `go test -race ./...` against a **real `postgres:16-alpine` service** (so the DB-gated tenancy/quota/ledger/crash-recovery tests execute there, not skip), a 10×-consecutive streaming-stability gate, and an explicit `TestCrashRecovery` step. GitHub Actions shows **9 runs, all success**, including HEAD `f362ceb` and release commit `49236a3`. This is the portfolio's only execution evidence on infrastructure the author does not control, and it is genuine.
- **The other five repos have zero workflows and zero runs**, while their docs describe CI as though wired: fleetlab `docs/testing.md` ("green in CI", "CI … runs the full suite … on every push"), inferbench `docs/testing.md` ("CI validates both directions"), inferops `docs/testing.md` ("CI must be able to spin the kind cluster" — kind was never installed anywhere), serving-contracts `docs/testing.md` ("CI matrix"). The underlying checks do pass when run locally (§2), but any CV/interview statement about "CI" is true **only for infergate**.

### 1.3 Test suites re-run in this audit [VERIFIED]

| Repo | Command (this audit, 2026-07-15) | Result |
|---|---|---|
| infergate @ `f362ceb` | `go vet ./...`; `go test -race ./...` | 17/17 packages pass, race-clean, ~214 test functions; PostgreSQL- and llama-server-gated tests self-skip locally (they run in GitHub CI, which provides postgres) |
| inferbench @ `62c2704` | `go vet ./...`; `go test ./...`; `PYTHONPATH=src CONTRACTS_BUNDLE=… python3 -m pytest -q` (analysis) | 11/11 Go packages pass; **103/103 Python tests pass** |
| fleetlab @ `dd05e7d` | `python3 -m pytest -q` (after installing declared deps numpy/jsonschema/pytest) | **297 passed, 4 skipped / 301 collected** (matches the claimed 301; the 4 skips are the full-corpus tier that requires sibling-repo checkout paths) |
| serving-contracts @ `507208b` | `python3 kit/contracts-validate.py selftest` | GREEN: 52/52 positives, 29/29 negatives fail-as-required, 12 schemas meta-valid |
| inference-lab @ `bb0c253` | `python3 pins/validate_pins.py` | OK, 28 artifact entries |

### 1.4 Headline-number recomputation from raw artifacts [VERIFIED]

Every number below was independently recomputed in this audit from raw archived events (formula noted), not read from reports:

| # | Claim | Published | Recomputed | Source of raw |
|---|---|---|---|---|
| R1 | Concurrent-stream integrity | 154 in-flight, 0 violations, 2736/2736 ok | max in-flight **154** (sweep-line over start/end ts); **2736 events all ok**; frame rule `output_tokens == len(itl)+1` → **0 violations** over 2736+4830 events | `inference-lab/evidence/i2/raw/runs/concurrency-100/events.jsonl.gz` |
| R2 | 3-point cancel deltas (mock, composed stack) | sub-ms, 0.247–0.724 ms | pre-first-token 0.247/0.398/0.573 ms; mid-stream 0.310/0.413/0.724 ms; near-completion 0.318/0.367/0.638 ms (abort-vs-cancel nearest-neighbor) | `evidence/i2/raw/runs/cancel-*/` + `debug-state.json` |
| R3 | Client-vs-gateway TTFT agreement | +1.9 ms | client mean 0.303917 s − gateway scrape (1459.732−1.026)/(4832−2)=0.302010 s = **+1.907 ms** | i2 raw + `metrics-*.prom` |
| R4 | Gateway overhead, paired, mock | p50 +1.04 / p95 +2.21 / p99 +2.81 ms (n=630) | **+1.039 / +2.208 / +2.813 ms**, n=630 pairs, warm-up 50/rep discarded, HF-7 quantiles | `inferbench/docs/evidence/ib-t010/e1-mock-compare/{direct,gateway}/rep-*/events.jsonl` |
| R5 | Admission E2 at ~5× | +25.16% p95 TTFT | **+25.1648%** (baseline p95 0.161199 s, 5x-sane 0.201764 s); accepted/shed counts match exactly (809/900 @ 0.101; 573/2550 @ 0.775) | `ib-t010/e2-*` raw |
| R6 | Capacity loop | 33.583 rps = +1.3% vs predicted 33.159 | phase-3 window: **2015 ok / 60 s = 33.583 rps**; (33.583−33.159)/33.159 = **+1.279%** | `inferops/experiments/autoscaling/evidence/signal-comparison-*/inferbench-run/events.jsonl` (6736 events) |
| R7 | Autoscaling signal lag | in_flight +6.1 s vs queue_depth +64.4 s | matches `summary.json` detection block (96.1 s vs 154.42 s first-fire) | same evidence dir |
| R8 | fleetlab recommendation | 6 replicas, 33.159±1.105 rps/replica, goodput [165.279, 189.036] | fit **re-derived**: C = achieved rps of the single training point 33.15910…; SE = 33.159/√900 = 1.10530…; `build_recommendation()` regenerated **byte-identical** to the committed JSON | fleetlab fixtures + `fleetlab/fitting/*`, `emit/*` |
| R9 | Failover outage | 142 s outage, zero client failures | downtime = `listening_ts − kill_ts` = **141.682 s**; 27 ok + exactly 1 typed `upstream_error` at the kill moment; 12/12 mock-served during outage, 0 aborts | `evidence/i3/raw` + logs |
| R10 | Fault-campaign roll-up | 12/12 executed, 11/12 matched, scenario 4 real defect | per-scenario verdict census = 6 clean + 5 matched-with-deviation + 1 not-matched (scenario 4); pm-001 timeline matches `part-a-stall.log` line-for-line (8 s stall vs 3 s deadline, stream not closed) | `inferops/faults/scenario-*/evidence/`, `campaign-matrix.md` |

**Not recomputable from published artifacts** [VERIFIED absence]: (a) the quickstart timings 2m08s/35s — a prose table only, no captured transcript exists under `quickstart/`; (b) crash-recovery "10/10 SIGKILL, 36/36 rows" — a pasted transcript in `infergate/docs/evidence/ig-t018/`, not machine-written (though the same test runs green in GitHub CI against real postgres, which independently exercises the mechanism); (c) E2b's +26.08% CI — report-level verification only in this audit; (d) the "8 workloads / ~13.4k events" fleetlab ingestion headline — asserted only by tests that skip without sibling checkouts at the orchestrator's paths.

### 1.5 Claim-consistency ledger (cross-document)

| Claim | Where stated | Cross-check | Verdict |
|---|---|---|---|
| "v1.0.0 tagged at `b940f5c`" | FINAL-REPORT.md:3; pins.yaml | no public tag; public release branch 2 commits ahead | **Unverifiable ref; stale by construction** (KI-1) |
| I4–I8 "ACCEPTED by user 2026-07-12" | FINAL-REPORT §3; `compatibility/matrix.md` rows; pins.yaml | every milestone checklist (`evidence/i5..i8`), `evidence/README.md`, the reproducibility audit, and matrix *prose* still say "acceptance-review-pending"; the acceptance exists only as commit message `bb0c253` | **Self-attested process metadata, internally inconsistent between table and prose.** Not independent validation either way — a hiring reviewer should ignore all "accepted" markers |
| G5 admission gate | FINAL-REPORT #7; limitations.md §4; reports 1/1b | REFUTED twice (+25.16% recomputed; +26.08% report), re-baselined by the program owner to typed-shedding/bounded-wait/no-starvation criterion; history preserved | **Consistent and honest** — the re-baseline is a self-set gate being re-set by the same party, disclosed |
| G8 capacity holdout | limitations: "documented MISS (12.6–20.4%) for the ib-t010 corpus" | `fleetlab/reports/holdout-validation.md` splits per config: ib-t008 6-point sweep WITHIN error (+0.7/−0.4% interior, ±7% hard); ib-t010 2-point configs MISS 12.6–20.4% | **Coherent split.** But ai-infra `program-state.md` §2 headline "G8 = capacity holdout within stated error" omits the MISS — the planning repo is more optimistic than the portfolio |
| Slow-client handling (scenario 4) | infergate `docs/interfaces.md:88` ("stream closed, engine released"), `docs/fault-state-machine.md:102,123` (cites `relay_test.go`+`acceptance_test.go`) | `internal/stream/relay.go:24-26` comment: "Full slow-client fault handling — scenario 4 — is later work"; **neither cited test contains a slow/stalled-client case**; the fault campaign then proved the defect (pm-001); no fix at HEAD | **Stale, contradicted docs at infergate HEAD — a genuine overclaim** inside an otherwise disclosure-heavy portfolio [VERIFIED] |
| Metric HELP strings | `internal/telemetry/vocabulary.go:107,112,115` | describe retry-budget/health-poller as "not yet landed" though IG-T012/T013 shipped and the poller sets the gauge | Minor stale docs-in-code |
| "production-grade" | inference-lab `README.md:5` ("one production-grade LLM inference-serving platform"); `portfolio/README.md` positioning quote | limitations.md itself: no production traffic, users, on-call, or external adoption | **Overclaim wording; must not migrate to a CV** |
| I1 "GREEN across all four consumers" at v1.0.0 | serving-contracts RELEASES.md:220; evidence/i1 | disclosed caveat at RELEASES.md:220-223: consumers' pins still read v0.2.0; the v1.0.0 re-validation was run by the serving-contracts side against consumers' artifacts | Self-attested but disclosed; low risk since v0.2.0→v1.0.0 is byte-identical in schemas/openapi except one description string [VERIFIED by diff] |
| Deploy image digests (ghcr.io paths) | infergate RELEASES.md:59-60, deploy contracts | images never pushed to the named public registry — local `registry:2` only, disclosed | Self-reported digests; not pullable |
| RQ-14 "proven at runc/nsexec level" | inferops compose headers, validate-k3s.sh | cites `/home/user/tools/k8s-env-probe-report.md` — **not committed anywhere**; the consequence (0 nodes, pods Pending) is fully evidenced, the mechanism is not inspectable | Assertion-by-reference to a missing artifact |

### 1.6 Presentation-surface facts a recruiter hits first [VERIFIED]

- **Four of six repos have no top-level README** (infergate, inferbench, fleetlab, inferops). All six have **no GitHub "About" description, 0 stars, 0 forks**, and were created within a 14-second window on 2026-07-10. A 10–15-minute reviewer who clicks any repo except inference-lab or serving-contracts lands on a bare file listing.
- The good landing page exists (`inference-lab/portfolio/README.md`) but nothing on the other repos points to it.

---

## 2. Role-fit and competency map

Scores use the 0–4 capability-state model (Implemented / Exercised / Measured / Representative). Role families: A = platform/serving, B = reliability/release/dev-prod, C = runtime/performance, D = GPU/K8s infra.

### 2.1 Inference serving & runtime boundaries

| Competency | Families | Score | Impl | Exer | Meas | Repr | Primary evidence | Counter-evidence / limit | Hiring interpretation |
|---|---|---|---|---|---|---|---|---|---|
| Streaming/SSE correctness | A,C | **4** | ✓ | ✓ | ✓ | ✓ (protocol-level) | `infergate@f362ceb internal/stream/relay.go`, `gateway.go:658-763`; conformance suite; R1/R2 recomputed; CI 10× stability gate | scale is 154 streams on 4 vCPU; single host | Genuinely demonstrated; safe to claim |
| Cancellation & resource release | A,C | **3** | ✓ | ✓ | ✓ | partial | 3-point mock with asserted 100 ms bounds (`acceptance_test.go:408,474`); real-engine slot release via `/slots` (`llamaserver_test.go:596-609`, 2 s asserted bound); R2 | on the *pinned* real model only 1 composed-stack point; 3-point adapter test used an unpinned random-weight GGUF; real-engine test env-gated, not in CI | Claim only with the scope qualifier the portfolio itself uses |
| Engine abstraction & adapters | A | **3** | ✓ | ✓ | ✓ | CPU only | `backend.ChatBackend` (`backend.go:17-32`); `llamacpp` adapter + probed capability descriptor; `Failover` | **no vLLM adapter code exists** [VERIFIED]; llama.cpp adapter reachable only via `-config` JSON, not default flags | "Engine-pluggable gateway" is fine; "vLLM integration" is false |
| Request-scheduling boundary (no double-queuing) | A,C | **3** | ✓ | ✓ | ✓ | mock-measured | ADR-0005 + boundary behavior in dispatch; measured cost ≈2 ms p95 (R4); article-1 | never observed against a continuous-batching GPU engine | Strong design story; weak empirical base beyond CPU |
| Prefill/decode separation | C | **1** | — | — | — | — | described in docs/articles only | no implementation or measurement | Not demonstrated |
| Continuous batching | C | **1** | — | — | — | — | llama.cpp `-np 2` used as a black box | no batching-interaction study | Not demonstrated |
| KV/prefix-cache behavior | C | **1** | — | — | — | — | shared-prefix workload exists (i3, 25/25 ok) | no KV-pressure or hit-rate measurement | Not demonstrated |
| Quantization / model loading | C | **1** | pin only | — | — | — | one Q4_K_M GGUF pinned by sha256 | no comparison across quantizations/models | Not demonstrated |
| Speculative decoding | C | **0** | — | — | — | — | — | — | Absent |
| Engine metrics & profiling | C | **2** | ✓ | ✓ | partial | CPU | llama.cpp `/metrics`,`/slots` consumed in tests; pressure normalization in `route/` | no profiler artifacts (pprof/flame); no GPU counters | Black-box only |

### 2.2 Model-serving platform

| Competency | Families | Score | Primary evidence | Counter-evidence / limit | Hiring interpretation |
|---|---|---|---|---|---|
| Routing, health, load balancing | A | **3** | P2C least-inflight (`route/route.go:245-281`), health poller, measured staleness→impact curve (`docs/evidence/ig-t017/raw-data.csv` matches report exactly) | default CLI wires N=1 backend; multi-backend via config JSON; no real fleet | Solid single-node mechanics |
| Admission control & backpressure | A,B | **3** | bounded tenant queues, WRR 30:10 + aging (asserted in `fairness_test.go`), typed 503+Retry-After; overload behavior measured at ~5× (R5); 100% typed sheds | ≤20% degradation target REFUTED twice; single host, mock engine | Real, measured, honestly failed its own target |
| Retry budget & circuit breaker | A,B | **3** | `reliability/retry.go`, breaker; zero-retry-after-first-token proven in tests | breaker mid-stream-blind (disclosed) | Good |
| Multi-tenancy, quotas, auth, accounting | A | **3** | PG tenancy + API keys; RPM/TPM quota; estimate→settle ledger idempotent by request_id PK; crash-recovery test in CI vs real postgres; noisy-neighbor p95 shift 0.0–4.6% | accounting not composed into the quickstart stack (D-001, disclosed); "36/36" transcript not machine-written | Strongest platform sub-story |
| Config reload, rollout, drain | A,B | **3** | config snapshots + drain (`config/`); compose rolling update 0/27+0/3; config rollout+rollback 0/24+0/4 (R10-adjacent, verified evidence) | compose substrate, ~30-request samples | Good, small scale |
| Model/version lifecycle | A | **2** | model registry per tenant; model pinned by sha256 | no model rollout/canary/version-routing story | Partial |

### 2.3 GPU & distributed acceleration

| Competency | Families | Score | Evidence | Interpretation |
|---|---|---|---|---|
| CUDA/ROCm/accelerator runtime | C,D | **0** | none; inferops proved via `ldd` its engine image has **no** CUDA backend | Absent — and the portfolio says so |
| GPU memory / OOM behavior | C | **0** | none | Absent |
| Kernels & profiling | C | **0** | none | Absent |
| NCCL / collectives | C,D | **0** | none | Absent |
| Tensor/pipeline/data parallelism | C | **0** | none | Absent |
| MIG/MPS / GPU sharing | D | **0** | none | Absent |
| Heterogeneous accelerator scheduling | D | **0–1** | GPU-node manifest shell authored, pod Pending forever, nodeSelector/toleration never evaluated by a scheduler | Manifest authorship only |

### 2.4 Kubernetes & orchestration

| Competency | Families | Score | Evidence | Interpretation |
|---|---|---|---|---|
| Real pod scheduling | D | **1** | Kustomize base/overlays; k3s **server-only** validation: `pods 0/1 Pending, NODE <none>`, `kubectl get nodes → No resources found` [VERIFIED from committed transcripts] | Zero pods ever ran. API-server validation ≠ operation |
| Readiness & lifecycle | A,D | **2** | k8s probes authored; the *behaviors* (warm-up 503→ready, drain incl. in-flight-at-SIGTERM, SIGTERM grace) exercised for real on Compose | k8s lifecycle machinery itself never exercised |
| Rollout/rollback/PDB | A,D | **2** | RollingUpdate maxUnavailable:0 + PDB manifests; compose rolling update + image rollback executed with two real digests, 22/22 smoke each | PDB/eviction never enforced by any controller |
| HPA/KEDA/autoscaling loops | D | **1** | HPA created in etcd: `TARGETS <unknown>, REPLICAS 0`; KEDA rejected by ADR; no metrics-server, no controller ever evaluated anything | Signal *analysis* is real (§2.8) but no control loop ever ran |
| Operators/controllers | D | **0** | none | Absent |
| Device plugins / GPU Operator | D | **0** | none | Absent |
| Node failure & rescheduling | D | **0** | none (single host) | Absent |
| Multi-node / multi-region | D | **0** | none; multi-gateway is ADR-0007 design-only | Absent |

### 2.5 Observability & SLO engineering

| Competency | Families | Score | Evidence | Interpretation |
|---|---|---|---|---|
| OTel + Prometheus + tracing | A,B | **3** | 11-metric contract implemented + conformance-tested against independently parsed contract (`telemetry/conformance_test.go:68`); OTel spans wired; Compose stack with digest-pinned collector/Prom/Grafana/Tempo | single host; Compose |
| TTFT/ITL/e2e/goodput metrics | A,B,C | **3** | contract-defined histograms; goodput@SLO in analysis; TTFT recomputed within +1.9 ms of gateway self-report (R3) | CPU timing regime |
| Metric cardinality | A,B | **3** | cardinality policy + <10k-series budget; guards in vocabulary; llm-d #1625 `fairness_id` unbounded-cardinality reproduction (5000-series demo) | — |
| Dashboards & alerts | A,B | **2** | golden dashboard (11/11 panels) provisioned as code, verified live via Grafana API | **no alert rules exist**; runbooks are symptom-indexed instead |
| SLO / error-budget reasoning | B | **2** | SLOs used as benchmark gates (p95<10ms/p99<20ms; G5 criteria) | no error-budget policy or burn-rate machinery |
| Cross-layer correlation | A,B | **3** | exemplar→Tempo trace end-to-end with real trace ID and full span sequence [VERIFIED from captured API outputs] | one demo path |

### 2.6 Performance methodology (the portfolio's core strength)

| Competency | Families | Score | Evidence | Interpretation |
|---|---|---|---|---|
| Open- vs closed-loop | B,C | **4** | schedule precomputed from seed before any I/O (`schedule.go:93-169`); scheduler cannot wait on responses; declared closed-loop refused with typed error | textbook-correct and enforced structurally |
| Coordinated omission | B,C | **4** | latency basis = `scheduled_send_ts` (`client.go:451`, `sse.go:115`); wire-stage watchdog; the exact 2 s-hidden-dial attack that broke v1 is now a regression test (`run_test.go:319-403`); ADR-0001 documents the failure | rare; survived an adversarial verifier and kept the scar as a test |
| Percentiles & pooling risks | B,C | **4** | pooled raw-sample quantiles with a construction-token guard making per-run-percentile averaging raise (`percentiles.py:78-89`) | — |
| Warm-up & steady state | B | **3** | discard-first-50/rep declared in manifests and honored (R4 reproduces only with it) | one shed-count label nit (2067 all-in vs 1977 measured-window; all typed either way) |
| Sample size & CIs | B | **3** | seeded bootstrap (B=1000) with genuine statistical coverage tests | modest n (630 pairs; 900-request arms) |
| Paired experiments & noise | B | **3** | paired per-request overhead design; tail anomaly and llama.cpp variance disclosed, E1-llama.cpp honestly INCONCLUSIVE (gateway measured *faster* — flagged as physically impossible as a gateway effect) | single-host co-location confound, disclosed |
| Goodput under SLO | B | **3** | goodput/shed-adjacent reporting; error/shed-gated latency (`WithheldLatency` cannot serialize) | — |
| Profiling & bottleneck attribution | C | **2** | queue-transit root cause of G5 refutation triple-confirmed (measured queue-wait, off-arm control, code) | no profiler-level artifacts |
| Reproducibility & isolation | B | **3** | seeds, replay `reference.json` + refuse-on-drift, pins, comparability rule | no hardware isolation (disclosed); reports not recomputable from inference-lab alone (§1.4) |

### 2.7 Reliability engineering

| Competency | Families | Score | Evidence | Interpretation |
|---|---|---|---|---|
| Fault injection | B | **3** | 12 scenarios, each with hypothesis/inject.sh/verdict/evidence, real timestamped captures; roll-up 11/12 consistent [VERIFIED] | Compose substrate; single-backend topology deviations in 4 scenarios (disclosed) |
| Timeout & retry semantics | A,B | **3** | staged timeout hierarchy; typed error taxonomy (10 classes, machine-readable in the contract) | — |
| Idempotency & accounting correctness | A,B | **3** | request_id PK dedup; settle-exactly-once via `finish` closure; crash test | — |
| Cancellation | A,B,C | **3** | see §2.1 | — |
| Crash recovery | A,B | **3** | 10× SIGKILL transcript (36/36 rows, 0 lost/dup); same test wired into GitHub CI vs real postgres | transcript is pasted, not machine-written; scale is 36 rows |
| Slow-client behavior | A,B | **2** | the write-deadline exists; the fault campaign *disproved* the handling (8 s stall uncaught, 2.6× deadline); root cause understood (per-write deadline bounds one syscall; kernel buffer absorbs small SSE events) | **defect unfixed at HEAD and infergate docs still claim the opposite** — the strongest single interview trap in the portfolio |
| Postmortems | B | **3** | pm-001..003 from real captures, timelines match raw logs line-for-line [VERIFIED] | self-authored; no production incidents |
| Soak/load/chaos coverage | B | **2** | load yes; chaos-on-Compose yes | no soak (longest windows are minutes) |

### 2.8 Capacity & cost

| Competency | Families | Score | Evidence | Interpretation |
|---|---|---|---|---|
| Fitted profiles + holdout | B | **3** | real holdout gate with both outcomes published (ib-t008 within error; ib-t010 MISS 12.6–20.4%) | **the flagship recommendation is built on the MISS-config profile** (disclosed, wired into the uncertainty bound) — and the "fit" behind 33.159±1.105 is a **single training point** with Poisson SE [VERIFIED by re-derivation] |
| Prediction error / loop closure | A,B | **3** | I6 loop: prediction (git-provably created before the change) → applied 1→2 → re-measured +1.279% (R6) | 6-replica recommendation itself never executed; higher rates diverge toward a different internal estimate (published) |
| Extrapolation boundaries | B | **3** | capacity clamp; "no finite latency prediction at/above C"; stated | — |
| Autoscaling-signal selection | B,D | **3** | measured lag comparison: in_flight +6.1 s vs queue_depth +64.4 s (R7); utilization-alone ruled out via 2-slot discretization argument | no controller ever consumed the signal |
| Cost per request/token | B | **2** | closed-form model on measured throughput; headline $0.181/1M on-demand labeled "MODEL DEMONSTRATION" first-line | price card is a GPU (A10G) rate applied to a CPU mock — disclosed mismatch |
| Utilization & saturation | B,C | **2–3** | bracketed knee 21.12 rps found by unmodified detector; honest `bracketed:true, confidence 0.8` | mock substrate |
| Model/hardware sensitivity | B,C | **1** | one model, one host | Not demonstrated |

### 2.9 API, contract & artifact design

| Competency | Families | Score | Evidence | Interpretation |
|---|---|---|---|---|
| OpenAPI/JSON Schema | A | **3** | 869-line OpenAPI 3.1 with normative SSE rules, 10-class machine-readable error taxonomy with retryability semantics, reject-not-ignore validation; kit selftest GREEN | consumers are all self-authored repos — conformance "by real consumers" is intra-portfolio |
| Compatibility & SemVer | A,B | **3** | two-clause breaking definition (artifact-invalidation AND measurement-meaning); v0.2.0→v1.0.0 freeze **byte-verified prose-only** in schemas/openapi [VERIFIED by diff]; a real pre-1.0 breaking change (CO fix) handled with migration note | one wording change in metrics.md §Start-definition would have changed a literal-reading consumer's measurement (disclosed edge) |
| Provenance & reproducibility of artifacts | B | **3** | pins.yaml (28 entries, digests for images/binaries/model), validator green; capacity schema makes provenance structurally mandatory | public tags missing (KI-1); report raws live cross-repo |
| Cross-repo release boundaries | A,B | **3** | inferops consumes only released infergate images by digest, no source checkout — digest byte-identical across compose files, deploy manifests, and evidence [VERIFIED] | registry is local; ghcr paths never went live |
| Model/tokenizer/config versioning | A,C | **2** | single-file GGUF sha256 covers weights+quant+tokenizer; engine flags recorded in the pin | single artifact, no lifecycle |

### 2.10 Delivery, IaC, security, supply chain

| Competency | Families | Score | Evidence | Interpretation |
|---|---|---|---|---|
| CI/CD & release gates | B | **2** | infergate CI real (9 green runs, race + DB + stability + crash gates); release process documented and followed once (v0.1.0) | 5 of 6 repos: no CI at all |
| Regression testing | B | **3** | the CO attack, seed determinism, replay refuse-on-drift, 10× stability gate — regressions are encoded as tests | — |
| Image/version/digest pinning | B,D | **3** | all 11 compose services digest-pinned, zero `:latest` [VERIFIED] | infergate Dockerfile *base* images tag-pinned only; build requires uncommitted `vendor/` |
| Terraform/Helm/Kustomize depth | D | **1** | Kustomize base+overlays, API-validated | no Helm, no Terraform, nothing applied to a real cluster |
| Secrets & tenant isolation | A,B | **2** | secret-rotation walkthrough on Compose; loopback-bound Grafana; honest finding on Grafana first-boot | admin API unauthenticated (disclosed); no secret manager |
| SBOM / vuln scanning | B,D | **0** | none found | Absent |
| Artifact signing/provenance | B,D | **1** | digests + contract provenance fields | no signing, no SLSA |
| Rollback & change safety | B | **3** | upgrade/rollback with two real digests, 22/22 smoke each; config rollback 0 drops | Compose substrate |

---

## 3. Transition-critical gaps (ranked by hiring damage)

| # | Gap | Families hit | What a hiring manager distrusts | What a staff engineer probes | Class | Smallest converting experiment | Acceptance criteria | Effort | Impact |
|---|---|---|---|---|---|---|---|---|---|
| G-1 | **No GPU, no vLLM execution — ever** | C (blocker), A (major), B (moderate) | "AI infra engineer who has never touched a GPU serving stack" | KV-cache pressure, batching interaction, engine metrics — any question here has no measured answer | Hard blocker for C; major for A | One scripted, pinned GPU session (single A10/L4, ~$10–30): run vLLM, build the missing `internal/backend/vllm` adapter against the existing `ChatBackend` seam, re-run the existing cancellation + overhead + admission experiments (IG-T014 + IB-T011 as already specced) | 3-point cancellation vs vLLM engine metrics; paired gateway overhead vs vLLM; one KV-pressure workload; all pinned in pins.yaml with driver/CUDA versions; negative results archived | MEDIUM | **HIGH** |
| G-2 | **No scheduled Kubernetes workload; no controller ever ran** | D (blocker), A (major) | "k8s on the CV, `kubectl get nodes → No resources found` in the evidence" | HPA behavior under load, eviction/PDB semantics, probe interactions — none observed | Hard blocker for D | One real kind/k3d/k3s cluster on any $10–20 VM; `kubectl apply` the **existing** Kustomize; metrics-server + HPA under inferbench load; kill a node/pod; execute the 6-replica recommendation for real | pods Running; HPA scales 2→N under load with captured events; rollout/rollback + PDB-respecting drain observed; 6-replica goodput measured vs the 189 rps prediction | MEDIUM | **HIGH** |
| G-3 | **Recruiter surface: 4 repos README-less, 0 descriptions, no CI badges, no public tags** | all | "Is this even finished?" — most reviewers never reach the good landing page | n/a | Major weakness (cheapest fix) | Write per-repo READMEs linking the portfolio narrative; set About strings; add the (already-passing) checks as Actions to the other 5 repos; push real tags | every repo: README + description + green badge; tags visible | SMALL | **HIGH** (screen-stage) |
| G-4 | **Slow-client defect unfixed; infergate docs still claim it handled** | A,B | honesty story cracks exactly where it's most advertised | "your state-machine doc cites tests that don't exist" | Major weakness | Fix cumulative-stall handling (per-write deadline → stall budget/heartbeat); re-run scenario 4; correct `fault-state-machine.md`/`interfaces.md`; write the fix into pm-001 as the corrective action | scenario 4 re-run shows stream closed ≤ deadline+ε; docs updated; regression test added | SMALL | MEDIUM |
| G-5 | **Capacity modeling is mock-backend; flagship recommendation sits on a single-point fit from a MISS-config profile** | B | "the loop is elegant but the model never saw a real engine" | "why ±1.105? that's Poisson SE on one point" | Major weakness | Fit a llama.cpp profile from the existing i3/IB-T010 real-engine runs + one new multi-rate sweep; re-emit recommendation; holdout it | holdout within stated error on ≥3-point fit for a real engine config | MEDIUM | MEDIUM |
| G-6 | **No external/production validation of any kind** (0 users, 0 OSS interaction posted, all reviews AI-or-self) | all | nothing outside the author's own loop has ever touched this | "who else has run this?" | Major weakness | Post the already-drafted llm-d #1625 comment; follow through to maintainer response; invite 1–2 external code reviews | public link with maintainer engagement | SMALL | MEDIUM |
| G-7 | **No multi-node anything** | D, senior-A | single-box ceiling | consistency/failure questions have design-note answers only | Bonus at mid-level, blocker for senior-D | (covered by G-2's cluster if ≥2 nodes) | — | — | — |

Credibility cost of the specific absences the brief asks about: **no real GPU** and **no vLLM/SGLang execution** together remove family C from consideration and cap family A at "adjacent"; **no real pod scheduling** and **no real autoscaling controller** remove family D; **mock-based capacity modeling** downgrades the loop story from "capacity engineering" to "capacity methodology"; **no production evidence** caps *all* families at portfolio-signal rather than experience-signal.

---

## 4. Interview exposure — the 12 hardest questions

| # | Question | Why asked | Strongest truthful answer (evidence) | Strength | Follow-up trap | Must NOT claim |
|---|---|---|---|---|---|---|
| 1 | "Client disconnects mid-stream. Walk the exact path from the socket error to the engine slot being free." | Tests real ownership of the flagship correctness claim | write fails → `cancelUpstream()` + `relay.Abandon()` (`gateway.go:698-710`) → adapter `Close()`/ctx-cancel tears down upstream conn (`openaihttp.go:186-191`) → llama.cpp slot freed, observed via `/slots` (1.25–5.24 ms adapter-level; 100 ms asserted bound on mock) | STRONG | "How do you *know* the slot freed — what did you poll?" (answer: `/slots` census; and the 21-vs-20 log-census deviation in i3 — knowing that detail proves ownership) | that 3-point cancellation was verified on the pinned model composed-stack (only mid-stream was) |
| 2 | "Your write deadline was 3 s; an 8 s stall sailed through. Why?" | The portfolio's own lead postmortem; also its biggest doc contradiction | `SetWriteDeadline` bounds a single `Write` syscall; small SSE events land in the kernel send buffer and return instantly; deadline resets per event; between events the loop blocks on upstream `Next()`, so a non-reading client is invisible until the buffer fills (`relay.go:73-95`; pm-001) | STRONG (if learned) | "So why do `interfaces.md` and `fault-state-machine.md` still say it's handled and tested?" — there is no good answer; concede the doc bug | that the defect is fixed (it is not, at HEAD) |
| 3 | "What is coordinated omission and where exactly does your generator defeat it?" | Core methodology differentiator | latency clock starts at `scheduled_send_ts` computed pre-I/O from seed; TTFT = first_byte − scheduledAt (`client.go:451`); wire-stage watchdog kills runs whose send slips; the original 2 s-hidden-dial attack is a permanent regression test (`run_test.go:319-403`) | STRONG | "Your first version had this bug — how was it found?" (answer honestly: an adversarial reviewer attack; the fix is commit `2828f12`) | that the generator was validated against a reference load tool |
| 4 | "Your admission gate failed its own ≤20% target twice and then you changed the target. Defend that." | Probes integrity + queueing understanding | mechanism triple-confirmed: admission-by-queueing adds one queue transit uniformly with load, so a *ratio* target is mis-shaped for this architecture; both REFUTED results published with CIs; replacement criterion (100% typed sheds, p95 queue-wait 134 ms, no starvation) is measurable and met | STRONG | "Isn't that moving goalposts?" — own it: self-set gate, re-set by the same party, history preserved; the honest phrasing is 'refuted, then re-scoped' | that "admission control met its overload SLO" unqualified |
| 5 | "33.159±1.105 rps per replica — where does the ±1.105 come from?" | The number looks like a regression fit; it isn't | it is Poisson SE = rate/√900 on a **single training point** (`corpus.py:57-67`, `capacity.py:26-30`); the loop then confirmed +1.28% at that exact rate; higher rates diverged 9–13% from this figure toward an internal 37.925 estimate — published | PARTIAL | "So the model is one number with an error bar. What would a real fit need?" (multi-rate sweep; the ib-t008 config has one and passed holdout) | "holdout-validated capacity model" for *this* config (its config family is the documented MISS) |
| 6 | "Swap llama.cpp for vLLM behind your gateway. What breaks?" | Tests engine literacy without GPU experience | capability descriptor changes (probed vs static), pressure-metric mapping (`route/` normalization), different queue/preemption semantics, streaming chunk shapes; the `ChatBackend` seam is where the adapter goes — and honestly: untested, IG-T014 was specced and deferred | PARTIAL | "What vLLM metric would you map to your pressure signal?" (needs prep: e.g. running/waiting reqs, KV-block usage) | any tested vLLM behavior |
| 7 | "Why did in_flight beat queue_depth as a scaling signal here, and would that transfer to vLLM on GPUs?" | Autoscaling reasoning vs memorization | queue cap is 3, so queue_depth saturates only near collapse (+64.4 s lag); in_flight moves with concurrency (+6.1 s); transfer is config-dependent — deep-queue or engine-side batching changes the answer; utilization-alone provably unusable at 2-slot discretization | PARTIAL-STRONG | "What signal would you use for a continuous-batching engine?" | that any controller acted on the signal |
| 8 | "+2.21 ms p95 overhead measured against a mock with 300 ms TTFT. Why is that the right instrument, and what at 10 ms-TTFT engines?" | Measurement-validity reasoning | mock is the resolving instrument: deterministic, so ms-scale deltas are attributable; against llama.cpp the same experiment was INCONCLUSIVE (variance 2–3 orders above the bound) and reported as such; at 10 ms-TTFT engines the relative overhead matters and would need re-measurement | STRONG | "Your gateway measured *faster* than direct in one llama.cpp arm — explain" (sequential warming; physically impossible as gateway effect; disclosed) | "≈2 ms overhead" as an engine-independent constant |
| 9 | "Why does zero-retry-after-first-token matter, and how is it enforced?" | Streaming + billing correctness depth | SSE deltas are not idempotent client-side; a post-first-token retry double-streams and double-bills; enforced structurally (retry only wraps `openStream` before first chunk, `gateway.go:640-656`) + proven in `reliability_test.go` | STRONG | "What about non-streaming?" (budget/attempt caps; typed retryability in the error taxonomy) | — |
| 10 | "Nothing here ever ran as a pod. What did k3s validation actually buy you?" | Honesty + k8s literacy | schema validation, defaulting, controller reconciliation to etcd (ReplicaSets created, pods Pending); it did **not** buy scheduler/kubelet/probe/eviction behavior — which is exactly why the runtime is Compose and the docs say so | PARTIAL | "What would break first on a real cluster?" (needs a prepared answer: probe timing vs warm-up, resource requests, PDB vs drain script) | "deployed on Kubernetes" |
| 11 | "Walk the money: request accepted → tokens streamed → crash — what does the ledger say?" | Accounting/transactions depth | estimate at admission, settle exactly-once via `finish` closure → async idempotent writer (`ON CONFLICT (request_id) DO NOTHING`); SIGKILL test: 36/36 rows, 0 lost/dup, in-flight resolved ≤4.4 ms; ADR-0003 was *corrected* to as-built truth: no request journal — lost-with-bound, never duplicated | STRONG | "So can you lose usage?" — yes, bounded, never duplicated; knowing the ADR correction is the ownership tell | "exactly-once accounting" without the lost-with-bound qualifier |
| 12 | "How much of this did you write yourself?" | The commit log answers it if the candidate doesn't | see §6.6 disclosure script | depends entirely on prep | "Explain this line" pointed at arbitrary code | sole hand-authorship |

---

## 5. Differentiating strengths (verified, with limits)

1. **Coordinated-omission-safe load generation that survived an adversarial attack and kept the scar as a regression test.**
   Evidence: latency basis `scheduled_send_ts` enforced in schema+client+analysis; the 2 s-hidden-dial attack reproduced as `TestSlowDialDelayCountsAgainstLatency`; overhead numbers recompute exactly (R4). Transfers to: B, C-methodology. Why unusual: most portfolios (and many production benchmark harnesses) measure from wire-write and silently hide connect-time queueing. Limit: only ever pointed at mock + CPU llama.cpp. CV-safe wording: *"Built a coordinated-omission-safe open-loop load generator (Go) whose latency clock starts at scheduled send; an adversarial review that found 2s of hidden dial-time queueing is preserved as a regression test."*

2. **Refusal-first analysis: reports are structurally unable to omit validity information.**
   Evidence: `_check_model` gates all rendering; latency above a 5% error+shed threshold becomes `WithheldLatency` that cannot serialize; pooling guard makes percentile-averaging raise. Transfers to: B (eval/release gating). Why unusual: honesty enforced by construction, not by policy. Limit: enforces section presence, not number truth; self-defined thresholds. CV-safe wording: *"Designed a benchmark-reporting pipeline that refuses to render results without validity blocks and structurally withholds latency when error/shed rates exceed a declared gate."*

3. **A closed capacity loop with the divergences published: predict → apply → re-measure.**
   Evidence: recommendation JSON (git-provably created before the change) → 1→2 replica change → re-measured 33.583 rps = +1.28% at the fitted rate (R6); higher-rate divergence toward an internal 37.925 estimate published rather than hidden. Transfers to: A, B. Why unusual: most capacity work never closes the loop at all. Limits: mock backend; 6-replica recommendation itself never executed; the underlying "fit" is single-point. CV-safe wording: *"Closed a capacity-planning loop: a fitted per-replica throughput prediction was applied as a real replica change and re-measured within +1.3% at the fitted rate (mock-engine testbed, single host; the 6-replica extrapolation was not executed)."*

4. **Negative-result discipline as a portfolio-wide invariant.**
   Evidence: G5 REFUTED twice with CIs, published as the finding; G8 holdout MISS published; E1-llama.cpp INCONCLUSIVE; scenario-4 defect surfaced as the lead postmortem; reproducibility audit narrowed 2 claims. Transfers to: every family — this is exactly the behavior release/reliability teams pay for. Why unusual: near-zero survivorship bias; verified at the raw-data level in this audit. Limit: all gates/criteria are self-set; §1.5 shows one place (infergate docs) where the discipline slipped. CV-safe wording: *"Published refuted hypotheses, a missed holdout gate, and an unfixed defect postmortem as first-class results with raw data, rather than reporting only successes."*

5. **Contract-first six-repo integration with digest-pinned, source-checkout-free consumption.**
   Evidence: OpenAPI 3.1 + 12 JSON Schemas with a two-clause breaking-change definition; kit selftest 52/29/12; v0.2.0→v1.0.0 freeze byte-verified prose-only; inferops runs only released infergate images whose digest is byte-identical across compose, deploy contracts, and evidence. Transfers to: A (platform interfaces), B (release boundaries). Limit: all four "consumers" are the same author's repos; no external consumer ever validated the contracts. CV-safe wording: *"Defined versioned serving contracts (OpenAPI + JSON Schema) consumed by four independent components via a validation kit; enforced SemVer with a byte-verified prose-only 1.0 freeze."*

---

## 6. Ownership and interview defensibility

**The facts [VERIFIED]:** 105 of 106 commits across the six repos are authored `Claude <noreply@anthropic.com>` (one by `duy-tung`, one by `inferops`); trailers credit Claude Fable 5 and one Opus 4.8. All 119 commits (including planning) span 2026-07-10 → 2026-07-12 — ~43k LOC of Go/Python plus evidence in 72 hours. The planning repo shows an orchestrator/verifier agent workflow with the human acting as reviewer and gate-approver ("user accepted", RQ decisions, G5/G6/RQ-14 rulings). Internal "fresh-context verifier" acceptances are AI-run; they are process metadata, **not** independent validation.

**Is it disqualifying?** No — but it converts every interview into a *comprehension* exam. The commit metadata is public and any reviewer who opens `git log` sees it immediately. The candidate's defensible position is "I directed, reviewed, and gated this system, and I can re-derive any result in it" — which must actually be true before interviewing.

### 6.1 Eight decisions to explain cold (no docs open)
1. Why the gateway must never batch/pace/model KV (ADR-0005) — and what the measured cost of that discipline was.
2. Estimate→settle usage accounting with request_id-PK idempotency; why "lost-with-bound, never duplicated" is the honest invariant (ADR-0003's correction).
3. Zero-retry-after-first-token: why streaming retries are unsafe post-first-chunk.
4. Latency basis = scheduled send, not wire write — and the attack that forced it.
5. Admission-by-queueing → why a TTFT-ratio overload target is architecturally mis-shaped (the G5 story).
6. Queue-depth vs in-flight vs utilization as scaling signals under 2-slot discretization.
7. Compose-pivot (RQ-14): why API-server validation was chosen over faking pod scheduling, and what it does/doesn't prove.
8. Bounded-staleness health snapshots: the measured staleness→misroute curve and why 200 ms was shipped.

### 6.2 Five quantitative results to re-derive on demand
1. +2.21 ms p95 paired overhead (pairing rule, warm-up discard, HF-7 quantile — from `e1-mock-compare` raws).
2. +25.16% G5 refutation (p95 ratio between arms; why the CI excludes 20%).
3. 33.583 rps / +1.28% loop closure (2015 ok events / 60 s window; vs 33.159 fit).
4. ±1.105 = 33.159/√900 (and why that's a thin uncertainty model).
5. 154 max concurrent in-flight (sweep-line over event timestamps) and the frame-integrity rule `output_tokens == len(itl)+1`.

### 6.3 Five code paths to trace on a whiteboard
1. `cmd/gateway/main.go` → admission → quota → route (P2C) → `openStream` → SSE relay → settle/ledger.
2. Client disconnect → `cancelUpstream` → adapter close → engine slot release (and how the test observes it).
3. `schedule.Build` (seeded, pre-I/O) → scheduler loop → wire watchdog → events.jsonl.
4. Raw events → analysis gate → pooled percentiles → refusal-first report render.
5. fleetlab ingest → single-point fit → `build_recommendation()` → Contract-7 JSON → inferops apply → re-measure.

### 6.4 Claims that expose shallow ownership if memorized
The ±1.105 provenance (Q5); the 21-vs-20 cancel-log census deviation; why E1-llama.cpp came back *faster* through the gateway; the 2067-vs-1977 shed-count nit; which of the two G8 corpora passed and which missed; why the fault-state-machine doc's scenario-4 row is wrong.

### 6.5 Synthetic-look risk
The 72-hour cadence, identical repo-creation timestamps, six-repo symmetry (fifteen planning docs each), and zero external interaction make the portfolio read as an AI-orchestrated program to any attentive reviewer — because it is one. Do not present it as months of evening work; the git history contradicts that in seconds. The scope is also over-engineered relative to any organic side project (12 fault scenarios, 10 runbooks, 8 milestone gates) — fine if presented as a deliberately structured program, damning if presented as organic.

### 6.6 Honest disclosure script (if asked)
> "I ran this as an AI-orchestrated engineering program: I set the architecture, contracts, gates and budgets; AI agents wrote most of the code and ran the experiments; separate fresh-context AI verifiers re-derived results before I accepted each milestone, and I personally reviewed and gated every release decision. The commit metadata is transparent about that. What I'll defend is the engineering judgment in it — ask me anything about why it's built the way it is or how any number was measured."
This framing is truthful, matches the visible history, and converts the metadata from a liability into a (2026-relevant) AI-supervision competency claim — *provided* the comprehension is real.

---

## 7. CV framing

**Most accurate project title:** *"inference-systems — a measured, contract-first LLM serving platform (CPU testbed): gateway, benchmark harness, capacity simulator, and operations stack across six repos."*

**Two-sentence description:** *"A six-repository portfolio that builds, measures, and operates a streaming LLM-serving path end-to-end: a Go gateway (SSE relay, cancellation, admission control, multi-tenant accounting) in front of a real CPU inference engine, a coordinated-omission-safe benchmarking system, and a capacity-planning loop whose prediction was applied and re-measured within +1.3%. All results are pinned, reproducible, and published with their failures — on a single-host, CPU/Docker-Compose testbed (no GPU, no scheduled Kubernetes workloads)."*

**Best-fit positioning:** Senior Backend Engineer → **Platform/Reliability Engineer for inference serving**. The phrase **"AI Infrastructure Engineer" is not yet defensible unqualified** — use *"Backend/Platform Engineer specializing in LLM serving infrastructure (benchmark methodology, serving-gateway reliability, capacity planning)"* until G-1/G-2 close.

### Resume bullets (25–35 words, evidence-cited)

| # | Bullet | Evidence IDs | Required qualifier | Overclaim risk |
|---|---|---|---|---|
| B1 | Built a Go inference gateway (SSE streaming, cancellation propagation, admission control, per-tenant quotas and usage settlement); 100+ concurrent streams showed zero frame-integrity violations and sub-millisecond cancellation-release deltas against a 100 ms bound. | R1, R2 | "mock engine, single host" if asked | LOW |
| B2 | Measured gateway overhead with a paired-request methodology: p50 +1.04 ms / p95 +2.21 ms / p99 +2.81 ms over 630 pairs; reported the real-engine arm as inconclusive rather than rounding it to a pass. | R4 | mock-backend arm; CPU testbed | LOW |
| B3 | Built a coordinated-omission-safe open-loop load generator; after review exposed 2 s of hidden connect-time queueing, moved the latency basis to scheduled-send and encoded the attack as a permanent regression test. | §5.1 | — | LOW |
| B4 | Load-tested admission control at 5× capacity; published two refuted latency-degradation results (+25.2%, +26.1%, with CIs) and root-caused the mechanism before re-scoping the gate to typed-shedding and bounded queue-wait criteria. | R5 | self-set gate, mock backend | LOW-MED (say "re-scoped", never "passed") |
| B5 | Closed a capacity-planning loop: a fitted per-replica throughput prediction was applied as a real replica change and re-measured within +1.3% at the fitted rate; divergences at higher rates were published, not hidden. | R6, R8 | mock-engine testbed; 6-replica extrapolation not executed | MED without qualifier |
| B6 | Ran a 12-scenario fault-injection campaign against the composed serving stack; 11/12 matched expected semantics and the exception — a slow-client write-deadline defect — was published as the lead postmortem with raw evidence. | R10 | Docker Compose substrate | LOW |
| B7 | Defined versioned serving contracts (OpenAPI 3.1 + 12 JSON Schemas) consumed by four components through a validation kit; enforced compatibility policy through a byte-verified, prose-only 1.0 freeze. | §5.5 | consumers are in-portfolio | LOW |
| B8 | Implemented crash-safe usage accounting (estimate→settle, idempotent by request ID); a 10× SIGKILL recovery test against real PostgreSQL runs in CI with zero lost or duplicated ledger rows. | §2.2, C14 | 36-row scale | LOW-MED |

### DO NOT USE — attractive but unsupported phrases

- **"production-grade"** — no production traffic, users, on-call, or external adoption exist. (The portfolio's own README uses it; do not copy it.)
- **"deployed on Kubernetes" / "Kubernetes operations"** — zero pods were ever scheduled; manifests were API-server-validated only.
- **"GPU inference"** — no GPU was ever rented or used; the engine image demonstrably lacks a CUDA backend.
- **"vLLM integration"** — no vLLM adapter code exists; vLLM appears only as a target description.
- **"autoscaled to six replicas"** — no autoscaler ever ran; the applied change was 1→2; six is an unexecuted extrapolation.
- **"validated at scale"** — single 4-vCPU host; peak measured concurrency 154 streams; 60-second measurement windows.
- **"production SLO"** — all SLOs are self-declared benchmark gates.
- **"open-source contributor"** — nothing was ever posted upstream; the draft comment exists locally only.
- **"holdout-validated capacity model"** (unqualified) — the flagship recommendation's config family is the documented 12.6–20.4% MISS.
- **"CI across six repositories"** — CI exists in exactly one.

---

## 8. Gap-closing roadmap (minimum set, highest impact-to-effort)

Ordered; each extends the existing system, defines pass/fail before execution, and archives raw evidence including failures.

**S1 — Publish-surface hardening (SMALL; do first, this week).**
Add READMEs to infergate/inferbench/fleetlab/inferops (each: what it is, one headline number with its qualifier, link to the portfolio landing page); set GitHub About strings; port the already-passing local checks into Actions workflows for the five CI-less repos; push the missing tags (or re-cut releases where the proxy dropped them). *Success:* every repo shows README + description + green badge; tags resolvable. *Improves:* every family's screen-stage survival; fixes the §1.2 CI-claim gap. *CV-safe afterward:* "CI-tested across all six repositories."

**S2 — One scripted GPU/vLLM session (MEDIUM; the single biggest credibility purchase).**
Execute the already-specced IG-T014 + IB-T011 on one rented GPU (A10/L4-class, pinned driver/CUDA/vLLM version, budget $30–50): build `internal/backend/vllm` against the existing `ChatBackend` seam; probe a capability descriptor; run 3-point cancellation verified against vLLM's own engine state; paired gateway-overhead experiment; one KV-cache-pressure workload (long-context shared-prefix at rising concurrency); record engine metrics; pin everything in pins.yaml. *Success criteria (pre-declared):* cancellation frees engine resources within a declared bound at all 3 points; overhead result (pass, fail, or inconclusive) published with CIs; KV-pressure onset characterized. *Improves:* C from 0-level to 2 on engine metrics/adapters; A's engine story; kills the "never touched a GPU" objection. *CV-safe afterward:* "built and measured a vLLM adapter on GPU" (single-session scope stated).

**S3 — One real cluster that schedules the existing manifests (MEDIUM).**
kind/k3d on any VM that permits nested containers (or a $15 VPS with k3s): apply the existing Kustomize; metrics-server + the existing HPA; drive load with inferbench; capture scale-up/down events; kill a pod and a node; run the rolling update and PDB-respecting drain for real; **execute the 6-replica recommendation and measure goodput vs the predicted [165.3, 189.0] rps**. *Success:* HPA scales on the chosen signal under load with captured controller events; 6-replica goodput measured (inside or outside the interval — either result is publishable). *Improves:* D from 1 to ~3 on scheduling/rollout/HPA rows; closes the I6 loop's biggest disclosed hole. *CV-safe afterward:* "deployed and autoscaled on Kubernetes" (cluster scope stated).

**S4 — Fix the slow-client defect and close pm-001 (SMALL).**
Implement cumulative-stall handling (stall budget across writes or read-side liveness), re-run fault scenario 4, add a regression test, and correct `fault-state-machine.md` + `interfaces.md`. *Success:* stream closed within deadline+ε under an 8 s stall; docs consistent. *Improves:* §2.7 slow-client to 3; converts the portfolio's worst doc contradiction into its best incident-lifecycle story (found → postmortem → fixed → regression-tested). *CV-safe afterward:* "found, root-caused, and fixed a slow-client deadline defect via fault injection."

**S5 — Post the drafted upstream comment and follow through (SMALL, user-action).**
The llm-d #1625 reproduction and comment draft already exist. Post it; respond to maintainers; if the cardinality gap is confirmed, offer the test as a PR. *Success:* public link + maintainer engagement. *Improves:* the only zero-cost external-validation item; every JD sampled lists OSS contribution as a differentiator. *CV-safe afterward:* "reproduced and reported an unaddressed metrics-cardinality gap in llm-d-router" (with link).

Explicitly *not* prioritized: more documentation, more scenarios on the same substrate, SBOM/signing (real but not screen-moving), SGLang breadth (S2 first; depth beats breadth).

---

## 9. Final verdict

Scores are **portfolio-alone** signals (the six repos as evidence, ignoring unstated prior backend experience), 0–10 per the calibration in the brief.

| Family | Mid-level | Senior | Decision | Strongest evidence | Decisive blocker | Moves ±1 point if… |
|---|---|---|---|---|---|---|
| **A — AI Platform / Model-Serving Platform** | **6** | **4** | MAYBE (mid) / NO (senior) | Working gateway with measured overhead, admission, tenancy/accounting, streaming correctness; 11-metric observability with exemplar→trace; digest-pinned release consumption | never ran against a real GPU serving engine; no k8s operation; single host; no production | +1: S2 (vLLM measured behind the gateway). −1: if interviews reveal the §6.4 items aren't owned |
| **B — Inference Reliability / Release / DevProd** | **7** | **5** | SHORTLIST (mid) / MAYBE (senior) | CO-safe methodology with adversarial regression tests; refusal-first reporting; fault campaign + postmortems traced to raw; loop-closure discipline; real CI with race/DB/crash gates (one repo) | gates and reviews are all self-set/AI-run; CI in only 1 of 6 repos; no production release ever shipped to users | +1: S1+S4 (CI everywhere + the defect fixed and regression-tested). −1: the infergate doc contradiction surfacing unprepared |
| **C — Inference Runtime / Performance** | **3** | **2** | NO | measurement methodology; black-box engine handling (slots/metrics); double-queuing design literacy | zero GPU/CUDA/vLLM/batching/KV work — the substance of the role is absent | +1: S2 executed with KV-pressure and engine-metric results. Nothing else moves this |
| **D — GPU / Kubernetes Infrastructure** | **2** | **1** | NO | honest k3s API-server validation; digest-pinned Compose operations; lifecycle semantics on Compose | no scheduled pod, no controller, no GPU, no multi-node — the role's substrate is entirely absent | +1: S3 (real cluster + HPA + node kill). +2 with S2's GPU node in that cluster |

**9.1 Best-fit role family today:** B — Inference Reliability / Release / Developer-Productivity Engineering (mid-level), pitched as "benchmark methodology + release-gate discipline for LLM serving."

**9.2 Single most damaging gap:** no execution on the real substrate — GPU/vLLM and a scheduling Kubernetes cluster — that every target JD treats as table stakes; every strong result in the portfolio is one substrate level below its claim's natural habitat.

**9.3 Single highest-leverage next change:** S2, the one scripted GPU/vLLM session (with S1 done the same week because it is nearly free and gates whether anyone even reads far enough to care).

**9.4 Most truthful one-sentence CV positioning:** *"Backend engineer specializing in LLM-serving infrastructure: built and operated a measured, contract-first serving gateway, benchmark methodology, and capacity-planning loop on a CPU/single-host testbed, with every result pinned, reproducible, and published including its failures."*

**9.5 Reviewer trust summary:** a knowledgeable interviewer will trust the raw evidence (it recomputes), the honesty architecture (it is real, with one located crack — infergate's scenario-4 docs), and the design reasoning (ADRs are substantive); they will *not* trust the substrate (CPU/Compose posing near GPU/k8s vocabulary), the acceptance/verification trail (self- and AI-attested), or unqualified use of "production-grade," and they will immediately see the AI authorship in the commit log.

**9.6 "Does this portfolio currently make the Backend → AI Infrastructure / Platform transition credible?"** — **Partially, and only with honest framing.** It is a genuinely strong reliability/measurement portfolio that earns mid-level platform/reliability interviews *today* if the candidate can personally defend it (§6). It is **not yet** credible evidence for GPU-runtime or Kubernetes-infrastructure roles, and presenting it as such would collapse in the first substrate-specific question. The gap is closable: S1–S4 represent roughly two focused weeks and ~$50 of infrastructure, and they convert the portfolio's two fatal absences into measured results wired into an already-excellent evidence system.

---

## Appendix A — Market calibration sample (accessed 2026-07-15)

Primary career pages were fetched where bot-accessible; two postings were readable only via job-board mirrors of the official text and one had recently closed — noted per row. Spot sample, not a survey.

| # | Role (family) | Source & access | Key extracted requirements |
|---|---|---|---|
| 1 | GM — Senior ML Infrastructure Engineer, Inference Platform (A) | search-careers.gm.com — primary, fetched | 5+ yrs ML systems/high-perf backend; Triton/RayServe/vLLM; serving strategy, versioning, autoscaling, caching; observability; GPU acceleration preferred |
| 2 | Red Hat — Forward Deployed Engineer, AI Inference (A/D) | Workday posting via BuiltIn mirror; listing removed 2026-06-22 | deploy llm-d + vLLM on k8s; disaggregated serving; KV-cache-aware routing; benchmarks to SLOs (TPOT); operators/CRDs, GPU scheduling; forward-pass/KV/continuous-batching literacy; Helm/Terraform; OSS plus |
| 3 | Anthropic — Staff+ SWE, Inference Runtime (C) | greenhouse.io — primary, fetched | accelerator-agnostic runtime (Rust/Python); profiling/latency at scale; CUDA/TPU/Trainium depth; SLO ownership |
| 4 | Anthropic — Staff/Senior SWE, Inference Deployment (B) | greenhouse text via Accel board mirror | deployment/release infra at scale; k8s; canary/soak/blue-green; automated rollback; capacity-aware scheduling; merge→prod cycle time |
| 5 | NVIDIA — AI Inference Performance Engineer NCG 2026 (C) | jobs.nvidia.com — primary; JD body not bot-extractable | (title-level only) |
| 6 | OpenAI — SWE, Model Inference (A/C) | openai.com/careers — 403 to bot | (title-level only) |
| 7 | CoreWeave — Senior GPU Infrastructure SWE (D) | official posting; mirror snippet only | Go/Python vs k8s; custom controllers/operators; infra test/validation automation |

Recurring across families: deep Kubernetes (operators, GPU scheduling), vLLM or equivalent, GPU familiarity, benchmark-to-SLO, observability, Python+Go, IaC, OSS as differentiator. The portfolio's overlap is strongest with #4/#1 and weakest with #2/#3/#7 — the latter all hard-require the substrates this portfolio never touched.

## Appendix B — What this audit ran (reproducibility of the audit itself)

- Clones: `git clone` + `fetch --unshallow` + full branch/tag fetch of all six repos, 2026-07-15; HEADs as in §1.1.
- Test executions: §1.3 table (environment: Linux 4-core sandbox; Go 1.24.x; Python 3.11; fleetlab deps installed from pyproject as documented).
- Recomputations: §1.4 (python3 over raw `events.jsonl[.gz]`, `debug-state.json`, Prometheus text snapshots; HF-7 quantiles via numpy; sweep-line concurrency; nearest-neighbor abort pairing).
- GitHub state: Actions runs listed via API (infergate: 9 success; others: none); repo metadata (creation timestamps, descriptions, stars) via API.
- Out of scope, untouched: other repos on the same account (e.g. `platform-engineering`, `terraform-modules`) — noted to exist, not audited, not credited.
