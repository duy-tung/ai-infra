# Prompt — Audit Remediation Program (post-Rev-3 hiring audit)

You are a senior platform engineer executing a remediation program over the six-repository
inference-systems portfolio (`serving-contracts`, `infergate`, `inferbench`, `fleetlab`,
`inferops`, `inference-lab` under `github.com/duy-tung`). Your source of truth is the
**corrected final hiring audit** at `ai-infra:hiring-audit-final-2026-07-15.md` (Rev 3,
independently re-verified — every file:line anchor below was confirmed against the live repos
on 2026-07-15). The audit's one-line synthesis is *"methodologically strong, substrate-poor"*;
your job is to (a) make every published claim factually safe, (b) fix the verified code and
portability defects, and (c) close the highest-leverage capability gaps in the audit's
priority order **Slice 2 → 1 → 3 → 5 → 4**.

## Non-negotiable operating rules

1. **Never rewrite published history.** `release/*` branches and all existing evidence stay
   byte-identical. Corrections are new commits with honest messages. Failed gates (G5's two
   REFUTED results, scenario 4) remain visible forever; you may add context, never delete.
2. **Evidence-first done-ness.** A task is done only when its raw evidence (JSONL, transcripts,
   run URLs) is committed and, where applicable, `inference-lab/pins/pins.yaml` is updated.
   Prose claims without artifacts do not count — that rule is *why* this remediation exists.
3. **No new overclaims.** Every new README/doc sentence must be defensible from an artifact in
   the same repo. When in doubt, understate. The audit's "DO NOT USE" list (§12) is a hard
   vocabulary blacklist until the corresponding substrate exists.
4. **Single-variable discipline** for anything measured: never change workload, seed, host,
   build, and config in the same comparison. Pin everything per the existing comparability rule.
5. **CPU-first.** GPU work (Phase 3) requires explicit user budget approval first (the RQ-2
   pattern: envelope, alerts, per-session approval). Do not rent anything without it.
6. **Work repo-by-repo on feature branches; ask the user before merging.** Keep each phase
   independently mergeable. Maintain a `remediation-state.md` tracker in `ai-infra` (mirror the
   `program-state.md` conventions: task board, evidence links, honest status).

---

## Phase R0 — Claim repair (docs-only, do first, ~half a day)

These are the audit §5.3 rows judged FALSE / MISLABELED / INTERNALLY CONTRADICTED. Fix the
wording at the *current heads*; do not touch release branches. Each edit cites its anchor.

| ID | Task | Exact target |
|---|---|---|
| R0.1 | Fix the release-status lie | `inference-lab/FINAL-REPORT.md:3` claims "portfolio tagged v1.0.0 (this repo, commit b940f5c)" and line ~164 "assembled … at commit b940f5c (tag v1.0.0)". Replace with the truth: pinnable public ref is branch `release/v1.0.0` @ `bb0c253`; annotated tag exists only in local history (KI-1: git proxy drops tag pushes); this report postdates `b940f5c`. |
| R0.2 | Qualify the Kubernetes sentence | `inference-lab/portfolio/README.md:147` ("I deployed and operated the system on Kubernetes") — rewrite to the qualified form its own evidence row (line 162) and `portfolio/limitations.md` already use: manifests validated against a server-only k3s API, zero pods scheduled, operations ran on Compose. The narrative sentence must not be stronger than its evidence row. |
| R0.3 | Retire "production-grade" | Replace in `inference-lab/README.md:5`, `inference-lab/docs/charter.md:11`, `inference-lab/portfolio/README.md:14`, `inferops/docs/charter.md:9,24`, `inferbench/docs/charter.md:62` with "experimental / evidence-driven serving lab" phrasing. No production traffic, users, or on-call exists. |
| R0.4 | Fix "four green consumer CI runs" | `inference-lab/pins/pins.yaml:103` comment + `docs/integration.md:132`. They were local same-session validations (`evidence/i1/checklist.md` says so). Rename to "four local consumer validations"; link the checklist, not imaginary CI runs. |
| R0.5 | Re-attribute "zero frame mixing" | Wherever I2 claims no-mixing (portfolio README "Three measured claims", I2 checklist), state precisely: the composed checker (`scenarios/a/checks.py#cmd_integrity`) proves status/chunk-count/concurrency only; stream-identity evidence is `infergate:internal/stream/acceptance_test.go#TestConcurrentStreamsNoFrameMixing` (100 streams, id+content). |
| R0.6 | Reconcile slow-client docs with code | `infergate/docs/interfaces.md:88`, `docs/architecture.md:114-115`, `docs/non-goals.md:29` promise "stream closed, engine released"; `internal/stream/relay.go:23-26` says full scenario-4 handling is later work, and inferops scenario 4 observed an 8 s stall NOT closing a 3 s-deadline stream. Docs must say: bound exists, full handling unverified, scenario-4 investigation open (link R1.4/R2.3). |
| R0.7 | Fix warm-up-readiness wording | I5 wording in `pins.yaml`/`evidence/i5/checklist.md`: what was measured is backend health + request behavior during warm-up; gateway `/readyz` (`internal/gateway/gateway.go:886-894`) is drain-only. Say exactly that until R2.2 ships. |
| R0.8 | Fix present-tense CI language | Until Phase R1 wires real CI: `inferbench/docs/testing.md:51`, `fleetlab/docs/testing.md:27,31,61`, `inferops/docs/interfaces.md:7`, `serving-contracts/docs/integration.md` — change "CI validates / green in CI / on every push" to "make check locally (CI wiring: R1.6)". Delete the reworded caveats again when R1.6 lands. |
| R0.9 | Narrow two more headline numbers | Failover: "12/12 requests during the recorded 141.7 s outage window succeeded via fallback; one typed `upstream_error` at the kill" (not "zero client failures"). Cancellation: sub-ms deltas are greedy timestamp correlations (aborts carry no request id), not per-request causal joins. |

