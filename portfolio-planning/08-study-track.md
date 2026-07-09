# 08 — Study-to-Artifact Track

Governing rule (preserved from all three source documents): **no resource is consumed for its own sake.** Every selected resource has a consuming project, an exact artifact, a relevance threshold, a stop condition, and a duplication check. A resource that produces no artifact after two sessions is dropped. There is no generic Raft project and no full-course completion anywhere in this track.

Provenance note: the source documents contain the paper list, source-reading plans, and point resources below. The MIT 6.5840, CMU 15-445, and book selections are program-brief requirements not present in the sources; they are scoped here in the same artifact-or-drop style. "AI Engineering from Scratch" was named as a companion by the program brief but **no copy exists in the workspace** — its entries are conditional on the user providing it (see `13-evidence-assumptions-and-deviations.md`).

---

## 1. MIT 6.5840 (selected topics only — no full course, no Raft lab in baseline)

Selected topics: RPC semantics, at-most-once behavior, linearizability, fault tolerance, cache consistency, task scheduling, invariant reasoning.

| Required artifact | Consuming repo/task | Relevance threshold | Stop condition |
|---|---|---|---|
| API-key revocation consistency ADR (staleness bounds of snapshot-based revocation; at-most-once admin semantics) | infergate / IG-T015 | must change the revocation design or its tests | ADR approved |
| Tenant-config consistency ADR (snapshot propagation vs read-your-writes for admins) | infergate / IG-T015 | must produce a testable consistency statement | ADR approved |
| Usage-settlement invariants (exactly-once *effect* via idempotent settle; duplicate/reorder cases enumerated) | infergate / IG-T008 | each invariant maps to a test | invariants tested |
| Multi-gateway scaling design (state partitioning, quota semantics across replicas — design note only) | infergate / IG-T015 | must state what breaks at N>1 and the chosen consistency trade-offs | note reviewed |
| Stale-health-snapshot experiment (quantified routing impact of stale signals) | infergate / IG-T017 | hypothesis + controlled experiment | report published |
| Fault-state machine (request lifecycle states incl. all failure/cancel edges) | infergate / IG-T017 | machine covers the full error taxonomy | diagram + tests aligned |

Optional micro-lab (MapReduce or KV) only if a demonstrated gap appears in the above (e.g. invariant reasoning proves weak); duplication check: none of these duplicates engine or K8s behavior.

## 2. CMU 15-445 (selected topics only)

Selected topics: concurrency control, MVCC, logging, crash recovery, distributed databases.

