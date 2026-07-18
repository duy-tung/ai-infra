# Evidence-Based Career, Learning, Portfolio & Interview Plan — Pham Duy Tung

*Research date: July 16, 2026. Candidate: Pham Duy Tung, Senior Software Engineer (~7 yrs), Ho Chi Minh City, Vietnam. This plan is decision-oriented: it takes positions, ties every recommendation to the candidate's actual CV evidence and one/both target jobs, and flags uncertainty explicitly.*

## TL;DR
- **Apply to Platform Engineer (Job A) now**, in parallel with a focused 6-week sprint — Tung's streaming/observability/reliability CV is a strong, direct match (fit **78/100**); the only real interview gaps (Flink/event-time, Helm/Terraform/Docker as artifacts, explicit authn/authz + metering) are closable with Portfolio Project 1.
- **Do NOT apply to Agentic AI (Job B) yet** — current fit is **46/100** (adjacent, not direct). Semantic search ≠ RAG, and general observability ≠ AI evaluation. Build Portfolio Project 2 (a durable, evaluated incident-investigation agent) first; that lifts credible fit to ~70/100.
- **One coherent narrative:** "A distributed-systems and observability engineer expanding into production AI infrastructure and agentic systems." Primary track = platform/streaming; secondary = production AI infrastructure. Total plan fits 24 weeks × 10 h/week (60% build / 25% study / 15% interview+CV), with API/cloud cost kept under ~USD 150 plus one paid book.

---

## Part 1 — Executive Assessment

Tung is a genuinely strong distributed-systems, streaming, and observability engineer. His CV maps cleanly onto **Target Job A (robotics developer Platform Engineer)** and only **adjacently** onto **Target Job B (Senior SWE, Agentic AI)**. The right move is to monetize the strong match immediately while building the missing evidence for the aspirational one — not to rebrand prematurely as an "AI engineer."

- **Platform Engineer (Job A) fit: 78/100, high confidence.** Weighted toward demonstrated production evidence, not keyword overlap.
- **Agentic AI (Job B) fit: 46/100 now → ~70/100 after Project 2, medium confidence.**
- **Recommended primary track:** Platform / streaming / infrastructure. **Secondary:** production AI infrastructure & agentic systems.

**Most important strengths (production-verified):** CDC→ClickHouse OLTP/OLAP separation (50M+ records/month, ~60% reporting gain); observability platform at **15+ TB logs/month** (Loki→ClickHouse migration, ~75% query-latency and ~40% storage-cost reduction); NATS Core→JetStream migration with **zero message loss** for critical streams; Go Kafka consumers migrating **millions of records without loss or duplication** (batching, concurrency-safe writes, manual offset management); hybrid keyword+semantic OpenSearch search (~35% accuracy gain over 50,000+ daily searches); multi-tenant SaaS at **1,000+ tenants**.

**Most important gaps:** For Job A — Flink/stream-processing engine, Helm/Terraform/Docker as artifacts, robotics/sensor/edge data, explicit authn/authz + rate limiting/metering implementation. For Job B — production LLM apps, RAG-with-generation, agent architecture, durable agent execution, LLM evaluation, AI observability/cost, production vector-DB operation.

---

## Part 2 — Requirement Matrices

Evidence classes: **Direct & strong / Direct but limited / Adjacent & transferable / Portfolio evidence needed / Missing / Unknown.** Gap classes: **application blocker / interview blocker / helpful differentiator / learnable on the job / unnecessary.**

### Job A — Robotics Developer Platform Engineer
| Requirement | Importance | CV Evidence | Strength | Gap class | Action |
|---|---|---|---|---|---|
| 4+ yrs platform/infra/backend | P0 | 7 yrs senior distributed backend | Direct & strong | none | Lead CV with it |
| Go | P0 | Go Kafka consumers; queue/worker pipelines | Direct & strong | none | Feature Go |
| Streaming (Kafka/Flink or similar) | P0 | Kafka, NATS JetStream; 50M+ rec/mo | Direct & strong (Kafka); Missing (Flink) | interview blocker (Flink) | Learn Flink event-time |
| Kubernetes / Docker / Helm | P0 | Kubernetes in CV | Direct (K8s); Missing (Helm/Docker explicit) | interview blocker | Add via Project 1 |
| gRPC | P1 | gRPC listed | Direct but limited | none | Deepen streaming gRPC |
| PostgreSQL / Redis | P0 | Both in CV | Direct & strong | none | — |
| Observability (Prom/OTel/Grafana) | P0 | 15 TB/mo platform; OTel, Jaeger, Loki | Direct & strong | none | Signature strength |
| IaC (Terraform/OpenTofu) | P1 | none | Missing | helpful differentiator | Learn in Project 1 |
| Real-time sensor/robotics data | P1 | none | Missing | learnable on the job | Simulate in Project 1 |
| Edge computing / intermittent connectivity | P1 | none | Missing | helpful differentiator | Project 1 edge gateway |
| Vector databases | P2 | OpenSearch vector-style retrieval | Adjacent & transferable | learnable on the job | Optional |
| MLOps / model registry / inference | P2 | none | Missing | learnable on the job | Awareness only |
| API security / rate limiting / quotas / metering | P1 | multi-tenant SaaS; feature-tier mgmt | Adjacent & transferable | interview blocker (explicit impl) | Implement in Project 1 |
| Autoscaling / failover / incident response | P0 | reliability eng; performance work | Adjacent & transferable | none | Frame explicitly |

**Five strongest signals:** observability platform at 15 TB/mo; JetStream zero-loss migration; Go Kafka loss/duplication-free migration; multi-tenant SaaS (1,000+ tenants); CDC→ClickHouse. **Five largest gaps:** Flink/stream-processing engine; Helm/Terraform/Docker as artifacts; robotics/sensor data; explicit authn/authz + rate limiting; edge/intermittent connectivity. **Recommendation: apply while learning; complete Project 1 MVP before onsite interviews.**