**R0 acceptance:** grep-clean for the DO-NOT-USE vocabulary across all six repos (excluding
`evidence/`, `reports/`, release branches, and quotations that explicitly negate the claim);
every §5.3 FALSE row has a corrected sentence citing its artifact.

## Phase R1 — Verified defects: code, tests, schema, CI, presentation (~2–4 days)

| ID | Task | Definition of done |
|---|---|---|
| R1.1 | **fleetlab ULP-brittle test** — `tests/dynamics/test_build_scenarios.py:59` (`assert backlog_ratio == ratio`) breaks under CPython 3.12's Neumaier `sum()` (gh-100425) via `fleetlab/dynamics/cold_start.py:77` | Replace with `math.isclose(..., rel_tol=1e-12)` or ULP-bounded compare; suite green on **both** 3.11 and 3.12 (tox or CI matrix proves it) |
| R1.2 | **fleetlab hard-coded sibling paths** — `tests/golden/test_real_inferbench_ingest.py:38-39` pins `/home/user/{inferbench,inference-lab}` | Env-var override (e.g. `FLEETLAB_SIBLING_ROOT`) with the old default; tier-2 corpus tests run in any checkout layout |
| R1.3 | **admission slot-leak race (code-confirmed)** — `infergate/internal/admission/admission.go`: dispatcher (≈500-505) removes ticket, increments `globalInFlight`, buffers grant; caller select (≈352-361) can take `ctx.Done()`; `cancelWaiting` (≈377-392) never drains the buffered grant | (a) Deterministic race test forcing the interleaving; (b) fix: cancel path drains `tk.done` and releases a won grant; (c) invariant `globalInFlight == live tickets` holds over ≥100k forced races under `-race`; (d) correct the "harmless unread value" comment |
| R1.4 | **scenario-4 root cause** — prove or refute the blocked-write theory | Instrument relay write start/end/deadline-error; constrain server send buffer; stream large enough to defeat kernel buffering; record RSS. Outcome is either a demonstrated deadline defect + fix, or a demonstrated kernel-buffering explanation + tightened bound — both are acceptable, silence is not. Update scenario-4 verdict + postmortem honestly |
| R1.5 | **hardware-profile schema CPU gap** — `serving-contracts/schemas/hardware-profile.schema.json` requires `gpu` | Additive MINOR (v1.1.0): make a CPU-only host expressible (optional `gpu` + required `cpu` block, or `oneOf`), with positive+negative fixtures; selftest still green; version + RELEASES entry per compatibility policy |
| R1.6 | **Wire real CI in the five repos without it** | Port `infergate/.github/workflows/ci.yml`'s pattern: serving-contracts→selftest; inferbench→go test + analysis pytest (pinned bundle); fleetlab→pytest matrix (3.11+3.12) + contracts-verify; inferops→shellcheck + compose config + kustomize build; inference-lab→pins validator + checks. Every repo: green run URL on `main` recorded in `remediation-state.md` |
| R1.7 | **Consumer bundle re-pin v0.2.0 → v1.0.0** | infergate, inferbench, fleetlab, inferops re-vendor/re-pin `serving-contracts@release/v1.0.0` (`507208b`, or v1.1.0 after R1.5); each consumer's validation green in its new CI; pins.yaml updated |
| R1.8 | **Presentation floor** | Root README (what/why/limitations/run-tests, ≤60 lines) for infergate, inferbench, fleetlab, inferops; GitHub description set on all six repos; each README's first paragraph names the substrate honestly (CPU llama.cpp / mock / single host) |
| R1.9 | **Dockerfile hermeticity note or fix** — `infergate/Dockerfile` COPYs untracked `vendor/` | Either CI job proves `go mod vendor && docker build` from clean checkout, or the Dockerfile header + README state the required pre-step explicitly |

