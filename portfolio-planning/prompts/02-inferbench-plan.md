# Standalone prompt — `inferbench` (load generation + benchmark analysis)

You are working on the repository **`inferbench`**, one of six repositories in the `inference-systems` portfolio. This prompt is self-contained: the master planning repo is NOT available to you. Everything you need is embedded here. Your first task is to create the repository documentation set (IB-T001), get it reviewed, and then implement strictly in task dependency order.

---

## 1. Mission and context

**Program.** The `inference-systems` portfolio is a set of independent, composable repositories that together form one production-grade LLM inference-serving platform and individually demonstrate senior-level engineering judgment. It converts an experienced backend/platform engineer's strengths (Go, PostgreSQL, distributed systems, streaming correctness, observability, reliability) into verifiable AI-inference-infrastructure evidence. The six repos: `serving-contracts` (versioned specs/schemas, no runtime logic), `infergate` (thin multi-tenant inference gateway, Go), `inferbench` (this repo), `fleetlab` (capacity/autoscaling/cost simulation, Python), `inferops` (Kubernetes/observability/chaos/runbooks), `inference-lab` (integration, evidence, portfolio narrative, OSS log).

**Target positioning of the portfolio (verbatim program goal):**

> Senior Backend / Platform Engineer capable of designing, building, benchmarking, operating, and reasoning about production-grade distributed AI inference infrastructure, with particular strength in streaming correctness, backpressure, scheduling boundaries, observability, capacity planning, reliability, and infrastructure orchestration.

**This repo's purpose.** `inferbench` is the portfolio's ONLY load-generation and benchmark-analysis system. It has two halves:

- **Go load generator:** open-loop and Poisson arrivals, fixed seeds, concurrent SSE streams, cancellation and slow-client workloads, rate sweeps, replay of recorded workloads, raw JSONL event capture.
- **Python analysis:** confidence intervals, pooled-percentile statistics, saturation-knee detection, goodput@SLO, cost per successful request and per 1M tokens, A/B comparisons, graphs, reports.

**Independent value.** `inferbench` benchmarks ANY OpenAI-compatible endpoint over the network — engine-direct (llama.cpp, vLLM, the deterministic mock backend) or with `infergate` in front. It must work WITHOUT `infergate`; proving that against a non-infergate endpoint is part of this repo's Definition of Done. Integration happens only via the API contract and result files. It never imports target source.

**Integration value.** Its result files are the evidence backbone of the portfolio: they gate the local request path (I2), produce the first benchmark report (I3), measure gateway overhead on GPU (I4), feed `fleetlab`'s capacity models and close the benchmark→capacity→deployment→re-benchmark loop (I6), and measure client impact during failure campaigns (I7). Methodologically valid benchmarking is on the program's never-cut list.

## 2. Hard rules (program-wide, non-negotiable)

1. Repositories integrate ONLY via versioned contracts, released artifacts, files, or documented network protocols. The dependency graph is acyclic. No shared application library between repos.
2. One gateway (`infergate`), one load-generation system (`inferbench`), one deployment stack (`inferops`) exist in the whole program. Never duplicate any of them; never let anyone else grow a second load generator.
3. No Kafka/NATS/Redis or any broker in the synchronous inference request path.
4. The gateway never owns continuous batching, per-token scheduling, KV-cache internals, prefix-cache internals, or GPU placement — those are engine-owned. `inferbench` treats both gateway and engine as black-box network targets and never re-implements or asserts their internals.
5. Basic development and CI must not require a GPU. Any GPU session requires a written hypothesis + full config manifest + auto-stop script + budget alert. Program GPU envelope: ~$150–250 total (as of 2026-07; user-confirmable), alerts at 50% and 80%.
6. Evidence rules: never claim tests/benchmarks succeeded without command output or artifacts to point at. Every number carries provenance (measured / source-reported / assumed) and a date. Invalid benchmark runs are invalidated, never published. `go test -race` clean is the floor for all Go concurrency work.
7. Volatile ecosystem facts (engine metric names, upstream repo layouts, GPU prices, OTel GenAI semconv status, `vllm bench serve` behavior, LiteLLM self-reported numbers) carry "as of 2026-07 — re-verify at use time" flags.

## 3. Dependencies and contracts

### What this repo consumes

| Provider | Mechanism | Content |
|---|---|---|
| `serving-contracts` | pinned released spec bundle (SemVer tag); CI validates against golden fixtures | Contract 1 (inference API), Contract 2 (metrics vocabulary), Contract 3 (benchmark data schemas), Contract 4 (backend capability), plus cost/SLO profile schemas used by the analysis half |
| `infergate` / engines / any OpenAI-compatible endpoint | **network only** (HTTP/SSE) at run time | benchmark targets; the released mock-backend image (owned by infergate) is the CI target |

### What this repo provides

| Consumer | Mechanism | Content |
|---|---|---|
| `fleetlab` | benchmark-result + raw-event **files** conforming to Contract 3 | goodput/memory/latency profiles input; I6 feedback loop |
| `inference-lab` | reports + result files | I2–I4, I6, I7 evidence; portfolio benchmark reports |

### Forbidden edges (checked at every review gate)

- `inferbench` → engine or gateway **source** (network targets only; build and test against recorded fixtures and the released mock image).
- `inferbench` does NOT own any schema. Workload/run/raw-event/result schemas are OWNED by `serving-contracts`. Any schema-affecting change here is blocked until contracts release it first.
- No shared statistics library with `fleetlab` — the metric definitions both rely on live in the contracts metric vocabulary; data exchange is files only.
- No capacity modeling, no dashboards, no Kubernetes manifests (those belong to `fleetlab` and `inferops`).

