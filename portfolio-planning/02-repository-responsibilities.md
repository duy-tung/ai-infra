# 02 — Repository Responsibilities

Single-owner responsibility matrix. Every capability has exactly one owner. When two repositories need the same concept, the concept is extracted into a contract (owned by `serving-contracts`) or exchanged as a released artifact — never as a shared application library.

---

## 1. Top-level matrix

| Capability | Owner | Notes |
|---|---|---|
| Shared API, schemas, metric vocabulary, compatibility policy | `serving-contracts` | Specs only; validation tooling is the only permitted code |
| Admission, routing, streaming, cancellation, quotas, gateway reliability | `infergate` | The only gateway |
| Load generation, raw events, statistics, benchmark reports | `inferbench` | The only load-generation system |
| Capacity, autoscaling policy comparison, cost, placement simulation | `fleetlab` | Simulation and reports; not a production scheduler |
| Kubernetes, observability deployment, chaos, runbooks | `inferops` | The only deployment stack |
| Integration tests, evidence, demos, portfolio narrative | `inference-lab` | Orchestrates releases; no core runtime logic |
| OSS activity tracking | `inference-lab` | Log + evidence; contributions happen upstream |

## 2. Per-repository ownership

### serving-contracts — owns
- OpenAI-compatible request/response **subset** definition (which fields are supported, which are rejected).
- Streaming and non-streaming semantics: SSE framing, `[DONE]` terminator, usage-in-stream (`stream_options.include_usage`), error envelope, request-ID propagation, cancellation contract.
- Backend-capability schema; workload, benchmark-run, benchmark-result, raw-event schemas; hardware, model, SLO, cost, deployment, and fault-scenario schemas.
- Metric vocabulary, trace-attribute conventions, label/cardinality policy.
- Compatibility policy: SemVer rules, breaking-change definition, deprecation, migration notes, consumer-test fixtures.

### serving-contracts — does not own
Gateway logic, load generation, Kubernetes manifests, capacity models, databases, provider SDKs, generated service frameworks (schema-validation tooling only).

### infergate — owns
- OpenAI-compatible endpoint for the supported subset; SSE relay with upstream cancellation.
- Validation, tenant resolution, API-key authentication; model registry; immutable config snapshots + graceful drain.
- Token estimation and estimate-and-settle accounting; RPM/TPM quotas; asynchronous idempotent usage persistence (PostgreSQL).
- Bounded per-tenant queues, fairness (priority + weighted round-robin + aging), starvation prevention; global and per-backend in-flight limits.
- Health-aware and pressure-aware routing; pre-first-token-only retry with retry budget; circuit breaker; load shedding.
- OTel traces + low-cardinality Prometheus metrics per the contracts metric vocabulary.
- Deterministic mock backend (in-repo, `cmd/mock-backend`), llama.cpp adapter, vLLM adapter.

### infergate — does not own
Continuous batching, per-token scheduling, KV/prefix-cache internals, GPU placement, Kubernetes manifests (beyond a reference Dockerfile/compose for local dev), benchmark statistics, fleet simulation, brokers on the request path.

**Independent mode:** `infergate + mock backend + local PostgreSQL`. Development and CI are GPU-free.

### inferbench — owns
- Go load generator: open-loop and Poisson arrivals, fixed seeds, concurrent streams, cancellation and slow-client workloads, rate sweeps, replay, raw event capture.
- Python analysis: confidence intervals, pooled-percentile statistics, saturation-knee detection, goodput@SLO, cost per successful request / per 1M tokens, comparisons, graphs, reports.
- Workload suite: `chat-short`, `rag-long-in`, `gen-long-out`, `shared-prefix`, `mixed`, `bursty`, `cancel-storm`, `slow-client` (versioned, seeded).
- Controlled engine experiments (hypothesis-driven; parameters include `max_num_seqs`, `max_num_batched_tokens`, `gpu_memory_utilization`, context length, prefix caching, chunked prefill, quantization, KV-cache dtype; speculative decoding/MTP and KV offloading as stretch).
- Validity protections: coordinated-omission avoidance, warm-up exclusion, output-length control, version manifests, repeated runs, no mean-only or cherry-picked reporting.

