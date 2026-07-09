# fleetlab — Standalone Planning & Implementation Prompt

You are working on the repository **fleetlab**, one of six repositories in the **Composable AI Inference Systems Portfolio** (`inference-systems`). This prompt is self-contained: everything you need is embedded here. Do not assume access to the master planning repo.

---

## 1. Mission & context

**Program summary.** The program builds a portfolio of independent, composable repositories that together form one production-grade LLM inference-serving platform and that individually demonstrate senior-level engineering judgment. It converts an experienced backend/platform engineer's strengths (Go, PostgreSQL, distributed systems, streaming correctness, observability, reliability) into verifiable AI-inference-infrastructure evidence. The six repositories: `serving-contracts` (versioned specs and schemas, no runtime logic), `infergate` (thin multi-tenant inference gateway, Go), `inferbench` (the only load-generation + benchmark-analysis system, Go + Python), `fleetlab` (this repo), `inferops` (the only Kubernetes/observability/chaos/runbook repo), `inference-lab` (integration, evidence, demos, portfolio narrative, OSS log).

**Target positioning (verbatim program goal):**

> Senior Backend / Platform Engineer capable of designing, building, benchmarking, operating, and reasoning about production-grade distributed AI inference infrastructure, with particular strength in streaming correctness, backpressure, scheduling boundaries, observability, capacity planning, reliability, and infrastructure orchestration.

**This repo's purpose.** `fleetlab` is an **explainable capacity, autoscaling, cost, configuration, and heterogeneous-placement SIMULATION**, written in **Python**. It is NOT a production scheduler, and it must never claim that simulation equals production. Every model parameter has provenance: either **fitted from measured benchmark data** or **explicitly assumed with a flag**. It runs entirely from files — no GPU, no cluster, no gateway needed.

**Independent value.** Answer capacity questions from data alone: given schema-conformant benchmark results and hardware/model/SLO/cost profiles from anyone, fleetlab produces capacity, autoscaling, cost, and placement analysis. It is useful to any team that has measurement files and a capacity question.

**Integration value.** fleetlab closes the program's central story, milestone **I6 — Capacity feedback**: benchmark results (from inferbench) → fleetlab recommendation → inferops applies the change → repeated benchmark → predicted-vs-measured comparison published, including where the prediction was wrong. The machine-readable capacity-recommendation file (Contract 7) is what makes the loop checkable.

---

## 2. Hard rules (program-wide, non-negotiable)

1. Repositories integrate ONLY via versioned contracts, released artifacts, files, or documented network protocols. The dependency graph is acyclic. No shared application library.
2. One gateway (`infergate`), one load-generation system (`inferbench`), one deployment stack (`inferops`) exist in the whole program — never duplicate any of them. fleetlab never generates load, never deploys, never proxies requests.
3. No Kafka/NATS/Redis or any broker in the synchronous inference request path (fleetlab is not on that path at all; do not put it there).
4. The gateway never owns continuous batching, per-token scheduling, KV-cache internals, prefix-cache internals, or GPU placement — those are engine-owned. fleetlab may *model* these behaviors from measurements, never implement or control them.
5. Basic development and CI must not require a GPU. Any GPU session requires a written hypothesis + full config manifest + auto-stop script + budget alert; program GPU envelope ~$150–250 total (as of 2026-07; user-confirmable). fleetlab itself needs no GPU sessions — it consumes files produced by others.
6. Evidence rules: never claim tests/benchmarks/deployments succeeded without command output or artifacts to point at. Every number carries provenance (measured / source-reported / assumed) and a date. Invalid benchmark runs are invalidated, never published. `go test -race` clean is the floor for all Go concurrency work (fleetlab is Python; the analogous floor here is deterministic seeded simulation runs and a green pytest suite).
7. Volatile ecosystem facts (engine metric names, upstream repo layouts, GPU prices, OTel GenAI semconv status) carry "as of 2026-07 — re-verify at use time" flags. GPU pricing in cost profiles is the most volatile input this repo touches: date every price.
8. fleetlab-specific hard rule: **simulation ≠ production.** Every published fleetlab artifact states its uncertainty and its limitations. Prediction error against holdout measurements is a publishable RESULT, not a failure to hide.

---

## 3. Dependencies & contracts

### 3.1 Position in the dependency graph

Topological order: `serving-contracts → {infergate, inferbench, fleetlab, inferops} → inference-lab`, with intra-tier edges pointing "later or sideways" in the order `infergate → inferbench → fleetlab → inferops`.

| Edge | This repo's side | Mechanism |
|---|---|---|
| fleetlab → serving-contracts | consumes | pinned released spec bundle; validates all input and output files against it |
| inferbench → fleetlab | consumes | benchmark-result + raw-event **files** (JSONL/JSON conforming to schemas) |
| fleetlab → inferops | provides | capacity-recommendation **files** (machine-readable, Contract 7) + human reports, used as experiment input for I6 |

