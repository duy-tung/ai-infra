# inferops — Standalone Planning & Implementation Prompt

You are working on the repository **inferops**, part of the `inference-systems` portfolio. This prompt is self-contained: everything you need is embedded here. Do not assume access to the master planning repository.

---

## 1. Mission & context

**Program summary.** The `inference-systems` portfolio is a set of six independent, composable repositories that together form one production-grade LLM inference-serving platform: `serving-contracts` (versioned specs/schemas, no runtime logic), `infergate` (the only inference gateway, Go), `inferbench` (the only load-generation + benchmark-analysis system, Go + Python), `fleetlab` (explainable capacity/autoscaling/cost/placement simulation, Python), `inferops` (this repo), and `inference-lab` (integration evidence, demos, portfolio narrative, OSS log). Repositories integrate only through versioned contracts, released artifacts, result files, or documented network protocols. The program converts an experienced backend/platform engineer's strengths (Go, PostgreSQL, distributed systems, streaming correctness, observability, reliability) into verifiable AI-inference-infrastructure evidence.

**Target positioning (verbatim program goal):**

> Senior Backend / Platform Engineer capable of designing, building, benchmarking, operating, and reasoning about production-grade distributed AI inference infrastructure, with particular strength in streaming correctness, backpressure, scheduling boundaries, observability, capacity planning, reliability, and infrastructure orchestration.

**This repo's purpose.** `inferops` is the portfolio's ONLY Kubernetes deployment, observability-deployment, failure-testing, and runbook repository. It deploys RELEASED images (pinned by digest) per the deployment contract — it never checks out component source. It owns: local Kubernetes (kind/k3s) plus a GPU-node profile; deployments for infergate, vLLM, llama.cpp, and dev PostgreSQL; the OTel Collector / Prometheus / Grafana / Tempo stack with dashboards as code; pod lifecycle semantics (warm-up-aware readiness, graceful drain, rolling updates); failure injection and chaos experiments (the 12 contract fault scenarios); autoscaling **experiments** (capacity **logic** stays in `fleetlab`); and 10 operational runbooks.

**Independent value.** A reference Kubernetes inference-ops stack deployable with released public images: honest probes for slow-warming model servers, dashboards keyed to a published metrics vocabulary, repeatable fault-injection scripts, and verified runbooks. Useful to anyone operating LLM inference on Kubernetes, without any other portfolio repo.

**Integration value.** `inferops` owns integration milestone I5 (the operational stack) and executes the I7 failure campaign; it is the verification arm of I6 (applies fleetlab capacity recommendations as experiments and measures the outcome). It is the "Kubernetes operations → failure campaigns" link of the program's technical story: correct request path → inference gateway → reproducible engine benchmarks → Kubernetes operations → capacity and autoscaling decisions → failure campaigns → open-source contribution.

---

## 2. Hard rules (program-wide, non-negotiable)