### Job B — Senior SWE, Agentic AI Systems
| Requirement | Importance | CV Evidence | Strength | Gap class | Action |
|---|---|---|---|---|---|
| 5+ yrs SWE | P0 | 7 yrs | Direct & strong | none | — |
| Strong Python | P0 | Python pipelines/services | Direct but limited (depth) | none | Deepen typed Python |
| Distributed systems / cloud-native | P0 | extensive | Direct & strong | none | Core strength |
| Reliability / observability / performance | P0 | 15 TB/mo; ~75% latency cut | Direct & strong | none | Bridge to AI obs |
| Semantic / hybrid search | P1 | OpenSearch hybrid search | Direct & strong | none | Position as retrieval |
| Production LLM apps | P0 | none | Missing | application blocker | Project 2 |
| RAG (with LLM generation) | P0 | retrieval only; no generation | Adjacent (retrieval); Missing (generation) | application blocker | Project 2 |
| Agent architecture / tool use / durable execution | P0 | event-driven workflows, DLQ, outbox | Adjacent (workflow); Missing (agent) | application blocker | Project 2 |
| LLM evaluation / benchmarking | P0 | none | Missing | application blocker | Project 2 eval harness |
| AI observability / token-cost monitoring | P1 | strong general observability | Adjacent & transferable | interview blocker | Project 2 (OTel GenAI) |
| Vector-DB operation | P1 | OpenSearch kNN adjacent | Adjacent & transferable | helpful differentiator | Project 2 |
| Knowledge graphs | P2 | none | Missing | unnecessary now | Defer |
| Technical leadership across AI platform | P1 | long-term platform ownership | Adjacent & transferable | helpful differentiator | Frame ownership |

**Five strongest signals:** 7 yrs production ownership; distributed backend + reliability; hybrid search/retrieval; observability depth; high-volume concurrency. **Five largest gaps:** production LLM apps; RAG-with-generation; agent/durable execution; LLM evaluation; AI observability/cost. **Recommendation: complete a substantial project first (Project 2) before applying.** The candidate must not be presented as an experienced Agentic AI engineer until Project 2 exists.

---

## Part 3 — Prioritized Competency Map

Priority P0 (needed to pass interviews / do the job) → P3 (defer). Depth: Awareness → Working → Can implement → Can operate in production → Can design & lead.

### A. Shared foundation (both roles)
- Delivery semantics, idempotency, ordering, exactly-once claims/trade-offs — **P0, Can design & lead** (already strong; deepen theory).
- Distributed failure models, consistency, consensus, replication, partitioning — **P0, Can design & lead** (DDIA + MIT 6.5840).
- Backpressure, load shedding, rate limiting, capacity planning, tail latency — **P0, Can operate in production**.
- SLOs, incident response, postmortems — **P0, Can design & lead**.
- API design, multi-tenancy, security (authn/authz) — **P0, Can implement independently** (make authz explicit).
- Testing distributed systems; Linux; networking; Kubernetes — **P0/P1, Can operate in production**.
- OpenTelemetry / Prometheus / Grafana — **P0, Can design & lead** (signature strength).

**High-leverage skills that benefit BOTH roles:** OpenTelemetry (extends to GenAI semantic conventions); reliability/SLOs (extends to nondeterministic AI systems); idempotency & durable workflows (extends to idempotent tool execution); hybrid retrieval (extends to RAG); multi-tenancy + rate limiting (extends to model-gateway/quotas); typed Python services.

### B. Platform / robotics-infra specialization
- Event-time processing, watermarks, out-of-order/late data, Flink/Kafka Streams — **P0, Can implement** (gap).
- gRPC streaming, WebSockets, schema evolution — **P1, Can implement**.
- Edge computing, store-and-forward, intermittent connectivity, time sync/clock skew — **P1, Working→Can implement** (gap).
- Sensor/telemetry ingestion (video/LiDAR/audio/joint-state formats) — **P1, Working** (gap).
- Helm, Terraform/OpenTofu, K8s operators, autoscaling/failover — **P0/P1, Can implement** (gap as artifacts).
- Object storage; ClickHouse (have); vector storage — **P1/P2**.
- API gateways, OAuth 2.0/OIDC, quotas, usage metering — **P1, Can implement** (gap: explicit).
- Model registries, model rollout, ML metadata, training-data lineage, HIL simulation, ROS 2/DDS concepts — **P2, Awareness→Working** (learnable on the job).

### C. Agentic AI specialization
- Transformer/LLM engineering fundamentals, tokenization, context windows, embeddings — **P0, Working→Can implement**.
- Retrieval, hybrid search (have), reranking, chunking, query transformation, grounded generation — **P0, Can implement** (build on OpenSearch).
- Structured output, tool calling, MCP — **P0, Can implement** (gap).
- Planning, agent state machines, durable workflows, human-in-the-loop workflows — **P0, Can implement** (gap; core of Project 2).
- Short/long-term memory, multi-agent trade-offs, model routing/fallback — **P1/P2, Working** (avoid over-engineering).
- Idempotency for tool execution, sandboxing, prompt-injection defense, tool authorization — **P0/P1, Can implement** (bridge from backend security).
- Eval datasets; offline/online eval; task-completion eval; LLM-as-judge limits; deterministic evaluators; groundedness; retrieval eval; regression; latency/cost eval — **P0, Can implement** (single biggest differentiator; gap).
- Agent tracing, AI observability, token/cost monitoring, AI incident response — **P0/P1, Can implement** (bridge from OTel strength).
- Vector-DB ops, semantic caching, model gateways, rate limiting, multi-tenancy, production deployment — **P1, Can implement**.
- Knowledge graphs — **P3, Awareness** (defer).

---

## Part 4 — Ranked Resource Library (28)

Scoring: relevance to the two jobs (25) + technical depth/correctness (20) + practical value (20) + interview/portfolio evidence (15) + source credibility (10) + accessibility/maintenance (10). Canonical distributed-systems papers are not penalized for age; recency is weighted for LLM/agent/observability/Kubernetes/stream tooling.

### Shared foundation
1. **Designing Data-Intensive Applications, 2nd ed.** — Kleppmann & Riccomini, O'Reilly. https://dataintensive.net/ — *Book, both, expert.* Study: replication, partitioning, transactions, "The Trouble with Distributed Systems," consistency & consensus, batch & stream processing chapters. Reuses: streaming/CDC/Kafka experience shortens ramp. Gap: distributed-correctness theory. ~30 h. Output: design notes. **96 — Must study.**
2. **MIT 6.5840 Distributed Systems (Spring 2026)** — Morris et al. https://pdos.csail.mit.edu/6.824/ — *University course w/ labs, Shared, advanced.* Go labs: MapReduce, KV server, Raft, fault-tolerant KV. Reuses: Go fluency. Gap: consensus by implementation. ~40 h (Labs 1–3). Output: Raft implementation on GitHub. **95 — Must study.**
3. **Google SRE Book + Workbook** (free) — https://sre.google/books/ — *Book, both, advanced.* Study: SLIs/SLOs/error budgets, alerting on SLOs, cascading failures, postmortems, Appendix A/B (SLO doc + error-budget policy). Reuses: reliability experience. ~12 h. Output: SLO doc for Project 1. **90 — Must study.**
4. **OpenTelemetry docs + "Inside the LLM Call: GenAI Observability" (2026)** — https://opentelemetry.io/ and https://opentelemetry.io/blog/2026/genai-observability/ — *Docs/blog, both, intermediate.* Study: traces/metrics/logs; GenAI semantic conventions (`gen_ai.*`, `invoke_agent`/`execute_tool` spans, token counts). ~8 h. Output: instrumented services in both projects. **90 — Must study.**

