# Evidence-Based Career Plan: Platform Engineering → Production AI Systems

**Candidate:** Pham Duy Tung — Senior Software Engineer, ~7 years, Ho Chi Minh City, Vietnam
**Research date:** 2026-07-16. All job postings, versions, and links were verified on this date unless flagged. Facts are cited; judgments are marked as judgment.
**Method:** 5 parallel research passes (platform job market, agentic-AI job market, framework/tooling maturity, platform-track resources, AI-track resources) over primary sources (Greenhouse/Ashby/company career pages, official docs, PyPI/GitHub releases, publisher pages), followed by adversarial spot-verification of the most surprising claims (all confirmed: DDIA 2e published Mar 2026; ClickHouse acquired Langfuse Jan 16, 2026; OpenAI acquiring promptfoo Mar 9, 2026; MCP donated to Linux Foundation's Agentic AI Foundation Dec 9, 2025).

---

# Part 1 — Executive Assessment

## Candidate narrative

One coherent, truthful story: **"A distributed-systems and observability engineer expanding into production AI infrastructure and agentic systems."** The evidence base is unusually good for this story: production Kafka/NATS JetStream migrations with zero-loss guarantees, a Loki→ClickHouse observability replatform at 15 TB/month, hybrid keyword+semantic search at 50K searches/day, and a 1,000-tenant SaaS platform. What is missing is (a) infrastructure-as-code and robotics-domain vocabulary for Job A, and (b) any LLM-application, agent, or AI-evaluation evidence for Job B.

The July 2026 job market strongly rewards exactly this profile — with one condition. Our 12-posting agentic-AI sample shows the market is split into two tiers: **AI-infrastructure/platform roles** (Databricks GenAI Platform: "Direct experience developing ML models is a plus but not required"; Temporal AI Foundations lists ML under "Nice to Have"; Glean AI Infrastructure: "ideally" AI/ML infra) that hire strong distributed-systems engineers today, and **agent-product roles** (Harvey, Decagon, Datadog LLM Observability) that hard-require shipped LLM applications. The single most-demanded LLM-specific skill across that sample was **evaluation** (9/12 postings), not model training. Separately, a "LLM Evals & Observability" title family now exists (Datadog, Glean, LangChain/LangSmith, Anthropic) that maps almost one-to-one onto this candidate's observability background — this is the highest-leverage niche identified in this research.

On the platform side, our 13-posting sample confirms the candidate already matches the modal JD (one posting — Inngest — is nearly his CV: Go, Postgres, Redis, ClickHouse, Kafka, K8s, gRPC). Robotics companies (Figure, Foxglove, Skild, Avride) explicitly hire cloud/data-lane platform engineers **without robotics experience**; ROS/MCAP appear only as bonus lines. The recurring hard gap is **Terraform/IaC** (required in ~5/13, bonus in 2 more) and Helm/GitOps for roles literally titled "Platform Engineer."

## Fit scores

| Role | Score /100 | Confidence | Recommendation |
|---|---|---|---|
| **Job A — Platform Engineer (robotics cloud-edge)** | **72** | High (13-posting sample + JD analysis) | **Apply while learning.** Start applying at week 4–6 after IaC evidence + CV reframe. Robotics-specific skills are learnable on the job per market evidence. |
| **Job B — Senior SWE, Agentic AI (agent-product tier)** | **48** | Medium-high | **Complete a substantial project first** (Project 2 minimum credible milestone, ~week 18–20). |
| Job B adjacent — AI Infrastructure / LLM Evals & Observability tier | ~62 | Medium-high | **Apply while learning** from ~week 10–12, once eval + AI-observability vocabulary and a partial Project 2 exist. |

Scoring weights demonstrated production evidence over keyword overlap. Job A score: strong direct evidence on ~60% of requirements, adjacent on ~20%, missing on ~20% (IaC, robotics data, MLOps, explicit API security). Job B score: strong adjacent foundation but zero direct evidence on the LLM-specific half of the requirements list; the score is held up by the seven years of production distributed-systems work the postings themselves say they value.

## Strongest signals (both roles)

1. Zero-message-loss NATS Core→JetStream migration (delivery semantics, acking, persistence — the exact "failure handling, retries, idempotency" language appearing verbatim in LaunchDarkly's JD).
2. Loki→ClickHouse observability replatform: 15 TB/month, −75% query latency, −40% cost — rare, senior, and ClickHouse is explicitly named (bolded) in current postings (LaunchDarkly, Inngest) and is now the storage engine behind Langfuse/ClickStack.
3. High-throughput Kafka consumers in Go with manual offset management and no loss/duplication — durable-skill evidence, transfers to any broker.
4. Production hybrid keyword+semantic search in OpenSearch (~35% accuracy gain, 50K/day) — covers the "retrieval" requirement of agentic-AI postings as actually worded (no posting in our sample named a vector DB).
5. 1,000-tenant SaaS platform with isolation and tiering — multi-tenancy appears in both target JDs and is hard to fake.

## Most important gaps

1. **Terraform/OpenTofu + Helm** (Job A application blocker for "Platform Engineer"-titled roles; cheapest gap to close).
2. **LLM evaluation practice** (Job B's #1 demanded skill; no evidence today).
3. **Agent architecture + durable tool-execution** evidence (Job B application blocker for product-tier roles).
4. **Event-time stream processing** (watermarks, late data, Flink concepts) — interview blocker for streaming-platform questions in Job A.
5. **Robotics data fluency** (ROS 2 concepts, MCAP, sensor-stream characteristics) — differentiator, not blocker; ~15 hours converts "generic backend candidate" into "rare candidate" per Foxglove/Figure JD bonus lines.

## Recommended tracks

**Primary:** Platform Engineer (Job A) — near-term applications from week 4–6.
**Secondary (build in parallel):** Agentic AI (Job B) — with the **LLM Evals & Observability niche as the bridge**, because it monetizes existing OTel/ClickHouse expertise while Project 2 matures.

---

# Part 2 — Requirement Matrices

Evidence classes: **Direct-strong** · **Direct-limited** · **Adjacent** (transferable) · **Portfolio-needed** · **Missing** · **Unknown**.
Gap classes: **AB** = application blocker · **IB** = likely interview blocker · **HD** = helpful differentiator · **OJ** = learnable on the job · **NN** = not necessary.

## Job A — Platform Engineer (robotics cloud-edge)

| Requirement | Importance | CV Evidence | Strength | Gap | Action |
|---|---|---|---|---|---|
| 4+ yrs platform/infra/backend | Must | 7 yrs backend/distributed/platform | Direct-strong | — | Lead with it |
| Go (or Rust/Python/TS) | Must | "High-throughput Kafka consumers in Go with batching, concurrency-safe writes, manual offset management" | Direct-strong | — | — |
| Python | Must | Production Python (pipelines, services) | Direct-strong | — | — |
| Concurrency & systems performance | Must | 5M records aggregated <3 min; 10x OpenSearch reindex; −60% reporting latency | Direct-strong | — | Quantify in CV |
| Kubernetes | Must | "Kubernetes" listed; multi-service production platforms | Direct-limited (depth unproven: no operators/Helm/autoscaling evidence) | IB | Project 1 K8s deploy + autoscaling |
| Docker | Must | Not explicitly on CV (implied by K8s use) | Unknown | AB (trivial) | State explicitly; Project 1 uses it |
| Helm | Should | None | Missing | AB for "Platform Engineer" titles | Weeks 1–3: Helm 4 charts for Project 1 |
| Infrastructure as code (Terraform) | Should | None | Missing | AB (required in ~5/13 sampled postings) | Weeks 1–3: Terraform modules, public repo |
| gRPC | Must | gRPC listed among demonstrated tech | Direct-limited (streaming gRPC unproven) | IB | Project 1 edge gateway uses gRPC streaming |
| Kafka/Flink/streaming | Must | Kafka (deep: offsets, batching, zero-loss migration), NATS JetStream migration | Direct-strong (Kafka) / Missing (Flink & event-time semantics) | IB | Streaming Systems + Learn Flink; Project 1 stream-processing stage |
| REST + WebSockets | Must | REST + Socket.io production experience | Direct-strong (REST), Adjacent (Socket.io→WebSockets) | — | Name WebSockets explicitly (Socket.io is WebSocket-based; truthful) |
| PostgreSQL, Redis | Must | Both in production | Direct-strong | — | — |
| Vector databases | Nice | OpenSearch k-NN/semantic search | Adjacent | HD | 3–4 h pgvector delta |
| Prometheus/Grafana/OTel | Must | Prometheus, OTel, Jaeger, Loki, ClickHouse log store; replatform achievement | Direct-strong | — | Lead with the replatform story |
| Real-time physical sensor/robotics data | Nice-to-have in practice (bonus line in Foxglove/Figure/Avride JDs) | None | Missing | HD (not AB per market evidence) | ROS 2 concepts + MCAP (~15 h); Project 1 simulates sensor streams |
| Edge computing / intermittent connectivity | Should | Adjacent only (durable streams, retries, DLQs) | Adjacent | IB | Project 1: store-and-forward, reconnect, JetStream leaf-node design |
| MLOps: registries, rollout, inference | Nice | None | Missing | OJ / HD | MLflow registry + KServe concepts (~10 h); optional Project 1 extension |
| Distributed training / HIL simulation | Nice | None | Missing | OJ / NN for entry | Awareness only; defer |
| API security: authN/Z, rate limiting, quotas, metering | Should | Multi-tenant SaaS ("data isolation, feature-tier management") = adjacent; idempotency keys direct | Adjacent | IB | Project 1 API layer: OIDC, RBAC, rate limits, metering |
| Developer-platform/API-product experience | Should | Multi-tenant SaaS with onboarding automation for 1,000+ tenants | Adjacent-strong | — | Reframe bullets in platform-product language |

**Gap classification (Job A):** AB: Terraform, Helm, explicit Docker. IB: event-time streaming/Flink, edge patterns, K8s depth, API security specifics, gRPC streaming. HD: robotics data fluency, vector DB, MLOps. OJ: HIL simulation, distributed training, GPU infra, specific robotics formats beyond MCAP. NN: Rust/C++ (only the onboard/edge C++ lane needs them — a different job; avoid per market evidence).

**Job A verdict: 72/100, high confidence. Apply while learning.** Top signals: Go+Kafka depth, ClickHouse at scale, JetStream migration, OTel ownership, multi-tenant SaaS. Top gaps: Terraform/Helm, Flink/event-time, edge patterns, API security evidence, robotics vocabulary.

## Job B — Senior Software Engineer, Agentic AI Systems

| Requirement | Importance | CV Evidence | Strength | Gap | Action |
|---|---|---|---|---|---|
| 5+ yrs software engineering | Must | 7 yrs | Direct-strong | — | — |
| Strong Python | Must | Production Python | Direct-strong (as backend; not yet in LLM context) | — | Project 2 in Python |
| Distributed systems, cloud-native | Must | Full CV | Direct-strong | — | Lead with it |
| Production-scale, reliability, observability, performance | Must | 15 TB/mo o11y platform; zero-loss migrations; 50M rec/mo CDC | Direct-strong | — | — |
| LLM applications | Must | None | Missing | AB (product tier); "plus" (infra tier) | Project 2 |
| RAG (with generation) | Must | Hybrid keyword+semantic OpenSearch search — retrieval half only | Adjacent | AB→closable | Project 2 RAG w/ citations + retrieval evals |
| Agent frameworks / orchestration | Must | Queue/worker + Azure Service Bus ordered workflows = adjacent orchestration | Adjacent | AB (product tier) | Project 2: explicit state machine + durable execution; framework ADR |
| Workflow orchestration (durable) | Must | Transactional outbox, DLQs, retries, idempotency keys | Adjacent-strong | IB | Temporal/DBOS-backed agent workflow |
| Evaluation & benchmarking | Must (top skill in sample: 9/12 postings) | None | Missing | AB | Project 2 eval harness: golden dataset, deterministic checks, judge w/ documented limits, CI regression gate |
| AI observability | Must | OTel/Jaeger/Prometheus/ClickHouse production ownership | Adjacent-strong (best conversion on the list) | HD once converted | OTel GenAI semconv + Langfuse instrumentation of Project 2 |
| Vector DBs / semantic search | Should | OpenSearch semantic + hybrid at 50K/day | Direct-strong (as worded in real postings; none named a vector-DB product) | — | Add pgvector benchmark for vocabulary breadth |
| Knowledge graphs | Nice | None | Missing | NN→P3 | Awareness only; defer |
| Guardrails / safety / prompt injection | Should | None | Missing | IB | Willison + OWASP LLM Top 10; promptfoo red-team suite in Project 2 |
| Cost/latency optimization | Should (emerging wedge: Temporal, Harvey postings) | Deep perf-engineering evidence (75% latency cut, 10x reindex) | Adjacent-strong | HD | Token/cost budgets + caching in Project 2; frame perf history in token/latency terms |
| Model selection & routing | Should | None | Missing | IB | Provider-independent LLM layer with routing/fallback in Project 2 |
| Technical leadership / own architecture→ops | Must | Redesigns/migrations owned end-to-end | Direct-strong (implicit; make explicit) | — | CV bullets: "designed…migrated…operated" |
| Productionizing prototypes / reducing ops complexity | Should | Loki→ClickHouse consolidation; JetStream simplification | Direct-strong | — | — |

**Gap classification (Job B):** AB (product tier): LLM apps, RAG-with-generation, agent architecture, evaluation. IB: durable agent execution, guardrails, model routing, LLM-specific observability vocabulary. HD: AI-observability conversion, cost/latency framing, pgvector. OJ: model serving infra, fine-tuning. NN now: knowledge graphs, distributed training, multi-agent systems (market sample: postings name primitives, not frameworks; "multi-agent" is not a requirement anywhere in our sample).

**Job B verdict: 48/100 product tier (medium-high confidence) — substantial project first; ~62/100 AI-infra/evals-obs tier — apply while learning from ~week 10–12.** Top signals: 7 yrs production distributed systems, Python, retrieval at scale, observability ownership, perf engineering. Top gaps: LLM apps, evals, agent architecture, guardrails, LLM-observability vocabulary.

---

# Part 3 — Prioritized Competency Map

Depth scale: Awareness → Working → Implement (can implement independently) → Operate (production) → Lead (design and lead).

## A. Shared foundation (both roles)

| Skill | Priority | Current → Target depth | Note |
|---|---|---|---|
| Failure models, delivery semantics, idempotency, ordering | P0 | Operate → Lead | Already strong; sharpen theory via DDIA 2e for interview articulation |
| Consistency, consensus, replication, partitioning | P0 | Working → Implement | DDIA 2e Ch. on replication/partitioning/consensus; optional Raft lab |
| Backpressure, load shedding, rate limiting | P0 | Working → Operate | SRE Workbook Ch 11 + Project 1 implementation |
| Capacity planning, tail latency, SLOs | P0 | Working → Operate | SRE Workbook Ch 2, 12; define SLOs in both projects |
| Kubernetes (beyond deploy: probes, HPA, operators-awareness) | P0 | Working → Operate | Project 1 |
| Linux & networking (DNS/TLS/LB) | P1 | Working → Operate | Named in Together/Adyen JDs; refresh, don't re-study |
| API design + security (OAuth2/OIDC, RBAC, quotas, metering) | P0 | Adjacent → Implement | RFC 9700; Project 1 API layer |
| Multi-tenancy | P1 | Operate → Lead | Already differentiated; reuse |
| Testing distributed systems (failure injection, DST awareness, Jepsen literacy) | P1 | Working → Implement | Jepsen analyses + FoundationDB talk; failure-injection scripts in Project 1 |
| Incident response & postmortems | P0 | Operate → Lead | Write real postmortems for both projects |
| Technical writing (ADRs, design docs) | P0 | Unknown → Implement | Named in 4/13 platform JDs; every project artifact doubles as evidence |

## B. Platform / robotics-infrastructure specialization

| Skill | Priority | Target depth | Note |
|---|---|---|---|
| Terraform/OpenTofu | P0 | Implement | Cheapest AB to close |
| Helm (v4) | P0 | Implement | Gates "Platform Engineer" titles |
| Docker (explicit) | P0 | Operate | Make visible; trivial |
| Event-time processing, watermarks, out-of-order data | P0 | Implement | Biggest interview delta vs. current knowledge |
| Flink (concepts + Learn Flink hands-on) | P1 | Working→Implement | Named in only 2/13 sampled JDs but both targets list it; concepts transfer |
| Kafka advanced (internals, EOS, cross-cluster) | P1 | Operate | Already strong; read TDG 2e Ch 6–8, 10 for articulation |
| NATS JetStream edge topologies (leaf nodes, mirroring) | P0 | Implement | Direct store-and-forward answer; builds on existing JetStream production work |
| Edge computing: intermittent connectivity, store-and-forward, clock skew | P0 | Implement | Project 1 core |
| Sensor-data fluency: ROS 2 concepts, MCAP, video/LiDAR/joint-state characteristics | P1 | Awareness→Working | ~15 h; converts candidate tier per JD bonus lines |
| gRPC streaming + flow control | P0 | Implement | Project 1 gateway |
| WebSockets (explicit) | P2 | Working | Socket.io experience transfers |
| Schema evolution (Protobuf/Avro registry) | P1 | Implement | Project 1 ingestion |
| Kubernetes operators (kubebuilder) | P2 | Awareness→Working | Read; build only if time allows |
| Autoscaling, failover, rolling deploys | P0 | Operate | Project 1 |
| ClickHouse telemetry schema design | P1 | Operate→Lead | Delta study on existing strength |
| Object storage patterns (large artifacts) | P1 | Working | Project 1 sensor blobs |
| OAuth2/OIDC, rate limiting, quotas, usage metering | P0 | Implement | Project 1 API |
| MLflow registry, KServe, model rollout concepts | P2 | Awareness→Working | ~10 h; interview vocabulary |
| Time sync (NTP/PTP awareness), event-time vs processing-time | P1 | Working | Project 1 clock-skew handling |
| HIL simulation, distributed training, GPU infra | P3 | Awareness | Defer; learnable on the job |

## C. Agentic AI specialization

| Skill | Priority | Target depth | Note |
|---|---|---|---|
| LLM engineering fundamentals (sampling, context, tokens, failure modes) | P0 | Working | Huyen Ch 2; Karpathy Deep Dive |
| Structured output + tool calling | P0 | Implement | Anthropic/OpenAI docs; Project 2 |
| RAG with generation, chunking, citations, groundedness | P0 | Implement | Builds directly on OpenSearch strength |
| Retrieval evaluation (recall@k, nDCG; hand-rolled) | P0 | Implement | Candidate can outperform typical applicants here |
| Agent state machines, planner-executor (only if justified) | P0 | Implement | Anthropic "Building Effective Agents" taxonomy |
| Durable workflows for agents (Temporal/DBOS), idempotent tool execution | P0 | Implement→Operate | Home-turf conversion; senior differentiator |
| Human-in-the-loop approval | P0 | Implement | Project 2 requirement |
| Evaluation systems: golden datasets, deterministic evaluators, LLM-as-judge limits, CI regression | P0 | Implement→Operate | #1 demanded skill in job sample |
| AI observability: OTel GenAI semconv, Langfuse, token/cost monitoring | P0 | Operate→Lead | Highest-leverage conversion of existing expertise; semconv still pre-stable = contribution opportunity |
| Prompt-injection defense, tool authorization, sandboxing | P0 | Implement | Willison + OWASP; promptfoo red-team |
| Model routing, retries, fallbacks, budget caps | P1 | Implement | Project 2 LLM layer |
| Context management (compaction, notes, sub-agent isolation) | P1 | Working | Anthropic context-engineering post |
| Semantic caching | P2 | Working | Project 2 optional |
| Vector DBs beyond OpenSearch (pgvector) | P1 | Working | ~4 h delta |
| Memory (short/long-term) | P2 | Working | Only where justified in Project 2 |
| Multi-agent orchestration | P3 | Awareness | Market sample: not required; Anthropic's own data (multi-agent ≈15× tokens) argues restraint |
| Model serving (vLLM), fine-tuning | P3 | Awareness | Concepts via Huyen Ch 9 only |
| Knowledge graphs | P3 | Awareness | Defer |

**Highest-leverage dual-purpose skills:** (1) OTel-based AI observability — one skill, both roles, near-unique positioning; (2) durable execution/idempotency for tools — his existing outbox/DLQ patterns are exactly agent-tool-execution patterns; (3) event-time thinking — telemetry pipelines and agent-trace analytics both need it; (4) API security/quotas/metering — platform APIs and model gateways share it; (5) ClickHouse — telemetry store, o11y store, and the engine behind Langfuse.

---

# Part 4 — Ranked Resource Library (30 resources)

Scoring: relevance 25 + depth 20 + practical value 20 + portfolio/interview evidence 15 + credibility 10 + accessibility/maintenance 10 = /100. Labels: **MUST** (must study) · **STRONG** (strong recommendation) · **REF** (reference) · **OPT** (optional). All URLs verified 2026-07-16 unless flagged. Estimated paid spend across the whole library: ≈ US$150–210 (three books; everything else free) — well under the $500 budget. An O'Reilly subscription (~US$49/mo × 3 months) is an alternative that covers R1, R14, R22, R26 at similar cost.

## Shared foundation

**R1. Designing Data-Intensive Applications, 2nd Edition** — Book · Kleppmann & Riccomini, O'Reilly · **Published Mar 2026** (verified) · https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/ (announcement: https://martin.kleppmann.com/2026/03/24/designing-data-intensive-applications-2e.html) · Track: Shared · Level: advanced.
Scope: replication, partitioning, transactions, "trouble with distributed systems," consistency & consensus (Ch 10, near-fully rewritten), batch/stream processing; skim data-model chapters. Why: converts 7 yrs of practice into interview-grade articulation; new edition adds cloud-native and AI-supporting data systems. Reuses: everything already operated in production. Gap: consensus/consistency theory, interview articulation. Time: ~25 h targeted. Output: notes + 5 written system-design answers. **Score 96 — MUST.**

**R2. Google SRE Book + SRE Workbook (selected chapters)** — Book (free online) · Google · sre.google (continuously hosted) · https://sre.google/sre-book/table-of-contents/ · https://sre.google/workbook/table-of-contents/ · Track: Shared · Level: intermediate-advanced.
Scope: SRE Book Ch 3, 4, 6, 19–22, 25; Workbook Ch 2 (Implementing SLOs), 5 (Alerting on SLOs), 11 (Managing Load), 12 (Non-Abstract Large System Design). Why: SLOs/capacity planning are explicit Job A responsibilities; Workbook Ch 12 is the best short capacity-planning tutorial available. Reuses: monitoring-infrastructure ownership. Gap: formal SLO design, capacity planning. Time: 12 h. Output: SLO documents for both projects. **Score 90 — MUST.**

**R3. Jepsen analyses + FoundationDB deterministic-simulation talk + TigerBeetle VOPR** — Analyses/talk/docs · Kyle Kingsbury; Will Wilson; TigerBeetle · 2014–2025 · https://jepsen.io/analyses (incl. TigerBeetle 0.16.11, Jun 2025) · https://www.youtube.com/watch?v=4fFDFbi3toc · https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/internals/vopr.md · Track: Shared · Level: expert.
Scope: 2–3 Jepsen analyses of systems he runs; the Strange Loop DST talk; TigerBeetle's "Fuzzer Blind Spots (Meet Jepsen!)" (2025). Why: "testing distributed systems" is a stated competency; this is interview-differentiating material. Gap: distributed correctness-testing literacy. Time: 8 h. Output: failure-injection scripts for Project 1 informed by these techniques. **Score 82 — STRONG.**

**R4. MIT 6.5840 Distributed Systems (selective)** — University course · MIT PDOS · Spring 2026 site live (verified) · https://pdos.csail.mit.edu/6.824/ · Track: Shared · Level: expert.
Scope: lecture notes for Raft/consistency topics; **Lab 3 (Raft) only, and only if time allows.** Why: consensus implementation depth; but heavyweight (Lab 3 alone 30–60 h) and not the shortest path to either job. Time: 10 h (notes) / +40 h (lab). Output: optional Raft implementation in Go. **Score 74 — OPT** (deprioritized by design; the roadmap does not schedule the lab).

## Platform track

**R5. Streaming Systems** — Book · Akidau, Chernyak, Lax, O'Reilly 2018 (no 2nd ed.; concepts framework-agnostic and current) · https://www.oreilly.com/library/view/streaming-systems/9781491983867/ · Track: Platform · Level: advanced.
Scope: Ch 1–3 (streaming 101/102, watermarks — essential), Ch 5 (exactly-once), Ch 7 (persistent state). Why: event time/watermarks/out-of-order data are the candidate's biggest streaming theory gap and a core Job A requirement. Reuses: deep Kafka/NATS practice. Time: 15–18 h. Output: watermark/late-data design section in Project 1 ADR. **Score 93 — MUST.**

**R6. "The Dataflow Model" paper** — Paper · Akidau et al., VLDB 2015 · https://dl.acm.org/doi/10.14778/2824032.2824076 (note: the old direct vldb.org PDF link is dead — use the ACM DOI) · Track: Platform · Level: advanced.
Scope: full paper. Why: the canonical source for the event-time/processing-time distinction interviewers probe. Time: 3 h. Output: notes. **Score 85 — STRONG.**

**R7. Apache Flink docs + "Learn Flink" hands-on training** — Docs/lab · Apache Flink · **Flink 2.3.0, released 2026-06-25** (verified; 2.x removed legacy APIs — learn on 2.x, know 1.20 LTS exists) · https://nightlies.apache.org/flink/flink-docs-stable/ · training: https://nightlies.apache.org/flink/flink-docs-master/docs/learn-flink/overview/ · Track: Platform · Level: intermediate-advanced.
Scope: all 6 Learn Flink lessons + exercises (apache/flink-training repo); Concepts: Time/Watermarks, State, Checkpointing; Production Readiness Checklist. Why: named in both target-JD skill lists; PyFlink is first-class, no Go API (use Kafka in/out from Go). Time: 20–25 h. Output: Project 1 fleet-health aggregation job. **Score 88 — MUST.**

**R8. Kafka: The Definitive Guide, 2nd ed. (advanced chapters)** — Book · Shapira, Palino, Sivaram, Petty, O'Reilly 2021 · https://www.oreilly.com/library/view/kafka-the-definitive/9781492043072/ · **Flag:** Confluent's "free ebook" page currently describes the 1st edition — get the 2e via O'Reilly. 2021 text predates KRaft-by-default (Kafka 4.x removed ZooKeeper); skip ZooKeeper ops advice and supplement with official KRaft docs · Track: Platform · Level: advanced.
Scope: Ch 6 (Internals), 7 (Reliable Delivery), 8 (Exactly-Once), 10 (Cross-Cluster Mirroring — relevant to edge→cloud), 13 (Monitoring). Why: converts hands-on Kafka skill into internals-level interview answers. Time: 12 h. Output: notes; Kafka-vs-JetStream trade-off ADR in Project 1. **Score 84 — STRONG.**

**R9. NATS JetStream docs + leaf nodes** — Docs · Synadia/CNCF · maintained; **nats-server 2.14.x (Jun 2026); Apache-2.0 status re-confirmed by CNCF May 2025 after the BSL dispute** · https://docs.nats.io/nats-concepts/jetstream · leaf nodes under Running a NATS service → Configuration · Track: Platform · Level: advanced.
Scope: JetStream internals (streams, consumers, replicas, mirroring/sourcing) + leaf-node edge topology. Why: leaf nodes + mirrored streams are the strongest official-doc answer to edge store-and-forward, building directly on his JetStream production migration. Time: 8–10 h. Output: Project 1 edge-buffering design. **Score 90 — MUST.**

**R10. Helm docs + Chart Best Practices** — Docs · Helm (CNCF) · **Helm 4 is current** (v3 docs archived) · https://helm.sh/docs/ · https://helm.sh/docs/chart_best_practices/ · Track: Platform · Level: intermediate.
Scope: Chart Template Guide + all 8 best-practices pages (values, dependencies, labels, pods, CRDs, RBAC). Why: closes an application blocker. Time: 8–10 h. Output: published Helm charts for Project 1 services. **Score 89 — MUST.**

**R11. Terraform tutorials (HashiCorp) + OpenTofu docs as reference** — Tutorials/docs · HashiCorp; OpenTofu (Linux Foundation, v1.12, May 2026) · https://developer.hashicorp.com/terraform/tutorials · https://opentofu.org/docs/ · Track: Platform · Level: intermediate.
Scope: Get Started (one cloud) + Fundamentals (CLI, config language, modules, **state**) + Automate Terraform; OpenTofu deltas (state encryption). Context: Terraform is BUSL/IBM-owned; OpenTofu is the OSS fork — concepts transfer 1:1. Why: the single most recurring hard gap in the platform job sample. Time: 12–15 h. Output: Terraform/OpenTofu modules provisioning Project 1 infra, public repo. **Score 91 — MUST.**

**R12. The Kubebuilder Book** — Docs/lab · kubernetes-sigs · continuously updated · https://book.kubebuilder.io/ · Track: Platform · Level: advanced.
Scope: Quick Start → CronJob tutorial → reconciliation, finalizers, webhooks, envtest. Why: operator literacy for "Platform Engineer" interviews; supersedes the dated *Programming Kubernetes* (2019). Time: 15 h (reading + partial build). Output: optional tiny operator or informed pass. **Score 78 — STRONG (P2; schedule only if ahead).**

**R13. ROS 2 docs (concepts only) + MCAP + Foxglove engineering blog** — Docs/blog · Open Robotics; Foxglove · ROS 2 Jazzy (LTS) / Lyrical Luth (LTS, May 2026); MCAP spec frozen-stable, default ROS 2 bag format · https://docs.ros.org/en/jazzy/Concepts.html · https://mcap.dev/ · https://foxglove.dev/blog/introducing-the-mcap-file-format · https://foxglove.dev/blog/best-practices-for-recording-and-uploading-robotics-data · https://foxglove.dev/blog/best-practices-for-processing-and-analyzing-robotics-data · Track: Platform · Level: intermediate.
Scope: ROS 2 nodes/topics/services/actions, DDS/QoS (loss semantics — maps to his delivery-semantics expertise), rosbag2; MCAP spec + guides; the 3 Foxglove posts (the best public writing on robot telemetry pipelines). Why: converts "no robotics" into credible domain fluency for exactly the bonus lines in Foxglove/Figure JDs. Time: 13–15 h. Output: Project 1 ingests MCAP; a "MCAP→ClickHouse" demo path. **Score 88 — MUST.**

**R14. Formant: "10 key considerations when developing your robot's cloud backend"** — Blog · Formant (~2020; architecturally still sound) · https://formant.io/blog/10-key-considerations-when-developing-your-robots-cloud-back-end/ + https://docs.formant.io/docs/fleet-observability · Track: Platform · Level: intermediate. Scope: full post + fleet-observability docs. Why: practitioner framing of intermittent connectivity, out-of-order sub-second data. Time: 2 h. Output: requirements checklist for Project 1. **Score 76 — REF.**

**R15. ClickHouse observability & schema-design docs** — Docs · ClickHouse Inc. · current · https://clickhouse.com/docs/use-cases/observability · Track: Platform (+AI obs) · Level: advanced.
Scope: "Build-your-own" track (schema design, managing data/TTLs, OTel integration) + best-practices pages (primary key, partitioning, insert batching). Why: sharpens an existing strength into telemetry-warehouse design authority; ClickHouse now also owns Langfuse — one storage story across both tracks. Time: 8 h. Output: Project 1 ClickHouse schema + ADR. **Score 87 — STRONG.**

**R16. OAuth 2.0/OIDC: RFC 9700 + oauth.net (+ OAuth 2 in Action as background)** — RFC/docs/book · IETF (RFC 9700, Jan 2025); Richer & Sanso (2017, partially dated — pair with RFC 9700) · https://datatracker.ietf.org/doc/html/rfc9700 · https://oauth.net/2/ · https://openid.net/specs/openid-connect-core-1_0.html · Track: Platform · Level: advanced.
Scope: RFC 9700 in full; OAuth 2.1 draft summary; OIDC core flows. Why: Job A requires secure APIs (authN/Z, rate limiting, quotas, metering) and CV evidence is only adjacent. Time: 8 h. Output: Project 1 auth design doc + implementation. **Score 83 — STRONG.**

**R17. gRPC guides: performance, flow control, keepalive, deadlines, retry** — Docs · gRPC (CNCF) · maintained · https://grpc.io/docs/what-is-grpc/core-concepts/ · https://grpc.io/docs/guides/performance/ · Track: Platform · Level: intermediate-advanced.
Scope: core concepts + the 6 listed guides. Key fact for the role: established streams bypass load balancing — central to robot-to-cloud link design. Time: 5 h. Output: Project 1 gateway design notes. **Score 82 — STRONG.**

**R18. MLOps pack: Google MLOps whitepaper + MLflow Model Registry + KServe docs** — Whitepaper/docs · Google (2021); MLflow (**3.13, May 2026** — 3.x uses aliases not stages; official Helm chart new in 3.13); KServe (**0.18/0.19rc, CNCF Incubating since Sep 2025**; pre-1.0, expect CRD churn) · https://services.google.com/fh/files/misc/practitioners_guide_to_mlops_whitepaper.pdf · https://mlflow.org/docs/latest/model-registry/ · https://kserve.github.io/website/ · Track: Platform · Level: intermediate.
Scope: whitepaper in full; MLflow registry concepts; KServe concepts + canary rollout. Why: Job A's ML-support responsibilities (registries, rollout, inference) at awareness→working depth. Time: 10 h. Output: model-rollout section in Project 1 "future work" ADR + interview vocabulary. **Score 79 — STRONG.**

**R19. Machine Learning Systems (mlsysbook.ai), edge/ops chapters** — Free open-access textbook · Vijay Janapa Reddi, Harvard/MIT Press 2026, actively updated · https://mlsysbook.ai/ · Track: Platform · Level: advanced. Scope: Vol II deployment/edge/fleet chapters, selectively. Why: the only quality resource covering edge ML ops properly. Time: 8–12 h. Output: notes. **Score 75 — REF/OPT.**

## Agentic AI track

**R20. AI Engineering** — Book · Chip Huyen, O'Reilly, Jan 2025 (current ed.) · https://www.oreilly.com/library/view/ai-engineering/9781098166298/ (ToC verified at https://github.com/chiphuyen/aie-book) · Track: Agentic · Level: intermediate (ideal for senior engineers new to LLMs).
Scope: **Ch 2** (foundation models, sampling, probabilistic failure modes), **Ch 3–4** (evaluation methodology incl. AI-as-judge limits pp. 136–156; designing an eval pipeline), **Ch 5** (prompts incl. defensive prompt engineering), **Ch 6** (RAG & agents, agent failure modes), **Ch 9** (inference optimization: TTFT/TPOT, KV cache, batching — substitutes for deep vLLM study), **Ch 10** (guardrails, router/gateway, caching, monitoring). Skip Ch 1, 7 (except "When to Finetune"), 8. Why: the consensus conceptual spine for exactly this transition. Time: 25–30 h. Output: interview-grade mental models; eval-pipeline design for Project 2. **Score 95 — MUST.**

**R21. Karpathy: "Deep Dive into LLMs like ChatGPT"** — Video · Andrej Karpathy · Feb 2025, 3h31m · https://www.youtube.com/watch?v=7xTGNNLPyMI · Track: Agentic · Level: intermediate.
Scope: full video with notes (tokenization→pretraining→SFT→RLHF, why hallucinations happen). The from-scratch GPT builds (zero-to-hero) are OPT luxuries at 10 h/wk. Why: engineering-level internals without becoming a researcher. Time: 4–5 h. Output: notes. **Score 88 — MUST.**

**R22. Anthropic agent canon: "Building Effective Agents" + engineering-blog series + tool-use docs** — Essay/blog/docs · Anthropic · Dec 2024–Nov 2025 · https://www.anthropic.com/engineering/building-effective-agents · https://www.anthropic.com/engineering/multi-agent-research-system · https://www.anthropic.com/engineering/writing-tools-for-agents · https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents · https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents · https://www.anthropic.com/engineering/advanced-tool-use · tool-use docs: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview · Track: Agentic · Level: intermediate-advanced.
Scope: all listed, in that order. Why: canonical workflow taxonomy (maps naturally to state machines for a distributed-systems engineer); the tools post is the best tool-design doc anywhere; multi-agent post gives the token-economics argument (agents ≈4× chat tokens, multi-agent ≈15×) for justified single-agent design. Time: 8–10 h. Output: Project 2 architecture rationale + tool-design standards. **Score 94 — MUST.**

**R23. Model Context Protocol spec** — Spec · MCP project (Linux Foundation / Agentic AI Foundation since Dec 9, 2025; co-founded by Anthropic, OpenAI, Block) · **current stable revision 2025-11-25; a 2026-07-28 revision lands in ~2 weeks — pin to 2025-11-25 and track the RC** · https://modelcontextprotocol.io/specification/2025-11-25 · Track: Agentic · Level: intermediate.
Scope: full spec (short) + build one small server. Why: de-facto tool-integration standard; named in Anthropic postings. Time: 5–6 h. Output: one working MCP server exposing a read-only diagnostic tool (feeds Project 2). **Score 86 — MUST.**

**R24. Evals canon: Hamel Husain evals FAQ + "Evals for AI Engineers" (book) + applied-llms.org 3-parter + Eugene Yan patterns** — Blog/book/articles · Husain & Shankar (O'Reilly early release); Yan et al. (O'Reilly Radar, 2024) · https://hamel.dev/blog/posts/evals/ · https://hamel.dev/blog/posts/evals-faq/ · https://www.oreilly.com/library/view/evals-for-ai/9798341660717/ · https://www.oreilly.com/radar/what-we-learned-from-a-year-of-building-with-llms-part-i/ (+parts II, III) · https://eugeneyan.com/writing/llm-patterns/ · Track: Agentic · Level: intermediate-advanced.
Scope: both Hamel posts; the book's error-analysis→unit-tests→judge→human-review workflow; all 3 applied-llms parts. Prefer the book over the ~$3–4K Maven cohort course (same material, book price). Why: evaluation was the single most-demanded LLM skill in the job sample (9/12). Time: 12–15 h. Output: Project 2 eval methodology doc + error-analysis workflow. **Score 93 — MUST.**

**R25. promptfoo docs (+ Ragas metric concepts as reference)** — OSS tool/docs · promptfoo (**OpenAI announced acquisition Mar 9, 2026; remains open source under current license** — verified via openai.com and promptfoo blog); Ragas (v0.4, now vibrantlabs — release cadence has slowed; use for metric definitions, not as harness) · https://www.promptfoo.dev/docs/ · https://docs.ragas.io/en/stable/ · Track: Agentic · Level: intermediate.
Scope: promptfoo evals-in-CI + red-team attack packs; Ragas faithfulness/context-precision/recall definitions; hand-roll retrieval metrics (recall@k, nDCG) given OpenSearch background. Why: one CLI-first tool covers regression evals AND injection red-teaming — two rubric lines of Project 2. Time: 8–10 h. Output: CI-gated eval suite + red-team report. **Score 89 — MUST.**

**R26. Langfuse docs + OpenTelemetry GenAI semantic conventions** — Docs/spec · Langfuse (**acquired by ClickHouse Jan 16, 2026; MIT core, self-hostable — v3 self-host needs ClickHouse+Postgres+Redis+S3, all home turf for this candidate**); OTel (conventions moved to dedicated repo; **client/inference spans stable early 2026, agent spans still Development**) · https://langfuse.com/docs · https://langfuse.com/integrations/native/opentelemetry · https://opentelemetry.io/docs/specs/semconv/gen-ai/ · https://github.com/open-telemetry/semantic-conventions-genai · Track: Agentic (+Platform) · Level: advanced.
Scope: self-host Langfuse; emit stable GenAI client-span conventions; gate experimental agent spans behind opt-in. Why: **the highest-leverage item in this library** — converts existing OTel expertise into near-unique AI-observability positioning; pre-stable semconv = live upstream-contribution opportunity. Time: 10–12 h. Output: fully traced Project 2 with token/cost dashboards; optionally a semconv-genai issue/PR. **Score 95 — MUST.**

**R27. Orchestration triad: PydanticAI docs + Temporal AI cookbook + LangGraph concept docs** — Docs · Pydantic (PydanticAI **1.106.0, Jun 2026**, MIT; durable-execution integrations: Temporal, DBOS, Prefect, Restate); Temporal (server 1.31, Python SDK 1.27, MIT; the most battle-tested durable-execution engine); LangChain (LangGraph **1.2.x**; 1.0 GA Oct 2025; MIT core but the production server runtime `langgraph-api` is Elastic License 2.0 — the durable deployment story funnels to commercial LangSmith Deployment) · https://ai.pydantic.dev/ · https://ai.pydantic.dev/durable_execution/overview/ · https://docs.temporal.io/ai-cookbook/openai-agents-sdk-python · https://temporal.io/blog/build-durable-ai-agents-pydantic-ai-and-temporal · https://docs.langchain.com/oss/python/langgraph/overview · Track: Agentic · Level: advanced.
Scope: PydanticAI agents/tools/evals/OTel; Temporal durable-agent pattern (+ DBOS as Postgres-only lighter alternative); LangGraph concepts (graphs, checkpointing, interrupts) for vocabulary/market surface. Why: powers the Project 2 framework ADR; Part 8 explains the selection. Time: 15–18 h. Output: framework-comparison ADR + working durable agent. **Score 92 — MUST.**

**R28. Prompt-injection defense: Simon Willison series + OWASP LLM Top 10 (2025)** — Blog/standard · Willison (2022–present; "The lethal trifecta," Jun 2025; via the series also Meta's "Agents Rule of Two" and DeepMind's CaMeL); OWASP GenAI Security Project (published Nov 2024) · https://simonwillison.net/series/prompt-injection/ · https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ · https://genai.owasp.org/llm-top-10/ · Track: Agentic · Level: intermediate-advanced.
Scope: full trifecta post + series highlights; OWASP LLM01–LLM10 (note LLM08 vector/embedding weaknesses intersects his retrieval expertise). Why: threat model + injection test suite are required Project 2 outputs. Time: 6–7 h. Output: Project 2 threat model + promptfoo red-team config. **Score 88 — MUST.**

**R29. Papers pack: RAG, ReAct, Lost in the Middle, LLM-as-judge, τ-bench/τ²-bench** — Papers · Lewis et al. 2020 (https://arxiv.org/abs/2005.11401); Yao et al. 2022 (https://arxiv.org/abs/2210.03629); Liu et al. 2023 (https://arxiv.org/abs/2307.03172); Zheng et al. 2023 (https://arxiv.org/abs/2306.05685); Sierra τ-bench 2024 (https://github.com/sierra-research/tau-bench) + τ²-bench 2025 (https://arxiv.org/abs/2506.07982) · Track: Agentic · Level: advanced.
Scope: all six, notes-level. Why: judge biases (position/verbosity/self-enhancement) and pass^k reliability are current interview currency; Amazon's corrected tau2-bench-verified is a good benchmark-quality talking point. Time: 8 h. Output: notes; eval-design justification in Project 2. **Score 84 — STRONG.**

**R30. Retrieval delta: OpenSearch neural/vector docs + pgvector** — Docs · OpenSearch (neural sparse search, hybrid score-normalization, k-NN tuning: https://docs.opensearch.org/latest/vector-search/); pgvector (**0.8.2 — update: fixes CVE-2026-3172 in parallel HNSW builds**: https://github.com/pgvector/pgvector) · Track: Agentic (+Platform) · Level: intermediate.
Scope: OpenSearch delta only (he already runs hybrid search); pgvector HNSW/IVFFlat + hybrid with tsvector + small benchmark. Why: reframes an existing strength in RAG vocabulary; Postgres-first RAG stacks dominate interviews. Time: 7–8 h. Output: "BM25 vs dense vs hybrid, OpenSearch vs pgvector, with retrieval evals" benchmark note (feeds Project 2). **Score 85 — STRONG.**

**Explicitly excluded (with reason):** Hands-On Large Language Models (high quality but ~half overlaps his production retrieval experience; internals better via R21) · LLM Engineer's Handbook (fine-tuning/LLMOps focus, agent/eval-light) · vLLM deep study (wrong allocation at 10 h/wk; concepts via R20 Ch 9) · DeepLearning.AI short courses (paced below this profile; "Evaluating AI Agents" and Ng's "Agentic AI" are acceptable warm-ups but redundant with R24/R26) · Understanding Distributed Systems (redundant with R1 at this level) · OpenAI hosted Evals platform (**shuts down Nov 30, 2026** — read the concept guides at https://developers.openai.com/api/docs/guides/evals, build nothing on the product) · Programming Kubernetes 2019 (superseded by R12) · OSS Arroyo (parked post-Cloudflare acquisition) · Semantic Kernel & classic AutoGen (superseded by Microsoft Agent Framework 1.0, GA Apr 2026 — itself only relevant if Azure-centric).

---

# Part 5 — Six-Week Platform Application Sprint (Milestone 1)

Goal: application-ready for Platform roles by end of week 6 (target week 4 for the first applications). Weekly budget 10 h ≈ 6 h build / 2.5 h study / 1.5 h career. No introductory Kafka/OTel/Postgres/Go material anywhere — only new-to-him topics.

| Wk | Objectives | Resources (exact scope) | Implementation task | Deliverable | Verification | Job | Interview Qs unlocked |
|---|---|---|---|---|---|---|---|
| 1 | Terraform working; Docker made explicit; Project 1 scaffold | R11 Fundamentals (CLI, language, modules, state); R14 | Terraform/OpenTofu modules for local kind cluster + one cloud VPC (plan-only to stay $0); Dockerize a Go service skeleton; mono-repo `robot-fleet-platform` with ADR template | Public repo w/ IaC dir, first ADR (architecture sketch), CV draft v1 | `terraform plan` clean in CI; ADR-0001 reviewed against Formant checklist | A | "How do you manage Terraform state/environments?" |
| 2 | Helm charts; K8s depth beyond deploy; edge simulator | R10 Chart Template Guide + best practices; R13 ROS 2 concepts (3 h) | Helm chart for services (probes, HPA, PodDisruptionBudget); Go fleet simulator: joint-state/health/control-ack messages @ configurable rates, disconnect/buffer/resume | Chart repo + running sim on kind; simulator README with data-model doc | `helm install` idempotent; sim survives kill/restart without silent loss (counter check) | A | "Design health checks/autoscaling for a stateful consumer" |
| 3 | Edge→cloud path: gRPC streaming gateway + JetStream ingestion | R17 all guides; R9 JetStream + leaf nodes; R13 MCAP spec (2 h) | Go edge gateway: gRPC bidirectional stream, token auth, batching, compression, retry w/ jitter, bounded buffer + backpressure; publish to JetStream w/ dedup IDs; leaf-node store-and-forward design written up | Working edge→cloud pipeline; ADR-0002 Kafka vs JetStream trade-off (JetStream implemented, Kafka analyzed) | Disconnect test: 10-min outage → zero loss, bounded memory, duplicates only at reconnect boundary (measured) | A | "Design robot fleet ingestion with intermittent connectivity"; "NATS vs Kafka" |
| 4 | Storage + observability E2E; SLOs; **applications open** | R15 schema-design track; R2 Workbook Ch 2; R5 Ch 1–2 (start) | ClickHouse telemetry schema (partitioning, TTL, insert batching); Postgres device registry; OTel traces edge→storage; Grafana: queue lag, E2E ingestion latency p50/95/99, dropped/reconnect counts | Dashboards + SLO doc (ingestion availability, E2E latency); CV v2 + LinkedIn live; 5 applications to distributed-systems platform roles | SLO doc peer-reviewable; trace shows full edge→CH path; CV bullet claims all mapped to evidence | A | "Design a telemetry warehouse; partitioning/TTL choices" |
| 5 | Reliability proof: failure injection, replay, postmortem; benchmark v1 | R3 (FoundationDB talk + 1 Jepsen analysis); R5 Ch 3 | Kill broker/consumer mid-load; replay from stream; duplicate-rate measurement; load test 10/50/200 simulated robots; document DR procedure | Benchmark report v1 (events/s, p50/95/99, recovery time, dup rate, cost estimate); incident postmortem #1; failure-injection scripts | Benchmarks reproducible via script; postmortem follows blameless format | A | "How did you verify no message loss?"; "Walk me through a real recovery" |
| 6 | Milestone 1 gate + interview intensive; robotics-lane applications | R1 (replication/partitioning chs); R6 paper; Part 9 question bank | Fix top 3 weaknesses found in drills; README + architecture diagram + deployment guide polish; API layer v1 (API keys, per-tenant rate limit, usage counter) | **Milestone 1: repo demonstrates IaC+Helm+K8s+edge-sim+JetStream+CH+OTel+benchmark+postmortem**; 5–8 applications incl. robotics cloud-lane (Foxglove/Figure/Skild-class) | Self-mock: 2 system-design prompts recorded + scored vs Part 9 outlines | A | Full Job A bank opens |

**Milestone 1 acceptance:** a stranger can `terraform apply` + `helm install` the stack, run the load test, and see dashboards; ADRs explain Kafka-vs-JetStream and schema choices; CV contains zero unsupported claims. **Learn-on-job (declared, not hidden):** Flink production ops, HIL simulation, model registries at depth, GPU infra, LiDAR specifics.

# Part 6 — Sixteen-Week Agentic AI Transition (Weeks 7–22, Milestone 2)

Goal: credible production-style AI-systems evidence. A simple RAG demo is explicitly insufficient — the gate is the eval + observability + durability triad. ~2 h/wk stays reserved for Job A applications/interviews through week 14. LLM cost guardrail: small/cheap models (Claude Haiku-class / GPT-mini-class) with hard budget caps; estimated total API spend US$60–150 for the whole phase; infra stays local (kind + docker-compose) except optional US$10–30/mo VPS.

| Wk | Objectives | Resources (exact scope) | Implementation task | Deliverable | Verification | Job | Interview Qs unlocked |
|---|---|---|---|---|---|---|---|
| 7 | LLM mental models; first structured calls | R20 Ch 2; R21 full | Provider-independent LLM client (Python): typed structured output (Pydantic), token counting, cost meter, hard budget cap, error taxonomy | `llm-client` module + cost-cap tests | Mock-provider unit tests pass; budget cap provably halts | B | "How do LLMs fail? Sampling vs temperature?" |
| 8 | Tool calling + MCP | R22 (essay + writing-tools + tool-use docs); R23 spec | Tool registry w/ JSON-schema defs, allow-lists, timeouts; one MCP server exposing read-only Prometheus query tool | MCP server repo (small, polished) | Tool-call round-trip traced; malformed-args rejected + logged | B | "Design a tool interface for an agent; why token-efficient responses?" |
| 9 | Retrieval with generation | R30 OpenSearch delta; R20 Ch 6 (RAG half) | Ingest runbooks + system docs (Project 1's own docs = the corpus); hybrid BM25+dense retrieval w/ metadata filters; grounded answers with inline citations | RAG service with citation spans | Manual spot-check: 20 Q&A, citations resolve to real chunks | B | "RAG system design; chunking/hybrid trade-offs" |
| 10 | Retrieval evaluation | R24 Hamel FAQ; R25 Ragas metric defs; R29 (RAG, Lost-in-the-Middle) | Golden retrieval set (~50 queries, labeled); recall@k, MRR, nDCG hand-rolled; hybrid-vs-BM25-vs-dense benchmark incl. pgvector variant | Retrieval eval report + benchmark note | Metrics reproducible in CI; report states limits honestly | B | "How do you evaluate retrieval? What did hybrid buy you?" |
| 11 | Agent core: explicit state machine | R22 taxonomy; R27 PydanticAI | Incident-investigation agent v0: plan → retrieve → tool-call → correlate → report loop as explicit typed state machine; short-term state persisted in Postgres | Agent state-machine diagram + v0 code | Every transition logged; replayable from state table | B | "Agent state management; why not a free-running loop?" |
| 12 | Framework ADR + durable execution | R27 (Temporal AI cookbook, durable-execution docs, LangGraph concepts) | ADR comparing LangGraph vs PydanticAI+Temporal vs custom (Part 8 criteria); implement chosen durable backend; idempotency keys per tool execution; retry/timeout policies; cancellation | ADR-A2 framework selection; durable agent survives worker kill mid-tool-call | Chaos test: kill worker during tool call → resumes exactly-once side effects | B (+A credibility) | "Durable execution for agents; exactly-once tool effects" — **AI-infra tier applications can open here** |
| 13 | Diagnostic tool suite | R22 advanced-tool-use; Project 1 stack as target | Tools: metrics query (Prometheus), log query (ClickHouse), trace lookup (Jaeger), runbook retrieval, service catalog, change history, mock ticket creation; per-tool permissions; read-only default | 7-tool registry w/ authz matrix | Tool-selection traces reviewed on 10 tasks; no unrestricted execution paths | B | "Tool authorization; blast-radius control" |
| 14 | Human-in-the-loop + workflow versioning | R27 (interrupts/signals); R22 harnesses post | Approval gate before any non-read-only action; resumable pause; versioned workflow definitions + rollback | HITL demo (approve/reject/timeout paths) | All 3 paths tested; audit log complete | B | "HITL design; versioning nondeterministic workflows" |
| 15 | Task-level eval harness | R24 book workflow; R25 promptfoo | Curated task dataset (25–40 incident scenarios w/ golden signals from Project 1 failure injections); deterministic evaluators (tool-selection accuracy, citation correctness, unsupported-claim detector vs sources); promptfoo CI gate | Eval harness v1 + regression suite in CI | Baseline scores recorded; CI fails on regression | B | "Design an eval system; deterministic vs judge" |
| 16 | Judge + failure analysis | R29 (MT-Bench, τ²-bench); R24 error analysis | LLM-as-judge for report quality w/ documented bias controls (position/verbosity); human-review rubric; failure classification taxonomy; retry-rate + failure dashboards | Eval report v1: task completion, unsupported-claim rate, latency, cost/task, pass^k-style repeat runs | Judge agreement vs human labels measured on 30 samples and reported honestly | B | "LLM-as-judge limitations — with your own agreement data" |
| 17 | AI observability (flagship week) | R26 (Langfuse + OTel GenAI semconv) | Self-host Langfuse (CH+PG+Redis+S3 — home turf); OTel GenAI spans for every model/tool/retrieval step; token/cost/latency/fallback dashboards; prompt+workflow version tags on traces | Fully traced agent; cost-per-task dashboard; example traces in repo | One trace tells the whole story of a task E2E; semconv stable-span compliance checked | B (+A) | "AI observability architecture" — the differentiator answer |
| 18 | Security hardening | R28 (Willison + OWASP); R25 red-team | Threat model (lethal-trifecta framing); promptfoo injection suite incl. poisoned-runbook attack; output validation; tenant isolation; rate + budget limits; audit log review | Threat model doc + red-team report + fixes | Injection suite passes; residual risks documented, not hidden | B | "Prompt injection defense; Rule-of-Two design" |
| 19 | Production hardening | R2 Workbook Ch 11; R20 Ch 9–10 | K8s deploy (reuse Project 1 Helm/IaC patterns); queue-backed task processing w/ backpressure; provider-outage fallback (model routing); partial-tool-failure degradation; load test | Deployed system + SLO doc (task latency, completion rate, cost/task) | Outage drill: kill provider key → fallback works; overload → sheds gracefully | B | "Reliability for nondeterministic systems" |
| 20 | **Milestone 2 gate** | — | Freeze scope; write design doc, eval report v2, cost report, README, limitations; record 10-min demo; incident scenario + postmortem #2 | **Milestone 2: production-style agent w/ evals + observability + durability + security artifacts** | External review (peer or mock interviewer) against Part 8 acceptance list | B | Product-tier Job B applications open |
| 21 | Job B interview intensive | Part 9 bank; R20 Ch 3–4 reread | Drill 6 system-design prompts + 4 deep-dives on own project; fix weak answers | Written answer outlines; 1 recorded mock | Self-score vs rubrics; iterate | B | — |
| 22 | Public narrative | — | Technical blog post: "Instrumenting an incident-investigation agent with OpenTelemetry GenAI conventions" (or the evals story); GitHub profile polish | Published post + pinned repos | Post reviewed for unsupported claims | A+B | Behavioral: "communication and influence" |

**Milestone 2 acceptance (minimum credible evidence):** eval-gated CI, measured task-completion/unsupported-claim/cost metrics with honest limitations, OTel-traced execution, durable resume-after-crash demo, threat model + red-team results, human-approval flow. This is the line between "shallow LLM demo" and "production evidence."

# Part 7 — Full 24-Week Hybrid Plan

| Phase | Weeks | Focus | Hours | Gate |
|---|---|---|---|---|
| Platform sprint | 1–6 | Project 1 MVM + IaC + CV; Job A applications open wk 4 | 60 | Milestone 1 |
| Agentic core | 7–14 | LLM fundamentals → RAG → agent → durability; Job A interviews in parallel (~2 h/wk) | 80 | Durable agent w/ tools + HITL |
| Evidence layer | 15–20 | Evals + AI observability + security + production; AI-infra applications from wk 12–14 | 60 | Milestone 2 |
| Consolidation | 21–24 | Interview intensives, blog, capstone-lite, final benchmarks | 40 | Milestone 3 |

**Weeks 23–24 (Milestone 3):** Capstone-lite integration (see Part 8 §3): point the Project 2 agent's tools at Project 1's live telemetry stack (they already share Prometheus/ClickHouse/Jaeger by design — weeks 13's tools were built against it). Deliver: one recorded E2E demo (robot-fleet incident → agent investigation → human-approved action → postmortem draft), final benchmark refresh on both projects, 2 full mock interviews per track, application wave 3. **Milestone 3 acceptance:** hybrid narrative demonstrable in one demo; both repos pass the "stranger can run it" test; interview banks internalized.

**Dependency order (hard):** Terraform/Helm → Project 1 deploy → OTel dashboards → failure injection (P1 chain). LLM client → tools/MCP → RAG → retrieval evals → agent → durability → task evals → AI observability → security → production (P2 chain; retrieval evals before agent is deliberate — eval-first habit). Project 1's stack is a prerequisite for Project 2's tool suite (week 13) — this is the integration trick that keeps 24 weeks feasible.

**Decision points:**
- **Week 6:** if Job A interviews are landing, shift up to 3 h/wk to interview prep and stretch phase 2 by 1–2 weeks (plan tolerates this; Milestone 2 slips to wk 21–22).
- **Week 12:** framework ADR decides the durability backend (default: Temporal dev-server via docker-compose; fallback: DBOS if Temporal ops overhead eats build time).
- **Week 14:** if an AI-infra offer process starts, freeze Project 2 scope at wks 15–17 essentials (evals + observability) and cut security week to 4 h — the triad matters more than breadth.
- **Week 20:** capstone go/no-go — integrate only if Milestone 2 fully passed; otherwise weeks 23–24 polish the two separate projects (per spec §12 guidance).
- **Any week:** if job A offer accepted, continue phase 2 at reduced pace (the AI-observability niche compounds inside any platform job).

**Deferred subjects re-taught nowhere (already production-proven):** Kafka basics, OTel basics, PostgreSQL, Go, Redis, queue/worker patterns, multi-tenancy fundamentals.

---

# Part 8 — Project Specifications

## 8.1 Project 1: `robot-fleet-platform` — Cloud-Edge Robot Telemetry Platform

**Problem statement:** operate a simulated fleet of 10–200 robots streaming heterogeneous telemetry over unreliable links into a cloud platform with developer-facing APIs — with provable no-silent-loss semantics and full observability. Substantially beyond a Kafka tutorial by design: the hard parts are disconnection, ordering, idempotency, event time, and operational proof.

**Language split:** all services in Go (per constraints); Flink job in PyFlink or SQL (no Go API exists — verified); load-gen in Go.

### Components

**Fleet simulator (Go):** N robots × message classes — joint states (50–100 Hz, downsampled at edge), pose/motion, device health (0.2 Hz), control acks, synthetic LiDAR metadata + small point-cloud samples (object-storage path), audio/video *metadata* with occasional low-rate sample frames (bytes go to object storage; only references stream through brokers). Each robot: monotonic per-source sequence numbers, deliberate clock skew (±NTP-realistic drift), scripted disconnects (10 s–10 min), local ring buffer with configurable size → **buffered replay on reconnect, no silent loss** (drop policy: oldest-first with dropped-count telemetry — an explicit, measured trade-off, not silence).

**Edge gateway (Go):** gRPC bidirectional streaming (WebSocket fallback endpoint documented, not built); per-device token auth (JWT; device registry issues); batching + zstd compression; retry w/ exponential backoff + jitter; bounded in-flight window = backpressure to simulator; preserves (device_id, source, seq) identity; stamps both event-time and gateway-receive-time to expose skew downstream. Resource mapping: R17 (gRPC flow-control/keepalive/deadlines), R9 (leaf-node pattern as design alternative — documented in ADR).

**Cloud ingestion — NATS JetStream implemented, Kafka as the analyzed alternative (ADR-0002):** JetStream chosen for implementation because (a) candidate has production JetStream migration evidence to deepen, (b) leaf nodes natively model edge store-and-forward, (c) lighter local footprint; Kafka trade-offs (partition-centric ordering, ecosystem, Flink-native connector, cross-cluster mirroring per R8 Ch 10) analyzed in the ADR — interviewers get both stories. Subject-per-message-class; publish dedup via Nats-Msg-Id = hash(device, source, seq); consumer-side idempotency table for effectively-once processing (**claim discipline: "at-least-once delivery + idempotent processing," never "exactly-once delivery"**). Protobuf schemas with explicit versioning + compatibility rules (schema-evolution section in ADR); DLQ subjects + replay tooling; per-tenant stream quotas.

**Stream processing:** Flink 2.3 (R7) for fleet-health aggregation — event-time windows, watermarks with bounded lateness, late-event side-output (counted, stored, not dropped silently), out-of-order handling demonstrated by the simulator's skew. Deliberate scope: one well-built job, not a zoo. RisingWave noted in ADR as the lighter alternative (verified active; Arroyo excluded — parked post-Cloudflare).

**Storage:** PostgreSQL (device registry, tenants, control state, idempotency/dedup tables); ClickHouse (telemetry: partition by day + device-class, ORDER BY (tenant, device, source, event_time), TTLs, async insert batching — R15); Redis (ephemeral presence + token-bucket rate-limit state); MinIO (LiDAR/AV artifacts, content-addressed).

**Platform APIs (Go, REST + gRPC):** device registration/provisioning, telemetry query (time-range + aggregates), command dispatch (idempotency keys, at-most-once execution w/ explicit ack timeout), API keys for services + OIDC (Keycloak or Dex) for users; RBAC (owner/operator/viewer per tenant); token-bucket rate limits; per-tenant quotas; usage metering (request + byte counters → monthly rollup job). Resource mapping: R16.

**Infra:** Docker; kind (local) + one small cloud K8s option; Helm charts per service (R10); Terraform/OpenTofu for cloud path (R11); HPA on consumers (queue-lag-based via KEDA or custom metric); rolling deploys; PodDisruptionBudgets; health/readiness probes everywhere.

**Observability (R2, R15):** OTel traces edge→API; Prometheus metrics; Grafana dashboards: queue lag, E2E ingestion latency (p50/95/99), dropped-message count (edge + broker + consumer separately), reconnect count, late-event count, per-tenant usage, storage growth + cost estimate panel. SLOs: 99.5% ingestion availability; p99 E2E < 5 s under nominal load; zero silent loss (all drops accounted). Alert rules on SLO burn rate.

**Reliability drills (weeks 5, 23):** broker kill, consumer kill mid-batch, gateway partition, ClickHouse outage (buffer + backpressure), replay-from-stream; DR runbook; incident postmortem (blameless format).

**Benchmarks:** 10/50/200 robots; events/s sustained; p50/95/99 E2E latency; recovery time after broker/consumer kill; duplicate rate at reconnect boundaries; CPU/mem per component; storage bytes/robot-day; cost table (local = $0; cloud variant estimate US$20–40/mo on 3 small nodes — stated as estimate).

**Repo outputs (required):** source, architecture diagram (Mermaid/Excalidraw), ADRs (broker choice, schema evolution, delivery semantics, storage layout, auth model), threat model (device spoofing, token theft, tenant crossover, DoS-by-chatty-robot), load-test + failure-injection scripts, benchmark report, dashboards-as-code, example traces (screenshots + exported JSON), postmortem, README, deployment guide, limitations & future work (Flink ops at scale, HIL simulation, model rollout — honest deferrals).

**Acceptance criteria:** stranger-runnable in ≤ 30 min (`make up && make loadtest`); disconnect drill provably lossless; every dashboard panel answers a stated operational question; ADRs argue both sides; zero "exactly-once delivery" claims.

## 8.2 Project 2: `incident-agent` — Production-Grade Incident-Investigation Agent

**Problem statement:** an engineering-operations agent that investigates incidents against a real observability stack (Project 1's), with controlled read-only tools, durable execution, human approval, and a measured eval story. Chosen because it compounds the candidate's strongest real experience (observability, distributed systems) instead of competing with generic chatbot portfolios. Not a chatbot; no unrestricted shell; single agent with an explicit workflow — multi-agent rejected on Anthropic's own token-economics evidence (≈15× tokens) absent measurable value.

### Framework decision (ADR-A2) — three approaches compared

| Criterion | LangGraph (OSS) | **PydanticAI + Temporal (chosen)** | Custom state machine |
|---|---|---|---|
| Durability | Checkpointers good; horizontally-scaled exactly-once runtime (`langgraph-api`) is Elastic-licensed/commercial | Event-sourced replay; survives crash/deploy; battle-tested (Cadence lineage; Netflix/Stripe-class adoption) | Only what you build; easy to get subtly wrong |
| Debuggability | Good w/ LangSmith (paid); middling OSS-only | Temporal UI full history/replay + OTel/Langfuse for agent layer | Your logging only |
| Testability | Graph unit-testable; LLM mocking on you | Time-skipping test framework + PydanticAI `TestModel`, typed DI | You own the harness |
| Observability | LangSmith or DIY | **Best OSS story: PydanticAI is OTel-native (GenAI semconv) → Langfuse** | DIY |
| Lock-in | MIT core, but production durability funnels to ELv2/LangSmith Deployment | MIT end-to-end; four swappable durability backends (Temporal/DBOS/Prefect/Restate) | None (that's the cost) |
| Ops complexity | Low as library / high as platform | Temporal dev-server in docker-compose locally; DBOS (Postgres-only) as lighter fallback | Low infra, high engineering |
| Maturity | 1.0 GA Oct 2025; large deployments (Uber/LinkedIn/Klarna per vendor claims) | Temporal: highest on list; PydanticAI 1.x fast-moving (churn risk noted) | n/a |
| Human approval | First-class `interrupt` | Signals/updates + durable timers; assemble the UX | DIY |
| Failure recovery | Checkpoint resume; coarser retries | Per-activity retries/timeouts/heartbeats — matches tool-execution needs exactly | DIY |

**Selection:** PydanticAI agents on Temporal workflows (tool calls as activities → idempotency, retries, and resume-mid-task come from the platform layer, which is also the candidate's strongest interview story). LangGraph concepts still studied (R27) for market vocabulary. Trade-off accepted: Temporal ops overhead + PydanticAI API churn, in exchange for MIT licensing, OTel-native tracing, and durability the candidate can defend at staff level. DBOS is the documented fallback (decision point wk 12).

### Architecture (summary against spec §11 requirements)

- **API/workflow service (Python/FastAPI):** typed request/response (Pydantic); workflow state in Temporal + investigation record in Postgres; queue-backed task intake; retry/timeout policies per activity; idempotency keys on every tool execution; cancellation; approval steps as signals.
- **LLM layer:** provider-independent interface (direct SDKs behind a port, or LiteLLM — evaluated in ADR); routing: cheap model for extraction/classification, stronger model for synthesis; fallback provider; structured output everywhere; context budget manager (compaction + structured notes per R22 context-engineering post); per-task token + dollar caps; typed error taxonomy (retryable/terminal/needs-human).
- **Retrieval:** hybrid lexical+semantic over runbooks/system docs/service catalog (OpenSearch — reusing production skill; pgvector variant benchmarked); metadata filters (service, severity, doc-type); optional reranking (evaluated, kept only if metrics justify); citations mandatory; ACL-aware retrieval (tenant + role filters at query time); retrieval eval suite (wk 10).
- **Agent design:** explicit typed state machine: `Intake → Plan → Evidence(retrieve|tool)* → Correlate → (NeedsApproval?) → Report → Postmortem-draft`; plan revision allowed with bounded iterations; planner-executor split **not** adopted (single-model loop measured as sufficient; documented). Tool registry w/ permissions; short-term state only (long-term memory rejected as unjustified for incident scope — documented). HITL: approval required for anything non-read-only.
- **Tools (all read-only except mock ticketing):** Prometheus range query; ClickHouse log search; Jaeger trace lookup; runbook retrieval; service-catalog lookup; change-history lookup (git log + deploy events from Project 1); ticket creation in mocked system. No shell. Every call: audit-logged, permission-checked, schema-validated, budgeted.
- **Evaluation:** 25–40 curated incident tasks (grounded in Project 1's failure injections → golden signals are *deterministic*); metrics: task completion, tool-selection accuracy, retrieval recall/nDCG, unsupported-claim rate (claim-to-citation checker), citation correctness, latency, tokens, cost/task, retry rate, failure classification; LLM-judge for report quality with measured human agreement + documented biases (R29); regression suite in CI (promptfoo); human-review rubric.
- **AI observability:** OTel GenAI spans (stable client conventions; experimental agent spans behind opt-in) → self-hosted Langfuse; dashboards: model/retrieval latency, tokens, cost, tool errors, retries, fallback rate, eval scores over time, prompt/workflow version, E2E completion.
- **Security:** threat model (lethal trifecta / Rule-of-Two budget: agent has private data + untrusted inputs → **no unapproved side effects**); prompt-injection suite incl. poisoned-runbook and tool-output injection; tenant isolation; output validation; secret management (K8s secrets → SOPS noted); rate + budget limits; read-only default; full audit trail.
- **Production:** containerized; Helm chart; HPA; queue overload → backpressure + shed with 429s; provider outage → routed fallback (drilled); partial tool failure → degraded-evidence report (labeled); timeout recovery via Temporal; versioned workflows + rollback; SLOs (p95 task latency, completion rate, cost/task ceiling).

**Repo outputs:** all items from spec §11 (source, diagrams, design doc, state-machine diagram, eval dataset + reports, benchmark + cost reports, dashboards, example traces, threat model, injection suite, incident scenarios, postmortem, README, limitations incl. honest discussion of what a real production deployment would still need — real ticketing/paging integration, SSO, longer eval baselines).

**Acceptance criteria (= Milestone 2 gate):** CI eval gate active; unsupported-claim rate measured and reported; crash-resume drill recorded; approval flow demonstrated; threat model + red-team results published; cost/task known to the cent; a senior engineer can read the design doc and find the trade-offs argued, not asserted.

**Cost estimate:** LLM APIs US$60–150 total (small models, cached fixtures for CI evals — judge runs sampled, not exhaustive); infra $0 local; optional VPS US$10–30/mo. Total program spend incl. books: ≈ US$250–400. Within budget.

## 8.3 Optional Capstone — Verdict: integrate lightly, don't merge

Full integration (fleet-ops assistant with control actions) would be **unnecessary scope** in 240 h — it adds demo surface, not new evidence classes; both hiring signals are already covered by the separate projects. However, because Project 2's tools were deliberately built against Project 1's stack (wk 13), a **capstone-lite** costs ~8–10 h in weeks 23–24: one recorded scenario — inject a broker failure into Project 1 → agent investigates real metrics/logs/traces → correlates with change history → recommends action → human approves a (mocked) command dispatch → postmortem draft. This yields the hybrid-narrative demo ("AI operations for a robot fleet") with near-zero new infrastructure. Recommendation: **do capstone-lite only if Milestone 2 passed by week 20**; otherwise polish separately (spec §12 default honored).

---

# Part 9 — Interview Preparation

## 9.1 Job A area map (clustered; fields per spec)

| Area cluster | Core concepts | Likely question | Strong-answer outline | Supporting CV evidence | Missing evidence → practice | Resource |
|---|---|---|---|---|---|---|
| Streaming & delivery semantics (Kafka partitioning, consumer recovery, NATS vs Kafka, exactly-once claims) | Partitions vs subjects; consumer groups; offset vs ack models; EOS = transactions + idempotent producer, never "exactly-once delivery"; dedup + idempotent processing | "Your consumer crashes mid-batch — what happens and what do you guarantee?" | Delivery model → failure window → idempotency table/manual offsets → replay path → measured duplicate rate | Kafka Go consumers w/ manual offsets, zero loss/dup migration; JetStream migration | EOS internals articulation → drill w/ R8 Ch 8 | R8, R9 |
| Event time & stream processing (Flink, backpressure) | Event vs processing time; watermarks; allowed lateness; state backends; checkpoint barriers; backpressure propagation | "Robots reconnect after an hour offline and dump buffered data — how does your aggregation stay correct?" | Event-time windows + watermark strategy → late side-output → replayable source → bounded state | CDC + queue/worker pipelines (processing-time so far — say so honestly) | Watermark design → Project 1 wk 4–5 + R5 Ch 1–3 | R5, R6, R7 |
| Edge→cloud design (intermittent connectivity, store-and-forward) | Local buffering; sequence numbers; reconnect protocols; clock skew; leaf nodes; bandwidth budgets | "Design telemetry ingestion for 10K robots on LTE" | Edge buffer + seq IDs → gateway batching/compression → durable broker w/ dedup → skew-tolerant event time → measured loss/dup SLIs | JetStream persistence + ack production work | Edge specifics → Project 1 wk 3 drill | R9, R13, R14 |
| Kubernetes & delivery (autoscaling, failover, Helm, IaC) | HPA/KEDA on queue lag; PDBs; probes; rolling deploys; GitOps; TF state | "How do you autoscale a consumer without losing ordering?" | Partition/subject-aware scaling → lag-based metric → drain + rebalance handling → PDB + graceful shutdown | K8s production use | Helm/TF depth → Project 1 wks 1–2 | R10, R11, R12 |
| Data stores (PostgreSQL, Redis, ClickHouse) | CH partitioning/ORDER BY/TTL/insert batching; PG for OLTP+idempotency; Redis token buckets | "Why ClickHouse over Loki for logs — and when is it wrong?" | Real migration story: query patterns → columnar wins → cost/latency numbers → when Loki is fine | Loki→CH replatform (−75% latency, −40% cost, 15 TB/mo); CDC OLTP/OLAP split | Nothing major — rehearse numbers | R15 |
| API security & platform product (authN/Z, rate limiting, metering, multi-region awareness) | OAuth2/OIDC flows; RFC 9700 threats; token buckets; quota vs rate limit; metering pipelines | "Design API-key + quota + metering for an external developer platform" | Identity model → key lifecycle → per-tenant buckets in Redis → usage events → billing rollup → abuse handling | Multi-tenant SaaS (1,000+ tenants, tiering, isolation); virtual-currency idempotency | OIDC specifics → Project 1 wk 6 API layer | R16, R2 |
| Observability & incident response (SLOs, capacity, performance debugging) | SLI/SLO/burn rates; RED/USE; trace-first debugging; capacity math (NALSD) | "Define SLOs for the ingestion pipeline and your alert strategy" | SLIs from user promise → burn-rate alerts → dashboards per question → postmortem culture | Owns o11y platform; Prometheus/OTel/Jaeger production | Formal SLO vocabulary → R2 Workbook Ch 2 | R2 |
| Robotics-data fundamentals | ROS 2 topics/QoS ↔ delivery semantics; MCAP structure; sensor rates/sizes (joint state vs LiDAR vs video) | "What's different about robot data vs web telemetry?" | Rates/size classes → QoS trade-offs → bags/MCAP for replay → metadata-vs-blob split | None (say so; pivot to transferable semantics) | All → R13 reading + Project 1 data model | R13 |

## 9.2 Job B area map

| Area cluster | Core concepts | Likely question | Strong-answer outline | Supporting evidence | Missing → practice | Resource |
|---|---|---|---|---|---|---|
| LLM app architecture (routing, structured output, cost/latency) | Context budgets; structured outputs; router/gateway; caching; TTFT/TPOT; token economics | "Design the serving path for an AI feature with a $0.05/task budget" | Model tiering → structured I/O → caching layers → budget caps + metering → measured cost/task | Perf-engineering history (75% latency cut) reframed | Build evidence → Project 2 LLM layer | R20 Ch 9–10 |
| RAG & retrieval evaluation | Chunking; hybrid + normalization; reranking justification; citations; recall@k/nDCG; groundedness | "Your RAG system hallucinates — walk me through diagnosis" | Retrieval-vs-generation fault isolation → retrieval metrics → grounding/citation checker → eval-gated fixes | Production hybrid search @50K/day (+35% accuracy) | Generation half → Project 2 wks 9–10 | R24, R25, R30 |
| Agent state & durable execution | Explicit state machines; checkpointing; idempotent tools; retries/timeouts; cancellation; HITL | "A tool call with side effects times out mid-execution — now what?" | Idempotency key → activity retry semantics → at-least-once + dedup = effectively-once → durable resume → audit trail | Outbox pattern, idempotency keys, DLQs — direct transfer | Agent context → Project 2 wks 11–14 | R27, R22 |
| Evaluation architecture (offline/online, judge limits) | Golden datasets; deterministic evaluators first; judge biases + agreement measurement; pass^k; CI gates; online sampling | "How would you gate an agent release?" | Eval pyramid: deterministic → judge (bias-controlled, agreement-measured) → sampled human review → regression CI → online monitors | Testing discipline from migrations (loss/dup measurement) | All LLM-specific → Project 2 wks 15–16 | R24, R29 |
| LLM observability | OTel GenAI semconv (stable vs experimental); trace-per-task; token/cost dashboards; version tags | "Design observability for a fleet of agents" | Span model per step → cost/latency/quality dashboards → eval scores as time series → version-tagged rollbacks | OTel/Jaeger/CH ownership — strongest transfer | Semconv specifics → Project 2 wk 17 | R26 |
| Safety & security (prompt injection, multi-tenancy) | Lethal trifecta; Rule of Two; tool authz; output validation; tenant isolation; audit | "Your agent reads user-supplied docs and can file tickets — attack it" | Trifecta analysis → capability budget → injection suite results → approval gate → residual risk statement | Multi-tenant isolation experience | Injection practice → Project 2 wk 18 | R28 |
| Reliability for nondeterministic systems | Fallback routing; degraded modes; bounded retries against variance; SLOs on completion rate | "Model provider goes down at 2 a.m. — design for it" | Multi-provider port → health-checked routing → degraded evidence-only mode → drill results | JetStream/ASB failure-handling production work | Provider-failure drill → wk 19 | R20 Ch 10, R2 |
| Productionizing prototypes / ownership | Prototype→prod deltas: evals, o11y, security, cost, ops | "Team hands you a notebook agent that 'works' — first 30 days?" | Eval baseline → instrument → harden tools → budget caps → CI gates → deprecation of prompt-spaghetti | Loki→CH and NATS→JetStream = productionizing migrations | Narrative practice | R24, R22 |

## 9.3 System-design prompts — Job A (12)

1. Edge-to-cloud telemetry for 10,000 robots with hours-long disconnects (loss budget, buffer sizing, dedup).
2. Fleet-wide OTA config/policy rollout with staged canary and rollback.
3. Multi-tenant developer API over robot data: authN/Z, quotas, metering, noisy-neighbor control.
4. Real-time fleet-health dashboard: event-time aggregation with late data (design the watermark story).
5. Video/LiDAR ingestion: metadata-stream + blob-store architecture; when do bytes touch the broker?
6. Migrate a 50M-events/day pipeline from processing-time to event-time without downtime.
7. Command dispatch to robots with at-most-once execution and human-visible outcome tracking.
8. Kafka vs NATS JetStream for this platform — argue both, pick one, defend replication + replay.
9. Regional failover for the ingestion plane (multi-region brokers, what does the edge see?).
10. Telemetry warehouse on ClickHouse: schema, partitioning, TTL, cost model at 15 TB/month (his own numbers).
11. Rate limiting + usage metering that finance can bill from (accuracy vs availability trade-off).
12. Training-data extraction pipeline: from raw MCAP-style logs to versioned, lineage-tracked datasets.

## 9.4 System-design prompts — Job B (12)

1. Incident-investigation agent over metrics/logs/traces with human approval (his Project 2 — must be flawless).
2. RAG over 100K internal docs with ACLs: retrieval, citations, permission-aware caching, eval plan.
3. Eval platform for 20 teams' agents: dataset registry, judge management, CI integration, drift.
4. Model gateway: routing, fallback, budget caps, semantic caching, per-tenant metering.
5. Durable multi-step agent workflow surviving deploys mid-task (Temporal-style reasoning expected).
6. LLM observability stack: span model, token/cost accounting, quality-score time series, version pinning.
7. Customer-support agent with tool side effects: idempotency, approval tiers, audit, injection defense.
8. Prompt/workflow versioning + regression system (nondeterminism, judge variance, rollback criteria).
9. Semantic search + RAG hybrid on OpenSearch vs pgvector: when each, benchmark design.
10. Batch agent processing of 1M documents: queueing, backpressure, cost ceilings, partial failure.
11. Multi-tenant agent platform: tenant isolation across prompts, retrieval corpora, tools, budgets.
12. Groundedness pipeline: claim extraction → citation verification → unsupported-claim rate as an SLO.

## 9.5 Debugging scenarios (10)

1. Consumer lag climbing while throughput flat (rebalance storm? poison message? GC?).
2. Duplicate telemetry rows in ClickHouse after a deploy (dedup table TTL? replay overlap?).
3. p99 ingestion latency 10× at constant p50 (queue head-of-line? partition skew? one slow tenant?).
4. Watermarks stalled → windows never close (idle source? skewed device clock?).
5. gRPC streams drop every ~60 s (LB idle timeout vs keepalive config).
6. K8s consumer pods OOM-killed only during broker failover (redelivery burst, unbounded prefetch).
7. Agent cost/task tripled overnight, no code change (model rerouted? retrieval returning 3× chunks? retry storm?).
8. Agent task-completion eval dropped 15% after a "harmless" prompt edit (regression suite forensics).
9. Judge scores disagree with user complaints (judge bias? dataset drift? metric gaming?).
10. Tool calls intermittently time out and duplicate tickets appear in the mock system (idempotency-key gap in retry path).

## 9.6 Behavioral questions (10) — each mapped to real experience

1. Highest-risk migration you led → **NATS Core→JetStream, zero-loss requirement** (verification design, rollback plan).
2. A time you cut costs without cutting capability → **Loki→ClickHouse (−40% cost, −75% latency)**.
3. Disagreement over architecture → **Kafka manual-offset design vs simpler auto-commit** (correctness argument, data).
4. When you were wrong → choose honestly (e.g., initial OpenSearch reindex design before the 10× queue-driven redesign).
5. Delivering under a hard deadline → **5M-record aggregation <3 min pipeline**.
6. Influencing without authority → **CDC pipeline splitting OLTP/OLAP** (convincing stakeholders reporting could move).
7. Handling a production incident you caused → any migration near-miss; emphasize postmortem + guardrail added.
8. Mentoring/raising the bar → observability standards rollout across services.
9. Long-term ownership → **multi-tenant SaaS platform** evolution (onboarding automation, tiering).
10. Why AI systems now → the Part 10 transition narrative (distributed-systems rigor is what production AI lacks).

## 9.7 Project deep-dive questions (10) — prepare answers before anyone asks

1. Why JetStream over Kafka in Project 1 — and where would Kafka have been better?
2. Prove "no silent loss": what exactly did you measure, and what can still be lost?
3. Your duplicate rate isn't zero — why is that the correct trade-off?
4. Why PydanticAI+Temporal over LangGraph — and steelman LangGraph.
5. Your judge agreement number: how was it measured, and what would make you distrust it?
6. Which eval metric is the weakest and why do you keep it?
7. What breaks first at 10× load in each project?
8. What did the injection red-team find, and what's still exploitable?
9. Cost per task: breakdown, biggest lever, and the floor you can't go below.
10. What would you delete from each project if you rebuilt it?

## 9.8 Production incidents & trade-offs (10)

1. Deploy a breaking schema change to a stream with live consumers — sequencing?
2. Broker disk 90% full at 3 a.m. — shed, expand, or throttle? Argue it.
3. Exactly-once vs at-least-once+idempotency: when is EOS worth the throughput tax?
4. A tenant's replay floods shared infrastructure — isolate without SLA breach.
5. Trace sampling: what do you lose at 1% and when is 100% justified (his 15 TB/mo context)?
6. Agent produced a confidently wrong incident report a human approved — process fix vs system fix?
7. Provider rate-limits you during an incident spike — priority queues, degradation ladder.
8. Eval suite passes but online quality drops — what monitoring closes the gap?
9. Rollback a workflow version with tasks in flight — drain, migrate, or dual-run?
10. Security asks to log all prompts; privacy asks to log none — design the compromise.

## 9.9 Mock interview schedule

Weeks 5–6: two Job A system-design mocks (prompts 1, 8) + one behavioral session — recorded, self-scored against outlines. Weeks 12–14: one Job A mock (maintain) + first Job B design mock (prompt 2). Weeks 20–22: two Job B mocks (prompts 1, 5) + one deep-dive grilling on Project 2 (§9.7) + one incident round (§9.8). Week 24: one full-loop simulation per track. Partners: Pragmatic Engineer-style peer communities, or a trusted senior colleague; record everything, review at 1.5×.

---

# Part 10 — CV, LinkedIn, GitHub, and Application Strategy

Claim labels: **[NOW]** supported now · **[P1]** after Project 1 Milestone 1 · **[P2]** after Project 2 Milestone 2 · **[NO]** not currently supportable.

## 10.1 Professional summary — Platform roles [NOW]

> Senior Software Engineer (7 yrs) specializing in distributed streaming systems, data pipelines, and observability infrastructure. Designed and operated production platforms processing 50M+ records/month and 15 TB/month of logs: migrated messaging to NATS JetStream with zero message loss, rebuilt log storage on ClickHouse (−75% query latency, −40% cost), and built high-throughput Kafka consumers in Go with provable no-loss/no-duplication semantics. Deep in Go, Python, Kubernetes, OpenTelemetry, PostgreSQL/Redis/ClickHouse, and multi-tenant SaaS platforms serving 1,000+ tenants.

## 10.2 Professional summary — Agentic AI roles [P2 — do not use before]

> Senior Software Engineer (7 yrs) building production AI systems on a distributed-systems foundation. Built an incident-investigation agent with durable Temporal-backed execution, permissioned diagnostic tools, human-in-the-loop approval, a CI-gated evaluation suite (task completion, groundedness, cost-per-task), and full OpenTelemetry GenAI tracing into Langfuse. Previously: production hybrid keyword+semantic search (50K queries/day, +35% relevance), zero-loss streaming migrations, and a 15 TB/month observability platform — the reliability and evaluation discipline that production agents require.

## 10.3 Core skills ordering — Job A [NOW]

Go · Python · Kafka · NATS JetStream · Kubernetes (+ Helm, Terraform after P1) · gRPC · PostgreSQL · Redis · ClickHouse · OpenTelemetry/Prometheus/Jaeger/Grafana · Event-driven architecture & delivery semantics · Multi-tenant SaaS & API platforms · Performance engineering.

## 10.4 Core skills ordering — Job B [P2 for the AI items]

Python · Distributed systems & durable workflows (Temporal) · LLM application architecture (tool calling, structured output, routing) · RAG & hybrid retrieval (OpenSearch, pgvector) · LLM evaluation (golden datasets, LLM-as-judge with measured agreement, CI regression) · AI observability (OTel GenAI, Langfuse, token/cost monitoring) · Prompt-injection defense & tool authorization · Go · Kafka/NATS · ClickHouse.

## 10.5 CV bullet improvements (truthful rewrites)

- Before: "Built a CDC pipeline that replicated transactional data into ClickHouse." → After **[NOW]**: "Designed and operated a CDC pipeline separating OLTP from OLAP workloads, replicating 50M+ records/month into ClickHouse and cutting reporting latency ~60%."
- Before: "Migrated messaging infrastructure from NATS Core to JetStream." → After **[NOW]**: "Led zero-message-loss migration from NATS Core to JetStream (persistent storage, explicit acknowledgements) for business-critical streams — designed the verification that proved zero loss."
- Before: "Redesigned an observability platform…" → After **[NOW]**: "Re-architected log/trace storage from Loki to ClickHouse with hybrid trace storage at 15 TB/month: −75% query latency, −40% storage cost."
- Add explicitly **[NOW]**: "Docker-based service delivery on Kubernetes" (implied today, invisible to ATS).
- Add **[NOW]**: "WebSocket-based real-time features (Socket.io)" — truthful naming of an existing skill.
- Move higher: JetStream migration and ClickHouse replatform to the top two bullets (they match 2026 posting language best — LaunchDarkly bolds ClickHouse; "failure handling, retries, idempotency, backpressure" appears verbatim in its JD).

## 10.6 Project bullets (usable only at stated milestones)

- **[P1]** "Built an open-source cloud-edge telemetry platform simulating 200-robot fleets: gRPC-streaming edge gateway with store-and-forward, NATS JetStream ingestion with idempotent processing, Flink event-time aggregation, ClickHouse telemetry warehouse; provisioned via Terraform + Helm; benchmarked p99 ingestion latency and verified zero silent loss under injected broker failures."
- **[P2]** "Built a production-grade incident-investigation agent (Python, PydanticAI + Temporal): permissioned read-only diagnostic tools over Prometheus/ClickHouse/Jaeger, hybrid RAG with mandatory citations, human-in-the-loop approval, CI-gated eval suite (tool-selection accuracy, unsupported-claim rate, cost-per-task), OTel GenAI tracing into self-hosted Langfuse, and a published prompt-injection threat model."

## 10.7 Terms policy

Add when supported: Terraform, Helm, Flink, MCAP/ROS 2 concepts **[P1]**; RAG, agent orchestration, LLM evaluation, AI observability, Temporal **[P2]**. Do **not** add yet **[NO]**: "AI Engineer," "LLM expert," "multi-agent systems," "model training/fine-tuning," "robotics engineer," "MLOps engineer," "vector database administration," "knowledge graphs." No keyword stuffing: every term must trace to a repo, a production system, or a benchmark.

## 10.8 GitHub presentation

Repos: `robot-fleet-platform` and `incident-agent` (descriptive, boring, searchable — judgment: avoid cute names). Each: 60-second architecture diagram at top of README, "run it in 30 minutes" section, benchmark table, ADR directory, limitations section (honesty is the differentiator). Pin both + the MCP server. Profile README: three-line positioning statement + links to the two benchmark reports and the blog post.

## 10.9 LinkedIn

**Headline [NOW]:** "Senior Software Engineer — Distributed Systems, Streaming & Observability | Go · Python · Kafka · ClickHouse · Kubernetes" (append "| Building production AI systems" only at **[P2]**).
**About [NOW, trim at will]:** first paragraph = §10.1 summary; second = "Currently building in public: a cloud-edge robot telemetry platform and a production-grade incident-investigation agent — links below"; third = what he wants (platform/AI-infrastructure roles, remote or APAC).

## 10.10 Spoken narratives

**30-second intro [NOW]:** "I'm a distributed-systems engineer — seven years building streaming platforms and observability infrastructure in Go and Python. I've done the unglamorous hard things: a zero-message-loss broker migration, a ClickHouse observability replatform at 15 terabytes a month, Kafka consumers that moved millions of records with provable no-loss semantics. I'm now applying that reliability discipline to AI infrastructure — durable agent execution, evaluation, and LLM observability."

**Two-minute project narrative [P2 version]:** Problem (incidents need evidence-backed investigation, LLM demos aren't trustworthy) → constraint-driven design (read-only tools, approval gates, budget caps) → the distributed-systems spine (Temporal durability, idempotent tool execution — "an agent tool call is just a side-effecting distributed operation, and we've known how to make those safe for a decade") → the eval story (deterministic golden signals from injected failures; judge with measured human agreement) → the observability story (OTel GenAI → Langfuse; cost per task to the cent) → honest limitations → what he'd do at production scale.

**Transition explanation [NOW]:** "Production AI systems are failing for distributed-systems reasons — unreliable orchestration, no evaluation discipline, no observability. Those are exactly the problems I've spent seven years solving. I'm not switching fields; I'm bringing reliability engineering to the newest class of unreliable systems."

## 10.11 Application strategy

**Job A:** apply from **week 4–6**, not immediately — the two-week IaC investment converts the most common hard screen (Terraform/Helm) and the CV reframe changes ATS outcomes. Close before interviews: event-time vocabulary, edge patterns, API-security specifics. Learnable on the job (say so if asked): Flink ops at scale, HIL simulation, model registries, GPU infra, LiDAR specifics. Explaining no-robotics: "Robotics platform lanes split cloud-side vs onboard. I'm applying to the cloud/data lane, where the problems are streaming, storage, and reliability — my exact background. I've built domain fluency (ROS 2 semantics, MCAP, sensor-data characteristics) and a fleet-telemetry platform to prove the transfer." Translation without exaggeration: "50M records/month CDC" → "high-rate telemetry ingestion"; "JetStream zero-loss" → "fleet uplink reliability"; never claim robot or sensor-hardware experience.

**Job B:** product-tier — apply **after Milestone 2 (~week 20)**; AI-infra/evals-obs tier — from **week 12–14** with partial Project 2 + the OTel story. Minimum credible milestone = the triad: durable execution + measured evals + GenAI-instrumented traces. Positioning semantic search: "I've run hybrid lexical+semantic retrieval in production at 50K queries/day — the retrieval half of RAG. Project 2 added grounded generation, citations, and retrieval evals on top." Premature claims to avoid: agent experience "at scale," fine-tuning, multi-agent, "AI researcher." Differentiators vs demo-portfolio applicants: measured unsupported-claim rates, crash-resume drills, cost-per-task accounting, a threat model — artifacts demo-builders don't have.

**Target-company search:** (1) LLM-observability/evals teams (Datadog, Glean, LangChain, Arize, Braintrust, Langfuse/ClickHouse — note ClickHouse now owns Langfuse and he has deep ClickHouse evidence); (2) durable-execution/infra companies (Temporal, Inngest, Restate — Inngest's posted stack ≈ his CV); (3) robotics cloud-data lanes (Foxglove, Figure, Skild, Nuro, Zipline — note Skild and Glean hire in Bengaluru; Sierra runs APAC agent teams in Singapore/Tokyo); (4) streaming/data platforms (LaunchDarkly-class, Adyen Bengaluru); (5) Vietnam/SEA: global remote-friendly infra companies + regional AI platform teams. Adjacent titles to search: Distributed Systems Engineer, Data/Streaming Platform Engineer, AI Infrastructure Engineer, ML Platform Engineer, LLM/AI Observability Engineer, Applied AI Engineer (infra flavor), Developer Platform Engineer.

**Networking topics:** OTel GenAI semconv (pre-stable — a real contribution niche), event-time correctness war stories, ClickHouse for telemetry/o11y, durable agent execution, eval-gated releases. **Questions for hiring managers:** "How do you evaluate agent changes before release?" · "What does your on-call look like for AI features?" · "Event-time or processing-time in your pipelines, and who owns late data?" · "What's the path from this role to owning architecture?"

**Referral template (≤90 words):** "Hi [name] — I'm a distributed-systems engineer (7 yrs: Go/Python, Kafka/NATS, ClickHouse, Kubernetes, OpenTelemetry) moving toward [platform/AI-infrastructure] work. I noticed [company] is hiring [role]. I've built [one-line most-relevant artifact + link]. Would you be open to referring me, or a 15-minute chat about what the team actually needs? Happy to send my CV and repos."

**Recruiter response template (≤60 words):** "Thanks [name] — interested. Quick fit summary: 7 yrs distributed systems (Go/Python); production Kafka/NATS JetStream with zero-loss migrations; ClickHouse observability at 15 TB/month; Kubernetes + OTel. Recent public work: [repo link]. Based in Ho Chi Minh City (UTC+7), open to [remote/relocation per role]. CV attached — when could we talk?"

**Portfolio introduction (for applications):** "Two production-style systems, built to be audited, not demoed: a cloud-edge robot-fleet telemetry platform (Terraform/Helm/K8s, gRPC streaming, JetStream, Flink event time, ClickHouse — with failure-injection benchmarks) and an incident-investigation agent (Temporal durability, permissioned tools, CI-gated evals, OTel GenAI tracing — with a published threat model). Benchmark reports and ADRs in each repo."

---

# Part 11 — Final Prioritized Actions

**1. Five actions in the next 7 days**
1. Create `robot-fleet-platform` repo; write ADR-0001 (architecture sketch) and the data-model doc.
2. Terraform Fundamentals (R11): CLI, language, modules, state — ~6 h, plan-only to stay at $0.
3. Rewrite CV per §10.1/10.5 (Docker + WebSockets made explicit; JetStream/ClickHouse bullets on top); update LinkedIn headline.
4. Buy/borrow DDIA 2e and AI Engineering; read DDIA replication chapter on commute time.
5. Order the reading queue: save R22 (Anthropic canon) and R13 (Foxglove/MCAP posts) — 30 min of skimming now to calibrate both projects' ambitions.

**2. Top five resources to start immediately:** R11 Terraform tutorials · R1 DDIA 2e · R5 Streaming Systems Ch 1–3 · R10 Helm docs · R13 MCAP/ROS 2/Foxglove pack.

**3. First GitHub deliverable (end of week 2):** `robot-fleet-platform` running locally on kind via `terraform plan` + `helm install` + `make sim` — fleet simulator streaming into the gateway skeleton, with ADR-0001/0002 and a README that states the no-silent-loss goal and how it will be proven.

**4. Earliest reasonable application dates:** Job A distributed-systems platform roles: **week 4** (≈ mid-Aug 2026). Job A robotics cloud-lane: **week 6**. Job B AI-infra/evals-observability tier: **week 12–14** (≈ Oct 2026). Job B agent-product tier: **week 20** (≈ Dec 2026).

**5. Ten highest-priority skills:** Terraform/OpenTofu · Helm · event-time stream processing (watermarks/late data) · edge store-and-forward patterns · API security (OIDC, rate limits, quotas, metering) · LLM evaluation (datasets, deterministic evaluators, judge limits) · durable agent execution + idempotent tools · AI observability (OTel GenAI + Langfuse) · RAG-with-generation on hybrid retrieval · prompt-injection defense & tool authorization.

**6. Three activities explicitly deferred:** model serving/fine-tuning infrastructure (vLLM depth, GPU infra) · multi-agent orchestration (no market requirement found; token economics argue against) · knowledge graphs and MIT 6.5840 labs (high cost, low role-specific yield).

**7. Clearest positioning statement:** **"I make unreliable systems provably reliable — first streaming platforms and observability infrastructure, now production AI agents. Same discipline: measured delivery semantics, evaluation before deployment, and traces for everything."**

---

# Appendix — Research Log & Source Notes

**Research date:** 2026-07-16. **Method:** five parallel research passes over primary sources; independent re-verification of the four most surprising claims.

**Job-market samples:** Platform: 13 postings read (12 full-text) — Figure AI, Anduril (Sydney), Together AI, LaunchDarkly, Adyen (Bengaluru + Amsterdam-flagged), Avride ×2, Foxglove (published 2026-04-02 via Ashby API), Inngest (older-than-180d, still live — flagged), Skild AI ×2, Zipline (Greenhouse API updated_at 2026-06-01). Agentic: 14 postings (10 full-text) — OpenAI Agent Infrastructure, Anthropic AI Observability + Agents Infrastructure (partial), Temporal AI Foundations, Harvey, Glean ×3 (incl. Bangalore), Datadog LLM Observability, Databricks GenAI Platform, Decagon (published 2026-04-01), LangChain, Sierra (partial), Salesforce Agentforce (partial). Frequency statements in this report refer only to these samples. All posting URLs are recorded in the underlying research notes reproduced in Parts 1–2 claims; recency flagged wherever a posting date could not be verified on the primary source.

**Key verified tool/version facts (as of 2026-07-16):** LangGraph 1.2.4 (1.0 GA Oct 2025; `langgraph-api` ELv2) · Temporal server 1.31 / Python SDK 1.27.2 (MIT) · PydanticAI 1.106.0 (durable-execution backends: Temporal/DBOS/Prefect/Restate) · OpenAI Agents SDK 0.17.x (pre-1.0) · Microsoft Agent Framework 1.0 GA Apr 2026 (Semantic Kernel/AutoGen legacy) · MCP spec 2025-11-25 (Linux Foundation AAIF since 2025-12-09; next revision 2026-07-28) · Ragas 0.4.3 (cadence slowed) · promptfoo (OpenAI acquisition announced 2026-03-09; stays OSS) · DeepEval 4.x · Langfuse v3.21x (ClickHouse acquisition 2026-01-16; MIT core) · OTel GenAI semconv: client spans stable, agent spans experimental, dedicated repo · vLLM 0.22.1+ · Qdrant 1.18 · pgvector 0.8.2 (CVE-2026-3172 fix) · Flink 2.3.0 (2026-06-25) · Kafka 4.3.1 · NATS server 2.14.x (Apache-2.0 confirmed by CNCF May 2025) · MCAP frozen-stable · KServe 0.18/0.19rc (CNCF Incubating) · MLflow 3.13 · DDIA 2e published Mar 2026.

**Uncertainty statement:** posting-frequency counts are small-sample and directional, not market statistics; several postings' publication dates were unverifiable (flagged); fast-moving libraries (PydanticAI, promptfoo, vLLM, LangGraph) will have newer versions within weeks — re-verify at time of use; salary figures quoted in research came from posting pages and were not independently audited. Everything labeled "judgment" is the author's assessment, not a sourced fact.





