# 11 — Traceability Matrix

Three mappings: (1) program-brief requirements → artifacts/tasks/milestones; (2) skills-to-deepen → evidence; (3) source-document decisions → adopted/deviated.

---

## 1. Program-brief requirements → plan artifacts

| Requirement (brief §) | Where satisfied |
|---|---|
| Six-repo baseline ecosystem (§5) | `01`, `02`; prompts 00–05 |
| Responsibility matrix ownership (§5) | `02` §1–2 |
| Project charters detail (§6.1–6.6) | prompts 00–05 (each embeds its charter) |
| Dependency/contract rules, acyclic graph (§7) | `03`; forbidden edges §3 |
| Five shared contracts + versioning (§7) | `04` (Contracts 1–7 incl. the five named + fault + capacity) |
| Study-to-artifact track incl. 6.5840/15-445 artifacts (§8) | `08`; tasks IG-T004/T008/T015/T017/T018 |
| OSS track: candidates, scoring, progression, minimum target, fallback, contingency (§9) | `09`; IL-T010–T012 |
| Required planning files (§10) | this directory; completeness audited in `14` |
| Standalone prompts with docs/ structure + deviation policy (§11) | prompts 00–05 |
| Task schema with stable IDs (§12) | `05` §8 register (71 tasks) |
| Integration milestones I1–I8 with prerequisites/acceptance/evidence/owner (§13) | `07` |
| Dependency-driven roadmap, waves, critical path, gates, GPU fallbacks (§14) | `05` §1–7, §9 |
| Priority tiers + kill criteria (§15) | `00` §5; `10` §2 |
| Planning-only boundary (§16) | `13` §6; verified in `14` |
| Definition of Done (§17) | `12`; audited in `14` |
| No broker in sync path; gateway boundary; one gateway/loadgen/deploy stack (§4) | `00` §6; `01` §2–3; `02` §3; boundary tests `02` §4 |
| No arbitrary calendar duration (§4) | `05` preamble (waves, not weeks) |
| Independent value per repo (§4) | `01` §4 boundary table |
| Controlled-evidence-only claims (§4) | `06` §8; IB-T009; G4 |

## 2. Skills to deepen → planned evidence

| Skill | Evidence path |
|---|---|
| Python for ML-systems tooling | inferbench analysis core (IB-T005/T006), fleetlab (all FL tasks) |
| Inference-engine behavior | IG-T005/T014 adapters; study-track source reading + sequence diagrams; IB-T011 experiments |
| llama.cpp / vLLM / selective SGLang | I3, I4 milestones; IB-T011/T012; capability descriptors |
| GPU memory/capacity/cost reasoning | KV worksheet (FL-T003), capacity/cost reports (FL-T008), benchmark cost metrics |
| Kubernetes operations for inference | inferops IO-T002–T010; I5; I7 |
| Benchmark methodology & statistical validity | IB-T002–T011; G4 gate; report validity blocks |
| Autoscaling & heterogeneous fleet planning | FL-T005–T009; IO-T009; I6 |
| Open-source contribution | `09`; IL-T010–T012; I8 OSS evidence |

## 3. Source-document decisions → adopted / deviated

| Source decision | Status in this plan | Where |
|---|---|---|
| Gateway↔engine boundary inviolable; no gateway batching | **Adopted** (hard rule + boundary tests) | `00` §6, `01` §3, `02` §4 |
| No broker on request path | **Adopted** | `00` §6 |
| Mock → llama.cpp → vLLM risk ordering | **Adopted** (waves 1/2/4) | `05` §1 |
| Retry pre-first-token only; 3-point cancellation; estimate–settle accounting | **Adopted** (IG-T003/T008/T013) | `04` Contract 1; `05` |
| Open-loop Poisson, goodput@SLO+shed-rate, pooled percentiles, manifests | **Adopted** (encoded in schemas) | `04` Contract 3 |
| Fixed gateway SLO targets (overhead p95<10ms, settle ±1%, revoke ≤5s, publish ≤5s, 5×-overload TTFT p95 degrade ≤20%) | **Adopted** as per-repo acceptance criteria (model-level SLOs still set only after measurement) | prompts 01/02; `12` |
| K8s only after behavior is proven; smallest tooling | **Adopted** (Wave 4+; tooling ADR) | `05`, IO-T001 |
| GPU budget ~$150–250, scripted auto-stopped sessions | **Adopted** (pending user confirmation) | `00` §7; `10` §4 |
| SGLang stretch-only with pre-armed fallback | **Adopted** | `10` §2 |
| Single repository (`infergate` monorepo) | **Deviated** — six composable repos (program-brief mandate; calendar cap removed) | `00` §4; `13` |
| 24-week / 480-hour calendar plan | **Deviated** — dependency waves, no time-boxing | `05` preamble; `13` |
| Capacity planning as worksheet/report only | **Deviated** — `fleetlab` simulator (brief mandate), with honesty guardrails (G8, limitations report) | `13` |
| OSS as post-program option | **Deviated** — in-scope track with minimum target | `09`; `13` |
| No university courses at all | **Partially deviated** — selected 6.5840/15-445 topics with mandatory artifacts (brief mandate); artifact-or-drop rule preserved | `08`; `13` |
| Interview/English/application overlay | **Excluded** from repository planning (out of scope for this program) | `13` |
| Agent runtime design note (study exercise) | **Adopted as optional stretch note** (not a milestone) | `08` §7; excluded from baseline scope |
