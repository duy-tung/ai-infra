# 00 — Program Charter

**Program:** Composable AI Inference Systems Portfolio (`inference-systems`)
**Run type of this document set:** Planning only — no runtime code, no infrastructure, no model downloads, no GPU workloads were produced in this run.
**Date:** 2026-07-09
**Working repository for planning artifacts:** `ai-infra` (branch `claude/inference-portfolio-planning-qxngwa`)

---

## 1. Mission

Build a portfolio of independent, composable repositories that together form one production-grade LLM inference-serving platform, and that individually demonstrate senior-level engineering judgment. The program converts an experienced backend/platform engineer's existing strengths (Go, PostgreSQL, distributed systems, streaming correctness, observability, reliability) into verifiable AI-inference-infrastructure evidence.

### Target positioning (verbatim program goal)

> Senior Backend / Platform Engineer capable of designing, building, benchmarking, operating, and reasoning about production-grade distributed AI inference infrastructure, with particular strength in streaming correctness, backpressure, scheduling boundaries, observability, capacity planning, reliability, and infrastructure orchestration.

### Required technical story

```text
correct request path
→ inference gateway
→ reproducible engine benchmarks
→ Kubernetes operations
→ capacity and autoscaling decisions
→ failure campaigns
→ open-source contribution
```

Every mandatory artifact in this plan exists to make one link of that story demonstrable with evidence.

---

## 2. Engineer profile

**Existing strengths (reuse, do not re-teach):** Go, PostgreSQL, distributed systems, event-driven architecture, Kafka/NATS JetStream, gRPC/REST/WebSockets/CDC, idempotency/retries/replay/DLQ/backpressure, OpenTelemetry, production debugging, Docker, CI/CD, systems above 10,000 QPS.

**Skills to deepen (every one maps to at least one repository or artifact — see `11-traceability-matrix.md`):** Python for ML-systems tooling and analysis; LLM inference-engine behavior; llama.cpp, vLLM, and selectively SGLang; GPU memory/capacity/cost reasoning; Kubernetes operations for inference workloads; benchmark methodology and statistical validity; autoscaling and heterogeneous fleet planning; open-source contribution.

---

## 3. Portfolio structure

Six repositories, each with independent user value, integrating only through versioned contracts, released artifacts, result files, or documented network protocols:

```text
inference-systems/
├── serving-contracts   # versioned specs & schemas; no runtime logic
├── infergate           # thin, measurable, multi-tenant inference gateway (Go)
├── inferbench          # the only load-generation + benchmark-analysis system (Go + Python)
├── fleetlab            # explainable capacity/autoscaling/cost/placement simulation (Python)
├── inferops            # the only Kubernetes/observability/chaos/runbook repository
└── inference-lab       # integration, evidence, demos, portfolio narrative, OSS log
```

Ownership details: `02-repository-responsibilities.md`. Dependency rules: `03-dependency-graph.md`. Contracts: `04-shared-contracts.md`.

---

## 4. Source reconciliation (summary)

Three consolidated source documents were inspected (see `13-evidence-assumptions-and-deviations.md` for the full inventory):

1. `final-ai-infrastructure-curriculum-24-weeks-vi.md` — reconciled 24-week curriculum (480 h), single flagship repo (`infergate`), 12 two-week milestones.
2. `ke-hoach-tong-hop-ai-infra-24-tuan.md` — final consolidated 24-week plan; same single-repo strategy; adds verified engine facts, GPU budget (~$150–250), SLO targets, benchmark protocol.
3. `bao-cao-tong-hop-cuoi-cung-ai-infra-24-tuan.md` — final synthesis/decision record arbitrating ChatGPT Deep Research, Gemini Deep Research, and Claude Research reports; decision log of 16 verdicts.

**What transfers unchanged:** the gateway↔engine boundary thesis; mock → llama.cpp → vLLM risk ordering; no broker on the synchronous path; benchmark methodology (open-loop Poisson, goodput@SLO, pooled percentiles, manifests); cancellation as a first-class correctness invariant; fixed gateway SLO targets; GPU cost discipline; paper and source-reading plans; portfolio evidence style ("depth artifact", measured claims only).

**What this program deliberately changes (task-mandated, recorded as deviations):**

