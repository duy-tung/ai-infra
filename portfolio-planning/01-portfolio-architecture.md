# 01 — Portfolio Architecture

This document defines the system-level architecture of the composed platform, the boundaries between repositories, and the design rationale. Per-repository detail lives in the standalone prompts under `prompts/`.

---

## 1. Composed system overview

```text
                              ┌────────────────────────────────────────────┐
                              │              serving-contracts             │
                              │  OpenAPI subset · JSON Schemas · metrics   │
                              │  vocabulary · compatibility policy         │
                              └───────┬───────────┬───────────┬────────────┘
                    validates against │           │           │ validates against
                                      │           │           │
   ┌───────────┐   HTTP/SSE   ┌───────▼─────┐  HTTP/SSE  ┌────▼──────────┐
   │ inferbench│─────────────▶│  infergate  │───────────▶│ engines        │
   │ loadgen + │              │  (Go)       │            │ mock (in       │
   │ analysis  │              │ admission · │            │  infergate) ·  │
   └─────┬─────┘              │ routing ·   │            │ llama.cpp ·    │
         │ result files       │ streaming · │            │ vLLM           │
         │ (versioned         │ quotas ·    │            └───────────────┘
         │  schemas)          │ cancellation│                 ▲
         ▼                    └──────┬──────┘                 │ deploys
   ┌───────────┐                     │ usage (async)          │
   │ fleetlab  │              ┌──────▼──────┐          ┌──────┴────────┐
   │ capacity/ │              │ PostgreSQL  │          │   inferops    │
   │ autoscale │              │ (tenants,   │          │ K8s · OTel ·  │
   │ simulation│              │  usage)     │          │ Prometheus ·  │
   └─────┬─────┘              └─────────────┘          │ Grafana·Tempo │
         │ deployment                                  │ chaos·runbooks│
         │ recommendations                             └──────┬────────┘
         ▼                                                    │
   ┌──────────────────────────────────────────────────────────▼─────────┐
   │                          inference-lab                             │
   │  version pins · quickstart · scenarios A–E · reports · ADRs ·      │
   │  postmortems · portfolio narrative · OSS log                       │
   └────────────────────────────────────────────────────────────────────┘
```

Data-flow (integration) edges — each is a file, artifact, or network protocol, never a source import:

- `serving-contracts` → all others: released, versioned schema/spec bundles.
- `inferbench` → any OpenAI-compatible endpoint (engine direct, or `infergate` in front): network only.
- `inferbench` → `fleetlab`: benchmark-result and raw-event files conforming to the benchmark schemas.
- `infergate` → `inferops`: released container images plus the deployment contract.
- `fleetlab` → `inferops`: deployment recommendation documents (machine-readable + human report).
- everything → `inference-lab`: released artifacts, result files, reports.

## 2. The synchronous request path (the correctness spine)

```text
client ──HTTP──▶ infergate ──HTTP──▶ engine (mock | llama.cpp | vLLM)
        ◀──SSE──          ◀──SSE──
```

Rules that define the path:

1. **No broker on the path.** Kafka/NATS/Redis Streams never sit between client and engine: hidden buffering breaks direct cancellation and adds a second queue in front of the engine's continuous batching (the "double-queuing" anti-pattern, verified against vLLM V1 scheduler design in the source research).
2. **Bounded everything.** Per-tenant admission queues, global and per-backend in-flight limits, per-stream write buffers with write deadlines. No unbounded queue exists anywhere in the gateway.
3. **Cancellation is a chain, not a flag.** Client disconnect → Go request-context cancel → upstream HTTP body close → engine abort (vLLM V1: `AsyncLLM.generate()` catches `asyncio.CancelledError` → `abort()` → scheduler `finish_requests(FINISHED_ABORTED)` → KV blocks freed; verified in source research). Cancellation is tested at three points: queued, dispatched-pre-first-token, mid-stream — and verified via engine metrics, never assumed.
4. **Retry only before the first token.** After the first streamed token, a retry would duplicate sampled output and double-bill; failures become a standardized SSE error event.
5. **Usage accounting is estimate → settle**, asynchronous, idempotent by request ID, and never on the hot path. PostgreSQL is durable state only; the data plane reads immutable config snapshots swapped atomically.

## 3. The gateway ↔ engine boundary (the thesis)

| Concern | Owner | Never owned by |
|---|---|---|
| Admission (which tenant request enters), fairness, priority, quotas | infergate | engine |
| Health/pressure-aware routing across backends | infergate | engine |
| Streaming relay, cancellation propagation, retry budget, circuit breaking, shedding | infergate | engine |
| Continuous batching, per-token scheduling, chunked prefill | engine | infergate |
| KV-cache and prefix-cache internals, preemption | engine | infergate |
| GPU placement and memory management | engine (+ inferops at pod level) | infergate |

The gateway keeps the engine "full but not choking": per-backend in-flight limits keep engine backlog shallow, while forwarding immediately when the engine has headroom (any added gateway delay when the engine is starved destroys batching efficiency). Pressure signals are read from engine metrics (e.g. vLLM `num_requests_waiting`, KV-cache usage) — polled, normalized, and used for routing; the gateway never re-derives engine internals. Prefix-affinity routing, if attempted, is a labeled heuristic (consistent hashing on prompt-prefix hash), never a claim of real KV awareness.

## 4. Repository boundary rationale

Each boundary was tested against: independent value, coupling, and maintenance cost. The source documents chose a single repository under a 480-hour calendar cap; this program removes that cap and mandates composability. The boundary test results:

| Repository | Independent value (works alone) | Coupling risk | Verdict |
|---|---|---|---|
| serving-contracts | Any OpenAI-compatible project can adopt the schemas/metric vocabulary | Low — pure specs | Separate |
| infergate | Gateway + mock backend + local PostgreSQL is a complete, GPU-free, useful system | Medium — must not absorb benchmarking or deployment | Separate |
| inferbench | Benchmarks any OpenAI-compatible endpoint, with or without the gateway | Low — network-only targets | Separate |
| fleetlab | Consumes any schema-conformant result files; useful for capacity questions generally | Low — file-based input | Separate |
| inferops | Deploys released images; useful as a reference inference-ops stack | Medium — must not require component source checkouts | Separate |
| inference-lab | Quickstart + evidence + narrative has standalone reader value | Low — orchestrates releases | Separate |

Consolidation triggers (any of these forces a user-review decision, see `10-risk-register.md` §K): a repo loses independent value; two repos require lockstep source changes across more than two consecutive milestones; shared internal code becomes the only workable integration mechanism; maintenance cost demonstrably exceeds learning value.

## 5. Technology decisions

| Area | Decision | Basis |
|---|---|---|
| Gateway language | Go | Existing strength; ecosystem fit (GAIE EPP, llm-d, AIBrix, Envoy AI Gateway control planes are Go — source-reported, as of 2026-07) |
| Load generator | Go (open-loop, Poisson, seeded) | Correct latency measurement requires open-loop; Go concurrency strength |
| Analysis | Python (pandas/matplotlib or equivalent) | Deliberate Python-deepening goal; standard analysis stack |
| Simulation | Python (`fleetlab`) | Numeric/statistical tooling; second Python artifact |
| Engines | mock → llama.cpp (`llama-server`, CPU, 1–3B GGUF) → vLLM (V1, pinned minor version; 7–8B AWQ/GPTQ on 24 GB GPU) → SGLang (comparison-only stretch) | Risk-ordered: protocol/cancellation correctness first, GPU cost last; source-verified ordering |
| Metadata store | PostgreSQL | Existing strength; tenants/keys/quotas/usage/config versions/benchmark manifests |
| Observability | OpenTelemetry SDK + Collector, Prometheus, Grafana, Tempo; OTel GenAI semantic conventions (version pinned — status "Development" as of 2026-07) | Existing OTel strength; program requirement |
| Kubernetes | kind/k3s locally + one GPU-node profile; smallest justified tooling set (decided in `inferops` planning: default Kustomize + raw manifests; Helm only if templating need is proven; no Argo CD/Terraform in baseline) | "Deploy after behavior is proven"; avoid YAML-exercise trap |
| Engine pins | vLLM v0.24.x (V1 architecture); llama.cpp/SGLang pinned by commit at execution time | Source-verified as of 2026-07; re-verify at execution (`curl /metrics` for metric-name drift) |

## 6. State ownership

| State | Owner | Consumers | Mechanism |
|---|---|---|---|
| Contract versions | serving-contracts | all | git tags + released bundles |
| Tenants, API keys, quotas, model registry, config versions | infergate (PostgreSQL) | infergate only | control plane publishes immutable snapshots; data plane atomic-swaps |
| Usage ledger | infergate (PostgreSQL, append-only, idempotent by request ID) | infergate; exported reports to inference-lab | async batched writer |
| Raw benchmark events + run manifests | inferbench (files) | inferbench analysis, fleetlab, inference-lab | JSONL + JSON conforming to schemas |
| Hardware/model/cost/SLO profiles | fleetlab (files, with provenance fields) | fleetlab, inference-lab | versioned YAML/JSON conforming to schemas |
| Cluster manifests, dashboards, runbooks, fault scenarios | inferops | inferops, inference-lab | git + released config bundles |
| Version-pin matrix, scenario evidence, OSS log | inference-lab | user, reviewers | markdown + machine-readable pins file |

## 7. Failure-semantics overview (platform level)

Standardized in `serving-contracts` (error envelope + taxonomy), implemented in `infergate`, injected and observed by `inferops`, measured by `inferbench`:

- Pre-first-token upstream failure → retry within retry budget, else typed 5xx with `Retry-After` where applicable.
- Post-first-token failure → standardized SSE error event, stream closed, tokens emitted so far counted for usage; never retried.
- Queue deadline exceeded / quota exhausted → 429 + reason code + `Retry-After`.
- All backends unhealthy / circuit open → 503 + `Retry-After`.
- Backend health transitions → routing shifts within a bounded interval; circuit breaker opens on pre-stream error rate only.
- Gateway drain → readiness fails, accepted streams complete within the drain deadline, new work is refused.

The 12 required fault scenarios and their expected semantics are contract-listed in `04-shared-contracts.md` §6 and executed by `inferops` (milestone I7).

## 8. Integration scenarios (proved in `inference-lab`)

```text
A. infergate → mock backend → PostgreSQL → OTel            (correctness spine, GPU-free)
B. infergate → llama.cpp → inferbench                      (first real engine, CPU)
C. infergate → vLLM → inferbench → observability           (GPU path, measured)
D. inferops → infergate → vLLM → OTel/Prometheus/Grafana/Tempo   (operated on K8s)
E. inferbench results → fleetlab → deployment recommendation → inferops → repeated benchmark
```

Scenario E is the central integration story: measurements become capacity decisions, decisions become deployments, deployments are re-measured. Milestones I1–I8 (in `07-integration-milestones.md`) gate these scenarios.

## 9. Explicit non-goals (platform level)

No second gateway, load generator, or deployment stack. No generic distributed-systems project without inference relevance. No CUDA kernels. No full agent runtime (design note only, produced in the study track). No production multi-region (architecture note only). No semantic caching, guardrails product features, full eval platform, or LLM-as-judge in the baseline. No claim that `fleetlab` simulation equals production behavior.
