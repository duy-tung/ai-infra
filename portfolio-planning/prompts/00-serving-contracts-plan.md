# serving-contracts — Standalone Planning & Implementation Prompt

You are working on the repository **serving-contracts**, part of the `inference-systems` portfolio. This prompt is self-contained: everything you need is embedded here. Do not assume access to the master planning repository.

---

## 1. Mission & context

**Program summary.** The `inference-systems` program builds six independent, composable repositories that together form one production-grade LLM inference-serving platform and that individually demonstrate senior-level engineering judgment: `serving-contracts` (this repo — versioned specs and schemas), `infergate` (the only gateway, Go), `inferbench` (the only load-generation + benchmark-analysis system, Go + Python), `fleetlab` (capacity/autoscaling/cost/placement simulation, Python), `inferops` (the only Kubernetes/observability/chaos/runbook stack), and `inference-lab` (integration, evidence, portfolio narrative, OSS log). The program converts an experienced backend/platform engineer's strengths (Go, PostgreSQL, distributed systems, streaming correctness, observability, reliability) into verifiable AI-inference-infrastructure evidence.

**Target positioning of the portfolio (verbatim program goal):**

> Senior Backend / Platform Engineer capable of designing, building, benchmarking, operating, and reasoning about production-grade distributed AI inference infrastructure, with particular strength in streaming correctness, backpressure, scheduling boundaries, observability, capacity planning, reliability, and infrastructure orchestration.

**This repo's purpose.** `serving-contracts` holds the versioned specifications and schemas for the whole portfolio: the OpenAI-compatible API subset, streaming/error/cancellation semantics, the metric and trace vocabulary, and every cross-repo data schema. It contains **NO runtime business logic** — schema-validation tooling is the only permitted code. All contracts are versioned together as one bundle under SemVer and released as git tags with downloadable artifacts; consumers pin a bundle version.

**Independent value.** Any OpenAI-compatible serving project — inside or outside this portfolio — can adopt the API subset definition, the metric vocabulary with normative measurement points, the benchmark-data schemas, or the fault-scenario catalog. The repo is useful alone as a rigorously specified, fixture-backed contract set.

**Integration value.** It is the root of the portfolio dependency graph: all five other repos consume the pinned released bundle, and no cross-repo interaction is legal except through these contracts, released artifacts, files, or documented network protocols. Milestone I1 (contract compatibility) is owned here.

## 2. Hard rules (program-wide, non-negotiable)

1. Repositories integrate ONLY via versioned contracts, released artifacts, files, or documented network protocols. The dependency graph is acyclic. No shared application library, ever.
2. One gateway (`infergate`), one load-generation system (`inferbench`), one deployment stack (`inferops`) exist in the whole program — never duplicate any of them.
3. No Kafka, NATS, Redis Streams, or any broker in the synchronous inference request path.
4. The gateway never owns continuous batching, per-token scheduling, KV-cache internals, prefix-cache internals, or GPU placement — those are engine-owned. Contracts you write must not smuggle engine-scheduling concepts into gateway responsibilities.
5. Basic development and CI must not require a GPU. (This repo is 100% GPU-free by construction.) Any GPU session anywhere in the program requires a written hypothesis + full config manifest + auto-stop script + budget alert; program GPU envelope ~$150–250 total (as of 2026-07; user-confirmable).
6. Evidence rules: never claim tests/validation/releases succeeded without command output or artifacts to point at; every number carries provenance (measured / source-reported / assumed) and a date; invalid benchmark runs are invalidated, never published; `go test -race` clean is the floor for any Go concurrency work (mostly N/A here — validation tooling should stay simple and single-purpose).
7. Volatile ecosystem facts (engine metric names, upstream repo layouts, GPU prices, OTel GenAI semconv status) carry "as of 2026-07 — re-verify at use time" flags. Preserve those flags inside the contracts you author.

## 3. Dependencies & contracts

**This repo depends on nothing.** Forbidden edges (checked at every review gate):

- `serving-contracts` → anything. It must remain dependency-free; validation tooling may use standard schema validators only (JSON Schema validators, OpenAPI linters). No provider SDKs, no generated service frameworks, no other portfolio repo.
- The repo must never import, vendor, or generate code for consumers. Consumers validate against fixtures; they do not link against this repo.

**This repo provides** the entire contract bundle. Consumers and their roles:

| Consumer | Consumes | Role |
|---|---|---|
| infergate | Contract 1 (implements), 2 (emits), 4 (adapters declare + probe), 5 (publishes descriptor per release), 6 (semantics tests) | pinned released bundle; CI validates fixtures |
| inferbench | Contract 1 (drives), 2 (client-side mirror definitions), 3 (emits), 4 (feature-gates workloads), 6 (client-impact measurement) | pinned bundle; emits schema-conformant files |
| fleetlab | Contract 2 (model inputs), 3 (consumes), 4 (model constraints), 7 (emits) + hardware/model/SLO/cost schemas | pinned bundle; validates input files |
| inferops | Contract 2 (dashboards/alerts), 4 (probe configuration), 5 (consumes), 6 (injects), 7 (applies as experiment) | deployment contract + fault-scenario schema |
| inference-lab | all (compatibility matrix + pins; demos; postmortems; Scenario E evidence) | compatibility matrix + pins file |