| Required artifact | Consuming repo/task | Relevance threshold | Stop condition |
|---|---|---|---|
| Versioned configuration-snapshot model (MVCC-flavored snapshot semantics doc) | infergate / IG-T004 | informs snapshot/versioning implementation | doc merged with ADR |
| Append-only usage ledger design | infergate / IG-T008 | write-path + compaction/retention stated | design implemented |
| Idempotent recovery design | infergate / IG-T018 | recovery cases enumerated | design tested |
| Crash-recovery integration test | infergate / IG-T018 | test kills the gateway mid-traffic | test green in CI |
| Transaction-boundary ADR (what is/isn't transactional between snapshot store, ledger, and quota state) | infergate / IG-T018 | boundaries explicit | ADR approved |

## 3. Papers (from source documents; deep-read vs skim as marked)

| Paper | Depth | Artifact | Consumer | Stop condition |
|---|---|---|---|---|
| PagedAttention (SOSP'23) | deep (§1–4, §6.1–6.2; skip kernels) | KV-cache memory worksheet feeding the fleetlab memory model + overload-signal notes | fleetlab FL-T003; infergate routing | worksheet cross-checked vs measured memory |
| Orca (OSDI'22) | deep (§1–3) | "Why the gateway must not batch" ADR basis | infergate ADR; article #1 | ADR approved |
| Sarathi-Serve (OSDI'24) | medium | `max_num_batched_tokens` TTFT/ITL trade-off hypothesis | inferbench IB-T011 | experiment run |
| DistServe (OSDI'24) | medium | goodput@SLO definition + when-to-disaggregate decision tree | contracts metric vocabulary; fleetlab; stretch notes | definition encoded in schemas |
| SGLang/RadixAttention (NeurIPS'24) | medium | shared-prefix workload design + hash-block vs radix comparison note | inferbench workloads; stretch comparison | workload designed |
| Mooncake (FAST'25) | medium | early-rejection lineage note for admission control | infergate IG-T010 ADR context | note done |
| FlashAttention (2022) | skim | HBM/SRAM IO-aware note ("reduces HBM traffic, not FLOPs") | study notes; interview depth | note done |
| Pope et al., Efficiently Scaling Transformer Inference | skim | capacity-math worksheet backbone | fleetlab FL-T003 | worksheet used |
| Goodput-critique (arXiv 2410.14257) | skim | stall-rate-beside-goodput reporting rule | inferbench report template | rule encoded |
| Speculative decoding (Leviathan et al.) | skim (stretch) | one-page mechanism note; hypothesis if IB-T012 runs | inferbench stretch | note done |

## 4. Engine source reading (artifact-first, path-pinned; commits re-verified at execution)

| Target | Artifact | Consumer | Stop condition |
|---|---|---|---|
| vLLM V1 (`vllm/v1/engine/async_llm.py`, `core.py`, `vllm/v1/core/sched/scheduler.py`, `kv_cache_manager.py`, entrypoints) | "Life of a streaming request in vLLM V1" sequence diagram + 2-page `Scheduler.schedule()` annotation + **3 contract tests preventing gateway batching logic** (boundary tests) | infergate adapter + boundary tests; study evidence | diagram + tests exist |
| llama.cpp `tools/server/` | slot-model vs token-budget note + `-np` parallelism experiment | infergate adapter; I3 | note + experiment done |
| Gateway API Inference Extension + llm-d (EPP scorers: queue depth, KV utilization, prefix/LoRA affinity) | "infergate router vs EPP" comparison + routing-signal design review | infergate routing ADR; OSS track | comparison published |
| SGLang scheduler + radix cache (read-only) | vLLM-vs-SGLang caching comparison 1-pager | stretch experiment design | 1-pager done |
| LiteLLM (product docs only) | accurate "Why not LiteLLM?" related-work section | inference-lab portfolio | section written |

Reading rule: follow one HTTP request's execution path; pin the commit; `git log -- <path>` before reading (paths drift). Do-not-read-deeply list: Triton/TensorRT-LLM, TGI (archived 2026-03), Ray Serve/KServe controllers, Kubernetes scheduler internals, CUDA kernels.

## 5. Books (program-brief additions; chapter-selective, artifact-or-drop)

| Book | Selected material | Artifact | Consumer | Stop condition |
|---|---|---|---|---|
| Designing Data-Intensive Applications | consistency, replication, transactions chapters | inputs to IG-T015/T018 ADRs (cited, not summarized) | infergate | ADRs approved |
| Systems Performance (Gregg) | methodology + latency analysis chapters | benchmark-methodology review checklist addition; one USE-method pass over gateway under load | inferbench G4; infergate | checklist merged |
| Google SRE | "Handling Overload", cascading failures, retry budgets | admission/retry-budget ADR + runbook review lens | infergate IG-T010/T013; inferops runbooks | ADR approved |
| Database Internals | storage/recovery chapters | ledger + recovery design inputs | infergate IG-T018 | design tested |
| AI Engineering (Huyen) | serving/inference chapters | capacity-report structure review; gap check vs fleetlab reports | fleetlab | review note done |
| Computer Architecture: A Quantitative Approach | memory-hierarchy + accelerator chapters (skim) | GPU-literacy note (bandwidth vs FLOPs reasoning) feeding hardware profiles | fleetlab | note done |

Duplication check: books never produce standalone summaries — only inputs to artifacts already in the register.

## 6. AI Engineering from Scratch (conditional — source not in workspace)

If provided by the user, index it as a companion for: inference economics, autoscaling, vLLM/SGLang internals, metrics, gateways, load testing, chaos, FinOps, serving stacks, orchestration, kill switches, circuit breakers — mapped chapter-by-chapter to the same consuming tasks as above with the same artifact-or-drop rule. Until then, no entries claim it.

## 7. Point resources

- OTel GenAI semantic conventions (pin version; status "Development" as of 2026-07) → contracts trace-attribute section (SC-T005).
- Kubernetes "Schedule GPUs" docs → inferops GPU-node profile (IO-T005).
- Modal GPU Glossary / vLLM docs (V1 guide, metrics design, optimization) → capability mapping (IG-T014) + fleetlab profiles.
- Engineering postmortems and blogs (e.g. published provider incident reports) → postmortem format for I7 (with the "quality regressions can pass latency SLOs" caveat noted in the SLO doc).