### Platform / streaming
5. **Kafka: The Definitive Guide, 2nd ed.** (Confluent, free) — https://www.confluent.io/resources/ebook/kafka-the-definitive-guide/ — *Book, Platform, advanced.* Study: reliable data delivery, exactly-once/transactions, consumers/offsets, cross-cluster mirroring. Reuses: manual offset mgmt. ~12 h (skip intro). Output: trade-off doc. **88 — Strong.**
6. **Apache Flink docs — Timely Stream Processing & Generating Watermarks** — https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/ — *Official docs, Platform, advanced.* Study: event vs processing time, watermarks, bounded-out-of-orderness, late data/allowed lateness, side outputs, per-partition watermarks. Gap: stream-processing engine. ~16 h. Output: fleet-health aggregation job. **90 — Must study.**
7. **Confluent Apache Flink 101** (free course) — https://developer.confluent.io/courses/apache-flink/ — *Course, Platform, intermediate.* Study: event-time & watermarks, windowing modules. ~6 h. Output: hands-on notes. **82 — Strong.**
8. **NATS JetStream docs** — https://docs.nats.io/nats-concepts/jetstream — *Official docs, Platform, intermediate.* Study: streams, consumers, retention (limits/work-queue/interest), exactly-once *publish* dedup + double-ack, and the caveat that exactly-once *processing* across systems remains the application's job. Reuses: JetStream migration. ~5 h. Output: trade-off analysis vs Kafka. **85 — Strong.**
9. **Kubernetes + Helm + Terraform official docs** — https://kubernetes.io/docs/ , https://helm.sh/docs/ , https://developer.hashicorp.com/terraform/docs — *Docs, Platform, intermediate.* Study: Helm charts, provider basics, HPA autoscaling, health/readiness. Gap: IaC/Helm artifacts. ~14 h. Output: Project 1 deployment. **84 — Strong.**
10. **gRPC docs — streaming** — https://grpc.io/docs/ — *Docs, Platform, intermediate.* Study: bidirectional streaming, deadlines, backpressure. ~5 h. Output: edge gateway. **80 — Reference.**
11. **ROS 2 concepts + DDS middleware docs** — https://docs.ros.org/en/humble/Concepts.html — *Docs, Platform, intermediate (Awareness).* Study: nodes/topics/QoS, DDS/RTPS, RMW abstraction. Purpose: robotics vocabulary for interviews only. ~4 h. Output: glossary notes. **76 — Reference.**
12. **ClickHouse docs (ingestion/perf)** — https://clickhouse.com/docs — *Docs, Platform, intermediate.* Study: async inserts, MergeTree, TTL. Reuses: strong ClickHouse experience. ~3 h. Output: telemetry schema. **78 — Reference.**
13. **Six Robotics — Senior Data Platform Engineer JD** (market signal) — https://careers.sixrobotics.com/jobs/7850241-senior-data-platform-engineer — *Job posting, Platform.* Validates real demand for schema-evolution, time-series/high-rate telemetry, and media-alongside-structured-data. **72 — Reference.**

### Agentic AI
14. **AI Engineering** — Chip Huyen, O'Reilly 2025 — https://www.oreilly.com/library/view/ai-engineering/9781098166298/ ; free companion repo https://github.com/chiphuyen/aie-book — *Book, Agentic AI, advanced.* Study: evaluation chapters, RAG & Agents (Ch. 6), inference optimization, AI architecture & user feedback (Ch. 10). Reuses: retrieval/eval instincts. ~24 h. Output: eval framework design. **95 — Must study.** (This is the single paid resource — within the USD 500 budget.)
15. **Anthropic — "Building Effective Agents"** — https://www.anthropic.com/research/building-effective-agents — *Engineering essay, Agentic AI, intermediate.* Study: workflows vs agents; the five patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer); "start simple, add complexity only when it delivers measurable value." ~3 h. Output: architecture ADR. **93 — Must study.**
16. **Model Context Protocol — spec + Python SDK** — https://modelcontextprotocol.io/ and https://github.com/modelcontextprotocol/python-sdk — *Spec + maintained SDK, Agentic AI, intermediate.* Study: tools/resources/prompts primitives, JSON-RPC, security (explicit human consent; treat tool descriptions/inputs as untrusted). ~8 h. Output: MCP diagnostic-tool server. **88 — Strong.**
17. **LangGraph docs — persistence, interrupts, durable execution** — https://docs.langchain.com/oss/python/langgraph/persistence , /interrupts , /durable-execution — *Official docs, Agentic AI, advanced.* Study: checkpointers/threads; `interrupt()` + `Command(resume=…)` for human approval; durability modes `exit`/`async`/`sync`. Note the official caveat that on resume "the runtime restarts the entire node from the beginning." LangGraph 1.0 reached GA in late October 2025 "with no breaking changes" after "more than a year of powering agents at companies like Uber, LinkedIn, and Klarna"; the current PyPI release is **langgraph 1.2.9** (mid-2026). ~12 h. Output: HIL approval workflow. **90 — Must study.**
18. **Temporal docs + LangGraph integration** — https://docs.temporal.io/ and https://docs.temporal.io/develop/python/integrations/langgraph — *Official docs, Agentic AI, advanced.* Study: workflow/activity determinism, event-history replay, retries/timeouts. Purpose: durability trade-off analysis (note the integration is labeled pre-stable). ~6 h. Output: framework-choice ADR. **84 — Strong.**
19. **DeepEval docs** (pytest-style LLM eval) — https://deepeval.com/ — *Docs, Agentic AI, intermediate.* Study: faithfulness, answer relevancy, contextual recall/precision, RAG metrics, CI/pytest integration, debuggable judge reasoning. ~8 h. Output: regression eval suite. **86 — Strong.**
20. **RAGAS docs** — https://docs.ragas.io/ — *Docs, Agentic AI, intermediate.* Study: faithfulness, answer relevance, context precision/recall; no-ground-truth metrics *and* their NaN/limitations. ~4 h. Output: retrieval eval report. **82 — Strong.**
21. **τ-bench / τ²-bench (Sierra)** — arXiv https://arxiv.org/abs/2406.12045 ; maintained repo https://github.com/sierra-research/tau2-bench — *Benchmark + paper, Agentic AI, advanced.* Study: tool-agent-user interaction, `pass^k` consistency, policy adherence. Reality check the paper reports: "even state-of-the-art function calling agents (like gpt-4o) succeed on <50% of the tasks, and are quite inconsistent (pass^8 <25% in retail)." Purpose: design task-completion & tool-selection eval. ~5 h. Output: eval dataset design. **84 — Strong.**
22. **Berkeley Function-Calling Leaderboard (BFCL, V4)** — https://gorilla.cs.berkeley.edu/leaderboard.html — *Benchmark, Agentic AI, advanced.* Study: AST + executable tool-call evaluation across languages; multi-turn/agentic tasks; ability to abstain. Purpose: tool-selection accuracy methodology. ~3 h. Output: metric definitions. **80 — Reference.**
23. **OpenTelemetry GenAI semantic conventions** (OTel SIG + Datadog/Greptime references) — https://opentelemetry.io/blog/2026/genai-observability/ — *Standard + vendor guides, Agentic AI, intermediate.* Study: `gen_ai.usage.input_tokens`/`output_tokens`, cost, tool spans; note most conventions are still experimental as of 2026. ~4 h. Output: AI dashboards. **82 — Strong.**
24. **OWASP Top 10 for LLM Applications** — https://genai.owasp.org/ — *Standard, Agentic AI, intermediate.* Study: prompt injection (LLM01), excessive agency (LLM06); mitigations (least privilege, human-in-the-loop checkpoints, kill switches). ~3 h. Output: threat model + prompt-injection tests. **83 — Strong.**
25. **LangChain "State of AI Agents" report (2025→26)** — https://www.langchain.com/state-of-agent-engineering — *Industry survey, Agentic AI.* Market validation from 1,340 respondents (surveyed Nov 18–Dec 2, 2025): 57.3% now run agents in production (up from ~51% the prior year); "Nearly 89% of respondents have implemented observability for their agents, outpacing evals adoption at 52%" (52.4% offline, 37.3% online evals; human review 59.8% and LLM-as-judge 53.3% lead eval methods). ~1 h. **70 — Reference.**
26. **Chip Huyen aie-book chapter summaries** (free) — https://github.com/chiphuyen/aie-book/blob/main/chapter-summaries.md — *Companion, Agentic AI.* Free reading aid alongside the book. ~2 h. **74 — Reference.**
27. **SWE-bench** — https://www.swebench.com/ — *Benchmark, Agentic AI, advanced.* Purpose: model of rigorous deterministic pass/fail eval (2,294 real GitHub-issue tasks; patch must pass FAIL_TO_PASS without breaking PASS_TO_PASS). ~1 h. **68 — Reference.**
28. **Anthropic — "Code execution with MCP"** — https://www.anthropic.com/engineering/code-execution-with-mcp — *Engineering essay, Agentic AI, intermediate.* Study: token-efficient tool composition; sandboxing/resource-limit requirements for agent-generated code. ~2 h. **76 — Reference.**