Deliberate single-consumer exclusion: **infergate's admin API (`/admin/v1/...`) is repo-private, NOT a shared contract** — single consumer; avoid speculative contract surface. Promote to a shared contract only if a second consumer appears (recorded program assumption A4).

Change-propagation rules you own: MINOR/additive → consumers upgrade at their own pace; compatibility tests stay green on both old and new fixtures during the deprecation window. MAJOR/breaking → migration note here, version bump in every consumer, and re-run of milestone I1 before any cross-repo scenario is re-claimed. Any inferbench schema-affecting change is blocked unless contracts released it first — schemas live here, not in inferbench.

## 4. The seven contracts (design-level definitions — you are the author)

You must turn each definition below into concrete spec/schema files plus golden example fixtures. These definitions are the approved design; deviations touch public contracts and therefore require a pause per the deviation policy.

### Candidate artifact layout

```text
openapi/inference-api.yaml
schemas/backend-capability.schema.json
schemas/workload.schema.json
schemas/benchmark-run.schema.json
schemas/raw-event.schema.json
schemas/benchmark-result.schema.json
schemas/hardware-profile.schema.json
schemas/model-profile.schema.json
schemas/slo.schema.json
schemas/cost-profile.schema.json
schemas/deployment-contract.schema.json
schemas/fault-scenario.schema.json
schemas/capacity-recommendation.schema.json
metrics/metrics.md
metrics/cardinality-policy.md
compatibility/compatibility-policy.md
examples/            # golden fixtures used by consumer compatibility tests
```

### Contract 1 — Inference API (OpenAI-compatible subset)

**Consumers:** infergate (implements), inferbench (drives), inferops (smoke tests), inference-lab (demos).

- **Endpoints:** `POST /v1/chat/completions` (stream + non-stream), `GET /v1/models`, `GET /healthz`, `GET /readyz`, `GET /metrics`. Admin surface (`/admin/v1/...`) is defined by infergate and is explicitly *not* part of the shared contract.
- **Supported subset:** explicitly enumerated request fields — `model`, `messages`, `max_tokens`/`max_completion_tokens`, `temperature`, `top_p`, `stream`, `stream_options.include_usage`, `stop`, `seed`, `user`. All unsupported fields are **rejected with a typed error, never silently ignored**. Response objects mirror the OpenAI chat-completion and chunk shapes for the supported subset.
- **Streaming semantics:** SSE with `data: <json-chunk>` events; terminal `data: [DONE]`; every event flushed; usage in the final chunk when `stream_options.include_usage=true`; per-event ordering guarantees (no interleaving across requests; monotonically increasing chunk indices per stream).
- **Error envelope:** `{"error": {"message", "type", "code", "param"}}` plus request ID. Error taxonomy with retryability: `invalid_request`, `authentication`, `permission`, `not_found`, `rate_limited` (429 + `Retry-After`), `overloaded` (503 + `Retry-After`), `upstream_error`, `upstream_timeout`, `canceled`, `internal`. Mid-stream failures are a standardized SSE error event followed by stream close — **never a retry** (post-first-token retry would duplicate sampled output and double-bill).
- **Request-ID contract:** `X-Request-Id` accepted or generated; echoed in responses, error bodies, traces, and usage records; it is the idempotency key for usage settlement.
- **Cancellation contract:** client disconnect or explicit connection close MUST propagate upstream (HTTP body close); observable effects (engine abort, resource release) are part of conformance; tokens emitted before cancellation are billable.

### Contract 2 — Metrics and trace vocabulary

**Consumers:** infergate (emits), inferops (dashboards/alerts), inferbench (client-side mirror definitions), fleetlab (model inputs).

Canonical metric set (Prometheus naming; units in name; histograms with declared bucket boundaries):

| Metric | Type | Labels |
|---|---|---|
| `inference_requests_total` | counter | `model`, `backend`, `tenant_tier`, `status_class`, `error_class` |
| `inference_requests_in_flight` | gauge | `backend` |
| `inference_queue_depth` | gauge | `tenant_tier` |
| `inference_queue_wait_seconds` | histogram | `tenant_tier` |
| `inference_ttft_seconds` | histogram | `model`, `backend` |
| `inference_itl_seconds` | histogram | `model`, `backend` |
| `inference_e2e_duration_seconds` | histogram | `model`, `backend`, `status_class` |
| `inference_sheds_total` | counter | `reason` |
| `inference_retries_total` | counter | `stage` (always pre-first-token) |
| `inference_backend_healthy` | gauge | `backend` |
| `inference_usage_tokens_total` | counter | `direction` (input/output), `model`, `tenant_tier` |

