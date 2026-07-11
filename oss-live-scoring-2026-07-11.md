# OSS Live Scoring Refresh — 2026-07-11 (IL-T010 preparation)

Read-only research. **No upstream interaction of any kind was performed** — no issues, comments,
PRs, or reactions. All facts checked live on 2026-07-11 with source URLs. Per the log's honesty
rules: everything below is verification, not activity; nothing here creates a log "entry" other
than this scoring refresh itself.

Method note: GitHub API access from this session is proxy-scoped to the user's own repos, so
facts were gathered from public github.com pages (via web fetch) rather than the REST API.
Dates shown on GitHub pages were cross-checked against each other where possible; two dates
originally rendered as relative ("last month") were resolved by the surrounding context and are
marked (~) where residual uncertainty exists.

---

## 1. GAIE — kubernetes-sigs/gateway-api-inference-extension

### Activity (verified 2026-07-11)
- Repo is **active but post-migration**: latest commit on `main` 2026-07-07 (dependabot);
  latest substantive human commits 2026-06-29/30 (Gateway API v1.6 bump, docs cleanup).
  https://github.com/kubernetes-sigs/gateway-api-inference-extension/commits/main
- Latest release **v1.5.0, ~2026-04-19** (release cadence roughly monthly through spring:
  v1.4.0 ~March, v1.5.0 April; nothing newer as of today).
  https://github.com/kubernetes-sigs/gateway-api-inference-extension/releases
- 709 stars, Go 88.6%. Project describes itself as GA.
  https://github.com/kubernetes-sigs/gateway-api-inference-extension

### The llm-d question — ANSWERED: the migration has happened
- The GAIE README (2026-07-11) states the **Endpoint Picker (EPP), InferenceObjective, and
  Body-Based Router have migrated to llm-d ecosystem repositories**, and community meetings
  moved to "llm-d Router".
  https://github.com/kubernetes-sigs/gateway-api-inference-extension
- The new home is **llm-d/llm-d-router** ("formerly known as the Inference Scheduler"), which
  absorbed the EPP core and the `InferenceObjective` / `InferenceModelRewrite` APIs.
  Go 96.7%, 249 stars, latest release **v0.9.0 (2026-06-23)**, 30 releases, Apache-2.0.
  https://github.com/llm-d/llm-d-router
