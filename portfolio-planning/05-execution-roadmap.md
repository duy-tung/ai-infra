# 05 — Execution Roadmap

Dependency-ordered roadmap. **No calendar durations.** Ordering is by prerequisites, verification gates, and integration risk. Waves may overlap wherever contracts are stable and no hidden coupling is created.

Task fields (schema from the program brief): **Repo · Complexity (S/M/L) · Critical path (CP) · Parallel-safe (Par) · Required/Stretch**, then Requirement/Hypothesis, Dependencies, Expected files, Review focus, Verification, Evidence, Integration impact, Stop condition.

---

## 1. Waves

**Wave 0 — Inspect & lock boundaries.** Completed by this planning run: source inspection, evidence inventory, blind-spot pass (`13-evidence-assumptions-and-deviations.md`), boundaries locked (`02`, `03`).

**Wave 1 — Contracts core + gateway spine.** Start: user approves plan. Tasks: SC-T001–T005, SC-T008–T009; IL-T001; IG-T001–T002, IG-T004. Exit gate: contracts `v0.1.0` released; gateway serves non-streaming completions from mock; consumer fixture validation green (I1 partial).
**Wave 2 — Streaming, cancellation, first engine, bench core.** Tasks: IG-T003, IG-T005–T006; IB-T001–T004; SC-T006–T007; IL-T002 (→ **I2**), IL-T003 (→ **I3**). Exit gate: I2 and I3 accepted.
**Wave 3 — Multi-tenancy, admission, bench validity, OSS start.** Tasks: IG-T007–T011; IB-T005–T006, IB-T009–T010; IL-T010. Exit gate: overload evidence produced (admission on/off, goodput protected); analysis pipeline emits schema-valid results; OSS primary target built locally.
**Wave 4 — GPU path + ops baseline.** Tasks: IG-T012–T014, IG-T016; IB-T007, IB-T011; IO-T001–T004; IL-T004 (→ **I4**). GPU gate opens here (budget rules below). Exit gate: I4 accepted; kind cluster runs gateway+mock with observability.
**Wave 5 — Kubernetes operations, failure campaigns begin, fleetlab core, study artifacts, OSS reproduction.** Tasks: IO-T005–T006, IO-T008; FL-T001–T005; IG-T015, IG-T017–T018; IL-T005 (→ **I5**); IL-T011; SC-T010. Exit gate: I5 accepted; fleetlab ingests real benchmark results; OSS reproducer communicated upstream.
**Wave 6 — Capacity feedback + autoscaling comparison + campaign completion.** Tasks: FL-T006–T009; IO-T007, IO-T009; IB-T012 (stretch); IL-T006 (→ **I6**), IL-T007 (→ **I7**). Exit gate: I6 and I7 accepted with published evidence.
**Wave 7 — Freeze, reproducibility audit, release, OSS follow-through.** Tasks: IL-T008–T009, IL-T012. Feature freeze at wave entry; only reliability fixes, evidence, and docs after. Exit gate: **I8** accepted.

Start/pause/skip conditions per wave: a wave starts when its listed prerequisites (prior gates) pass; pauses when its gate fails twice for the same cause (triggers a review); GPU-dependent portions are skipped (not the wave) when the GPU budget rule blocks, using the CPU fallbacks in §5.

## 2. Critical path

```text
SC-T001 → SC-T002/T003 → SC-T009 (v0.1.0)
  → IG-T002 → IG-T003 → IB-T002 → IB-T004 → IL-T002 (I2)
  → IG-T005 → IL-T003 (I3) → IB-T005 → IB-T006
  → IG-T010 → IG-T012 → IG-T013 → IG-T014 (GPU) → IL-T004 (I4)
  → IO-T002 → IO-T003 → IO-T004 → IO-T005 → IL-T005 (I5)
  → FL-T002 → FL-T003 → FL-T004 → FL-T006 → FL-T009 → IL-T006 (I6)
  → IO-T006/T007 → IL-T007 (I7) → IL-T009 (I8)
```

Everything else runs off-path in parallel. The longest risk concentrations: IG-T003 (streaming/cancellation correctness), IG-T014 + IL-T004 (first GPU work), FL-T004→I6 (models must fit real data), and OSS latency (external).

## 3. Parallel workstreams

| Stream | Contents | May run alongside |
|---|---|---|
| Contracts | SC-T004–T008, SC-T010 | everything after SC-T009 |
| Gateway tenancy/fairness | IG-T006–T011 | bench core, contracts |
| Bench analysis (Python) | IB-T005–T006, T009 | gateway GPU work |
| Ops baseline (CPU) | IO-T001–T004 | gateway/bench work |
| Fleetlab (file-driven) | FL-T001–T005 | all runtime work |
| Study artifacts | IG-T015, T017, T018 + `08-study-track.md` outputs | any wave ≥3 |
| OSS track | IL-T010–T012 | any wave ≥3 (externally paced) |