- **Cardinality policy:** allowed label values are enumerable and low-cardinality (`model`, `backend`, `tenant_tier`, `status_class`, `error_class`, `reason`, `stage`, `direction`). Forbidden as labels: request IDs, raw tenant/user IDs, prompts, arbitrary strings. Per-request detail belongs in traces; exemplars link histograms to traces.
- **Trace attributes:** OTel GenAI semantic conventions at a **pinned version** (status "Development" as of 2026-07 — re-verify at use time; the pin is mandatory), plus platform attributes `inference.config_version`, `inference.tenant_tier`, `inference.backend`, `inference.request_id`. Gateway span sequence: `recv → queue.wait → upstream.connect → ttft → stream.relay → settle`.
- **Measurement-point definitions (normative — gateway, benchmark, and simulation numbers must be comparable):** TTFT = first upstream body byte at the gateway (client-side TTFT measured by inferbench is a separate, named series); ITL = inter-chunk gap; queue wait = admission-enqueue to dispatch.

### Contract 3 — Benchmark data (workload, run, raw events, results)

**Consumers:** inferbench (emits), fleetlab (consumes), inference-lab (reports).

- **workload.schema.json:** name, version, seed; arrival process (`open-loop-poisson` rate | `closed-loop` with mandatory disclosure flag); input/output-length distributions; prefix-sharing ratio; cancellation-rate profile; slow-client profile; duration or request count. The eight named workloads — `chat-short`, `rag-long-in`, `gen-long-out`, `shared-prefix`, `mixed`, `bursty`, `cancel-storm`, `slow-client` — ship as versioned examples.
- **benchmark-run.schema.json (manifest):** run ID; target topology (`engine-direct` | `via-gateway` | `gateway-mock`); engine name/version/commit + all runtime flags (`max_num_seqs`, `max_num_batched_tokens`, `gpu_memory_utilization`, prefix caching, chunked prefill, quantization, KV dtype, speculative decoding config); model checkpoint + revision + tokenizer; hardware (GPU model, VRAM, driver, CUDA version, instance type); gateway version + config version; client location/RTT; warm-up policy; repetition count; hypothesis statement.
- **raw-event.schema.json:** one JSONL record per request: request ID, workload item, send timestamp, TTFT, ITL series or summary + max stall, end timestamp, status, error class, input/output token counts, shed/retry flags, cancellation point.
- **benchmark-result.schema.json:** aggregates per run set: pooled-percentile tables (percentiles computed on pooled raw data — never averaged across runs), throughput, goodput with explicit SLO reference, shed rate (always adjacent to goodput), stall rate, saturation-knee estimate, cost per successful request and per 1M tokens (with cost-profile reference), validity block (warm-up handling, run count, threats to validity, unexplained anomalies), links to raw events and manifest.

### Contract 4 — Backend capability

**Consumers:** infergate (adapters declare + probe), inferbench (feature-gates workloads), fleetlab (model constraints), inferops (probe configuration).

Fields: engine name + version/commit; streaming support; usage-in-stream support; cancellation mechanism (HTTP-close semantics) and expected release observability; metrics endpoint + name mapping (e.g. vLLM waiting/KV-usage gauges — names vary by version and must be mapped, not hardcoded); tokenizer identity; context limit; max concurrency hints; prefix-cache support + observability; quantization; priority support. Capability descriptors for the mock backend, llama.cpp, and vLLM ship as examples.

### Contract 5 — Deployment

**Consumers:** infergate (publishes descriptor per release), inferops (consumes), inference-lab (pins).

Fields: image + digest; ports (API, metrics); environment variables and config mounts; startup/readiness/liveness semantics including warm-up-aware readiness (readiness false during model load/warm-up); model mount path and expected volume; resource requests/limits including GPU count; graceful termination (`preStop` drain hook, termination grace period > max stream duration); secret expectations.

### Contract 6 — Fault scenarios (shared vocabulary for milestone I7)

**Consumers:** inferops (injects), infergate (semantics tests), inferbench (client-impact measurement), inference-lab (postmortems).

The 12 required scenarios, each encoded with: ID, injection description, expected gateway semantics, expected client-visible behavior, metrics that must move, and abort condition:

1. backend killed before first token → pre-first-token retry within budget or typed 5xx
2. backend killed after first token → SSE error event, no retry, partial usage settled
3. slow backend → pressure-aware routing shifts; timeouts typed
4. slow client → bounded write buffer + write deadline; stream closed, engine released
5. gateway termination during streaming → drain semantics; accepted streams complete
6. queue saturation → sheds with 429 + `Retry-After`; accepted-request latency protected
7. retry storm → retry budget caps amplification
8. config reload during traffic → snapshot swap, zero dropped streams
9. usage database failure → requests unaffected; settlement backlog drains idempotently
10. one unhealthy backend → routing shifts within bounded interval; circuit opens on error rate
11. readiness during model warm-up → no traffic before warm; no restart loops
12. rolling update with active requests → zero client-visible errors