### Contract summaries (embed-level detail)

**Contract 1 — Inference API (OpenAI-compatible subset).** `inferbench` DRIVES this contract. Endpoints: `POST /v1/chat/completions` (stream + non-stream), `GET /v1/models`, `GET /healthz`, `GET /readyz`, `GET /metrics`. Supported request fields (all others are rejected by conformant servers, never ignored): `model`, `messages`, `max_tokens`/`max_completion_tokens`, `temperature`, `top_p`, `stream`, `stream_options.include_usage`, `stop`, `seed`, `user`. Streaming: SSE `data: <json-chunk>` events, terminal `data: [DONE]`, every event flushed, usage in the final chunk when `stream_options.include_usage=true`, monotonically increasing chunk indices per stream, no cross-request interleaving. Error envelope: `{"error": {"message", "type", "code", "param"}}` + request ID; taxonomy with retryability: `invalid_request`, `authentication`, `permission`, `not_found`, `rate_limited` (429 + `Retry-After`), `overloaded` (503 + `Retry-After`), `upstream_error`, `upstream_timeout`, `canceled`, `internal`. Mid-stream failures arrive as a standardized SSE error event then stream close. `X-Request-Id` is accepted or generated and echoed everywhere. Cancellation contract: client disconnect / connection close MUST propagate upstream; tokens emitted before cancellation are billable. `inferbench` exercises all of this: it issues cancellations, parses error events, records request IDs, and classifies outcomes per the taxonomy.

**Contract 2 — Metrics vocabulary (client-side mirror).** Normative measurement points: gateway TTFT = first upstream body byte at the gateway; **client-side TTFT measured by inferbench is a separate, named series** — never conflate the two; ITL = inter-chunk gap; queue wait = admission-enqueue to dispatch (gateway-side). `inferbench` maintains client-side mirror definitions with explicit names (e.g. `client_ttft`, `client_itl`) so gateway, benchmark, and simulation numbers are comparable and their differences (network RTT, client scheduling) are explainable, not mysterious.

**Contract 3 — Benchmark data schemas (this repo EMITS, contracts OWN).**
- `workload.schema.json`: name, version, seed; arrival process (`open-loop-poisson` rate | `closed-loop` with mandatory disclosure flag); input/output-length distributions; prefix-sharing ratio; cancellation-rate profile; slow-client profile; duration or request count. The eight named workloads ship as versioned examples in contracts.
- `benchmark-run.schema.json` (manifest): run ID; target topology (`engine-direct` | `via-gateway` | `gateway-mock`); engine name/version/commit + ALL runtime flags (`max_num_seqs`, `max_num_batched_tokens`, `gpu_memory_utilization`, prefix caching, chunked prefill, quantization, KV dtype, speculative decoding config); model checkpoint + revision + tokenizer; hardware (GPU model, VRAM, driver, CUDA version, instance type); gateway version + config version; client location/RTT; warm-up policy; repetition count; hypothesis statement.
- `raw-event.schema.json`: one JSONL record per request: request ID, workload item, send timestamp, TTFT, ITL series or summary + max stall, end timestamp, status, error class, input/output token counts, shed/retry flags, cancellation point.
- `benchmark-result.schema.json`: pooled-percentile tables (percentiles computed on pooled raw data — never averaged across runs), throughput, goodput with explicit SLO reference, shed rate (ALWAYS adjacent to goodput), stall rate, saturation-knee estimate, cost per successful request and per 1M tokens (with cost-profile reference), validity block (warm-up handling, run count, threats to validity, unexplained anomalies), links to raw events and manifest.

**Contract 4 — Backend capability.** Fields: engine name + version/commit; streaming support; usage-in-stream support; cancellation mechanism (HTTP-close semantics) and expected release observability; metrics endpoint + name mapping (vLLM gauge names vary by version — mapped, never hardcoded); tokenizer identity; context limit; max concurrency hints; prefix-cache support + observability; quantization; priority support. `inferbench` uses capability descriptors to **feature-gate workloads**: e.g. usage-in-stream support determines whether output token counts come from the stream's usage chunk or from tokenizer-side estimation (declared in the manifest); prefix-cache support gates the shared-prefix experiments; the metrics mapping drives optional engine cache-info collection.

## 4. Architecture guidance

**Data flow.**

```text
workload file (versioned, seeded, schema-valid)
      │
      ▼
seeded arrival scheduler ──► SSE streaming client ──HTTP/SSE──► target
(send times fixed by seed,      │        │                (mock | llama.cpp | vLLM |
 never by responses)            │        │                 infergate in front | any
      │                         │        │                 OpenAI-compatible endpoint)
      │              cancellation      slow-client
      │              controller        emulator
      ▼                         │        │
raw-event recorder ◄────────────┴────────┘        manifest capturer ──► run manifest (JSON)
(JSONL, streaming writes)                          engine-metrics poller (side channel)
      │
      ▼
Python analysis: load/validate ─► pooled stats ─► knee/goodput/cost ─► report + result file
                                                                        (benchmark-result
                                                                         schema, consumed
                                                                         by fleetlab &
                                                                         inference-lab)
```

**Suggested repository layout.**