- kubernetes-sigs GAIE retains: the InferencePool API surface, conformance suite, and site/docs.
  Its open-issue pool is now small (12 open issues listed on 2026-07-11) and partly
  migration-cleanup themed ("[Migration] Site cleanup" #2907).
  https://github.com/kubernetes-sigs/gateway-api-inference-extension/issues
- llm-d org itself is highly active (llm-d v0.8.1 released 2026-06-26; a dozen repos pushed
  2026-07-07..11): https://github.com/orgs/llm-d/repositories

### Small-issue availability
- kubernetes-sigs GAIE: **zero** open `good first issue` items (verified via label filter,
  2026-07-11):
  https://github.com/kubernetes-sigs/gateway-api-inference-extension/issues?q=is%3Aissue%20is%3Aopen%20label%3A%22good%20first%20issue%22
  Remaining candidates are docs-shaped (#2876 GKE conformance docs, #2931 prune non-conformant
  implementations — both needs-triage/triage-accepted). The attractive conformance issue #2933
  (migrate echo backend to llm-d-inference-sim) is **assigned to a maintainer (danehans)** — not
  available. https://github.com/kubernetes-sigs/gateway-api-inference-extension/issues/2933
- llm-d/llm-d-router: **7 open `good first issue`**, **12 open `help wanted`** (2026-07-11) —
  see candidate list in §2.
  https://github.com/llm-d/llm-d-router/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22

### Review-latency signal (llm-d-router, sampled external PRs, 2026-07-11)
- PR #1902 (docs fix, external contributor anxkhn): opened 2026-07-06, **first maintainer
  response ~1 hour** (elevran, same day), merged 2026-07-09 by ahg-g.
  https://github.com/llm-d/llm-d-router/pull/1902
- PR #1835 (DumpState feature, external contributor thc1006): opened 2026-06-27, **first
  maintainer review next day** (shmuelk 06-28), two substantive review cycles, merged 2026-07-10.
  https://github.com/llm-d/llm-d-router/pull/1835
- Merge throughput: ~20 PRs merged 2026-07-09..11 alone, majority from human external
  contributors. https://github.com/llm-d/llm-d-router/pulls?q=is%3Apr+is%3Aclosed
- Read: median time-to-first-maintainer-response on external PRs is **hours to ~1 day** —
  better than the planning-time expectation (scored 2, now evidence for 3).

### Contribution process
- kubernetes-sigs GAIE: **Kubernetes/CNCF CLA required** before PRs are accepted; standard
  k8s contributor guide + OWNERS.
  https://github.com/kubernetes-sigs/gateway-api-inference-extension/blob/main/CONTRIBUTING.md
- llm-d org: **DCO, not CLA** (`git commit -s`); k8s-convention OWNERS files; lazy consensus;
  **new features / new test methodologies / API changes must be discussed first** (issue or SIG
  channel before code); rebase-and-squash. llm-d-router: #sig-router Slack, bi-weekly meetings
  Wed 10AM PDT. https://github.com/llm-d/llm-d/blob/main/CONTRIBUTING.md and
  https://github.com/llm-d/llm-d-router

## 2. Candidate newcomer issues (all llm-d-router unless noted; verified open 2026-07-11)

1. **#1798 — [Operations] Implement DumpState for program-aware-fairness plugin**
   good-first-issue + help-wanted, milestone v0.10, **unassigned, no linked PR** as of today.
   Implement `plugin.StateDumper` with bounded/sanitized output + tests. Template exists: merged
   sibling PRs #1833/#1835 show exactly the expected shape and review bar. Pure Go + unit tests,
   no GPU. **Tractability: high.** Caveat: contributor thc1006 is actively sweeping this family
   (#1838/#1840/#1850) — claim by commenting before starting.
   https://github.com/llm-d/llm-d-router/issues/1798
2. **#1803 — [Operations] Add pluginName to the default DumpState**
   good-first-issue + help-wanted, v0.10. Smallest of the family; listed open in the label query,
   but per-issue assignment not individually verified — check live before claiming.
   https://github.com/llm-d/llm-d-router/issues/1803
3. **#1625 — [Observability] epp/metrics: unbounded label cardinality from user-controlled
   inputs (metrics cardinality DoS)** — help-wanted, kind/bug, needs-triage, **unassigned**.
   `model_name`/`fairness_id`/pod labels flow unvalidated into Prometheus metrics → unbounded
   time series. **Best portfolio alignment of all candidates** (directly the metrics-contract /
   SC-T005 territory; a reproducer is CPU-only). Tractability: medium — the fix needs a design
   choice (bounding/allowlisting), so per the llm-d contributing guide it should start with an
   issue discussion, which is itself the "documented maintainer interaction" target.
   https://github.com/llm-d/llm-d-router/issues/1625
4. **#1693 / #1694 — Add span for filter / Add span for picker** — help-wanted, observability,
   v0.10, small tracing additions in the EPP scheduling path. Aligns with the OTel secondary
   track; testable with in-memory span exporters. **Tractability: high.**
   https://github.com/llm-d/llm-d-router/issues/1693 and
   https://github.com/llm-d/llm-d-router/issues/1694
5. **GAIE #2876 — [DOCS] Add documentation for running conformance tests on GKE** — needs-triage,
   docs-shaped, keeps a foot in the kubernetes-sigs repo (CLA needed). Tractability: medium
   (requires access to a conformant environment; kind may partially substitute).
   https://github.com/kubernetes-sigs/gateway-api-inference-extension/issues/2876

Noted but NOT candidates: #1630 (trace/log correlation — **assigned** to umakantv);
#1789 (DumpState mm-embeddings — open PR #1838 already fixes it);
GAIE #2933 (conformance echo→inference-sim — assigned to maintainer).

## 3. OTel GenAI semantic conventions

- **Structural change since the 2026-07 planning sources:** at **v1.42.0 (2026-06-12)** all
  `gen_ai.*` attributes, metrics, events, and spans were **deprecated in
  open-telemetry/semantic-conventions and moved to a dedicated repo,
  open-telemetry/semantic-conventions-genai**.
  https://github.com/open-telemetry/semantic-conventions/releases and
  https://opentelemetry.io/docs/specs/semconv/gen-ai/
- Core repo latest release: **v1.43.0 (2026-07-03)** — no gen-ai content anymore.
- New repo status (2026-07-11): **Development**, **no releases published yet** (schema URL
  "TODO"), 152 stars, **123 open issues**, 35 open PRs, active commits; covers gen-ai, MCP, and
  provider-specific (openai/anthropic/aws-bedrock/azure-ai-inference) conventions; versions
  against core semconv via Weaver.
  https://github.com/open-telemetry/semantic-conventions-genai
- **Impact on the v1.34.0 pin:** yes, attribute names moved after the pin — most notably
  **`gen_ai.system` was renamed to `gen_ai.provider.name` in v1.37.0**, which also deprecated
  the chat-message events in favor of attributes; v1.38–v1.41 added streaming/cache-token/agent
  attributes. Any metrics-contract attribute list pinned at v1.34.0 must be re-audited against
  the new repo before feeding gaps upstream.
  https://github.com/open-telemetry/semantic-conventions/releases (v1.37.0 notes)
- Opportunity read: a brand-new Development-status repo with 123 open issues and no release yet
  is the **best possible window** for spec-ambiguity contributions — but the target repo for
  IL-T011+ changes from `semantic-conventions` to `semantic-conventions-genai`.

## 4. vLLM (light check)

- Latest release **v0.24.0 (2026-06-29)** — the v0.24.x line is current (planning assumption
  holds). https://github.com/vllm-project/vllm/releases
- Scale signal (2026-07-11): 85.9k stars, **~2k open issues, ~3.7k open PRs** — enormous review
  competition; first-response latency for unsolicited PRs is structurally poor. Fallback-only
  role (docs/metrics/tests) remains the right call. https://github.com/vllm-project/vllm

## 5. Updated scoring (09-open-source-track.md rubric, 0–3 × 8 columns)

⚠→✓: maintainer-signal and small-issue columns are now live-verified (2026-07-11), no longer
expectations.

| Candidate | Go/DS | Portfolio | CPU repro | Maintainer ✓ | Small issues ✓ | Testability | Learning | Hiring | Total | Δ vs plan |
|---|---|---|---|---|---|---|---|---|---|---|
| **llm-d/llm-d-router** (EPP's new home) | 3 | 3 | 3 | **3** (1h–1d first response, sampled) | **3** (7 GFI + 12 HW) | 3 | 3 | 2 | **23** | was "llm-d ≈19"; router repo is Go 96.7% and directly the EPP |
| GAIE (kubernetes-sigs, post-migration remainder) | 3 | 2 (EPP gone; API/conformance remain) | 3 | 2 | **1** (0 GFI, ~12 open issues) | 3 | 2 | 2 | **18** | was 21; drops on portfolio fit + issue pool |
| OTel GenAI semconv (**new repo: semantic-conventions-genai**) | 2 | 3 | 3 | 2 (new repo, latency unverified) | **3** (123 open issues, pre-1.0) | 2 | 2 | 2 | **19** | unchanged total; target repo changed |
| vLLM | 1 | 3 | 2 | 3 | 2 | 2 | 3 | 3 | **19** | unchanged |

## 6. Verdict

The GAIE-primary recommendation survives **in spirit but changes address**: the pre-agreed
contingency in 09-open-source-track.md ("if EPP work has moved, follow it into llm-d") has
triggered — as of 2026-07-11 the GAIE README confirms the EPP, InferenceObjective, and BBR have
migrated to the llm-d org, concretely to **llm-d/llm-d-router** (formerly llm-d-inference-scheduler),
which is now the highest-scoring target (~23): Go 96.7%, exactly the infergate routing/scheduling
boundary, CPU-testable (llm-d-inference-sim exists precisely to avoid GPUs), 7 open good-first-issues
plus an observability help-wanted cluster that overlaps the metrics-contract work, verified
fast maintainer response (hours–1 day on sampled external PRs), and a DCO instead of a CLA.
kubernetes-sigs GAIE remains active and is worth keeping as a secondary surface for
conformance/docs items, but its newcomer issue pool is effectively empty today. The OTel
secondary track holds but must be **re-pointed at open-telemetry/semantic-conventions-genai**
(gen_ai.* moved out of the core repo at v1.42.0, 2026-06-12; the v1.34.0 attribute pin is stale —
`gen_ai.system`→`gen_ai.provider.name` in v1.37.0), which being pre-release with 123 open issues
is arguably an even better spec-ambiguity window than planned. vLLM fallback unchanged
(v0.24.0 current, 2026-06-29). Recommended IL-T010 decision: primary = llm-d/llm-d-router
(first move: comment-claim #1798 or open the discussion on #1625), secondary =
semantic-conventions-genai, fallback = vLLM; update oss/log.md targets table accordingly —
after user sign-off.

---
*All interaction with upstream projects (claiming issues, commenting, PRs) requires user
approval per the log rules; nothing was posted in this run.*