### inferbench — does not own
The gateway, engines, Kubernetes, capacity modeling (it produces the result files `fleetlab` consumes), dashboards.

**Independent mode:** benchmarks any OpenAI-compatible endpoint over the network; works without `infergate`.

### fleetlab — owns
- Ingestion of versioned workload manifests, benchmark results, hardware/model/SLO/cost profiles (schema-conformant files).
- Arrival and length models; token-rate model; memory and goodput profiles; cold start, warm-up, and scaling-delay modeling; headroom and queue-growth analysis; failure-capacity analysis.
- Autoscaling-signal comparison: CPU utilization, GPU utilization, queue depth, in-flight requests, token-arrival rate, predicted-goodput deficit.
- Heterogeneous placement: GPU memory/throughput differences, cost, model fit, cold starts, failover headroom, fragmentation, workload affinity.
- Reports: autoscaling policy comparison, cold-start headroom, heterogeneous placement, cost/capacity model, simulation limitations.

### fleetlab — does not own
Provisioning, Kubernetes controllers, a global scheduler, multi-region consensus, live migration, universal hardware abstraction, benchmark implementation, or any claim that simulation equals production.

**Independent mode:** runs entirely from files; no GPU, no cluster, no gateway required.

### inferops — owns
- Local Kubernetes (kind/k3s) and a GPU-node profile; deployments for infergate, vLLM, llama.cpp, dev PostgreSQL.
- OTel Collector, Prometheus, Grafana, Tempo deployment; dashboards as code.
- Startup/readiness/liveness semantics including warm-up-aware readiness; graceful `preStop`; rolling updates; disruption behavior; resources; GPU device plugin; config rollout; secret strategy.
- Failure injection and chaos experiments (the 12 required fault scenarios); operational runbooks (deploy, upgrade, rollback, drain, backend failure, performance regression, config rollback, capacity shortfall, observability outage, database outage).
- Autoscaling **experiments** (HPA, justified KEDA; signals: queue depth, in-flight, token-arrival rate). Capacity **logic** stays in `fleetlab`.

### inferops — does not own
Gateway/engine/benchmark source (deploys released images only — never checks out component source), capacity math, benchmark analysis.

**Independent mode:** a reference Kubernetes inference-ops stack deployable with released public images.

### inference-lab — owns
- Version-pin matrix (machine-readable), local quickstart, end-to-end orchestration of scenarios A–E, demo scenarios and scripts.
- Reports, diagrams, ADR index, postmortems, compatibility matrices, portfolio landing page, articles, curriculum/study progress, OSS activity log.

### inference-lab — does not own
Any core runtime logic, any duplicated capability. It composes released artifacts.

## 3. Duplication guards

| Shared concept | Resolution |
|---|---|
| Request/response/SSE shapes needed by infergate, inferbench, inferops smoke tests | `serving-contracts` OpenAPI + examples; consumers validate against fixtures |
| TTFT/ITL/goodput definitions needed by infergate (metrics), inferbench (analysis), fleetlab (models) | `serving-contracts` metric vocabulary defines names, units, histogram buckets, and measurement points |
| Workload definitions needed by inferbench (generation) and fleetlab (arrival models) | `serving-contracts` workload schema; both consume the same versioned files |
| Fault scenarios needed by inferops (injection) and infergate (expected semantics tests) | `serving-contracts` fault-scenario schema enumerates the 12 scenarios and expected client-visible behavior |
| Deployment expectations needed by infergate (image) and inferops (manifests) | `serving-contracts` deployment contract (image/digest, ports, probes, env, model mount, resources, termination) |
| Mock backend needed by infergate CI and inferbench targets | Owned by infergate, consumed by others as a released image — not copied |

## 4. Boundary tests (used at every review gate)

1. Can this repository be demonstrated alone, to a stranger, with value? If no → consolidation trigger.
2. Does a change here force a same-day change in another repository's source? If yes twice in a row → contract gap; fix the contract, not the boundary.
3. Is any code copied between repositories? If yes → move the concept into a contract or a released artifact.
4. Does the gateway contain any engine-scheduling concept (batch formation, token budgets, KV state)? If yes → reject the change (hard rule).
