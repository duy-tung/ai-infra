# 09 — Open-Source Contribution Track

Minimum completion target (mandatory for I8): one acknowledged issue reproduction; one PR merged **or under substantive review**; one public benchmark or design artifact; documented maintainer interaction. All activity is logged in `inference-lab` (IL-T010–T012). **No upstream issues or PRs were created in this planning run.**

---

## 1. Candidate scoring

Criteria (0–3 each, eight columns): Go/distributed-systems fit; portfolio relevance; local reproducibility without GPU (this column also covers low GPU need); maintainer responsiveness visibility; availability of small well-scoped issues; testability; learning value; hiring signal.

Honesty note on provenance: rows marked ⚠ rely on facts reported in the source documents as of 2026-07 (e.g. project language splits, GA status, repo migrations). **Maintainer responsiveness and current issue availability were NOT verified in this planning run** — they are scored as expectations and must be re-verified live at IL-T010 before committing.

| Candidate | Go/DS fit | Portfolio fit | CPU repro | Maintainer signal ⚠ | Small issues ⚠ | Testability | Learning | Hiring signal | Total (≈) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Gateway API Inference Extension (GAIE) | 3 | 3 | 3 | 2 | 2 | 3 | 3 | 2 | **21** | Go; EPP routing/scheduling is exactly the infergate boundary; kind-testable; ⚠ repo migration toward llm-d (`InferenceModel`→`InferenceObjective` rename) must be re-verified first |
| OpenTelemetry GenAI semantic conventions | 2 | 3 | 3 | 2 | 3 | 2 | 2 | 2 | **19** | Spec/docs work; status "Development" ⇒ conventions still moving; direct overlap with the metrics contract; no GPU |
| llm-d | 3 | 3 | 2 | 2 | 2 | 2 | 3 | 2 | **19** | ~96.5% Go per sources ⚠; KV/prefix-aware routing = high learning value; younger project, scope churn risk |
| vLLM | 1 (Python) | 3 | 2 | 3 | 2 | 2 | 3 | 3 | **19** | Huge visibility; docs/metrics/tests contributions feasible CPU-side; competition for issues; Python-deepening bonus |
| Envoy AI Gateway | 3 | 2 | 3 | 2 | 2 | 2 | 2 | 2 | **18** | Go control plane; v1.0 GA per sources ⚠; product overlap means contributions compete with a company roadmap |
| AIBrix | 3 | 2 | 2 | 1 | 1 | 2 | 2 | 1 | **14** | Go; less visibility into maintainer cadence from available evidence |
| SGLang | 1 | 2 | 1 | 2 | 1 | 1 | 3 | 2 | **13** | Python/Rust; GPU-heavy verification; already stretch-only in the portfolio |

## 2. Selection

- **Primary: Gateway API Inference Extension** (with the llm-d migration caveat re-verified first; if EPP work has moved, follow it into `llm-d` — same score profile).
- **Secondary (spec track, runs in parallel cheaply): OpenTelemetry GenAI semantic conventions** — the metrics-contract work (SC-T005) will surface real gaps/ambiguities; feeding one upstream is a natural, GPU-free contribution.
- **Fallback: vLLM** (docs/metrics/tests scope only — e.g. metric documentation drift found during IG-T014, or a reproducible behavior report from IB-T011 with full manifests).
- Avoid regardless of target: scheduler rewrites, CUDA kernels, architecture replacements, unsolicited large refactors, unverified performance claims.

## 3. Progression (gated; maps to IL-T010–T012)

1. Read contribution guide + architecture docs of the primary target.
2. Build and test locally (kind-based for GAIE; record versions).
3. Reproduce an existing open issue (prefer `good-first-issue`/`help-wanted` with a testable behavior).
4. Create a minimal reproducer (smallest config/cluster/test that shows it).
5. Communicate evidence upstream (issue comment with reproducer + environment manifest).
6. Submit a small contribution: test, fix, benchmark, validation, Kubernetes example, or documentation improvement.
7. Address review promptly; keep scope fixed.
8. Record public evidence + lessons in the OSS log.

Gates: step 3 requires IL-T010 sign-off on target choice; step 6 requires user review of the submission before posting.

## 4. Contingency for slow/unresponsive review

- 2 weeks silence on an issue comment → polite ping once; continue with a second candidate item in parallel (never block on one thread).
- 4 weeks silence on a PR → switch active effort to the fallback target while leaving the PR open; the "under substantive review" completion criterion may be satisfied by the fallback.
- If both primary and fallback stall by I8: the completion target degrades gracefully to the acknowledged reproduction + the public benchmark/design artifact (e.g. a reproducible engine-behavior report from IB-T011, or the "infergate router vs EPP" analysis published), with the stall documented in the OSS log. This is the documented contingency path, not a silent scope cut.

## 5. Portfolio linkage

The OSS story slots into the final narrative as: "I contributed reproducible evidence or a fix upstream." The strongest candidates for that sentence, in order: a merged GAIE/llm-d test or fix; an accepted GenAI-semconv clarification grounded in the metrics contract; a vLLM docs/metrics correction grounded in measured IG-T014/IB-T011 evidence.
