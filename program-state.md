# Program State — inference-systems portfolio

Orchestrator state file. Rewritten every iteration; recoverable from this file + git alone.
Last updated: iteration 14b (FL-T001 + IO-T001 done; 3 agents running: IB-T008/9, IL-T002 P1, IG-T009/10), 2026-07-09.

## Environment (blind-spot pass, iteration 0 — re-verify on container restart)

- Container: 4 vCPU, 15 GiB RAM, ~30 GiB free disk, linux/amd64, **no GPU** (GPU work is rented, Wave 4+, behind G6).
- Toolchain (measured 2026-07-09): go 1.24.7 · Python 3.11.15 / pip 24.0 · node v22.22.2 · GNU Make 4.3 · jq 1.7 · git 2.43.0 · docker 29.3.1 + compose v5.1.1.
- **Docker daemon is not auto-started.** `sudo dockerd &` works; must be restarted after any container restart.
- kind / kubectl / kustomize / k3s: **not installed** — install at Wave 4 (IO-T002); network permitting.
- Network: outbound HTTPS via agent proxy. Verified working: Go module proxy (go get succeeded). PyPI assumed working (not yet exercised). GitHub API via MCP tools only (no `gh` CLI).
- Remote repos: session GitHub scope is `duy-tung/ai-infra` only. Creating six GitHub repos = external-resource hard block → review-queued (RQ-1). Components are **local-only git repos** until decided.
- Network policy (measured iters 3–8): package registries bypass the proxy (PyPI, proxy.golang.org, npm, crates work); Ubuntu main apt archive WORKS (PPAs blocked). **DENIED: huggingface.co, github.com downloads, and Docker Hub blob CDN (production.cloudfront.docker.com → 403)** — no container images can be pulled at all. Consequences: no GGUF download; no GitHub release binaries; no postgres/otel/grafana/prometheus images; kind/k3s cluster images unavailable → **Wave 4/5 Kubernetes milestones (I5, in-cluster I7) are NOT executable in this environment as planned** without a network-policy change. Working fallbacks proven: native llama-server built from PyPI sdist; PostgreSQL 16 via apt (running at 127.0.0.1:5432, dev/test DBs created); OTel collector / Prometheus are Go programs installable via the Go module proxy (unverified yet); Grafana/Tempo TBD. → RQ-4 (expanded).
- Remaining unknown unknowns: kind/kubectl acquisition path under this policy (Wave 4); GPU rental provider access (Wave 4, G6); container ephemerality until RQ-1 decided.

## Workspace layout

Planning repo: `/home/user/ai-infra` (branch `claude/inference-systems-orchestration-77l8wk`).
Components (side-by-side local git repos, branch `main`): `/home/user/serving-contracts`, `/home/user/infergate`, `/home/user/inferbench`, `/home/user/fleetlab`, `/home/user/inferops`, `/home/user/inference-lab`.

## Wave & gate status

- **Current wave: 2** (streaming ✓, first engine, bench core). Wave 1 exit criteria met: v0.1.0 released ✓, gateway serves non-streaming from mock ✓, fixture validation green in the consumer that exists (infergate CI) — I1-partial by design (4-consumer I1 completes as consumers gain CI).
- **G2 PASSED** (2026-07-09, fresh-context verifier, zero defects). G1: v0.1.0 fixture layer green; full I1 pending consumer wiring. Others: not reached. Milestones I1–I8: none accepted yet.

## Task board (Wave 1 scope; full register in portfolio-planning/05 §8)

