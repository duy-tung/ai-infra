# 04 — Shared Contracts

All contracts are owned by `serving-contracts`, versioned together as one bundle under SemVer, and released as git tags with downloadable artifacts. Consumers pin a bundle version. This document is the design-level definition; the exact schema files are produced by `serving-contracts` tasks (see `prompts/00-serving-contracts-plan.md`).

Planned artifact layout in the `serving-contracts` repository:

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

---

## Contract 1 — Inference API (OpenAI-compatible subset)

**Owner:** serving-contracts. **Consumers:** infergate (implements), inferbench (drives), inferops (smoke tests), inference-lab (demos).

- **Endpoints:** `POST /v1/chat/completions` (stream + non-stream), `GET /v1/models`, `GET /healthz`, `GET /readyz`, `GET /metrics`. Admin surface (`/admin/v1/...`) is defined by infergate and is explicitly *not* part of the shared contract (single consumer).
- **Supported subset:** explicitly enumerated request fields (`model`, `messages`, `max_tokens`/`max_completion_tokens`, `temperature`, `top_p`, `stream`, `stream_options.include_usage`, `stop`, `seed`, `user`); all unsupported fields are rejected with a typed error, never silently ignored. Response objects mirror the OpenAI chat-completion and chunk shapes for the supported subset.
- **Streaming semantics:** SSE with `data: <json-chunk>` events, terminal `data: [DONE]`; every event flushed; usage in the final chunk when `stream_options.include_usage=true`; per-event ordering guarantees (no interleaving across requests; monotonically increasing chunk indices per stream).
- **Error envelope:** `{"error": {"message", "type", "code", "param"}}` plus request ID. Error taxonomy with retryability: `invalid_request`, `authentication`, `permission`, `not_found`, `rate_limited` (429 + `Retry-After`), `overloaded` (503 + `Retry-After`), `upstream_error`, `upstream_timeout`, `canceled`, `internal`. Mid-stream failures are a standardized SSE error event followed by stream close — never a retry.
- **Request ID:** `X-Request-Id` accepted or generated; echoed in responses, error bodies, traces, and usage records; the idempotency key for usage settlement.
- **Cancellation contract:** client disconnect or explicit connection close MUST propagate upstream (HTTP body close); observable effects (engine abort, resource release) are part of conformance; tokens emitted before cancellation are billable.

## Contract 2 — Metrics and trace vocabulary

**Owner:** serving-contracts. **Consumers:** infergate (emits), inferops (dashboards/alerts), inferbench (client-side mirror definitions), fleetlab (model inputs).

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
- **Trace attributes:** OTel GenAI semantic conventions at a pinned version (status "Development" as of 2026-07 — the pin is mandatory), plus platform attributes (`inference.config_version`, `inference.tenant_tier`, `inference.backend`, `inference.request_id`). Span sequence for the gateway: `recv → queue.wait → upstream.connect → ttft → stream.relay → settle`.
- **Measurement-point definitions:** TTFT = first upstream body byte at the gateway (client-side TTFT measured by inferbench is a separate, named series); ITL = inter-chunk gap; queue wait = admission-enqueue to dispatch. Definitions are normative so gateway, benchmark, and simulation numbers are comparable.

## Contract 3 — Benchmark data (workload, run, raw events, results)

**Owner:** serving-contracts. **Consumers:** inferbench (emits), fleetlab (consumes), inference-lab (reports).