Safe because: contracts are pinned per wave; all cross-repo interaction is via released artifacts/files; no shared code.

## 4. Verification gates

| Gate | After | Check |
|---|---|---|
| G1 contracts | SC-T009 | fixtures validate; consumer kits green (I1) |
| G2 streaming correctness | IG-T003 | 100 concurrent streams, no frame mixing; 3-point cancellation tests; race detector clean |
| G3 local loop | IL-T002/T003 | I2, I3 acceptance (see `07-integration-milestones.md`) |
| G4 methodology | IB-T006 + IB-T009 | pooled percentiles, CO-safe, warm-up excluded, validity block present; review sign-off |
| G5 overload | IG-T010/T011 + IB-T010 | at ~5× capacity: accepted-request TTFT p95 degrades ≤20%; sheds typed; no starvation |
| G6 GPU entry | before IG-T014 | written hypothesis + manifest + auto-stop script + budget alert |
| G7 ops | IO-T002–T005 | I5 acceptance |
| G8 capacity | FL-T004/T009 | prediction vs holdout benchmark within stated error; limitations report |
| G9 campaign | IO-T006/T007 | 12 scenarios executed; expected semantics observed or deviation documented |
| G10 release | IL-T009 | fresh-clone quickstart reproduced; reproducibility audit passes (I8) |

## 5. GPU-dependent gates and CPU fallbacks

- GPU-dependent: IG-T014, IB-T007 (calibration vs `vllm bench serve`), IB-T011, IB-T012, IO-T005, IL-T004, parts of IL-T006/T007, FL profiles from GPU runs.
- Budget: ~$150–250 total (user-review item); scripted sessions with auto-stop + budget alerts; every session has a written hypothesis + manifest; batch GPU tasks into few sessions (target ≤6).
- Fallbacks: llama.cpp (CPU) substitutes as measured engine for I3-level evidence and fleetlab profile shape; mock backend provides deterministic load for all gateway/ops correctness work; I4/I5-GPU/I6-GPU portions degrade to "llama.cpp-backed" variants with the repositioning note from `00-program-charter.md` §7; SGLang comparison drops first (kill order in `10-risk-register.md`).

## 6. External dependencies

- Upstream maintainer responsiveness (OSS track): externally paced; mitigations in `09-open-source-track.md` (fallback target, contingency path). Never on the critical path.
- Engine releases/drift: vLLM v0.24.x pin; metric-name drift re-verified at IG-T014 (`curl /metrics`).
- GPU spot market: prices volatile; re-check at G6.

## 7. Human-review bottlenecks

Single reviewer (the user). Mandatory review points: contract releases (SC-T009, SC-T010); G2, G4, G5 evidence; every ADR; GPU session plans (G6); consolidation triggers; OSS submissions before posting. Batch reviews per wave exit to reduce interrupts; everything else proceeds under the deviation policy.

---

## 8. Task register

### serving-contracts

**SC-T001 — Bootstrap repo docs + versioning/compatibility policy.** SC · S · CP · Par:no · Required.
Requirement: contract inventory, SemVer rules, breaking-change definition, release process. Deps: approved plan. Files: `docs/*` (per prompt), `compatibility/compatibility-policy.md`. Review: policy soundness. Verify: docs complete per prompt checklist. Evidence: committed policy. Integration: unblocks all consumers. Stop: policy reviewed.

**SC-T002 — Inference API contract.** SC · M · CP · Par:no · Required.
Requirement: OpenAPI subset, SSE semantics, error envelope+taxonomy, request-ID, cancellation contract, examples. Deps: SC-T001. Files: `openapi/inference-api.yaml`, `examples/api/*`. Review: subset completeness vs OpenAI shapes; rejection-not-ignore rule. Verify: spec lints; fixtures validate. Evidence: spec + fixtures. Integration: gates IG-T002/IB-T002. Stop: fixtures cover stream, non-stream, all error classes.

**SC-T003 — Benchmark data schemas.** SC · M · CP · Par:yes · Required.
Requirement: workload/run/raw-event/result schemas + 8 named workload examples. Deps: SC-T001. Files: `schemas/{workload,benchmark-run,raw-event,benchmark-result}.schema.json`, `examples/workloads/*`. Review: manifest completeness (pins, flags, hardware); pooled-percentile + shed-adjacent-goodput rules encoded. Verify: JSON Schema validation of examples. Evidence: schemas + examples. Integration: gates IB-T002, FL-T002. Stop: all 8 workloads expressible.

**SC-T004 — Backend-capability schema.** SC · S · CP:no · Par:yes · Required.
Requirement: capability fields incl. metric-name mapping, cancellation observability. Deps: SC-T001. Files: `schemas/backend-capability.schema.json`, `examples/capabilities/{mock,llamacpp,vllm}.json`. Review: no engine internals leak into gateway responsibilities. Verify: examples validate. Evidence: schema+examples. Integration: IG adapters, IB feature-gating. Stop: three example descriptors validate.

