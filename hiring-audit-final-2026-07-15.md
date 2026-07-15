# Evidence-Backed Hiring Audit

## Backend Engineer → AI Infrastructure / Platform Engineer

**Audit date:** 2026-07-15
**Revision:** 3 — combined audit, reconciled against the user-supplied second report on 2026-07-15, then **independently re-verified on 2026-07-15** against live GitHub state and fresh full clones at the audited HEADs (all raw-number recomputations reproduced exactly; corrections applied in this revision are listed in Appendix C)
**Mode:** read-only, adversarial portfolio review
**Repositories:** `serving-contracts`, `infergate`, `inferbench`, `fleetlab`, `inferops`, `inference-lab` under `github.com/duy-tung`
**Evidence standard:** raw artifacts → generators/tests → reachable implementation → executed delivery evidence → narrative documents
**Decision scope:** the repositories alone. Prior backend experience, private work, and unlinked external validation are excluded.

---

## 0. Executive verdict

This portfolio makes a **credible mid-level transition case for inference reliability / release / developer-productivity work (family B)** and a **borderline-to-credible adjacent case for model-serving platform work (family A)**. It does **not** currently demonstrate inference-runtime/performance engineering (family C) or GPU/Kubernetes infrastructure engineering (family D).

The strongest evidence is not "AI" in the accelerator sense. It is backend/platform engineering applied thoughtfully to an inference-shaped system: a reachable Go request path, correct pre-first-token retry boundary, SSE relay and cancellation handling, bounded admission, an open-loop benchmark harness, raw measurements, a fault campaign, and unusually candid negative results. The decisive limitations are equally clear: CPU-only `llama.cpp`; no vLLM/SGLang; no GPU; no real pod scheduling or autoscaling controller; one host; mock-backed capacity fitting; no executed six-replica recommendation; no production users or external review.

The most accurate one-line synthesis from both audits is: **methodologically strong, substrate-poor**. The second report materially strengthened the raw-evidence census and exposed additional presentation/CI problems, but it did not change the role-family verdict or scores.

There are also material claim-integrity defects:

- No public repository has any Git tag. The advertised `inference-lab@v1.0.0` cannot be resolved; only a mutable `release/v1.0.0` branch exists. (Fairness context: the repositories publicly disclose the cause — known issue **KI-1**, "the session git proxy drops tag pushes," stated in `serving-contracts` `RELEASES.md` and `inference-lab` `pins/pins.yaml` — and designate `release/<version>` branches as the pinnable remote refs. That mitigates intent, not the defect: the headline release wording below remains wrong as written.)
- `FINAL-REPORT.md` claims `v1.0.0@b940f5c`, but that file was introduced later at `c5cf6b7`; it did not exist at `b940f5c`, and it carries no KI-1 caveat.
- "Deployed and operated on Kubernetes" is false under ordinary hiring semantics: the API server accepted manifests, but no kubelet/scheduler ever ran a workload pod.
- "Warm-up-aware readiness" is not implemented in the gateway readiness endpoint. `/readyz` reports drain state only; the warm-up script checks backend health separately.
- The N-backend P2C router exists and is tested as a library, but the shipped command constructs exactly one backend and file configuration cannot construct the router. It is not a launchable multi-backend gateway.
- The slow-client experiment failed to observe deadline closure, but did not prove the server was blocked on a write. Calling the result a confirmed product defect is stronger than the evidence.

### Reconciled portfolio-alone scores

| Role family | Mid-level | Decision | Senior | Decision | Bottom line |
|---|---:|---|---:|---|---|
| A. AI Platform / Model Serving Platform | **6/10** | MAYBE | **4/10** | NO | Real gateway/platform mechanics, but single-backend launch path, false readiness claim, one host, and no real serving fleet |
| B. Inference Reliability / Release / Dev Productivity | **7/10** | SHORTLIST | **5/10** | MAYBE | Best fit: good benchmark discipline, fault work, CI on one repo, raw negative results; release and cross-repo delivery remain thin |
| C. Inference Runtime / Performance | **4/10** | NO | **2/10** | NO | Useful measurement adjacency, but no engine internals, GPU profiling, batching/KV work, kernels, or distributed execution |
| D. GPU / Kubernetes Infrastructure | **2/10** | NO | **1/10** | NO | Manifests and API validation only; no workload scheduling, device plugin, GPU Operator, controller loop, node failure, or multi-node work |

**Blunt answer:** yes, the portfolio makes the Backend → AI Infrastructure transition credible **if the target is qualified to mid-level inference reliability or serving-platform-adjacent backend work**. It does not justify an unqualified runtime, GPU, Kubernetes, or senior AI-infrastructure claim.

### Reconciliation with the supplied second audit

The supplied text ends at the heading for its role-fit section, so this revision merges and checks all content actually provided: executive verdict, snapshots, CI/tests, raw-number recomputations, claim consistency and presentation surface. Its narrative is not treated as independent evidence; claims were rechecked against the locked clones or live GitHub state.

| Supplied-audit claim | Combined finding | Resolution |
|---|---|---|
| "105 of 106 commits are authored by Claude" | Main histories contain **119 commits**; **117** have author name `Claude`, one is `duy-tung`, and one is `inferops` with an Anthropic noreply address; 97 commits also carry AI co-author trailers | **FALSE and internally inconsistent** with the supplied report's own per-repo counts (which sum to 119). Re-verified 2026-07-15: all four figures exact |
| All suites pass; fleetlab 297 passed, 4 skipped | Python 3.12.13 rerun: inferbench 103/103 passed; contracts green; fleetlab **296 passed, 1 failed, 4 skipped** | **ENVIRONMENT-DEPENDENT — both reports are right in their own interpreters.** The failure is a one-ULP exact-float equality (`8.489426933050082 != 8.489426933050083`) that fires **only under Python 3.12** (CPython 3.12 switched float `sum()` to Neumaier compensated summation, gh-100425); under Python 3.11 the suite passes 297/0/4. The defect is the brittle exact-equality assertion, not the model |
| Nine infergate Actions runs, all successful | GitHub Actions API reports exactly 9 push runs and 9 successes; the workflow uses real PostgreSQL and explicitly runs crash recovery | **VERIFIED** (workflow name is `ci`, lowercase) |
| I2 proves max 154 concurrent streams and zero frame mixing | Raw events verify max 154, 2,736/2,736 `ok`, and zero token-count/ITL-length invariant violations | **NARROWED.** That invariant does not identify cross-stream content; actual no-mixing identity evidence is the separate infergate 100-stream self-test |
| Sub-millisecond three-point cancellation deltas | Recomputed min/median/max: 0.247/0.398/0.573 ms; 0.310/0.413/0.724 ms; 0.318/0.367/0.638 ms | **ARITHMETIC VERIFIED, CAUSAL CLAIM PARTIAL.** Events and aborts have no shared request ID (abort records carry only `{at_unix_nano, chunks_sent, phase}`) and are greedily timestamp-paired; near-completion leaves one canceled event unmatched |
| Scenario 4 is a "real defect" | An eight-second reader stall did not visibly close the bounded stream under a three-second setting | **OVERSTATED.** It is a real failed acceptance observation; the test did not show a blocked server write, buffer growth, or distinguish kernel buffering from an implementation defect |
| Failover: 142-second outage, zero client failures | Timeline is 141.682 s; total run has 27 `ok` and **one typed `upstream_error` at the kill**; all 12 requests issued during the outage are `ok` via mock failover | **NARROWED.** Zero failures during the post-kill outage window, not zero failures across the failover event |
| fleetlab recommendation regenerates byte-identically | In-memory `build_recommendation()` serialization exactly matches committed SHA-256 `85e5d972…`; six replicas and [165.279, 189.036] rps interval reproduce | **VERIFIED** (reproduced on both Python 3.11 and 3.12), still mock/linear/unexecuted |
| Quickstart timings and crash transcript are raw evidence | Quickstart contains only a prose timing table; crash results are pasted prose, while current CI independently executes the mechanism | **NARROWED.** Useful records, not machine-produced raw artifacts |
| Four repos lack README; all six have blank descriptions, 0 stars/forks, and were created within 14 seconds | Verified through file trees and GitHub repository API (23:57:44–23:57:58Z on 2026-07-10) | **VERIFIED**; material 10–15-minute presentation weakness |

---

## 1. Method and evidence labels