```text
cmd/inferbench/          # single CLI: run, sweep, replay, compare, experiment
internal/schedule/       # seeded arrival processes (open-loop poisson, closed-loop flagged)
internal/client/         # SSE client, monotonic timing, cancellation, slow-client
internal/events/         # raw-event JSONL recorder
internal/sweep/          # rate-sweep orchestration
internal/replay/         # deterministic replay
internal/experiment/     # hypothesis-file governance
internal/manifest/       # manifest capture + refusal logic
workloads/               # the 8 versioned seeded workload files
analysis/                # Python package: stats, knee, goodput, cost, compare, report
docs/                    # §6 documentation set
```

**Components (Go generator).** Workload loader/validator (reads versioned workload files, validates against the pinned schema); seeded arrival scheduler (open-loop: send times computed from the seed + arrival process BEFORE and INDEPENDENT of any response — this is the coordinated-omission defense); SSE streaming client (monotonic clocks for TTFT/ITL capture, per-chunk timestamps, max-stall tracking); cancellation controller (issues deliberate cancels at declared points: queued / pre-first-token / mid-stream, per the workload's cancellation profile); slow-client emulator (bounded read rate); raw-event recorder (streaming JSONL writes, bounded memory); sweep orchestrator (≥6 rate points, repetition control); replay runner (re-issues a recorded workload deterministically); manifest capturer (collects target/engine/hardware/config facts before the run; refuses to run without them); optional engine-metrics poller (scrapes `/metrics` via the capability mapping, records as side-channel series, never blocks the load path).

**Components (Python analysis).** Loader/validator (raw events + manifests, schema-checked; refuses undeclared or manifest-less data); statistics core (pooled percentiles, bootstrap CIs, warm-up exclusion); knee detector; goodput@SLO calculator (with shed rate and stall rate computed in the same pass — a goodput figure can never be produced without them); cost calculator (per successful request / per 1M tokens from cost-profile files); comparison engine (A/B across runs sharing all variables except one declared variable); plotting; report generator (template embeds manifest, interpretation rules, threats-to-validity and unexplained-anomalies sections; emits schema-valid benchmark-result files).

**Data and state.** Files only. No database, no server. Raw events are append-only JSONL per run; manifests are JSON; results are schema-valid JSON; reports are Markdown/HTML with embedded graphs. Every run directory is self-describing: manifest + workload reference + raw events + logs.

**Concurrency model (Go).** One scheduler goroutine owns the send timeline; per-request goroutines own the stream lifecycle; the recorder is a single writer fed by a bounded channel. The send schedule must never be perturbed by slow responses, slow disk, or a saturated target (open-loop invariant). If the client host itself cannot keep the schedule (CPU/FD/network limits), the run is INVALID: detect this (schedule-slip watchdog, client resource sampling) and abort with a typed reason, recording it in the run log. `go test -race` clean is mandatory.

**Failure, cancellation, retry behavior.** Target errors, timeouts, sheds, and mid-stream SSE error events are recorded as classified raw events — they never crash the run and are never silently dropped (shed/error visibility is what makes goodput honest). The generator NEVER retries: a retry would corrupt the open-loop arrival process and hide errors; retry behavior is the gateway's concern and is observed, not performed. Deliberate cancellation is a workload feature, executed by closing the connection at the declared point and recording the cancellation point in the event. Runs have abort conditions (schedule slip, client saturation, target unreachable at start) that mark the run invalid rather than emitting misleading data.

## 5. Methodology (normative — encode these in code, templates, and review checklists)

These rules are the repo's reason to exist. Violating them is the program's R4 risk (benchmark invalidity). Gate G4 (methodology review) must pass before ANY report is published.

1. **Open-loop Poisson arrivals are mandatory for any latency or goodput claim.** Closed-loop mode exists only to find a throughput ceiling and every closed-loop result is flagged as such (closed-loop hides queueing delay — coordinated omission).
2. **Warm-up exclusion:** the first ≥50 requests or 60–120 s are excluded from statistics; every run declares cache state (cold/warm) in the manifest.
3. **Rate sweeps:** ≥6 points spanning 10% → 120% of estimated capacity.
4. **Repetition:** ≥3 runs per point; report median ± range across runs.
5. **Pooled percentiles:** percentiles are computed on pooled raw per-request data across repetitions. NEVER average percentiles across runs.
6. **Full manifest per run:** GPU model + VRAM, driver/CUDA, instance type, model checkpoint + revision + quantization + tokenizer, engine version + commit + all flags, gateway commit + config version, client location/RTT, warm-up policy, repetition count, hypothesis.
7. **Goodput@SLO** requires an explicit, pre-declared SLO; the **shed rate is ALWAYS reported adjacent** (goodput can be gamed by shedding early), and stall rate beside it (a stream can meet TTFT SLO and still stall mid-generation).
8. **One-command reproduction** per report: the report names the exact command + pinned versions that regenerate it.
9. Every report has mandatory **"threats to validity"** and **"unexplained anomalies"** sections. An empty anomalies section means "we looked and found none", stated explicitly.
10. **No comparisons across uncontrolled variables:** results are comparable only when model revision, quantization, tokenizer, engine version+flags, hardware, driver/CUDA, workload version+seed, and warm-up policy all match, or the difference is the single declared experimental variable. No cross-hardware or cross-tool comparisons.
11. **No extrapolation past the saturation knee.** Relative claims (A vs B under identical conditions) are more durable than absolute numbers; prefer them.
12. **Anti-patterns to detect and refuse:** coordinated omission, uncontrolled output lengths (cap or direct them per workload), missing warm-up handling, version drift between compared runs, undisclosed hardware, single-run conclusions, mean-only reporting, cherry-picking runs.

**Metrics measured:** TTFT; ITL/TPOT (full distribution + max stall + stall rate); end-to-end latency; throughput (tokens in/out per second); goodput at declared SLO (shed rate adjacent); stream completion rate; queue delay (gateway-reported, correlated by request ID); shed/retry/error rates; engine cache info when the capability descriptor exposes it; cost per successful request and per 1M tokens.

**Workload suite (versioned, seeded, per the workload schema):**

| Workload | Intent | Key controlled parameters |
|---|---|---|
| `chat-short` | interactive chat baseline | short input/output length distributions |
| `rag-long-in` | prefill-heavy (long context in) | long input, short output |
| `gen-long-out` | decode-heavy (long generation) | short input, long directed output |
| `shared-prefix` | prefix-cache behavior | **controlled prefix-sharing ratio** (measurable, tunable) |
| `mixed` | realistic blend | declared mix proportions of the above |
| `bursty` | queueing/admission behavior | burst amplitude + period over a base Poisson rate |
| `cancel-storm` | cancellation correctness under load | cancellation-rate profile with declared cancel points |
| `slow-client` | backpressure/write-buffer behavior | bounded client read rate profile |

All eight: name, version, seed, arrival process, input/output-length distributions (output length capped/directed — never uncontrolled), duration or request count, per the workload schema.

**Controlled experiments (hypothesis-driven, single-variable, with stop conditions; NO full-matrix sweeps):** `max_num_seqs`; `max_num_batched_tokens` (reproduce the Sarathi-Serve TTFT/ITL trade-off with your own numbers); `gpu_memory_utilization` (including preemption onset); context length; prefix caching on/off with controlled prefix-sharing ratio; chunked prefill; quantization (AWQ/GPTQ vs FP16 where budget allows); KV-cache dtype. Stretch (IB-T012 only): speculative decoding/MTP, KV offloading, SGLang comparison.

## 6. Required documentation set (FIRST task — IB-T001)

Create `docs/` with exactly this set; each file must have real content for THIS repo:

```text
docs/
├── charter.md                # mission, independent value, "the only load generator" rule
├── architecture.md           # generator + analysis components, open-loop design, data flow, CO defense
├── scope.md                  # loadgen, workloads, stats, experiments, reports — and nothing else
├── non-goals.md              # no gateway/engine/K8s/capacity-model/dashboards; no schema ownership; no retries in the client
├── interfaces.md             # consumed contracts (1–4 summaries + pinned bundle version), emitted file formats, CLI surface
├── milestones.md             # §7 below, dependency-ordered, acceptance criteria
├── tasks.md                  # §8 task register (IB-T001…IB-T012) with all schema fields
├── risks.md                  # R4, R10, GPU budget, client-as-bottleneck, tool-calibration risk
├── testing.md                # §9 testing strategy; synthetic known-answer tests; determinism; CO-safety test
├── observability.md          # run logs, client-side metric series naming, schedule-slip watchdog, self-diagnostics
├── security.md               # target credentials via env only; no secrets in manifests/events; synthetic prompts only
├── experiments.md            # methodology rules (§5 verbatim-in-substance), experiment governance, hypothesis template, experiment catalog
├── integration.md            # roles in I2/I3/I4/I6/I7 with the acceptance criteria from §10
├── oss-opportunities.md      # §12 below
├── implementation-notes.md   # running log + Deviations section (see §14)
└── adr/                      # ADRs: open-loop scheduler design, statistics choices, closed-loop flagging, tool calibration protocol
```

## 7. Repository milestones (dependency-ordered; no calendar durations)

| # | Milestone | Contents | Acceptance criteria |
|---|---|---|---|
| M1 | Plan & docs | IB-T001 | all 16 docs entries exist with repo-specific content; reviewed |
| M2 | Generator core | IB-T002, IB-T003 | open-loop + Poisson + seeds; 8 workloads validate against pinned schema and dry-run vs the released mock image; emitted JSONL events schema-valid; same seed → identical send schedule; CO-safety design reviewed |
| M3 | Measurement correctness | IB-T004 | client TTFT/ITL vs mock's configured latencies agree within declared tolerance (calibration report vs mock); cancellation issuance works at all 3 points; slow-client emulation bounded-rate verified |
| M4 | Analysis & reports (G4) | IB-T005, IB-T006 | synthetic known-answer statistics tests green; pooled-percentile + shed-adjacent-goodput + stall-rate enforced in code; sample end-to-end report from a mock run is schema-valid and passes G4 methodology review |
| M5 | Sweeps & governance | IB-T008, IB-T009 | sweep (≥6 points) produces a knee on the mock; replay deterministic; framework rejects hypothesis-less experiment runs and combinatorial sweeps |
| M6 | Calibration | IB-T007 | deltas vs reference tooling (`vllm bench serve` on GPU, or llama.cpp-based reference on CPU — as of 2026-07, re-verify tool behavior at use time) tabulated and within stated tolerance or explained |
| M7 | Experiment set 1 (CPU) | IB-T010 | benchmark report #1 published: gateway overhead (direct vs via-gateway, mock + llama.cpp) and admission on/off at ~5× capacity; ≥3 runs/point, pooled stats, validity block; feeds gate G5 |
| M8 | Experiment set 2 (GPU) | IB-T011 | benchmark report #2 published from ≤ budgeted scripted GPU sessions, or the documented CPU fallback deviation |
| M9 | Independence proof | (part of DoD) | a run against a non-infergate OpenAI-compatible endpoint completes with schema-valid outputs |
| M10 | Stretch | IB-T012 | only if budget remains and baseline stable; kill rules apply |

## 8. Task seeds (stable IDs — use EXACTLY these)

Tasks must stay narrow, independently reviewable, and evidence-producing. You may split a task into sub-points but keep the IDs.

### IB-T001 — Planning docs bootstrap
- **Goal / repo:** create the full `docs/` set per §6, including the methodology doc skeleton (`experiments.md` with the §5 rules) — inferbench.
- **Requirement:** every file populated with repo-specific content, not templated boilerplate.
- **Dependencies:** this prompt; contracts bundle v0.1.x available. **Expected files:** `docs/*`, `docs/adr/`.
- **Complexity:** M. **Critical path:** no. **Parallel-safe:** yes. **Required.**
- **Review focus:** methodology rules correctly and completely embedded; non-goals explicit.
- **Verification:** checklist against §6; every §5 rule appears in `experiments.md`.
- **Evidence:** committed docs. **Integration impact:** none direct; unblocks everything.
- **Stop condition:** all docs exist with content and the plan is reviewed.

### IB-T002 — Open-loop generator core + raw events
- **Goal / repo:** the load-generation engine — inferbench.
- **Requirement:** open-loop + Poisson arrivals, fixed seeds, concurrent SSE streams, JSONL raw events per `raw-event.schema.json`; send schedule computed independently of responses; schedule-slip watchdog; no client-side retries ever.
- **Dependencies:** contracts SC-T002/SC-T003 (API + benchmark schemas released); released mock-backend image. **Expected files:** `cmd/inferbench/`, `internal/schedule/`, `internal/client/`, `internal/events/`, tests.
- **Complexity:** L. **Critical path:** yes. **Parallel-safe:** no. **Required.**
- **Review focus:** coordinated-omission safety (send-schedule independence) — this review is mandatory.
- **Verification:** schema validation of emitted events against pinned fixtures; deterministic replay with same seed vs mock (identical schedules); `go test -race ./...` clean.
- **Evidence:** sample run artifacts vs the mock image; CI output. **Integration impact:** prerequisite for I2.
- **Stop condition:** CO-safety reviewed; emitted events validate.

### IB-T003 — Workload suite v1
- **Goal / repo:** the 8 named workloads as versioned seeded files per the workload schema — inferbench.
- **Requirement:** `chat-short`, `rag-long-in`, `gen-long-out`, `shared-prefix` (controlled prefix-sharing ratio), `mixed`, `bursty`, `cancel-storm`, `slow-client`; controlled input/output-length distributions (output length capped/directed — uncontrolled output length is an anti-pattern); cancellation and slow-client profiles encoded.
- **Dependencies:** SC-T003. **Expected files:** `workloads/*` (format per schema), dry-run scripts, tests.
- **Complexity:** M. **Critical path:** no. **Parallel-safe:** yes. **Required.**
- **Review focus:** length distributions controlled; prefix-sharing ratio actually controlled (measurable, not incidental).
- **Verification:** all 8 validate against the pinned schema; dry-run vs mock completes.
- **Evidence:** workload files + dry-run logs. **Integration impact:** shared with fleetlab arrival models (same versioned files).
- **Stop condition:** 8 workloads run.

### IB-T004 — Streaming client correctness
- **Goal / repo:** trustworthy client-side measurement — inferbench.
- **Requirement:** client-side TTFT/ITL capture with monotonic clocks; per-chunk timestamps + max-stall; cancellation issuance at queued / pre-first-token / mid-stream; slow-client emulation (bounded read rate); client series named per the metrics-contract mirror rule (client TTFT ≠ gateway TTFT — separate named series).
- **Dependencies:** IB-T002. **Expected files:** `internal/client/` extensions, calibration harness, tests.
- **Complexity:** M. **Critical path:** yes. **Parallel-safe:** no. **Required.**
- **Review focus:** measurement-point alignment with the metrics contract.
- **Verification:** run vs mock with known configured latencies — measured ≈ configured within declared tolerance.
- **Evidence:** calibration report vs mock. **Integration impact:** I2/I3 measurements depend on it.
- **Stop condition:** mock calibration within tolerance.

### IB-T005 — Analysis core (Python)
- **Goal / repo:** the statistics engine — inferbench.
- **Requirement:** pooled-percentile computation (never average percentiles across runs — enforced in code, not convention); bootstrap CIs; warm-up exclusion (≥50 requests or 60–120 s); saturation-knee detection; goodput@SLO with shed rate adjacent and stall rate computed in the same pass; cost per successful request / per 1M tokens using cost-profile files.
- **Dependencies:** IB-T002 outputs (sample raw events). **Expected files:** `analysis/` Python package, unit tests with synthetic distributions.
- **Complexity:** L. **Critical path:** yes. **Parallel-safe:** no. **Required.**
- **Review focus:** statistics choices (bootstrap parameters, knee method, pooling correctness).
- **Verification:** unit tests on synthetic distributions with analytically known answers, all green.
- **Evidence:** test suite output. **Integration impact:** results feed fleetlab.
- **Stop condition:** synthetic-data tests green.

### IB-T006 — Report generator + validity block
- **Goal / repo:** the honest-report machine — inferbench.
- **Requirement:** report template embedding the full manifest, interpretation rules, mandatory "threats to validity" + "unexplained anomalies" sections, the one-command reproduction line, and the comparability rule; results emitted per `benchmark-result.schema.json`; closed-loop results visibly flagged.
- **Dependencies:** IB-T005. **Expected files:** `analysis/report/`, templates, sample report.
- **Complexity:** M. **Critical path:** yes. **Parallel-safe:** no. **Required.**
- **Review focus:** honesty rules encoded (goodput never rendered without shed + stall rates; no mean-only tables).
- **Verification:** end-to-end report from a mock run; result file validates against the pinned schema.
- **Evidence:** sample report. **Integration impact:** the evidence format for I3 and everything after.
- **Stop condition:** sample report approved — this is gate **G4** together with IB-T009.

### IB-T007 — Calibration vs reference tooling
- **Goal / repo:** prove the generator's numbers are not an artifact of the generator — inferbench.
- **Requirement:** cross-check against `vllm bench serve` (GPU session, behind G6) or a llama.cpp-based reference (CPU fallback); identical workload/target; document deltas and their causes.
- **Dependencies:** IB-T004; G6 for the GPU variant. **Expected files:** calibration report under `docs/`, comparison scripts.
- **Complexity:** M. **Critical path:** no. **Parallel-safe:** yes. **Required.**
- **Review focus:** calibration protocol — same measurement points? same warm-up? same arrival process? Differences must be enumerated before comparing.
- **Verification:** comparison table within stated tolerance or every delta explained.
- **Evidence:** calibration report. **Integration impact:** credibility of all published numbers; possible upstream findings (§12).
- **Stop condition:** deltas explained.

### IB-T008 — Sweeps, replay, comparison mode
- **Goal / repo:** the experiment mechanics — inferbench.
- **Requirement:** rate sweeps (≥6 points, 10% → 120% of estimated capacity); replay of recorded workloads (deterministic); A/B comparison runner that refuses comparisons violating the single-variable rule.
- **Dependencies:** IB-T004. **Expected files:** `internal/sweep/`, `internal/replay/`, comparison CLI, tests.
- **Complexity:** M. **Critical path:** no. **Parallel-safe:** yes. **Required.**
- **Review focus:** sweep design (point placement around the estimated knee).
- **Verification:** sweep vs mock produces a detectable knee; replay determinism test green.
- **Evidence:** sweep artifacts. **Integration impact:** saturation/knee inputs for fleetlab; I4 gateway-overhead sweeps.
- **Stop condition:** sweep produces a knee on mock.

### IB-T009 — Controlled-experiment framework
- **Goal / repo:** experiment governance in code — inferbench.
- **Requirement:** a hypothesis file is required per experiment (hypothesis, single declared variable, expected direction, stop condition, repeat policy); the framework rejects hypothesis-less runs and combinatorial/full-matrix sweeps; GPU experiments additionally require the session manifest + auto-stop reference (G6 enforcement).
- **Dependencies:** IB-T006. **Expected files:** `internal/experiment/`, hypothesis template, governance docs.
- **Complexity:** M. **Critical path:** no. **Parallel-safe:** yes. **Required.**
- **Review focus:** experiment governance completeness.
- **Verification:** demo showing a hypothesis-less run is rejected and a matrix sweep is rejected.
- **Evidence:** framework docs + dry-run transcript. **Integration impact:** G6 enforcement arm; makes IB-T010/T011 auditable.
- **Stop condition:** governance demo done. (With IB-T006, closes gate **G4**.)

### IB-T010 — Experiment set 1 (CPU): gateway overhead + admission value
- **Goal / repo:** the first published benchmark report — inferbench.
- **Hypotheses:** (a) infergate adds ≤ low single-digit ms p95 non-queue overhead vs direct — falsify against LiteLLM's self-reported 8 ms p95 as a source-reported baseline (as of 2026-07 — re-verify); (b) with admission control ON at ~5× estimated capacity, accepted-request TTFT p95 degrades ≤20% vs the capacity-boundary baseline while sheds are typed 429/503 + `Retry-After` (admission OFF as control).
- **Requirement:** direct-vs-gateway on mock + llama.cpp; admission on/off overload runs; full methodology (≥3 runs/point, pooled stats, validity block, one-command repro).
- **Dependencies:** IB-T006; infergate IG-T010 (admission control) released. **Expected files:** hypothesis files, run artifacts, benchmark report #1.
- **Complexity:** M. **Critical path:** yes. **Parallel-safe:** no. **Required.**
- **Review focus:** hypothesis + design BEFORE running; fresh-context report audit against the validity checklist AFTER.
- **Verification:** report regenerates from raw events via the one command; G5 evidence criteria met.
- **Evidence:** benchmark report #1. **Integration impact:** gate G5; portfolio claim #1.
- **Stop condition:** report published.

### IB-T011 — Experiment set 2 (GPU): vLLM behavior
- **Goal / repo:** controlled vLLM engine-behavior evidence — inferbench.
- **Hypotheses/experiments (each single-variable, hypothesis-first):** `max_num_batched_tokens` TTFT/ITL trade-off (reproduce the Sarathi-Serve trade-off with own numbers); `max_num_seqs`; `gpu_memory_utilization` including preemption onset; prefix caching on/off with controlled prefix-sharing ratio (`shared-prefix` workload); chunked prefill; quantization (AWQ/GPTQ vs FP16 where budget allows); KV-cache dtype if feasible. NO full-matrix sweeps. Engine metrics collected via the capability mapping.
- **Dependencies:** IB-T009; infergate IG-T014 (vLLM adapter); gate G6 per session (written hypothesis + manifest + auto-stop + budget alert). **Expected files:** hypothesis files, session manifests, run artifacts, benchmark report #2.
- **Complexity:** L. **Critical path:** no. **Parallel-safe:** no. **Required** (GPU; documented CPU fallback allowed per program rules).
- **Review focus:** GPU session plans reviewed BEFORE spend.
- **Verification:** manifests complete; ≥3 repeats per point; engine metrics present; report schema-valid.
- **Evidence:** benchmark report #2 + session logs. **Integration impact:** fleetlab profiles (FL-T004); I4 and I6 inputs.
- **Stop condition:** budget cap reached or hypotheses answered.

### IB-T012 — Experiment set 3 (stretch): speculative decoding/MTP, KV offloading, SGLang comparison
- **Goal / repo:** stretch depth only if the baseline is safe — inferbench.
- **Requirement:** same governance as IB-T011; SGLang comparison uses the RadixAttention-informed shared-prefix design.
- **Dependencies:** IB-T011 complete + GPU budget remaining + baseline stable. **Expected files:** hypothesis files, report addendum.
- **Complexity:** L. **Critical path:** no. **Parallel-safe:** no. **Stretch.**
- **Review focus:** kill-rule adherence.
- **Verification:** same as IB-T011.
- **Evidence:** report addendum or a documented kill note. **Integration impact:** portfolio depth only.
- **Stop condition:** any kill trigger — SGLang is first to drop (killed if >4 h setup without a running comparison, GPU budget ≥80% consumed, or the vLLM baseline is unstable; pre-armed fallback = vLLM prefix caching on/off, which is already in IB-T011).

## 9. Testing, observability, security

**Testing.** GPU-free CI. Layers: (1) unit tests — arrival-schedule determinism (same seed → byte-identical schedule), Poisson distribution sanity, SSE parser against contract fixtures, event serialization vs pinned schema; (2) statistics known-answer tests — synthetic distributions with analytically known percentiles/CIs/knees; a pooled-vs-averaged-percentile test that FAILS if anyone reintroduces percentile averaging; (3) CO-safety test — a deliberately stalled mock target must not shift subsequent send times; (4) calibration tests vs the mock's configured TTFT/ITL/error rates; (5) contract compatibility — validate emitted workload/run/event/result files against the pinned contracts bundle in CI (`make contracts-verify` pattern; this repo's arm of milestone I1); (6) replay determinism; (7) `go test -race ./...` clean as the floor; Python tests via pytest.