**SC-T005 — Metrics vocabulary + cardinality policy.** SC · S · CP · Par:yes · Required.
Requirement: canonical metric set, units, buckets, labels, forbidden labels, trace attributes (OTel GenAI pin), measurement-point definitions. Deps: SC-T001. Files: `metrics/metrics.md`, `metrics/cardinality-policy.md`. Review: TTFT/ITL/queue-wait definitions unambiguous. Verify: doc review + fixture dashboard names match. Evidence: committed vocabulary. Integration: IG-T006, IO-T003, IB-T005, FL-T003. Stop: every roadmap metric named here.

**SC-T006 — Deployment + fault-scenario contracts.** SC · M · CP:no · Par:yes · Required.
Requirement: deployment descriptor schema; 12 fault scenarios with expected semantics. Deps: SC-T001. Files: `schemas/{deployment-contract,fault-scenario}.schema.json`, `examples/faults/*`. Review: termination-grace > max-stream rule; scenario semantics match `04` §Contract 6. Verify: examples validate. Evidence: schemas. Integration: IO-T002/T006, IG-T016. Stop: 12 scenarios encoded.

**SC-T007 — Fleet schemas.** SC · M · CP:no · Par:yes · Required.
Requirement: hardware/model/SLO/cost/capacity-recommendation schemas with provenance fields. Deps: SC-T001. Files: `schemas/{hardware-profile,model-profile,slo,cost-profile,capacity-recommendation}.schema.json`, examples. Review: provenance mandatory; no fabricated defaults. Verify: examples validate. Evidence: schemas. Integration: FL-T002, IL-T006. Stop: Scenario E expressible end-to-end.

**SC-T008 — Consumer compatibility test kit.** SC · M · CP · Par:no · Required.
Requirement: golden fixtures + validation tooling consumable in each repo's CI. Deps: SC-T002/T003. Files: `examples/**`, minimal validator CLI/config. Review: kit stays validation-only (no framework). Verify: kit runs green locally. Evidence: kit output. Integration: I1 mechanism. Stop: four consumer repos can wire it (documented usage).

**SC-T009 — Release v0.1.0.** SC · S · CP · Par:no · Required.
Requirement: tagged bundle + release notes + migration policy stated. Deps: SC-T002–T005, T008. Verify: tag exists; consumers pin it. Evidence: release. Integration: opens Waves 2+. Stop: I1 green on v0.1.0. Review: release notes.

**SC-T010 — v1.0.0 freeze.** SC · S · CP:no · Par:yes · Required.
Requirement: freeze Contracts 1–3 before I6; migration notes for accumulated changes. Deps: I5 experience. Review: breaking-change audit. Verify: consumer kits green on v1.0.0. Evidence: release. Integration: prerequisite for I6. Stop: I1 re-run green.

### infergate

**IG-T001 — Planning docs bootstrap.** IG · M · CP · Par:no · Required.
Requirement: create `docs/` set per prompt (charter…adr/). Deps: prompt + contracts v0.1 draft. Files: `docs/*`. Review: gateway-vs-engine boundary section. Verify: prompt checklist. Evidence: docs. Integration: none. Stop: all 15 docs exist with content.

**IG-T002 — Gateway skeleton + mock backend + non-streaming path.** IG · M · CP · Par:no · Required.
Requirement: HTTP server, `/v1/chat/completions` (non-stream), `/v1/models`, `/healthz|readyz|metrics` stubs, request IDs, deterministic mock backend (configurable TTFT/ITL/error rate) as separate binary. Deps: SC-T002. Files: `cmd/gateway`, `cmd/mock-backend`, `internal/...`. Review: mock determinism; contract conformance. Verify: contract fixtures pass against running pair; `go test -race`. Evidence: CI run. Integration: I2 prerequisite. Stop: fixtures green.

**IG-T003 — SSE relay + cancellation.** IG · L · CP · Par:no · Required.
Requirement: per-event flush, `[DONE]`, usage-in-stream; 3-point cancellation (queued / pre-first-token / mid-stream) with bounded release time; 100 concurrent streams without frame mixing. Deps: IG-T002. Files: `internal/stream`, tests. Review: cancellation chain design; buffer bounds. Verify: automated concurrency + cancellation tests (race clean); mock-side abort observed ≤100ms. Evidence: test output. Integration: correctness spine for everything. Stop: acceptance tests green 10 consecutive runs.

**IG-T004 — Config snapshots + graceful drain.** IG · M · CP:no · Par:yes · Required.
Requirement: immutable versioned snapshot, atomic swap, publish ≤5s, drain completes accepted streams, readiness flips. Deps: IG-T002. Review: snapshot/transaction boundary (maps to CMU-track ADR). Verify: reload-under-traffic test, zero dropped streams. Evidence: test output. Integration: fault scenarios 5/8. Stop: tests green.

