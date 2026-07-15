# Evidence-Backed Hiring Audit — Backend Engineer → AI Infrastructure / Platform Engineer

**Audit date:** 2026-07-15
**Auditor:** independent read-only audit (two-pass: hiring manager + skeptical staff engineer, then reconciled)
**Scope:** the six-repository `inference-systems` portfolio under `github.com/duy-tung`
**Method:** full clones with complete history; code-path tracing; test suites re-run; headline numbers recomputed from raw archived events where present; live GitHub Actions state checked via API; market sample of current job descriptions.

Everything below is tagged where it matters: **[VERIFIED]** (checked directly against code, raw evidence, or recomputation), **[INFERENCE]** (judgment from verified facts), **[UNVERIFIED]** (claim found in documents but not independently checkable from published artifacts).

---

## 0. Executive verdict (read this first)

- **Best-fit role family today:** B — Inference Reliability / Release / Developer-Productivity Engineering, closely followed by A — AI Platform / Model-Serving Platform (with the "serving platform" claim heavily qualified to CPU + Docker Compose).
- **The portfolio is methodologically excellent and substrate-poor.** The measurement discipline, failure-analysis honesty, and contract-first architecture are genuinely rare. But no GPU, no vLLM, no scheduled Kubernetes pod, no autoscaling controller, no multi-node system, and no production traffic exist anywhere in the evidence — and role families C and D are scored accordingly low.
- **The single most damaging gap for hiring:** everything runs on a substrate (CPU llama.cpp + Docker Compose, single host) one level below what every sampled job description asks for (vLLM/GPU + real Kubernetes).
- **The single most damaging gap for credibility of ownership:** 105 of 106 commits are authored by `Claude <noreply@anthropic.com>` over a 72-hour window. The work is defensible only if the candidate can personally re-derive the key results and trade-offs (§6).
- **Blunt answer to "does this make the transition credible?"** — Partially. It makes the *platform/reliability* half of the transition credible at mid-level; it does not yet make "AI Infrastructure Engineer" in the GPU/runtime sense defensible. One scripted GPU+vLLM session and one real kind/k3s cluster with scheduled workloads would change that materially (§8).

---

## 1. Snapshot and claim-integrity audit

### 1.1 Snapshot manifest [VERIFIED]

Fetched 2026-07-15 (full history, all remote branches and tags):

| Repo | main HEAD (= audited current-head scope) | Release refs on GitHub | Commits | Last commit (UTC) |
|---|---|---|---|---|
| serving-contracts | `507208b` | `release/v0.1.0`=`2df9f81`, `release/v0.2.0`=`484b449`, `release/v1.0.0`=`507208b` (= main) | 16 | 2026-07-12 00:12 |
| infergate | `f362ceb` | `release/v0.1.0`=`49236a3` | 33 | 2026-07-11 23:06 |
| inferbench | `62c2704` | none | 13 | 2026-07-11 23:08 |
| fleetlab | `dd05e7d` | none | 18 | 2026-07-11 22:21 |
| inferops | `c695425` | none | 13 | 2026-07-12 02:56 |
| inference-lab | `bb0c253` | `release/v1.0.0`=`bb0c253` (= main) | 26 | 2026-07-12 05:23 |

**Published-release scope:** `inference-lab@v1.0.0` is claimed as an annotated tag on `b940f5c` (FINAL-REPORT.md line 3). **No tag of any kind exists on any of the six GitHub remotes** [VERIFIED via `git fetch +refs/tags/*`]. The program's own planning log (ai-infra `program-state.md`, KI-1) records that the session git proxy silently dropped tag pushes and `release/<version>` branches were pushed as pinnable substitutes. Consequences:

1. An external reviewer cannot verify "v1.0.0" as a tag at all; the only public pinnable ref, `release/v1.0.0`, points at `bb0c253` — **two commits past** the claimed tag commit `b940f5c` (it includes FINAL-REPORT.md itself and the acceptance-note commit).
2. `serving-contracts` "tag v1.0.0 (tag object 64c3205…)" cited in `pins/pins.yaml` is likewise unverifiable publicly; `release/v1.0.0` = `507208b` matches the claimed tag commit, so the pin is recoverable, but the annotated-tag object is not public.
3. All milestone-pinned component commits named in `pins/pins.yaml` and `program-state.md` (e.g. infergate `5d69aeb`, `74f2372`, `49236a3`; inferbench `caa5074`, `69a5abc`, `6a3fb53`, `cc404a6`; fleetlab `dd05e7d`; inferops `135dd34`…`db30279`, `f5fdd86`, `89871a6`) **exist in the public history** [VERIFIED against `git log` of all six repos].

