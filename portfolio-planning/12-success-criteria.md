# 12 — Success Criteria

## 1. Program Definition of Done

The program is done when all of the following hold, each with linked evidence in `inference-lab`:

1. **I1–I8 accepted** per `07-integration-milestones.md`, including the central capacity-feedback loop (I6) and the failure campaign (I7).
2. **Contracts at v1.0.0** with four consumers green and a maintained supported-version matrix.
3. **Correctness evidence set:** 100-concurrent-stream integrity; 3-point cancellation verified on mock, llama.cpp, and vLLM (engine-metrics-verified); automated proof of zero post-first-token retries; crash-recovery test green; config reload under traffic with zero dropped streams.
4. **Overload evidence set:** at ~5× capacity with admission control: accepted-request TTFT p95 degrades ≤20% vs the capacity-boundary baseline; sheds are typed with `Retry-After`; no tenant starvation; noisy-neighbor p95 shift bounded (target <15%).
5. **Gateway SLO targets met and published** (from source-verified targets): non-queue gateway overhead p95 <10ms / p99 <20ms; cancellation propagation p95 <250ms (gateway+mock path); usage settle variance <1% and 100% idempotent by request ID; key revocation ≤5s; config publish ≤5s. Model-level TTFT/ITL/goodput SLOs are declared only from measurement, never in advance.
6. **Benchmark evidence set:** ≥2 reports (CPU overhead/admission; GPU engine behavior) with manifests, pooled percentiles, goodput@SLO with shed rate adjacent, validity + threats-to-validity blocks, reproducible via one command per report.
7. **Capacity evidence set:** fleetlab holdout validation within stated error; autoscaling-signal comparison report; cost/capacity report; recommendation → deployment → re-measurement loop published including prediction-error analysis; simulation-limitations report.
8. **Operations evidence set:** I5 stack; warm-up-aware readiness demonstrated; rolling update under load with zero client errors; 12-scenario campaign matrix (or documented reduced set per kill criteria); ≥2 postmortems; 10 runbooks walked through.
9. **OSS minimum target:** acknowledged reproduction; PR merged or under substantive review; public benchmark/design artifact; documented maintainer interaction — or the documented contingency degradation in `09` §4.
10. **Study track:** all required 6.5840/15-445 artifacts delivered (6 + 5 artifacts, see `08`); every consumed resource maps to a shipped artifact.
11. **Portfolio release:** fresh-clone quickstart ≤15 min (GPU-free path); demo; landing page; 2 articles; honest limitations; reproducibility audit passed — any claim that can't be re-derived from pinned artifacts is removed.

## 2. Per-repository acceptance (summary; detail in each prompt)

| Repo | Accepted when |
|---|---|
| serving-contracts | v1.0.0 released; I1 green ×4 consumers; compatibility policy exercised at least once (one deprecation or migration executed cleanly) |
| infergate | independent mode demo (mock + PostgreSQL, GPU-free); correctness + overload + SLO evidence sets green; released image + descriptors consumed by inferops without source checkout |
| inferbench | methodology gate G4 passed; calibration report; both experiment sets published; works against a non-infergate endpoint (proves independence) |
| fleetlab | G8 holdout gate passed; five required reports published; recommendation consumed by inferops |
| inferops | I5 + I7 accepted; runbooks verified; deploys only released artifacts |
| inference-lab | I2–I8 evidence archived; pins/compatibility matrices current; portfolio release shipped |

## 3. Honest-limitations statement (published at I8, kept current)

The portfolio must state plainly: single-node Kubernetes scale (one GPU node); 1–2 rented GPUs, not fleet-scale production; simulation ≠ production (fleetlab predictions carry stated uncertainty); SGLang/PD-disaggregation at study/benchmark level (if at all); no CUDA/kernel work; multi-region and multi-replica-gateway as design notes only; benchmark numbers valid only for the pinned hardware/model/engine configurations.

## 4. Anti-goals at completion (must NOT exist)

A second load generator, gateway, or deployment stack; broker on the synchronous path; gateway batching/KV logic; unreproducible headline numbers; note-taking artifacts with no consumer; a toy Raft/CUDA project; claims that this planning run executed anything it didn't.