**IG-T005 — llama.cpp adapter.** IG · M · CP · Par:no · Required.
Requirement: adapter behind unified interface; capability descriptor; mock↔llama.cpp failover; CPU-only (1–3B GGUF). Deps: IG-T003, SC-T004. Review: slot-model differences noted (study artifact). Verify: streaming+cancellation tests vs local `llama-server`. Evidence: test output + descriptor. Integration: I3 prerequisite. Stop: 3-point cancellation verified on llama.cpp.

**IG-T006 — Observability per contract.** IG · M · CP:no · Par:yes · Required.
Requirement: OTel spans (`recv→queue.wait→upstream.connect→ttft→stream.relay→settle`), Prometheus metrics exactly per vocabulary, cardinality guard test. Deps: IG-T003, SC-T005. Review: no forbidden labels. Verify: metric-name conformance test; trace inspect. Evidence: scrape + trace screenshots/exports. Integration: IO dashboards depend on names. Stop: conformance test green.

**IG-T007 — Tenancy + auth + model registry.** IG · M · CP:no · Par:yes · Required.
Requirement: PostgreSQL schema (tenants, keys hashed, models, quota policies, config versions); key auth (constant-time, revocation ≤5s via snapshot); tenant resolution. Deps: IG-T004. Review: key lifecycle + revocation consistency (study ADR). Verify: revocation timing test; no hot-path DB reads (assert via instrumentation). Evidence: tests + migration files. Integration: multi-tenant scenarios. Stop: revoke ≤5s proven.

**IG-T008 — Usage accounting (estimate → settle).** IG · M · CP:no · Par:yes · Required.
Requirement: token estimation, estimate-debit/settle-refund, async idempotent append-only writer (unique request ID), settle variance <1%, DB outage never fails requests; usage-settlement invariants doc. Deps: IG-T007. Review: invariants + ledger design (CMU-track artifact). Verify: variance test; DB-down test; duplicate-delivery test. Evidence: test output. Integration: fault scenario 9. Stop: invariants tested.

**IG-T009 — RPM/TPM quotas.** IG · S · CP:no · Par:yes · Required.
Requirement: two-sided token buckets per tenant; typed 429 + `Retry-After`. Deps: IG-T008. Review: estimate-vs-settle interaction. Verify: quota tests. Evidence: tests. Integration: fairness experiments. Stop: tests green.

**IG-T010 — Admission control.** IG · L · CP · Par:no · Required.
Requirement: bounded per-tenant queues, queue deadlines, global in-flight budget, load shedding with typed errors. Deps: IG-T003; parallel-safe with T007–T009. Review: bound choices; shed reason taxonomy. Verify: saturation test (queue full → shed; accepted work protected). Evidence: tests + metrics. Integration: G5, fault scenario 6. Stop: overload behavior matches spec.

**IG-T011 — Fairness + starvation prevention.** IG · M · CP:no · Par:yes · Required.
Requirement: priority tiers, WRR, aging; noisy-neighbor protection (tenant A 10× load → tenant B p95 shift bounded). Deps: IG-T010. Review: fairness policy. Verify: noisy-neighbor test. Evidence: test + graphs. Integration: overload evidence. Stop: bounded-shift criterion met.

**IG-T012 — Routing (health + pressure).** IG · M · CP · Par:no · Required.
Requirement: health poller, engine pressure normalization from capability-mapped metrics, least-inflight P2C, per-backend in-flight limits. Deps: IG-T005, SC-T004. Review: signals stay engine-external; no fake KV-awareness. Verify: unhealthy-backend routing test (shift within bounded interval). Evidence: tests. Integration: fault scenarios 3/10. Stop: tests green.

**IG-T013 — Reliability: retries, circuit breaker, timeouts.** IG · M · CP · Par:no · Required.
Requirement: retry budget, pre-first-token-only invariant (tested), circuit breaker on pre-stream error rate, timeout hierarchy. Deps: IG-T012. Review: retry-budget ADR (SRE-track artifact). Verify: automated proof of zero post-first-token retries; breaker open/half-open tests. Evidence: tests. Integration: fault scenarios 1/7. Stop: invariant test green.

**IG-T014 — vLLM adapter (GPU gate G6).** IG · M · CP · Par:no · Required.
Requirement: adapter + metric-name mapping (verify via `/metrics` at session start), priority mapping, cancellation verified via engine metrics (KV usage / running count drop ≤ bounded interval). Deps: IG-T013 + G6. Review: session plan + hypothesis (pre-GPU). Verify: streaming/cancellation tests on rented GPU; recorded metrics. Evidence: session log + metrics exports. Integration: I4 prerequisite. Stop: cancellation release proven; session auto-stopped.

**IG-T015 — Consistency ADRs + multi-gateway design.** IG · M · CP:no · Par:yes · Required.
Requirement: API-key revocation consistency ADR; tenant-config consistency ADR; multi-gateway (N-replica) scaling design note. Deps: IG-T007; study inputs (6.5840 topics). Review: consistency reasoning. Verify: ADR review. Evidence: ADRs. Integration: interview/portfolio + inferops multi-replica experiments. Stop: ADRs approved.