**Current-HEAD vs release pins:** infergate main (`f362ceb`) is 3 commits past its released `v0.1.0` (`49236a3`) — the delta is IG-T017 (stale-health experiment), IG-T018 (crash recovery), and an ADR finalization; all evidenced at HEAD, none claimed retroactively for v0.1.0. `compatibility/matrix.md`'s "Current component state" table states these drifts accurately [VERIFIED].

### 1.2 CI claims [VERIFIED]

- **infergate is the only repo with CI.** `.github/workflows/ci.yml` runs gofmt, `go vet`, `go test -race ./...` against a real `postgres:16-alpine` service, a 10×-consecutive streaming/conformance stability gate, and the IG-T018 crash-recovery integration test. GitHub Actions shows **9 runs, all `success`**, including HEAD `f362ceb` (2026-07-11T23:06Z) and the release commit `49236a3`. This is the portfolio's only *independent-infrastructure* execution evidence, and it is genuine.
- **Five repos have zero CI on GitHub**, while their docs speak of CI as though wired: fleetlab `docs/testing.md` ("both wired into `make check`, green in CI", "CI … runs the full suite … on every push"), inferbench `docs/testing.md` ("CI validates both directions"), inferops `docs/testing.md` ("CI must be able to spin the kind cluster" — kind was never installed), serving-contracts `docs/testing.md` ("CI matrix"). The underlying checks demonstrably pass when run locally (§2), but **any CV or interview statement about "CI" is only true for infergate**.

### 1.3 Claim-consistency ledger (cross-document)

| Claim | FINAL-REPORT | limitations.md | pins.yaml | Reality check | Verdict |
|---|---|---|---|---|---|
| v1.0.0 tagged at `b940f5c` | stated | — | stated (SC tag object cited) | no public tag; release branch 2 commits ahead | **Stale/unverifiable ref** [VERIFIED] |
| "User accepted I4–I8" | stated (accepted 2026-07-12) | says "acceptance-review-pending" (§7) | I5–I8 entries say "ACCEPTED BY USER 2026-07-12" | limitations.md §7 and inference-lab README status block written before `bb0c253`; one commit stale | Minor staleness, disclosed pattern |
| G5 admission gate | "REFUTED twice … re-baselined" | same | same | matches raw reports; re-baseline decision was the program owner's own call (see §2.6) | **Consistent and honest** [VERIFIED] |
| G8 capacity holdout | "documented MISS (12.6–20.4%) for the ib-t010 corpus" | same | — | holdout-validation.md splits per-config: ib-t008 sweep WITHIN error (+0.7/−0.4% interior, ±7% hard), ib-t010 2-point MISS 12.6–20.4%. Coherent split, but ai-infra `program-state.md` §2 headline "G8 = capacity holdout within stated error" omits the MISS | **Consistent inside the portfolio; the planning repo's roll-up is optimistic** [VERIFIED] |
| 3-point cancellation on real engine | narrowed: 1 point composed-stack pinned model; 3 points adapter-level on unpinned tiny GGUF | same, §2 | engine-llamacpp pin notes the same | matches infergate + i3/i4 evidence | **Consistent, honestly narrowed** [VERIFIED] |
| "Deployed and operated on Kubernetes" | qualified | qualified §1 | qualified | k3s API-server-only validation; 0 pods ever scheduled; HPA `REPLICAS 0`, `TARGETS <unknown>` [VERIFIED from inferops evidence] | Qualified everywhere it appears — but the phrase itself should never appear on a CV (§7) |
| OSS contribution | "drafted, not posted" | same | — | oss/log.md table: 0 of 4 minimum targets met | **Honest; capability NOT DEMONSTRATED** |
| "production-grade" | — | — | — | inference-lab README line 5: "one production-grade LLM inference-serving platform"; portfolio/README.md positioning quote: "production-grade distributed AI inference" | **Overclaim relative to own limitations.md** (no production traffic, users, or on-call exist) [VERIFIED] |

### 1.4 Missing/asymmetric artifacts [VERIFIED]