*(Excluded on principle: "build an agent in 10 minutes" tutorials, prompt-collection listicles, star-ranked framework roundups, unmaintained agent-framework repos, and any resource that hides distributed-systems complexity behind a framework.)*

---

## Part 5 — Six-Week Platform Application Sprint (10 h/week)
Goal: application-ready for Platform roles; Project 1 MVP.

- **Week 1 — Distributed-correctness vocabulary + Project 1 scaffolding.** Resources: DDIA (replication/partitioning), Kafka Guide (reliability ch.). Task: robot/edge simulator emitting joint-state/telemetry/health for N robots; repo skeleton + architecture diagram. Deliverable: running simulator + README. Verify: multi-robot config, stable message IDs. *Job A. Unlocks:* "How do you model out-of-order sensor data?"
- **Week 2 — Event-time/watermarks + edge gateway.** Resources: Flink docs (time/watermarks), Confluent Flink 101. Task: Go edge gateway with gRPC streaming, batching, compression, retries, backpressure, clock-skew handling; local buffer + resume on disconnect. Deliverable: gateway + reconnect demo. Verify: zero silent loss across a forced disconnect. *Job A. Unlocks:* backpressure, store-and-forward.
- **Week 3 — Cloud ingestion + delivery semantics.** Resources: JetStream docs, Kafka EOS chapter. Task: implement one of Kafka/JetStream ingestion (schema versioning, DLQ, replay, idempotent processing); write a trade-off ADR for the other. Deliverable: ingestion service + ADR. Verify: duplicate rate ≈ 0 under forced redelivery. *Job A. Unlocks:* exactly-once claims/trade-offs.
- **Week 4 — Storage + platform APIs + security.** Resources: ClickHouse docs, OAuth/OIDC. Task: PostgreSQL metadata + ClickHouse telemetry + Redis rate limiting; REST+gRPC device registration/query/command; API keys/OIDC, RBAC, quotas, usage metering, idempotency. Deliverable: API layer + threat model. Verify: authz enforced; rate-limit + metering counters correct. *Job A. Unlocks:* explicit authn/authz + metering.
- **Week 5 — Infra + observability.** Resources: K8s/Helm/Terraform, OTel, SRE book. Task: Dockerize; Helm chart; Terraform/OpenTofu for local/modest cloud; autoscaling, health checks, rolling deploy; OTel traces + Prometheus/Grafana dashboards (queue lag, e2e latency, dropped/reconnect/late-event counts); define SLI/SLO. Deliverable: deploy guide + dashboards. Verify: HPA scales; dashboards populated. *Job A. Unlocks:* capacity planning, SLOs.
- **Week 6 — Reliability proof + CV/interview.** Resources: SRE (postmortems), stream-processing job. Task: Flink/Kafka-Streams fleet-health aggregation with watermarks/late handling; failure-injection scripts; benchmark report (robot counts, events/s, p50/p95/p99, recovery, duplicate rate, cost); incident postmortem. Deliverable: benchmark + postmortem + revised CV/LinkedIn. Verify: automatic recovery after broker/consumer kill; bounded memory. *Job A. Unlocks:* performance debugging, incident response.

**Project 1 MVP milestone (end W6):** simulator + edge gateway + one ingestion path + ClickHouse/Postgres storage + secured API with rate limiting/metering + K8s/Helm deploy + OTel dashboards + one benchmark + one postmortem. **This is application-ready evidence for Job A.**

---

## Part 6 — Sixteen-Week Agentic AI Transition Plan (10 h/week)
Runs after (or overlapping) the sprint. Goal: credible production AI-system evidence (Project 2).