## Phase R2 — Audit Slice 2: platform correctness on a real multi-process path (MEDIUM)

Close the three claims that are currently *factually unsafe to say in an interview*.

- **R2.1 N-backend launch path.** Extend `internal/config` schema + CLI so ≥2 backends build a
  real `route.Router` (today: `cmd/gateway/main.go:153-156` hardcodes one `BackendSpec`;
  `store.go#buildBackend` cannot construct the router). Two distinct backend processes receive
  P2C traffic through the public endpoint; unhealthy→removed within a stated bound; reload/drain
  preserves in-flight streams. Library-only tests do not count.
- **R2.2 Warm-up-aware readiness.** `/readyz` = not-draining AND ≥1 eligible warmed backend AND
  required DB state. Prove: gateway not-ready while backend warming; zero-eligible ⇒ non-200;
  flips ready without restart. Then update the inferops probe assumptions
  (`deploy/infergate/base/deployment.yaml:96-101`) and re-run `warmup-readiness-test.sh`
  asserting **gateway** `/readyz` transitions this time.
- **R2.3 Slow-client under real backpressure** (builds on R1.4): fast-client TTFT/RSS unchanged
  within stated bounds while a stalled reader trips the deadline, closes the stream, and
  releases upstream — verified by test, not narrative.

**R2 acceptance:** the audit's §9 questions 1, 2, and 3 now have strong truthful answers;
re-write the affected claim rows and CV bullets accordingly.

## Phase R3 — Audit Slice 1: one pinned real-GPU vLLM vertical slice (LARGE, user-gated)

Blocked on explicit budget approval. Execute exactly as audit §13 Slice 1: pinned GPU/driver/
CUDA/vLLM/model; randomized interleaved ≥3-rep direct-vs-gateway; three-point cancellation with
**engine-request-id joins** (fixing the correlation weakness); batch/KV pressure; one OOM/
recovery negative; profiler trace; archive bill + raw logs. An inconclusive result is reported
as inconclusive.

## Phase R4 — Audit Slice 3: real scheduling + autoscaling (kind/k3s **with agents**), then
## Phase R5 — Audit Slice 5: immutable cross-repo release (cut tags from an environment that
can push them — KI-1 is operational, not architectural: real tags/RepoDigests/SBOM/signing,
six-repo CI matrix, distinct-digest rollback), then
## Phase R6 — Audit Slice 4: capacity/cost re-fit on the R3 vLLM data (execute predicted N and
N−1; billed cost per output token; retire the "ILLUSTRATIVE ONLY" A10G placeholder).

Use the audit §13 acceptance criteria verbatim for R4–R6; do not weaken a criterion after
seeing data — if one fails, publish the failure (that discipline is the portfolio's best asset).

---

## Reporting and stop conditions

- After each phase: update `remediation-state.md` + the affected §5.3 ledger rows (FALSE →
  FIXED with commit/run links), and tell the user what changed, what's proven, what remains.
- **If interviews are imminent:** R0+R1 alone is a coherent stopping point — it makes every
  published claim safe and the test/CI story real. R2 is the next-cheapest credibility jump.
- Never present R0 wording fixes as capability gains; scores move only when substrate ships.

Begin with Phase R0. List the exact diffs you plan for R0.1–R0.9 before writing them.
