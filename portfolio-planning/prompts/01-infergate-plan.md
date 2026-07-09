# Standalone Prompt — `infergate` (thin, measurable, multi-tenant LLM inference gateway)

You are working on the repository **`infergate`**, one of six repositories in the **Composable AI Inference Systems Portfolio** (`inference-systems`). This prompt is self-contained: the master planning repository is NOT available to you. Everything you need is embedded here. Follow it exactly; record evidence-forced deviations per the Deviation Policy at the end.

---

## 1. Mission & context

**Program summary.** The portfolio is a set of six independent, composable repositories that together form one production-grade LLM inference-serving platform and individually demonstrate senior-level engineering judgment: `serving-contracts` (versioned specs/schemas, no runtime logic), `infergate` (this repo — the only gateway, Go), `inferbench` (the only load-generation + benchmark-analysis system, Go + Python), `fleetlab` (explainable capacity/autoscaling/cost/placement simulation, Python), `inferops` (the only Kubernetes/observability/chaos/runbook repository), and `inference-lab` (integration, evidence, demos, portfolio narrative, OSS log). Repos integrate only via versioned contracts, released artifacts, result files, or documented network protocols.

**Target positioning of the portfolio (verbatim program goal):**

> Senior Backend / Platform Engineer capable of designing, building, benchmarking, operating, and reasoning about production-grade distributed AI inference infrastructure, with particular strength in streaming correctness, backpressure, scheduling boundaries, observability, capacity planning, reliability, and infrastructure orchestration.

**This repo's purpose.** `infergate` is a **thin, measurable, multi-tenant LLM inference gateway in Go**. It is positioned as a **"depth artifact"** — a demonstration of exactly where gateway responsibility ends and engine responsibility begins — **NOT** a gateway product competing with LiteLLM, Envoy AI Gateway, or the Gateway API Inference Extension (GAIE). Every design decision must be explainable through that boundary thesis.

**Independent value.** `infergate + deterministic mock backend + local PostgreSQL` is a complete, GPU-free, useful system: OpenAI-compatible multi-tenant serving with admission control, fairness, quotas, streaming correctness, usage accounting, and full observability — demonstrable alone, to a stranger. **Development and CI are GPU-free.**

**Integration value.** infergate is the correctness spine of the composed platform: `inferbench` drives it over the network; `inferops` deploys its released images (never its source); `inference-lab` orchestrates scenarios A–E through it; its metrics/traces feed the shared dashboards; its fault semantics are what the failure campaign (I7) verifies.

**What infergate owns (single-owner, program-wide):**
- OpenAI-compatible endpoint for the supported subset; SSE relay with upstream cancellation.
- Validation, tenant resolution, API-key authentication (hashed keys, constant-time compare); model registry.
- Token estimation + estimate-and-settle accounting; RPM/TPM quotas; asynchronous idempotent usage persistence (PostgreSQL, append-only, unique request ID).
- Bounded per-tenant queues, fairness (priority + weighted round-robin + aging), starvation prevention; global and per-backend in-flight limits.
- Health-aware and pressure-aware routing (least-inflight power-of-two-choices; engine pressure normalized from capability-mapped metrics).
- Retry **before first token only**, retry budget, circuit breaker (opens on pre-stream error rate only), load shedding.
- Graceful drain + immutable config snapshots (atomic pointer swap; publish visible ≤5s).
- OTel traces + low-cardinality Prometheus metrics per the contracts metrics vocabulary.
- Deterministic mock backend (in-repo, `cmd/mock-backend`, configurable TTFT/ITL/error rate), llama.cpp adapter, vLLM adapter.

**What infergate does NOT own:** continuous batching, per-token scheduling, KV-cache/prefix-cache implementation or internals, GPU placement, Kubernetes manifests (beyond a reference Dockerfile/compose for local dev), benchmark statistics, fleet simulation, brokers on the request path.

---

## 2. Hard rules (program-wide, non-negotiable)