- **Weeks 7–8 — LLM foundations + retrieval.** Resources: AI Engineering (Ch. 1–3, 6), Anthropic patterns. Task: hybrid lexical+semantic retrieval over runbooks/docs (reuse OpenSearch), metadata filtering, reranking, citations, access-control-aware retrieval. Deliverable: retrieval service + retrieval-eval baseline (recall@k, nDCG). Verify: citations resolve to sources. *Job B. Unlocks:* RAG design, retrieval evaluation.
- **Weeks 9–10 — Provider-independent LLM layer.** Resources: MCP spec/SDK, AI Engineering (inference). Task: model interface with routing/fallback, structured (typed) output, context/token/cost limits, error handling. Deliverable: LLM gateway module. Verify: fallback on induced provider error; cost cap enforced. *Job B. Unlocks:* provider-failure handling, cost control.
- **Weeks 11–12 — Agent design + durable execution.** Resources: LangGraph docs (persistence/interrupts/durable-execution), Temporal integration, Anthropic patterns. Task: explicit state machine (workflow graph) with tool registry + permissions; `interrupt()`/`Command(resume=)` HIL approval before risky actions; checkpointer persistence; retries/timeouts/cancellation; idempotency for tool execution. Deliverable: agent workflow + state-machine diagram + framework-choice ADR. Verify: resume after crash from checkpoint; approval gate blocks writes. *Job B. Unlocks:* durable execution, HIL, tool idempotency.
- **Weeks 13–14 — Tools + security.** Resources: OWASP LLM Top 10, MCP security. Task: read-only diagnostic tools (metrics/log/trace query, runbook retrieval, service-catalog, change-history), mocked ticket creation, no shell; tool authorization, tenant isolation, audit logging, prompt-injection tests, budget limits, read-only default. Deliverable: tool suite + threat model + prompt-injection test suite. Verify: injection tests fail closed; unauthorized tool blocked. *Job B. Unlocks:* prompt injection, excessive-agency mitigation.
- **Weeks 15–16 — Evaluation harness (the differentiator).** Resources: DeepEval, RAGAS, τ-bench, BFCL. Task: curated task dataset with golden/deterministic signals; tool-selection accuracy, retrieval recall/ranking, task-completion rate, unsupported-claim rate, citation correctness, latency, token usage, cost/task, retry rate, failure classification, regression suite, human-review rubric; written analysis of LLM-as-judge limitations. Deliverable: evaluation report + regression CI. Verify: eval reproducible; regression catches an injected fault. *Job B. Unlocks:* eval architecture, LLM-as-judge limits.
- **Weeks 17–18 — AI observability + production concerns.** Resources: OTel GenAI conventions. Task: OTel traces for agent/tool steps, model/retrieval latency, token/cost, tool errors, workflow retries, fallback, eval score, prompt/workflow version; containerize + K8s deploy, config/secrets, horizontal scaling, queue overload/backpressure, versioned workflows, rollback, SLOs. Deliverable: AI dashboards + deploy guide + cost report. Verify: end-to-end task completion visible; cost/task tracked. *Job B. Unlocks:* AI incident response, token/cost monitoring.
- **Weeks 19–22 — Hardening + narrative.** Task: incident scenarios, postmortem, benchmark report, limitations/trade-off discussion, design document, README polish; write CV bullets and the two-minute narrative. Deliverable: complete Project 2 repo + writeup. Verify: a fresh reader can run evals and read traces.

**Project 2 minimum credible milestone (end W16):** incident-investigation agent with a typed API/workflow service, durable state + HIL approval, hybrid retrieval with citations, ≥4 read-only authorized tools, an evaluation harness with a curated dataset and deterministic metrics, and AI observability (traces + token/cost). **A simple RAG demo is explicitly NOT sufficient.**

---

## Part 7 — Full 24-Week Hybrid Plan
Dependency order and decision points:
- **Weeks 1–6:** Platform sprint + Project 1 MVP. **Decision point (end W6):** if ingestion path + secured API + one benchmark + one postmortem are published → **start applying to Job A**.
- **Weeks 7–16:** Agentic AI transition + Project 2 to minimum credible milestone. **Decision point (end W16):** if eval harness + durable HIL agent + AI observability are done → **start applying to Job B / Applied AI**.
- **Weeks 17–24:** Harden both projects; optionally integrate (capstone). **Decision point (end W20):** capstone only if both projects are polished and ≥3 weeks remain; otherwise keep separate.
- **Time mix (24 wks):** ~60% implementation, ~25% books/papers/docs, ~15% interview/CV/writing. **Cost:** small open models + hosted APIs with hard budget caps → expect **< USD 150 total** (eval-run LLM calls dominate; cap per-run token budgets; use cheap/small models as judges). One paid book (AI Engineering); everything else free/official. No large GPU clusters required.

The plan is explicitly *not* "finish all 24 weeks before applying" — Job A applications begin at Week 6.

---

## Part 8 — Project Specifications

### Project 1 — Cloud-Edge Robot Telemetry Platform
**Architecture:** robot/edge simulator (joint states, position/motion, health, control acks, synthetic LiDAR metadata/point-cloud samples, audio/video metadata or low-rate frames; temporary disconnect + local buffer + resume without silent loss) → **Go edge gateway** (gRPC streaming/WebSockets, auth, batching, compression, retries, backpressure, preserved message IDs, clock-skew/out-of-order handling) → **cloud ingestion** (Kafka *or* JetStream implemented; the other analyzed in an ADR; schema versioning, DLQ, replay, idempotent processing) → **stream processing** (Flink/Kafka Streams; event time, watermarks, late data, fleet-health aggregations) → **storage** (PostgreSQL metadata/control, ClickHouse telemetry, Redis ephemeral/rate limiting, object storage for artifacts, optional vector store only if justified) → **platform APIs** (REST+gRPC; device registration, telemetry query, command dispatch; API keys/OIDC; RBAC/policy; rate limiting; quotas; usage metering; idempotency) → **infra** (Docker, K8s, Helm, Terraform/OpenTofu, autoscaling, health checks, rolling deploy, recovery) → **observability** (OTel, Prometheus, Grafana, traces, structured logs, queue-lag, e2e ingestion latency, dropped/reconnect/late-event counts, cost estimates) → **reliability** (at-least-once + idempotent processing, bounded memory, backpressure, graceful degradation, replay, DR procedure, SLI/SLO, incident sim, postmortem).
**Benchmarks:** multiple robot counts; events/s; p50/p95/p99 ingestion latency; recovery after broker/consumer failure; duplicate rate; CPU/mem/storage cost.
**Repo outputs:** source, architecture diagram, ADRs, threat model, load-test scripts, benchmark report, dashboards, example traces, failure-injection scripts, incident postmortem, README, deployment guide, limitations/future work.
**Acceptance:** zero silent loss; duplicate rate ≈ 0; automatic recovery after injected broker/consumer kill; dashboards show all required metrics; SLOs defined with an error-budget policy.
**Resource→component map:** simulator→(Kafka Guide, ClickHouse docs); gateway→(gRPC docs, Flink watermark concepts for clock skew); ingestion→(Kafka Guide EOS, JetStream docs); stream processing→(Flink docs, Confluent Flink 101); storage→(ClickHouse docs, DDIA); APIs/security→(OAuth/OIDC, DDIA multi-tenancy); infra→(K8s/Helm/Terraform docs); observability→(OTel docs, SRE book); reliability→(SRE book, DDIA "Trouble with Distributed Systems").

