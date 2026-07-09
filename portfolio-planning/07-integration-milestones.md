# 07 — Integration Milestones

Integration milestones are separate from per-repository milestones (which live in each repository's `docs/milestones.md`, seeded by the prompts). Each defines: prerequisites, version pins, acceptance criteria, future commands (**to be executed in future runs — nothing here was executed in this planning run**), failure handling, evidence, and owner.

Common rules: every milestone runs against pinned released artifacts recorded in the `inference-lab` pins file; evidence is archived in `inference-lab`; a milestone is "accepted" only when its acceptance criteria are demonstrated and reviewed.

---

## I1 — Contract compatibility

**Owner:** serving-contracts. **Prerequisites:** SC-T009 (bundle v0.1.0), consumer CI wiring in all four consumer repos. **Pins:** contracts v0.1.0.
**Acceptance:** all four consumers (infergate, inferbench, fleetlab, inferops) validate the golden fixtures and their own emitted artifacts against the bundle in CI; unsupported-field rejection cases covered.
**Future commands (indicative):** `make contracts-verify` in each consumer repo.
**Failure handling:** fixture mismatch → fix consumer or file a contract defect; contract defect → PATCH release, re-run I1.
**Evidence:** four green CI runs referencing the same bundle tag, linked in the pins file.
**Re-run trigger:** every contract release (I1 is re-entrant; v1.0.0 re-run is a prerequisite for I6).

## I2 — Local request path

**Owner:** inference-lab. **Prerequisites:** IG-T003 (streaming+cancellation), IB-T004, IL-T001; contracts v0.1.x. **Pins:** contracts, infergate image, mock image, inferbench version.
**Acceptance:** `inferbench → infergate → mock backend` runs a seeded workload: 100 concurrent streams, zero frame mixing; 3-point cancellation verified (mock abort observed within bound); raw events schema-valid; client-vs-gateway TTFT agreement within declared tolerance; traces/metrics visible (Scenario A includes PostgreSQL usage write + OTel).
**Future commands (indicative):** `docker compose up` in inference-lab scenario A; `inferbench run --workload chat-short --seed 42 --target http://infergate...`.
**Failure handling:** frame mixing or cancellation leak → stop, fix in infergate, re-run; measurement disagreement → check measurement-point definitions before touching code.
**Evidence:** run logs, raw-event files, trace export, acceptance checklist.

## I3 — Local inference

**Owner:** inference-lab. **Prerequisites:** I2; IG-T005; IB-T006. **Pins:** + llama.cpp commit + GGUF model revision.
**Acceptance:** `inferbench → infergate → llama.cpp` completes `chat-short` and `shared-prefix` workloads on CPU; first schema-valid benchmark report generated (with manifest + validity block); cancellation verified against llama.cpp; failover mock↔llama.cpp demonstrated.
**Future commands (indicative):** scenario B compose file; `inferbench report --run <id>`.
**Failure handling:** llama.cpp behavioral surprises → capability descriptor updated, adapter fixed; report invalid → G4 review before proceeding.
**Evidence:** benchmark report #0 (methodology shakedown), campaign logs.

## I4 — GPU inference

**Owner:** inference-lab. **Prerequisites:** I3; IG-T014; G6 (hypothesis + manifest + auto-stop + budget alert); IB-T011 first session. **Pins:** + vLLM version/commit, model checkpoint + quantization, driver/CUDA, instance type.
**Acceptance:** `inferbench → infergate → vLLM` on a rented GPU: streaming + cancellation verified via engine metrics (KV usage / running-count drop within bound); gateway-overhead comparison (direct vs via-gateway) measured with ≥3 runs/point; session auto-stopped; all artifacts carry the full manifest.
**Future commands (indicative):** GPU session runbook script; `inferbench sweep --target ... --rates ...`.
**Failure handling:** engine metric names drift → update capability mapping, re-verify; budget trip → stop, record, fall back per §5 of `05-execution-roadmap.md`.
**Evidence:** session log, benchmark report #1 (GPU), cancellation-verification metrics export.
**CPU fallback:** documented deviation; llama.cpp variant becomes the measured baseline.

## I5 — Operational stack

**Owner:** inferops. **Prerequisites:** I4 (or its recorded fallback); IG-T016; IO-T002–T005. **Pins:** + inferops release, dashboard/config bundle versions.
**Acceptance:** `inferops → infergate → vLLM → OTel/Prometheus/Grafana/Tempo` on the local cluster + GPU node: deployment from released images only (no source checkout); warm-up-aware readiness demonstrated; rolling update under load with zero client-visible errors; golden dashboards live; traces end-to-end.
**Future commands (indicative):** `kubectl apply -k ...` per inferops runbook; scripted rolling-update test.
**Failure handling:** probe/drain violations → fix manifests or deployment contract (contract change ⇒ re-run I1); observability gaps → dashboard/collector fix.
**Evidence:** manifests, smoke outputs, dashboard exports, rolling-update test log.

## I6 — Capacity feedback (the central story)

**Owner:** inference-lab (loop), fleetlab (recommendation). **Prerequisites:** I5; FL-T009; IO-T009; contracts v1.0.0 (SC-T010); benchmark corpus from IB-T010/T011. **Pins:** everything above + fleetlab release.
**Acceptance:** benchmark results → fleetlab produces a schema-valid capacity recommendation (with stated uncertainty) → inferops applies the recommended change (replica count / config) → repeated benchmark measures the outcome → predicted vs measured compared and published, including where the prediction was wrong.
**Future commands (indicative):** `fleetlab recommend --results ... --slo ... --cost ...`; inferops apply; `inferbench` re-run.
**Failure handling:** prediction badly off → that is a *result*, not a failure — publish the error analysis and refine profiles (G8); loop mechanics broken → fix contract 7 plumbing.
**Evidence:** the loop report (recommendation file, applied manifests, before/after benchmark results, error analysis).

## I7 — Failure campaign

**Owner:** inferops (execution), inference-lab (evidence). **Prerequisites:** I5; IO-T006/T007; fault-scenario contract. **Pins:** frozen component set for the campaign.
**Acceptance:** all 12 contract fault scenarios injected (GPU-dependent ones may run on the llama.cpp/mock path with a recorded deviation); for each: expected gateway semantics observed or deviation documented; client impact measured by inferbench for at least the streaming-critical scenarios (1, 2, 5, 6, 12); ≥2 postmortems published in the standard format (timeline from real metrics, detection gap, root cause, mitigation, action items).
**Future commands (indicative):** `inferops faults run --scenario <id>` per runbook.
**Failure handling:** semantics mismatch → gateway defect or spec defect; fix, re-run scenario; repeated flakiness → scenario marked unreliable with analysis.
**Evidence:** campaign matrix (12 rows: injected / observed / verdict), postmortems, client-impact measurements.

## I8 — Portfolio release

**Owner:** inference-lab. **Prerequisites:** I1–I7 accepted; OSS minimum target met or contingency documented; IL-T009.
**Acceptance:** fresh-clone quickstart reproduces Scenario A in ≤15 minutes on a GPU-free machine; demo script + recorded demo; benchmark report(s) and capacity report published with validity blocks; failure-campaign evidence linked; OSS evidence (public links) recorded; compatibility matrix current; reproducibility audit passed (a fresh session can re-derive every headline claim from pinned artifacts); honest limitations section published.
**Failure handling:** any headline claim that cannot be reproduced is removed or re-measured — no exceptions.
**Evidence:** release tag of inference-lab + the audit checklist.