1. Repos integrate ONLY via versioned contracts, released artifacts, files, or documented network protocols. The dependency graph is acyclic. No shared application library between repos.
2. One gateway (`infergate`), one load-generation system (`inferbench`), one deployment stack (`inferops`) exist in the whole program. Never duplicate any of them. In particular: this repo must never grow a second load generator or gateway shim.
3. No Kafka, NATS, Redis Streams, or any broker in the synchronous inference request path.
4. The gateway never owns continuous batching, per-token scheduling, KV-cache internals, prefix-cache internals, or GPU placement — those are engine-owned. (inferops owns GPU placement only at the pod/node level: device plugin, resource limits, node labels.)
5. Basic development and CI must not require a GPU. Everything except IO-T005 and the GPU variants of later tasks runs on a CPU-only kind/k3s cluster with the mock backend and llama.cpp. Any GPU session requires a written hypothesis + full config manifest + auto-stop script + budget alert; the program GPU envelope is ~$150–250 total (as of 2026-07; user-confirmable), shared across all repos.
6. Evidence rules: never claim tests/deployments/experiments succeeded without command output or artifacts to point at. Every number carries provenance (measured / source-reported / assumed) and a date. Invalid runs are invalidated, never published. `go test -race` clean is the floor for any Go concurrency work (this repo has little Go, but any test harness code obeys it).
7. Volatile ecosystem facts (vLLM metric names, engine version pins, GPU spot prices, OTel GenAI semconv status "Development", NVIDIA device-plugin details) carry "as of 2026-07 — re-verify at use time" flags in every doc that states them.
8. Ops work must produce **evidence**, not manifests for their own sake. Ops starts only after gateway behavior is proven (infergate's I4-level evidence exists before IO-T005; the CPU baseline IO-T002–T004 starts only after infergate has released an image, IG-T016).

---

## 3. Dependencies & contracts

### What inferops consumes

| Provider | Artifact | Mechanism |
|---|---|---|
| serving-contracts | Contract bundle (SemVer tag, e.g. `v0.1.0`): deployment contract, fault-scenario schema, metrics vocabulary, backend-capability descriptors, API fixtures | pinned released spec bundle; CI validates against fixtures |
| infergate | gateway image + mock-backend image | released container **images by digest** + deployment-contract descriptor per release |
| fleetlab | capacity recommendation documents | **files** (machine-readable, schema-conformant), consumed as experiment input for I6 |

### What inferops provides

| Consumer | Artifact |
|---|---|
| inference-lab | manifests, dashboard/config bundles (released as inferops git tags), campaign logs, runbooks, smoke outputs, GPU-node profile records (driver/CUDA per node) |
| I5/I6/I7 milestones | acceptance evidence (see §9) |

### Forbidden edges (checked at every review gate)

- `inferops` → any component **source checkout**. Released images only. If you find yourself cloning infergate, vLLM, or inferbench source to make a deployment work, stop: that is a deployment-contract gap — file it against `serving-contracts`/`infergate`, do not work around it.
- `inferops` → capacity math or benchmark analysis. Autoscaling **experiments** run here; the signal-comparison logic, capacity models, and predictions live in `fleetlab`. Client-impact **measurement** during fault scenarios is done by running `inferbench` (released binary/image) against the cluster — never by reimplementing load generation.
- No repo consumes inferops as a library. Dashboards/configs are released artifacts.

### Contract summaries (embed-level; the normative schemas live in the pinned `serving-contracts` bundle)

**Contract 5 — Deployment (primary contract for this repo).** Per released component: image + digest; ports (API, metrics); environment variables and config mounts; startup/readiness/liveness semantics including warm-up-aware readiness (readiness false during model load/warm-up); model mount path and expected volume; resource requests/limits including GPU count; graceful termination (`preStop` drain hook, `terminationGracePeriodSeconds` strictly greater than the maximum stream duration); secret expectations. Manifests must be derivable from the descriptor; a manifest that contradicts the descriptor is a defect in one of them, never a silent local fix.

**Contract 6 — Fault scenarios (shared vocabulary for I7).** Each of the 12 scenarios carries: ID, injection description, expected gateway semantics, expected client-visible behavior, metrics that must move, and abort condition. The 12 scenarios and expected gateway semantics:

| # | Scenario | Expected gateway semantics |
|---|---|---|
| 1 | backend killed before first token | pre-first-token retry within retry budget or typed 5xx |
| 2 | backend killed after first token | SSE error event, no retry, partial usage settled |
| 3 | slow backend | pressure-aware routing shifts; timeouts typed |
| 4 | slow client | bounded write buffer + write deadline; stream closed, engine released |
| 5 | gateway termination during streaming | drain semantics; accepted streams complete |
| 6 | queue saturation | sheds with 429 + `Retry-After`; accepted-request latency protected |
| 7 | retry storm | retry budget caps amplification |
| 8 | config reload during traffic | snapshot swap, zero dropped streams |
| 9 | usage database failure | requests unaffected; settlement backlog drains idempotently |
| 10 | one unhealthy backend | routing shifts within bounded interval; circuit opens on error rate |
| 11 | readiness during model warm-up | no traffic before warm; no restart loops |
| 12 | rolling update with active requests | zero client-visible errors |

**Contract 2 — Metrics and trace vocabulary (dashboards key on this).** Canonical Prometheus metrics emitted by infergate; dashboards, alerts, and autoscaling signals must use these exact names — never invent parallel names:

`inference_requests_total` (counter; `model`, `backend`, `tenant_tier`, `status_class`, `error_class`) · `inference_requests_in_flight` (gauge; `backend`) · `inference_queue_depth` (gauge; `tenant_tier`) · `inference_queue_wait_seconds` (histogram; `tenant_tier`) · `inference_ttft_seconds` (histogram; `model`, `backend`) · `inference_itl_seconds` (histogram; `model`, `backend`) · `inference_e2e_duration_seconds` (histogram; `model`, `backend`, `status_class`) · `inference_sheds_total` (counter; `reason`) · `inference_retries_total` (counter; `stage`, always pre-first-token) · `inference_backend_healthy` (gauge; `backend`) · `inference_usage_tokens_total` (counter; `direction`, `model`, `tenant_tier`).

Cardinality policy: forbidden labels are request IDs, raw tenant/user IDs, prompts, arbitrary strings — per-request detail lives in traces; **exemplars link histograms to traces** and must be wired through the collector/Prometheus/Grafana path. Trace attributes follow OTel GenAI semantic conventions at a pinned version (status "Development" as of 2026-07 — the pin is mandatory) plus platform attributes (`inference.config_version`, `inference.tenant_tier`, `inference.backend`, `inference.request_id`). Gateway span sequence: `recv → queue.wait → upstream.connect → ttft → stream.relay → settle`. Measurement points: TTFT = first upstream body byte at the gateway; ITL = inter-chunk gap; queue wait = admission-enqueue to dispatch.

**Contract 4 — Backend capability (probe configuration input).** Per engine: metrics endpoint + metric-name mapping (vLLM waiting/KV-usage gauge names vary by version — mapped, never hardcoded; as of 2026-07, re-verify via `curl /metrics` at session start), cancellation observability, context limits, concurrency hints. inferops uses these descriptors to configure scrapes and health probes for engine pods.

**Contract 1 — Inference API (smoke-test surface).** `POST /v1/chat/completions` (stream + non-stream), `GET /v1/models`, `/healthz`, `/readyz`, `/metrics`; SSE with `data:` events and terminal `data: [DONE]`; error envelope `{"error": {"message","type","code","param"}}` + request ID. inferops smoke tests validate the in-cluster gateway against the bundle's golden fixtures — it does not define or extend the API. The gateway admin surface (`/admin/v1/...`) is NOT part of the shared contract and must never be exposed outside the cluster.

**Contract 7 — Capacity recommendation (fleetlab → inferops).** Fields: input references (benchmark-result IDs, workload version, SLO, cost profile, hardware profiles); recommended topology (replica counts per hardware type, engine config); predicted goodput/latency/cost with stated uncertainty; autoscaling signal + threshold recommendation; assumptions and sensitivity notes. inferops applies a recommendation as a deployment change and records observed outcomes — it never edits the prediction.

### Version pinning (recorded in manifests and the inference-lab pins file)

Contract bundle by SemVer tag; infergate + mock images by digest + tag; engine versions (vLLM v0.24.x baseline minor + exact commit, llama.cpp commit — as of 2026-07, re-verify); model checkpoint revision + quantization + tokenizer; driver/CUDA recorded per GPU-node profile; dashboards/collector configs released as an inferops tag. On every infergate image release: inferops bumps the digest and re-runs I5-level smoke evidence before the pins file advances.

---

## 4. Architecture guidance

### Tooling (the smallest justified set — decide in IO-T001, record as ADR)

Choose the SMALLEST combination out of {Helm, Kustomize, raw manifests, optional Terraform, Argo CD} that the actual requirements justify — do not adopt all of them. **Program default (record as the ADR's decision unless repository evidence overturns it): Kustomize + raw manifests.** Helm is admitted only if a proven templating need emerges (record the concrete need in the ADR before adopting); no Argo CD and no Terraform in the baseline (single local cluster, single operator — GitOps controllers and cloud provisioning add surface without evidence value). Revisit the ADR only on evidence, per the deviation policy.

### Cluster layout

- **Base:** kind or k3s locally (pick one in IO-T001's ADR; kind favors CI reproducibility, k3s favors a persistent local node — decide on evidence of what CI needs). All CPU-path work (mock backend, llama.cpp, dev PostgreSQL, observability stack) runs here GPU-free.
- **GPU-node profile:** a documented, reproducible node setup for a rented single 24 GB-class GPU node (RTX 4090 / L4 / A10 class; source-reported spot prices as of 2026-07: 4090 ~$0.31–0.69/h, L4 ~$0.39/h — re-verify): NVIDIA device plugin installation, `nvidia.com/gpu` resource limits, node labels/taints for GPU scheduling, and a recording step capturing driver + CUDA versions into the node profile document (these are part of benchmark comparability). Grounded in the Kubernetes "Schedule GPUs" documentation (study-track point resource).
- **Workloads:** infergate Deployment (multi-replica capable), mock-backend Deployment, llama.cpp Deployment (CPU), vLLM Deployment (GPU node, model mount per deployment contract), dev PostgreSQL (StatefulSet or single-replica Deployment with a PVC — dev-grade only, documented as such), observability stack (OTel Collector, Prometheus, Grafana, Tempo).

### Lifecycle semantics (the heart of I5)

- **Warm-up-aware readiness:** vLLM model load + warm-up takes minutes. Readiness must be honest — false until the engine can actually serve; startupProbe (or equivalent long-window probe) tolerates the full warm-up; **liveness must never kill a warming pod** (scenario 11's "no restart loops"). Probe endpoints and semantics come from the deployment contract, not invention.
- **Graceful shutdown:** `preStop` drain hook flips readiness and lets accepted streams complete; `terminationGracePeriodSeconds` > maximum stream duration (contract rule — compute the max stream duration from gateway config and set the grace period above it, with the arithmetic recorded).
- **Rolling updates + disruption:** rolling-update strategy tuned so an update under live load produces zero client-visible errors (scenario 12); PodDisruptionBudget for the gateway; documented disruption behavior.
- **Config rollout:** gateway config changes roll out as an immutable snapshot swap (gateway-side); inferops owns the in-cluster mechanics (ConfigMap/secret versioning, rollout, and rollback procedure) exercised by scenario 8.
- **Secret strategy:** no secrets in manifests (see §8 Security).

### Failure injection

Injection is scripted and repeatable: each scenario has an injection script (e.g. `kubectl delete pod` at a controlled phase, network delay via tc/chaos tooling only if justified — prefer the simplest injector that produces the fault), an observation checklist (which metrics must move, which dashboards to capture, which log/trace queries to run), and an expected-vs-observed verdict recorded in a campaign matrix. **Hypotheses are written BEFORE injection** — each run states the expected gateway semantics (from Contract 6) and expected client-visible behavior first, then injects, then compares. Client impact for streaming-critical scenarios (1, 2, 5, 6, 12) is measured by running inferbench against the cluster during injection. GPU-dependent scenarios may fall back to the llama.cpp/mock path with a recorded deviation.

### Autoscaling experiments (experiments only — logic stays in fleetlab)

HPA is the baseline mechanism. KEDA is admitted only if a required signal cannot be served by HPA (+ metrics adapter) — justify in an ADR before adding it. Signals under test: **queue depth** (`inference_queue_depth`), **in-flight requests** (`inference_requests_in_flight`), **token-arrival rate** (derived from `inference_usage_tokens_total`). Each experiment: seeded load (inferbench), a scaling configuration, observed scaling events, and a comparison of observed behavior against fleetlab's predictions for the same workload. inferops never computes what the capacity *should* be — it deploys, drives load, observes, and reports observed-vs-predicted.

### State ownership & failure behavior

inferops owns cluster manifests, dashboards, runbooks, and fault-scenario scripts (git + released config bundles). It owns no application state. Failure/cancellation/retry semantics are the gateway's (Contract 6 column 3 is what inferops verifies, not implements). Observability-stack outage must not take down the request path (verify: kill the collector; gateway keeps serving; runbook "observability outage" covers recovery).

---

## 5. Required documentation set (FIRST task: IO-T001)

Create `docs/` with exactly this structure and content before any implementation:

```text
docs/
├── charter.md                # mission, independent + integration value, positioning (from §1)
├── architecture.md           # cluster layout, tooling decision summary, GPU-node profile design, lifecycle semantics, observability topology (§4)
├── scope.md                  # what inferops owns (§1, §3); the released-images-only rule stated prominently
├── non-goals.md              # no capacity math, no benchmark analysis, no second loadgen/gateway, no source checkouts, no Argo CD/Terraform baseline, no production multi-region
├── interfaces.md             # contracts consumed (deployment, fault-scenario, metrics, capability, API fixtures, capacity recommendation) with pinned bundle version
├── milestones.md             # §6 milestones with acceptance criteria
├── tasks.md                  # IO-T001–IO-T010 expanded per §7
├── risks.md                  # §12 risks incl. R7 and reducible scope
├── testing.md                # smoke tests, lifecycle tests, campaign methodology (§8)
├── observability.md          # dashboards-as-code plan keyed to Contract 2 names; exemplar wiring; alert sketches
├── security.md               # §8 security section content
├── experiments.md            # autoscaling experiment designs + fault-campaign hypothesis templates
├── integration.md            # I5/I6/I7 roles + acceptance criteria (§9); pins handling
├── oss-opportunities.md      # §11 content
├── implementation-notes.md   # running log + Deviations section (see §13 policy)
└── adr/                      # ADR-0001 tooling choice (Kustomize + raw manifests default); later: KEDA justification (if any), kind-vs-k3s, chaos tooling choice
```

---

## 6. Repository milestones (dependency-ordered; no calendar durations)

| # | Milestone | Depends on | Acceptance criteria |
|---|---|---|---|
| M1 | Docs + tooling ADR | prompt approval | all 15 docs/ files + the `adr/` directory exist with content; ADR-0001 (tooling) reviewed |
| M2 | CPU cluster baseline | M1; infergate release IG-T016; contracts bundle with deployment/fault schemas | released infergate + mock + dev PostgreSQL deployed by digest; contract-fixture smoke test green against in-cluster gateway; zero source checkouts (auditable) |
| M3 | Observability stack | M2 | OTel Collector, Prometheus, Grafana, Tempo running; golden dashboards render from a test stream using exact Contract 2 metric names; exemplars link a histogram panel to a Tempo trace |
| M4 | Lifecycle semantics | M2 | scripted rolling-update-under-load test: zero client-visible errors; warm-up-aware readiness demonstrated (llama.cpp/mock warm-up simulation on CPU); preStop drain verified; PDB in place; grace period > max stream duration recorded with arithmetic |
| M5 | GPU node + vLLM | M4; infergate GPU evidence (IG-T014); GPU gate G6 | in-cluster vLLM serves via gateway; readiness honest during real multi-minute warm-up; driver/CUDA recorded; session auto-stopped; Scenario D smoke green |
| M6 | Campaign part 1 | M3, M4 | scenarios 1–6 injected on mock/llama.cpp path: hypothesis-first, scripted, checklist observed, verdicts recorded |
| M7 | Campaign complete | M6; M5 for GPU-relevant scenarios (CPU fallback allowed with recorded deviation) | 12/12 scenarios executed (or the documented reduced set, §12); client impact measured via inferbench for scenarios 1, 2, 5, 6, 12 |
| M8 | Runbooks verified | M4 (+M5/M7 for their subjects) | 10 runbooks each verified by tabletop or live walkthrough with notes |
| M9 | Autoscaling experiments | M3; fleetlab signal-comparison outputs | HPA experiments on ≥1 signal run with seeded load; observed-vs-predicted comparison report done |
| M10 | Procedures hardened | M4 | config rollout (scenario 8 in-cluster), secret strategy, upgrade/rollback procedures scripted and verified |

I5 acceptance requires M2–M5; I7 requires M6–M7 (+M8 for runbook references); I6's verification arm requires M9.

---

## 7. Task seeds (stable IDs — use exactly these)

Schema per task: Goal/Repo · Requirement or hypothesis · Dependencies · Expected files · Complexity (S/M/L) · Critical path · Parallel-safe · Human-review focus · Verification · Evidence · Integration impact · Required/Stretch · Stop condition.

### IO-T001 — Planning docs bootstrap + tooling ADR
- **Goal/Repo:** create the full `docs/` set (§5) and decide the deployment tooling. inferops.
- **Requirement:** all 15 docs/ files + the `adr/` directory with repo-specific content; ADR-0001 records the smallest justified tooling set — program default: Kustomize + raw manifests; Helm only on a proven templating need; no Argo CD/Terraform in baseline.
- **Dependencies:** this prompt; pinned contracts bundle (read-only). **Expected files:** `docs/*`, `docs/adr/0001-deployment-tooling.md`.
- **Complexity:** M. **Critical path:** no. **Parallel-safe:** yes.
- **Human-review focus:** tooling ADR reasoning (does each admitted tool have a concrete justification?); released-images-only rule stated in scope.
- **Verification:** docs checklist against §5; ADR review.
- **Evidence:** committed docs + ADR. **Integration impact:** unblocks all IO tasks. **Required.**
- **Stop condition:** 15 docs/ files + `adr/` exist with content + tooling ADR reviewed.

### IO-T002 — Local cluster baseline
- **Goal/Repo:** kind/k3s cluster running released infergate + mock backend + dev PostgreSQL, deployed by digest per the deployment contract. inferops.
- **Requirement:** no source checkouts anywhere; manifests derived from the deployment-contract descriptor; images pinned by digest; smoke test drives the in-cluster gateway with contract fixtures (stream + non-stream + error classes).
- **Dependencies:** IO-T001; infergate release (IG-T016); contracts deployment/fault schemas (SC-T006). **Expected files:** `clusters/local/*`, `deploy/infergate/*`, `deploy/mock-backend/*`, `deploy/postgres-dev/*`, `scripts/smoke.sh`.
- **Complexity:** M. **Critical path:** yes. **Parallel-safe:** no.
- **Human-review focus:** contract-only consumption (audit: no git clone of component repos, no image builds from source).
- **Verification:** `scripts/smoke.sh` — contract fixtures pass against the in-cluster gateway; `kubectl get pods` all Ready.
- **Evidence:** manifests + smoke output. **Integration impact:** I5 path start. **Required.**
- **Stop condition:** smoke green.

### IO-T003 — Observability stack
- **Goal/Repo:** deploy OTel Collector, Prometheus, Grafana, Tempo; dashboards as code keyed to the Contract 2 metrics vocabulary; exemplars wired end-to-end. inferops.
- **Requirement:** dashboard JSON/jsonnet committed (as code, not click-ops); every panel queries the exact contract metric names; an exemplar on a latency histogram panel opens the corresponding Tempo trace; scrape configs use the capability descriptors for engine metric endpoints.
- **Dependencies:** IO-T002; contracts metrics vocabulary (SC-T005). **Expected files:** `deploy/observability/*`, `dashboards/*.json`, `docs/observability.md` updates.
- **Complexity:** M. **Critical path:** yes. **Parallel-safe:** no.
- **Human-review focus:** dashboard names/queries match vocabulary exactly; no forbidden-cardinality labels introduced by relabeling.
- **Verification:** run a test stream through the gateway; metrics visible end-to-end; exemplar click-through demonstrated.
- **Evidence:** dashboard exports/screenshots + scrape configs. **Integration impact:** I5 (golden dashboards); all campaign observation. **Required.**
- **Stop condition:** golden dashboard renders from live traffic.

### IO-T004 — Lifecycle semantics
- **Goal/Repo:** implement and prove startup/readiness/liveness (warm-up-aware), preStop drain, rolling update under load, disruption budget. inferops.
- **Requirement:** readiness false during warm-up (simulate slow warm-up on the CPU path via mock/llama.cpp startup delay); liveness never kills warming pods; startupProbe window covers worst-case warm-up; preStop drain lets accepted streams finish; `terminationGracePeriodSeconds` > max stream duration (arithmetic recorded); rolling update under scripted live load with zero client-visible errors; PDB defined.
- **Dependencies:** IO-T002. **Expected files:** probe/lifecycle sections of `deploy/*`, `scripts/rolling-update-test.sh`, `docs/testing.md` updates.
- **Complexity:** M. **Critical path:** yes. **Parallel-safe:** no.
- **Human-review focus:** probe semantics vs the deployment contract (any mismatch is a contract defect, not a local hack).
- **Verification:** scripted rolling-update-under-load test output shows 0 client errors; warm-up test shows no restarts and no early traffic.
- **Evidence:** test output logs. **Integration impact:** fault scenarios 11/12; I5. **Required.**
- **Stop condition:** zero-error rolling update demonstrated.

### IO-T005 — GPU node profile + vLLM deployment (GPU gate G6)
- **Goal/Repo:** reproducible GPU-node profile and a contract-conformant vLLM deployment. inferops.
- **Requirement:** device plugin install, `nvidia.com/gpu` limits, node labels, driver/CUDA versions recorded into the node profile; vLLM deployed per deployment contract with model mount and secret strategy; readiness honest during real multi-minute warm-up. GPU session per program rules: written hypothesis + full config manifest + auto-stop script + budget alert; teardown script tested.
- **Dependencies:** IO-T004; infergate vLLM evidence (IG-T014); GPU gate G6 open. **Expected files:** `clusters/gpu-node/*`, `deploy/vllm/*`, `docs/gpu-node-profile.md`, session log.
- **Complexity:** M. **Critical path:** yes. **Parallel-safe:** no.
- **Human-review focus:** GPU session plan BEFORE the session (hypothesis, manifest, auto-stop, teardown).
- **Verification:** in-cluster vLLM serves via the gateway (Scenario D smoke); readiness observed false→true across warm-up with no restarts; instance auto-stopped.
- **Evidence:** session log + manifests + driver/CUDA record. **Integration impact:** I5. **Required (GPU).** CPU fallback: llama.cpp-backed I5 variant with recorded deviation.
- **Stop condition:** Scenario D smoke green; instance stopped.

### IO-T006 — Fault injection: scenarios 1–6
- **Goal/Repo:** repeatable injection scripts + observation checklists + verdicts for Contract 6 scenarios 1–6, run against mock/llama.cpp paths first. inferops.
- **Requirement:** per scenario: hypothesis written BEFORE injection (expected gateway semantics + expected client behavior + metrics that must move); injection script; observation checklist; expected-vs-observed verdict in the campaign matrix. Client impact for scenarios 1, 2, 5, 6 measured with inferbench running during injection.
- **Dependencies:** IO-T003, IO-T004. **Expected files:** `faults/scenario-{01..06}/{inject.sh,checklist.md,hypothesis.md,verdict.md}`, `faults/campaign-matrix.md`.
- **Complexity:** L. **Critical path:** yes. **Parallel-safe:** no.
- **Human-review focus:** the expected-semantics table vs Contract 6 (verbatim agreement or a filed contract defect).
- **Verification:** each scenario: injected, observed, gateway semantics match or deviation recorded; scripts re-runnable.
- **Evidence:** campaign logs + matrix rows 1–6 + inferbench client-impact files for 1, 2, 5, 6. **Integration impact:** I7. **Required.**
- **Stop condition:** 6/6 executed with verdicts.

### IO-T007 — Fault injection: scenarios 7–12 + noisy neighbor
- **Goal/Repo:** complete the campaign: scenarios 7–12 (same hypothesis-first pattern), plus a noisy-neighbor observation run (tenant A 10× load; verify tenant B protection at the ops level — the fairness logic itself is infergate's). inferops.
- **Requirement:** scenarios 7–12 injected and adjudicated; scenario 12 client impact measured with inferbench; GPU-relevant scenarios (esp. 11 with real vLLM warm-up) may run on the CPU fallback path with a recorded deviation.
- **Dependencies:** IO-T006; IO-T005 for GPU-relevant scenarios (CPU fallback allowed). **Expected files:** `faults/scenario-{07..12}/*`, updated `faults/campaign-matrix.md`, noisy-neighbor run notes.
- **Complexity:** M. **Critical path:** yes. **Parallel-safe:** no.
- **Human-review focus:** deviations honestly recorded (fallback paths, semantics mismatches → gateway or spec defects, not silent passes).
- **Verification:** matrix shows 12/12 executed or documented CPU-fallback subset; each row: injected / observed / verdict.
- **Evidence:** campaign logs + client-impact measurements (inferbench). **Integration impact:** I7. **Required.**
- **Stop condition:** 12/12 executed or documented fallback subset.

### IO-T008 — Runbooks
- **Goal/Repo:** write and verify the 10 operational runbooks. inferops.
- **Requirement:** runbooks for: **deploy, upgrade, rollback, drain, backend failure, performance regression, config rollback, capacity shortfall, observability outage, database outage** — each with preconditions, steps, verification commands, and rollback path; each verified by tabletop or live walkthrough with notes. Apply the Google SRE overload/cascading-failures review lens (see §10) to backend-failure, capacity-shortfall, and performance-regression runbooks.
- **Dependencies:** IO-T004 (plus IO-T005/T007 for the runbooks whose subjects need them). **Expected files:** `runbooks/{deploy,upgrade,rollback,drain,backend-failure,performance-regression,config-rollback,capacity-shortfall,observability-outage,database-outage}.md`, `runbooks/walkthroughs/*.md`.
- **Complexity:** M. **Critical path:** no. **Parallel-safe:** yes.
- **Human-review focus:** runbook accuracy — every command in a runbook must have been actually run in a walkthrough.
- **Verification:** tabletop or live walkthrough per runbook, notes captured.
- **Evidence:** runbooks + walkthrough notes. **Integration impact:** I7/I8. **Required.**
- **Stop condition:** 10 walkthroughs done.

### IO-T009 — Autoscaling experiments
- **Goal/Repo:** run HPA-based autoscaling experiments and compare observed behavior against fleetlab predictions. inferops.
- **Hypothesis (per experiment, written first):** scaling on <signal> at <threshold> keeps <SLO metric> within <bound> under the seeded workload — as predicted by fleetlab report <ID>.
- **Requirement:** HPA baseline; KEDA only if a required signal cannot be served otherwise (justify in an ADR before adopting); signals: queue depth, in-flight requests, token-arrival rate; mock/llama.cpp backends (GPU variant only if budget remains); seeded inferbench load; record scaling events (`kubectl get events`, HPA status, metric snapshots); compare observed vs fleetlab-predicted behavior. Capacity logic stays in fleetlab — this task deploys, drives, observes, reports.
- **Dependencies:** IO-T003; fleetlab signal-comparison output (FL-T006). **Expected files:** `experiments/autoscaling/*`, `experiments/autoscaling/report.md`, optional `docs/adr/000X-keda.md`.
- **Complexity:** M. **Critical path:** no. **Parallel-safe:** yes.
- **Human-review focus:** experiment design (seeded, controlled, one variable); no capacity math creeping in.
- **Verification:** scaling events observed and recorded per experiment; comparison table predicted-vs-observed.
- **Evidence:** experiment report. **Integration impact:** I6 verification arm. **Required (depth reducible — see §12).**
- **Stop condition:** comparison report done.

### IO-T010 — Config rollout + secrets + upgrade procedure
- **Goal/Repo:** harden the operational procedures: in-cluster config rollout (fault scenario 8 mechanics), secret strategy, upgrade/rollback. inferops.
- **Requirement:** config rollout procedure exercised in-cluster under traffic (pairs with scenario 8); secret strategy documented and implemented (no secrets in manifests — see §8); upgrade and rollback procedures scripted and verified (digest bump → smoke → pins-file advance; rollback to previous digest).
- **Dependencies:** IO-T004. **Expected files:** `scripts/{config-rollout,upgrade,rollback}.sh`, `docs/security.md` secret-strategy section, procedure docs.
- **Complexity:** S. **Critical path:** no. **Parallel-safe:** yes.
- **Human-review focus:** secret handling.
- **Verification:** scripted checks run with captured output.
- **Evidence:** procedure docs + outputs. **Integration impact:** scenarios 8; release/pin mechanics for I5+. **Required.**
- **Stop condition:** procedures verified.

---

## 8. Testing, observability, security, performance hypotheses

**Testing (`docs/testing.md`).**
- Smoke tier: contract fixtures against the in-cluster gateway (every deploy, every digest bump).
- Lifecycle tier: scripted rolling-update-under-load, warm-up-readiness, drain tests (IO-T004) — re-runnable, output-capturing scripts, not manual checklists.
- Campaign tier: hypothesis-first fault scenarios with injection scripts + observation checklists + verdicts (IO-T006/T007); flaky scenarios are marked unreliable with analysis, never quietly retried to green.
- Everything runs GPU-free except IO-T005 and GPU variants; CI must be able to spin the kind cluster and run smoke + lifecycle tiers.

**Observability (`docs/observability.md`).**
- Dashboards as code, keyed to the exact Contract 2 metric names; a "golden dashboard" covering: request rate/status, queue depth + queue wait, TTFT/ITL/E2E histograms, sheds by reason, retries by stage, backend health, token throughput.
- Exemplars wired: histogram panels link to Tempo traces; trace view shows the `recv → queue.wait → upstream.connect → ttft → stream.relay → settle` span sequence.
- Alert sketches (not paged, documented): backend unhealthy, shed-rate spike, queue-depth sustained growth, readiness flapping.
- The observability stack is not on the request path: its outage must not affect serving (verified in the observability-outage runbook walkthrough).

**Security (`docs/security.md`) — must cover:**
- **Secret strategy:** no secrets in manifests or git — Kubernetes Secrets created out-of-band (scripted from local env/files excluded from git), documented rotation procedure; SOPS/sealed-secrets only if a real need emerges (ADR).
- **API-key material handling:** gateway tenant API keys are infergate's domain (hashed at rest in PostgreSQL); inferops handles only the bootstrap/admin credentials needed to operate — never logs them, never bakes them into images or ConfigMaps.
- **Image provenance:** deploy by digest only; the digest recorded in manifests must match the released artifact in the pins file; no `:latest`, no locally built component images.
- **Network exposure:** the gateway admin surface (`/admin/v1/...`) and all `/metrics` endpoints stay in-cluster (ClusterIP; no Ingress/NodePort for them); only the public inference API is exposed for test traffic; dev PostgreSQL never exposed outside the cluster.

**Performance hypotheses (`docs/experiments.md`; all numbers get measured provenance + date when produced).**
- H1: rolling update under load with correct probes/drain yields 0 client-visible errors (scenario 12 target — this is a program success criterion, not a guess).
- H2: with warm-up-aware readiness, a vLLM pod receives 0 requests before warm-up completes and undergoes 0 liveness restarts during warm-up (scenario 11).
- H3: scaling on queue depth reacts faster than scaling on CPU utilization for token-heavy workloads — test against fleetlab's prediction, report agreement or divergence (divergence is a result, not a failure).
- H4: killing the observability stack changes gateway request success rate by 0.

---

## 9. Integration milestones this repo participates in

**I5 — Operational stack (inferops OWNS this milestone).**
Prerequisites: I4 (or its recorded CPU fallback); infergate release IG-T016; IO-T002–T005. Pins: contracts bundle, infergate image digest, inferops release, dashboard/config bundle versions.
**Acceptance:** `inferops → infergate → vLLM → OTel/Prometheus/Grafana/Tempo` on the local cluster + GPU node: **deployment from released images only (no source checkout); warm-up-aware readiness demonstrated; rolling update under load with zero client-visible errors; golden dashboards live; traces end-to-end.**
Failure handling: probe/drain violations → fix manifests or the deployment contract (a contract change requires re-running I1 contract compatibility); observability gaps → dashboard/collector fix. Evidence: manifests, smoke outputs, dashboard exports, rolling-update test log.

**I7 — Failure campaign (inferops owns EXECUTION; inference-lab owns evidence archival).**
Prerequisites: I5; IO-T006/T007; the fault-scenario contract. Pins: frozen component set for the campaign.
**Acceptance:** all 12 contract fault scenarios injected (GPU-dependent ones may run on the llama.cpp/mock path with a recorded deviation); for each: expected gateway semantics observed or deviation documented; client impact measured by inferbench for at least the streaming-critical scenarios (1, 2, 5, 6, 12); **≥2 postmortems published in the standard format: timeline from real metrics, detection gap, root cause, mitigation, action items.**
Failure handling: semantics mismatch → gateway defect or spec defect; fix, re-run scenario; repeated flakiness → scenario marked unreliable with analysis. Evidence: campaign matrix (12 rows: injected / observed / verdict), postmortems, client-impact measurements.

**I6 — Capacity feedback (inferops is the verification arm; loop owned by inference-lab, recommendation by fleetlab).**
inferops' role: apply the fleetlab capacity recommendation (replica count / config change per Contract 7) as a deployment change, so a repeated benchmark can measure the outcome; run the IO-T009 autoscaling experiments whose observed behavior is compared against fleetlab predictions. A wrong prediction is a *result* to publish with error analysis, never a failure to hide. inferops never edits the recommendation or the analysis.

---

## 10. Study-track artifacts owned/consumed by this repo

| Resource | Artifact | Consumer | Stop condition |
|---|---|---|---|
| Google SRE book — "Handling Overload", cascading failures, retry budgets | runbook + campaign review lens: a written checklist applied when reviewing the backend-failure / capacity-shortfall / performance-regression runbooks and when adjudicating campaign scenarios 6/7/10 (retry amplification, load shedding, cascade containment) | IO-T008 runbooks; I7 campaign reviews | lens applied and cited in walkthrough notes |
| Kubernetes "Schedule GPUs" documentation | GPU-node profile (device plugin, resource limits, labels, driver/CUDA recording) | IO-T005 | profile reproducible + recorded |

Governing rule: artifact-or-drop — a resource that produces no artifact after two sessions is dropped. No standalone summaries; only inputs to registered artifacts.

---

## 11. OSS opportunities

- **Kubernetes examples/docs improvements for Gateway API Inference Extension (GAIE) / llm-d** discovered while building the reference stack: probe configurations, kind-based test setups, GPU-node examples. GAIE is the program's primary OSS target (Go, kind-testable, exactly the gateway/routing boundary); note the repo-migration caveat toward llm-d (`InferenceModel`→`InferenceObjective` rename, source-reported as of 2026-07 — re-verify before engaging).
- **Reproducible K8s inference-ops configurations are publishable artifacts** in their own right: a warm-up-aware readiness pattern for model servers, a drain-correct rolling-update recipe, dashboards keyed to a published metrics vocabulary. These qualify as the OSS track's "public benchmark or design artifact."
- All OSS activity is logged in `inference-lab` (IL-T010–T012); submissions require user review before posting; avoid scheduler rewrites, architecture replacements, and unverified performance claims.

---

## 12. Risks and kill criteria

| Risk | Trigger | Mitigation |
|---|---|---|
| **R7 — Kubernetes time sink ("YAML exercise")** (L:M, I:M — the repo's headline risk) | ops work blocks a wave exit without producing new evidence | smallest-tooling ADR (IO-T001); ops starts only after gateway behavior is proven; runbook/probe scope fixed by the deployment contract; every task's stop condition is an evidence artifact, not a manifest count; autoscaling depth is reducible |
| R2 — GPU budget/availability | budget alert fires; no GPU access | G6 gate; IO-T005 is the repo's only GPU task; CPU fallback = llama.cpp-backed I5 variant + fallback subset for GPU-relevant scenarios, all with recorded deviations |
| R3 — ecosystem drift (device plugin, engine metric names, dashboards) | scrape/probe configs break on a new pin | pin everything; capability metric-name mapping, never hardcoding; dated provenance flags |
| R12 — overclaiming | any claim without a log/output | evidence rules §2.6; campaign matrix links every verdict to captured output |

**Pre-decided scope reductions (cut in this order if a wave exit is threatened — never silently):**
1. KEDA/autoscaling breadth → keep ONE HPA experiment + the fleetlab simulation comparison.
2. Chaos breadth → the 12 scenarios reduce to the 6 streaming-critical ones: **1, 2, 5, 6, 11, 12** — with a documented deviation.

**Never cut:** fault-injection evidence entirely (some campaign must run), contract validation, the I6 feedback loop (it may shrink to mock/llama.cpp scale but must close), cancellation-correctness observation in scenarios.

**Generic drop rule:** drop or postpone anything that blocks the critical path without producing new evidence, duplicates an existing capability, lacks a measurable artifact, exceeds GPU budget, or creates source coupling.

---

## 13. Definition of Done

inferops is accepted when (aligned with program success criteria §2):

1. **I5 accepted** — operated stack from released images only; warm-up-aware readiness demonstrated; rolling update under load with zero client-visible errors; golden dashboards live; end-to-end traces.
2. **I7 accepted** — 12-scenario campaign matrix published (or the documented reduced set per §12), each row injected/observed/verdict; client impact measured for scenarios 1, 2, 5, 6, 12; ≥2 postmortems in the standard format.
3. **10 runbooks walked through** with notes (deploy, upgrade, rollback, drain, backend failure, performance regression, config rollback, capacity shortfall, observability outage, database outage).
4. **Deploys only released artifacts** — auditable: no component source checkout anywhere in the repo history or CI.
5. **Campaign matrix published** and archived in inference-lab with the pins that were in effect.

## 14. Deviation policy

> Keep `docs/implementation-notes.md`. When repository evidence forces a deviation from the approved plan, choose the conservative reversible option, record the evidence, decision, consequences, and follow-up under `Deviations`, and continue. Pause only when the deviation changes public contracts, repository ownership, security posture, or milestone scope.

## 15. Session operating instructions

1. **First**: execute IO-T001 — create the full `docs/` set (§5) including the tooling ADR. Get the plan reviewed before any implementation.
2. Then implement strictly in task dependency order (§7; the critical path is IO-T002 → IO-T003 → IO-T004 → IO-T005 → I5 → IO-T006 → IO-T007 → I7). `Par:yes` tasks (IO-T001, IO-T008, IO-T009, IO-T010) may run alongside once their dependencies pass.
3. Run every task's verification command/procedure, capture the output, and link it from the task's evidence location.
4. Commit with clear messages, one logical change per commit. Never push to other repositories; cross-repo issues (contract defects, image/descriptor mismatches) are filed against the owning repo, not fixed here.
5. GPU work (IO-T005 and any GPU-variant experiment) only behind the G6 gate: written hypothesis + config manifest + auto-stop script + budget alert, reviewed before the session; teardown verified; session log committed.
6. Record everything notable — surprises, ecosystem drift, fallbacks taken, contract defects filed — in `docs/implementation-notes.md`; deviations per §14.
7. Mandatory human-review points: the tooling ADR (and any KEDA ADR), the expected-semantics table before the campaign starts, every GPU session plan, secret handling, and wave-exit evidence bundles (short summary + evidence links + the specific question to decide — never raw logs).