### Project 2 — Production-Grade Agentic Incident-Investigation Agent
**Direction:** an incident/operations agent that receives an incident question; retrieves runbooks/system docs; queries metrics/logs/traces via controlled read-only tools; forms and revises an investigation plan; correlates evidence; maintains workflow state; asks for human approval before risky actions; produces an evidence-backed incident report + draft postmortem; records every tool call and decision. This leverages Tung's real observability and distributed-systems strengths.
**Architecture:** Python typed API/workflow service (persistent state, durable execution, queue-backed processing where justified, retry/timeout, idempotency for tool execution, cancellation, HIL approval) → provider-independent LLM layer (routing/fallback, structured output, context/token/cost limits, error handling) → hybrid lexical+semantic retrieval (reuse OpenSearch; metadata filtering, reranking, citations, access-control-aware retrieval, retrieval evaluation) → agent design (explicit state machine + tool registry + permissions; short-term state; long-term memory only if justified; HIL controls; no multi-agent unless measurable value) → tools (metrics/log/trace query, runbook retrieval, service-catalog, change-history, mocked ticket creation; **no unrestricted shell**) → evaluation (curated dataset, golden/deterministic signals, tool-selection accuracy, retrieval recall/ranking, task-completion, unsupported-claim rate, citation correctness, latency, tokens, cost/task, retry rate, failure classification, regression, human rubric, LLM-as-judge limitations) → AI observability (OTel traces for agent/tool steps, model/retrieval latency, tokens, cost, tool errors, retries, fallback, eval score, prompt/workflow version, e2e completion) → security (prompt-injection tests, tool authz, tenant isolation, sensitive-data handling, output validation, audit logging, rate limiting, budget limits, read-only default) → production (containerization, K8s, config/secrets, horizontal scaling, queue overload/backpressure, dependency/provider-outage handling, partial-tool-failure, timeout recovery, versioned workflows, rollback, SLOs).
**Repo outputs:** source, architecture diagram, design doc, state-machine diagram, eval dataset, eval report, benchmark report, cost report, dashboards, example traces, threat model, prompt-injection test suite, incident scenarios, postmortem, README, limitations/trade-offs.

**Framework decision (compare ≥3):**
- **Custom state machine** — maximum debuggability/testability, zero vendor lock-in; but you build persistence, retries and observability yourself.
- **LangGraph (1.2.x; 1.0 GA late Oct 2025)** — application-layer durability via checkpointers + `interrupt()`/`Command(resume=)` for HIL; native for cyclical agent reasoning, streaming, memory. Protects against *application-level* failures (bad branches, HIL pauses) but not *infrastructure-level* crashes mid-node; some framework lock-in; note node re-execution on resume.
- **Temporal** — *infrastructure-level* durable execution (event-history replay), retries/timeouts; battle-tested (Netflix, Stripe, OpenAI Codex) but verbose and awkward for open-ended reasoning loops; best for macro orchestration.

**Recommendation:** use **LangGraph for agent reasoning + HIL**, and add a thin durable boundary (Temporal or a durable queue) **only if** the workflow exceeds ~30 s, makes ≥3 external calls, or must survive process crashes — the layered pattern documented across production write-ups. Justify in an ADR; do **not** default to "most popular," and do **not** use multi-agent unless it demonstrates measurable value (a single explicit workflow is preferred).
**Acceptance:** eval harness reproducible with deterministic metrics; HIL approval blocks write/risky actions; resume-after-crash from checkpoint; prompt-injection tests fail closed; token/cost per task visible in traces.

### Optional Capstone — Observable AI Operations for a Robot Fleet
An operations assistant for the Project 1 simulated fleet that investigates fleet incidents; queries telemetry + observability; retrieves runbooks; correlates metrics/logs/traces/recent deployments; explains likely causes; recommends actions; requires human approval before control operations; records all evidence and tool calls.
**Verdict:** high narrative value (unifies both tracks into one story) but real scope risk within 24 weeks. **Default: keep the two projects separate and polished.** Integrate only as a Weeks-20–24 stretch *if* Project 2's core is solid — and then **reuse** the Project 2 agent + Project 1 tools rather than rebuilding.

---

## Part 9 — Interview Preparation

**Mock schedule:** one system-design mock/week from Week 3 (Job A) and Week 11 (Job B); behavioral mocks at Weeks 5 and 15; project deep-dive mocks at Weeks 6 and 16. For each area below: state core concepts, likely questions, a strong-answer outline anchored in the candidate's real projects, the missing evidence to acknowledge honestly, a practice exercise drawn from Projects 1/2, and the mapped Part-4 resource.

**Job A — 12 system-design prompts:** (1) edge-to-cloud ingestion for 10k robots with intermittent connectivity; (2) guarantee no silent loss from a disconnecting robot; (3) out-of-order/late sensor events via event-time processing; (4) Kafka vs NATS JetStream — choose and justify; (5) exactly-once: what's real vs application responsibility; (6) partitioning for per-robot ordering at scale; (7) consumer recovery after crash without duplication; (8) gRPC streaming vs WebSockets for the gateway; (9) multi-region failover for the control plane; (10) autoscaling ingestion under bursty load; (11) storing video/LiDAR/joint-state — tiering + query design; (12) API security: authn/authz, rate limiting, quotas, usage metering for an external developer platform.

**Job B — 12 system-design prompts:** (1) architect an incident-investigation agent with retrieval + tools + HIL; (2) RAG with citations + access-control-aware retrieval; (3) retrieval evaluation metrics and how to measure them; (4) durable agent execution surviving a mid-investigation crash; (5) model-provider outage — routing/fallback; (6) evaluation architecture for completion/correctness/cost/safety; (7) LLM observability — spans/metrics you emit; (8) latency/cost optimization for a multi-step loop; (9) prompt-injection defense + excessive-agency mitigation; (10) multi-tenancy + budget limits for an AI platform; (11) hybrid vector+lexical retrieval + reranking trade-offs; (12) when NOT to use multi-agent vs a single explicit workflow.