**IG-T016 — Release: image + deployment descriptor + conformance fixtures.** IG · S · CP · Par:no · Required.
Requirement: versioned image (digest), deployment-contract descriptor, capability descriptors, released mock-backend image. Deps: IG-T006 + current milestone scope. Review: descriptor completeness. Verify: fixture validation; container starts healthy. Evidence: release artifacts. Integration: unblocks IO-T002. Stop: inferops consumes without source checkout.

**IG-T017 — Stale-health-snapshot experiment + fault-state machine.** IG · M · CP:no · Par:yes · Required.
Requirement: experiment quantifying impact of stale health/pressure snapshots on routing decisions; explicit request fault-state machine doc. Deps: IG-T012. Review: experiment design. Verify: controlled experiment w/ mock-backend fault injection. Evidence: experiment report. Integration: study track (6.5840); routing tuning. Stop: report published.

**IG-T018 — Crash-recovery integration test + transaction-boundary ADR.** IG · M · CP:no · Par:yes · Required.
Requirement: kill gateway mid-traffic; verify idempotent usage recovery, snapshot reload, no double-count; ADR on transaction boundaries. Deps: IG-T008, IG-T004. Review: recovery invariants. Verify: scripted crash test. Evidence: test output + ADR. Integration: study track (15-445); fault scenario 5/9 depth. Stop: recovery test green.

### inferbench

**IB-T001 — Planning docs bootstrap.** IB · M · CP:no · Par:yes · Required. (Same pattern as IG-T001; includes methodology doc skeleton.) Stop: 15 docs exist.

**IB-T002 — Open-loop generator core + raw events.** IB · L · CP · Par:no · Required.
Requirement: open-loop + Poisson arrivals, fixed seeds, concurrent SSE streams, JSONL raw events per schema. Deps: SC-T002/T003. Review: coordinated-omission safety (send-schedule independence). Verify: schema validation of emitted events; deterministic replay with same seed vs mock. Evidence: sample runs vs mock image. Integration: I2. Stop: CO-safety reviewed; events validate.

**IB-T003 — Workload suite v1.** IB · M · CP:no · Par:yes · Required.
Requirement: 8 named workloads as versioned seeded files per schema (incl. controlled prefix-sharing ratio, cancellation, slow-client profiles). Deps: SC-T003. Review: length distributions controlled (output length capped/directed). Verify: workloads validate; dry-run vs mock. Evidence: files + dry-run. Integration: shared with fleetlab arrival models. Stop: 8 workloads run.

**IB-T004 — Streaming client correctness.** IB · M · CP · Par:no · Required.
Requirement: client-side TTFT/ITL capture with monotonic clocks, cancellation issuance, slow-client emulation (bounded read rate). Deps: IB-T002. Review: measurement-point alignment with metrics contract. Verify: vs mock with known configured latencies (measured ≈ configured within tolerance). Evidence: calibration report vs mock. Integration: I2/I3 measurements. Stop: mock calibration within tolerance.

**IB-T005 — Analysis core (Python).** IB · L · CP · Par:no · Required.
Requirement: pooled-percentile computation (never average percentiles across runs), bootstrap CIs, warm-up exclusion, knee detection, goodput@SLO with shed rate adjacent, stall-rate; cost per successful request / per 1M tokens using cost profiles. Deps: IB-T002 outputs. Review: statistics choices. Verify: unit tests on synthetic distributions with known answers. Evidence: test suite. Integration: results feed fleetlab. Stop: synthetic-data tests green.

**IB-T006 — Report generator + validity block.** IB · M · CP · Par:no · Required.
Requirement: report template embedding manifest, interpretation rules, "threats to validity" + "unexplained anomalies" sections; results emitted per benchmark-result schema. Deps: IB-T005. Review: honesty rules encoded. Verify: end-to-end report from a mock run; schema-valid result file. Evidence: sample report. Integration: I3+ evidence format. Stop: sample report approved (G4).

**IB-T007 — Calibration vs reference tooling.** IB · M · CP:no · Par:yes · Required.
Requirement: cross-check generator against `vllm bench serve` (GPU session) or llama.cpp-based reference (CPU fallback); document deltas. Deps: IB-T004; G6 for GPU variant. Review: calibration protocol. Verify: comparison table within stated tolerance or explained. Evidence: calibration report. Integration: credibility of all numbers. Stop: deltas explained.

**IB-T008 — Sweeps, replay, comparison mode.** IB · M · CP:no · Par:yes · Required.
Requirement: rate sweeps (≥6 points, 10%→120% of estimated capacity), replay of recorded workloads, A/B comparison runner. Deps: IB-T004. Verify: sweep vs mock; replay determinism. Evidence: sweep artifacts. Integration: saturation/knee inputs. Review: sweep design. Stop: sweep produces knee on mock.