- **Four of six repos have no top-level README on GitHub** (infergate, inferbench, fleetlab, inferops — LICENSE/RELEASES only). In a 10–15-minute recruiter pass, four of the six links land on a bare file listing. This is the single cheapest fix in the whole portfolio.
- The RQ-14 root-cause artifact `"/home/user/tools/k8s-env-probe-report.md"` cited as proving the "runc/nsexec-level" impossibility of pod scheduling is **not committed anywhere** — the consequence (pods Pending, 0 nodes) is evidenced, the mechanism is not inspectable.
- The "8 workloads / ~13.4k events" fleetlab ingestion headline is verifiable only in a tier-2 test that **skips** unless sibling repos are checked out at the orchestrator's paths; the committed corpus subset is 3 workloads.
- Benchmark reports 1/1b headline numbers (+2.21 ms p95 overhead, +25.16 %/+26.08 % TTFT, 134 ms queue-wait p95) are archived as *reports*; their full raw run directories live in inferbench evidence paths, only partially re-archived (§2.6 states what was and wasn't recomputable).

---

## 2. Role-fit and competency map

*(placeholder — filled in §2 of final assembly)*

---

## MARKET CALIBRATION (supporting data for §2 and §9)

Sampled 2026-07-15. Primary pages where fetchable; two postings only via job-board mirrors of the official text and one recently closed — disclosed per row. This is a spot sample, not a survey.

| # | Role (family) | Source | Key requirements extracted |
|---|---|---|---|
| 1 | GM — Senior ML Infrastructure Engineer, Inference Platform (A) | gm.com careers [primary, fetched] | 5+ yrs ML systems/high-perf backend; serving frameworks (Triton, RayServe, vLLM); serving strategy, versioning, autoscaling, caching; observability; GPU acceleration preferred |
| 2 | Red Hat — Forward Deployed Engineer, AI Inference (A/D) | Workday posting via BuiltIn mirror [official text; listing removed 2026-06-22] | deploy llm-d + vLLM on k8s; disaggregated serving, KV-cache-aware routing; benchmarks to SLOs (incl. TPOT); k8s operators/CRDs + GPU workload scheduling; LLM forward pass/KV cache/continuous batching literacy; Helm/Terraform; OSS contributions preferred |
| 3 | Anthropic — Staff+ SWE, Inference Runtime (C) | greenhouse.io [primary, fetched] | accelerator-agnostic runtime (Rust/Python); profiling + latency optimization at scale; depth in CUDA/GPU, TPU, or Trainium; SLO definition and measurable improvement |
| 4 | Anthropic — Staff/Senior SWE, Inference Deployment (B) | greenhouse via Accel board mirror [official text] | deployment/release infra at scale; k8s; canary/soak, blue-green, automated rollback; capacity-aware scheduling; cycle-time reduction |
| 5 | NVIDIA — AI Inference Performance Engineer, New College Grad 2026 (C) | jobs.nvidia.com [primary; JD body not bot-fetchable — existence/title only] | (title-level: inference perf engineering) |
| 6 | OpenAI — Software Engineer, Model Inference (A/C) | openai.com/careers [primary; 403 to bot — existence/title only] | — |
| 7 | CoreWeave — Senior GPU Infrastructure Software Engineer (D) | official posting via WTTJ mirror snippet | Go/Python services against k8s; custom controllers/operators; infra testing/validation automation |

Cross-family recurring requirements: deep Kubernetes (operators/CRDs, GPU scheduling), a real serving framework (vLLM first), GPU familiarity, benchmark-to-SLO work, observability, Python+Go, IaC, OSS contribution as a differentiator.
Runtime/performance-specific: accelerator-ecosystem depth (CUDA/TPU/Trainium), profiling, batching/KV internals.
Platform/reliability-specific: release pipelines, canary/rollback, capacity-aware scheduling, deployment velocity/SLO metrics.
GPU/K8s-infra-specific: GPU Operator/device plugins/DRA, bare-metal, RDMA; controllers as code.

**Calibration conclusion [INFERENCE]:** the portfolio's strongest overlaps are with rows 4 and 1 (release safety, gates, measurement, serving-platform mechanics minus GPU); its weakest are rows 2, 3, 7 — every one of which hard-requires the exact substrates this portfolio never touched (vLLM-on-k8s, accelerator depth, real cluster operations).

---

*(Sections 2–9 assembled below after per-repo verification results.)*