### Contract 7 — Capacity recommendation (fleetlab → inferops)

**Consumers:** fleetlab (emits), inferops (applies as experiment), inference-lab (Scenario E evidence).

Fields: input references (benchmark-result IDs, workload version, SLO, cost profile, hardware profiles); recommended topology (replica counts per hardware type, engine config); predicted goodput/latency/cost with stated uncertainty; autoscaling signal + thresholds recommendation; assumptions and sensitivity notes. This closes the I6 feedback loop in a machine-checkable form.

### Fleet schemas (feed Contracts 3 and 7)

`hardware-profile`, `model-profile`, `slo`, `cost-profile` schemas all carry **mandatory provenance fields** (measured / source-reported / assumed + date) — no fabricated defaults. The SLO schema must be able to express the program's source-verified gateway targets (as of 2026-07, re-baseline from measurement if infeasible): non-queue gateway overhead p95 <10ms / p99 <20ms; cancellation propagation p95 <250ms (gateway+mock path); usage settle variance <1%; key revocation ≤5s; config publish ≤5s. Model-level TTFT/ITL/goodput SLOs are declared only from measurement, never in advance.

### Versioning and evolution policy (you author and enforce this)

- **SemVer on the bundle.** MAJOR = any breaking change (removed/renamed field, semantics change, metric rename, bucket change); MINOR = additive optional fields, new schemas, new examples; PATCH = clarifications and fixture fixes.
- **Breaking-change definition:** anything that can make a previously-valid consumer artifact invalid, or change the meaning of a previously-recorded measurement.
- **Deprecation:** deprecated fields carry `deprecated: true` + a removal version; at least one MINOR release separates deprecation from removal; migration notes are mandatory for every MAJOR.
- **Consumer compatibility tests:** `examples/` golden fixtures are consumed by every repo's CI (validate emitted artifacts against schemas; validate accepted inputs against fixtures). Milestone I1 = all four consumers green against the same bundle version.
- **Supported-version matrix:** maintained in `inference-lab` (which bundle versions each released component supports).
- **Pinning:** consumers pin the bundle by SemVer tag in CI config + the inference-lab pins file. The benchmark comparability rule is normative and printed in every benchmark report: results are comparable only when model revision, quantization, tokenizer, engine version+flags, hardware, driver/CUDA, workload version+seed, and warm-up policy all match, or the difference is the single declared experimental variable.
- **Pre-1.0 rule:** during `v0.x`, MINOR may break with an explicit migration note (documented honestly); `v1.0.0` freezes Contract 1–3 shapes and is a prerequisite for milestone I6.

## 5. Architecture guidance

- **Components:** spec files (OpenAPI YAML, JSON Schema, normative Markdown for metrics/cardinality/compatibility), golden fixtures under `examples/` (positive AND negative — e.g. unsupported-field requests that must be rejected), and one minimal validator kit (CLI or config) that consumers invoke in CI. That kit is the only code; it must stay validation-only — the moment it grows request handling, code generation, or shared helpers for consumers, you have violated the ownership matrix.
- **Interfaces:** the release bundle (git tag + downloadable artifact) is the only interface. Consumers never check out this repo's source in their build; they fetch a pinned release.
- **Data & state:** the repo is stateless. All state is versioned files in git; the release tag is the unit of truth.
- **Concurrency model:** none needed. Keep tooling single-threaded and deterministic.
- **Failure/cancellation/retry behavior:** this repo *defines* those semantics (Contract 1 error taxonomy + retryability, Contract 6 expected semantics) but implements none of them. Your job is to make the definitions unambiguous enough that infergate can test against them and inferops can observe them.
- **Normativity discipline:** every spec statement is either normative (MUST/MUST NOT, machine-checkable where possible) or explanatory. Where a rule cannot be schema-encoded (e.g. "percentiles are computed on pooled raw data, never averaged across runs"; "shed rate always adjacent to goodput"), encode it as required fields/structure (e.g. `benchmark-result` requires the validity block and places shed rate next to goodput) plus a normative sentence in the schema `description`.

## 6. Required documentation set (FIRST task: SC-T001)

Create `docs/` with exactly this set:

```text
docs/
├── charter.md               # mission, independent + integration value, ownership boundary (specs only)
├── architecture.md          # artifact layout, bundle/release mechanics, validator-kit design, normativity rules
├── scope.md                 # the seven contracts + fleet schemas + metric vocabulary + compatibility policy
├── non-goals.md             # see §7 below; explicit list, each with the reason
├── interfaces.md            # the release bundle interface; per-contract consumer table; fixture usage per consumer
├── milestones.md            # repo milestones from §8, dependency-ordered, acceptance criteria
├── tasks.md                 # SC-T001…SC-T010 with full schema fields (§9)
├── risks.md                 # R8, R3, R1 + pre-1.0 churn + single-consumer-contract guard (§13)
├── testing.md               # schema lint, fixture validation (positive+negative), kit self-test, CI matrix (§10)
├── observability.md         # this repo DEFINES the vocabulary; document stewardship + drift-check procedure
├── security.md              # no secrets/PII in fixtures; cardinality policy as PII guard; error-envelope leak rules
├── experiments.md           # N/A for runtime; record spec-ambiguity probes (e.g. semconv gap notes for OSS track)
├── integration.md           # I1 ownership, I1 re-run triggers, v1.0.0-before-I6 rule, consumer wiring guide
├── oss-opportunities.md     # OTel GenAI semconv track (§12)
├── implementation-notes.md  # running log + Deviations section (deviation policy §14)
└── adr/                     # e.g. bundle-vs-per-schema versioning; JSON Schema draft choice; OpenAPI version; fixture layout
```

## 7. Non-goals (state verbatim in `docs/non-goals.md`)