1. Repositories integrate ONLY via versioned contracts, released artifacts, files, or documented network protocols. The dependency graph is acyclic. No shared application library between repos, ever.
2. One gateway (`infergate`), one load-generation system (`inferbench`), one deployment stack (`inferops`) exist in the whole program — never duplicate any of them. Do not build load generation, benchmark statistics, or Kubernetes manifests here.
3. No Kafka, NATS, Redis Streams, or any broker in the synchronous inference request path. Hidden buffering breaks direct cancellation and adds a second queue in front of the engine's continuous batching.
4. The gateway never owns continuous batching, per-token scheduling, KV-cache internals, prefix-cache internals, or GPU placement — these are engine-owned. (Source-verified basis, as of 2026-07: vLLM V1's scheduler is a token-budget scheduler with no prefill/decode phase distinction; a second scheduler in the gateway is the "double-queuing" anti-pattern.)
5. Basic development and CI must not require a GPU. Any GPU session requires a written hypothesis + full config manifest + auto-stop script + budget alert; the program GPU envelope is ~$150–250 total (as of 2026-07; user-confirmable). In this repo only IG-T014 spends GPU time.
6. Evidence rules: never claim tests/benchmarks/deployments succeeded without command output or artifacts to point at; every number carries provenance (measured / source-reported / assumed) and a date; invalid runs are invalidated, never published; **`go test -race` clean is the floor for all Go concurrency work.**
7. Volatile ecosystem facts (engine metric names, upstream repo layouts, GPU prices, OTel GenAI semconv status) carry "as of 2026-07 — re-verify at use time" flags. Notably: vLLM pin is v0.24.x (V1 architecture); metric names must be re-verified via `curl /metrics` at IG-T014 session start; OTel GenAI semantic conventions are status "Development" as of 2026-07 and must be version-pinned.

---

## 3. Dependencies & contracts

### 3.1 Dependency position

- **infergate consumes:** a pinned released `serving-contracts` bundle (SemVer tag, e.g. `v0.1.0`); CI validates against its golden fixtures (the consumer compatibility test kit). That is infergate's ONLY dependency.
- **infergate provides:** released container images (gateway + mock-backend, pinned by digest + tag), a deployment-contract descriptor per release, and backend-capability descriptors. `inferops` consumes the images + descriptor; `inferbench` uses the released mock-backend image as a CI target; `inference-lab` pins everything.
- **Forbidden edges (checked at every review gate):** infergate → any other runtime/integration repo (it must build, test, and demo alone); infergate → any shared internal application library; any inward runtime edge (the mock backend lives in-repo precisely so none exists). `inferbench` reaches infergate over the network at run time only; `inferops` consumes images only — neither may ever require an infergate source checkout, and infergate must never require theirs.
- The admin surface (`/admin/v1/...`) is repo-private, NOT part of the shared contract (single consumer). Promote it to a contract only if a second consumer appears (recorded deviation).

### 3.2 Contract 1 — Inference API (OpenAI-compatible subset) — infergate IMPLEMENTS

- **Endpoints:** `POST /v1/chat/completions` (stream + non-stream), `GET /v1/models`, `GET /healthz`, `GET /readyz`, `GET /metrics`.
- **Supported subset (enumerated request fields):** `model`, `messages`, `max_tokens`/`max_completion_tokens`, `temperature`, `top_p`, `stream`, `stream_options.include_usage`, `stop`, `seed`, `user`. **All unsupported fields are rejected with a typed error, never silently ignored.** Responses mirror OpenAI chat-completion and chunk shapes for the subset.
- **Streaming:** SSE `data: <json-chunk>` events; terminal `data: [DONE]`; every event flushed; usage in the final chunk when `stream_options.include_usage=true`; no interleaving across requests; monotonically increasing chunk indices per stream.
- **Error envelope:** `{"error": {"message", "type", "code", "param"}}` + request ID. Taxonomy with retryability: `invalid_request`, `authentication`, `permission`, `not_found`, `rate_limited` (429 + `Retry-After`), `overloaded` (503 + `Retry-After`), `upstream_error`, `upstream_timeout`, `canceled`, `internal`. Mid-stream failures are a standardized SSE error event followed by stream close — never a retry.
- **Request ID:** `X-Request-Id` accepted or generated; echoed in responses, error bodies, traces, and usage records; it is the idempotency key for usage settlement.
- **Cancellation contract:** client disconnect or connection close MUST propagate upstream (HTTP body close); observable effects (engine abort, resource release) are part of conformance; tokens emitted before cancellation are billable.

### 3.3 Contract 2 — Metrics & trace vocabulary — infergate EMITS

Canonical Prometheus set (units in name; declared histogram buckets): `inference_requests_total{model,backend,tenant_tier,status_class,error_class}` (counter); `inference_requests_in_flight{backend}` (gauge); `inference_queue_depth{tenant_tier}` (gauge); `inference_queue_wait_seconds{tenant_tier}` (histogram); `inference_ttft_seconds{model,backend}` (histogram); `inference_itl_seconds{model,backend}` (histogram); `inference_e2e_duration_seconds{model,backend,status_class}` (histogram); `inference_sheds_total{reason}` (counter); `inference_retries_total{stage}` (counter — `stage` is always pre-first-token); `inference_backend_healthy{backend}` (gauge); `inference_usage_tokens_total{direction,model,tenant_tier}` (counter).

- **Cardinality policy:** allowed labels are enumerable and low-cardinality only. **Forbidden as labels:** request IDs, raw tenant/user IDs, prompts, arbitrary strings. Per-request detail belongs in traces; exemplars link histograms to traces.
- **Trace attributes:** OTel GenAI semantic conventions at a pinned version (status "Development" as of 2026-07 — pin mandatory) + platform attributes `inference.config_version`, `inference.tenant_tier`, `inference.backend`, `inference.request_id`. Gateway span sequence: `recv → queue.wait → upstream.connect → ttft → stream.relay → settle`.
- **Measurement points (normative):** TTFT = first upstream body byte at the gateway (client-side TTFT is inferbench's separate named series); ITL = inter-chunk gap; queue wait = admission-enqueue to dispatch.

### 3.4 Contract 4 — Backend capability — infergate adapters DECLARE + PROBE

Fields: engine name + version/commit; streaming support; usage-in-stream support; cancellation mechanism (HTTP-close semantics) and expected release observability; metrics endpoint + **name mapping** (e.g. vLLM waiting/KV-usage gauges — names vary by version and must be mapped, never hardcoded); tokenizer identity; context limit; max concurrency hints; prefix-cache support + observability; quantization; priority support. infergate ships capability descriptors for mock, llama.cpp, and vLLM.

### 3.5 Contract 5 — Deployment — infergate PUBLISHES a descriptor per release

Fields: image + digest; ports (API, metrics); env vars and config mounts; startup/readiness/liveness semantics including warm-up-aware readiness; model mount path; resource requests/limits incl. GPU count; graceful termination (`preStop` drain hook; termination grace period > max stream duration); secret expectations. `inferops` deploys from this descriptor and the image alone.

### 3.6 Contract 6 — Fault scenarios — infergate implements the EXPECTED SEMANTICS

12 scenarios (injected by inferops at I7; infergate must behave as specified and have semantics tests): (1) backend killed pre-first-token → retry within budget or typed 5xx; (2) backend killed post-first-token → SSE error event, no retry, partial usage settled; (3) slow backend → pressure-aware routing shifts, timeouts typed; (4) slow client → bounded write buffer + write deadline, stream closed, engine released; (5) gateway termination during streaming → drain semantics, accepted streams complete; (6) queue saturation → sheds with 429 + `Retry-After`, accepted-request latency protected; (7) retry storm → retry budget caps amplification; (8) config reload during traffic → snapshot swap, zero dropped streams; (9) usage DB failure → requests unaffected, settlement backlog drains idempotently; (10) one unhealthy backend → routing shifts within bounded interval, circuit opens on error rate; (11) readiness during model warm-up → no traffic before warm, no restart loops; (12) rolling update with active requests → zero client-visible errors.

---

## 4. Architecture guidance

### 4.1 The gateway ↔ engine boundary (this repo's thesis — embed in `docs/architecture.md` and defend at every review)

| Concern | Owner | Never owned by |
|---|---|---|
| Admission (which tenant request enters), fairness, priority, quotas | infergate | engine |
| Health/pressure-aware routing across backends | infergate | engine |
| Streaming relay, cancellation propagation, retry budget, circuit breaking, shedding | infergate | engine |
| Continuous batching, per-token scheduling, chunked prefill | engine | infergate |
| KV-cache and prefix-cache internals, preemption | engine | infergate |
| GPU placement and memory management | engine (+ inferops at pod level) | infergate |

**The "full but not choking" principle:** the gateway keeps the engine full but not choking — per-backend in-flight limits keep engine backlog shallow, while requests are forwarded immediately when the engine has headroom (any added gateway delay when the engine is starved destroys batching efficiency). Pressure signals are read from engine metrics (e.g. vLLM `num_requests_waiting`, KV-cache usage — capability-mapped, names as of 2026-07), polled and normalized for routing; the gateway never re-derives engine internals. Prefix-affinity routing, if attempted, is a **labeled heuristic** (consistent hashing on prompt-prefix hash), never a claim of real KV awareness.

### 4.2 Request path & concurrency model

```text
client ──HTTP──▶ [validate → authenticate → resolve tenant → estimate tokens → quota check
        → per-tenant bounded queue → fairness dispatch (priority+WRR+aging)
        → route (health + pressure, least-inflight P2C, per-backend in-flight limit)
        → upstream HTTP/SSE relay] ──▶ engine (mock | llama.cpp | vLLM)
client ◀──SSE relay (per-event flush, bounded write buffer + write deadline)──
                    └─▶ async usage settle (PostgreSQL, idempotent by request ID)
```

- One goroutine tree per request, rooted in the request `context.Context`; every downstream action derives from it. **Bounded everything:** per-tenant admission queues, global and per-backend in-flight limits, per-stream write buffers with write deadlines. No unbounded queue or channel exists anywhere in the gateway.
- Data plane reads immutable config snapshots via atomic pointer swap; the control plane (admin API + PostgreSQL) builds and publishes snapshots (visible ≤5s). **No hot-path database reads.**
- PostgreSQL is durable state only: tenants, hashed API keys, models, quota policies, config versions, and the append-only usage ledger. Usage writes are asynchronous and batched; the request path never blocks on them.

### 4.3 Failure, cancellation, and retry semantics (normative)

- **Pre-first-token upstream 5xx** → retry within the retry budget, else typed 5xx (with `Retry-After` where applicable).
- **Post-first-token failure** → standardized SSE error event, close the stream, **NEVER retry** (tokens already emitted are sampled output and billable; a retry would duplicate output and double-bill).
- **Queue deadline exceeded / quota exhausted** → 429 + `Retry-After` + machine-readable reason.
- **All backends down / circuit open** → 503 + `Retry-After`. Circuit breaker opens on **pre-stream error rate only** (mid-stream failures never trip it).
- **Cancellation is a chain, not a flag** (verified in source research as of 2026-07 against vLLM V1 — re-verify at IG-T014): client disconnect → Go request-context cancel → upstream HTTP body close → `AsyncLLM.generate()` catches `asyncio.CancelledError` → `abort()` → scheduler `finish_requests(FINISHED_ABORTED)` → KV blocks freed. Cancellation is tested at **three points** — queued, dispatched-pre-first-token, mid-stream — and verified via engine metrics (mock counters, llama.cpp/vLLM metrics), never assumed.
- **Graceful drain:** readiness fails first, accepted streams complete within the drain deadline, new work is refused with typed errors.

### 4.4 Anti-patterns (reject in review; encode as tests where possible)

1. **Double-queuing** — any second scheduler/batcher in front of the engine's continuous batching.
2. **Broker on the hot path** — no Kafka/NATS/Redis between client and engine, ever.
3. **Unbounded queues anywhere** — including per-stream write buffers; slow clients get a bounded buffer + write deadline, then the stream is closed and the engine released (fault scenario 4).
4. **Swallowed client disconnects** — the most expensive naive-gateway bug: a disconnected client whose request keeps burning engine tokens. Context cancellation must reach the engine; prove it with metrics.
5. **Blind use of `httputil.ReverseProxy`** — hidden buffering breaks per-event flush and TTFT measurement; build the SSE relay deliberately (explicit flush, explicit copy loop, explicit deadlines).
6. **Fake KV-aware routing** — prefix affinity only as a labeled heuristic via consistent hashing on the prompt-prefix hash; never claim KV-cache awareness.

### 4.5 Numeric acceptance targets (source-derived as of 2026-07 — adopted from the program's source documents for this same gateway concept; re-baseline only via a recorded deviation if measurement proves a target infeasible)

| Target | Value |
|---|---|
| Non-queue gateway overhead | p95 < 10 ms, p99 < 20 ms |
| Cancellation propagation (gateway + mock path) | p95 < 250 ms |
| Usage settle variance | < 1%, and 100% idempotent by request ID |
| API-key revocation visibility | ≤ 5 s |
| Config snapshot publish | ≤ 5 s, without blocking in-flight streams |
| Overload (≈5× capacity, admission ON) | accepted-request TTFT p95 degrades ≤ 20% vs capacity-boundary baseline |
| Noisy neighbor (tenant A at 10× load) | tenant B p95 shift < 15% |
| Stream integrity | 100 concurrent streams, zero frame mixing |
| Post-first-token retries | zero, proven by automated test |

Model-level TTFT/ITL/goodput SLOs are declared **only after measurement**, never in advance.

---

## 5. Required documentation set (FIRST task: IG-T001)

Create `docs/` exactly as follows before any implementation:

```text
docs/
├── charter.md                # mission, depth-artifact positioning, independent + integration value, explicit "not a LiteLLM/Envoy-AI-GW/GAIE competitor" statement
├── architecture.md           # components, request path, concurrency model, snapshot/control-plane split, THE BOUNDARY TABLE + "full but not choking" principle
├── scope.md                  # owned capabilities (§1) and the required spec list below, each mapped to tasks
├── non-goals.md              # §1 "does NOT own" list + anti-patterns (§4.4) as named non-goals
├── interfaces.md             # Contract 1/2/4/5/6 summaries as implemented; admin API (repo-private); adapter interface
├── milestones.md             # §6 milestones with acceptance criteria (no calendar durations)
├── tasks.md                  # IG-T001…IG-T018 with full schema fields; status tracking
├── risks.md                  # §12 risks (R5, R14, R3-drift) + kill/reduction rules
├── testing.md                # §8.1 strategy: race-clean floor, 3-point cancellation, conformance fixtures, crash recovery
├── observability.md          # metric set, cardinality guard, span sequence, exemplars (per Contract 2)
├── security.md               # key hashing, constant-time compare, revocation ≤5s, secret handling, admin-surface exposure
├── experiments.md            # stale-health-snapshot experiment (IG-T017) + any hypothesis-driven work; GPU session rules
├── integration.md            # I2/I3/I4 criteria (§9), I5 hand-off via IG-T016, pinned contract bundle version
├── oss-opportunities.md      # §11 items and how evidence from this repo feeds them
├── implementation-notes.md   # running log + Deviations section (deviation policy, §13)
└── adr/                      # one ADR per: revocation consistency, tenant-config consistency, transaction boundaries, retry budget, why-the-gateway-must-not-batch, snapshot model, multi-gateway design
```

**Required specifications this session must write** (as sections of the docs above or standalone files under `docs/` — every one must exist and be reviewable): API/streaming, cancellation, tenant and key lifecycle, accounting, admission, fairness, routing, retries, circuit breaking, draining, configuration, usage settlement, observability, security, state ownership, failure model, multi-replica behavior, gateway-versus-engine boundary.

---

## 6. Repository milestones (dependency-ordered; NO calendar durations)

| # | Milestone | Tasks | Acceptance criteria |
|---|---|---|---|
| M0 | Docs & plan approved | IG-T001 | All 15 docs + adr/ exist with content; boundary section reviewed; plan approved by the user |
| M1 | Skeleton + mock + non-streaming path | IG-T002 | Contract fixtures pass against running gateway+mock pair; `go test -race` clean; mock TTFT/ITL/error-rate configurable and deterministic |
| M2 | Streaming & cancellation correctness (gate G2) | IG-T003 | 100 concurrent streams, zero frame mixing; 3-point cancellation with mock-side abort observed ≤100 ms; `[DONE]` + usage-in-stream conformant; acceptance tests green 10 consecutive runs, race clean |
| M3 | Config snapshots + drain | IG-T004 | Reload under traffic: zero dropped streams; publish ≤5 s; drain completes accepted streams; readiness flips correctly |
| M4 | First real engine (llama.cpp, CPU) | IG-T005 | 3-point cancellation verified against local `llama-server` (1–3B GGUF); capability descriptor validates; mock↔llama.cpp failover demonstrated → feeds I3 |
| M5 | Observability conformance | IG-T006 | Metric-name conformance test green; cardinality guard rejects forbidden labels; span sequence visible in a trace export |
| M6 | Multi-tenancy: auth, accounting, quotas | IG-T007, IG-T008, IG-T009 | Key revocation ≤5 s proven; zero hot-path DB reads (instrumented assert); settle variance <1%; DB-down test: requests unaffected; duplicate-delivery test: no double count; typed 429 + `Retry-After` |
| M7 | Admission & fairness (gate G5) | IG-T010, IG-T011 | At ≈5× capacity: accepted TTFT p95 degrades ≤20%; sheds typed; no starvation; noisy neighbor: tenant B p95 shift <15% |
| M8 | Routing & reliability | IG-T012, IG-T013 | Unhealthy-backend shift within bounded interval; automated proof of zero post-first-token retries; breaker open/half-open tests green |
| M9 | vLLM adapter (GPU gate G6) | IG-T014 | Cancellation verified via engine metrics (KV usage / running count drop within bound); metric mapping re-verified via `/metrics`; session auto-stopped → feeds I4 |
| M10 | Release for operations | IG-T016 | Image (digest) + deployment descriptor + capability descriptors + mock image released; inferops consumes without source checkout → unblocks I5 |
| M11 | Depth & study artifacts | IG-T015, IG-T017, IG-T018 | ADRs approved; stale-health experiment report published; crash-recovery test green in CI |

---

## 7. Task seeds (stable IDs — use EXACTLY these)

Schema per task: Goal · Repo · Requirement/Hypothesis · Dependencies · Expected files · Complexity (S/M/L) · Critical path (CP) · Parallel-safe (Par) · Review focus · Verification · Evidence · Integration impact · Required/Stretch · Stop condition.

**IG-T001 — Planning docs bootstrap.** Goal: create the full `docs/` set of §5. Repo: infergate. Requirement: all 15 docs + `adr/` with real content, including the boundary table, the required-spec list, and this task register. Deps: this prompt + contracts v0.1 draft. Files: `docs/*`, `docs/adr/`. Complexity: M. CP: yes. Par: no. Review: gateway-vs-engine boundary section. Verification: checklist against §5 of this prompt. Evidence: committed docs. Integration impact: none directly; gates everything. Required. Stop: all 15 docs exist with content and the plan is reviewed.

**IG-T002 — Gateway skeleton + mock backend + non-streaming path.** Goal: minimal conformant gateway and the program's only mock engine. Repo: infergate. Requirement: HTTP server; `/v1/chat/completions` (non-stream), `/v1/models`, `/healthz`, `/readyz`, `/metrics` stubs; request-ID accept/generate/echo; unsupported-field rejection; deterministic mock backend as a **separate binary** (`cmd/mock-backend`) with configurable TTFT, ITL, and error rate. Deps: contracts Inference API released (SC-T002). Files: `cmd/gateway/`, `cmd/mock-backend/`, `internal/...`, CI config. Complexity: M. CP: yes. Par: no. Review: mock determinism; contract conformance; rejection-not-ignore. Verification: contract fixtures pass against the running pair; `go test -race ./...`. Evidence: CI run output. Integration impact: I2 prerequisite; mock image later consumed by inferbench CI and inferops smoke tests. Required. Stop: fixtures green.

**IG-T003 — SSE relay + cancellation.** Goal: the correctness spine. Repo: infergate. Requirement: per-event flush; `[DONE]` terminator; usage-in-stream (`stream_options.include_usage`); monotonic chunk indices; no cross-request interleaving; 3-point cancellation (queued / dispatched-pre-first-token / mid-stream) with bounded release time; 100 concurrent streams without frame mixing; bounded per-stream write buffer + write deadline (slow-client handling); no `httputil.ReverseProxy` on the streaming path. Deps: IG-T002. Files: `internal/stream/`, cancellation + concurrency tests. Complexity: L. CP: yes. Par: no. Review: cancellation chain design; buffer bounds; flush behavior. Verification: automated concurrency + cancellation tests, race clean; mock-side abort observed ≤100 ms. Evidence: test output archived. Integration impact: everything downstream; G2 gate; I2 acceptance. Required. Stop: acceptance tests green 10 consecutive runs.

**IG-T004 — Config snapshots + graceful drain.** Goal: immutable-config data plane + clean shutdown. Repo: infergate. Requirement: immutable versioned snapshot; atomic pointer swap; publish visible ≤5 s; drain completes accepted streams within deadline; readiness flips before refusal; no stream blocked by a swap. Deps: IG-T002. Files: `internal/config/`, drain logic, reload-under-traffic test. Complexity: M. CP: no. Par: yes. Review: snapshot/transaction boundary (maps to the CMU-track snapshot-model artifact). Verification: reload-under-traffic test with zero dropped streams. Evidence: test output. Integration impact: fault scenarios 5 and 8. Required. Stop: tests green.

**IG-T005 — llama.cpp adapter.** Goal: first real engine, CPU-only. Repo: infergate. Requirement: adapter behind the unified backend interface; capability descriptor (Contract 4); mock↔llama.cpp failover; CPU-only against `llama-server` with a 1–3B GGUF model; note slot-model differences vs vLLM (study artifact input). Deps: IG-T003; capability schema (SC-T004). Files: `internal/backend/llamacpp/`, `examples/capabilities/llamacpp.json`-equivalent descriptor, tests. Complexity: M. CP: yes. Par: no. Review: slot-model differences documented; no engine internals leak into gateway logic. Verification: streaming + 3-point cancellation tests vs local `llama-server`. Evidence: test output + descriptor. Integration impact: I3 prerequisite. Required. Stop: 3-point cancellation verified on llama.cpp.

**IG-T006 — Observability per contract.** Goal: exact conformance with the metrics vocabulary. Repo: infergate. Requirement: OTel spans `recv → queue.wait → upstream.connect → ttft → stream.relay → settle`; Prometheus metrics exactly per §3.3; cardinality guard test (forbidden labels fail CI); exemplars. Deps: IG-T003; metrics vocabulary (SC-T005). Files: `internal/telemetry/`, conformance test. Complexity: M. CP: no. Par: yes. Review: no forbidden labels; measurement points match the normative definitions. Verification: metric-name conformance test; trace inspection. Evidence: scrape output + trace export. Integration impact: inferops dashboards depend on these exact names. Required. Stop: conformance test green.

**IG-T007 — Tenancy + auth + model registry.** Goal: multi-tenant control plane. Repo: infergate. Requirement: PostgreSQL schema (tenants, API keys **hashed** with constant-time compare, models, quota policies, config versions); key auth; tenant resolution; revocation visible ≤5 s via snapshot publish; zero hot-path DB reads. Deps: IG-T004. Files: migrations, `internal/tenant/`, `internal/auth/`, timing tests. Complexity: M. CP: no. Par: yes. Review: key lifecycle + revocation consistency (feeds the 6.5840 revocation ADR). Verification: revocation timing test; instrumentation assert proving no hot-path DB reads. Evidence: tests + migration files. Integration impact: all multi-tenant scenarios. Required. Stop: revoke ≤5 s proven.

**IG-T008 — Usage accounting (estimate → settle).** Goal: billable-token correctness. Repo: infergate. Requirement: token estimation; estimate-debit/settle-refund flow; asynchronous idempotent append-only writer (unique request ID); settle variance <1%; DB outage never fails requests (backlog drains idempotently); usage-settlement invariants doc with duplicate/reorder cases enumerated, each mapped to a test. Deps: IG-T007. Files: `internal/usage/`, ledger migration, invariants doc, tests. Complexity: M. CP: no. Par: yes. Review: invariants + ledger design (CMU-track artifact). Verification: variance test; DB-down test; duplicate-delivery test. Evidence: test output. Integration impact: fault scenario 9. Required. Stop: every invariant tested.

**IG-T009 — RPM/TPM quotas.** Goal: two-sided rate limiting. Repo: infergate. Requirement: per-tenant token buckets for requests/min and tokens/min; typed 429 + `Retry-After`; correct interaction with estimate-vs-settle (estimated tokens debit the TPM bucket; settlement corrects). Deps: IG-T008. Files: `internal/quota/`, tests. Complexity: S. CP: no. Par: yes. Review: estimate-vs-settle interaction. Verification: quota tests. Evidence: tests. Integration impact: fairness experiments build on this. Required. Stop: tests green.

**IG-T010 — Admission control.** Goal: bounded, sheddable ingress. Repo: infergate. Requirement: bounded per-tenant queues; queue deadlines; global in-flight budget; load shedding with typed errors + reason taxonomy; accepted work protected under saturation. Deps: IG-T003 (parallel-safe with T007–T009). Files: `internal/admission/`, saturation tests. Complexity: L. CP: yes. Par: no. Review: bound choices; shed reason taxonomy; early-rejection rationale (Mooncake-lineage note). Verification: saturation test — queue full → shed with 429 + `Retry-After`; accepted-request latency protected. Evidence: tests + metrics. Integration impact: gate G5; fault scenario 6; inferbench experiment set 1 (admission on/off). Required. Stop: overload behavior matches the spec.

**IG-T011 — Fairness + starvation prevention.** Goal: multi-tenant isolation under contention. Repo: infergate. Requirement: priority tiers (2 tiers minimum), weighted round-robin, aging; noisy-neighbor protection — tenant A at 10× load shifts tenant B p95 <15%; no starvation of any admitted tenant. Deps: IG-T010. Files: `internal/admission/fairness*`, noisy-neighbor test. Complexity: M. CP: no. Par: yes. Review: fairness policy choice + aging parameters. Verification: noisy-neighbor test. Evidence: test output + graphs. Integration impact: overload evidence set. Required (breadth reducible: keep 2 tiers + fairness evidence). Stop: bounded-shift criterion met.

**IG-T012 — Routing (health + pressure).** Goal: engine-external routing signals. Repo: infergate. Requirement: health poller; engine pressure normalization from capability-mapped metrics (never hardcoded names); least-inflight power-of-two-choices; per-backend in-flight limits ("full but not choking"). Deps: IG-T005; capability schema. Files: `internal/route/`, routing tests. Complexity: M. CP: yes. Par: no. Review: signals stay engine-external; no fake KV-awareness (prefix affinity only as a labeled consistent-hash heuristic if attempted). Verification: unhealthy-backend routing test — shift within a bounded, stated interval. Evidence: tests. Integration impact: fault scenarios 3 and 10. Required. Stop: tests green.

**IG-T013 — Reliability: retries, circuit breaker, timeouts.** Goal: bounded failure amplification. Repo: infergate. Requirement: retry budget; **pre-first-token-only retry invariant, tested**; circuit breaker opening on pre-stream error rate only; explicit timeout hierarchy (connect / TTFT / idle-stream / total). Deps: IG-T012. Files: `internal/reliability/`, invariant tests, retry-budget ADR. Complexity: M. CP: yes. Par: no. Review: retry-budget ADR (Google-SRE "Handling Overload" lens). Verification: automated proof of zero post-first-token retries; breaker open/half-open tests. Evidence: tests. Integration impact: fault scenarios 1 and 7. Required. Stop: invariant test green.

**IG-T014 — vLLM adapter (GPU gate G6).** Goal: real-GPU engine verification. Repo: infergate. Requirement: vLLM adapter + metric-name mapping verified via `curl /metrics` at session start (names drift; capability-mapped, as of 2026-07 pin v0.24.x); priority mapping; cancellation verified via engine metrics — KV-cache usage / running-request count drop within a bounded interval after client disconnect. GPU session requires written hypothesis + full config manifest + auto-stop script + budget alert BEFORE starting. Deps: IG-T013 + G6 approval. Files: `internal/backend/vllm/`, capability descriptor, session manifest + log. Complexity: M. CP: yes. Par: no. Review: session plan + hypothesis (pre-GPU, user-reviewed). Verification: streaming + 3-point cancellation tests on the rented GPU; recorded engine metrics. Evidence: session log + metrics exports. Integration impact: I4 prerequisite. Required. Stop: cancellation release proven; session auto-stopped. CPU fallback: llama.cpp becomes the measured baseline with a recorded deviation.

**IG-T015 — Consistency ADRs + multi-gateway design.** Goal: distributed-systems depth artifacts. Repo: infergate. Requirement: (a) API-key revocation consistency ADR — staleness bounds of snapshot-based revocation, at-most-once admin semantics; (b) tenant-config consistency ADR — snapshot propagation vs read-your-writes for admins, with a testable consistency statement; (c) multi-gateway (N-replica) scaling design note — state partitioning, quota semantics across replicas, what breaks at N>1 and the chosen trade-offs (design note only; no implementation). Deps: IG-T007; MIT 6.5840 selected-topic inputs. Files: `docs/adr/*`, design note. Complexity: M. CP: no. Par: yes. Review: consistency reasoning. Verification: ADR review by the user. Evidence: approved ADRs. Integration impact: portfolio depth; inferops multi-replica experiments. Required. Stop: ADRs approved.

**IG-T016 — Release: image + deployment descriptor + conformance fixtures.** Goal: the hand-off artifact for inferops. Repo: infergate. Requirement: versioned gateway image (digest + SemVer tag); deployment-contract descriptor (Contract 5, incl. warm-up-aware readiness and `preStop` drain, termination grace > max stream duration); capability descriptors; released mock-backend image. Deps: IG-T006 + current milestone scope. Files: release workflow, descriptor, release notes. Complexity: S. CP: yes. Par: no. Review: descriptor completeness vs Contract 5. Verification: fixture validation; container starts healthy from the released image alone. Evidence: release artifacts. Integration impact: unblocks inferops IO-T002 and milestone I5. Required. Stop: inferops consumes without source checkout.

**IG-T017 — Stale-health-snapshot experiment + fault-state machine.** Goal: quantify routing-signal staleness; formalize the request lifecycle. Repo: infergate. Requirement: (a) controlled experiment quantifying the impact of stale health/pressure snapshots on routing decisions, using mock-backend fault injection with a written hypothesis; (b) explicit request fault-state machine document covering the full error taxonomy including all failure/cancel edges, aligned with tests. Deps: IG-T012. Files: `docs/experiments.md` entry + report, fault-state-machine diagram + test mapping. Complexity: M. CP: no. Par: yes. Review: experiment design. Verification: controlled experiment executed with mock fault injection; state machine cross-checked against the error taxonomy tests. Evidence: experiment report. Integration impact: study track (6.5840); routing tuning. Required. Stop: report published; diagram and tests aligned.

**IG-T018 — Crash-recovery integration test + transaction-boundary ADR.** Goal: durability depth artifact. Repo: infergate. Requirement: scripted test that kills the gateway mid-traffic and verifies idempotent usage recovery (no double count), snapshot reload, and clean restart; ADR stating what is and is not transactional between snapshot store, ledger, and quota state; idempotent-recovery design with recovery cases enumerated. Deps: IG-T008, IG-T004. Files: crash-test script + CI wiring, `docs/adr/transaction-boundaries.md`. Complexity: M. CP: no. Par: yes. Review: recovery invariants. Verification: scripted crash test green (repeatably, in CI). Evidence: test output + ADR. Integration impact: study track (15-445); depth for fault scenarios 5 and 9. Required. Stop: recovery test green.

---

## 8. Testing, observability, security, performance hypotheses

### 8.1 Testing
- Floor: `go test -race ./...` clean on every commit touching concurrency.
- Contract conformance: golden fixtures from the pinned `serving-contracts` bundle run in CI (streaming, non-streaming, every error class, unsupported-field rejection).
- Cancellation: 3-point tests (queued / pre-first-token / mid-stream) on mock, llama.cpp, and vLLM; release verified via engine metrics, never assumed.
- Concurrency: 100-concurrent-stream frame-integrity test; slow-client (bounded read rate) test proving buffer bound + write deadline + engine release.
- Invariant tests: zero post-first-token retries (automated proof); usage idempotency under duplicate delivery and reorder; reload-under-traffic zero dropped streams; crash-recovery (IG-T018).
- Boundary tests: the three contract tests from the vLLM source-reading artifact (§10) that fail if batching/scheduling/KV logic appears in the gateway.
- Fault-semantics tests: one per Contract 6 scenario where the gateway is the subject (1, 2, 4, 5, 6, 7, 8, 9, 10).

### 8.2 Observability
Exactly the Contract 2 metric set (§3.3) — no more labels, no fewer metrics; cardinality guard in CI; span sequence `recv → queue.wait → upstream.connect → ttft → stream.relay → settle`; exemplars linking histograms to traces; OTel GenAI semconv version pinned (status "Development" as of 2026-07 — re-verify at use time).

### 8.3 Security
Hashed API keys (never plaintext at rest), constant-time comparison; revocation ≤5 s via snapshot publish; admin API repo-private and never exposed on the data-plane port without auth; secrets via environment/mounts per the deployment contract; no tenant/user identifiers or prompts in metric labels or logs at default level.

### 8.4 Performance hypotheses (each becomes a measured claim or is dropped)
- H1: Non-queue gateway overhead p95 <10 ms / p99 <20 ms vs direct-to-mock and direct-to-llama.cpp (measured by inferbench experiment set 1; the gateway must not editorialize its own numbers).
- H2: Cancellation propagation p95 <250 ms on the gateway+mock path.
- H3: At ≈5× capacity, admission ON protects accepted-request TTFT p95 to ≤20% degradation while shedding typed 429s (vs collapse with admission OFF).
- H4: Tenant A at 10× load shifts tenant B p95 <15% under priority+WRR+aging.
- H5 (IG-T017): stale health/pressure snapshots degrade routing quality measurably as staleness grows; quantify the staleness bound at which misrouting exceeds a stated threshold.
All numeric targets are source-derived as of 2026-07; provenance and dates go on every published number.

---

## 9. Integration milestones this repo participates in

**I2 — Local request path** (owner: inference-lab; infergate prerequisites: IG-T003). Acceptance: `inferbench → infergate → mock backend` runs a seeded workload with 100 concurrent streams, zero frame mixing; 3-point cancellation verified (mock abort observed within bound); raw events schema-valid; client-vs-gateway TTFT agreement within declared tolerance; traces/metrics visible; Scenario A includes the PostgreSQL usage write + OTel. Failure handling: frame mixing or cancellation leak → stop, fix in infergate, re-run.

**I3 — Local inference** (infergate prerequisite: IG-T005). Acceptance: `inferbench → infergate → llama.cpp` completes `chat-short` and `shared-prefix` workloads on CPU; first schema-valid benchmark report generated (manifest + validity block); cancellation verified against llama.cpp; mock↔llama.cpp failover demonstrated. Behavioral surprises → capability descriptor updated, adapter fixed.

**I4 — GPU inference** (infergate prerequisite: IG-T014 behind gate G6). Acceptance: `inferbench → infergate → vLLM` on a rented GPU; streaming + cancellation verified via engine metrics (KV usage / running-count drop within bound); gateway-overhead comparison (direct vs via-gateway) measured with ≥3 runs/point; session auto-stopped; all artifacts carry the full manifest. Metric-name drift → update capability mapping, re-verify. CPU fallback: documented deviation, llama.cpp becomes the measured baseline.

**I5 — Operational stack** (owner: inferops). infergate's contribution is **IG-T016**: released image (digest) + deployment descriptor + capability descriptors + mock image, consumable by inferops **without any source checkout**. I5 additionally requires warm-up-aware readiness and drain semantics to hold in-cluster (rolling update under load, zero client-visible errors) — these behaviors are built in IG-T004/IG-T016 and verified by inferops.

---

## 10. Study-track artifacts owned by this repo (artifact-or-drop; a resource with no artifact after two sessions is dropped)

**MIT 6.5840-derived (selected topics: RPC semantics, at-most-once, linearizability, fault tolerance, cache consistency, invariant reasoning) — six artifacts:**
1. API-key revocation consistency ADR (staleness bounds of snapshot-based revocation; at-most-once admin semantics) → IG-T015; stop: ADR approved.
2. Tenant-config consistency ADR (snapshot propagation vs read-your-writes for admins; must produce a testable consistency statement) → IG-T015; stop: ADR approved.
3. Usage-settlement invariants (exactly-once *effect* via idempotent settle; duplicate/reorder cases enumerated, each mapped to a test) → IG-T008; stop: invariants tested.
4. Multi-gateway scaling design note (state partitioning, quota semantics across replicas; states what breaks at N>1) → IG-T015; stop: note reviewed.
5. Stale-health-snapshot experiment (hypothesis + controlled experiment quantifying routing impact) → IG-T017; stop: report published.
6. Fault-state machine (request lifecycle incl. all failure/cancel edges; covers the full error taxonomy) → IG-T017; stop: diagram + tests aligned.

**CMU 15-445-derived (selected topics: concurrency control, MVCC, logging, crash recovery) — five artifacts:**
1. Versioned configuration-snapshot model (MVCC-flavored snapshot semantics doc) → IG-T004; stop: doc merged with ADR.
2. Append-only usage ledger design (write path + compaction/retention stated) → IG-T008; stop: design implemented.
3. Idempotent recovery design (recovery cases enumerated) → IG-T018; stop: design tested.
4. Crash-recovery integration test (kills the gateway mid-traffic) → IG-T018; stop: test green in CI.
5. Transaction-boundary ADR (what is/isn't transactional between snapshot store, ledger, quota state) → IG-T018; stop: ADR approved.

**vLLM source-reading artifact** (path-pinned as of 2026-07 — `vllm/v1/engine/async_llm.py`, `core.py`, `vllm/v1/core/sched/scheduler.py`, `kv_cache_manager.py`, entrypoints; run `git log -- <path>` before reading, paths drift): a "Life of a streaming request in vLLM V1" **sequence diagram** + a 2-page **`Scheduler.schedule()` annotation** + **THREE contract tests that prevent gateway batching logic** from ever being introduced (the boundary tests of §8.1). Stop: diagram + tests exist. Follow one HTTP request's execution path; pin the commit.

---

## 11. OSS opportunities fed by this repo (activity logged in `inference-lab`; nothing posted without user review)

- **"infergate router vs GAIE EPP" comparison** — a routing-signal design review comparing infergate's health/pressure/least-inflight-P2C approach against the Gateway API Inference Extension EPP scorers (queue depth, KV utilization, prefix/LoRA affinity). Feeds the GAIE/llm-d track (the program's primary OSS target — caveat as of 2026-07: GAIE repo migration toward llm-d, `InferenceModel`→`InferenceObjective` rename, must be re-verified live before committing effort).
- **Metric-mapping drift discoveries** — any vLLM metric-name or documentation drift found during IG-T014's `/metrics` verification becomes a candidate vLLM docs/metrics fix (the program's OSS fallback target), grounded in recorded evidence with full manifests.

---

## 12. Risks and kill criteria for this repo

| ID | Risk | Trigger | Mitigation |
|---|---|---|---|
| R5 | **Gateway/engine boundary erosion** (batching/KV logic creeping into infergate) — likelihood M, impact H | Boundary tests fail; review finds scheduling logic in the gateway | **Hard review rule:** any change containing an engine-scheduling concept (batch formation, token budgets, KV state) is rejected outright; the three boundary contract tests (§10) run in CI |
| R14 | **Mock backend fidelity gap** (correctness evidence doesn't transfer to real engines) — L/M: M/M | I3/I4 reveal behaviors the mock never modeled | Mock gains fidelity features **only** when a real-engine surprise justifies them; llama.cpp lands early (IG-T005) precisely to bound this |
| R3 | Engine/ecosystem drift (vLLM metric names, semconv changes) — H/M | Conformance or mapping tests fail on a new pin | Pin everything; capability metric-name mapping instead of hardcoding; re-verify at IG-T014 |

**Reducible scope (pre-decided, never cut below):** multi-tenant policy breadth reduces to **2 priority tiers + fairness evidence** (the noisy-neighbor bound must still be demonstrated). **Never cut:** cancellation correctness, streaming integrity, contract validation, the zero-post-first-token-retry invariant. Generic drop rule: drop any work item that blocks progress without producing new evidence, duplicates a capability, lacks a measurable artifact, or creates tight source coupling.

---

## 13. Definition of Done for `infergate`

The repo is accepted when, with linked evidence:
1. **Independent-mode demo** runs GPU-free: gateway + mock backend + local PostgreSQL, demonstrable to a stranger.
2. **Correctness evidence set green:** 100-concurrent-stream integrity; 3-point cancellation verified on mock, llama.cpp, and vLLM (engine-metrics-verified); automated proof of zero post-first-token retries; crash-recovery test green; config reload under traffic with zero dropped streams.
3. **Overload evidence set green:** at ≈5× capacity with admission control, accepted-request TTFT p95 degrades ≤20%; sheds typed with `Retry-After`; no tenant starvation; noisy-neighbor p95 shift <15%.
4. **SLO evidence set green (source-derived targets, §4.5):** overhead p95 <10 ms / p99 <20 ms; cancellation propagation p95 <250 ms (gateway+mock); settle variance <1% and 100% idempotent; key revocation ≤5 s; config publish ≤5 s. Model-level SLOs declared only from measurement.
5. **Released image + descriptors consumed by inferops without source checkout** (IG-T016 → I5).
6. All study-track artifacts of §10 delivered; ADRs approved; docs current.

---

## 14. Deviation policy

> Keep `docs/implementation-notes.md`. When repository evidence forces a deviation from the approved plan, choose the conservative reversible option, record the evidence, decision, consequences, and follow-up under `Deviations`, and continue. Pause only when the deviation changes public contracts, repository ownership, security posture, or milestone scope.

---

## 15. Session operating instructions

1. **First task is IG-T001:** create the complete `docs/` set of §5 (including the required-specification list), then get the plan reviewed by the user before writing implementation code.
2. Implement strictly in task dependency order (§7); tasks marked Par:yes may proceed in parallel once their dependencies are met. Never reorder past a failing verification gate.
3. Run each task's verification command/procedure, capture the output, and link it from `docs/implementation-notes.md` (cross-repo evidence is archived by `inference-lab`, not here).
4. Commit with clear messages, one logical change per commit. **Never push to any other repository.** Never check out or modify another repo's source to "make integration work" — fix the contract or file the issue instead.
5. Claims discipline: if a test failed, say so; if a step was skipped, say so; no "should work". Numbers carry provenance and dates; re-verify all "as of 2026-07" facts at use time.
6. Record everything notable — decisions, surprises, deviations, dropped items — in `docs/implementation-notes.md` as you go.