**IB-T009 — Controlled-experiment framework.** IB · M · CP:no · Par:yes · Required.
Requirement: hypothesis file required per experiment; single-variable rule; repeat policy; stop conditions; guard against combinatorial sweeps. Deps: IB-T006. Review: experiment governance. Verify: framework rejects hypothesis-less runs. Evidence: framework docs + dry run. Integration: G6 enforcement. Stop: governance demo.

**IB-T010 — Experiment set 1 (CPU): gateway overhead + admission value.** IB · M · CP · Par:no · Required.
Requirement: direct-vs-gateway overhead (mock + llama.cpp); admission on/off at ~5× capacity → goodput protection evidence. Deps: IB-T006, IG-T010. Review: hypothesis + design. Verify: ≥3 runs/point; pooled stats; validity block. Evidence: benchmark report #1. Integration: G5; portfolio claim #1. Stop: report published.

**IB-T011 — Experiment set 2 (GPU): vLLM behavior.** IB · L · CP:no · Par:no · Required (GPU).
Requirement: selected controlled experiments: `max_num_batched_tokens` TTFT/ITL trade-off; `max_num_seqs`; `gpu_memory_utilization` (incl. preemption onset); prefix caching on/off with controlled prefix-sharing ratio; chunked prefill; quantization (AWQ/GPTQ vs FP16 where budget allows); KV dtype if feasible. No full-matrix sweeps; hypothesis per experiment. Deps: IB-T009, IG-T014, G6. Review: session plans. Verify: manifests + repeats; engine metrics collected. Evidence: benchmark report #2. Integration: fleetlab profiles; I6 inputs. Stop: budget cap or hypotheses answered.

**IB-T012 — Experiment set 3 (stretch): speculative decoding/MTP, KV offloading, SGLang comparison.** IB · L · CP:no · Par:no · Stretch.
Deps: IB-T011 complete + budget remaining + baseline stable. Kill rules from `10-risk-register.md` apply (SGLang first to drop). Stop: any kill trigger.

### fleetlab

**FL-T001 — Planning docs bootstrap.** FL · M · CP:no · Par:yes · Required. Stop: 15 docs exist.

**FL-T002 — Ingestion + validation.** FL · M · CP · Par:no · Required.
Requirement: load and validate benchmark results, raw events, hardware/model/SLO/cost profiles (schema-conformant; provenance required). Deps: SC-T007; sample data from IB. Review: refuse unproven data (no fabricated defaults). Verify: golden-file tests. Evidence: tests. Integration: I6 entry. Stop: real IB files ingest cleanly.

**FL-T003 — Core models.** FL · M · CP · Par:no · Required.
Requirement: arrival/length models from workload schema; token-rate model; Little's-law relationships; KV-memory-per-token model (`2 × layers × kv_heads × head_dim × dtype_bytes × tokens`) validated against measured engine memory metrics. Deps: FL-T002. Review: model assumptions documented. Verify: unit tests + cross-check vs measured llama.cpp/vLLM data where available. Evidence: model validation note. Integration: everything downstream. Stop: cross-checks within stated error.

**FL-T004 — Goodput/memory profiles from measurements.** FL · M · CP · Par:no · Required.
Requirement: fit per-(hardware, model, engine-config) goodput and memory profiles from benchmark results; holdout validation (predict a run not used for fitting). Deps: FL-T003, IB-T010/T011 outputs. Review: overfitting guard; error bars. Verify: holdout prediction within stated error. Evidence: validation report. Integration: G8. Stop: stated error achieved or documented as limitation.

**FL-T005 — Dynamics: queue growth, cold start, scaling delays, headroom.** FL · M · CP:no · Par:yes · Required.
Requirement: simulate queue growth under bursts; cold-start/warm-up delays; scale-up/down lag; failover headroom; failure-capacity analysis. Deps: FL-T003. Review: delay parameters sourced (measured warm-up from IO/IB, not invented). Verify: scenario tests with known-answer limits. Evidence: scenario outputs. Integration: autoscaling comparison. Stop: scenarios reviewed.

**FL-T006 — Autoscaling signal comparison.** FL · M · CP · Par:no · Required.
Requirement: compare CPU util, GPU util, queue depth, in-flight, token-arrival rate, predicted-goodput deficit as scaling signals across workloads; report with recommendation + when-each-fails analysis. Deps: FL-T004/T005. Review: fairness of comparison. Verify: reproducible simulation runs (seeded). Evidence: autoscaling policy report. Integration: informs IO-T009; I6. Stop: report published.

**FL-T007 — Heterogeneous placement.** FL · L · CP:no · Par:yes · Required (depth reducible).
Requirement: model fit vs VRAM, throughput/cost differences, cold-start, failover headroom, fragmentation, workload affinity; placement recommendations. Deps: FL-T004. Review: honesty about profile coverage (only measured hardware). Verify: seeded runs; sanity invariants. Evidence: placement report. Integration: portfolio depth. Stop: report published or reduced-scope note.

