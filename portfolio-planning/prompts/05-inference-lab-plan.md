# inference-lab — Standalone Planning & Implementation Prompt

You are working on the repository **inference-lab**, the integration, evidence, demonstration, and portfolio-narrative repository of the **inference-systems** portfolio. This prompt is self-contained: everything you need is embedded here. Do not assume access to the master planning repo.

---

## 1. Mission & context

**Program.** The inference-systems portfolio is a set of six independent, composable repositories that together form one production-grade LLM inference-serving platform, and that individually demonstrate senior-level engineering judgment: `serving-contracts` (versioned specs/schemas, no runtime logic), `infergate` (the only gateway, Go), `inferbench` (the only load-generation + benchmark-analysis system, Go + Python), `fleetlab` (explainable capacity/autoscaling/cost/placement simulation, Python), `inferops` (the only Kubernetes/observability/chaos/runbook repo), and `inference-lab` (this repo). Repos integrate only via versioned contracts, released artifacts, files, or documented network protocols.

**Target positioning of the portfolio (verbatim program goal):**

> Senior Backend / Platform Engineer capable of designing, building, benchmarking, operating, and reasoning about production-grade distributed AI inference infrastructure, with particular strength in streaming correctness, backpressure, scheduling boundaries, observability, capacity planning, reliability, and infrastructure orchestration.

**This repo's purpose.** Integration, research, evidence, demonstrations, and portfolio narrative. It contains **NO core runtime logic**; it orchestrates released artifacts only (compose files, scripts, pinned versions). It must never become a monolith and must never duplicate any capability owned elsewhere.

**Independent value.** A stranger can clone this repo alone and get: a working ≤15-minute GPU-free quickstart of a real gateway+mock+PostgreSQL+OTel stack, honest benchmark and capacity reports, postmortems, a compatibility matrix stating exactly which versions are proven together, and a readable portfolio narrative. Quickstart + evidence + narrative has standalone reader value.

**Integration value.** inference-lab is the pure sink of the dependency graph: it archives evidence for all eight integration milestones (I1–I8), owns the version-pin matrix and compatibility matrices (the single source of "what is proven together"), and orchestrates the five end-to-end scenarios — including Scenario E, the central integration story of the whole program.

**The five integration scenarios (owned here):**

```text
A. infergate → mock backend → PostgreSQL → OTel                        (correctness spine, GPU-free)
B. infergate → llama.cpp → inferbench                                  (first real engine, CPU)
C. infergate → vLLM → inferbench → observability                       (GPU path)
D. inferops → infergate → vLLM → OTel/Prometheus/Grafana/Tempo         (operated on K8s)
E. inferbench results → fleetlab → deployment recommendation → inferops → repeated benchmark
                                                                       (THE central integration story)
```

**The final portfolio narrative this repo must make demonstrable, sentence by sentence, with evidence (embed verbatim in the landing page):**

> "I built a correct serving gateway. I measured the gateway and engine independently and together. I converted measurements into capacity decisions. I deployed and operated the system on Kubernetes. I injected failures and documented recovery. I contributed reproducible evidence or a fix upstream."

**This repo owns:** the machine-readable version-pin matrix; the local quickstart (fresh clone → running Scenario A in ≤15 minutes on a GPU-free machine); end-to-end orchestration of scenarios A–E; demo scenarios and scripts; reports; diagrams; the ADR index across the portfolio; the postmortems archive; compatibility matrices (which released versions are proven together, per integration milestone); the portfolio landing page; technical articles; the demo video script; the curriculum/study progress tracker; the OSS activity log.

**This repo does not own:** any core runtime logic, any duplicated capability, gateway/bench/simulation/ops source. It composes released artifacts. Runtime defects discovered here are routed to the owning repo, never fixed here.

---

## 2. Hard rules (program-wide, non-negotiable)