| Source position | Program position | Rationale |
|---|---|---|
| One repository (`infergate`) containing loadgen, deploys, benchmarks, docs | Six composable repositories | Program brief mandates composability, independent value per repo, and contract-based integration; the single-repo verdict was driven by a 480-hour calendar cap this program removes |
| 24 weeks × 20 h calendar plan | Dependency-ordered waves, verification gates, no calendar box | Program brief forbids arbitrary time-boxing |
| Capacity planning as a worksheet/report | `fleetlab` simulation repository | Program brief requires an explainable capacity/autoscaling/placement simulator |
| OSS as post-program option | In-scope OSS track with primary + fallback targets | Program brief requires at least one credible contribution |
| No university courses | Selected MIT 6.5840 / CMU 15-445 topics with mandatory engineering artifacts | Program brief requires the study-to-artifact track; the sources' "no full courses, artifact-or-drop" rule is preserved |
| Interview/English/application overlay (~50% of source hours) | Out of scope for repository planning | Not a repository concern; portfolio evidence (articles, demos, README narrative) stays in `inference-lab` |

Consolidation of repositories remains available under explicit triggers (see `10-risk-register.md` §K) and is a **user-review decision**, not an autonomous one.

---

## 5. Priorities

**Mandatory:** shared contracts; `infergate` with mock and llama.cpp paths; `inferbench` with valid methodology; `inference-lab` integration scenarios; streaming/cancellation/retry/overload evidence; one Kubernetes operational path; one benchmark-to-capacity feedback loop (Scenario E / milestone I6); one credible OSS contribution track.

**Reducible:** full multi-tenant policy surface; many autoscaling policies; broad chaos campaign; deep heterogeneous placement; SGLang integration.

**Stretch (separate phase, only if evidence justifies):** PD disaggregation; MTP/speculative decoding experiments; KV offloading; advanced heterogeneous scheduling; multi-cluster/multi-region designs beyond architecture notes.

**Outside baseline entirely:** CUDA kernels, a full agent runtime, production multi-region implementation.

Kill criteria for each tier: `10-risk-register.md`.

---

## 6. Hard constraints (apply to all future execution)

1. Plan and execute by dependency order, verification gates, and integration risk — never by elapsed time.
2. Every repository provides independent user value; integration only via versioned contracts, released artifacts, files, or documented network protocols.
3. Dependency graph stays acyclic; no shared application library; no hidden monolith.
4. One gateway, one load-generation system, one deployment stack.
5. No Kafka, NATS, Redis Streams, or any broker in the synchronous inference request path.
6. The gateway never owns continuous batching, per-token scheduling, KV-cache internals, prefix-cache internals, or GPU placement. (Source-verified basis: vLLM V1's scheduler is a token-budget scheduler with no prefill/decode phase distinction; a second scheduler in the gateway is the "double-queuing" anti-pattern.)
7. No optimization claims without controlled evidence; no comparison across uncontrolled hardware/model/config/workload; invalid runs are invalidated, not published.
8. Basic development and CI for every repository must work without a GPU.
9. Study resources must produce engineering artifacts or be dropped after two sessions.
10. GPU spend requires a written hypothesis and config manifest; instances are auto-stopped; budget alerts are mandatory.

---

## 7. Budget and hardware assumptions

Adopted from source documents (provenance: reported as of 2026-07, volatile — re-verify at execution time; see `13-evidence-assumptions-and-deviations.md`):

- Total GPU rental envelope: **~$150–250** unless the user raises it (user-review item).
- Target rental hardware: single 24 GB-class GPU (RTX 4090 / L4 / A10; A100 80GB only if a specific experiment requires it). Source-reported spot prices: 4090 ~$0.31–0.69/h, L4 ~$0.39/h, A100 80GB ~$0.67–2/h.
- Local/CPU development: llama.cpp with 1–3B GGUF models; deterministic mock backend for everything else.
- GPU models for experiments: 7–8B AWQ/GPTQ checkpoints sized for 24 GB VRAM.
- Contingency: if GPU access fails, llama.cpp becomes the primary measured engine and the portfolio is repositioned around CPU/edge inference plus the mock-backend evidence; GPU experiments compress into one scripted final session.

---

## 8. Governance

- **Authority order for decisions:** program brief > workspace evidence > source documents > general knowledge.
- **Deviation policy:** every repository keeps `docs/implementation-notes.md`; evidence-forced deviations choose the conservative reversible option and are recorded under `Deviations`; pause only for changes to public contracts, repository ownership, security posture, or milestone scope.
- **Evidence rule:** no claim of test/benchmark/deployment success without a command output, file, or trace to point at.
- **Review model:** one human reviewer (the user). Review bottlenecks are planned explicitly in `05-execution-roadmap.md` §7.

## 9. Definition of Done for the program

See `12-success-criteria.md`. The short form: all eight integration milestones (I1–I8) pass their acceptance criteria with published evidence, the OSS minimum target is met, and the portfolio release (quickstart, demo, benchmark report, capacity report, failure-campaign postmortem, OSS evidence) is reproducible by a stranger from a fresh clone.