**FL-T008 — Cost model + sensitivity.** FL · M · CP:no · Par:yes · Required.
Requirement: cost/capacity model (cost per 1M tokens at SLO per config); sensitivity analysis over price/load/SLO. Deps: FL-T004. Review: provenance of prices (volatile — dated). Verify: recompute vs benchmark-report cost figures. Evidence: cost report. Integration: I6 recommendation quality. Stop: report published.

**FL-T009 — Recommendation emitter + limitations report.** FL · M · CP · Par:no · Required.
Requirement: emit capacity-recommendation files (Contract 7); "simulation limitations" report (explicitly: simulation ≠ production). Deps: FL-T006/T008. Review: uncertainty statements. Verify: schema-valid output; recommendation consumed by inferops in a dry run. Evidence: recommendation file + report. Integration: I6 loop. Stop: inferops dry-run consumes it.

### inferops

**IO-T001 — Planning docs bootstrap.** IO · M · CP:no · Par:yes · Required. Includes the tooling decision (smallest justified set; default Kustomize + raw manifests). Stop: 15 docs + ADR on tooling.

**IO-T002 — Local cluster baseline.** IO · M · CP · Par:no · Required.
Requirement: kind/k3s cluster; deploy released infergate + mock + dev PostgreSQL by digest per deployment contract; no source checkouts. Deps: IG-T016, SC-T006. Review: contract-only consumption. Verify: smoke test via contract fixtures against in-cluster gateway. Evidence: manifests + smoke output. Integration: I5 path start. Stop: smoke green.

**IO-T003 — Observability stack.** IO · M · CP · Par:no · Required.
Requirement: OTel Collector, Prometheus, Grafana, Tempo; dashboards-as-code keyed to the metrics contract; exemplars wired. Deps: IO-T002, SC-T005. Review: dashboard names match vocabulary. Verify: metrics visible end-to-end from a test stream. Evidence: dashboard exports/screenshots. Integration: I5. Stop: golden dashboard renders.

**IO-T004 — Lifecycle semantics.** IO · M · CP · Par:no · Required.
Requirement: startup/readiness/liveness incl. warm-up-aware readiness; `preStop` drain; rolling update under load with zero client errors; disruption budget. Deps: IO-T002. Review: probe semantics vs deployment contract. Verify: scripted rolling-update-under-load test. Evidence: test output. Integration: fault scenarios 11/12. Stop: zero-error update demonstrated.

**IO-T005 — GPU node profile + vLLM deployment.** IO · M · CP · Par:no · Required (GPU).
Requirement: GPU node profile (device plugin, resources, labels, driver/CUDA recording), vLLM deployment per contract, model mount, secret strategy. Deps: IO-T004, IG-T014 evidence, G6. Review: session plan; teardown script. Verify: in-cluster vLLM serves via gateway; readiness honest during warm-up. Evidence: session log + manifests. Integration: I5. Stop: scenario D smoke green; instance stopped.

**IO-T006 — Fault injection: scenarios 1–6.** IO · L · CP · Par:no · Required.
Requirement: repeatable injection scripts + observation checklists for scenarios 1–6 (Contract 6), run against mock/llama.cpp paths first. Deps: IO-T003/T004. Review: expected-semantics table. Verify: each scenario: injected, observed, gateway semantics match or deviation recorded. Evidence: campaign logs. Integration: I7. Stop: 6/6 executed.

**IO-T007 — Fault injection: scenarios 7–12 + noisy neighbor.** IO · M · CP · Par:no · Required.
Deps: IO-T006, IO-T005 for GPU-relevant scenarios (CPU fallback allowed). Same pattern. Evidence: campaign logs + client-impact measurements (via inferbench). Stop: 12/12 executed or documented CPU-fallback subset.

**IO-T008 — Runbooks.** IO · M · CP:no · Par:yes · Required.
Requirement: 10 runbooks (deploy, upgrade, rollback, drain, backend failure, performance regression, config rollback, capacity shortfall, observability outage, database outage), each tested by walkthrough. Deps: IO-T004+. Review: runbook accuracy. Verify: tabletop or live walkthrough each. Evidence: runbooks + walkthrough notes. Integration: I7/I8. Stop: 10 walkthroughs done.

**IO-T009 — Autoscaling experiments.** IO · M · CP:no · Par:yes · Required (depth reducible).
Requirement: HPA baseline; KEDA only if a signal needs it (justify); signals: queue depth, in-flight, token-arrival rate; compare against fleetlab predictions (mock/llama.cpp backends; GPU variant only if budget). Deps: IO-T003, FL-T006. Review: experiment design. Verify: scaling events observed + recorded. Evidence: experiment report. Integration: I6 verification arm. Stop: comparison report done.

**IO-T010 — Config rollout + secrets + upgrade procedure.** IO · S · CP:no · Par:yes · Required.
Requirement: config rollout (scenario 8 in-cluster), secret strategy documented, upgrade/rollback procedure verified. Deps: IO-T004. Verify: scripted checks. Evidence: procedure docs + outputs. Review: secret handling. Stop: procedures verified.

### inference-lab