**Observability.** The generator's own health is part of validity: structured run logs; schedule-slip watchdog with typed abort; client host resource sampling (CPU, FDs, network) recorded into the run log and cited in threats-to-validity; per-run summary printed at completion (sent/completed/canceled/shed/error counts). Client-side metric series follow the mirror-naming rule from the metrics contract. Optional engine `/metrics` polling is side-channel only and never on the load path.

**Security.** Target API keys only via environment variables or an ignored local file — never in manifests, raw events, workloads, logs, or git. Redact `Authorization` headers everywhere. Workload prompts are synthetic (generated from seeds) — no real user data, no PII, ever. Result files are shareable by construction; verify no secret can leak into an emitted artifact (test it).

**Performance hypotheses (examples to be TESTED, never assumed; provenance flagged).**

| Hypothesis | Provenance | Where tested |
|---|---|---|
| infergate non-queue overhead ≤ low single-digit ms p95 (program SLO: p95 <10 ms / p99 <20 ms); LiteLLM self-reports 8 ms p95 — a source-reported baseline (as of 2026-07) to falsify, not a measured fact | source-reported / program target | IB-T010 |
| Admission control at ~5× overload keeps accepted-request TTFT p95 degradation ≤20% vs capacity-boundary baseline | program target (G5) | IB-T010 |
| Raising `max_num_batched_tokens` improves throughput but worsens ITL/TPOT tail (Sarathi-Serve trade-off) — reproduce with own numbers | source-reported (paper) | IB-T011 |
| Prefix caching improves TTFT proportionally to the controlled prefix-sharing ratio; near-zero effect at ratio ≈ 0 | assumed, from RadixAttention reasoning | IB-T011 |
| The generator sustains all published rates without client-side schedule slip | must be measured on the client host | every run (watchdog) |