**Forbidden edges (checked at every review gate):**

- `fleetlab` → `inferbench` **code**. Files only. No shared statistics library — the metric definitions both repos rely on live in `serving-contracts` (metric vocabulary). If you feel the urge to import an inferbench module, stop: the fix is a contract clarification, never a code dependency.
- `fleetlab` → `infergate`, `inferops`, or engine source code. fleetlab never checks out, imports, or links any other component's source.
- No repo imports fleetlab as a library; consumers read its emitted files.

**State owned by fleetlab:** hardware/model/cost/SLO profiles as versioned YAML/JSON files **with provenance fields**, conforming to the contract schemas. Consumers: fleetlab, inference-lab.

**Independent mode:** runs entirely from files; no GPU, no cluster, no gateway required.

### 3.2 Contracts this repo touches (summaries; pin a released bundle version)

All contracts are owned by `serving-contracts`, versioned as one SemVer bundle, released as git tags with artifacts. Consumers pin a bundle version. **Contracts v1.0.0 (which freezes Contract 1–3 shapes) is a prerequisite for I6.** During v0.x, MINOR may break with a migration note.

**Contract 3 — Benchmark data (fleetlab consumes; primary input):**
- `workload.schema.json`: name, version, seed; arrival process (`open-loop-poisson` rate | `closed-loop` with mandatory disclosure flag); input/output-length distributions; prefix-sharing ratio; cancellation-rate profile; slow-client profile; duration or request count. Eight named workloads ship as versioned examples: `chat-short`, `rag-long-in`, `gen-long-out`, `shared-prefix`, `mixed`, `bursty`, `cancel-storm`, `slow-client`. fleetlab's arrival and length models are parameterized from these manifests — the same versioned files inferbench generates from, so simulation and measurement describe the same workload by construction.
- `benchmark-run.schema.json` (manifest): run ID; target topology (`engine-direct` | `via-gateway` | `gateway-mock`); engine name/version/commit + all runtime flags (`max_num_seqs`, `max_num_batched_tokens`, `gpu_memory_utilization`, prefix caching, chunked prefill, quantization, KV dtype, speculative decoding config); model checkpoint + revision + tokenizer; hardware (GPU model, VRAM, driver, CUDA version, instance type); gateway version + config version; client location/RTT; warm-up policy; repetition count; hypothesis statement. This is the provenance record for every fitted profile.
- `raw-event.schema.json`: one JSONL record per request: request ID, workload item, send timestamp, TTFT, ITL series or summary + max stall, end timestamp, status, error class, input/output token counts, shed/retry flags, cancellation point. fleetlab fits token-rate and length models from these.
- `benchmark-result.schema.json`: aggregates per run set: pooled-percentile tables (percentiles computed on pooled raw data — never averaged across runs), throughput, goodput with explicit SLO reference, shed rate (always adjacent to goodput), stall rate, saturation-knee estimate, cost per successful request and per 1M tokens (with cost-profile reference), validity block, links to raw events and manifest.

**Contract 2 — Metrics and trace vocabulary (fleetlab consumes as model-input definitions):** canonical Prometheus metric set (`inference_requests_total`, `inference_requests_in_flight`, `inference_queue_depth`, `inference_queue_wait_seconds`, `inference_ttft_seconds`, `inference_itl_seconds`, `inference_e2e_duration_seconds`, `inference_sheds_total`, `inference_usage_tokens_total`, …) with normative measurement-point definitions: TTFT = first upstream body byte at the gateway (client-side TTFT is a separate named series); ITL = inter-chunk gap; queue wait = admission-enqueue to dispatch. fleetlab's simulated quantities MUST use these exact definitions so simulation, gateway, and benchmark numbers are comparable. Autoscaling-signal candidates in FL-T006 map to these metric names.

**Contract 4 — Backend capability (fleetlab consumes as model constraints):** engine name + version/commit; streaming support; cancellation mechanism; metrics endpoint + name mapping (e.g. vLLM waiting/KV-usage gauge names vary by version and must be mapped, not hardcoded — as of 2026-07, re-verify); tokenizer identity; context limit; max concurrency hints; prefix-cache support; quantization; priority support. Use these to bound what a simulated backend can do (context limits, concurrency hints).

