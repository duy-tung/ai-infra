# 10 — Risk Register and Kill Criteria

Likelihood/Impact: L/M/H. Every risk has an owner repo (or "program"), a trigger, and a mitigation. Kill criteria are pre-decided so scope cuts never happen under pressure.

---

## 1. Risks

| ID | Risk | L | I | Owner | Trigger | Mitigation |
|---|---|---|---|---|---|---|
| R1 | Multi-repo overhead for a single engineer (release/pin churn eats building time) | M | H | program | pin/release bookkeeping dominates a wave; lockstep changes across repos twice in a row | contract-first discipline; consolidation triggers (§K below) as a user-review decision; automation of release/pin mechanics (06 §6) |
| R2 | GPU budget overrun or unavailability | M | H | program | budget alert fires; no GPU by Wave 4 exit | G6 gate (hypothesis+manifest+auto-stop); ≤6 scripted sessions; CPU fallbacks per `05` §5; repositioning contingency from charter §7 |
| R3 | Engine/ecosystem drift (vLLM metric names, EPP repo migration, semconv changes) | H | M | infergate/contracts | conformance or mapping tests fail on a new pin | pin everything; capability metric-name mapping instead of hardcoding; re-verify at G6/IL-T010; dated provenance on all ecosystem facts |
| R4 | Benchmark invalidity (coordinated omission, uncontrolled variables, cherry-picking) | M | H | inferbench | G4 audit failure; validity block incomplete | methodology encoded in schemas + report template; "invalidate, don't publish"; fresh-context audit of every published report |
| R5 | Gateway/engine boundary erosion (batching/KV logic creeping into infergate) | M | H | infergate | boundary tests fail; review finds scheduling logic in gateway | boundary contract tests (study track artifact); hard review rule in `02` §4.4 |
| R6 | OSS latency or rejection | H | M | inference-lab | contingency thresholds in `09` §4 | parallel secondary target; graceful completion degradation; never on critical path |
| R7 | Kubernetes time sink ("YAML exercise") | M | M | inferops | ops work blocks a wave exit without new evidence | smallest-tooling ADR; ops starts only in Wave 4; runbook/probe scope fixed by contract; autoscaling depth is reducible |
| R8 | Contract churn destabilizing consumers | M | M | serving-contracts | >1 breaking change per wave after v0.2 | pre-1.0 rules; consumer kits catch breaks at I1; v1.0 freeze before I6 |
| R9 | Fleetlab drifts into fantasy (models unmoored from measurements) | M | H | fleetlab | holdout validation error exceeds stated bounds; profiles cover hardware never measured | G8 holdout gate; provenance-mandatory profiles; limitations report is a required artifact |
| R10 | SGLang/stretch experiments destabilize the baseline | M | M | inferbench | >4h setup without a running comparison; baseline unstable | pre-armed fallback = vLLM prefix caching on/off; kill order §2 |
| R11 | Single-reviewer bottleneck | M | M | program | review queue blocks two waves | batched wave-exit reviews; decision-ready summaries; deviation policy for reversible calls |
| R12 | Fabrication/overclaiming (numbers without provenance) | L | H | program | any claim lacking a manifest/log | evidence rules (06 §8); reproducibility audit at I8 removes unreproducible claims |
| R13 | Study track decays into note-taking | M | M | program | resource with no artifact after two sessions | artifact-or-drop rule enforced in study tracker |
| R14 | Mock backend fidelity gap (correctness evidence doesn't transfer to real engines) | M | M | infergate | I3/I4 reveal behaviors mock never modeled | mock gains fidelity features only when a real-engine surprise justifies them; llama.cpp arrives early (Wave 2) precisely to bound this |

## 2. Kill criteria (pre-decided cut order)

When a wave exit is threatened, cut in this order — never touch the never-cut list:

1. SGLang comparison (fallback: vLLM prefix caching on/off) — also killed if: >4h setup without a running benchmark, GPU budget ≥80% consumed, or vLLM baseline unstable.
2. Speculative decoding / MTP / KV-offloading experiments (IB-T012).
3. KEDA/autoscaling breadth (keep one HPA experiment + fleetlab simulation).
4. Heterogeneous-placement depth (FL-T007 reduces to two hardware profiles).
5. Chaos breadth (12 scenarios reduce to the streaming-critical 6: 1, 2, 5, 6, 11, 12 — with documented deviation).
6. Multi-tenant policy breadth (keep 2 tiers + fairness evidence).

**Never cut:** cancellation correctness, fault-injection evidence (some campaign must run), methodologically valid benchmarking, contract validation, the I6 feedback loop (it may shrink to mock/llama.cpp scale but must close).

**PD disaggregation (stretch) is postponed when:** two suitable GPUs are unavailable, methodology can't isolate the effect, KV transfer can't be observed, or the result would be configuration theater.

**Generic drop rule:** drop or postpone any work item that blocks the critical path without producing new evidence, duplicates an existing capability, requires an overlapping framework, lacks a measurable artifact, exceeds GPU budget, creates tight source coupling, or can't be explained and reviewed by the user.

## 3. §K — Consolidation triggers (user-review decision, never autonomous)

Consolidate two repositories only when at least one holds:

1. A repository demonstrably lacks independent value (boundary test `02` §4.1 fails at two consecutive wave exits).
2. Lockstep source changes across two repos are unavoidable for two consecutive milestones despite contract fixes.
3. Shared internal code is the only workable integration mechanism (contract/artifact exchange demonstrably insufficient).
4. Maintenance cost clearly exceeds learning value (documented time evidence).

Likeliest candidate pairs if triggered (pre-analysis): `serving-contracts` folding into `inference-lab` (both are coordination repos) or `fleetlab` folding into `inferbench` (producer/consumer of the same files). Either consolidation is presented to the user with evidence; the responsibility matrix is updated before any code moves.

## 4. GPU budget guardrails (restated as risk controls)

- Envelope ~$150–250 (user-confirmable); alert at 50% and 80%.
- Only IG-T014, IB-T007/T011/T012, IO-T005, IL-T004/T006/T007 may spend GPU time; each session pre-registered (hypothesis + manifest) and auto-stopped.
- Any hypothesis-less GPU run is stopped immediately (source-document discipline preserved).