| Task | Status | Evidence / commit |
|---|---|---|
| SC-T001 policy+docs bootstrap | done (verifier PASS) | serving-contracts `8a4de1f` |
| SC-T002 inference API contract | done (verifier PASS: exact field subset, 10 error classes, 36 fixtures) | serving-contracts `116d903` |
| SC-T003 benchmark data schemas | done (verifier PASS: pooled-percentile/shed-adjacent/validity-block enforced structurally) | serving-contracts `d604a72` |
| SC-T004 backend-capability schema | done (verifier PASS) | serving-contracts `f2d1b2d` |
| SC-T005 metrics vocabulary | done (verifier PASS: 11/11 metrics match Contract 2; semconv v1.36.0 pinned) | serving-contracts `15edc81` |
| SC-T008 consumer compatibility kit | done (verifier PASS: 65 checks green, negative tests exit 1) | serving-contracts `8173098` |
| SC-T009 release v0.1.0 | done — tag `v0.1.0` created after RELEASE-READY audit; release notes in docs/releases/v0.1.0.md; review queued (RQ-3); deviation D1 recorded in SC implementation-notes | serving-contracts `6619185` + tag |
| SC-T006 deployment+fault contracts | done (orchestrator re-ran validator: 103 checks green; 12 fault scenarios FS-01..12; grace>max-stream structural) | serving-contracts `f219e05` |
| SC-T007 fleet schemas | done (provenance-mandatory quantities; Scenario E worked example chain) | serving-contracts `f8a21a7`; released as tag `v0.2.0` |
| IL-T001 inference-lab skeleton | done (verified iter 0: pins validator green, 15-doc set present, clean tree) | inference-lab `4fb1036` |
| IG-T001 infergate docs bootstrap | done (verified iter 0: 15 docs + 7 ADRs, clean tree) | infergate `60458ac` |
| IG-T002 gateway skeleton + mock | done (orchestrator re-ran: vet clean, race tests ok, CONFORMANCE PASS; auth/permission/rate_limited deferred to IG-T007/T009 by design) | infergate `3d089cb`,`27969ae`,`1cd4431` |
| IG-T004 config snapshots + drain | done (reload under traffic 5421 req / 0 fail; publish 2.1ms vs 5s budget; e2e drain test green) | infergate `9f83e0a` |
| IG-T003 SSE relay + cancellation | done — **GATE G2 PASSED** (fresh verifier: all checks PASS, zero defects; noted minor test-design caveats in verifier report) | infergate `0d5256b..c27e93d` |
| IG-T006 observability per contract | done (orchestrator re-ran: telemetry tests race-green, CONFORMANCE PASS; 7 metrics live exact-per-contract, queue/retry metrics honestly deferred to IG-T010/T013; spans recv→connect→ttft→relay→settle evidenced) | infergate `8d3afd8`,`c906780` |
| IG-T005 llama.cpp adapter | done (orchestrator re-ran full harness: LLAMACPP VERIFY PASS, 31 engine cancel confirmations; descriptor validates; 3-pt cancel: mid-stream p95 9.7ms, pre-first-token p95 62ms incl. prefill nuance, queued bounded by slot availability ~3s; failover both directions; deviation D2 = tiny model, RQ-4) | infergate `b3df27d..3674768` |
| IB-T002 open-loop generator | done (schema-valid events; deterministic replay proven by digest; CO-safety test; race+vet green) | inferbench `6708154` |
| IB-T003 workload suite v1 | done (8 workloads validate; dry-runs green vs gateway+mock) | inferbench `19d8ba2` |
| IB-T004 streaming client correctness | done (calibration: client TTFT/ITL within ~1–2ms of configured; 17/17 cancels observed at mock) | inferbench `3b12013` |
| IG-T007 tenancy+auth+registry | done (orchestrator re-ran store/auth tests + conformance; revocation 506ms poller / 5.5ms reload vs 5s bound; 0 hot-path DB queries) | infergate `f2f168a`,`1e2c138` |
| IG-T008 usage accounting | done (orchestrator re-ran usage tests + conformance; settle variance 0.0000% engine-grounded; DB-outage max enqueue 79.7µs, exactly-once drain; invariants doc w/ 10 invariants→tests) | infergate `fcd49b1`,`2d45fb9`,`562a641` |
| IG-T009 RPM/TPM quotas | in-progress (agent dispatched iter 13) | — |
| IG-T010 admission control | in-progress (same agent; G5 mechanism) | — |
| IL-T002 Scenario A / I2 | in-progress (Phase-1 prep agent dispatched iter 13; Phase 2 after images rebuilt at IG-T008 HEAD) | — |
| IO-T001 inferops docs bootstrap | done (verified iter 14: 15 docs + tooling ADR Kustomize+raw; RQ-4 dual-path A/B with semantics-preservation map) | inferops `2231096` |
| FL-T001 fleetlab docs bootstrap | done (verified iter 14: 15 docs + ADR-0001 hybrid simulator; R9 guardrails structural; pins v0.2.0) | fleetlab `19222e8` |
| IB-T005 analysis core | done (orchestrator re-ran: 74 pytest + race green; pooled≠averaged proof; known-answer stats) | inferbench `d2ce815` |
| IB-T006 report generator | done (orchestrator re-ran contracts-verify: result/manifests/events all ok; G4-candidate report at inferbench/reports/ib-t006-sample/report.md — review-queued in RQ-3) | inferbench `5a3da84` |
| IB-T008 sweeps/replay/comparison | in-progress (agent dispatched iter 12) | — |
| IB-T009 experiment governance | in-progress (same agent) | — |
| IB-T001 inferbench docs bootstrap | done (verified iter 2: 15 docs + 5 ADRs, pin v0.1.0 recorded, clean tree) | inferbench `b5cf196` |
| All other tasks | todo | — |

## Pins