**10 debugging scenarios:** consumer-lag spike; duplicate records after redelivery; watermark stalls so windows never fire; edge gateway OOM under backpressure; ClickHouse ingestion-latency regression; K8s crashloop after a Helm upgrade; rate limiter allowing bursts; agent tool-call loop that never terminates; RAG returns a confident but unsupported answer; token-cost spike from a routing regression.

**10 behavioral questions (mapped to real projects):** (1) biggest reliability win → JetStream zero-loss migration; (2) cost/performance trade-off → Loki→ClickHouse (~40% cost, ~75% latency); (3) data-correctness under pressure → Go Kafka migration (no loss/dup); (4) cross-team analytics need → CDC→ClickHouse OLAP separation; (5) performance optimization → OpenSearch reindex ~10x; (6) owning a platform long-term → multi-tenant SaaS (1,000+ tenants); (7) ordered workflows/failure handling → Azure Service Bus DLQ/retries; (8) improving a product metric → hybrid search ~35% accuracy; (9) architecture disagreement → the messaging-migration decision; (10) learning a new domain fast → the Project 1 robotics ramp.

**10 project deep-dive questions:** walk through Project 1 ingestion path; why at-least-once + idempotency; how you tested recovery; watermark tuning; API metering design; Project 2 framework-choice ADR; how the eval dataset was built; how you measure tool-selection accuracy; how HIL approval is enforced; what the AI dashboards show.

**10 production-incident/trade-off questions:** exactly-once vs at-least-once cost; when to shed load; SLO-breach response; multi-leader vs single-leader; ClickHouse vs Postgres for telemetry; LangGraph vs Temporal durability; LLM-as-judge vs deterministic evaluators; vector DB vs OpenSearch kNN; sync vs async checkpoint durability; build vs framework for agents.

---

## Part 10 — CV, LinkedIn, GitHub & Application Strategy

1. **Platform summary (Supported now):** "Senior software engineer with ~7 years building distributed, event-driven backends, streaming pipelines and observability platforms in Go and Python — including a 15+ TB/month observability platform and zero-message-loss messaging migrations — now focused on cloud-edge telemetry and developer-platform infrastructure."
2. **Agentic AI summary (Supported after Project 2):** "Distributed-systems and observability engineer building production-grade AI systems — retrieval, tool-using agents with durable execution and human-in-the-loop, plus evaluation and AI observability — grounded in reliability and cost discipline."
3. **Core skills for Job A (ordered):** Go; Kafka/NATS JetStream; stream processing/event time; Kubernetes/Helm/Terraform; gRPC; PostgreSQL/ClickHouse/Redis; OpenTelemetry/Prometheus/Grafana; reliability/SLOs; multi-tenant SaaS; API security/rate limiting.
4. **Core skills for Job B (ordered):** Python; distributed backend systems; RAG/hybrid retrieval; agent orchestration + durable execution; LLM evaluation; AI observability (OTel GenAI); reliability for nondeterministic systems; vector search; cost/latency optimization; multi-tenancy.
5. **Truthful CV bullet improvements:** quantify every bullet (records/month, TB, %, tenants, searches/day); lead with the outcome then the mechanism, e.g. "Cut observability query latency ~75% and storage cost ~40% at 15+ TB/month by migrating log storage Loki→ClickHouse with hybrid trace storage."
6. **Achievements to move higher:** observability platform migration; JetStream zero-loss; Go Kafka migration — the strongest Job A signals.
7. **Terms to add only when supported:** "RAG," "agent," "LLM evaluation," "AI observability," "vector database (production)" — after Project 2; "Helm," "Terraform," "Flink" — after Project 1.
8. **Terms NOT to add yet:** "Agentic AI expert," "multi-agent systems," "LLM fine-tuning," "distributed model training," "robotics engineer," "RAG in production" — until the corresponding project ships.
9. **GitHub naming/presentation:** `edge-fleet-telemetry-platform` and `incident-investigation-agent`; each repo gets a crisp README with architecture diagram, "what/why," benchmarks, dashboard screenshots, ADRs, and limitations. Pin both. Avoid star-count claims.
10. **LinkedIn headline (now):** "Senior Software Engineer — Distributed Systems, Streaming & Observability (Go/Python) | building cloud-edge platforms."
11. **LinkedIn About (now):** three short paragraphs — (a) reliability/streaming track record with numbers; (b) current focus on cloud-edge platform + production AI infrastructure; (c) explicit "expanding into" framing, no overclaiming.
12. **30-second intro:** "I'm a senior backend engineer with about seven years in distributed systems, streaming and observability. I've run a 15-terabyte-a-month observability platform, migrated messaging to zero message loss, and moved millions of records without duplication. I'm now building cloud-edge telemetry infrastructure and production AI systems."
13. **Two-minute project narrative:** problem → architecture → delivery-semantics decision → reliability proof (failure injection + recovery) → benchmark numbers → next steps (Project 1); or retrieval → tools → durable HIL agent → evaluation harness → observability → limitations (Project 2).
14. **Transition explanation:** "My core is reliability and data infrastructure. Production AI systems fail on the same axes I already own — retrieval quality, evaluation, observability, cost and correctness under nondeterminism — so I'm extending my strengths into agentic systems rather than starting over."

**Labeled example CV bullets:**
- "Designed a cloud-edge telemetry platform ingesting simulated fleet data with at-least-once delivery, idempotent processing and OTel-based SLOs" — **Supported after Project 1.**
- "Built an incident-investigation agent with durable human-in-the-loop execution and an evaluation harness measuring task completion, tool-selection accuracy and cost per task" — **Supported after Project 2.**
- "Ran a 15+ TB/month observability platform, cutting query latency ~75% and storage cost ~40%" — **Supported now.**
- "Led a multi-agent RAG platform in production" — **Not currently supportable.**