**Profile schemas (SC-T007; fleetlab's own input files conform to these):** `hardware-profile.schema.json`, `model-profile.schema.json`, `slo.schema.json`, `cost-profile.schema.json` — all **with mandatory provenance fields**; no fabricated defaults. If a profile lacks provenance, fleetlab refuses to ingest it.

**Contract 7 — Capacity recommendation (fleetlab emits; inferops applies; inference-lab archives as Scenario E evidence):** fields — input references (benchmark-result IDs, workload version, SLO, cost profile, hardware profiles); recommended topology (replica counts per hardware type, engine config); predicted goodput/latency/cost **with stated uncertainty**; autoscaling signal + thresholds recommendation; assumptions and sensitivity notes. This closes the I6 feedback loop in a machine-checkable form. `capacity-recommendation.schema.json` is owned by serving-contracts; fleetlab's emitter must validate its own output against the pinned bundle in CI.

---

## 4. Architecture guidance

**Language & stack:** Python (deliberate Python-deepening goal; standard numeric/statistical stack, e.g. pandas/numpy/scipy — pick minimal, justify in an ADR). No daemon, no server, no database: fleetlab is a CLI + library that reads files and writes files. Indicative future command shape (from the program plan): `fleetlab recommend --results ... --slo ... --cost ...`.

**Components (suggested layout; adjust with an ADR if evidence demands):**

1. **Ingestion & validation** (`fleetlab/ingest/`) — loads workload manifests, benchmark results, raw events, hardware/model/SLO/cost profiles; validates everything against the pinned contract bundle; **rejects any profile without provenance fields and any unproven/fabricated default**. Golden-file tests.
2. **Core analytic models** (`fleetlab/models/`) — arrival and length models parameterized from workload schema; token-rate model; Little's-law relationships (L = λW applied to in-flight requests, queue depth, concurrency); **KV-memory-per-token model: `2 × layers × kv_heads × head_dim × dtype_bytes × tokens`**, cross-checked against measured engine memory metrics. Every closed-form model gets a documented derivation and known-answer tests.
3. **Profile fitting** (`fleetlab/fitting/`) — fits per-(hardware, model, engine-config) goodput and memory profiles from benchmark-result + raw-event files; overfitting guard; error bars on every fitted parameter; **holdout validation is structural** (the fitting API takes an explicit train/holdout split and refuses to report fit quality on training data).
4. **Dynamics simulator** (`fleetlab/dynamics/`) — discrete-event or analytic simulation of queue growth under bursts; cold-start/warm-up delays; scale-up/down lag; failover headroom; failure-capacity analysis ("N−1 replicas at peak: what breaks?"). Delay parameters must be sourced (measured warm-up from inferops/inferbench artifacts), never invented — assumed values carry an explicit `provenance: assumed` flag.
5. **Autoscaling-signal comparison** (`fleetlab/signals/`) — evaluates candidate scaling signals against simulated workloads: CPU utilization, GPU utilization, queue depth, in-flight requests, token-arrival rate, predicted-goodput deficit.
6. **Placement engine** (`fleetlab/placement/`) — heterogeneous placement over measured hardware profiles only: model fit vs VRAM, throughput/cost differences, cold starts, failover headroom, fragmentation, workload affinity.
7. **Cost model** (`fleetlab/cost/`) — cost per 1M tokens at SLO per configuration; sensitivity analysis over price/load/SLO; all prices dated and provenance-flagged (volatile — as of the date recorded in the cost profile, re-verify at use time).
8. **Recommendation emitter + report generator** (`fleetlab/emit/`, `fleetlab/reports/`) — Contract-7 files (schema-validated) + human-readable reports.

**State ownership:** fleetlab owns its profile files (versioned, provenance-carrying) and its emitted recommendations/reports. It never mutates its inputs; ingestion is read-only.

**Concurrency model:** effectively none — single-process, deterministic. **Every simulation run is seeded and reproducible**; the seed, input file digests, and contract bundle version are recorded in every output artifact. Parallelism (if ever needed for parameter sweeps) must not break determinism per seed.

**Failure/cancellation/retry behavior relevant here:** fleetlab is offline, so its failure semantics are input-validation semantics: fail fast and loudly on schema violations, missing provenance, version-pin mismatches, or metric-definition ambiguity; never silently coerce or default. A failed ingest names the file, the field, and the rule violated. Modeling of *platform* failure behavior (retries pre-first-token only, shed-with-429, mid-stream errors never retried) follows Contract 1/2 semantics as measured by inferbench — model what was measured, not what the spec hopes.

---

## 5. Required documentation set (FIRST task — FL-T001)

Create `docs/` with exactly these files:

```text
docs/
├── charter.md               # fleetlab mission, independent value, I6 role, simulation ≠ production pledge
├── architecture.md           # components above, data flow (files in → models → files out), determinism rules
├── scope.md                   # what fleetlab owns (ingestion, models, fitting, dynamics, signals, placement, cost, reports)
├── non-goals.md               # §6 below, verbatim in substance
├── interfaces.md              # consumed schemas (Contract 3, 4, profiles) + emitted Contract 7 + report formats; pinned bundle version
├── milestones.md              # §7 below, dependency-ordered, acceptance criteria
├── tasks.md                   # FL-T001…FL-T009 with full schema fields (§8 below)
├── risks.md                   # R9 and locals; kill/reduction rules (§13)
├── testing.md                 # golden files, known-answer tests, holdout protocol, seeded-run reproducibility
├── observability.md           # what fleetlab logs/records about its own runs (input digests, seeds, versions)
├── security.md                # input-file trust model; no secrets; no network at runtime
├── experiments.md             # simulation experiment log: hypothesis → seeded run → result (incl. holdout predictions)
├── integration.md             # I1 consumer-CI wiring; I6 loop role and acceptance criteria (§10)
├── oss-opportunities.md       # §12 below
├── implementation-notes.md    # running log + Deviations section (deviation policy §14)
└── adr/                       # numbered ADRs: stack choice, fitting method, simulator style (discrete-event vs analytic), signal-comparison design
```

Each file must be concrete for THIS repo — no boilerplate. `non-goals.md` and the limitations discipline are first-class portfolio artifacts, not filler.

---

## 6. Non-goals (embed in `docs/non-goals.md`)

fleetlab does NOT own and must never grow: provisioning; Kubernetes controllers; a global scheduler; multi-region consensus; live migration; universal hardware abstraction; benchmark implementation or importing benchmark code; load generation; deployment; **any claim that simulation equals production**. Placement reasoning is restricted to hardware actually covered by measured profiles — no extrapolation to unmeasured GPUs. Autoscaling **experiments** (HPA, justified KEDA) belong to inferops; capacity **logic** stays here.

---

## 7. Repository milestones (dependency-ordered; no calendar durations)

| # | Milestone | Depends on | Acceptance criteria |
|---|---|---|---|
| M1 | Docs bootstrap | approved plan | all 15 docs/ files + the `adr/` directory exist and are repo-specific; reviewed |
| M2 | Contract-conformant ingestion | M1; contracts bundle pinned; sample data from inferbench | golden-file tests green; real inferbench files ingest cleanly; provenance-less profiles and fabricated defaults rejected with typed errors; consumer fixture validation wired into CI (I1 obligation) |
| M3 | Core models validated | M2 | arrival/length/token-rate/Little's-law/KV-memory models unit-tested with known-answer limits; KV formula cross-checked against measured llama.cpp/vLLM engine memory where available, within stated error; model-validation note published with all assumptions flagged |
| M4 | Fitted profiles + G8 holdout | M3; benchmark corpus (IB-T010 CPU, IB-T011 GPU if available) | per-(hardware, model, engine-config) goodput/memory profiles fitted with error bars; **G8 gate: prediction of a holdout benchmark run (not used for fitting) within stated error bars, or the miss documented as a limitation** — either outcome is publishable; validation report reviewed (mandatory human review point) |
| M5 | Dynamics scenarios | M3 | queue growth, cold start/warm-up, scaling delay, failover headroom, failure-capacity scenarios pass known-answer-limit tests; all delay parameters sourced or flagged assumed; scenario outputs reviewed |
| M6 | Autoscaling-signal report | M4, M5 | six-signal comparison across workloads published with recommendation + when-each-signal-fails analysis; seeded, reproducible runs |
| M7 | Placement + cost reports | M4 | heterogeneous-placement report (measured hardware only) and cost/capacity report with sensitivity analysis published; prices dated |
| M8 | Recommendation emitter + limitations report | M6, M7 | Contract-7 files schema-valid in CI; **inferops consumes a recommendation in a dry run**; simulation-limitations report published; ready for I6 |

---

## 8. Task seeds (stable IDs — use exactly these)

Field key: **Goal/Repo · Requirement/Hypothesis · Deps/Expected files · Complexity · CP (critical path) · Par (parallel-safe) · Review focus · Verification · Evidence · Integration impact · Required/Stretch · Stop condition.**

### FL-T001 — Planning docs bootstrap
- **Goal/Repo:** create the full docs set (§5) in fleetlab.
- **Requirement:** all 15 docs/ files + the `adr/` directory, repo-specific, embedding non-goals, the simulation-≠-production pledge, and the G8 holdout protocol.
- **Deps:** approved plan. **Expected files:** `docs/*`, `docs/adr/0001-stack-and-simulator-style.md`.
- **Complexity:** M. **CP:** no. **Par:** yes. **Required.**
- **Review focus:** scope/non-goals honesty; holdout protocol correctness; no boilerplate.
- **Verification:** checklist against §5; user review of charter/scope/non-goals.
- **Evidence:** committed docs.
- **Integration impact:** unblocks all fleetlab work; states the I6 role.
- **Stop condition:** 15+ docs exist and are reviewed.

### FL-T002 — Ingestion + validation
- **Goal/Repo:** load and validate all input file types in fleetlab.
- **Requirement:** ingest benchmark results, raw events, workload manifests, hardware/model/SLO/cost profiles; schema-conformant against the pinned contract bundle; **provenance required — refuse unproven data, no fabricated defaults**; typed, file-and-field-naming errors.
- **Deps:** SC-T007 (profile schemas released); sample data from inferbench. **Expected files:** `fleetlab/ingest/*`, `tests/golden/*` (valid + invalid fixtures incl. provenance-missing cases), `profiles/examples/*`.
- **Complexity:** M. **CP:** yes. **Par:** no. **Required.**
- **Review focus:** refusal paths (no silent coercion); provenance enforcement; contract-version pinning recorded in outputs.
- **Verification:** golden-file tests (pytest); contract-bundle fixture validation in CI.
- **Evidence:** green test run output; CI log validating against the pinned bundle tag.
- **Integration impact:** I6 entry; satisfies fleetlab's I1 consumer obligation.
- **Stop condition:** real inferbench files ingest cleanly.

### FL-T003 — Core models
- **Goal/Repo:** implement the analytic backbone in fleetlab.
- **Requirement:** arrival/length models parameterized from the workload schema; token-rate model; Little's-law relationships; KV-memory-per-token model (`2 × layers × kv_heads × head_dim × dtype_bytes × tokens`) validated against measured engine memory metrics. All model assumptions documented with provenance flags.
- **Deps:** FL-T002. **Expected files:** `fleetlab/models/*`, `tests/models/*`, `docs/notes/model-validation.md`, KV-memory worksheet + capacity-math worksheet (study track, §11).
- **Complexity:** M. **CP:** yes. **Par:** no. **Required.**
- **Review focus:** model assumptions documented; derivations correct; measurement-point definitions (Contract 2) used exactly.
- **Verification:** unit tests with known-answer limits + cross-check vs measured llama.cpp/vLLM data where available.
- **Evidence:** model-validation note with cross-check numbers and error statements.
- **Integration impact:** everything downstream (fitting, dynamics, signals, placement, cost).
- **Stop condition:** cross-checks within stated error.

### FL-T004 — Goodput/memory profiles from measurements
- **Goal/Repo:** fit empirical profiles in fleetlab.
- **Requirement:** fit per-(hardware, model, engine-config) goodput and memory profiles from benchmark results; **holdout validation — predict a run not used for fitting**; overfitting guard; error bars on all fitted parameters.
- **Deps:** FL-T003; IB-T010 (CPU corpus) / IB-T011 (GPU corpus, if budget allowed) outputs. **Expected files:** `fleetlab/fitting/*`, `profiles/fitted/*` (with provenance = the source run manifests), `reports/holdout-validation.md`.
- **Complexity:** M. **CP:** yes. **Par:** no. **Required.**
- **Review focus:** overfitting guard; error bars honest; train/holdout separation structural, not honor-system. **This is the G8 gate — mandatory human review.**
- **Verification:** holdout prediction within stated error (G8); seeded, reproducible fitting runs.
- **Evidence:** validation report (prediction vs holdout, error analysis).
- **Integration impact:** G8; the credibility basis for everything fleetlab publishes.
- **Stop condition:** stated error achieved **or documented as limitation** (prediction error is a result, not a failure).

### FL-T005 — Dynamics: queue growth, cold start, scaling delays, headroom
- **Goal/Repo:** simulate time-dependent behavior in fleetlab.
- **Requirement:** simulate queue growth under bursts; cold-start/warm-up delays; scale-up/down lag; failover headroom; failure-capacity analysis (capacity with N−1 replicas, degraded hardware).
- **Deps:** FL-T003. **Expected files:** `fleetlab/dynamics/*`, `tests/dynamics/*` (known-answer limits: e.g. λ<μ stable queue, λ>μ linear growth), `reports/scenarios/*`.
- **Complexity:** M. **CP:** no. **Par:** yes. **Required.**
- **Review focus:** delay parameters sourced (measured warm-up from inferops/inferbench artifacts, not invented); assumed parameters explicitly flagged.
- **Verification:** scenario tests with known-answer limits; seeded runs.
- **Evidence:** scenario outputs committed with seeds and input digests.
- **Integration impact:** feeds the autoscaling comparison (FL-T006) and cold-start-headroom report.
- **Stop condition:** scenarios reviewed.

### FL-T006 — Autoscaling signal comparison
- **Goal/Repo:** compare scaling signals in fleetlab simulation.
- **Requirement:** compare **CPU utilization, GPU utilization, queue depth, in-flight requests, token-arrival rate, predicted-goodput deficit** as scaling signals across the named workloads; report with recommendation + **when-each-signal-fails analysis**. Hypothesis to test (source-reported, as of 2026-07 — the source research warns GPU utilization is NOT a reliable overload signal for LLM inference): does GPU utilization mislead the autoscaler in simulation, and under which workloads?
- **Deps:** FL-T004, FL-T005. **Expected files:** `fleetlab/signals/*`, `reports/autoscaling-signal-comparison.md`, seeded run configs.
- **Complexity:** M. **CP:** yes. **Par:** no. **Required.**
- **Review focus:** fairness of comparison (same workloads, same SLOs, same tuning effort per signal).
- **Verification:** reproducible simulation runs (seeded); rerun reproduces the tables.
- **Evidence:** autoscaling policy report (one of the five required reports).
- **Integration impact:** informs inferops IO-T009 (HPA experiment compares cluster behavior against these predictions); I6.
- **Stop condition:** report published.

### FL-T007 — Heterogeneous placement
- **Goal/Repo:** placement recommendations across GPU types in fleetlab.
- **Requirement:** model fit vs VRAM; throughput/cost differences; cold starts; failover headroom; fragmentation; workload affinity; placement recommendations — **restricted to hardware actually covered by measured profiles**.
- **Deps:** FL-T004. **Expected files:** `fleetlab/placement/*`, `tests/placement/*` (sanity invariants: never place a model that doesn't fit VRAM; never recommend unmeasured hardware), `reports/heterogeneous-placement.md`.
- **Complexity:** L. **CP:** no. **Par:** yes. **Required (depth reducible — see §13).**
- **Review focus:** honesty about profile coverage (only measured hardware); invariants enforced in code, not prose.
- **Verification:** seeded runs; sanity-invariant tests.
- **Evidence:** placement report (one of the five required reports).
- **Integration impact:** portfolio depth (capacity reasoning breadth).
- **Stop condition:** report published, or reduced-scope note (two hardware profiles) recorded as a deviation.

### FL-T008 — Cost model + sensitivity
- **Goal/Repo:** cost/capacity economics in fleetlab.
- **Requirement:** cost per 1M tokens at SLO per configuration; sensitivity analysis over price/load/SLO; all prices carry provenance and dates (volatile — re-verify at use time).
- **Deps:** FL-T004. **Expected files:** `fleetlab/cost/*`, `profiles/cost/*` (dated), `reports/cost-capacity-model.md`.
- **Complexity:** M. **CP:** no. **Par:** yes. **Required.**
- **Review focus:** provenance of prices (dated, source-flagged); sensitivity ranges honest.
- **Verification:** recompute vs the cost figures in inferbench benchmark reports (which reference the same cost profiles) — must agree.
- **Evidence:** cost report (one of the five required reports).
- **Integration impact:** I6 recommendation quality (cost is a recommendation field).
- **Stop condition:** report published.

### FL-T009 — Recommendation emitter + limitations report
- **Goal/Repo:** close the loop artifact in fleetlab.
- **Requirement:** emit capacity-recommendation files (Contract 7: input references, recommended topology with replica counts per hardware type + engine config, predicted goodput/latency/cost with stated uncertainty, autoscaling signal + thresholds, assumptions and sensitivity notes); publish the **"simulation limitations" report** stating explicitly that simulation ≠ production, what is modeled, what is not, and known error magnitudes from G8.
- **Deps:** FL-T006, FL-T008. **Expected files:** `fleetlab/emit/*`, `examples/recommendations/*.json`, `reports/simulation-limitations.md`, CLI entry (`fleetlab recommend --results ... --slo ... --cost ...`).
- **Complexity:** M. **CP:** yes. **Par:** no. **Required.**
- **Review focus:** uncertainty statements on every predicted number; limitations report is candid (it is a mandatory honesty artifact, part of G8 review).
- **Verification:** schema-valid output against the pinned bundle in CI; **recommendation consumed by inferops in a dry run**.
- **Evidence:** recommendation file + limitations report + inferops dry-run log.
- **Integration impact:** I6 loop (the central story).
- **Stop condition:** inferops dry-run consumes it.

**Wave context (ordering only, no dates):** FL-T001–T005 run in the program's Wave 5 alongside ops work; FL-T006–T009 in Wave 6 feeding I6. Critical path within the program: `FL-T002 → FL-T003 → FL-T004 → FL-T006 → FL-T009 → I6`. The program's stated risk concentration for this repo: **FL-T004 → I6 — the models must fit real data.**

---

## 9. Testing, observability, security, performance hypotheses

**Testing (`docs/testing.md`):**
- Golden-file tests for ingestion (valid, invalid, provenance-missing, unsupported-field cases).
- Known-answer-limit tests for every analytic model (Little's law identities; KV formula against hand-computed cases; queue stability boundaries).
- Contract-fixture validation in CI against the pinned bundle tag (I1 obligation): validate accepted inputs against fixtures AND emitted recommendations against `capacity-recommendation.schema.json`.
- Holdout protocol encoded in the fitting API (structural train/holdout split); a test proves fit-quality reporting on training data is impossible.
- Determinism tests: same seed + same inputs ⇒ byte-identical result tables.
- A test that cannot fail is not evidence — review generated suites for real failure modes.

**Observability (`docs/observability.md`):** fleetlab is offline; its observability is run-record discipline. Every output artifact embeds: contract bundle version, input file digests, seed, fleetlab version/commit, timestamp, and per-parameter provenance flags. Logs name every rejected input with file/field/rule.

**Security (`docs/security.md`):** input files are untrusted data — schema validation before use, no code execution from inputs (no pickle, no eval; YAML safe-load only), path handling confined to declared input/output dirs. No secrets, no network calls at runtime (contract bundles are vendored/pinned, not fetched at run time).

**Performance hypotheses (`docs/experiments.md` seeds — each becomes a seeded simulation experiment with a written hypothesis):**
1. GPU utilization is not a reliable overload signal (source-reported, as of 2026-07): predicted-goodput deficit and queue depth detect overload earlier and with fewer false positives on `bursty` and `gen-long-out` than GPU utilization. Test in simulation; report where each signal fails.
2. KV-memory-per-token model predicts measured engine memory within stated error for llama.cpp (CPU) and vLLM profiles; disagreement localizes to allocator/fragmentation effects the formula ignores (document the residual).
3. Cold-start delays dominate headroom requirements on `bursty` workloads: required headroom is set by warm-up time × arrival growth rate, not steady-state throughput.
4. Cost per 1M tokens at SLO is most sensitive to goodput near the saturation knee, not to raw GPU price — sensitivity analysis quantifies this.
5. On heterogeneous fleets, workload affinity (long-context vs short-chat) changes optimal placement even when per-GPU cost/throughput ratios are equal.

---

## 10. Integration milestones this repo participates in

**I1 — Contract compatibility (fleetlab is one of four consumers).** Acceptance: all four consumers (infergate, inferbench, fleetlab, inferops) validate the golden fixtures and their own emitted artifacts against the bundle in CI; unsupported-field rejection cases covered. Re-run on every contract release; **the v1.0.0 re-run is a prerequisite for I6**. fleetlab's obligation: `make contracts-verify` (or equivalent) green in CI against the pinned bundle tag.

**I6 — Capacity feedback (the central story; fleetlab's headline milestone).**
- **Owner:** inference-lab (loop), **fleetlab (recommendation)**.
- **Prerequisites:** I5 (operational stack accepted); FL-T009; IO-T009 (inferops autoscaling experiment); contracts v1.0.0 (SC-T010); benchmark corpus from IB-T010/T011.
- **Pins:** everything above + fleetlab release.
- **Acceptance:** benchmark results → fleetlab produces a schema-valid capacity recommendation (with stated uncertainty) → inferops applies the recommended change (replica count / config) → repeated benchmark measures the outcome → **predicted vs measured compared and published, including where the prediction was wrong.**
- **Future commands (indicative):** `fleetlab recommend --results ... --slo ... --cost ...`; inferops apply; `inferbench` re-run.
- **Failure handling:** prediction badly off → that is a *result*, not a failure — publish the error analysis and refine profiles (G8); loop mechanics broken → fix Contract 7 plumbing.
- **Evidence:** the loop report (recommendation file, applied manifests, before/after benchmark results, error analysis).
- **Scale fallback:** if the GPU budget is exhausted, the loop closes at mock/llama.cpp scale with a recorded deviation — the loop must close; it may shrink, never vanish.

---

## 11. Study-track artifacts owned by this repo

Artifact-or-drop rule: every resource produces a named artifact consumed by a register task, or it is dropped. Reading rule for sources: pin versions/commits; re-verify paths at use time.

| Resource | Depth | Artifact | Consumed by | Stop condition |
|---|---|---|---|---|
| PagedAttention (SOSP'23) | deep (§1–4, §6.1–6.2; skip kernels) | KV-cache memory worksheet feeding the fleetlab memory model + overload-signal notes | FL-T003 | worksheet cross-checked vs measured memory |
| Pope et al., *Efficiently Scaling Transformer Inference* | skim | capacity-math worksheet backbone | FL-T003 | worksheet used |
| DistServe (OSDI'24) | medium | goodput@SLO definition + when-to-disaggregate decision tree | fleetlab reports; contracts metric vocabulary | definition encoded in schemas; decision tree published |
| *AI Engineering* (Huyen), serving/inference chapters | chapter-selective | capacity-report structure review; gap check vs fleetlab reports | fleetlab report templates | review note done |
| *Computer Architecture: A Quantitative Approach*, memory-hierarchy + accelerator chapters | skim | GPU-literacy note (bandwidth vs FLOPs reasoning) feeding hardware profiles | fleetlab hardware profiles | note done |

Point resource: Modal GPU Glossary / vLLM docs (V1 guide, metrics design, optimization) → fleetlab profile inputs (as of 2026-07 — re-verify at use time).

---

## 12. OSS opportunities (modest for this repo)

- **Published capacity/goodput methodology artifacts** (the holdout-validation report, the signal-comparison methodology, the KV-memory worksheet) qualify as the program's "public benchmark or design artifact" OSS-track item.
- **Possible upstream feedback to vLLM docs** on the metrics used for profile fitting (e.g., documentation drift or ambiguity in waiting/KV-usage gauges discovered during ingestion) — vLLM is the program's OSS fallback target, docs/metrics/tests scope only, grounded in measured evidence with full manifests. Any submission requires user review before posting; maintainer responsiveness is unverified as of 2026-07 — re-verify live.
- Never: scheduler rewrites, architecture proposals, unverified performance claims.

---

## 13. Risks and kill criteria

| ID | Risk | Trigger | Mitigation |
|---|---|---|---|
| **R9** (owner: fleetlab; L:M, I:H) | **fleetlab drifts into fantasy — models unmoored from measurements** | holdout validation error exceeds stated bounds; profiles cover hardware never measured | **G8 holdout gate; provenance-mandatory profiles; the limitations report is a required artifact** |
| R3 (shared) | ecosystem drift (engine metric names change under a new pin) | mapping/conformance failures on new pins | capability metric-name mapping, never hardcoding; dated provenance on ecosystem facts |
| R12 (program) | overclaiming — numbers without provenance | any claim lacking a manifest/log | evidence rules; reproducibility audit at I8 removes unreproducible claims |

**Pre-decided reductions (never cut under pressure — these are the pre-approved fallbacks):**
- Program kill order item: KEDA/autoscaling breadth is cut before fleetlab work — the cut keeps **one HPA experiment + the fleetlab simulation**.
- **FL-T007 heterogeneous-placement depth is reducible to two hardware profiles** (recorded as a deviation, not silently).
- **Never-cut:** the I6 feedback loop. It may shrink to mock/llama.cpp scale if the GPU budget is gone, but it must close.
- Generic drop rule applies: drop anything that blocks the critical path without new evidence, duplicates a capability, lacks a measurable artifact, or creates tight source coupling (e.g., importing inferbench code).

---

## 14. Definition of Done (repo acceptance)

fleetlab is done when, with evidence linked from `docs/`:

1. **G8 holdout gate passed:** prediction of a benchmark run not used for fitting, within stated error bars — or the miss published as an honest limitation with error analysis (prediction error is a result).
2. **All five required reports published:** autoscaling policy comparison; cold-start headroom; heterogeneous placement; cost/capacity model; **simulation limitations** (the mandatory honesty artifact).
3. **Recommendation consumed by inferops:** a Contract-7 file validated in CI, consumed in an inferops dry run, and used in the real I6 loop (at whatever scale the budget permitted, with deviations recorded).

Program-level context: the portfolio's honest-limitations statement (published at I8) includes "simulation ≠ production — fleetlab predictions carry stated uncertainty." Nothing you build may contradict that sentence.

---

## 15. Deviation policy

> Keep `docs/implementation-notes.md`. When repository evidence forces a deviation from the approved plan, choose the conservative reversible option, record the evidence, decision, consequences, and follow-up under `Deviations`, and continue. Pause only when the deviation changes public contracts, repository ownership, security posture, or milestone scope.

---

## 16. Session operating instructions

1. **First:** execute FL-T001 — create the full `docs/` set (§5). Present the plan (charter, scope, non-goals, milestones, tasks) for review before writing implementation code.
2. Then implement strictly in task dependency order: FL-T002 → FL-T003 → FL-T004 (G8 review) → {FL-T005, FL-T007, FL-T008 parallel-safe} → FL-T006 → FL-T009. Never start a task whose dependencies lack evidence.
3. Pin the contracts bundle version at session start; record it in `docs/interfaces.md` and in every emitted artifact. Contract questions are filed against serving-contracts, never patched locally.
4. Every simulation/fitting run: seeded, inputs digested, outputs carry provenance. Every claimed number: measured / source-reported / assumed + date.
5. Commit with clear messages, one reviewable concern per commit. Never push to, edit, or import from other repositories — inferbench data arrives as files; recommendations leave as files.
6. Record everything notable — surprises, assumption changes, reduced scope, prediction misses — in `docs/implementation-notes.md`; deviations go under its `Deviations` heading per §15.
7. Mandatory human-review points: the docs-set plan (FL-T001), G8 evidence (FL-T004 and FL-T009 limitations report), every ADR, any OSS submission before posting.