- contracts bundle: **v0.2.0** latest; inferbench pins **v0.2.0** (needs cost/slo schemas; verified additive vs v0.1.0); infergate + inference-lab pin **v0.1.0**. I1 not yet run in full.
- engine pins (from plan, re-verify at use): vLLM v0.24.x; llama.cpp by commit at IG-T005; OTel GenAI semconv pinned at SC-T005.

## Review queue

| ID | Question | Blocks | Status |
|---|---|---|---|
| RQ-1 | Remote hosting: create six GitHub repos (`serving-contracts`, `infergate`, `inferbench`, `fleetlab`, `inferops`, `inference-lab`) under your account? Needed for durability (this container is ephemeral) and for OSS-visible portfolio. | Nothing immediately; durability risk grows each wave | open (surfaced iter 0) |
| RQ-3 | Wave-1 exit review batch (non-blocking, queue-and-continue): infergate boundary doc (`infergate/docs/architecture.md` §1 + ADR-0001), inference-lab skeleton structure, and (when released) contracts v0.1.0 release notes. | Nothing — deviation policy allows continuing; feedback folded in when received | open (accumulating until Wave 1 exit) |
| RQ-4 | Network policy blocks huggingface.co, github.com downloads, AND all container-image pulls (Docker Hub CDN 403). Wave 2/3 proceed fine with proven fallbacks (native llama-server from PyPI sdist; apt PostgreSQL; local tiny GGUF). **But Wave 4/5 Kubernetes work (kind/k3s clusters, I5) cannot run without images.** Request: allow huggingface.co (I3/I4 model realism), github.com release assets, and container registries (registry-1.docker.io + production.cloudfront.docker.com, registry.k8s.io, quay.io, ghcr.io) in the environment network settings — or tell me to plan I5/I7 around process-based (non-K8s) fallbacks with a recorded scope deviation. | I3/I4 realism; **I5 (Wave 4/5) entirely** | open (surfaced iter 3, expanded iter 8) |
| RQ-2 | Confirm four planning defaults (13 §7): six-repo strategy (default: yes), GPU budget envelope (default $150–250, alerts 50%/80%), OSS primary target (default: Gateway API Inference Extension), career overlay excluded (default: yes). | GPU spend (Wave 4) blocks on budget; rest proceed on defaults | open — defaults applied provisionally (surfaced iter 0) |

## Toolchain (local, outside component repos)

- /home/user/toolchain/ DONE (iter 5, orchestrator spot-checked: server starts, /health ok, deterministic completion):
  - bin/llama-server — native, CPU, llama.cpp commit `78d2f524682d9fee790a6460c93d018dafeb5229` via llama-cpp-python 0.3.33 sdist (PyPI, sha256 369ba03d…acd92); UI disabled (needs blocked downloads).
  - models/tiny-llama-local.gguf — 38 MiB, ~19.7M params F16, random weights seed 42 + vendored SPM vocab, byte-reproducible, provenance in models/PROVENANCE.md. RQ-4 fallback model; swap for real 1–3B GGUF if network policy opens.
  - Cancellation observability: no dedicated cancel counter; slot release + `llamacpp:requests_processing` gauge → capability descriptor for IG-T005. Metrics prefix `llamacpp:` (no labels).
  - Scripts: build.sh, make-model.sh, run-llama-server.sh, smoke-test.sh (all reproducible).
  - bin/otelcol-file — minimal OTel collector (otlp receiver → file/debug exporters), built iter 12 via ocb v0.114.0 from Go proxy; bin/builder. Prometheus via go install FAILED (module-path quirk) — revisit at Wave 4 (IO-T003) with a different acquisition route.
  - docker build FROM scratch works (no registry needed) — static-Go images for gateway/mock are buildable locally.

## Budget ledger (GPU)

Envelope: $150–250 (default, unconfirmed — RQ-2). Spent: $0. Sessions used: 0 of ≤6 target.

## Lessons

- L1: Docker daemon must be started manually (`sudo dockerd &`) after container restart — check before any compose/scenario work.
- L2: Component repos are local-only; commit early and often, and treat container loss as a real risk until RQ-1 is decided.
- L3: Deterministic hashing in the mock needed a splitmix64 finalizer (raw FNV-64a clustered badly on short IDs) — reuse that pattern for any seeded determinism elsewhere.
- L5: One implementation agent per repo at a time — dispatched IG-T007/8 while IG-T005 still held infergate (iter 8); stopped it before damage. Check running agents' repos before every dispatch.
- L4: Environment acquisition order that works: PyPI/Go-proxy/apt-main only. Anything shipped as 'download from GitHub/HF/DockerHub' must be re-sourced via PyPI sdists, Go module proxy (go install), or apt — check before planning any task that needs new binaries/images.

## Deviations index

- none yet (each repo keeps docs/implementation-notes.md §Deviations).