## 10. Integration milestones this repo participates in

- **I1 — Contract compatibility (re-entrant).** inferbench CI validates golden fixtures AND its own emitted artifacts against the pinned bundle; green run linked in the inference-lab pins file.
- **I2 — Local request path.** `inferbench → infergate → mock`: seeded workload with 100 concurrent streams, zero frame mixing; 3-point cancellation verified (mock abort observed within bound); raw events schema-valid; **client-vs-gateway TTFT agreement within declared tolerance**; traces/metrics visible. Failure handling: measurement disagreement → check measurement-point definitions before touching code.
- **I3 — Local inference.** `inferbench → infergate → llama.cpp` completes `chat-short` and `shared-prefix` on CPU; **first schema-valid benchmark report** generated (manifest + validity block); cancellation verified against llama.cpp. Invalid report → G4 review before proceeding.
- **I4 — GPU inference.** `inferbench → infergate → vLLM` on a rented GPU: streaming + cancellation verified via engine metrics; **gateway-overhead comparison (direct vs via-gateway) measured with ≥3 runs/point**; session auto-stopped; all artifacts carry the full manifest. CPU fallback = documented deviation, llama.cpp becomes the measured baseline.
- **I6 — Capacity feedback (the central story).** inferbench's benchmark corpus (IB-T010/T011) feeds fleetlab → capacity recommendation → inferops applies it → **inferbench re-benchmarks the outcome**; predicted vs measured published, including where the prediction was wrong. Requires contracts v1.0.0.
- **I7 — Failure campaign.** inferbench measures **client impact** for at least the streaming-critical fault scenarios **1 (backend killed pre-first-token), 2 (killed post-first-token), 5 (gateway termination during streaming), 6 (queue saturation), 12 (rolling update under load)**; measurements attached to the campaign matrix and ≥2 postmortems.

