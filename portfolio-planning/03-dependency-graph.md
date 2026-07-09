# 03 — Dependency Graph

## 1. The graph

```text
                serving-contracts
                       ▲
        ┌──────────────┼──────────────┬──────────────┐
        │              │              │              │
    infergate      inferbench      fleetlab       inferops
        │              │              ▲              ▲
        │              └── result ────┘              │
        │                  files                     │
        └──────────── released images ───────────────┘

released components + evidence from all five ──▶ inference-lab
fleetlab recommendations (files) ──────────────▶ inferops (as experiment input)
```

Edge list (direction = "depends on / consumes"):

| # | Consumer | Provider | Mechanism (never a source import) |
|---|---|---|---|
| 1 | infergate | serving-contracts | pinned released spec bundle; CI validates fixtures |
| 2 | inferbench | serving-contracts | pinned released spec bundle; emits schema-conformant files |
| 3 | fleetlab | serving-contracts | pinned released spec bundle; validates input files |
| 4 | inferops | serving-contracts | deployment contract + fault-scenario schema |
| 5 | inference-lab | serving-contracts | compatibility matrix + pins |
| 6 | fleetlab | inferbench | benchmark-result + raw-event **files** |
| 7 | inferops | infergate | released container **images** (by digest) + deployment contract |
| 8 | inferops | fleetlab | deployment recommendation **files** (for milestone I6 experiments) |
| 9 | inference-lab | all five | released artifacts, result files, reports |
| 10 | inferbench | infergate / engines | **network** (OpenAI-compatible HTTP/SSE) at run time only |

## 2. Acyclicity argument

Topological order exists: `serving-contracts → {infergate, inferbench, fleetlab, inferops} → inference-lab`, with the intra-tier edges (6, 7, 8) all pointing "later or sideways" in the order `infergate → inferbench → fleetlab → inferops`. Concretely:

- `serving-contracts` depends on nothing.
- `infergate` depends only on contracts (edge 1). The mock backend lives inside it, so no inward runtime edge exists.
- `inferbench` depends on contracts; its edge to `infergate`/engines is a runtime network target, not a build dependency — it builds and tests against recorded fixtures and the released mock image.
- `fleetlab` depends on contracts + inferbench *output files*.
- `inferops` depends on contracts + infergate *images* + fleetlab *recommendation files*.
- `inference-lab` is a pure sink.

No edge points from a later tier back to an earlier one. Feedback in Scenario E (recommendation → deployment → re-benchmark) is a **runtime loop over artifacts**, not a build-time dependency cycle: each iteration consumes already-released artifacts.

## 3. Forbidden edges (checked at every review gate)

- `infergate` → any other runtime/integration repo (it must build, test, and demo alone).
- `inferbench` → engine or gateway **source** (network targets only).
- `fleetlab` → `inferbench` **code** (files only; no shared statistics library — the metric definitions both rely on live in contracts).
- `inferops` → any component **source checkout** (released images only).
- `inference-lab` → anything as a library (orchestration of released artifacts only).
- Any repo → another repo via a shared internal application library.
- `serving-contracts` → anything (it must remain dependency-free; validation tooling may use standard schema validators only).

## 4. Version pinning rules

| Artifact | Pinned by | Where recorded |
|---|---|---|
| Contract bundle | SemVer tag (e.g. `v0.3.0`) | each consumer's CI config + `inference-lab` pins file |
| infergate image | digest + SemVer tag | inferops manifests + pins file |
| mock-backend image | digest + tag | inferbench CI + inferops + pins file |
| Engine versions | vLLM minor version (v0.24.x baseline) + exact commit; llama.cpp commit; SGLang commit (if used) | benchmark-run manifests + inferops manifests + pins file |
| Model + tokenizer | checkpoint revision + quantization + tokenizer hash | benchmark-run manifests + pins file |
| Driver/CUDA | recorded per benchmark run and per GPU-node profile | benchmark-run manifests + inferops node profile |
| Dashboards/collector configs | inferops release tag | pins file |

Benchmark comparability rule: results are comparable only when model revision, quantization, tokenizer, engine version+flags, hardware, driver/CUDA, workload version+seed, and warm-up policy all match, or the difference is the single declared experimental variable. `inference-lab`'s compatibility matrix states which released versions have been proven together (per integration milestone).

## 5. Change propagation

- **Contract change (minor/additive):** consumers upgrade at their own pace; compatibility tests must stay green on both old and new fixtures during the deprecation window.
- **Contract change (major/breaking):** requires a migration note in `serving-contracts`, a version bump in every consumer, and a re-run of milestone I1 (contract compatibility) before any cross-repo scenario is re-claimed.
- **infergate image release:** inferops bumps digest; I5-level smoke evidence re-run before the pins file advances.
- **inferbench schema-affecting change:** blocked unless contracts released it first (schemas live in contracts, not in inferbench).