**IL-T001 — Skeleton: pins, quickstart, scenarios, logs.** IL · M · CP · Par:no · Required.
Requirement: machine-readable version-pin matrix; quickstart doc structure; scenario A–E definitions; OSS log; study-progress tracker. Deps: plan approval. Review: pins format. Verify: structure complete. Evidence: repo skeleton. Integration: everything reports here. Stop: structure reviewed.

**IL-T002 — Scenario A + milestone I2.** IL · M · CP · Par:no · Required.
Requirement: orchestrate `inferbench → infergate → mock → PostgreSQL → OTel` locally (compose); record evidence per I2 acceptance. Deps: IG-T003, IB-T004, SC-T009. Verify: I2 acceptance checklist. Evidence: run logs + traces. Review: evidence completeness. Integration: I2. Stop: I2 accepted.

**IL-T003 — Scenario B + milestone I3.** IL · M · CP · Par:no · Required. Deps: IG-T005, IB-T006. As above for llama.cpp. Stop: I3 accepted.

**IL-T004 — Scenario C + milestone I4 (GPU).** IL · M · CP · Par:no · Required. Deps: IG-T014, IB-T011 (first GPU experiments), G6. Evidence incl. GPU session manifest. Stop: I4 accepted (or CPU-fallback deviation recorded).

**IL-T005 — Scenario D + milestone I5.** IL · M · CP · Par:no · Required. Deps: IO-T005. Stop: I5 accepted.

**IL-T006 — Scenario E + milestone I6.** IL · L · CP · Par:no · Required.
Requirement: benchmark results → fleetlab recommendation → inferops deployment change → repeated benchmark; compare predicted vs measured; publish loop evidence. Deps: FL-T009, IO-T009, SC-T010. Review: loop honesty (prediction vs outcome). Verify: I6 acceptance. Evidence: loop report. Integration: the central story. Stop: I6 accepted.

**IL-T007 — Failure campaign evidence + milestone I7.** IL · M · CP · Par:no · Required.
Requirement: for selected scenarios: inject (inferops), observe gateway semantics, measure client impact (inferbench), publish ≥2 postmortems (standard format). Deps: IO-T006/T007. Verify: I7 acceptance. Evidence: postmortems. Stop: I7 accepted.

**IL-T008 — Compatibility matrix upkeep.** IL · S · CP:no · Par:yes · Required. Ongoing per release; verified at each integration milestone. Stop: matrix current at I8.

**IL-T009 — Portfolio release + milestone I8.** IL · L · CP · Par:no · Required.
Requirement: quickstart ≤15 min from fresh clone; demo script; benchmark + capacity reports linked; failure evidence; OSS evidence; landing page + articles (2: double-queuing/gateway-boundary; cancellation-and-accounting; optional benchmarking-honesty); reproducibility audit. Deps: I2–I7 evidence. Verify: I8 acceptance incl. stranger-test dry run. Evidence: release. Stop: I8 accepted.

**IL-T010 — OSS: score, build, first reproduction.** IL · M · CP:no · Par:yes · Required.
Requirement: refresh candidate scoring with live checks (per `09-open-source-track.md`), build primary target locally, reproduce one existing issue. Deps: Wave ≥3. Review: target choice sign-off. Verify: build + reproduction logs. Evidence: OSS log entries. Integration: I8 OSS evidence. Stop: reproduction acknowledged or fallback triggered.

**IL-T011 — OSS: minimal reproducer + upstream communication.** IL · M · CP:no · Par:yes · Required.
Deps: IL-T010. Evidence: public issue/comment links (created at execution time, not in this planning run). Stop: maintainer response or 2-week silence → contingency path.

**IL-T012 — OSS: contribution + review follow-through.** IL · M · CP:no · Par:yes · Required.
Requirement: small test/fix/benchmark/validation/docs PR; address review; record lessons. Deps: IL-T011. Evidence: PR links + review threads + lessons note. Stop: merged, or under substantive review at I8 with contingency documented.

---

## 9. Roadmap audit (self-check)

- **Overlap/duplication:** one loadgen (IB), one gateway (IG), one deploy stack (IO); mock backend owned once (IG) and consumed as image. No task creates a second copy of any capability.
- **Dependency order:** every task's deps appear earlier in wave order; the register contains no cycle (spot-check: FL consumes IB files only; IO consumes IG releases only; IL is a sink).
- **GPU cost:** GPU appears only in IG-T014, IB-T007 (variant), IB-T011/T012, IO-T005, IL-T004/T006/T007 (partial) — all behind G6 with fallbacks; target ≤6 scripted sessions within budget.
- **OSS latency:** externally paced, off critical path, with fallback + contingency.
- **Integration risk:** every cross-repo hop has a milestone (I1–I8) with acceptance criteria before dependent work claims it.
- **Review burden:** concentrated at wave exits; ~10 mandatory review points before I8.
- **Fastest safe route:** critical path touches only mandatory evidence; reducible/stretch items are all off-path.