### Application strategy (answers to the required questions)
- **Apply to Job A immediately?** Yes — begin applying at Week 6 with the Project 1 MVP as the interview artifact. The CV already clears the bar; the sprint closes interview gaps.
- **Gaps to close before a Job A interview:** Flink/event-time fluency; Helm/Terraform/Docker artifacts; explicit authn/authz + rate limiting/metering. **Learnable on the job:** robotics/sensor-data specifics, ROS 2/DDS, model registries/inference, HIL simulation — say so honestly.
- **Explaining the lack of robotics experience:** "I haven't shipped robots, but I've built high-rate, lossless telemetry pipelines and 15 TB/month observability systems; robot fleets are out-of-order, intermittently-connected, high-cardinality streams — the exact problems I solve. My Project 1 simulates a fleet end-to-end to prove it."
- **Translating pipeline work into robotics-telemetry language (no exaggeration):** "50M+ records/month CDC" → "high-rate event ingestion with OLTP/OLAP separation"; "Kafka consumers, no loss/dup" → "at-least-once delivery with idempotent processing and offset recovery"; "15 TB/month logs" → "high-volume time-series telemetry storage and query at scale."
- **Apply to Job B now or after Project 2?** After Project 2's minimum credible milestone (Week 16). **Minimum credible evidence:** durable HIL agent + tool authorization + a real evaluation harness (task completion, tool-selection accuracy, cost/task) + AI observability. A RAG demo alone is not evidence.
- **Positioning semantic search as adjacent to RAG (honestly):** "I built hybrid keyword+vector retrieval improving match accuracy ~35% over 50k daily searches. That's the retrieval half of RAG; in Project 2 I added grounded generation with citations plus retrieval evaluation."
- **Premature claims to avoid:** "experienced agentic AI engineer," "multi-agent," "fine-tuning," "RAG in production" — before Project 2.
- **What distinguishes this candidate from shallow-LLM-demo applicants:** production reliability, evaluation rigor, observability/cost discipline, and durable-execution/idempotency instincts — exactly what the market says is the real signal ("eval literacy" and production observability), and exactly what most demo-only candidates lack.
- **Target-company search strategy:** robotics/drone/AV platform teams (e.g., Foxglove-style tooling, fleet-data platforms), streaming/data-platform teams, observability vendors, and AI-infra teams at companies that already run agents in production. Use remote-friendly boards and company career pages given HCMC location and time-zone overlap constraints. **Adjacent titles to target:** Platform Engineer, Data Platform Engineer, Streaming Platform Engineer, Infrastructure Software Engineer, Distributed Systems Engineer (near-term); AI Infrastructure Engineer, ML/AI Platform Engineer, Applied AI Engineer, AI Observability Engineer (after Project 2).
- **Networking topics:** event-time correctness, exactly-once trade-offs, observability cost control, durable agent execution, eval design. **Questions to ask hiring managers:** "What's your delivery-semantics model and how do you handle late/out-of-order sensor data?"; "How do you evaluate and observe your agents in production?"; "What does on-call/SLO ownership look like for this platform?"
- **Referral message template:** "Hi [name] — I'm a senior distributed-systems/observability engineer (Go/Python) who's run 15 TB/month observability and zero-loss streaming migrations. I've built a cloud-edge fleet-telemetry platform [link] that maps directly to [team]'s work. Would you be open to a quick chat or a referral for [role]?"
- **Recruiter-response template:** "Thanks for reaching out. My core is distributed systems, streaming and observability in Go/Python — recent work includes a 15 TB/month observability platform and lossless messaging migrations. I'm most interested in platform/streaming/AI-infra roles. Here's my CV and two portfolio repos with benchmarks and dashboards: [links]."
- **Technical portfolio introduction:** "Two repos: a cloud-edge fleet-telemetry platform (streaming, delivery semantics, K8s/Helm, OTel SLOs, benchmarks + postmortem), and an incident-investigation agent (durable human-in-the-loop execution, hybrid retrieval with citations, an evaluation harness, and AI observability). Both emphasize production reliability and measured results, not demos."

---

## Part 11 — Final Prioritized Actions
1. **Next seven days (5):** (a) create both GitHub repos with README skeletons + architecture-diagram stubs; (b) start DDIA replication/partition chapters and set up MIT 6.5840 Lab 1; (c) scaffold the Project 1 robot simulator in Go; (d) rewrite CV bullets outcome-first with numbers; (e) update LinkedIn headline/About to the "expanding into" framing.
2. **Top five resources to start now:** DDIA 2e; MIT 6.5840; Flink docs (time/watermarks); AI Engineering (Huyen); Anthropic "Building Effective Agents."
3. **First GitHub deliverable:** `edge-fleet-telemetry-platform` with a running multi-robot simulator + README + architecture diagram (end of Week 1).
4. **Earliest reasonable apply dates:** **Job A — end of Week 6** (Project 1 MVP + benchmark + postmortem). **Job B / Applied AI — end of Week 16** (Project 2 minimum credible milestone: durable HIL agent + eval harness + AI observability).
5. **Ten highest-priority skills:** event-time/stream processing (Flink); exactly-once/idempotency depth; Helm/Terraform/Docker artifacts; explicit authn/authz + rate limiting/metering; RAG-with-generation; agent state machines + durable HIL execution; LLM evaluation-harness design; AI observability (OTel GenAI) + token/cost; provider routing/fallback; prompt-injection/tool-authorization security.
6. **Three activities to explicitly defer:** knowledge graphs; multi-agent systems; LLM fine-tuning / distributed model training.
7. **Clearest professional positioning statement:** *"A distributed-systems and observability engineer expanding into production AI infrastructure and agentic systems — bringing reliability, evaluation and cost discipline to systems that must work under real-world failure and nondeterminism."*

---

## Caveats
- **Fit scores are informed judgment, not measurement.** They weight demonstrated production evidence over keyword overlap, per the task's scoring rule.
- **Hiring-demand signals are directional, not statistical.** Job-market sources (Built In, Glassdoor, KORE1, and LangChain's "State of Agent Engineering," n=1,340, surveyed Nov 18–Dec 2, 2025) indicate patterns — e.g., ~89% of surveyed teams have agent observability vs 52% running evals, and 57.3% run agents in production — but this is not a rigorous frequency sample of the two target roles; treat as context.
- **Fast-moving tooling:** LangGraph reached 1.0 GA in late October 2025 and is at 1.2.9 by mid-2026; OTel GenAI semantic conventions are still largely experimental; MCP and agent benchmarks (τ-bench/τ²-bench, BFCL V4) evolve quickly — **verify versions/links at apply time.**
- **Some comparison framings** (LangGraph = application-level vs Temporal = infrastructure-level durability) originate in analyst/vendor blogs but are corroborated by LangGraph's own durable-execution docs (which concede `exit` mode "cannot recover from system failures... that occur mid-execution").
- **Cost estimates** assume strict API budget caps, small open models where possible, and cheap models used as LLM judges; real spend scales with eval-run frequency.
- **No experience was invented:** every "Supported now" claim traces to a stated CV achievement; all AI-agent, robotics, RAG-in-production, Helm/Terraform/Flink claims are labeled as supportable only after the specified project ships.