The two requested reviewer passes were completed independently and sealed before reconciliation. They examined the same fixed snapshots but used different hiring lenses. No finding from one pass was supplied to the other before both verdicts were recorded. A third, fully independent re-verification pass (2026-07-15, Python 3.11.15 / Go 1.24.7, reimplemented recomputation code rather than reruns of the portfolio's scripts) reproduced every quantitative and forensic claim in this document except the corrections recorded in Appendix C.

This report uses three labels:

- **VERIFIED FACT:** directly observed in a public ref, source path, raw artifact, test, workflow result, or recomputation.
- **INFERENCE:** a reasoned conclusion from verified facts that was not itself reproduced; interviewers should probe it.
- **UNVERIFIED CLAIM:** portfolio wording for which the required execution artifact, representative substrate, immutable ref, or independent validation was not found.

Capability scores follow the requested 0–4 model. "Representative" means representative of the hiring claim, not merely internally consistent with a CPU/mock/Compose experiment.

### Bounded verification performed during this audit

| Repository / check | Snapshot | Environment | Result |
|---|---|---|---|
| `python3 pins/validate_pins.py` | `inference-lab@bb0c253` | Python 3.12.13, local read-only checkout | PASS: 28 artifact entries and 3 seed entries (reproduced on 3.11) |
| `python kit/contracts-validate.py selftest` | `serving-contracts@507208b` | Python 3.12.13; jsonschema 4.26.0; PyYAML 6.0.3 | PASS: 12 schemas meta-valid, 52/52 positives, 29/29 negatives fail as required (reproduced on 3.11) |
| `go vet ./...`; `go test -race ./...` | `infergate@f362ceb` | Go 1.24.7 linux/amd64; isolated caches; no local PostgreSQL/llama server | PASS: **16** tested internal packages race-clean (corrected from 17 — see Appendix C); DB/llama-gated cases self-skip locally (33 skips observed on re-run). Public CI supplies PostgreSQL and runs the crash test |
| `go vet ./...`; `go test ./...` | `inferbench@62c2704` | Go 1.24.7 linux/amd64; isolated caches | PASS: 11/11 packages |
| `PYTHONPATH=src CONTRACTS_BUNDLE=… python -m pytest -q -p no:cacheprovider` | `inferbench@62c2704:analysis` | Python 3.12.13; pytest 9.1.1; numpy 2.5.1; jsonschema 4.26.0 | PASS: 103/103 (reproduced on 3.11) |
| `python -m pytest -q -p no:cacheprovider` | `fleetlab@dd05e7d` | same isolated Python environment | **Python 3.12: 296 passed, 1 failed, 4 skipped. Python 3.11: 297 passed, 0 failed, 4 skipped.** The failure is a one-ULP exact-float equality (`8.489426933050082 != 8.489426933050083`) in `test_cold_start_headroom_illustrative_scenario_shows_the_mechanism`, triggered by CPython 3.12's Neumaier float-`sum()` change (gh-100425) acting on `dynamics/cold_start.py`'s mean — a brittle portability assertion rather than a model failure; four full-corpus tests skip because they hard-code absent `/home/user/{inferbench,inference-lab}` sibling paths |
| Headline E1 recomputation | `inferbench@62c2704` raw JSONL | Read-only Python calculation | PASS: n=630 paired requests; p50 +1.0386 ms, p95 +2.2075 ms, p99 +2.8135 ms; output matched the committed result (independently re-reproduced to float precision, including the 65/630 negative-delta count) |

Dependencies and Go were installed only under `/tmp`; bytecode/cache writes were disabled or redirected outside the repositories. All six worktrees were clean after verification. No issue, comment, pull request, cloud resource, or paid infrastructure was created.

---

## 2. Independent reviewer pass 1 — Hiring Manager

### Decision before staff-engineer reconciliation

| Role family | Mid | Senior | Recruiter/technical decision |
|---|---:|---:|---|
| A. Serving platform | 7 | 5 | Recruiter screen and mid-level technical interview |
| B. Reliability / release / dev productivity | 7 | 5 | Recruiter screen and mid-level technical interview |
| C. Runtime / performance | 3 | 1 | No, unless the role is explicitly benchmark-tooling adjacent |
| D. GPU / Kubernetes | 2 | 1 | No |

### What is visible in a realistic 10–15 minute review

**Positive signal:** the landing page quickly exposes real limitations, measured numbers, raw evidence paths, and failed hypotheses. The gateway, benchmark methodology, capacity loop, observability stack, and fault campaign form a coherent story rather than six unrelated toy APIs. `inference-lab@bb0c253:portfolio/README.md#Three measured claims` and `portfolio/limitations.md#Honest limitations` are unusually candid for a personal portfolio.

**Negative signal:** the same quick review also encounters "production-grade," an advertised but unresolvable release tag, "deployed and operated on Kubernetes" beside an admission that no pod ran, and a sprawling six-repository documentation surface. Four component repositories have no root README; all six have blank GitHub descriptions, zero stars and zero forks, and were created within 14 seconds. Only `infergate` has GitHub Actions. This creates a credibility tax before an interviewer reaches the strongest code.

### Hiring-manager interpretation

- **Relevance:** high for platform/reliability-adjacent backend roles; low for runtime/GPU roles.
- **Credibility:** moderate. Raw evidence and limitations help; overbroad headings and release inconsistencies hurt.
- **Differentiation:** stronger than a typical CRUD/backend portfolio because the candidate measured and falsified serving-system hypotheses.
- **Scope:** substantial personally, but single-host and self-generated. It is not organizational or production scope.
- **CV framing:** the project should be sold as an **experimental CPU LLM-serving gateway and reliability lab**, not as a production AI platform.

**Hiring-manager recommendation:** interview for mid-level B and selected A roles, provided the CV carries CPU/single-host/Compose qualifiers and removes Kubernetes/GPU/production wording.

---

## 3. Independent reviewer pass 2 — Skeptical Staff Engineer

### Decision before hiring-manager reconciliation

| Role family | Mid | Senior | Technical decision |
|---|---:|---:|---|
| A. Serving platform | 6 | 4 | MAYBE / NO |
| B. Reliability / release / dev productivity | 7 | 5 | SHORTLIST / MAYBE |
| C. Runtime / performance | 4 | 2 | NO / NO |
| D. GPU / Kubernetes | 2 | 1 | NO / NO |

### Findings most likely to surface in interview

1. **The advertised multi-backend router is not a shipped configuration path.** `infergate@f362ceb:cmd/gateway/main.go#main` builds `route.NewRouter` with one `BackendSpec` (the in-code comment itself concedes "internal/route is not yet flag-driven for N>1, a recorded scope reduction"). `internal/config/store.go#buildBackend` can build one adapter plus static fallback, not an N-node `route.Router`. Router tests prove a library, not an operable multi-backend deployment.
2. **Readiness is drain-only.** `infergate@f362ceb:internal/gateway/gateway.go#handleReadyz` never checks backend/model/DB health (its own doc comment: "Warm-up-aware readiness is IG-T016" — never shipped). `inferops@89871a6:scripts/warmup-readiness-test.sh#Verdicts` polls the backend `/healthz` and a metric but never asserts gateway `/readyz==false`. Kubernetes probes point at gateway `/readyz`, so the written warm-up-ready claim is not demonstrated.
3. **The slow-client root cause is unresolved.** `inferops@a07fd2f:faults/scenario-04/verdict.md` (Parts A/B and Verdict; the summary "Observed" cell lives in `faults/campaign-matrix.md`, scenario-4 row) shows the socket stayed open after an eight-second reader stall with a three-second configured deadline. The response was bounded and small enough for kernel buffering; the evidence never shows the server blocked in `stream.Relay.writeEvent`, and the verdict itself concedes the campaign "could not tell which without adding instrumentation to infergate itself." This is a failed acceptance observation, not proof of a deadline implementation defect.
4. **Admission slot leak — CODE-CONFIRMED PATH, not runtime-reproduced.** In `infergate@49236a3:internal/admission/admission.go#Manager.Admit`, cancellation can win the caller select after the dispatcher has removed a ticket, incremented `globalInFlight`, and buffered a grant. `cancelWaiting` then finds nothing, never drains the buffered grant, never decrements, and no returned `Ticket` exists to release the slot. Code reading confirms no drain path exists on the cancel side (the in-code comment calling the unread buffered value "harmless" is false for grant results), and the code is byte-identical at release and main. Existing tests do not force that interleaving; the leak has not been reproduced at runtime.
5. **"Zero frame mixing" is evidenced by a gateway self-test, not by the I2 checker cited for the composed run.** `inference-lab@b940f5c:scenarios/a/checks.py#cmd_integrity` checks statuses and token/ITL counts, not stream identity/content (composed events carry no content at all). `infergate@49236a3:internal/stream/acceptance_test.go#TestConcurrentStreamsNoFrameMixing` does check distinct IDs/content across 100 streams.
6. **Cancellation timing has weak causal attribution.** The scenario scripts greedily pair timestamp-only abort events rather than joining by request ID (abort records carry only `{at_unix_nano, chunks_sent, phase}`). The aggregate evidence supports cancellation propagation and resource release; sub-millisecond per-request causal deltas are not robustly proven.
7. **The benchmark core is the best technical work.** `inferbench@62c2704:internal/schedule/schedule.go#Build`, `internal/run/run.go#Execute`, and `analysis/.../percentiles.py#pooled_table` implement seeded response-independent open-loop scheduling, scheduled-send latency, slip detection, raw pooling, and goodput denominators that include shed/error/cancel outcomes. The bootstrap resamples individual requests rather than run clusters, so its interval can understate temporal/run correlation.
8. **Admission gate G5 failed its original criterion twice.** `inference-lab@b940f5c:reports/benchmark-report-1.md#Gate G5` records +25.16% against ≤20%; `benchmark-report-1b.md#Gate G5 follow-up` records +26.08%. The ≤20% criterion is genuinely pre-declared in a committed hypothesis file (`inferbench:hypotheses/EXP-ib-t010-e2-admission-value.json`). Reframing the gate around typed shedding and bounded wait is reasonable governance, but it is not validation of the original performance claim.
9. **The capacity model is mechanics evidence, not serving-capacity validation.** It uses a deterministic mock. The source two-point profile misses the holdout by 12.6%; E2b ranges from −17.0% to +20.4%. The six-replica result is extrapolated, has only 5.2% point headroom at the upper demand, fails N−1, and was never executed. An A10G price is applied to mock CPU throughput only to populate a schema — the recommendation's own method string admits "ILLUSTRATIVE ONLY."
10. **The "closed loop" did not strictly reproduce its fit.** `inferops@89871a6:experiments/autoscaling/results.md#Capacity feedback` changes build, host/config, workload/seed, repetitions, warm-up, and auth. Phase 3 actually offered 39.25 rps, not the declared 37.8072 (the actual rate is disclosed in `results.md` §2.1's client-observed column; §4.1's headline comparison row uses the planned rate). The +1.3% arithmetic is true, but not independent confirmation of the original capacity profile.
11. **Kubernetes/GPU is manifest-only.** The k3s evidence starts a server with `--disable-agent`; zero nodes means Pending pods, no HPA metrics/control loop, no PDB/rollout behavior, no device plugin, no GPU Operator, no scheduler, and no rescheduling. The GPU overlay explicitly points to a CPU-only image (the patch file itself records that `ldd` shows only `libggml-cpu.so`).
12. **Delivery and supply chain are thin.** Only `infergate` has CI. There are no public tags or pullable repository digests, no SBOM, vulnerability scan, signature, or provenance attestation. `infergate@f362ceb:Dockerfile#COPY vendor` requires an untracked generated `vendor/` tree, so a clean checkout is not hermetic.
13. **Contracts are structurally good but have semantic cracks.** `serving-contracts@507208b:schemas/hardware-profile.schema.json#required` requires a GPU and cannot represent the actual CPU-only host. Consumer pins remain v0.2-era in several places despite a claimed v1 freeze. The compatibility run was manual, not four public CI runs.
14. **Security is dev-only.** API-key hashing, quotas, and a PostgreSQL usage ledger are implemented; admin access has no application authentication, process-local quota semantics do not form a multi-gateway isolation guarantee, and no NetworkPolicy exists.
15. **Current crash recovery is useful but limited.** `infergate@f362ceb:internal/gateway/crash_recovery_test.go#TestCrashRecovery` exercises real gateway processes, PostgreSQL, SIGKILL, restart, and reload. It is post-release, loopback-scale, and archives summarized results in documentation rather than immutable raw run logs.
16. **Slow-client documentation contradicts the implementation's own caveat.** `infergate@f362ceb:docs/interfaces.md#Fault contract`, `docs/architecture.md#Streaming` and `docs/non-goals.md#NG-10` say a stalled stream is closed and the engine released; `internal/stream/relay.go#Relay` says full scenario-4 handling is later work. Neither the cited relay nor acceptance test creates a truly blocked client write. (Partial mechanism exists — a failed client write triggers `cancelUpstream()` — but it is untested against a stalled reader.)
17. **The fleetlab suite is not all-green under Python 3.12.** At `fleetlab@dd05e7d` under Python 3.12.13, 296 tests pass, four full-corpus cases skip, and one illustrative cold-start test fails because exact float equality differs by one ULP; under Python 3.11 the same suite passes 297/0/4 (the divergence is CPython 3.12's compensated float summation, gh-100425). This is low-severity test brittleness — an exact-equality assertion over floats — but it reinforces the need for real CI rather than prose claims that every push is green.

**Staff-engineer recommendation:** proceed for B; proceed cautiously for A only if the candidate can trace code and correct the portfolio's own overclaims in conversation. Reject for C/D until a real GPU/runtime/Kubernetes substrate is exercised.

---

## 4. Market calibration: current official roles

**Access date:** 2026-07-15; **liveness, titles, levels, and locations re-verified 2026-07-15.** The sample intentionally includes platform vendors and non-frontier infrastructure roles, not only frontier-lab senior roles. Public openings still skew senior — in this sample, materially more senior than the earlier revision represented: three of the four Anthropic postings are Staff-level or above, and two are Dublin (EUR-band) postings. They are used to identify recurring capabilities, not to impose senior scope on every mid-level candidate; if anything, the corrected levels make the mid-level verdicts in this audit conservative.

| Company / official posting | Family | Level / location (verified) | Repeated signals used for calibration |
|---|---|---|---|
| OpenAI — Software Engineer, Productivity – Inference Runtime (posting confirmed live via OpenAI's Ashby application page and mirrors; the exact `openai.com/careers/...` slug cited in the prior revision could not be confirmed and may be constructed) | B/C | IC, San Francisco | developer productivity, test/release systems, runtime reliability, performance regression work |
| [OpenAI — Software Engineer, Inference – Multi Modal](https://openai.com/careers/software-engineer-inference-multi-modal-san-francisco/) | A/C | IC, San Francisco | serving systems, distributed systems, latency/throughput, operating inference paths |
| [OpenAI — Software Engineer, Inference – Performance Optimization](https://openai.com/careers/software-engineer-inference-performance-optimization-san-francisco/) | C | IC, San Francisco | profiling, model/runtime optimization, accelerator utilization, latency and cost |
| [OpenAI — Software Engineer, Inference – AMD GPU Enablement](https://openai.com/careers/software-engineer-inference-amd-gpu-enablement-san-francisco/) | C/D | IC, San Francisco | GPU enablement, kernels/toolchains (HIP/CUDA/Triton), accelerator software, performance debugging |
| [Anthropic — Senior Software Engineer, Inference](https://job-boards.greenhouse.io/anthropic/jobs/4641822008) | A/C | **Senior; Dublin, Ireland (EUR band)** | high-scale inference, distributed systems, operational reliability and efficiency |
| [Anthropic — **Staff** Software Engineer, AI Reliability Engineering](https://job-boards.greenhouse.io/anthropic/jobs/5101169008) | B | **Staff; Dublin, Ireland (EUR band)** | testing/evaluation systems, regressions, reliability, incident-oriented engineering |
| [Anthropic — **Staff+** Software Engineer, Inference Runtime](https://job-boards.greenhouse.io/anthropic/jobs/5257650008) | B/C | **Staff+; US (SF/Seattle/NYC)** | runtime mechanics, performance, correctness, testing and deployment safety |
| [Anthropic — **Senior Staff+** Software Engineer, Kubernetes Platform](https://job-boards.greenhouse.io/anthropic/jobs/5211241008) | D | **Senior Staff+; US** | hands-on Kubernetes internals, controllers/operators, cluster reliability, workload scheduling |
| [Baseten — Software Engineer – Infrastructure](https://jobs.ashbyhq.com/baseten/ae64d1d4-7b0a-4be4-8d77-7f5ce63849a7/) | A/D | IC, San Francisco | model-serving infrastructure, Kubernetes/cloud, observability, reliability, accelerator fleets |
| [Modal — Member of Technical Staff – Platform Engineering](https://jobs.ashbyhq.com/modal/84467a68-6876-4730-9d80-6c6f3d0c2d71) | A/D | IC | distributed platform systems, container orchestration, operational ownership, developer interfaces |

### Market-derived recurring requirements

- **Across many roles:** distributed-systems reasoning, operational ownership, observability/SLOs, CI/CD and release safety, cloud/container systems, incident debugging, and demonstrable performance/reliability measurement.
- **A/B-specific:** routing and multi-tenancy, safe rollouts, deploy gates, regression detection, reliable streaming APIs, incident automation, and correlation from client/gateway to engine/infrastructure.
- **C-specific:** hands-on profiling; batching/scheduling/memory behavior; CUDA, Triton, HIP or equivalent; real engines such as vLLM/Triton; kernels/collectives; accelerator efficiency and cost-to-serve.
- **D-specific:** Kubernetes beyond writing manifests—scheduler/controllers/operators/CRDs, control-plane behavior, device plugins, topology/gang scheduling, accelerator fleets, node failure, and on-call cluster operation.

**Calibration consequence:** the portfolio aligns meaningfully with the first half of A/B. Its C/D vocabulary does not substitute for the representative substrate these postings repeatedly expect. Because the calibration sample skews Staff+/Dublin at the reliability and Kubernetes rows, the family-B and family-D bars implied here are at or above US-senior; the mid-level scores in this audit already discount for that.

---

## 5. Snapshot and claim-integrity audit

### 5.1 Repository snapshot manifest

**VERIFIED FACT:** `git ls-remote --tags` returned zero tags for every repository (re-confirmed via the GitHub API: zero tags and zero releases on all six). Therefore the requested published scope `inference-lab@v1.0.0` is not a publicly immutable snapshot. The closest public object is the mutable `release/v1.0.0` branch at current HEAD. Component commit pins in `pins/pins.yaml` can still be audited individually. The repositories disclose the cause as KI-1 (git proxy drops tag pushes) and designate `release/<version>` branches as the pinnable refs; this context is absent from `FINAL-REPORT.md`'s headline status line.

| Repository | Advertised release / audited published ref | Audited published commit | Current `main` HEAD | HEAD differs from published pin? | Evidence/document existence at claimed snapshot |
|---|---|---|---|---|---|
| `serving-contracts` | claimed local `v1.0.0`; public `release/v1.0.0` branch | `507208b25737470b9eb2f9553a5c55f8f535f1d5` | same | No | Bundle/docs/evidence claims exist; no public tag. Earlier public release branches: v0.1.0 `2df9f81`, v0.2.0 `484b449` |
| `infergate` | claimed v0.1.0; public `release/v0.1.0` branch | `49236a3e38850474fad63ff2cca4065f8cf6feed` | `f362ceb7835c91182f19645a705de66af3017c82` | **Yes** | Release code exists. Health-staleness and crash-recovery work are current-only (`20878ad`, `f511d89`, `f362ceb`) |
| `inferbench` | no tag/branch; I7/current pin | `62c2704997e6c8a2966307ee3d8dbfd16747b631` | same | No for I7 | Raw IB-T010 evidence exists. Older milestone pins include `caa5074`/`69a5abc`; no public release tag |
| `fleetlab` | no tag/branch; I6 pin | `dd05e7decca5a998afdf496d1c439141caba5a29` | same | No | Profiles, reports, tests and recommendation exist; all measured capacity inputs are mock-backed |
| `inferops` | no tag/branch; I6 pin `89871a6`, I7 pin `a07fd2f` | milestone-dependent | `c6954256fcbce3e8f0a5a8ff955598dbea5e2e6c` | **Yes** | I5–I7 artifacts exist at cited commits. IO-T009, count correction and ten runbooks are later; current work cannot validate earlier release wording |
| `inference-lab` | claimed `v1.0.0@b940f5c`; public `release/v1.0.0` branch | tag absent; claimed commit `b940f5c` | `bb0c2537295bb77b5659518c544db9167abb1b06` | **Yes** relative to claim | `FINAL-REPORT.md` did **not** exist at `b940f5c`; added at `c5cf6b7`, acceptance wording updated at `bb0c253`. Other landing/evidence/report/pin files existed at `b940f5c` |

Every abbreviated component commit explicitly sampled from `pins/pins.yaml` resolves in public history: serving-contracts `2df9f81`/`484b449`/`507208b`; infergate `5d69aeb`/`74f2372`/`49236a3`; inferbench `caa5074`/`69a5abc`/`6a3fb53`/`cc404a6`/`62c2704`; fleetlab `dd05e7d`; inferops `135dd34`/`db30279`/`f5fdd86`/`89871a6`/`a07fd2f`. This makes the component evidence recoverable even though the top-level release ref is not immutable.

### 5.2 Release scope versus current-head scope

| Area | Published/component-pin scope | Current-head scope | Hiring treatment |
|---|---|---|---|
| Routing health | One-node router and tests at `infergate@49236a3` | health-staleness experiment added after release | Current readiness evidence only; no retroactive release credit |
| Crash recovery | Not in v0.1 release pin | real process/PostgreSQL crash test and CI at `f511d89`/`f362ceb` | Counts toward readiness today, not v1 portfolio release claims |
| Operations runbooks | I5/I7 operational docs at older pins | ten-runbook set at `inferops@c695425` | Current documentation signal only; not executed incident history |
| Portfolio report | absent at claimed `b940f5c` | present at `bb0c253` | Current narrative may be assessed, but "tagged at b940f5c" is false |
| Acceptance status | checklists/task trackers contain pending states | later `FINAL-REPORT`/pins say accepted | Internal acceptance is process metadata either way, not external proof |

### 5.3 Claim-consistency ledger

| Claim | Documents compared | Verdict | Evidence conflict / correction |
|---|---|---|---|
| "Portfolio tagged v1.0.0 at b940f5c" | `FINAL-REPORT.md#Status`, git refs/history (note: `pins/pins.yaml` makes **no** tag@b940f5c claim — the wording lives only in FINAL-REPORT.md) | **FALSE** | No public tag (disclosed cause: KI-1 git-proxy tag drop); report absent at b940. Public release branch points to bb0c253 |
| "Four green consumer CI runs" | `pins.yaml#I1`, `evidence/i1/checklist.md`, component workflows | **UNVERIFIED / MISLABELED** | They were local manual compatibility executions ("in the same session," per the checklist); only infergate has a workflow and no four run URLs are supplied (zero `actions/runs` URLs exist in the repo) |
| "Deployed and operated on Kubernetes" | `portfolio/README.md#The final narrative`, `limitations.md#Scale`, k3s transcripts | **FALSE under normal meaning** | Server-only API validation, zero nodes and zero scheduled workloads |
| "Warm-up-aware readiness demonstrated" | `pins.yaml#I5`, `evidence/i5/checklist.md`, `handleReadyz`, warm-up script | **NOT DEMONSTRATED** | Backend health transitions were measured; gateway readiness stayed drain-only |
| "Zero-error rolling update" | I5 narrative, `scripts/rolling-update-test.sh`, HAProxy config/raw CSV | **NARROWLY DEMONSTRATED on Compose** | Same digest, two local containers, HAProxy retry/redispatch; not Kubernetes rollout, not version change, and POST replay semantics are not proven safe |
| "100 concurrent, zero frame mixing" | I2 checklist, Scenario A checker, infergate self-test | **PARTLY MISATTRIBUTED** | Composed checker does not compare stream identity; gateway self-test does |
| "3-point cancellation on real engine" | landing page, limitations, I2/I3, IG-T005 | **BROADER THAN EVIDENCE** | Three-point composed run is mock; pinned Qwen composed run is mid-stream only; adapter three-point run used an unpinned random GGUF |
| "G5 passed" | benchmark reports, reproducibility audit, landing page | **ONLY AFTER CRITERION CHANGE** | Original ≤20% target failed twice at +25.16%/+26.08% |
| "Capacity prediction applied and confirmed" | final report, I6 loop, fleetlab holdout, inferops results | **PARTIAL** | 1→2 change measured; six replicas not run; same-corpus holdout miss; reproduction changed important variables |
| "Slow-client defect" | I7 checklist, postmortem, raw scenario-04 | **UNRESOLVED** | Deadline closure not observed, but blocked server write and buffer growth were not demonstrated |
| "Slow-client handling is implemented" | `infergate:docs/interfaces.md`, `docs/architecture.md`, `docs/non-goals.md`, `internal/stream/relay.go`, relay/acceptance tests | **INTERNALLY CONTRADICTED** | Interface/architecture text promises closure and engine release; the relay comment says full scenario-4 handling is later, and cited tests never create a blocked reader |
| "Usage accounting is crash-safe / exactly once" | infergate docs/tests, quickstart limitation, current crash test | **PARTIAL** | Real PostgreSQL/idempotency and current crash test exist; single process/host, no multi-gateway proof, and release quickstart did not compose usage DB |
| "All local suites / CI are green" | component `docs/testing.md`, actual workflows, combined-audit rerun | **FALSE PORTFOLIO-WIDE** | Only infergate has CI. Current fleetlab rerun is 296 pass, 1 one-ULP equality failure, 4 skipped under Python 3.12 (passes 297/0/4 under 3.11 — the brittleness, not the suite, is the defect); other runnable bounded suites pass |
| "Quickstart measured at 2m08s and 35s" | `quickstart/timing-log.md`, `quickstart/` contents | **SELF-REPORTED ONLY** | Timing table exists; no raw command transcript or machine timing artifact is published |
| "RQ-14 proven at runc/nsexec level" | inferops implementation notes and k3s scripts | **MECHANISM UNVERIFIED** | Cited `/home/user/tools/k8s-env-probe-report.md` is referenced in 6+ committed files but is not committed anywhere. The consequence—server-only k3s, zero nodes and no scheduling—is independently evidenced |
| "Open-source contribution" | final narrative, `oss/log.md`, draft comment | **NOT DEMONSTRATED** | Local build/reproduction only; no public issue/PR/comment link. (`oss/log.md` itself states the minimum target is "not met as of this release" — the repo is candid; the portfolio-level narrative should not outrun it) |
| "Production-grade" | root/landing README versus all limitations | **UNSUPPORTED** | No production traffic, users, on-call, real fleet, public release chain, or external validation |

### 5.4 Exact workflow evidence

Only `infergate` supplies an auditable GitHub Actions workflow (`infergate@f362ceb:.github/workflows/ci.yml`, workflow name `ci`). The live API reports **nine runs, all successful push runs**. Exact milestone runs include:

- release commit `49236a3`: [Actions run 29163823049](https://github.com/duy-tung/infergate/actions/runs/29163823049), 2026-07-11, formatting/vet/race tests/streaming stability;
- crash-test commit `f511d89`: [Actions run 29171200694](https://github.com/duy-tung/infergate/actions/runs/29171200694), 2026-07-11, including crash recovery;
- current `f362ceb`: [Actions run 29171600445](https://github.com/duy-tung/infergate/actions/runs/29171600445), 2026-07-11, including five crash-recovery repetitions.

The other five repositories have no workflow files or runs, even though several `docs/testing.md`/`docs/integration.md` files use present-tense CI phrases — verbatim in fleetlab ("green in CI"; "CI … runs the full suite + `contracts-verify` on every push") and near-verbatim in inferbench ("CI validates both directions") and inferops ("CI validates against the bundle's golden fixtures"). Their checks may be locally runnable; the CI claims are not wired.

---

## 6. Material evidence ledger

The IDs below are reused by the competency map and CV bullets. Evidence reuse is explicit: I6, fleetlab's fit, and inferops's scale experiment all derive from the same IB-T010 E2 mock corpus; the I7 postmortems summarize the same fault campaign rather than adding independent experiments; I1's archive summarizes component-local manual checks.

| ID | Material claim and exact primary evidence | Reachable runtime path | Exercise and raw evidence | Pin / configuration | Counter-evidence / limitation | Confidence |
|---|---|---|---|---|---|---|
| **EC-01** | Public release integrity: `inference-lab@bb0c2537295bb77b5659518c544db9167abb1b06:FINAL-REPORT.md#Status`; `pins/pins.yaml#milestone_evidence`; git refs/history | N/A | `git ls-remote --tags` across all six; `git cat-file -e b940f5c:FINAL-REPORT.md` failed | Claimed `v1.0.0@b940f5c`; public branch now bb0c253 | No immutable tag (KI-1 tag-drop publicly disclosed in RELEASES.md/pins.yaml; FINAL-REPORT status line carries no caveat); report postdates claimed commit | HIGH |
| **EC-02** | Core gateway path: `infergate@49236a3e38850474fad63ff2cca4065f8cf6feed:internal/gateway/gateway.go#Gateway.handleChatCompletions` | HTTP middleware → auth → validation → quota → `Manager.Admit` → staged timeouts → selector/retry → stream/non-stream → usage settlement | package/conformance tests plus I2/I3 Compose runs; `inference-lab@b940f5c:scenarios/a/run.sh` and `evidence/i3/checklist.md` | mock and CPU `llama.cpp`; Go 1.24.7 in archived build; one host | No production traffic; Scenario A omits PostgreSQL usage composition | HIGH |
| **EC-03** | Streaming/retry boundary: `infergate@49236a3e38850474fad63ff2cca4065f8cf6feed:internal/gateway/gateway.go#Gateway.streamCompletion`; `internal/stream/relay.go#Relay.writeEvent` | `reliability.Do(openStream)` before HTTP 200; hand relay after first chunk; no retry after status commit; upstream cancel on client write failure | `internal/stream/acceptance_test.go#TestConcurrentStreamsNoFrameMixing`; `internal/backend/llamacpp/llamaserver_test.go`; I2/I3 cancellation artifacts | mock three-point composed test; pinned Qwen mid-stream composed point; unpinned random-GGUF adapter test | I2 checker does not itself test identity; real-engine three-point scope absent; slow-client deadline not established | HIGH for mechanics; MEDIUM for real-engine breadth |
| **EC-04** | Routing: `infergate@f362ceb7835c91182f19645a705de66af3017c82:internal/route/route.go#Router`; `cmd/gateway/main.go#main`; `internal/config/store.go#buildBackend` | Library router is reachable, but command constructs exactly one `BackendSpec`; reloadable config constructs adapter/fallback, not N-backend router | `internal/route/router_test.go`, `staleness_experiment_test.go`, `internal/gateway/routing_test.go` | current HEAD; post-release staleness work | N-backend P2C is not launchable through shipped CLI/config; no multi-replica run | HIGH |
| **EC-05** | Benchmark methodology: `inferbench@62c2704997e6c8a2966307ee3d8dbfd16747b631:internal/schedule/schedule.go#Build`; `internal/run/run.go#Execute`; `analysis/src/inferbench_analysis/percentiles.py#pooled_table`; `goodput.py#evaluate_goodput` | workload → seeded response-independent schedule → client → raw JSONL → warm-up/pooling/goodput/report | unit tests plus IB-T010 raw runs under `docs/evidence/ib-t010/**/events.jsonl` | open-loop Poisson; scheduled-send latency; per-run warm-up; three repetitions in E1/E2 | No closed-loop executor; request-level bootstrap ignores run/temporal clustering; one co-located host | HIGH |
| **EC-06** | Paired gateway overhead: `inferbench@62c2704997e6c8a2966307ee3d8dbfd16747b631:docs/evidence/ib-t010/compute_overhead.py`; `e1-mock-overhead.json`; raw `e1-mock-compare/{direct,gateway}/rep-{1..3}/events.jsonl` | Direct and gateway arms use same benchmark stack and deterministic mock | Independently recomputed twice (audit and re-verification, matching to float precision): 630 pairs; delta = TTFT_gateway − TTFT_direct; p50 1.0386 ms, p95 2.2075 ms, p99 2.8135 ms | mock, same host, sequential arms, 50 warm-up requests per repetition | No randomized/interleaved arms or paired CI; llama.cpp counterpart is inconclusive; pooled p99 is distorted by direct-arm tail anomaly | HIGH for this configuration |
| **EC-07** | Admission G5: `inferbench@62c2704997e6c8a2966307ee3d8dbfd16747b631:docs/evidence/ib-t010/benchmark-report-1.md#E2`; `benchmark-report-1b.md#E2b`; raw E2/E2b JSONL | Gateway admission manager receives severe mock load | E2 original +25.16%; E2b +26.08% (both independently recomputed from raw JSONL: +25.1648%, +26.0800%); typed shedding and bounded waits measured; criterion pre-declared in committed hypothesis file | ~5× open-loop offered load; deterministic mock | Original ≤20% target refuted twice; mock has no organic engine saturation; "no starvation" only covers the tested tenant mix | HIGH |
| **EC-08** | Fault campaign: `inferops@c6954256fcbce3e8f0a5a8ff955598dbea5e2e6c:faults/campaign-matrix.md`; `faults/scenario-{01..12}`; `inference-lab@bb0c2537295bb77b5659518c544db9167abb1b06:evidence/i7/checklist.md` | Compose gateway/backend/PostgreSQL/HAProxy paths; selected scenarios use inferbench client | 12 injected; 11 matched expected or documented-deviation semantics; client impact for 1/2/5/6/12; raw logs/JSONL under each evidence directory | single-host Compose, mostly mock; selected llama.cpp operational tests | Scenario 4 root cause unresolved; several failover scenarios structurally single-backend; self-authored campaign is not production chaos evidence | MEDIUM-HIGH |
| **EC-09** | Observability and lifecycle: `inferops@89871a6:compose/docker-compose.observability.yml`; `scripts/verify-observability.sh`; `scripts/evidence/observability-20260711T233804Z/*`; `scripts/drain-test.sh` | gateway OTel/Prometheus metrics → collector/Prometheus/Tempo/Grafana; drain endpoint → readiness state → stream completion | real trace/exemplar/dashboard queries; Compose drain, config reload, upgrade/rollback scripts | one host; mock and CPU llama.cpp; released local image IDs | No production alert history; readiness is not backend warm-up aware; rollout uses same digest and HAProxy semantics | MEDIUM-HIGH |
| **EC-10** | Capacity loop: `fleetlab@dd05e7decca5a998afdf496d1c439141caba5a29:reports/holdout-validation.md`; `examples/recommendations/e2-admission-sane-v1-5x-scaleout.capacity-recommendation.json`; `inferops@89871a6:experiments/autoscaling/results.md#Capacity feedback` | inferbench result ingest → fit/holdout → recommendation → Compose replica change → remeasurement | ib-t008 six-point mock capacity holdouts −6.7% to +7.2% at extrapolation and near-zero interior; latency low-rate miss −34.4%. Recommendation's ib-t010 two-point fit 33.159±1.105, holdout miss 12.6%; 1→2 result and two-rep 72.391 rps run | deterministic mock; linear replica assumption; A10G cost schema; changed remeasurement conditions | Six replicas never run; recommendation uses the weaker two-point corpus; E2b errors −17.0% to +20.4%; no N−1 headroom; cost is not measured cost-to-serve | HIGH for mechanics; LOW for real capacity |
| **EC-11** | Kubernetes/GPU: `inferops@c6954256fcbce3e8f0a5a8ff955598dbea5e2e6c:clusters/local/evidence/k3s-validation-20260712-hpa.txt`; `deploy/infergate/base/hpa.yaml`; `clusters/gpu-node/gpu-profile-patch.yaml`; `docs/gpu-node-profile.md#Validation result` | Kustomize render → server-only k3s API apply | API accepted ten objects; no agent/node/pod/controller execution | k3s v1.30.4 with `--disable-agent`; GPU overlay only | No kubelet/scheduler/HPA/KEDA/device plugin/Operator/GPU. GPU overlay image is CPU-only (declared under `limits`, the standard form for extended resources) | HIGH |
| **EC-12** | Contracts/provenance: `serving-contracts@507208b25737470b9eb2f9553a5c55f8f535f1d5:openapi/inference-api.yaml`; `schemas/*.schema.json`; `kit/contracts-validate.py#selftest`; `compatibility/compatibility-policy.md#Consumer compatibility tests` | Consumers emit/accept artifacts and invoke vendored/local validators | Combined-audit rerun (and re-verification): 12 schemas meta-valid, 52/52 positives pass, 29/29 negatives fail as required | claimed v1 bundle on release branch; consumers often still carry v0.2 bundles | No public tag; no four public consumer CI runs; GPU-required hardware schema cannot encode actual CPU host | HIGH for local structural checks; MEDIUM for release conformance |
| **EC-13** | Delivery/supply chain: `infergate@f362ceb7835c91182f19645a705de66af3017c82:.github/workflows/ci.yml#jobs`; `Dockerfile`; `inference-lab@bb0c2537295bb77b5659518c544db9167abb1b06:pins/pins.yaml#artifacts` | CI tests infergate; local scripts build images and record image IDs | live API: nine Actions runs, all success; local digest/pin validation | floating Actions/base tags; local image IDs, no registry RepoDigest | Five repos lack CI despite present-tense CI docs; no public tags, SBOM, scanning, signing, provenance; clean Docker build requires generated untracked `vendor/` | HIGH |
| **EC-14** | Current-only crash recovery: `infergate@f362ceb7835c91182f19645a705de66af3017c82:internal/gateway/crash_recovery_test.go#TestCrashRecovery`; `.github/workflows/ci.yml#Crash recovery`; `docs/evidence/ig-t018/crash-recovery-results.md` | spawn PostgreSQL-backed gateway → send work → SIGKILL → restart/reload → inspect clients/ledger | pasted 10-repeat transcript reports 36/36 completed ledger rows, 26/26 in-flight failures resolved, maximum 4.418 ms; public CI independently executes the real PostgreSQL mechanism | current HEAD, loopback, modest workload | Not in published component pin; invariant `ledger_rows <= completed` permits loss even though none observed; transcript is prose, not machine-written raw artifact; no multi-gateway failure | MEDIUM-HIGH |
| **EC-15** | Ownership metadata: all six git histories, author/trailer census | N/A | **119** main-history commits over 52 h 45 m; **117** authored with name Claude; 97 carry explicit AI co-author trailers; remaining authors are one `duy-tung` and one `inferops`/Anthropic noreply commit | 2026-07-10 through 2026-07-12 | Metadata does not prove lack of ownership, but creates a high interview-defensibility burden; self/AI verifier is not external validation | HIGH for metadata; no inference about actual authorship competence |

### Quantitative recomputations

All figures below were recomputed a second, fully independent time on 2026-07-15 (own pairing/percentile/sweep implementations); every value matched.

1. **E1 paired TTFT overhead (EC-06).** For each request identity, \(d_i=TTFT_{gateway,i}-TTFT_{direct,i}\), after the archived warm-up exclusions. With \(n=630\), type-7 linear percentile interpolation gives p50 = 1.0386 ms, p95 = 2.2075 ms, p99 = 2.8135 ms, mean = 0.7089 ms; 65/630 (10.32%) deltas are negative. This exactly supports "+2.21 ms paired p95 on a same-host deterministic mock," not "the gateway costs 2 ms on LLM inference generally."
2. **G5 original criterion (EC-07).** \((TTFT_{accepted,overload}/TTFT_{baseline}-1)\times100\) is +25.16% in E2 (baseline p95 0.161199 s, n=809; overload 0.201764 s, n=573) and +26.08% in E2b, both above the predeclared 20% limit. The original gate failed twice.
3. **I6 fitted-rate comparison (EC-10).** \((33.583-33.159)/33.159\times100=1.2787\%\). The arithmetic is right. The run's actual offered rate (39.25 rps, disclosed in results.md §2.1) and other changed conditions prevent calling it a strict independent replication.
4. **Two-replica capacity (EC-10).** \(4357\ successful/60.187s=72.391\ rps\). This is +9.16% against \(2\times33.159=66.318\), and −4.56% against \(2\times37.925=75.850\). It is a measured two-container mock result, not a six-replica serving result.
5. **One→two replica demand-capped run (EC-10).** One replica: 2,207 successful and 795 shed of 3,002 over 60.128 s, goodput 36.705 rps. Two replicas: 3,002 successful, zero shed over 60.086 s, 49.962 rps. It proves relief at ~50 offered rps, not the two-replica ceiling.
6. **I2 concurrency and gateway/client TTFT agreement (EC-03).** A sweep over request start/end timestamps in `inference-lab@bb0c253:evidence/i2/raw/runs/concurrency-100/events.jsonl.gz` reaches **154 simultaneous requests**; all 2,736 records are `ok`, and `output_tokens = len(ITL)+1` has zero violations. That is a framing/count consistency check, not an identity-based no-mixing proof. Separately, using `runs/chat-short/events.jsonl.gz` and the deltas between `metrics-00-pre-chat-short.prom` and `metrics-01-post-chat-short.prom`, client mean TTFT 0.303917 s minus gateway histogram mean \((1459.732-1.026)/(4832-2)=0.302010\ s\) is **+1.907 ms** for the archived interval.
7. **Three-point cancellation timing (EC-03).** Greedy nearest-timestamp joins between `inference-lab@bb0c253:evidence/i2/raw/runs/cancel-{pre-first-token,mid-stream,near-completion}/events.jsonl` and each run's `debug-state.json` yield min/median/max deltas of **0.247/0.398/0.573 ms** before first token (30 pairs), **0.310/0.413/0.724 ms** mid-stream (29), and **0.318/0.367/0.638 ms** near completion (12 pairs, one canceled event unmatched). The arithmetic is reproducible; absent a shared request ID, these are timing correlations rather than definitive per-request causal measurements.
8. **Autoscaling-signal lag (EC-10).** Against the archived knee onset at 90 s in `inferops@c695425:experiments/autoscaling/evidence/signal-comparison-20260712T022504Z/summary.json`, requests-in-flight first fires at 96.10 s (**+6.10 s**) and queue depth at 154.42 s (**+64.42 s**). Token rate and gateway CPU fire **34.12 s** and **38.14 s before** the declared knee and are labeled false-early. This ranks signals in one Compose/mock trace; no autoscaling controller consumed them.
9. **Failover window (EC-08).** `listening_ts-kill_ts` in `inference-lab@bb0c253:evidence/i3/raw/failover-timeline.json` is **141.682 s**. The associated run contains 28 requests: 27 `ok` and one typed `upstream_error` at the kill (terminated ~230 ms after the kill timestamp). All 12 requests issued after the kill and before llama.cpp returned were served by the mock. The CV-safe statement is "12/12 requests during the recorded outage window succeeded via fallback," not "zero client failures during failover."
10. **Recommendation regeneration (EC-10).** Re-running `fleetlab.fitting` and `fleetlab.emit.build_recommendation()` in memory produced serialization byte-identical to `fleetlab@dd05e7d:examples/recommendations/e2-admission-sane-v1-5x-scaleout.capacity-recommendation.json` (SHA-256 `85e5d9727775d89f96437daf8a3087690d45ec3f0500850adbd660e595c1ec9f`), including six replicas and predicted aggregate goodput interval **[165.279, 189.036] rps** — reproduced under both Python 3.12 and 3.11. This verifies deterministic derivation from the mock fit, not the recommendation in execution.

---

## 7. Role-fit and competency map

Legend: Y = yes; P = partial; N = no. "Measured" requires inspectable output. "Representative" is judged against the hiring claim. Scores are deliberately not averaged across role families.

| Competency | Role family | Score | Implemented | Exercised | Measured | Representative | Primary evidence | Counter-evidence | Hiring interpretation |
|---|---|---:|:---:|:---:|:---:|:---:|---|---|---|
| OpenAI-subset API and engine boundary | A | 3 | Y | Y | Y | P | EC-02, EC-12 | one model/adapter style; CPU only | Credible platform API work with substrate limitation |
| CPU `llama.cpp` adapter/model loading | A/C | 3 | Y | Y | Y | P | EC-02, EC-03; `inferops:compose/docker-compose.llamacpp.yml` | generic OpenAI HTTP adapter; no engine internals | Demonstrates integration, not runtime engineering |
| vLLM/SGLang adapter execution | A/C | 0 | N | N | N | N | none | task/interface references only | Not demonstrated |
| SSE framing and post-first-token retry boundary | A/B | 3 | Y | Y | Y | P | EC-03 | composed identity proof is misattributed; one host | Strong mechanics, materially limited scale/substrate |
| Cancellation and resource release | A/B/C | 3 | Y | Y | Y | P | EC-03 | real pinned engine only mid-stream; causal timing joins weak | Credible semantics, not full engine-resource proof |
| Slow-client protection | A/B | 2 | Y | P | P | N | EC-03, EC-08 | experiment never proves blocked write/bounded memory | Implementation exists; behavior under actual backpressure unresolved |
| N-backend routing, health, P2C | A | 2 | Y | Y | Y | N | EC-04 | library-only N>1; shipped launch path has one node | Partially demonstrated; do not call it a multi-backend platform |
| Admission/backpressure/fairness | A/B | 3 | Y | Y | Y | P | EC-02, EC-07 | mock; original TTFT target failed; code-confirmed (unreproduced) cancel/grant race | Real platform logic with a material limitation |
| Retry budget/circuit breaker/timeouts | A/B | 3 | Y | Y | Y | P | EC-02, EC-03, fault scenarios 1/2/7 | primarily mock/single-backend; no fleet retry storm | Credible bounded retry mechanics |
| Authentication, quota, accounting | A/B | 3 | Y | Y | Y | P | EC-02, EC-14 | process-local quota; dev admin/no NetworkPolicy; release quickstart omits DB | Solid backend platform signal, not tenant-isolation proof |
| Config reload and drain | A/B | 3 | Y | Y | Y | P | EC-09 | Compose/local; no orchestrated model rollout | Credible lifecycle mechanics |
| Backend/model warm-up readiness | A/B/D | 1 | P | P | P | N | EC-09, EC-11 | gateway `/readyz` is drain-only | Claimed-but-thin; current portfolio wording is wrong |
| Model/version lifecycle and canarying | A/B | 1 | P | P | P | N | config alias rollout scripts | no real model replacement/canary/rollback across nodes | Interface/demo only |
| Prefill/decode separation | C | 0 | N | N | N | N | none | discussed as engine boundary | Not demonstrated |
| Continuous batching/request scheduler internals | C | 0 | N | N | N | N | none | gateway intentionally does not batch; no engine work | Not demonstrated |
| KV/prefix-cache pressure or behavior | C | 0 | N | N | N | N | workload descriptors only | no engine metrics/experiments | Not demonstrated |
| Quantization/model-loading sensitivity | C | 1 | P | Y | P | N | one Qwen Q4_K_M CPU run | one quantization/model, no comparison | Claimed substrate exists; engineering capability not shown |
| Speculative decoding | C | 0 | N | N | N | N | none | none | Absent |
| Engine profiling/bottleneck attribution | C | 1 | P | P | P | N | llama timing and gateway histograms | no profiler, flame graph, kernel/engine attribution | Measurement adjacency only |
| CUDA/ROCm, GPU OOM, kernels | C/D | 0 | N | N | N | N | none | no GPU rented | Hard blocker for GPU/runtime roles |
| NCCL/collectives/tensor-pipeline parallelism | C/D | 0 | N | N | N | N | none | single host/engine | Absent |
| MIG/MPS/heterogeneous accelerator scheduling | C/D | 0 | N | N | N | N | manifest vocabulary only | no device or scheduler | Absent |
| Real Kubernetes pod scheduling | D/A | 1 | P | N | P | N | EC-11 | API validation only, zero nodes | Manifest-authoring evidence, not operations |
| Readiness/PDB/rollout/rollback on Kubernetes | D/B | 1 | P | N | N | N | Kustomize objects | Compose lifecycle cannot substitute for controller behavior | Claimed-but-thin |
| HPA/KEDA/controller loop | D/A/B | 1 | P | N | P | N | HPA manifest/API acceptance | no metrics adapter, decisions, scale events; KEDA rejected | Not operationally demonstrated |
| Operators/device plugins/GPU Operator | D | 0 | N | N | N | N | none | overlay only declares `nvidia.com/gpu` (under `limits`, the standard extended-resource form) | Absent |
| Node failure/rescheduling/multi-node | D | 0 | N | N | N | N | none | one machine | Hard blocker for D and senior platform roles |
| OTel/Prometheus/tracing | A/B | 3 | Y | Y | Y | P | EC-09 | single host; no long-term cardinality/retention evidence | Strong personal-portfolio observability signal |
| TTFT/ITL/throughput/goodput metrics | A/B/C | 3 | Y | Y | Y | P | EC-05, EC-06 | engine/gateway/client semantics not always causally joined | Good measurement vocabulary and implementation |
| Cardinality policy/dashboards/alerts | A/B | 2 | Y | Y | Y | P | metrics policy, golden dashboard, alert queries | no alert firing/incident history at scale | Useful platform evidence, limited operation |
| SLO/error-budget reasoning | B/A | 3 | Y | Y | Y | P | EC-05, EC-07 | "production SLO" unsupported; re-framed G5 | Strong test-governance signal if described honestly |
| Open-loop generation/CO avoidance | B/C | 3 | Y | Y | Y | P | EC-05 | no closed-loop execution; generator shares host | Differentiating benchmark-methodology signal |
| Percentiles/warm-up/repetitions/noise | B/C | 3 | Y | Y | Y | P | EC-05, EC-06 | sequential arms; three reps; request bootstrap not cluster bootstrap | Credible methodology with known statistical limits |
| Paired experiments and confidence intervals | B/C | 2 | Y | Y | Y | P | EC-06 | no paired/run-cluster CI; limited noise control | Partially demonstrated |
| Fault injection/timeout/crash recovery | B/A | 3 | Y | Y | Y | P | EC-08, EC-14 | personal loopback campaign; current crash test post-release | Best B-family operational evidence |
| Idempotency/accounting correctness | B/A | 3 | Y | Y | Y | P | EC-02, EC-14 | no multi-gateway linearizability; crash invariant permits loss | Solid backend reliability signal |
| Soak/load/chaos coverage | B | 2 | Y | Y | Y | N | EC-07, EC-08 | short runs, one machine, no soak | Partial only |
| Postmortems/corrective actions | B | 2 | Y | Y | P | N | `inference-lab:postmortems/pm-001..003.md` | authored from synthetic campaign; slow-client root cause unresolved | Good practice signal, not incident-response experience |
| Capacity fit and holdout | A/B/C | 2 | Y | Y | Y | N | EC-10 | mock, two-point miss, six replicas unrun | Mechanics demonstrated; serving-capacity claim not demonstrated |
| Autoscaling-signal selection | A/B/D | 2 | Y | Y | Y | N | EC-10, inferops signal ramp | offline/Compose observation, no controller | Useful reasoning evidence, not autoscaling operation |
| Cost/request or cost/token | A/C | 1 | Y | N | P | N | fleetlab cost schema/report | A10G price combined with mock CPU capacity (the emitter itself labels it "ILLUSTRATIVE ONLY") | Do not claim cost optimization |
| Contract/SemVer/provenance design | A/B | 3 | Y | Y | Y | P | EC-12 | public tag absent; CPU schema gap | Differentiating cross-repo interface discipline |
| Real-consumer conformance | A/B | 2 | Y | Y | P | P | EC-12 | local manual runs mislabeled CI; stale v0.2 consumer pins | Partial delivery proof |
| CI/regression gates | B | 2 | Y | Y | Y | P | EC-13, EC-14 | only one of six repos; fleetlab carries a one-ULP exact-float assertion that fails under Python 3.12 (passes under 3.11) | Useful but insufficient portfolio release system |
| Kustomize/IaC depth | D/B | 2 | Y | P | P | N | EC-11 | no Helm/Terraform/GitOps; no scheduled resources | Manifest competence, not infrastructure operation |
| Secrets/tenant isolation | A/B/D | 2 | Y | Y | P | N | auth/DB tests, secret scripts | dev-only, no NetworkPolicy/admin auth/multi-gateway isolation | Backend security mechanics only |
| SBOM/scanning/signing/provenance | B/D | 1 | P | N | N | N | digests/pins only | no SBOM, scanner, signature, attestation | Claimed release rigor exceeds implementation |

### 7.1 What is genuinely demonstrated versus described

**Genuinely demonstrated, with material limitations:** Go gateway request mechanics; CPU llama.cpp integration; mock and CPU streaming; cancellation/retry semantics; bounded admission; PostgreSQL-backed usage/accounting tests; open-loop benchmark tooling; raw pooled analysis; Compose observability and lifecycle; fault injection; current crash/restart test; contract/provenance tooling; mock capacity-loop mechanics.

**Partly demonstrated:** multi-backend routing as a tested library; slow-client handling; release automation; real-consumer contract conformance; readiness; cost model; autoscaling-signal choice; Kubernetes manifests; security/isolation.

**Merely described or absent:** vLLM/SGLang; GPU memory/KV/batching/kernel work; prefill/decode separation; speculative decoding; NCCL/multi-GPU; real Kubernetes scheduling/controllers/device plugins/Operator; HPA/KEDA execution; multi-node/multi-region; production use/on-call; public OSS contribution.

---

## 8. Transition-critical gaps, ranked by hiring damage

| Rank / gap | Families | What a hiring manager will distrust | Staff-engineer probe | Severity | Smallest credible experiment and acceptance criteria | Effort | Hiring impact |
|---|---|---|---|---|---|---|---|
| **1. No real GPU or vLLM/SGLang execution** | A, C, D | Whether "AI infrastructure" is more than backend systems with LLM vocabulary | Show engine metrics, batching/KV behavior, GPU memory limits, cancellation release, profiler output, and a real bottleneck | **Hard blocker C/D; major A** | Run existing gateway + inferbench against pinned vLLM on one rented GPU. Predeclare direct/gateway paired runs, cancellation points, batch/KV sweeps, OOM negative test, engine metrics, driver/CUDA/model/image digests; archive raw logs. Pass only if results reproduce and causal engine signals move as predicted | LARGE | HIGH |
| **2. No real pod scheduling or controller loop** | D, A, B | Whether Kubernetes claims survive beyond YAML authoring | Show Pod events, readiness transitions, rollout/PDB behavior, HPA decisions, node failure/reschedule, device-plugin resources | **Hard blocker D; major A/B** | Use a real kind/k3s cluster with agents. Schedule gateway/backend/Postgres; prove gateway not Ready before engine; execute distinct-digest rollout and rollback; drive HPA/KEDA; archive `kubectl events`, metrics and timelines. No credit for API-only apply | MEDIUM–LARGE | HIGH |
| **3. Launch path cannot configure N>1 and readiness is false-positive** | A, B | Whether the "platform" actually routes a fleet safely | Trace CLI/config construction into `Router`; explain `/readyz` contract under backend warm-up | **Major weakness** | Extend existing config schema to N backends; make `/readyz` depend on at least one eligible warmed backend and required DB state; run two distinct backend processes, health transitions, drain/reload, and a zero-ready negative. All assertions must hit public endpoints | MEDIUM | HIGH |
| **4. No runtime-internal performance work** | C | Whether the candidate can reason below HTTP | Attribute latency to queueing, prefill, decode, batch formation, KV allocation/eviction, memory bandwidth, kernels | **Hard blocker C** | In the same vLLM slice, collect per-request engine timing, batch-size series, KV occupancy/eviction, GPU utilization/memory, and profiler traces across controlled input/output lengths. Identify and validate one bottleneck with a before/after change | LARGE | HIGH |
| **5. Mock-based capacity recommendation; six replicas unexecuted** | A, B, C | Whether capacity/cost claims predict a real serving system | Re-derive 33.159, explain 37.925 discrepancy, headroom/N−1, linear scaling, and A10G-price mismatch | **Major weakness** | Fit ≥3-rate, ≥3-repetition randomized profiles on real vLLM; hold out predeclared points; execute the recommended N and N−1; require error bounds and SLO/goodput acceptance before seeing results; calculate cost/output-token from actual billed session | LARGE | HIGH |
| **6. No multi-node system** | A, C, D | Whether distributed failure and topology claims are real | What happens on node loss, network partition, collective failure, placement skew, and rescheduling? | **Hard blocker D/senior; major senior A/C** | Two-node cluster with one worker deliberately stopped during load; measure reschedule, capacity loss, PDB/rollout behavior and client impact. For C, a real distributed engine/collective is needed; HTTP replicas alone do not prove multi-GPU runtime | LARGE | HIGH for D/senior; MEDIUM otherwise |
| **7. Release chain is not immutable or portfolio-wide** | A, B | Whether anyone can reproduce the advertised release | Resolve v1.0.0, identify exact component artifacts, rebuild cleanly, verify all consumers, roll back a changed image | **Major weakness B/A** | Create actual immutable tags/releases for future work; six-repo CI keyed to component SHAs; clean-checkout image builds; registry RepoDigests; SBOM, vulnerability gate, signature/attestation; distinct-digest upgrade and rollback with public run links | MEDIUM | HIGH for B |
| **8. Slow-client result unresolved; code-confirmed admission race** | A, B | Whether reliability conclusions outrun tests | Prove sender-side blocked write and bound memory; linearize grant vs cancellation and show slot accounting | **Major correctness weakness** | Constrain server send buffer, stream an effectively unbounded response, instrument write start/end/deadline and RSS, compare fast-client TTFT; add a deterministic grant/cancel race test and invariant `globalInFlight==live tickets`. Fix and rerun negative/positive cases | SMALL–MEDIUM | HIGH |
| **9. No production/external-user/on-call/OSS evidence** | A–D, especially senior | Whether the system has met independent requirements or adversarial use | Ask for real users, incidents, external review comments, upstream links, adoption and maintenance history | **Major senior weakness; useful bonus at mid** | Obtain one genuine external consumer/reviewer or a merged/upstream-reviewed contribution tied to these repos, with public discussion and follow-up. This cannot be manufactured by more self-authored documentation | MEDIUM, calendar-dependent | MEDIUM–HIGH senior |

### Explicit credibility loss from the known constraints

- **No real GPU:** removes representative evidence for accelerator efficiency, OOM behavior, kernels, GPU telemetry, memory/KV pressure and most C/D roles. Honest disclosure improves judgment signal but does not demonstrate the capability.
- **No vLLM/SGLang execution:** makes engine-interface and workload files preparatory only. A generic OpenAI adapter is not a vLLM integration.
- **No real pod scheduling:** makes "Kubernetes deployment/operations" unsafe wording. API validation earns manifest competency only.
- **No real autoscaling controller:** signal-analysis work is useful reasoning, but cannot establish HPA/KEDA correctness, lag, stability, scale-to-zero, or interaction with readiness.
- **No multi-node system:** blocks claims about cluster reliability, rescheduling, distributed execution, collectives, topology or fleet behavior.
- **Mock-based capacity modeling:** demonstrates data plumbing/model governance; it does not validate LLM-serving capacity or real cost-to-serve.
- **No production/external-user evidence:** blocks production-grade, production SLO, organizational adoption and on-call claims. It is not a mid-level disqualifier when the portfolio is framed as a lab; it is a serious senior-scope gap.

---

## 9. Interview exposure: the hardest staff-engineer questions

### 1. "How do I launch the gateway with two P2C backends from a clean checkout?"

- **Why asked:** to distinguish a tested abstraction from a shipped platform feature.
- **Strongest truthful answer:** "You cannot through the current CLI or reloadable file config. `main` builds a one-node `Router`; N-node routing is covered in package/gateway tests. I should describe it as an implemented/tested routing library, not an operable multi-backend gateway."
- **Support:** `infergate@f362ceb7835c91182f19645a705de66af3017c82:cmd/gateway/main.go#main`; `internal/config/store.go#buildBackend`; `internal/route/router_test.go`; `internal/gateway/routing_test.go`.
- **Strength:** **PARTIAL**.
- **Follow-up trap:** "Then what exactly did the health/P2C load-balancing measurement exercise?"
- **Must not claim:** multi-backend production routing, fleet load balancing, or a config-driven P2C deployment.

### 2. "What makes `/readyz` false while the model is warming?"

- **Why asked:** readiness is safety-critical, and the portfolio names it as demonstrated.
- **Strongest truthful answer:** "Nothing currently. `/readyz` reflects drain state only. The warm-up experiment measured backend health and request failure/success around startup, but did not assert gateway readiness. The Kubernetes probe would mark the gateway ready too early."
- **Support:** `infergate@f362ceb7835c91182f19645a705de66af3017c82:internal/gateway/gateway.go#handleReadyz`; `inferops@c6954256fcbce3e8f0a5a8ff955598dbea5e2e6c:scripts/warmup-readiness-test.sh#Verdicts`; `deploy/infergate/base/deployment.yaml#readinessProbe`.
- **Strength:** **WEAK**, but the honest diagnosis is strong.
- **Follow-up trap:** "Why did the final report say warm-up-aware readiness passed?"
- **Must not claim:** warm-up-aware gateway readiness or safe Kubernetes readiness gating.

### 3. "Prove the slow client blocked a server write for longer than three seconds."

- **Why asked:** to test whether a negative observation supports the stated root cause.
- **Strongest truthful answer:** "The archived experiment cannot prove that. It proves an eight-second reader stall did not visibly close a bounded stream. Kernel buffering may have prevented `Write` from blocking. I need server-side write instrumentation, constrained buffers, a much larger stream and memory measurements."
- **Support:** `inferops@c6954256fcbce3e8f0a5a8ff955598dbea5e2e6c:faults/scenario-04/verdict.md` (Parts A/B, Verdict) and the scenario-4 "Observed" cell in `faults/campaign-matrix.md`; `infergate@49236a3e38850474fad63ff2cca4065f8cf6feed:internal/stream/relay.go#Relay.writeEvent`.
- **Strength:** **WEAK** for the defect claim.
- **Follow-up trap:** "Why call it reproducible and defect-shaped rather than an inconclusive test?"
- **Must not claim:** a proven Go deadline defect, unbounded memory, or confirmed upstream resource leak.

### 4. "Linearize admission grant versus client cancellation. Can a slot leak?"

- **Why asked:** admission correctness depends on exact concurrency ownership.
- **Strongest truthful answer:** "There is a code-confirmed but runtime-unreproduced interleaving: the dispatcher removes the ticket, increments in-flight, and buffers a grant; if cancellation wins the caller select, `cancelWaiting` finds nothing, never drains the grant, and no returned `Ticket` releases the slot. The in-code 'harmless unread value' comment is wrong for grants. It needs a deterministic race test."
- **Support:** `infergate@49236a3e38850474fad63ff2cca4065f8cf6feed:internal/admission/admission.go#Manager.Admit`; `#Manager.cancelWaiting`; dispatcher grant path (code identical at release and main).
- **Strength:** **PARTIAL**.
- **Follow-up trap:** "What invariant and ownership protocol would fix it?"
- **Must not claim:** proven leak-free cancellation or exactly paired slots under every interleaving.

### 5. "Trace one streaming request and explain exactly why retry stops after the first token."

- **Why asked:** this is central serving correctness, not documentation recall.
- **Strongest truthful answer:** "`handleChatCompletions` admits and creates staged deadlines, then `streamCompletion` calls `reliability.Do(openStream)`. The first upstream chunk arrives before status 200 is committed, so pre-first-token failures can retry. After commit, the relay loop has no retry path; failures become an SSE error/cancellation and close upstream."
- **Support:** `infergate@49236a3e38850474fad63ff2cca4065f8cf6feed:internal/gateway/gateway.go#Gateway.handleChatCompletions`; `#Gateway.streamCompletion`; `internal/reliability/retry.go#Do`.
- **Strength:** **STRONG**.
- **Follow-up trap:** "What happens to usage settlement when the client disconnects after three chunks?"
- **Must not claim:** retry after a committed chunk or exactly-once client delivery.

### 6. "How do your cancellation logs prove causal engine resource release?"

- **Why asked:** timestamp correlation can look stronger than it is.
- **Strongest truthful answer:** "They show aggregate abort/resource recovery and a composed pinned-Qwen mid-stream point. Some timing analyses greedily pair timestamp-only events rather than joining by request ID, so the sub-millisecond per-request delta is weaker than the broader cancellation result."
- **Support:** `inference-lab@bb0c2537295bb77b5659518c544db9167abb1b06:evidence/i3/checklist.md#Cancellation`; `portfolio/limitations.md#Model and engine coverage`; infergate llama adapter tests.
- **Strength:** **PARTIAL**.
- **Follow-up trap:** "Why are there 21 abort-log entries for 20 planned cancellations in the first attempt?"
- **Must not claim:** three-point, request-correlated resource release on the pinned Qwen engine.

### 7. "Did admission control pass G5?"

- **Why asked:** to test governance honesty and understanding of changed success criteria.
- **Strongest truthful answer:** "The original ≤20% accepted-TTFT degradation criterion failed twice: +25.16% and +26.08%. A later decision evaluated typed shedding, bounded queue wait and tested fairness instead. That later criterion passed; the original performance target did not."
- **Support:** `inference-lab@bb0c2537295bb77b5659518c544db9167abb1b06:reports/benchmark-report-1.md#Gate G5`; `reports/benchmark-report-1b.md#Follow-up`; EC-07.
- **Strength:** **STRONG** if answered this way.
- **Follow-up trap:** "Was the criterion changed before or after seeing the data, and why is that not p-hacking?"
- **Must not claim:** admission preserved accepted TTFT within 20% or protected a real saturated engine.

### 8. "Why does scheduled-send latency address coordinated omission, and what is still statistically weak?"

- **Why asked:** to test performance-methodology depth.
- **Strongest truthful answer:** "Arrivals are precomputed independently of responses, and latency begins at the scheduled send, so generator dispatch/connect slip counts. Raw requests are pooled rather than averaging percentiles. Limits: client and target share a host, arms are sequential, there are three repetitions, and bootstrap resamples requests rather than run clusters."
- **Support:** `inferbench@62c2704997e6c8a2966307ee3d8dbfd16747b631:internal/schedule/schedule.go#Build`; `internal/run/run.go#Execute`; `analysis/src/inferbench_analysis/percentiles.py#bootstrap_ci/#pooled_table`.
- **Strength:** **STRONG**.
- **Follow-up trap:** "Why can request-level bootstrap understate uncertainty?"
- **Must not claim:** dedicated-hardware noise control, independent samples, or universal 2.21 ms overhead.

### 9. "Derive six replicas from 33.159 rps and tell me why you should not trust it."

- **Why asked:** capacity recommendations are easy to overstate.
- **Strongest truthful answer:** "Six is the schema-valid linear result for the selected mock demand/SLO assumptions. The same two-point corpus misses holdout by 12.6%; 33.159 and the overload-derived 37.925 disagree; point headroom is only about 5.2% at upper demand; N−1 is deficient; and six was never run."
- **Support:** `fleetlab@dd05e7decca5a998afdf496d1c439141caba5a29:reports/holdout-validation.md#E2`; `examples/recommendations/e2-admission-sane-v1-5x-scaleout.capacity-recommendation.json`; `inference-lab@bb0c2537295bb77b5659518c544db9167abb1b06:evidence/i6/loop-report.md`.
- **Strength:** **PARTIAL**.
- **Follow-up trap:** "Why use an A10G price for CPU mock throughput?"
- **Must not claim:** validated six-replica capacity, a real autoscaling target, or measured cost-to-serve.

### 10. "Show one Kubernetes scheduler or HPA decision caused by your manifests."

- **Why asked:** to distinguish API syntax validation from operations.
- **Strongest truthful answer:** "There is none. k3s ran server-only with `--disable-agent`; objects were rendered and accepted but no pod or HPA control loop executed. Compose supplied the operational experiments."
- **Support:** `inferops@c6954256fcbce3e8f0a5a8ff955598dbea5e2e6c:clusters/local/evidence/k3s-validation-20260712-hpa.txt#starting k3s`; `experiments/autoscaling/results.md#Scope boundary`.
- **Strength:** **WEAK** for Kubernetes, **STRONG** as honest scope control.
- **Follow-up trap:** "Then why does the portfolio say deployed on Kubernetes?"
- **Must not claim:** deployment on Kubernetes, autoscaling, rescheduling, PDB behavior, or GPU scheduling.

### 11. "What crash-safety guarantee does the current PostgreSQL test actually establish?"

- **Why asked:** "crash-safe" and "exactly once" invite formal scrutiny.
- **Strongest truthful answer:** "At current HEAD, ten loopback repetitions kill and restart a real gateway process backed by PostgreSQL; 26 in-flight clients resolve within 4.42 ms maximum and no duplicate ledger rows were observed. It does not prove no lost settlements, multi-gateway linearizability or production durability."
- **Support:** `infergate@f362ceb7835c91182f19645a705de66af3017c82:internal/gateway/crash_recovery_test.go#TestCrashRecovery`; Actions runs 29171200694 and 29171600445.
- **Strength:** **PARTIAL**.
- **Follow-up trap:** "Why does the asserted `ledger_rows <= completed` invariant allow loss?"
- **Must not claim:** exactly-once accounting across crashes or distributed gateways.

### 12. "Reproduce the advertised v1.0.0 release and its four green consumer CI runs."

- **Why asked:** immutable provenance is a core release-engineering claim.
- **Strongest truthful answer:** "I cannot from the public refs as written. There is no tag — our git proxy dropped tag pushes (KI-1) and we pinned release branches instead, but the final report's headline doesn't say that; `FINAL-REPORT.md` did not exist at claimed b940f5c; and the four consumer checks were local manual runs, not four linked CI jobs. Exact component commits are recoverable from pins, but the release claim needs repair."
- **Support:** EC-01, EC-12, EC-13; `inference-lab@bb0c2537295bb77b5659518c544db9167abb1b06:pins/pins.yaml#I1`; `serving-contracts@507208b25737470b9eb2f9553a5c55f8f535f1d5:RELEASES.md#v1.0.0`.
- **Strength:** **WEAK** for the published release.
- **Follow-up trap:** "Which exact artifact can a third party pull by digest today?"
- **Must not claim:** immutable public v1 release, four consumer CI runs, or pullable signed release images.

---

## 10. Differentiating strengths — only the defensible ones

| Strength | Technical decision/result and measured evidence | Transfer and differentiation | Material limitation | Exact CV-safe wording |
|---|---|---|---|---|
| **Coordinated-omission-aware load generation** | Seeded response-independent open-loop schedules; latency begins at scheduled send; raw requests are pooled; shed/error/cancel remain in goodput denominator. E1 raw recomputation produced n=630 and +2.21 ms paired p95 (EC-05/06) | Directly transfers to B and performance-tooling portions of C. Most backend portfolios quote latency without controlling issuance or denominator bias | Same host, sequential arms, three repetitions, request-level—not run-cluster—bootstrap; real llama result inconclusive | "Built a seeded open-loop benchmark harness using scheduled-send latency, raw-event pooling and goodput denominators that include shed, canceled and errored requests." |
| **Correct streaming failure boundary** | First upstream chunk is acquired inside bounded retry before status commit; after HTTP 200 the code has no retry path; client write failure cancels upstream. Gateway self-test verifies 100 distinct concurrent streams (EC-03) | Strong A/B signal because streaming retry/cancellation mistakes create duplicates and wasted inference | Real pinned engine has only one composed cancellation point; slow-client backpressure remains unresolved; no fleet load | "Implemented and tested SSE relay semantics with retry only before the first upstream chunk, explicit post-commit error handling and upstream cancellation on client disconnect." |
| **Falsification and preserved negative results** | Original G5 criterion failed twice (+25.16%, +26.08%); capacity holdout miss and unexecuted six-replica result are disclosed; scenario 4 remains non-passing (EC-07/08/10) | Valuable B-family engineering judgment: hypotheses are versioned and failed outcomes remain visible instead of being silently relabeled | Criteria were re-framed after data; all review is self-authored; scenario-4 root cause is overstated in some docs | "Predeclared and audited reliability/performance gates, preserving two failed admission-control results and model-validation misses instead of reporting only favorable experiments." |
| **Cross-repository contracts and provenance discipline** | OpenAPI plus 12 JSON Schemas, 52 positive and 29 negative fixtures, model/engine/workload/image pins and explicit comparability rule (EC-12) | Stronger release/interface thinking than a typical monorepo demo; transfers to A/B platform boundaries | Public v1 tag absent; compatibility checks mislabeled CI; GPU-only hardware schema cannot encode measured CPU host | "Versioned an OpenAPI serving contract and 12 JSON Schemas with positive/negative fixtures and explicit model, engine, workload and artifact provenance." |
| **Reachable fault/observability work, not just diagrams** | Compose OTel/Prometheus/Tempo/Grafana path, trace/exemplar capture, drain/reload scripts, 12 injected scenarios, and current PostgreSQL/SIGKILL test (EC-08/09/14) | Differentiates B-family readiness from ordinary API portfolios because it exercises failure semantics and archives client impact | Single host, mostly mock, short runs; one scenario inconclusive; crash test is post-release; no production incident response | "Exercised a single-host Compose serving stack through 12 fault scenarios, tracing selected client impact and retaining one unresolved slow-client result as a failed acceptance case." |

---

## 11. Ownership and interview defensibility

### 11.1 AI-assistance evidence and fair interpretation

**VERIFIED FACT (EC-15):** across **119 main-history commits in 52 h 45 m**, **117** use `Claude <noreply@anthropic.com>` as author metadata and **97** include explicit AI co-author trailers. The other two author records are one `duy-tung` commit and one `inferops <noreply@anthropic.com>` commit. `serving-contracts`, `inferbench`, `fleetlab`, and `inference-lab` are entirely Claude-authored by metadata; `infergate` and `inferops` each contain one differently named author record. The supplied report's "105 of 106" figure is false. (Re-verified 2026-07-15; additionally, the six repos were created within a single 14-second window and all nine CI runs occurred within one ~23-hour span — consistent with a scripted program, which an interviewer will notice.)

This is **not automatic disqualification**. Git metadata cannot establish who made the decisions, validated outputs, or can modify the system. It does mean a knowledgeable interviewer will require live, detailed ownership proof. Internal "AI verifier," "fresh-context verification," or "user accepted" wording supplies no independent validation.

### 11.2 Eight decisions the candidate must explain without reading the docs

| Decision | Minimum defensible explanation | Key code/evidence |
|---|---|---|
| 1. Response-independent open-loop scheduling | Why response-coupled issuance hides queueing; why latency begins at scheduled send; how dispatch and wire slip are detected | `inferbench@62c2704:internal/schedule/schedule.go#Build`; `internal/run/run.go#Execute` |
| 2. Gateway versus engine scheduling boundary | Why tenant admission belongs at the gateway but continuous batching/KV/token scheduling belongs inside the engine; when double queueing occurs | `infergate@f362ceb:docs/adr/0005-why-the-gateway-must-not-batch.md` |
| 3. Retry only before first token | HTTP/SSE status-commit mechanics, duplicate-token risk, staged deadline transitions, retry budget and circuit-breaker interaction | `infergate@49236a3:internal/gateway/gateway.go#streamCompletion` |
| 4. Bounded admission and fairness | Global in-flight versus per-tenant/global queue caps, priority/WRR/aging trade-offs, overload reasons, and the code-confirmed cancel/grant race | `infergate@49236a3:internal/admission/admission.go`; `fairness.go` |
| 5. Immutable config snapshots, reload and drain | Request consistency across reload, pointer/snapshot lifetime, why drain changes readiness and blocks new work, what readiness currently misses | `infergate@f362ceb:internal/config/snapshot.go`; `store.go`; `drain.go`; `gateway.go#handleReadyz` |
| 6. Contract/version/provenance boundary | Why schema shape and semantic meaning both affect SemVer; how every comparability field should be pinned; why the missing public tag breaks the claim | `serving-contracts@507208b:compatibility/compatibility-policy.md`; `inference-lab@bb0c253:pins/pins.yaml` |
| 7. Capacity fitting and holdout governance | Why the selected fit uses few points, how prediction error is computed, why 33.159 and 37.925 diverge, and why six replicas/N−1 remain unproven | `fleetlab@dd05e7d:reports/holdout-validation.md`; recommendation JSON |
| 8. Compose pivot and non-adoption of KEDA | What k3s server-only validation proves, why it proves no scheduling, how signal analysis differs from a controller, and what real HPA evidence needs | `inferops@c695425:docs/adr/0003-keda-not-adopted.md`; k3s transcript; autoscaling results |

### 11.3 Five quantitative results the candidate must re-derive

1. **Paired p95 overhead:** join 630 direct/gateway requests, compute \(d_i\), apply type-7 p95, and obtain +2.2075 ms; explain why this is not the pooled-p95 difference and why the llama.cpp arm is inconclusive (EC-06).
2. **G5 failures:** reproduce +25.16% and +26.08% from baseline/overload accepted-request TTFTs and state exactly which original threshold failed (EC-07).
3. **Capacity-loop delta:** \((33.583-33.159)/33.159=1.2787\%\); then list the changed conditions that stop this from being a strict replication (EC-10).
4. **Two-replica result:** \(4357/60.187=72.391\) rps; compare with 66.318 and 75.850, and explain why demand-capped 49.962 rps is not capacity (EC-10).
5. **Crash/fault scope:** ten crash repetitions, 26 in-flight clients, maximum 4.42 ms resolution and no observed duplicate rows; explain why `rows <= completed` does not prove no loss and why 11/12 fault scenarios does not mean production reliability (EC-08/14).

### 11.4 Five code paths to whiteboard end-to-end

1. `POST /v1/chat/completions` → request ID → auth → schema/model validation → token estimate → quota → admission → staged timeout → selector/retry → backend → settlement (`infergate:internal/gateway/gateway.go#handleChatCompletions`).
2. Streaming open → first chunk before status commit → SSE ID/data write/flush → client cancel/write failure → upstream context cancellation → usage settlement (`gateway.go#streamCompletion`, `stream/relay.go`).
3. File/DB/static configuration → immutable `Snapshot` → backend construction → `selectorFor` → why N-backend router disappears from file-config path (`config/store.go`, `snapshot.go`, `gateway.go#selectorFor`).
4. Workload JSON → seeded arrival offsets → run epoch/goroutine dispatch → scheduled/wire timestamps → raw event → warm-up → pooled percentile/goodput report (`inferbench:internal/schedule`, `run`, `client`, Python analysis).
5. Estimated usage → quota debit → backend usage/chunk observations → async PostgreSQL writer/idempotency key → settlement/recovery (`infergate:internal/usage`, `quota`, `tenant`; current crash test).

### 11.5 Claims that will expose shallow ownership

- Saying "P2C routing" without knowing that the executable constructs one node.
- Saying "warm-up readiness" without opening `handleReadyz`.
- Quoting "2 ms overhead" without distinguishing paired deltas, pooled-percentile difference, and inconclusive real-engine results.
- Calling G5 a pass without leading with the two refutations.
- Quoting six replicas without deriving headroom, N−1 deficit, fit error and the fact that six was never run.
- Calling scenario 4 a proven defect without explaining socket/kernel buffering and missing blocked-write instrumentation.
- Saying "Kubernetes validation" as if a scheduler, kubelet or HPA controller acted.
- Saying "exactly once" without defining the crash invariant and multi-gateway boundary.
- Claiming v1 release or four consumer CI runs without producing immutable refs and job URLs.

### 11.6 Synthetic / over-engineered appearance risk

Six repositories, highly uniform ADR/task/risk/testing templates, 119 commits in about 53 hours, dense acceptance vocabulary, explicit AI co-authorship, and long self-verification narratives can look generated faster than they can be personally internalized. The six repositories were created within one 14-second window and all CI activity fits one day. The absence of simple root READMEs in four component repos contrasts with very extensive internal documentation. Repeated "accepted," "verifier," and "production-grade" language amplifies that concern.

The remedy is not hiding AI use. It is pruning overclaims, adding immutable external evidence, and demonstrating live command of code, data and failure trade-offs.

### 11.7 Honest disclosure if asked

> "I used Claude/Codex as implementation and review assistants. I set the architecture, acceptance criteria and experiment scope, verified the outputs, and I can trace and change the code myself. The current evidence is self-generated; it is not production or independent external validation."

Do not claim sole hand-authorship if the public metadata says otherwise. Do not volunteer a percentage that cannot be substantiated. Focus on decision ownership, verification, and live defensibility.

---

## 12. CV framing

### Recommended title

**Experimental LLM Serving Gateway and Reliability Lab — Go, CPU llama.cpp, Single Host**

### Two-sentence project description

Built a six-repository experimental serving stack around a Go inference gateway, open-loop benchmark tooling, contract schemas, fault injection, observability and mock-backed capacity analysis. Exercised the system on one host with Docker Compose and CPU-only llama.cpp; Kubernetes work was manifest/API validation, with no GPU, vLLM or scheduled pod execution.

### Best-fit positioning

Lead with **Inference Reliability / Release / Developer Productivity**, followed by **Model-Serving Platform Backend**. The unqualified title **"AI Infrastructure Engineer" is premature as a proven current role identity**; "Backend/Platform Engineer transitioning into AI serving infrastructure" or "AI-serving infrastructure project" is defensible.

### Resume bullets

| CV bullet | Evidence IDs | Required qualifier | Overclaim risk |
|---|---|---|---|
| Built a Go LLM-serving gateway with SSE streaming, bounded admission, quotas, pre-first-token retries, circuit breaking, usage settlement and graceful drain; exercised it locally against deterministic mock and CPU llama.cpp backends. | EC-02, EC-03 | local; CPU llama.cpp; mock | LOW |
| Designed a seeded open-loop benchmark harness using scheduled-send latency and slip invalidation; recomputed paired p95 gateway TTFT overhead of 2.21 ms across 630 same-host deterministic-mock request pairs. | EC-05, EC-06 | paired; same-host; deterministic mock | LOW |
| Ran a 12-scenario single-host Docker Compose fault campaign: 11 matched expected or documented-deviation semantics, while the slow-client case failed to observe a configured three-second deadline during an eight-second reader stall. | EC-08 | single host; Compose; result is unresolved, not a proven defect | LOW |
| Measured a one-to-two-container Compose change across 3,002-request mock workloads, reducing shed fraction from 26.48% to zero at roughly 50 offered requests per second; did not execute the six-replica recommendation. | EC-10 | mock; demand-capped; six replicas unexecuted | LOW |
| Built mock-backed capacity and holdout tooling that exposed 12.6%–20.4% two-point-profile misses, then used a measured-data latency bracket instead of presenting an unfitted model as validated serving capacity. | EC-10 | mock; not real model-serving capacity | LOW |
| Versioned an OpenAPI serving contract and 12 JSON Schemas with 52 positive and 29 negative fixtures, plus explicit engine, model, workload, binary and image pins; compatibility execution remained local. | EC-12, EC-13 | local checks; no public immutable tag | LOW |
| Added a PostgreSQL-backed crash-restart test using real gateway processes; ten same-host SIGKILL repetitions resolved 26 in-flight clients within 4.42 ms maximum, with no duplicate ledger rows observed. | EC-14 | current HEAD; loopback; no proof of zero loss | MEDIUM if "crash-safe" is added |

### "DO NOT USE" list

- **"production-grade"** — no production users, traffic, SLO history, on-call, external validation or fleet.
- **"deployed on Kubernetes" / "operated Kubernetes workloads"** — no pod was scheduled.
- **"GPU inference" / "GPU serving" / "GPU optimization"** — no GPU was exercised.
- **"vLLM integration" / "SGLang adapter"** — neither was built and run.
- **"autoscaled to six replicas"** — only a manual 1→2 Compose change ran; six is extrapolation.
- **"validated at scale"** — one host, short runs, mock/CPU model.
- **"production SLO"** — targets are experimental gates, not production objectives.
- **"open-source contributor"** — no public interaction or accepted contribution is linked.
- **"multi-backend P2C serving platform"** — N-backend router is not configurable in the shipped executable.
- **"warm-up-aware readiness"** — gateway `/readyz` is drain-only.
- **"zero-downtime Kubernetes rollout"** — only same-digest Compose/HAProxy lifecycle evidence exists.
- **"exactly-once crash-safe accounting"** — current tests do not prove no lost settlements or distributed linearizability.
- **"cost-optimized inference"** — cost combines an A10G price with mock CPU capacity and no actual bill.

---

## 13. Minimum gap-closing roadmap

Each slice extends the existing system, uses a currently missing real substrate, predeclares pass/fail criteria, and archives raw evidence including negative results. Documentation-only work receives no score credit.

### Slice 1 — One real-GPU vLLM session through the existing gateway and benchmarker

- **Scope:** complete `IG-T014` and `IB-T011`; add a vLLM-specific adapter only where generic OpenAI behavior is insufficient; run direct and gateway arms on one real GPU.
- **Predeclared acceptance:** pinned GPU SKU/UUID, driver, CUDA, vLLM image/version, model/tokenizer revision and flags; randomized/interleaved ≥3 repetitions; engine request IDs join gateway/client records; test pre-first/mid/near-completion cancellation, continuous-batch growth, KV pressure and one OOM/recovery negative; collect vLLM/Prometheus metrics and profiler trace.
- **Failure rule:** if engine identifiers cannot causally join results, if load generator slip exceeds threshold, or if the OOM/recovery path is unclassified, report inconclusive/fail—not a performance number.
- **Archive:** raw JSONL, engine/gateway logs, metrics snapshots, profiler output, `nvidia-smi`/driver inventory, exact commands, bill and negative results.
- **Expected movement:** A serving/engine-integration 3→4 and total +1; C engine metrics/profiling/KV/batching 0–1→2–3 and total +2.
- **CV-safe afterward:** "Integrated and benchmarked the gateway against pinned vLLM on one GPU, measuring batching/KV/cancellation behavior under a declared workload."
- **Effort:** LARGE; **impact:** highest.

### Slice 2 — Close the platform-correctness holes on a real multi-process path

- **Scope:** make N backends expressible in the existing config/CLI; make `/readyz` depend on eligible warmed backend(s) and required control-plane state; repair and retest slow-client behavior; test the admission cancel/grant interleaving.
- **Predeclared acceptance:** two differently identified backend processes receive P2C traffic; unhealthy transition removes a backend within a stated bound; zero eligible backends forces `/readyz` non-200; reload/drain preserves in-flight streams; instrumented server write exceeds the deadline and releases upstream without materially regressing fast-client TTFT/RSS; 100k forced cancel/grant races end with zero slot drift under `-race`.
- **Failure rule:** library-only tests do not pass the slice; every key assertion must traverse the executable's public endpoint/config path.
- **Archive:** config snapshots, backend IDs per request, health timelines, race logs, write start/end/error traces, RSS and fast/slow client raw events.
- **Expected movement:** A routing/readiness/slow-client rows +1 each and total +1; B reliability total +1.
- **CV-safe afterward:** "Operated a configurable two-backend gateway with health-aware readiness, bounded drain/reload and instrumented slow-client backpressure tests."
- **Effort:** MEDIUM; **impact:** HIGH.

### Slice 3 — Schedule the existing stack and execute a real autoscaling control loop

- **Scope:** run the current Kustomize stack on a real kind/k3s cluster with agents; use the corrected readiness; execute distinct-digest rollout/rollback, PDB disruption and HPA or KEDA scaling under inferbench load.
- **Predeclared acceptance:** pods schedule and become Ready only after backend warm-up; HPA/KEDA produces documented metric observations and scale decisions; scale-out reaches ready capacity before a stated SLO breach or is reported failed; one worker/pod loss produces measured rescheduling and client impact; PDB blocks an unsafe voluntary disruption; rollback restores the prior digest.
- **Failure rule:** `kubectl apply`/schema validation alone is failure. Archive controller events even if oscillation, missing metrics or readiness races occur.
- **Archive:** cluster/node versions, manifests, image RepoDigests, full events, HPA status series, pod timelines, client raw JSONL, metrics and rollback transcript.
- **Expected movement:** D scheduling/control-loop/lifecycle rows 0–1→3 and total +2; A/B total +1.
- **CV-safe afterward:** "Scheduled and autoscaled the serving stack on a real Kubernetes cluster, measuring readiness, rollout, disruption and client-impact timelines."
- **Effort:** MEDIUM–LARGE; **impact:** HIGH.

### Slice 4 — Close capacity and cost on the measured vLLM substrate

- **Scope:** feed Slice 1's real vLLM results into fleetlab; replace the two-point mock profile; execute the predicted replica count and N−1 case on the real cluster; calculate actual cost/output-token.
- **Predeclared acceptance:** ≥3 offered-rate levels around knee, ≥3 randomized repetitions per level, run-level/cluster bootstrap interval, predeclared holdout rates, prediction error threshold selected before viewing holdout, explicit hardware/model sensitivity, SLO-goodput denominator, executed N and N−1, actual billed GPU-seconds and successful output tokens.
- **Failure rule:** linear extrapolation is rejected when observed N-replica error exceeds threshold; an unexecuted recommendation remains a model artifact, not capacity evidence.
- **Archive:** all raw runs, fit code/output, holdout decisions, cluster topology, cost source/bill, predicted versus observed table, negative points and sensitivity analysis.
- **Expected movement:** capacity 2→3–4, cost 1→3, performance methodology 3→4; A/C totals +1.
- **CV-safe afterward:** "Fit and holdout-validated a vLLM capacity profile, executed the predicted replica count and measured cost per output token on the pinned GPU configuration."
- **Effort:** LARGE; **impact:** HIGH.

### Slice 5 — Publish one reproducible, immutable cross-repository release

- **Scope:** repair the existing release path rather than add documents: actual immutable Git tags/releases, clean-checkout builds, public registry RepoDigests, six-repo CI compatibility matrix, SBOM/vulnerability gate and signed provenance. (If the KI-1 tag-push constraint persists in the build environment, cut tags from an environment that can push them — the constraint is real but the fix is operational, not architectural.) Also fix the two portability defects this audit surfaced: the fleetlab one-ULP exact-equality assertion (use `math.isclose`/ULP tolerance) and the hard-coded `/home/user/*` sibling paths in the tier-2 corpus tests.
- **Predeclared acceptance:** a third party can resolve the tag, pull every image by RepoDigest, verify signature/attestation, reproduce contract fixtures, run the quickstart, see exact CI jobs for all six SHAs, and execute a distinct-digest rollback. Any dependency or action not pinned by immutable revision fails the release gate.
- **Archive:** workflow URLs, release manifest, SBOMs, scan outputs including accepted exceptions, signatures/attestations, build logs and rollback transcript.
- **Expected movement:** B delivery/supply-chain 1–2→3–4 and total +1; A release-boundary confidence +1.
- **CV-safe afterward:** "Published a reproducible six-repository release with immutable component refs, pullable image digests, cross-consumer CI, SBOMs and verified rollback."
- **Effort:** MEDIUM; **impact:** HIGH for B.

Priority order by hiring impact-to-effort is **Slice 2 → Slice 1 → Slice 3 → Slice 5 → Slice 4**. If only one major investment is possible, choose **Slice 1** because it removes the most damaging "AI infrastructure without an AI runtime substrate" objection. If interviews are imminent, complete Slice 2 first because it is smaller and closes claims that are currently factually unsafe.

---

## 14. Final verdict

| Family / level | Score | Decision | Strongest evidence | Decisive blocker | What moves it at least +1 |
|---|---:|---|---|---|---|
| **A mid-level** | **6/10** | MAYBE | Reachable Go gateway, streaming/retry/cancel boundaries, admission, auth/accounting, OTel and Compose lifecycle (EC-02/03/09) | Executable is single-backend; readiness claim is false; no real serving fleet/GPU/Kubernetes | Slice 2 or one end-to-end vLLM/GPU deployment with N-backend routing |
| **A senior** | **4/10** | NO | Coherent platform boundaries and evidence discipline | No production/external scope, multi-node control plane, model lifecycle, fleet rollout or representative substrate | Real multi-node serving platform plus operational/external evidence; one GPU session alone is insufficient |
| **B mid-level** | **7/10** | SHORTLIST | Open-loop harness, raw/recomputed measurements, preserved failures, fault campaign, current crash CI (EC-05–08/14) | Five repos lack CI; release ref is broken; short single-host/self-authored operational evidence | Slice 2 plus immutable cross-repo release, or Slice 5 alone if executed cleanly |
| **B senior** | **5/10** | MAYBE | Good methodology and reliability instincts | No production incident ownership, deploy-gate adoption, organization-wide tooling, on-call or external users | Real Kubernetes rollout/autoscaling plus public release use or independent consumer evidence |
| **C mid-level** | **4/10** | NO | Benchmark design, TTFT/ITL/goodput analysis, CPU llama integration (EC-03/05/06) | No vLLM/SGLang, GPU, profiling, batching/scheduling/KV mechanics or bottleneck intervention | Slice 1 with causal engine metrics/profiler evidence; should move +2 if complete |
| **C senior** | **2/10** | NO | Awareness of engine/gateway boundary | No engine internals, kernels, distributed runtime, accelerator efficiency or cost optimization | Multiple representative GPU/runtime interventions, not one benchmark session |
| **D mid-level** | **2/10** | NO | Kustomize manifests and k3s API validation (EC-11) | No node, pod, scheduler, controller, device plugin, GPU or failure/reschedule execution | Slice 3; real scheduling/HPA/PDB/node-failure evidence should move +2 |
| **D senior** | **1/10** | NO | Honest statement that the cluster did not run workloads | No cluster operations, multi-node, accelerator fleet, controller/operator or on-call evidence | Sustained real cluster/device-plugin/operator work; a single local cluster is not enough |

### Required final answers

1. **Single best-fit family today:** **B — Inference Reliability / Release / Developer Productivity Engineer**, especially benchmark/regression/fault-tooling work adjacent to serving systems.
2. **Single most damaging gap:** **no representative AI-serving substrate—no real GPU and no executed vLLM/SGLang path**.
3. **Single highest-leverage next change:** **one fully pinned, scripted real-GPU vLLM vertical slice through infergate + inferbench, with engine-correlated cancellation, batching/KV pressure, profiling and raw evidence**.
4. **Most truthful one-sentence CV positioning:** "Backend/platform engineer transitioning into AI-serving infrastructure through a single-host Go gateway, reliability and benchmarking portfolio exercised with mock backends and CPU llama.cpp."
5. **Does the portfolio currently make the transition credible?** **Yes, narrowly and role-specifically:** credible for mid-level B and selected A interviews when qualified honestly; not credible today for C, D, senior AI-infrastructure, GPU, Kubernetes-operations or production-platform claims.

---

## Appendix A. Exact commit aliases used in citations

| Short alias | Full commit |
|---|---|
| `inference-lab@b940f5c` | `b940f5c15209127217f515afb7a72102a7544623` |
| `inference-lab@c5cf6b7` | `c5cf6b774fc6f9e2950398308a274cf135e86e32` |
| `serving-contracts@507208b` | `507208b25737470b9eb2f9553a5c55f8f535f1d5` |
| `infergate@49236a3` | `49236a3e38850474fad63ff2cca4065f8cf6feed` |
| `infergate@f362ceb` | `f362ceb7835c91182f19645a705de66af3017c82` |
| `infergate@74f2372` | `74f2372acea62645fa3c1d91689574ea9de7c589` |
| `inferbench@62c2704` | `62c2704997e6c8a2966307ee3d8dbfd16747b631` |
| `inferbench@69a5abc` | `69a5abc604a737235ea3f1721ddb6b7f64334289` |
| `inferbench@caa5074` | `caa507498fa417b3e4f5cdb0285737ef3f36856e` |
| `fleetlab@dd05e7d` | `dd05e7decca5a998afdf496d1c439141caba5a29` |
| `inferops@89871a6` | `89871a64d35bab9450481ff1afdd19ad8310a9d9` |
| `inferops@a07fd2f` | `a07fd2ff35a1c6a7d26a596fd95365bf884595bd` |
| `inferops@c695425` | `c6954256fcbce3e8f0a5a8ff955598dbea5e2e6c` |
| `inference-lab@bb0c253` | `bb0c2537295bb77b5659518c544db9167abb1b06` |

## Appendix B. Audit cautions

- Dependency- or optional-sibling-gated tests are reported as skips, not silently promoted to passes. The fleetlab one-ULP equality failure is counted as a real brittleness defect, with the qualification that it is environment-bound: it fires under Python 3.12's compensated float summation and passes bit-exactly under Python 3.11. The defect is the exact-equality assertion, not the model.
- Existing raw artifacts are candidate-generated. They are stronger than narrative reports but not independent industry validation.
- Hardware/model/engine/workload results are comparable only under the portfolio's own full pin rule. No cross-configuration generalization is made here.
- A passing self-authored test establishes behavior under that test, not production scale, organizational adoption or completeness of the state space.
- Post-release current-head evidence is credited to readiness today only; it never retroactively repairs the advertised v1 release.

## Appendix C. Corrections applied in Revision 3 (independent re-verification, 2026-07-15)

The re-verification pass reproduced every quantitative and forensic claim in Revisions 1–2 except the items below, which are now corrected in place:

1. **infergate race-clean package count: 17 → 16.** `go test -race ./...` covers 16 tested internal packages (admission, api, auth, backend, backend/llamacpp, config, conformance, gateway, mockengine, quota, reliability, route, stream, telemetry, tenant, usage) plus three `cmd/*` packages with no test files. (§1)
2. **fleetlab test failure is Python-3.12-specific.** 296/1/4 under Python 3.12.13; 297/0/4 under Python 3.11.15. Root cause identified: CPython 3.12's Neumaier compensated float `sum()` (gh-100425) shifts `dynamics/cold_start.py`'s mean by one ULP, breaking the exact-equality assertion at `tests/dynamics/test_build_scenarios.py:59`. All occurrences now carry the qualifier. (§0, §1, §3.17, §5.3, §7, Appendix B)
3. **Market-calibration titles, levels and geography corrected.** Anthropic 5101169008 is "Staff Software Engineer, AI Reliability Engineering" (Dublin); 5257650008 is "Staff+ Software Engineer, Inference Runtime"; 5211241008 is "Senior Staff+ Software Engineer, Kubernetes Platform"; 4641822008 is Senior, Dublin. Baseten is "Software Engineer – Infrastructure"; Modal is "Member of Technical Staff – Platform Engineering." The exact `openai.com` slug for the Productivity–Inference-Runtime posting could not be confirmed (the posting exists via OpenAI's Ashby page and mirrors). A calibration caveat is added: the sample skews Staff+/Dublin, which makes this audit's mid-level verdicts conservative. (§4)
4. **KI-1 context added to the tag findings.** The repositories publicly disclose that the session git proxy dropped tag pushes (serving-contracts `RELEASES.md`, `pins/pins.yaml`) and designate `release/<version>` branches as pinnable refs. The FALSE verdict on the FINAL-REPORT wording stands — the report cannot have existed "at" a commit that predates it, and its status line carries no caveat — but intent should be read as sloppy release wording over a disclosed limitation, not concealment. (§0, §5.1, §5.3, EC-01, §9 Q12)
5. **`pins/pins.yaml#I8` removed as a source for the tag@b940f5c claim.** pins.yaml contains no such wording; the claim lives only in `FINAL-REPORT.md`. (§5.3)
6. **Scenario-4 citation corrected.** `faults/scenario-04/verdict.md` has no "Observed" heading (its sections are Part A / Part B / Verdict / Client impact); the "Observed" cell is the scenario-4 row of `faults/campaign-matrix.md`. Substance unchanged. (§3.3, §9 Q3)
7. **39.25 rps disclosure noted.** The actual client-observed offered rate of the I6 re-measurement is disclosed in `experiments/autoscaling/results.md` §2.1; only the §4.1 headline comparison row uses the planned 37.8072. The replication criticism stands; the implication that the true rate was buried in raw evidence does not. (§3.10, recomputation note 3)
8. **Admission race upgraded from INFERENCE to code-confirmed.** Code reading (release and main, byte-identical) confirms no grant-drain exists on the cancel path and the in-code "harmless unread value" comment is wrong for grants; the leak remains unreproduced at runtime and no test forces the interleaving. (§3.4, §7, §8.8, §9 Q4, §11.2)
9. **Minor precision fixes.** infergate's workflow name is `ci` (lowercase) (§5.4); the GPU overlay declares `nvidia.com/gpu` under `limits` (the standard extended-resource form), not `requests` (§7, EC-11); the fleetlab CI phrases "green in CI" / "on every push" are verbatim, the inferbench ones near-verbatim (§5.4); the fleetlab recommendation's A10G linkage is via `cost_profile_ref` → hardware profile (one hop), with the emitter's own "ILLUSTRATIVE ONLY" admission now quoted (§3.9, §7); `oss/log.md`'s own candour ("not met as of this release") is credited in §5.3.
10. **Verified-fact strengthenings folded in:** the six repositories were created within one 14-second window (23:57:44–58Z, 2026-07-10) with all nine CI runs inside one ~23-hour span (§11.1, §11.6); the ≤20% G5 criterion is pre-declared in a committed hypothesis file (§3.8, EC-07); the E1 recomputation was re-reproduced to float precision including the 65/630 negative-delta count (EC-06); the failover `upstream_error` terminated ~230 ms after the kill timestamp (recomputation note 9); the uncommitted RQ-14 probe report is cited in six-plus committed locations (§5.3).