- **workload.schema.json:** name, version, seed; arrival process (`open-loop-poisson` rate | `closed-loop` with mandatory disclosure flag); input/output-length distributions; prefix-sharing ratio; cancellation-rate profile; slow-client profile; duration or request count. The eight named workloads (`chat-short`, `rag-long-in`, `gen-long-out`, `shared-prefix`, `mixed`, `bursty`, `cancel-storm`, `slow-client`) ship here only as **non-normative example fixtures**; the canonical versioned workload suite is authored and owned by `inferbench` (IB-T003), and `fleetlab` consumes inferbench's suite, not the fixtures.
- **benchmark-run.schema.json (manifest):** run ID; target topology (`engine-direct` | `via-gateway` | `gateway-mock`); engine name/version/commit + all runtime flags (`max_num_seqs`, `max_num_batched_tokens`, `gpu_memory_utilization`, prefix caching, chunked prefill, quantization, KV dtype, speculative decoding config); model checkpoint + revision + tokenizer; hardware (GPU model, VRAM, driver, CUDA version, instance type); gateway version + config version; client location/RTT; warm-up policy; repetition count; hypothesis statement.
- **raw-event.schema.json:** one JSONL record per request: request ID, workload item, send timestamp, TTFT, ITL series or summary + max stall, end timestamp, status, error class, input/output token counts, shed/retry flags, cancellation point.
- **benchmark-result.schema.json:** aggregates per run set: pooled-percentile tables (percentiles computed on pooled raw data — never averaged across runs), throughput, goodput with explicit SLO reference, shed rate (always adjacent to goodput), stall rate, saturation-knee estimate, cost per successful request and per 1M tokens (with cost-profile reference), validity block (warm-up handling, run count, threats to validity, unexplained anomalies), links to raw events and manifest.

## Contract 4 — Backend capability

**Owner:** serving-contracts. **Consumers:** infergate (adapters declare + probe), inferbench (feature-gates workloads), fleetlab (model constraints), inferops (probe configuration).

Fields: engine name + version/commit; streaming support; usage-in-stream support; cancellation mechanism (HTTP-close semantics) and expected release observability; metrics endpoint + name mapping (e.g. vLLM waiting/KV-usage gauges — names vary by version and must be mapped, not hardcoded); tokenizer identity; context limit; max concurrency hints; prefix-cache support + observability; quantization; priority support. Capability descriptors for the mock backend, llama.cpp, and vLLM ship as examples.

## Contract 5 — Deployment

**Owner:** serving-contracts. **Consumers:** infergate (publishes descriptor per release), inferops (consumes), inference-lab (pins).

Fields: image + digest; ports (API, metrics); environment variables and config mounts; startup/readiness/liveness semantics including warm-up-aware readiness (readiness false during model load/warm-up); model mount path and expected volume; resource requests/limits including GPU count; graceful termination (`preStop` drain hook, termination grace period > max stream duration); secret expectations.

## Contract 6 — Fault scenarios (shared vocabulary for I7)

**Owner:** serving-contracts. **Consumers:** inferops (injects), infergate (semantics tests), inferbench (client-impact measurement), inference-lab (postmortems).

The 12 required scenarios, each with: ID, injection description, expected gateway semantics, expected client-visible behavior, metrics that must move, and abort condition:

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

## Contract 7 — Capacity recommendation (fleetlab → inferops)

**Owner:** serving-contracts. **Consumers:** fleetlab (emits), inferops (applies as experiment), inference-lab (Scenario E evidence).

Fields: input references (benchmark-result IDs, workload version, SLO, cost profile, hardware profiles); recommended topology (replica counts per hardware type, engine config); predicted goodput/latency/cost with stated uncertainty; autoscaling signal + thresholds recommendation; assumptions and sensitivity notes. This closes the I6 feedback loop in a machine-checkable form.

---

## Versioning and evolution policy

- **SemVer on the bundle.** MAJOR = any breaking change (removed/renamed field, semantics change, metric rename, bucket change); MINOR = additive optional fields, new schemas, new examples; PATCH = clarifications and fixture fixes.
- **Breaking-change definition:** anything that can make a previously-valid consumer artifact invalid, or change the meaning of a previously-recorded measurement.
- **Deprecation:** deprecated fields carry `deprecated: true` + a removal version; at least one MINOR release separates deprecation from removal; migration notes are mandatory for every MAJOR.
- **Consumer compatibility tests:** `examples/` golden fixtures are consumed by every repo's CI (validate emitted artifacts against schemas; validate accepted inputs against fixtures). Milestone I1 = all four consumers green against the same bundle version.
- **Supported-version matrix:** maintained in `inference-lab` (which bundle versions each released component supports).
- **Pinning:** engine/container/model/tokenizer pins and driver/CUDA recording rules as specified in `03-dependency-graph.md` §4; the benchmark comparability rule is normative and printed in every benchmark report.
- **Pre-1.0 rule:** during `v0.x`, MINOR may break with an explicit migration note (documented honestly); `v1.0.0` freezes Contract 1–3 shapes and is a prerequisite for milestone I6.