No gateway logic. No load generator. No Kubernetes manifests. No capacity/planner models. No database. No provider SDKs. No generated service frameworks (schema-validation tooling only). No runtime business logic of any kind. No speculative contract surface for single-consumer interfaces (infergate's admin API stays repo-private to infergate). No shared application library for consumers.

## 8. Repository milestones (dependency-ordered; no calendar durations)

| # | Milestone | Depends on | Acceptance criteria |
|---|---|---|---|
| M1 | Docs + versioning/compatibility policy committed | plan approval | all 15 docs exist with content; `compatibility/compatibility-policy.md` states SemVer rules, breaking-change definition, deprecation rules, release process; policy reviewed by the user |
| M2 | Core contracts drafted (API + benchmark data) | M1 | `openapi/inference-api.yaml` lints; 4 benchmark schemas valid; fixtures cover stream, non-stream, every error class, and all 8 named workloads |
| M3 | Full schema set | M1 (parallel with M2 tail) | capability (3 example descriptors), metrics vocabulary + cardinality policy, deployment, fault-scenario (12 encoded), 5 fleet schemas — all examples validate |
| M4 | Consumer compatibility kit | M2 | kit runs green locally; documented usage shows all four consumer repos can wire it into CI without checking out this repo's source |
| M5 | **v0.1.0 release** → I1 | M2, M3 (Contracts 1–3 + capability + metrics), M4 | tag exists with release notes + migration policy; all four consumers pin it and are green (I1 accepted) |
| M6 | Evolution stewardship through v0.x | M5 | every change classified (MAJOR/MINOR/PATCH); ≤1 breaking change per program wave after v0.2 (R8 trigger); at least one deprecation or migration executed cleanly through the policy |
| M7 | **v1.0.0 freeze** | M6 + operational experience from milestone I5 | breaking-change audit done; migration notes for accumulated changes; consumer kits green on v1.0.0; I1 re-run green — this is a prerequisite for milestone I6 |

## 9. Task seeds (stable IDs — use exactly these)

**SC-T001 — Bootstrap repo docs + versioning/compatibility policy.**
- Goal/Repository: create the full `docs/` set and the compatibility policy. serving-contracts.
- Requirement: contract inventory (all seven + fleet schemas), SemVer rules, breaking-change definition, deprecation rules, release process, consumer-test approach — per §4 "Versioning and evolution policy".
- Dependencies: approved plan. Expected files: `docs/*` (all 15 + `adr/`), `compatibility/compatibility-policy.md`.
- Complexity: Small. Critical path: yes. Parallel-safe: no. Required.
- Review focus: policy soundness (breaking-change definition covers measurement-meaning changes, not just shape changes).
- Verification: docs complete per §6 checklist; policy internally consistent (pre-1.0 rule, deprecation window, I1 re-run triggers all stated).
- Evidence: committed policy + docs. Integration impact: unblocks all consumers and every other SC task.
- Stop condition: policy reviewed by the user.

**SC-T002 — Inference API contract.**
- Goal/Repository: author Contract 1 as OpenAPI + fixtures. serving-contracts.
- Requirement: OpenAPI subset (endpoints + the enumerated request-field subset, rejection-not-ignore rule), SSE semantics (`data:` framing, `[DONE]`, flush, ordering, usage-in-stream via `stream_options.include_usage`), error envelope + full taxonomy with retryability, request-ID contract, cancellation contract, examples — per §4 Contract 1.
- Dependencies: SC-T001. Expected files: `openapi/inference-api.yaml`, `examples/api/*` (positive + negative fixtures).
- Complexity: Medium. Critical path: yes. Parallel-safe: no. Required.
- Review focus: subset completeness vs OpenAI shapes; the rejection-not-ignore rule; mid-stream-error-never-retried semantics.
- Verification: spec lints (OpenAPI linter); fixtures validate against the spec; negative fixtures (unsupported fields) exist for each rejection case.
- Evidence: spec + fixtures + lint output. Integration impact: gates IG-T002 (gateway skeleton) and IB-T002 (generator core).
- Stop condition: fixtures cover stream, non-stream, and all ten error classes.

**SC-T003 — Benchmark data schemas.**
- Goal/Repository: author Contract 3. serving-contracts.
- Requirement: workload / benchmark-run / raw-event / benchmark-result schemas with every field listed in §4 Contract 3, plus the 8 named workload examples.
- Dependencies: SC-T001. Expected files: `schemas/{workload,benchmark-run,raw-event,benchmark-result}.schema.json`, `examples/workloads/*`.
- Complexity: Medium. Critical path: yes. Parallel-safe: yes. Required.
- Review focus: manifest completeness (pins, engine flags, hardware, warm-up policy, hypothesis); pooled-percentile + shed-adjacent-goodput + validity-block rules encoded in structure, not just prose.
- Verification: JSON Schema validation of all examples; a deliberately incomplete manifest fixture fails validation.
- Evidence: schemas + examples + validator output. Integration impact: gates IB-T002 and FL-T002.
- Stop condition: all 8 workloads expressible (including prefix-sharing ratio, cancellation-rate and slow-client profiles, closed-loop disclosure flag).

**SC-T004 — Backend-capability schema.**
- Goal/Repository: author Contract 4. serving-contracts.
- Requirement: capability fields per §4 Contract 4, including metric-name mapping (engine metric names vary by version — mapped, never hardcoded; as of 2026-07, re-verify) and cancellation-release observability.
- Dependencies: SC-T001. Expected files: `schemas/backend-capability.schema.json`, `examples/capabilities/{mock,llamacpp,vllm}.json`.
- Complexity: Small. Critical path: no. Parallel-safe: yes. Required.
- Review focus: no engine internals leak into gateway responsibilities (capability describes what the engine exposes, not how the gateway should schedule).
- Verification: three example descriptors validate.
- Evidence: schema + examples. Integration impact: infergate adapters (IG-T005/T012/T014), inferbench feature-gating.
- Stop condition: mock, llama.cpp, and vLLM example descriptors validate.

**SC-T005 — Metrics vocabulary + cardinality policy.**
- Goal/Repository: author Contract 2. serving-contracts.
- Requirement: the canonical metric table (all 11 metrics with types, labels, units-in-name, declared histogram bucket boundaries), forbidden-label list, trace attributes with the OTel GenAI semconv version pin (status "Development" as of 2026-07 — pin mandatory, re-verify at use time), platform attributes, span sequence, and the normative TTFT/ITL/queue-wait measurement-point definitions.
- Dependencies: SC-T001. Expected files: `metrics/metrics.md`, `metrics/cardinality-policy.md`.
- Complexity: Small. Critical path: yes. Parallel-safe: yes. Required.
- Review focus: TTFT/ITL/queue-wait definitions unambiguous (gateway-side vs client-side series explicitly separated).
- Verification: doc review; cross-check that every metric named anywhere in the program roadmap appears here; fixture dashboard names (inferops) can be keyed to it.
- Evidence: committed vocabulary. Integration impact: IG-T006 (gateway observability), IO-T003 (dashboards), IB-T005 (analysis), FL-T003 (models). Ambiguities discovered while writing this are candidate OSS contributions (§12).
- Stop condition: every roadmap metric named here.

**SC-T006 — Deployment + fault-scenario contracts.**
- Goal/Repository: author Contracts 5 and 6. serving-contracts.
- Requirement: deployment descriptor schema (all fields in §4 Contract 5, including warm-up-aware readiness and termination-grace > max-stream-duration); fault-scenario schema + all 12 scenarios encoded with ID, injection, expected gateway semantics, expected client-visible behavior, metrics that must move, abort condition.
- Dependencies: SC-T001. Expected files: `schemas/{deployment-contract,fault-scenario}.schema.json`, `examples/faults/*`.
- Complexity: Medium. Critical path: no. Parallel-safe: yes. Required.
- Review focus: termination-grace > max-stream rule; scenario semantics match §4 Contract 6 exactly.
- Verification: examples validate; 12 scenario files present and schema-valid.
- Evidence: schemas + examples. Integration impact: IO-T002 (cluster baseline), IO-T006/T007 (fault campaigns), IG-T016 (release descriptor).
- Stop condition: 12 scenarios encoded.

**SC-T007 — Fleet schemas.**
- Goal/Repository: author hardware/model/SLO/cost/capacity-recommendation schemas (Contract 7 + inputs). serving-contracts.
- Requirement: five schemas with mandatory provenance fields (measured / source-reported / assumed + date); capacity-recommendation fields per §4 Contract 7 including stated uncertainty; SLO schema expresses the §4 gateway targets and supports measurement-derived model-level SLOs.
- Dependencies: SC-T001. Expected files: `schemas/{hardware-profile,model-profile,slo,cost-profile,capacity-recommendation}.schema.json`, examples.
- Complexity: Medium. Critical path: no. Parallel-safe: yes. Required.
- Review focus: provenance mandatory (validation fails without it); no fabricated defaults.
- Verification: examples validate; a provenance-less example fails.
- Evidence: schemas + examples. Integration impact: FL-T002 (ingestion), IL-T006 (Scenario E / milestone I6).
- Stop condition: Scenario E (benchmark results → recommendation → deployment change → re-measurement) is expressible end-to-end in fixtures.

**SC-T008 — Consumer compatibility test kit.**
- Goal/Repository: golden fixtures + validation tooling consumable in each consumer repo's CI. serving-contracts.
- Requirement: `examples/**` organized as the golden fixture set (positive + negative); a minimal validator CLI/config wrapping standard schema validators; documented wiring instructions per consumer (fetch pinned release → validate own emitted artifacts against schemas → validate accepted inputs against fixtures).
- Dependencies: SC-T002, SC-T003. Expected files: `examples/**`, minimal validator CLI/config, usage docs.
- Complexity: Medium. Critical path: yes. Parallel-safe: no. Required.
- Review focus: kit stays validation-only (no framework, no shared library creep).
- Verification: kit runs green locally against all fixtures; deliberately broken fixture fails.
- Evidence: kit output (both green and demonstrated-failure runs). Integration impact: this is the I1 mechanism.
- Stop condition: four consumer repos can wire it (documented usage, no source checkout of this repo needed).

**SC-T009 — Release v0.1.0.**
- Goal/Repository: first tagged bundle. serving-contracts.
- Requirement: tagged bundle + release notes + migration policy stated (pre-1.0 rules explicit).
- Dependencies: SC-T002–T005, SC-T008. Expected files: tag `v0.1.0`, release notes, downloadable bundle artifact.
- Complexity: Small. Critical path: yes. Parallel-safe: no. Required.
- Review focus: release notes (mandatory user review — contract releases are a program review point).
- Verification: tag exists; bundle artifact downloadable; consumers pin it.
- Evidence: the release. Integration impact: opens program Waves 2+ for all consumers.
- Stop condition: milestone I1 green on v0.1.0.

**SC-T010 — v1.0.0 freeze.**
- Goal/Repository: freeze Contracts 1–3 shapes before milestone I6. serving-contracts.
- Requirement: breaking-change audit of everything accumulated during v0.x; migration notes for all accumulated changes; freeze Contract 1 (API), Contract 2 (metrics — via I1 fixtures), Contract 3 (benchmark data).
- Dependencies: operational experience from milestone I5. Expected files: tag `v1.0.0`, migration notes, audit record.
- Complexity: Small. Critical path: no. Parallel-safe: yes. Required.
- Review focus: breaking-change audit (mandatory user review).
- Verification: consumer kits green on v1.0.0; I1 re-run green across all four consumers.
- Evidence: the release + I1 re-run CI links. Integration impact: **prerequisite for milestone I6** (the capacity-feedback loop must run on frozen contracts).
- Stop condition: I1 re-run green.

## 10. Testing

- Every schema has positive AND negative fixtures; CI validates all of `examples/` on every commit (GPU-free by construction).
- OpenAPI linting for `openapi/inference-api.yaml`; JSON Schema meta-validation (declare and pin the JSON Schema draft in an ADR).
- Kit self-test: the validator must demonstrably fail on a broken fixture — a validator that cannot fail is not evidence.
- Rejection coverage: one negative fixture per unsupported API field class and per error-taxonomy entry.
- Release check: tag content == committed content; bundle artifact reproducible from the tag.

## 11. Observability & security (as they apply to a spec repo)

- **Observability:** this repo *defines* the program's observability vocabulary (Contract 2). Its own observability is CI logs and release artifacts. Maintain a drift-check note: engine metric names and OTel GenAI semconv are volatile (as of 2026-07) — re-verify pins when consumers report conformance failures (program risk R3).
- **Security:** no secrets, API keys, tokens, or real user/tenant identifiers in any fixture. The cardinality policy doubles as a PII guard (raw tenant/user IDs and prompts forbidden as labels). The error-envelope spec must state that messages never leak internal addresses, stack traces, or upstream credentials. Deployment-contract secret expectations name *what* secrets exist, never values.
- **Performance hypotheses:** minimal by design — the only one worth recording: the validator kit adds negligible time to consumer CI (target: seconds, measured once and recorded in `docs/testing.md` with date).

## 12. Integration milestones

**I1 — Contract compatibility (THIS REPO OWNS IT).**
- Prerequisites: SC-T009 (bundle v0.1.0); consumer CI wiring in all four consumer repos. Pins: contracts v0.1.0.
- Acceptance: all four consumers (infergate, inferbench, fleetlab, inferops) validate the golden fixtures and their own emitted artifacts against the bundle in CI; unsupported-field rejection cases covered.
- Future commands (indicative): `make contracts-verify` in each consumer repo.
- Failure handling: fixture mismatch → fix consumer or file a contract defect; contract defect → PATCH release, re-run I1.
- Evidence: four green CI runs referencing the same bundle tag, linked in the inference-lab pins file.
- Re-run trigger: **every contract release** (I1 is re-entrant); the v1.0.0 re-run (SC-T010) is a prerequisite for **I6** (capacity feedback, the program's central story).

This repo also indirectly gates I2–I8: every milestone runs against pinned bundle versions, and I7 executes the 12 fault scenarios you encode in Contract 6.

## 13. Study-track & OSS

- **Study-track artifacts touching this repo:** the DistServe paper's goodput@SLO definition is encoded in the metric vocabulary and benchmark-result schema (SC-T003/T005); the goodput-critique rule ("stall rate reported beside goodput") is enforced by benchmark-result structure. The OTel GenAI semantic conventions point-resource (pin version; status "Development" as of 2026-07) feeds the trace-attribute section of SC-T005.
- **OSS opportunity (secondary program target, runs cheaply in parallel):** OpenTelemetry GenAI semantic conventions — spec/docs work, no GPU, direct overlap with your metrics contract. While writing SC-T005 you will hit real gaps and ambiguities in the conventions (they are still moving — status "Development" as of 2026-07); record each in `docs/experiments.md` as a candidate upstream clarification. Progression is gated: target sign-off happens at inference-lab task IL-T010; every upstream submission gets user review before posting. Never put OSS on the critical path; the program's contingency rules for slow review apply.

## 14. Risks and kill criteria

| Risk | Trigger | Mitigation (yours to execute) |
|---|---|---|
| R8 — contract churn destabilizing consumers (M/M) | >1 breaking change per program wave after v0.2 | pre-1.0 rules honestly applied (v0.x MINOR may break WITH migration note); consumer kits catch breaks at I1; v1.0.0 freeze before I6 |
| R3 — ecosystem drift: vLLM metric names, semconv changes (H/M) | conformance or mapping tests fail on a new pin | pin everything; capability metric-name *mapping* instead of hardcoding; dated provenance flags on all ecosystem facts |
| R1 — multi-repo overhead: release/pin churn eats building time (M/H) | pin/release bookkeeping dominates; lockstep changes across repos twice in a row | contract-first discipline; if a change here forces same-day source changes in another repo twice in a row, that is a contract gap — fix the contract, not the boundary |
| Speculative surface | a schema exists with only one real consumer | do not ship it: infergate's admin API is deliberately NOT a shared contract; apply the same test to any new schema proposal |

- **Never-cut list (program-wide):** contract validation is on it. Fixtures and the compatibility kit are not reducible.
- **Consolidation trigger (§K, user-review decision, never autonomous):** if this repo demonstrably lacks independent value at two consecutive wave exits, the pre-analyzed candidate is folding `serving-contracts` into `inference-lab`. Present evidence to the user; never decide alone.
- **Reducible/stretch here:** nothing in SC-T001–T010 is stretch; all ten tasks are Required. Depth of *examples* (extra fixtures beyond required coverage) is the only flexible dimension.

## 15. Definition of Done

The repo is accepted when: **v1.0.0 is released; milestone I1 is green across all four consumers on that version; and the compatibility policy has been exercised at least once — one deprecation or one migration executed cleanly through the documented process** (deprecation marker → MINOR window → removal, or MAJOR + migration note + consumer bumps + I1 re-run). Program-level: contracts at v1.0.0 with four consumers green and a maintained supported-version matrix is item 2 of the program Definition of Done.

## 16. Deviation policy

> Keep `docs/implementation-notes.md`. When repository evidence forces a deviation from the approved plan, choose the conservative reversible option, record the evidence, decision, consequences, and follow-up under `Deviations`, and continue. Pause only when the deviation changes public contracts, repository ownership, security posture, or milestone scope.

Note: in this repo, almost every substantive file IS a public contract — expect the pause condition to apply more often than elsewhere. Fixture additions, doc clarifications, and PATCH-level fixes proceed under the policy; field/semantics changes pause for review.

## 17. Session operating instructions

1. FIRST: execute SC-T001 — create the full `docs/` set (§6) and the compatibility policy. Get the plan reviewed by the user before writing any schema.
2. Then implement strictly in task dependency order: SC-T002/T003 (parallel), SC-T004–T007 (parallel after T001), SC-T008 (after T002/T003), SC-T009 (release, user review), then stewardship (M6) and SC-T010 when I5 experience exists.
3. Commit with clear messages, one logical change per commit. Never push to any other repository. Cross-repo verification happens via released bundles and consumer CI, never by editing a consumer in this session.
4. Record everything notable — ambiguities, semconv gaps, classification decisions (MAJOR/MINOR/PATCH), review outcomes — in `docs/implementation-notes.md`.
5. Evidence discipline: every "validates"/"lints"/"green" claim points at command output. Preserve every "as of 2026-07 — re-verify at use time" flag inside the specs you author.