## 11. Study-track artifacts owned by or consumed through this repo

| Resource | Artifact | Consuming task | Stop condition |
|---|---|---|---|
| Sarathi-Serve (OSDI'24, medium read) | `max_num_batched_tokens` TTFT/ITL trade-off hypothesis file | IB-T011 | experiment run |
| DistServe (OSDI'24, medium read) | goodput@SLO definition (encoded in contracts; this repo implements it faithfully) | IB-T005/T006 | definition encoded |
| Goodput-critique paper (arXiv 2410.14257, skim) | stall-rate-beside-goodput reporting rule in the report template | IB-T006 | rule encoded |
| SGLang / RadixAttention (NeurIPS'24, medium read) | shared-prefix workload design (+ hash-block vs radix comparison note if IB-T012 runs) | IB-T003, IB-T012 | workload designed |
| Systems Performance (Gregg) — methodology + latency chapters | benchmark-methodology review checklist addition used at G4 | G4 / `docs/experiments.md` | checklist merged |

Rule: artifact-or-drop. A resource with no artifact after two sessions is dropped.

## 12. OSS opportunities

- **Reproducible engine-behavior reports** (IB-T011) with full manifests are upstream-communicable evidence — the vLLM fallback track of the program's OSS plan (docs/metrics/tests scope only; e.g. a reproducible behavior report or a metric-documentation correction grounded in measured evidence).
- **Calibration deltas vs `vllm bench serve`** (IB-T007) may surface upstream documentation or tooling issues worth filing (as of 2026-07 — re-verify the tool's current name/behavior first).
- All upstream communication goes through the inference-lab OSS log and requires user review before posting. Avoid: unverified performance claims, scheduler rewrites, unsolicited large refactors.

## 13. Risks and kill criteria

| Risk | Trigger | Mitigation |
|---|---|---|
| **R4 — Benchmark invalidity** (coordinated omission, uncontrolled variables, cherry-picking). Owner: this repo. | G4 audit failure; validity block incomplete | methodology encoded in schemas + report template + framework (IB-T006/T009); **G4 gate: methodology review before ANY published report**; "invalidate, don't publish"; fresh-context audit of every published report |
| **R10 — Stretch experiments destabilize the baseline.** | >4 h SGLang setup without a running comparison; baseline unstable | kill order: **SGLang comparison drops first**; pre-armed fallback = vLLM prefix caching on/off; then speculative decoding/MTP/KV offloading (IB-T012) drop |
| **R2 — GPU budget overrun/unavailability.** | budget alert fires | G6 gate per session (hypothesis + manifest + auto-stop + budget alert); envelope ~$150–250 (as of 2026-07, user-confirmable), alerts at 50%/80%; only IB-T007 (GPU variant), IB-T011, IB-T012 may spend GPU time here; any hypothesis-less GPU run is stopped immediately; CPU fallbacks documented as deviations |
| Client host becomes the bottleneck (silent invalidity) | schedule-slip watchdog fires | abort + invalidate the run; record in threats-to-validity |
| Tool-calibration mismatch undermines credibility | IB-T007 deltas unexplained | do not publish comparative claims until deltas are explained |

Reducible/stretch here: IB-T012 is entirely stretch. Never cut: methodologically valid benchmarking (program never-cut list) and this repo's role in the I6 loop (it may shrink to mock/llama.cpp scale but must close).

## 14. Definition of Done (this repository)

`inferbench` is accepted when, with linked evidence:

1. **G4 passed** — methodology review of the analysis pipeline + report template + experiment governance (IB-T006 + IB-T009).
2. **Calibration report done** (IB-T007) with deltas within tolerance or explained.
3. **Experiment set 1 (CPU) published** (IB-T010) and **experiment set 2 (GPU) published** (IB-T011) — or the documented CPU-fallback deviation for set 2 — both with manifests, pooled percentiles, goodput@SLO with shed rate adjacent, validity + threats-to-validity blocks, and one-command reproduction.
4. **Proven to work against a non-infergate endpoint** (independence demonstrated with schema-valid outputs).
5. CI green including contract-compatibility validation against the pinned bundle; `go test -race` clean.

## 15. Deviation policy

> Keep `docs/implementation-notes.md`. When repository evidence forces a deviation from the approved plan, choose the conservative reversible option, record the evidence, decision, consequences, and follow-up under `Deviations`, and continue. Pause only when the deviation changes public contracts, repository ownership, security posture, or milestone scope.

## 16. Session operating instructions

1. **First**: execute IB-T001 — create/update the full `docs/` set per §6. Present it for review before writing implementation code.
2. Implement strictly in task dependency order (§8; the critical path here is IB-T002 → IB-T004 → IB-T005 → IB-T006 → IB-T010). Tasks marked parallel-safe may proceed concurrently once their dependencies are met.
3. Run each task's verification command/procedure, capture the output, and link it from `docs/implementation-notes.md` (cross-repo evidence goes to inference-lab at integration time).
4. Commit with clear messages; never push to other repositories; schema changes are proposed to `serving-contracts`, never made locally.
5. GPU work only behind gate G6 (written hypothesis + full manifest + auto-stop script + budget alert), and only for IB-T007 (GPU variant), IB-T011, IB-T012.
6. Claims discipline: tests failed → say so; step skipped → say so; no "should work". Invalid runs are invalidated, never published.
7. Record everything notable — decisions, surprises, measured facts with provenance and dates — in `docs/implementation-notes.md`.
