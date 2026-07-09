# 13 — Evidence, Assumptions, and Deviations

## 1. Sources inspected (evidence inventory)

| Source | Location | Size | How inspected |
|---|---|---|---|
| Workspace repository `ai-infra` | `/home/user/ai-infra` | 1 file (`README.md`, 10 bytes, content `# ai-infra`) + git history (single commit `cdaeb6f "Initial commit"`, branches `main` and the designated planning branch) | direct: `git status/log/branch`, full file listing, README read |
| Final 24-week curriculum (VI) | uploads: `9cc8f2ab-finalaiinfrastructurecurriculum24weeksvi.md` | 64,339 bytes / 786 lines | full read + structured extraction by dedicated subagent |
| Consolidated 24-week plan (VI) | uploads: `28042399-kehoachtonghopaiinfra24tuan.md` | 96,888 bytes / 707 lines | full read + structured extraction by dedicated subagent |
| Final consolidated report (VI) | uploads: `4ec9849f-baocaotonghopcuoicungaiinfra24tuan.md` | 92,122 bytes / 739 lines | full read + structured extraction by dedicated subagent |
| "A Field Guide to Fable: Finding Your Unknowns" (Thariq) | uploads: `0018cb39-…pdf` | ~13k chars extracted | full text extraction + review (supplied after the initial planning pass; drove the prompts' working-style revision) |
| "Prompting Claude Fable 5" (Anthropic platform docs, retrieved 2026-07-09) | uploads: `ec095e21-…pdf` | ~18k chars extracted | full text extraction + review (same revision) |

Workspace findings: no source code, tests, docs, ADRs, `CLAUDE.md`, CI, Docker/Compose, Kubernetes/Helm/Kustomize/Terraform/Argo CD, benchmark, observability, schema, release, or experiment artifacts exist. The repository was effectively empty; nothing was overwritten, deleted, or reorganized. The six implementation repositories do not exist and were **not** initialized (planning-only rule).

## 2. Missing sources (searched for, not found)

- ChatGPT Deep Research original report (cited inside the consolidated documents as "Report A"; only its arbitrated conclusions are available second-hand).
- Gemini Deep Research original resource report ("Report B"; explicitly noted inside the sources themselves as absent from their own document set — doubly second-hand).
- Claude Research / Claude Science originals (four documents cited as "Report C"; their verified claims are quoted inside the available syntheses with commit-level citations, but the originals were not in the workspace).
- "AI Engineering from Scratch" companion material (named by the program brief; no copy in workspace or uploads; the study track treats it as conditional — `08` §6).
- Any prior `ke-hoach`/`bao-cao` versions beyond the three uploads.

Consequence: where this plan relies on Report-C-verified facts (vLLM V1 cancellation chain, scheduler design, commit pins, GPU prices, ecosystem status), it inherits them **as reported by the syntheses, dated 2026-07**, flagged for re-verification at execution time.

## 3. Blind-spot pass

**Known knowns.** Engineer profile and strengths; the sources' verified technical core (boundary thesis, cancellation chain, benchmark methodology, SLO targets); the program brief's mandatory structure (six repos, contracts, milestones I1–I8, study/OSS tracks); empty workspace.

**Known unknowns.** Actual GPU budget the user will authorize (assumed $150–250 from sources); GPU market prices/availability at execution time; upstream maintainer responsiveness and current issue availability (scored as expectations only, `09` §1); current vLLM/GAIE/llm-d/semconv state (2026-07 facts will have drifted); whether "AI Engineering from Scratch" will be provided; user's appetite for the multi-repo maintenance overhead vs the sources' single-repo advice.

**Implicit conventions discovered.** Source documents are Vietnamese with English technical vocabulary — all planning output is English per the brief. Sources use evidence-confidence tags ([verified]/[sourced]/[inferred]) — this plan preserves that discipline via provenance flags. Sources treat acceptance criteria as numbers, not adjectives — adopted throughout. The sources' decision-log style (explicit verdicts with rationale) is mirrored in `11` §3.

**Unknown unknowns (could change architecture/scope/cost/verification).**
1. Ecosystem consolidation: gateway-layer features (prefix-aware routing, fairness) already shipped in GAIE/llm-d per sources; further consolidation could erode the portfolio's differentiation → mitigated by depth-artifact positioning; re-check at Wave 3.
2. vLLM V2 or breaking engine rearchitecture during execution → pins + capability mapping localize the damage.
3. Multi-repo coordination cost for a single engineer is unproven at this scale → consolidation triggers pre-defined (`10` §K).
4. Mock-fidelity gap (R14): correctness evidence may not transfer to real engines → llama.cpp lands early to bound it.
5. The I6 loop's prediction quality is unknowable before data exists → G8 treats prediction error as a publishable result, not a failure.

## 4. Assumptions (safe, reversible, recorded)

| # | Assumption | Basis | Reversal cost |
|---|---|---|---|
| A1 | GPU budget ~$150–250, single 24 GB-class rented GPU, scripted sessions | sources (2026-07) | low — roadmap gates GPU work behind G6; budget change rescales IB-T011/T012 only |
| A2 | vLLM v0.24.x (V1) as engine baseline; llama.cpp/SGLang by commit pin at execution | sources (verified there against code as of 2026-07) | low — capability mapping absorbs drift |
| A3 | Six-repo structure per brief despite sources' single-repo verdict | brief mandate; consolidation triggers kept | medium — triggers defined, user decides |
| A4 | Admin API of infergate is repo-private, not a shared contract | single consumer; avoids speculative contract surface | low — promote to contract if a second consumer appears |
| A5 | inferops default tooling = Kustomize + raw manifests (Helm only if proven need; no Argo CD/Terraform baseline) | "smallest justified combination" rule | low — IO-T001 ADR revisits with evidence |
| A6 | Career overlay (interview drilling, English practice, application cadence) is out of planning scope | brief's portfolio focus; sources' overlay is personal-schedule material | low — user can re-add outside repo plans |
| A7 | Eight named workloads (sources' four + brief's four additional) form the canonical suite | union of both requirement sets | low |
| A8 | The 5-minute demo video / articles from sources map into `inference-lab` portfolio artifacts | direct transfer | none |
| A9 | Source-reported SLO targets carry over as gateway acceptance targets | sources derived them for the same gateway concept | low — targets re-baselined after first measurements if infeasible |

## 5. Deviations from sources (full rationale in `11` §3)

1. **Six repositories instead of one** — brief mandate; the sources' single-repo verdict was explicitly driven by the 480-hour calendar cap this program removes. Consolidation path preserved as a user decision.
2. **No calendar plan** — waves + gates replace weeks; all source milestone *content* was preserved, re-expressed as dependencies.
3. **fleetlab exists** — sources scoped capacity work as a worksheet; the brief requires a simulator. Guardrails (G8 holdout, limitations report, provenance-mandatory profiles) prevent the simulation-fantasy failure mode the sources implicitly warned about.
4. **OSS in scope** — sources deferred contributions post-program; the brief requires a track with a minimum target. Progression is gated and off the critical path to respect the sources' focus concern.
5. **Selected-course topics in scope** — sources rejected all courses; the brief requires 6.5840/15-445-derived artifacts. The sources' artifact-or-drop rule is applied to every entry, so the deviation preserves their principle while meeting the brief.
6. **Interview/application overlay excluded** — roughly half the sources' 480 hours addressed interview prep, English, and job-search cadence; that is out of scope for repository planning and was not converted into tasks.

## 6. Planning-only compliance statement

This run: inspected sources and the workspace non-destructively; wrote Markdown planning documents and prompts under `portfolio-planning/` only; defined design-level schemas/contracts/milestones/commands (all future commands are labeled as future). It did **not**: write runtime code or dependencies; provision anything; download models; run GPU workloads; execute tests or benchmarks; create upstream issues/PRs; initialize the six implementation repositories; rewrite git history. Git usage was limited to committing and pushing these planning documents to the designated branch.

## 7. User-review decisions (the only open decisions)

1. **Confirm the six-repo strategy** knowing the sources recommended one repo for focus reasons (consolidation triggers exist either way). Default if unconfirmed: proceed with six.
2. **Confirm the GPU budget envelope** (~$150–250) or set a different number — it directly scales IB-T011/T012 and the I4–I7 GPU variants. Default: $150–250, alerts at 50%/80%.
3. **Confirm the OSS primary target** (Gateway API Inference Extension, with OTel GenAI semconv secondary and vLLM fallback). Default: as scored, re-verified live at IL-T010.
4. **Confirm exclusion of the career overlay** from repository planning. Default: excluded.