1. Repos integrate ONLY via versioned contracts, released artifacts, files, or documented network protocols. The dependency graph is acyclic. No shared application library anywhere.
2. One gateway (**infergate**), one load-generation system (**inferbench**), one deployment stack (**inferops**) exist in the whole program — never duplicate any of them. inference-lab in particular must never grow a second copy of any capability.
3. No Kafka/NATS/Redis or any broker in the synchronous inference request path.
4. The gateway never owns continuous batching, per-token scheduling, KV-cache internals, prefix-cache internals, or GPU placement — those are engine-owned. (Basis: vLLM V1's scheduler is a token-budget scheduler; a second scheduler in front of it is the "double-queuing" anti-pattern. This boundary is also the thesis of portfolio article #1.)
5. Basic development and CI must not require a GPU. Any GPU session requires a written hypothesis + full config manifest + auto-stop script + budget alert. Program GPU envelope ~$150–250 total (as of 2026-07; user-confirmable).
6. Evidence rules: never claim tests/benchmarks/deployments succeeded without command output or artifacts to point at; every number carries provenance (measured / source-reported / assumed) and a date; invalid benchmark runs are invalidated, never published; `go test -race` clean is the floor for all Go concurrency work (relevant here only for glue scripts, if any are Go).
7. Volatile ecosystem facts (engine metric names, upstream repo layouts, GPU prices, OTel GenAI semconv status) carry "as of 2026-07 — re-verify at use time" flags. This repo's pins file and OSS log are where many of those re-verifications get recorded.

---

## 3. Dependencies & contracts

### Consumes

| Provider | Mechanism (never a source import) |
|---|---|
| serving-contracts | pinned released spec bundle (SemVer tag); compatibility matrix + pins reference it |
| infergate | released container images by digest (gateway + mock-backend) + deployment descriptor + capability descriptors |
| inferbench | released binary/version; benchmark-result + raw-event files; reports |
| fleetlab | capacity-recommendation files + reports |
| inferops | released manifests/config bundles, dashboards, runbooks, campaign logs |
| all five | released artifacts, result files, reports — archived here as milestone evidence |

### Provides

- Version-pin matrix (machine-readable) — the authoritative record of which contract bundle, image digests, engine versions, model revisions, and config bundles are proven together per milestone.
- Scenario compose files/scripts, quickstart, demo scripts, evidence archive, compatibility matrices, landing page, articles, postmortems archive, ADR index, study tracker, OSS log.

### Forbidden edges (checked at every review gate)

- `inference-lab` → anything **as a library**: orchestration of released artifacts only. Never check out another repo's source to build it; never vendor another repo's code; never patch a component here.
- inference-lab is a **pure sink**: no other repo may depend on inference-lab artifacts at build time.
- Runtime fixes are routed to the owning repo (infergate/inferbench/fleetlab/inferops/serving-contracts) as defect reports with evidence; this repo waits for the next release and bumps its pin.

### Contract summaries this repo touches (bundle owned by serving-contracts, pinned by tag)

- **Contract 1 — Inference API (OpenAI-compatible subset):** `POST /v1/chat/completions` (stream + non-stream), `GET /v1/models`, `/healthz`, `/readyz`, `/metrics`. Enumerated supported request fields (`model`, `messages`, `max_tokens`/`max_completion_tokens`, `temperature`, `top_p`, `stream`, `stream_options.include_usage`, `stop`, `seed`, `user`); unsupported fields rejected with typed errors, never ignored. SSE: `data: <json-chunk>` events, terminal `data: [DONE]`, usage in final chunk when requested, no cross-request interleaving. Error envelope `{"error": {"message", "type", "code", "param"}}` + request ID; taxonomy includes `rate_limited` (429 + `Retry-After`), `overloaded` (503), `canceled`, etc. Cancellation: client disconnect propagates upstream; observable engine release is part of conformance; tokens emitted before cancel are billable. Used here by: quickstart smoke calls, demo scripts, scenario checklists.
- **Contract 2 — Metrics/trace vocabulary:** canonical Prometheus names (`inference_ttft_seconds`, `inference_itl_seconds`, `inference_queue_depth`, `inference_sheds_total`, …), low-cardinality label policy, OTel GenAI semantic-convention trace attributes at a **pinned version** (semconv status "Development" as of 2026-07 — re-verify), gateway span sequence `recv → queue.wait → upstream.connect → ttft → stream.relay → settle`. TTFT = first upstream body byte at gateway; client-side TTFT (inferbench) is a separate named series. Used here by: scenario evidence (traces/dashboards must show these names), I2 acceptance.
- **Contract 3 — Benchmark data:** workload schema (8 named workloads: `chat-short`, `rag-long-in`, `gen-long-out`, `shared-prefix`, `mixed`, `bursty`, `cancel-storm`, `slow-client`; seeded, versioned); benchmark-run manifest (engine version/commit + all flags, model revision + tokenizer, hardware/driver/CUDA, gateway + config version, warm-up policy, repetition count, hypothesis); raw-event JSONL per request; benchmark-result with pooled percentiles (never averaged across runs), goodput@SLO with shed rate adjacent, validity block. Used here by: archived reports, reproducibility audit, compatibility matrix comparability rule.
- **Contract 5 — Deployment:** image + digest, ports, env/config mounts, warm-up-aware readiness, model mount, resources incl. GPU, `preStop` drain with termination grace > max stream duration, secrets. Used here by: pins file entries and scenario D evidence.
- **Contract 6 — Fault scenarios:** 12 scenarios with expected gateway semantics and client-visible behavior (1 backend killed pre-first-token; 2 killed post-first-token; 3 slow backend; 4 slow client; 5 gateway termination during streaming; 6 queue saturation; 7 retry storm; 8 config reload under traffic; 9 usage-DB failure; 10 one unhealthy backend; 11 readiness during warm-up; 12 rolling update with active requests). Used here by: postmortems and the I7 campaign-evidence archive.
- **Contract 7 — Capacity recommendation (fleetlab → inferops):** input references (benchmark-result IDs, workload version, SLO, cost profile, hardware profiles); recommended topology (replica counts, engine config); predicted goodput/latency/cost **with stated uncertainty**; autoscaling signal + thresholds; assumptions and sensitivity notes. Used here by: Scenario E loop evidence (I6) — the recommendation file is a first-class evidence artifact.

**Version-pinning rules this repo enforces (the pins file is the ledger):** contract bundle by SemVer tag; infergate + mock-backend images by digest + tag; engine versions (vLLM v0.24.x baseline + exact commit; llama.cpp commit; SGLang commit if ever used — all as of 2026-07, re-verify); model checkpoint revision + quantization + tokenizer hash; driver/CUDA per GPU run; inferops dashboard/collector config bundle tags. **Benchmark comparability rule (normative, print in the compatibility matrix):** results are comparable only when model revision, quantization, tokenizer, engine version+flags, hardware, driver/CUDA, workload version+seed, and warm-up policy all match, or the difference is the single declared experimental variable.

---

## 4. Architecture guidance

**Components (all declarative/orchestration — no services, no daemons):**

- `pins/` — machine-readable pin matrix (YAML or JSON; one entry per artifact with tag, digest, provenance, date, and the milestone(s) it is proven at).
- `scenarios/a` … `scenarios/e` — one directory per scenario: compose file(s) or invocation scripts referencing pinned images/versions only, a README stating purpose and expected outcome, and an acceptance checklist mirroring the owning milestone's criteria.
- `quickstart/` — the ≤15-minute GPU-free path (Scenario A), with a timed dry-run procedure.
- `evidence/i1` … `evidence/i8` — archived milestone evidence: run logs, raw-event files, trace exports, dashboards, manifests, checklists. Evidence is immutable once a milestone is accepted; corrections are new dated entries.
- `compatibility/` — compatibility matrices per integration milestone (which released versions are proven together) + the comparability rule.
- `reports/` — benchmark, capacity, autoscaling, loop (I6), and calibration reports (archived copies of the owning repos' published reports, linked by pin).
- `postmortems/` — standard format: timeline from real metrics, detection gap, root cause, mitigation, action items.
- `portfolio/` — landing page, two articles, demo script + demo video script, honest-limitations statement, architecture diagrams, ADR index (links to every ADR across the six repos).
- `study/` — curriculum/study progress tracker (artifact-or-drop rule enforced here).
- `oss/` — OSS activity log (real interactions only; drafts marked as drafts).

**State ownership:** this repo owns the pin matrix, scenario evidence, compatibility matrices, OSS log, and study tracker. Everything else is an archived copy with a link to its origin and pin. No databases, no runtime state.

**Concurrency model:** none — scripts are sequential and idempotent. Scenario scripts must be re-runnable: bring-up, smoke, evidence capture, teardown, each a separate step with recorded output.

**Failure/cancellation/retry behavior relevant here:** scenario scripts must fail loudly (non-zero exit, captured logs) and never mask a component failure; a failed scenario run is evidence of a defect in the owning repo — record it, file it upstream (in-program), pin-bump when fixed, re-run. Never "fix it locally to make the demo work."

---

## 5. Required documentation set (FIRST task: IL-T001 creates this)

```text
docs/
├── charter.md               # mission, independent value, integration value, final narrative (verbatim)
├── architecture.md          # repo layout above; sink position in dependency graph; pins-as-ledger design
├── scope.md                 # owns-list from §1; the five scenarios; portfolio artifacts
├── non-goals.md             # no runtime logic; no duplicated capability; no source checkouts; no local fixes
├── interfaces.md            # contract summaries consumed (§3), pins file format spec, evidence layout conventions
├── milestones.md            # repo milestones from §6 with acceptance criteria
├── tasks.md                 # IL-T001..IL-T012 expanded per §7, kept current with status + evidence links
├── risks.md                 # §12 risks localized; kill/reduction order; never-cut core
├── testing.md               # scenario acceptance checklists; quickstart timing protocol; reproducibility-audit procedure
├── observability.md         # what evidence must show (metric names, trace spans, dashboards) per scenario
├── security.md              # no secrets in pins/evidence; API keys in demos are throwaway; redaction rules for logs
├── experiments.md           # loop (I6) prediction-vs-measured protocol; quickstart timing runs; demo dry runs
├── integration.md           # I1–I8 roles: owner for I2/I3/I4/I6/I8, evidence archivist for all; re-run triggers
├── oss-opportunities.md     # §11 embedded: targets, progression, contingency, avoid-list, review gate
├── implementation-notes.md  # running log + Deviations section (deviation policy §14)
└── adr/                     # this repo's own ADRs (e.g. pins file format, evidence immutability) + the cross-portfolio ADR index
```

---

## 6. Repository milestones (dependency-ordered; no calendar durations)

| # | Milestone | Acceptance criteria |
|---|---|---|
| M1 | Skeleton + docs | All 15 docs exist with content; pins file format defined + validated by a script; scenario A–E definitions written; OSS log + study tracker initialized. |
| M2 | Scenario A / I2 accepted | I2 acceptance (see §9) demonstrated and reviewed; evidence archived under `evidence/i2`; pins record contracts v0.1.x + infergate/mock images + inferbench version. |
| M3 | Scenario B / I3 accepted | I3 acceptance demonstrated; benchmark report #0 archived; llama.cpp commit + GGUF revision pinned. |
| M4 | Scenario C / I4 accepted | I4 acceptance demonstrated (or CPU-fallback deviation recorded); GPU session manifest archived; vLLM/model/driver/CUDA pins recorded. |
| M5 | Scenario D / I5 evidence archived | I5 (owned by inferops) accepted; this repo archives manifests, smoke outputs, dashboard exports, rolling-update log; compatibility matrix updated. |
| M6 | Scenario E / I6 accepted | The loop closes: recommendation → applied change → re-benchmark → predicted-vs-measured comparison published **including where the prediction was wrong**. Contracts v1.0.0 pinned. |
| M7 | Failure campaign / I7 evidence | Campaign matrix (12 rows or documented reduced set) archived; ≥2 postmortems in standard format published. |
| M8 | Portfolio release / I8 accepted | Quickstart ≤15 min fresh-clone verified; landing page + 2 articles + demo script + honest limitations published; OSS evidence recorded; reproducibility audit passed. |

OSS milestones (externally paced, run parallel from any wave ≥3 equivalent): **MO1** target re-verified + built + issue reproduced (IL-T010); **MO2** reproducer communicated upstream (IL-T011); **MO3** contribution merged or under substantive review (IL-T012).

---

## 7. Task seeds (stable IDs — do not renumber; IL-T010–T012 are the OSS-track execution tasks)

**IL-T001 — Skeleton: pins, quickstart, scenarios, logs.**
- Goal/repo: bootstrap inference-lab structure + full `docs/` set. inference-lab.
- Requirement: machine-readable version-pin matrix (format + validator script); quickstart doc structure; scenario A–E definitions (purpose, components, pinned inputs, acceptance checklist each); OSS log skeleton; study-progress tracker.
- Dependencies: plan approval. Expected files: `docs/*` (15 files + `adr/`), `pins/pins.yaml` (+ validator), `scenarios/{a..e}/README.md`, `quickstart/README.md`, `oss/log.md`, `study/tracker.md`, `compatibility/README.md`.
- Complexity: M. Critical path: yes. Parallel-safe: no. Required/Stretch: Required.
- Review focus: pins format (machine-readable, provenance + date fields, digest support); no-runtime-logic scope honored.
- Verification: docs checklist complete; pins validator runs green on a seed entry.
- Evidence: committed skeleton + validator output.
- Integration impact: every repo reports evidence here; pins format unblocks all milestone recording.
- Stop condition: structure reviewed and approved.

**IL-T002 — Scenario A + milestone I2.**
- Goal/repo: orchestrate `inferbench → infergate → mock → PostgreSQL → OTel` locally via compose; record I2 evidence. inference-lab.
- Requirement: compose file pinned to released images; seeded workload run; evidence per the full I2 acceptance list (§9).
- Dependencies: IG-T003 (gateway streaming+cancellation), IB-T004 (bench client correctness), SC-T009 (contracts v0.1.0), IL-T001. Expected files: `scenarios/a/compose.yaml`, run scripts, `evidence/i2/*` (run logs, raw-event files, trace export, acceptance checklist).
- Complexity: M. Critical path: yes. Parallel-safe: no. Required.
- Review focus: evidence completeness against the I2 checklist; measurement-tolerance statement present.
- Verification: I2 acceptance checklist executed item-by-item; indicative commands: `docker compose up` in `scenarios/a`; `inferbench run --workload chat-short --seed 42 --target http://infergate...`.
- Evidence: run logs, raw events, trace export, completed checklist.
- Integration impact: I2 accepted; first pins-file "proven together" row.
- Stop condition: I2 accepted (demonstrated + reviewed).

**IL-T003 — Scenario B + milestone I3.**
- Goal/repo: orchestrate `inferbench → infergate → llama.cpp` on CPU; record I3 evidence. inference-lab.
- Requirement: scenario B compose/scripts; `chat-short` + `shared-prefix` workloads complete; first schema-valid benchmark report (report #0, methodology shakedown) archived; cancellation verified against llama.cpp; mock↔llama.cpp failover demonstrated.
- Dependencies: I2; IG-T005 (llama.cpp adapter), IB-T006 (report generator). Expected files: `scenarios/b/*`, `evidence/i3/*` (benchmark report #0, campaign logs), pins update (llama.cpp commit + GGUF model revision).
- Complexity: M. Critical path: yes. Parallel-safe: no. Required.
- Review focus: report #0 validity block; failover evidence.
- Verification: I3 acceptance checklist; indicative: scenario B compose; `inferbench report --run <id>`.
- Evidence: benchmark report #0, campaign logs, checklist.
- Integration impact: I3 accepted; first real-engine "proven together" row.
- Stop condition: I3 accepted.

**IL-T004 — Scenario C + milestone I4 (GPU).**
- Goal/repo: orchestrate `inferbench → infergate → vLLM → observability` on a rented GPU; record I4 evidence. inference-lab.
- Requirement/hypothesis: GPU path works within the pinned config; streaming + cancellation verified via engine metrics; gateway-overhead comparison (direct vs via-gateway) measured with ≥3 runs/point. GPU session requires written hypothesis + full manifest + auto-stop + budget alert (gate G6).
- Dependencies: I3; IG-T014 (vLLM adapter), IB-T011 first session, G6. Expected files: `scenarios/c/*`, `evidence/i4/*` (session log, benchmark report, cancellation-verification metrics export, full GPU session manifest), pins update (vLLM version/commit, model checkpoint + quantization, driver/CUDA, instance type).
- Complexity: M. Critical path: yes. Parallel-safe: no. Required.
- Review focus: GPU session plan pre-approved; manifest completeness; fallback honesty.
- Verification: I4 acceptance checklist; session auto-stop confirmed in log.
- Evidence: session log + reports + metrics exports, all carrying the full manifest.
- Integration impact: I4 accepted; GPU pins recorded.
- Stop condition: I4 accepted, **or** CPU-fallback deviation recorded (llama.cpp becomes the measured baseline, per §12).

**IL-T005 — Scenario D + milestone I5.**
- Goal/repo: archive evidence for the operated stack `inferops → infergate → vLLM → OTel/Prometheus/Grafana/Tempo`; verify Scenario D from the consumer side. inference-lab.
- Requirement: scenario D definition points at inferops runbooks + released manifests (no source checkouts); this repo captures and archives the I5 evidence set (I5 is owned by inferops — see §9 archiving duty).
- Dependencies: IO-T005 (in-cluster vLLM via gateway). Expected files: `scenarios/d/README.md` (+ invocation pointers), `evidence/i5/*` (manifests, smoke outputs, dashboard exports, rolling-update test log), pins update (inferops release, dashboard/config bundle versions).
- Complexity: M. Critical path: yes. Parallel-safe: no. Required.
- Review focus: deployment-from-released-images-only confirmed; evidence completeness.
- Verification: I5 acceptance evidence present and cross-checked against the inferops smoke/rolling-update outputs.
- Evidence: archived I5 evidence set + updated compatibility matrix row.
- Integration impact: I5 archived; prerequisite for I6/I7 evidence.
- Stop condition: I5 accepted (by its owner) and archived here.

**IL-T006 — Scenario E + milestone I6 (the central story).**
- Goal/repo: close and publish the capacity-feedback loop. inference-lab (loop owner; fleetlab owns the recommendation).
- Requirement: benchmark results → fleetlab produces a schema-valid capacity recommendation (Contract 7, with stated uncertainty) → inferops applies the recommended change (replica count / config) → repeated benchmark measures the outcome → predicted vs measured compared and **published, including where the prediction was wrong**. Prediction error is a result, not a failure.
- Dependencies: I5 archived; FL-T009 (recommendation emitter), IO-T009 (autoscaling experiments), SC-T010 (contracts v1.0.0). Expected files: `scenarios/e/*` (loop orchestration script + README), `evidence/i6/*` (recommendation file, applied manifests, before/after benchmark results, error analysis = the loop report), pins update (fleetlab release, contracts v1.0.0).
- Complexity: L. Critical path: yes. Parallel-safe: no. Required.
- Review focus: loop honesty — prediction vs outcome stated plainly; uncertainty carried through; no cherry-picking.
- Verification: I6 acceptance checklist; indicative: `fleetlab recommend --results ... --slo ... --cost ...`; inferops apply; `inferbench` re-run.
- Evidence: the loop report (recommendation file, applied manifests, before/after results, error analysis).
- Integration impact: I6 accepted — the sentence "I converted measurements into capacity decisions" becomes demonstrable.
- Stop condition: I6 accepted. (Never-cut: the loop may shrink to mock/llama.cpp scale but must close.)

**IL-T007 — Failure campaign evidence + milestone I7.**
- Goal/repo: turn the inferops fault campaign into archived evidence + postmortems. inference-lab (evidence; inferops executes).
- Requirement: for selected scenarios: inject (inferops), observe gateway semantics, measure client impact (inferbench); publish ≥2 postmortems in the standard format (timeline from real metrics, detection gap, root cause, mitigation, action items); archive the 12-row campaign matrix (injected / observed / verdict), with client impact measured for at least the streaming-critical scenarios (1, 2, 5, 6, 12).
- Dependencies: IO-T006/T007. Expected files: `evidence/i7/*` (campaign matrix, client-impact measurements), `postmortems/pm-001.md`, `postmortems/pm-002.md` (+ format template).
- Complexity: M. Critical path: yes. Parallel-safe: no. Required.
- Review focus: postmortems built from real metrics, not narrative; deviations (GPU-dependent scenarios run on llama.cpp/mock path) recorded.
- Verification: I7 acceptance checklist.
- Evidence: postmortems + campaign matrix + measurements.
- Integration impact: I7 evidence archived; "I injected failures and documented recovery" demonstrable.
- Stop condition: I7 accepted.

**IL-T008 — Compatibility matrix upkeep.**
- Goal/repo: keep the compatibility matrices and pins current across every release and milestone. inference-lab.
- Requirement: on every consumed release: pin bump entry (tag/digest/date/provenance); matrix row per integration milestone stating which released versions are proven together; the benchmark comparability rule printed in the matrix; re-run trigger notes (e.g. contract MAJOR ⇒ I1 re-run before any scenario is re-claimed).
- Dependencies: IL-T001; ongoing per release. Expected files: `pins/pins.yaml` (living), `compatibility/matrix.md` (+ per-milestone rows).
- Complexity: S. Critical path: no. Parallel-safe: yes. Required.
- Review focus: no unproven "compatible" claims; every row cites milestone evidence.
- Verification: pins validator green; each matrix row links to archived evidence; verified at each integration milestone.
- Evidence: matrix diffs + validator output.
- Integration impact: the single source of "what is proven together" for all repos and the I8 audit.
- Stop condition: matrix current at I8.

**IL-T009 — Portfolio release + milestone I8.**
- Goal/repo: ship the portfolio release and pass the reproducibility audit. inference-lab.
- Requirement: quickstart ≤15 min from fresh clone (GPU-free, Scenario A); demo script + recorded demo (demo video script owned here); benchmark + capacity reports linked; failure evidence linked; OSS evidence (public links) recorded; landing page + articles per §Portfolio artifacts below; honest-limitations statement; compatibility matrix current; **reproducibility audit**: a fresh session re-derives every headline claim from pinned artifacts; claims that fail are removed or re-measured — no exceptions.
- Dependencies: I2–I7 evidence archived; IL-T008 current; IL-T010–T012 state known. Expected files: `portfolio/landing.md` (or site), `portfolio/articles/{article-1,article-2}.md` (+ optional third), `portfolio/demo-script.md`, `portfolio/demo-video-script.md`, `portfolio/limitations.md`, `quickstart/*` finalized, release tag + audit checklist.
- Complexity: L. Critical path: yes. Parallel-safe: no. Required.
- Review focus: stranger-test dry run (someone with no context follows the quickstart); audit rigor; limitations honesty.
- Verification: I8 acceptance checklist incl. timed fresh-clone quickstart run and stranger-test dry run; audit checklist executed in a fresh session.
- Evidence: release tag of inference-lab + the audit checklist + timing log.
- Integration impact: I8 accepted = program Definition of Done reached.
- Stop condition: I8 accepted.

**IL-T010 — OSS: score, build, first reproduction.**
- Goal/repo: refresh OSS candidate scoring with live checks, build the primary target locally, reproduce one existing issue. inference-lab (log; work happens upstream).
- Requirement: re-verify volatile facts live before committing — especially the Gateway API Inference Extension → llm-d migration (`InferenceModel`→`InferenceObjective` rename; as of 2026-07 — re-verify): if EPP work has moved, follow it into llm-d (same score profile). Build + test the chosen primary locally (kind-based for GAIE; record versions). Reproduce an existing open issue (prefer `good-first-issue`/`help-wanted` with testable behavior).
- Dependencies: program wave ≥3 equivalent (gateway + bench core exist, so reproductions can cite real experience). Expected files: `oss/scoring-refresh.md`, `oss/log.md` entries (build log, reproduction log, environment versions).
- Complexity: M. Critical path: no. Parallel-safe: yes. Required.
- Review focus: target choice sign-off by the user before proceeding to upstream contact.
- Verification: build + reproduction logs with recorded versions.
- Evidence: OSS log entries.
- Integration impact: feeds I8 OSS evidence.
- Stop condition: reproduction acknowledged upstream, or fallback triggered per contingency (§11).

**IL-T011 — OSS: minimal reproducer + upstream communication.**
- Goal/repo: reduce the reproduction to the smallest config/cluster/test that shows it; communicate evidence upstream. inference-lab (log).
- Requirement: minimal reproducer + environment manifest posted as an issue/comment upstream. Public links recorded (created at execution time, not before). User reviews every submission before posting.
- Dependencies: IL-T010. Expected files: `oss/log.md` entries with public issue/comment links + the reproducer reference.
- Complexity: M. Critical path: no. Parallel-safe: yes. Required.
- Review focus: submission text reviewed by the user pre-post; evidence-quality (manifest, versions, exact steps).
- Verification: public link exists and matches the logged draft.
- Evidence: public issue/comment links in the OSS log.
- Integration impact: I8 OSS evidence.
- Stop condition: maintainer response, or 2-week silence → contingency path (§11).

**IL-T012 — OSS: contribution + review follow-through.**
- Goal/repo: land a small upstream contribution and follow review through. inference-lab (log).
- Requirement: small test / fix / benchmark / validation / Kubernetes example / docs PR (scope from §11 avoid-list applies); address review promptly, keep scope fixed; record lessons.
- Dependencies: IL-T011. Expected files: `oss/log.md` entries (PR links, review threads, lessons note).
- Complexity: M. Critical path: no. Parallel-safe: yes. Required.
- Review focus: user reviews the PR before posting; review responses stay in scope.
- Verification: PR link + review thread state recorded.
- Evidence: PR links + review threads + lessons note.
- Integration impact: completes the "contributed reproducible evidence or a fix upstream" narrative sentence.
- Stop condition: merged, **or** under substantive review at I8 with the contingency documented.

---

## 8. Testing, observability, security, performance hypotheses

**Testing.** This repo tests orchestration, not runtime: (a) pins validator (schema-checks every pins entry: tag, digest, date, provenance); (b) scenario acceptance checklists — each scenario has an executable checklist mirroring its milestone's criteria; (c) quickstart timing protocol — fresh clone, clean Docker cache noted, wall-clock measured, target ≤15 minutes on a GPU-free machine, ≥2 timed runs before I8; (d) reproducibility-audit procedure — for each headline claim: locate the pinned artifacts, re-derive the number in a fresh session, pass/fail recorded; (e) link integrity check over evidence/reports/ADR index.

**Observability.** This repo consumes observability rather than emitting it: scenario evidence must show the contract metric names and the gateway span sequence (`recv → queue.wait → upstream.connect → ttft → stream.relay → settle`) in archived trace exports and dashboard screenshots/exports. Any name mismatch is a defect report to infergate/inferops, never a local rename.

**Security.** No secrets, API keys, or tokens in pins, compose files, or archived evidence (demo keys are throwaway and rotated); redact bearer tokens from archived logs; upstream OSS communications contain no private data; the landing page claims are traceable, so nothing unpublishable enters evidence.

**Performance hypotheses (this repo's own):** H1 — Scenario A quickstart completes in ≤15 minutes from fresh clone on a GPU-free machine (verified by timed runs; the number is measured, never assumed). H2 — every headline portfolio claim is re-derivable from pinned artifacts by a fresh session (the I8 audit is the test). All other performance numbers in this repo are archived copies with provenance; this repo never generates new performance claims.

---

## 9. Integration milestones (this repo owns I2, I3, I4, I6 — the loop — and I8; and archives evidence for all of I1–I8)

Common rules: every milestone runs against pinned released artifacts recorded in this repo's pins file; evidence is archived here; a milestone is "accepted" only when its acceptance criteria are demonstrated and reviewed.

**I2 — Local request path (owner: inference-lab).** Prereqs: IG-T003, IB-T004, IL-T001; contracts v0.1.x. Pins: contracts, infergate image, mock image, inferbench version. **Acceptance:** `inferbench → infergate → mock backend` runs a seeded workload: 100 concurrent streams, zero frame mixing; 3-point cancellation verified (mock abort observed within bound); raw events schema-valid; client-vs-gateway TTFT agreement within declared tolerance; traces/metrics visible (Scenario A includes PostgreSQL usage write + OTel). Failure handling: frame mixing or cancellation leak → stop, fix in infergate, re-run; measurement disagreement → check measurement-point definitions before touching code. Evidence: run logs, raw-event files, trace export, acceptance checklist.

**I3 — Local inference (owner: inference-lab).** Prereqs: I2; IG-T005; IB-T006. Pins: + llama.cpp commit + GGUF model revision. **Acceptance:** `inferbench → infergate → llama.cpp` completes `chat-short` and `shared-prefix` workloads on CPU; first schema-valid benchmark report generated (manifest + validity block); cancellation verified against llama.cpp; failover mock↔llama.cpp demonstrated. Failure handling: llama.cpp behavioral surprises → capability descriptor updated, adapter fixed (in infergate); invalid report → G4 review before proceeding. Evidence: benchmark report #0, campaign logs.

**I4 — GPU inference (owner: inference-lab).** Prereqs: I3; IG-T014; G6 (hypothesis + manifest + auto-stop + budget alert); IB-T011 first session. Pins: + vLLM version/commit, model checkpoint + quantization, driver/CUDA, instance type. **Acceptance:** `inferbench → infergate → vLLM` on a rented GPU: streaming + cancellation verified via engine metrics (KV usage / running-count drop within bound); gateway-overhead comparison (direct vs via-gateway) measured with ≥3 runs/point; session auto-stopped; all artifacts carry the full manifest. Failure handling: engine metric-name drift → update capability mapping, re-verify; budget trip → stop, record, fall back. **CPU fallback:** documented deviation; llama.cpp variant becomes the measured baseline. Evidence: session log, GPU benchmark report, cancellation-verification metrics export.

**I6 — Capacity feedback, the central story (owner: inference-lab for the loop; fleetlab for the recommendation).** Prereqs: I5; FL-T009; IO-T009; contracts v1.0.0 (SC-T010); benchmark corpus from IB-T010/T011. Pins: everything above + fleetlab release. **Acceptance:** benchmark results → fleetlab produces a schema-valid capacity recommendation (with stated uncertainty) → inferops applies the recommended change (replica count / config) → repeated benchmark measures the outcome → predicted vs measured compared and published, **including where the prediction was wrong**. Failure handling: prediction badly off → that is a *result*, not a failure — publish the error analysis and refine profiles; loop mechanics broken → fix Contract 7 plumbing. Evidence: the loop report (recommendation file, applied manifests, before/after benchmark results, error analysis).

**I8 — Portfolio release (owner: inference-lab).** Prereqs: I1–I7 accepted; OSS minimum target met or contingency documented; IL-T009. **Acceptance:** fresh-clone quickstart reproduces Scenario A in ≤15 minutes on a GPU-free machine; demo script + recorded demo; benchmark report(s) and capacity report published with validity blocks; failure-campaign evidence linked; OSS evidence (public links) recorded; compatibility matrix current; reproducibility audit passed (a fresh session can re-derive every headline claim from pinned artifacts); honest-limitations section published. **Failure handling: any headline claim that cannot be reproduced is removed or re-measured — no exceptions.** Evidence: release tag of inference-lab + the audit checklist.

**Archiving duty for milestones owned elsewhere:**

| Milestone | Owner | This repo archives |
|---|---|---|
| I1 — Contract compatibility (all four consumers validate golden fixtures against the same bundle in CI; re-entrant per contract release; v1.0.0 re-run is an I6 prerequisite) | serving-contracts | the four green CI run links referencing the same bundle tag, linked in the pins file |
| I5 — Operational stack (deployment from released images only; warm-up-aware readiness; rolling update under load with zero client-visible errors; golden dashboards live; traces end-to-end) | inferops | manifests, smoke outputs, dashboard exports, rolling-update test log (IL-T005) |
| I7 — Failure campaign (all 12 fault scenarios injected — GPU-dependent ones may run on llama.cpp/mock with recorded deviation; expected semantics observed or deviation documented; client impact measured for scenarios 1, 2, 5, 6, 12; ≥2 postmortems) | inferops (execution), inference-lab (evidence) | campaign matrix, postmortems, client-impact measurements (IL-T007) |

---

## 10. Portfolio artifacts (owned here; assembled at IL-T009)

**Landing page — this exact order:**
1. Positioning statement (the target positioning from §1).
2. **"Why not LiteLLM / Envoy AI Gateway / GAIE?"** related-work section — accurate, sourced from product docs (LiteLLM entry produced via the study track), respectful, and specific about what this portfolio does differently (measured gateway/engine boundary, evidence-first).
3. Three measured claims, each linked to its report (with manifest + validity block).
4. Architecture diagram with the **explicit gateway/engine boundary** drawn (gateway: admission, routing, streaming relay, cancellation, quotas, retry budget; engine: continuous batching, per-token scheduling, KV/prefix cache, GPU placement).
5. Quickstart (the ≤15-minute Scenario A path).
6. Honest limitations (below).
7. The final narrative (§1, verbatim), each sentence hyperlinked to its evidence.

**Articles (working titles):**
1. "Double-Queuing in LLM Serving: When a Gateway Destroys Continuous Batching"
2. "Correct Cancellation, Retry and Token Accounting for Streaming Inference"
3. (optional) "How to Benchmark TTFT, ITL and Goodput Without Lying to Yourself"

**Demo:** demo script + demo video script (5-minute class); walks the narrative sentence-by-sentence over real evidence.

**Postmortem standard format (every postmortem):** timeline from real metrics, detection gap, root cause, mitigation, action items.

**Honest-limitations statement (embed and keep current; publish at I8):** single-node Kubernetes scale (one GPU node); 1–2 rented GPUs, not fleet-scale production; simulation ≠ production (fleetlab predictions carry stated uncertainty); SGLang/PD-disaggregation at study/benchmark level (if at all); no CUDA/kernel work; multi-region and multi-replica-gateway as design notes only; benchmark numbers valid only for the pinned hardware/model/engine configurations.

---

## 11. OSS track (executed via IL-T010–T012; all activity logged here)

**Minimum completion target (mandatory for I8):** one acknowledged issue reproduction; one PR merged **or under substantive review**; one public benchmark or design artifact; documented maintainer interaction.

**Targets:**
- **Primary: Gateway API Inference Extension (GAIE)** — Go; EPP routing/scheduling is exactly the infergate boundary; kind-testable without GPU. **Re-verify the llm-d migration first** (`InferenceModel`→`InferenceObjective` rename; repo layout reported as of 2026-07 — re-verify live at IL-T010): if EPP work has moved, follow it into llm-d (same score profile).
- **Secondary (parallel, cheap): OpenTelemetry GenAI semantic conventions** — spec/docs work; status "Development" as of 2026-07 ⇒ conventions still moving; the metrics-contract work will surface real gaps to feed upstream; no GPU.
- **Fallback: vLLM** — docs/metrics/tests scope only (e.g. metric-documentation drift found during gateway adapter work, or a reproducible behavior report with full manifests from GPU experiments).

**Progression (gated):** read contribution guide + architecture → build and test locally (record versions) → reproduce an existing issue → create a minimal reproducer → communicate evidence upstream (comment with reproducer + environment manifest) → submit a small contribution (test, fix, benchmark, validation, K8s example, or docs) → address review promptly, scope fixed → record public evidence + lessons in the OSS log. Gates: reproduction step requires user sign-off on target choice; **the user reviews every submission before posting**.

**Contingency:** 2 weeks silence on an issue → one polite ping + start a second candidate item in parallel (never block on one thread). 4 weeks silence on a PR → switch active effort to the fallback target, leave the PR open ("under substantive review" may be satisfied by the fallback). If both primary and fallback stall by I8 → documented graceful degradation: the acknowledged reproduction + a public benchmark/design artifact (e.g. reproducible engine-behavior report, or the "infergate router vs EPP" analysis), with the stall documented in the OSS log — a documented contingency, never a silent scope cut.

**Avoid regardless of target:** scheduler rewrites, CUDA kernels, architecture replacements, large unsolicited refactors, unverified performance claims.

**Honesty:** the OSS log records real interactions only; planned-but-not-sent communications are marked as drafts. No upstream issues or PRs existed at planning time — all public links are created at execution time.

---

## 12. Risks and kill criteria

| Risk | Trigger | Mitigation |
|---|---|---|
| This repo absorbs runtime fixes / becomes a monolith | any component patch, vendored code, or source checkout appears here | hard rule: route defects to the owning repo with evidence; pin-bump on release; reject the change in review |
| Pin/release churn eats building time (program risk R1) | pin bookkeeping dominates; lockstep changes across repos twice in a row | contract-first discipline; automate pins validation; consolidation is a user-review decision only |
| OSS latency or rejection (R6) | contingency thresholds in §11 | parallel secondary target; graceful degradation; OSS is never on the critical path |
| Fabrication/overclaiming (R12) | any claim lacking a manifest/log | evidence rules; the I8 reproducibility audit removes unreproducible claims — no exceptions |
| GPU-dependent scenarios blocked (R2) | budget alert fires; no GPU access | scenario variants fall back to llama.cpp/mock with **recorded deviations**; portfolio repositioned around CPU/edge evidence if needed |
| Demo breadth balloons | scenario/demo work blocks a milestone without new evidence | demo breadth is reducible; cut per order below |

**Reduction/kill order (when a milestone exit is threatened):** cut demo breadth and optional article #3 first; reduce chaos-evidence breadth to the streaming-critical scenarios (with documented deviation); reduce GPU scenario variants to CPU fallbacks with recorded deviations. **Never cut:** the Scenario A quickstart and the Scenario E loop — they are the never-cut core (the loop may shrink to mock/llama.cpp scale but must close). Also never cut (program-wide): cancellation correctness, some fault-injection evidence, methodologically valid benchmarking, contract validation.

**Generic drop rule:** drop or postpone any work item that blocks the critical path without producing new evidence, duplicates an existing capability, lacks a measurable artifact, exceeds GPU budget, or can't be explained and reviewed by the user.

---

## 13. Definition of Done

inference-lab is accepted when: **I2–I8 evidence is archived** (I2/I3/I4/I6/I8 accepted as owner; I1/I5/I7 archived per duty); **pins and compatibility matrices are current** (verified at I8); and the **portfolio release is shipped** — quickstart (≤15 min, GPU-free, stranger-tested), recorded demo, benchmark + capacity reports linked, failure-campaign evidence and ≥2 postmortems linked, OSS evidence (public links) recorded or contingency documented, two articles + landing page + honest-limitations statement published, and the reproducibility audit passed (every headline claim re-derivable from pinned artifacts by a fresh session; failing claims removed or re-measured — no exceptions).

---

## 14. Deviation policy

> Keep `docs/implementation-notes.md`. When repository evidence forces a deviation from the approved plan, choose the conservative reversible option, record the evidence, decision, consequences, and follow-up under `Deviations`, and continue. Pause only when the deviation changes public contracts, repository ownership, security posture, or milestone scope.

---

## Working style (Claude Fable 5)

Conduct rules for every session run from this prompt:

- **Start with a blind-spot pass.** Before executing the first task, inspect the actual repository and ecosystem state (workspace contents, pinned upstream versions, everything marked "as of 2026-07 — re-verify") and list your unknown unknowns. Where an ambiguity would change architecture, public contracts, or milestone scope, interview the user about those items first — one question at a time, highest-impact first. For everything else, record a reversible assumption in `docs/implementation-notes.md` and proceed.
- **Act when you have enough information.** Do not re-derive facts this prompt already establishes, re-litigate its decisions, or survey options you will not pursue. When weighing a choice, give one recommendation with brief rationale.
- **Build the simplest thing that meets the spec.** No features, refactors, or abstractions beyond what the current task requires; do not design for hypothetical future requirements; validate at system boundaries (user input, network, files) and trust internal code otherwise. This portfolio's value comes from measurement and correctness evidence, not surface area.
- **Pause only when genuinely required:** a destructive or irreversible action, a real scope change, or input only the user can provide (the deviation policy's pause list). Ask and end the turn. Never end a turn on a promise of undone work — if your last paragraph says "I'll now…", do that work instead.
- **Ground every progress claim.** Before reporting progress, audit each claim against a tool result from this session; report failures with their output, skipped steps as skipped, and verified work plainly.
- **Delegate and verify with subagents.** Run independent parallel-safe tasks via subagents where the harness supports them and keep working while they run. At each milestone gate, use a separate fresh-context verifier subagent to check the work against this prompt's acceptance criteria — self-review alone is not acceptance evidence.
- **Communicate for a reader who wasn't watching.** Lead with the outcome. Review bundles are a short summary, evidence links, and the specific question to decide — never raw logs, arrow-chain shorthand, or labels invented mid-session.

## 15. Session operating instructions

1. **First task is IL-T001:** create the full `docs/` set (§5) and the repo skeleton before anything else. Get the plan (docs + `tasks.md`) reviewed by the user.
2. Then implement strictly in task dependency order: IL-T002 → IL-T003 → IL-T004 → IL-T005 → IL-T006 → IL-T007 → IL-T009, with IL-T008 ongoing and IL-T010–T012 in parallel once the program's gateway + bench core exist (externally paced; never let OSS block a milestone).
3. Every scenario run: pin first, run second, archive third. No scenario is claimed without its acceptance checklist executed and evidence archived.
4. Never push to other repos; never check out or patch their source. Defects found here become evidence-backed reports to the owning repo; wait for a release, bump the pin, re-run.
5. Commit with clear messages (one logical change per commit; evidence commits reference the milestone).
6. Record everything notable — decisions, surprises, deviations, re-verification results of volatile facts — in `docs/implementation-notes.md`.
7. Mandatory user-review points: IL-T001 plan review; each milestone acceptance (I2/I3/I4/I6/I8); OSS target choice and every OSS submission before posting; GPU session plans; anything touching the deviation-policy pause list.
