# Evidence-based Platform and Agentic AI career plan

**Candidate:** Pham Duy Tung  
**Research date:** 16 July 2026  
**Planning horizon:** 24 weeks, 10 hours/week, ending 31 December 2026  
**Target A:** Platform Engineer, robotics developer platform  
**Target B:** NVIDIA Senior Software Engineer, Agentic AI Systems, Vietnam  

## How to read this report

This report uses three kinds of statement:

- **Fact:** directly supported by the supplied candidate profile or a cited primary source.
- **Assessment:** my hiring or engineering judgment. Scores and dates are estimates, not promises.
- **Target:** an acceptance threshold to test in a portfolio project. It must never be presented as an achieved result until a dated benchmark proves it.

The two primary listings were live when researched: Menlo's [Platform Engineer](https://jobs.ashbyhq.com/menlo/98255ff5-5a96-4d17-9bd2-6438efaf7adf) role and NVIDIA's [Senior Software Engineer, Agentic AI Systems](https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/Senior-Software-Engineer--Agentic-AI-Systems_JR2020868) role in Ho Chi Minh City/Hanoi. Job availability can change without notice. The broader hiring sample is purposive rather than statistically representative.

---

# Part 1 — Executive assessment

## Decision summary

| Decision | Recommendation |
|---|---|
| Coherent narrative | **A distributed-systems and observability engineer who has operated high-volume streaming, search, and multi-tenant platforms and is now building verifiable cloud-edge and production AI systems.** |
| Job A current fit | **73/100, medium-high confidence, plausible range 68–78.** Apply now while closing narrow gaps. |
| Job B current fit | **54/100, high confidence, plausible range 49–59.** The engineering substrate is strong; direct LLM/agent/evaluation evidence is absent. |
| Primary track now | Platform, robotics data infrastructure, streaming platform, observability platform, or AI infrastructure roles that value distributed-systems depth. |
| Secondary track | Production Agentic AI systems, built deliberately through one evaluated, durable, secure project. |
| Exact NVIDIA vacancy | Submit a truthful stretch application by **19 July 2026** because it is local and newly active; do not wait months for this particular requisition. Treat it as a low-probability application, not evidence that the general Job B gap has closed. |
| Repeatable Job B readiness | Begin broad Senior Agentic AI applications after Project 2 passes its minimum credible gates: **5 November 2026** on a dedicated 16-week sequence; **19 November 2026** is the earliest hybrid gate, while **17 December 2026** is the safer fully hardened date. |
| 24-week result | Two separate, polished repositories plus an optional thin, read-only integration—not one sprawling capstone. |

## Overall candidate narrative

The strongest story is not “backend engineer starting over in robotics or AI.” It is “production distributed-systems engineer moving one layer closer to robotics data and intelligent workflows.”

The supplied evidence already supports senior-level claims in streaming reliability, idempotency, storage/search architecture, observability economics, high-volume migration, and multi-tenancy. It does **not** support claims of robotics engineering, edge-fleet operations, RAG, agent design, LLM evaluation, model serving, or AI safety. The roadmap preserves that boundary.

The unusual advantage is production depth. Many portfolio candidates can call an LLM or deploy a broker; fewer can discuss why an acknowledged event may still be duplicated, how a retry can repeat an external side effect, how to bound a reconnect storm, how to separate event time from processing time, or how to make traces useful during a partial outage. Those are the themes to emphasize.

## Fit scoring method

Scores weight demonstrated production evidence, not keyword overlap. Learning and portfolio work can add evidence, but course completion adds no points by itself.

### Job A weighted score

| Evidence domain | Weight | Current score | Basis |
|---|---:|---:|---|
| Backend/platform/distributed systems | 30 | 27 | Seven years; Go/Python; gRPC; multi-tenant SaaS; concurrency, idempotency, outbox, ordered workflows |
| Streaming and data infrastructure | 20 | 18 | Kafka/NATS/JetStream, CDC, ClickHouse, queues, high-volume migrations; Flink/event-time evidence missing |
| Kubernetes and reproducible delivery | 15 | 8 | Kubernetes is explicit; Docker, Helm, IaC, GitOps, and autoscaling implementation are not |
| Reliability and observability | 15 | 14 | Direct production OTel/Prometheus/Jaeger/Loki/ClickHouse evidence with quantified scale and outcomes |
| Robotics, edge, and physical sensor data | 12 | 2 | Transferable streaming concepts but no direct robot, edge-fleet, ROS, timing, or sensor-format evidence |
| ML-platform and secure developer-platform features | 8 | 4 | APIs, search, multi-tenancy transfer; model registry/rollout, metering, and explicit authz evidence missing |
| **Total** | **100** | **73** | |

**Assessment:** the largest uncertainty is not whether the candidate understands reliable data movement; it is whether an interviewer treats real robotics/edge experience as mandatory. A robotics-first team could score this 5–10 points lower. A developer-platform team could score it slightly higher.

### Job B weighted score

| Evidence domain | Weight | Current score | Basis |
|---|---:|---:|---|
| Production software and distributed systems | 25 | 23 | Direct, high-volume, long-running systems evidence |
| Retrieval and data systems | 15 | 11 | Hybrid keyword/semantic search and ranking are strong adjacency; generated-answer RAG is unproven |
| LLM, RAG, tools, memory, and agent orchestration | 25 | 2 | Python is present; no direct project or production evidence in the supplied profile |
| Evaluation, safety, and AI-specific reliability | 15 | 2 | General reliability transfers; no AI task dataset, graders, injection testing, or regression evidence |
| Observability, performance, and operations | 10 | 9 | Strongest transferable differentiator |
| Ownership and technical leadership | 10 | 7 | Architecture/optimization/operations are demonstrated; cross-functional AI leadership is not |
| **Total** | **100** | **54** | |

**Assessment:** the NVIDIA description explicitly values systems engineering as much as AI familiarity, which prevents the score from being lower. Its explicit requirement for experience with LLMs, RAG, agent frameworks, or workflow orchestration remains a material application gap. A credible Project 2 can raise the evidence-based score to roughly 70–75; it cannot manufacture production tenure.

## Strongest matching signals

### Job A

1. Kafka and Go consumers that migrated millions of records without loss or duplication.
2. NATS Core to JetStream reliability migration with persistent storage and acknowledgements.
3. More than 15 TB/month observability platform, with approximately 75% lower query latency and 40% lower storage cost.
4. CDC-to-ClickHouse pipeline handling more than 50 million records/month.
5. Kubernetes, gRPC, Prometheus, OpenTelemetry, PostgreSQL, Redis, ClickHouse, performance engineering, and multi-tenancy.

### Job B

1. Seven years building and operating production software rather than notebook prototypes.
2. Distributed-system correctness: idempotency, outbox, locking, retries, manual offsets, DLQ, and ordered processing.
3. Hybrid keyword/semantic OpenSearch work across more than 50,000 searches/day with a measured relevance outcome.
4. Observability and performance work at unusually strong scale.
5. Multi-tenant and high-volume platform ownership—the operational substrate agent systems need.

## Largest gaps and their classification

| Gap | Job | Classification now | Why | Closure |
|---|---|---|---|---|
| Robot/edge fleet, intermittent connectivity, physical sensor/time semantics | A | Likely interview blocker; sometimes application blocker | Central domain of the role | Project 1 simulator, durable edge spool, clock-skew/outage tests, MCAP/ROS concepts; be explicit that it is simulated |
| Docker, Helm, IaC, deployment/autoscaling evidence | A | Likely interview blocker | Kubernetes alone is not proof of delivery ownership | Docker Compose/k3d, Helm chart, OpenTofu module, HPA and failure drill |
| Flink/event time/watermarks/late data | A | Likely interview blocker | Role names stream processing; candidate evidence is broker-centric | Implement one event-time job with deterministic late-data fixtures |
| Authn/authz, rate limits, quotas, metering | A and B | Likely interview blocker | Current sample makes secure multi-tenancy a recurring design concern | Tenant-scoped JWT/OIDC, RBAC, Redis token bucket, durable usage events, threat model |
| Model registry/rollout/ML metadata | A | Helpful differentiator; learnable on job | Platform support responsibility, not the core current match | MLflow alias-based rollout and deterministic canary router; no GPU needed |
| Production-style LLM/RAG/agent system | B | Application blocker for normal Job B pipeline | Explicit requirement with no supplied evidence | Project 2 working service, not a course certificate |
| Durable tool workflow and idempotent effects | B | Interview blocker | Agents are failure-prone distributed workflows | Temporal workflow, typed state, activities, retries, cancellation, approval, idempotency ledger |
| Evaluation and regression evidence | B | Application and interview blocker | Reliability cannot be asserted from screenshots | Curated tasks, repeated trials, deterministic graders, retrieval metrics, calibrated model graders |
| Prompt injection, tool authorization, tenant isolation | B | Interview blocker | Tool use creates security boundaries | Read-only tools, policy checks outside prompts, adversarial test suite, audit trail |
| AI traces, token/cost budgets, provider routing/failure | B | Interview blocker | General OTel is adjacent, not AI observability | GenAI spans, per-run budget, model adapter/fallback and outage tests |

### Learn on the job or defer

- **Reasonable to learn on the job for Job A:** a particular robot vendor SDK, deep ROS package development, real LiDAR calibration, distributed training internals, a specific cloud, and hardware-in-the-loop vendor tooling—unless a listing marks them required.
- **Helpful but not immediate for Job B:** knowledge graphs, self-hosted large-model serving, semantic caching, and multi-agent coordination.
- **Explicitly unnecessary for this plan:** Rust/C++/CUDA, foundation-model training, a GPU cluster, and autonomous robot control. Reconsider only when a chosen vacancy requires them.

## Apply-now recommendation

**Job A:** apply now. Use the existing production achievements and say plainly: “My direct experience is high-volume cloud data and reliability; my robotics evidence is currently a simulated cloud-edge platform.” Do not wait for six weeks before entering hiring cycles. The six-week sprint is to improve interview conversion, not to grant permission to apply.

**Job B:** use two lanes.

1. For the exact live NVIDIA Vietnam role, send one well-tailored, transparent stretch application now because the vacancy is local, current, and explicitly values production-system fundamentals. Lead with distributed systems, semantic retrieval, observability, and operational ownership; acknowledge that direct Agentic AI experience is being built.
2. For the repeatable job search, do not brand yourself “Senior Agentic AI Engineer” until the minimum credible Project 2 milestone exists. Apply earlier to bridge roles such as AI Platform Engineer, AI Reliability Engineer, GenAI Platform Engineer, ML Platform Engineer, or AI Observability Engineer.

## Primary and secondary track

The **primary track** is Platform/AI Infrastructure: it has the best evidence-to-market ratio and can generate interviews immediately. The **secondary track** is Agentic AI Systems: it has high upside, but its credibility should be earned through durable execution, evaluation, security, and observability—not through framework breadth.

---

# Part 2 — Requirement matrices

## Job A — robotics developer-platform Platform Engineer

| Requirement | Importance | CV evidence | Evidence strength | Gap | Action |
|---|---|---|---|---|---|
| 4+ years platform/backend/data engineering | Critical | Approximately seven years as a Senior Software Engineer across backend, distributed, streaming, search, and platform work | Direct and strong | None | Lead summary with production ownership and scale |
| Go or Python | Critical | Go and Python are primary professional languages | Direct and strong | None | Build Project 1 gateway in Go |
| Concurrency and systems performance | Critical | Concurrent Kafka consumers, batch/worker pipelines, 10x reindexing, 5M records under three minutes | Direct and strong | Formal capacity/tail-latency explanation can deepen | Publish load model and p50/p95/p99 benchmark |
| Distributed failure and delivery semantics | Critical | Manual offsets, idempotency keys, outbox, locking, acknowledgements, DLQs/retries, ordered workflows | Direct and strong | Need cloud-edge failure application | Test disconnect/restart/replay and document invariants |
| Kafka or comparable broker | Critical | Kafka, NATS and JetStream in production | Direct and strong | None at broker level | Implement Kafka; compare JetStream in an ADR |
| Flink/event-time stream processing | High | No Flink or explicit event-time/watermark evidence | Missing | Likely interview blocker | Flink SQL/PyFlink aggregation with late side output |
| Cloud-edge synchronization | Critical | Streaming/retry patterns transfer, but no edge-fleet evidence | Adjacent and transferable | Intermittent links, local durability, resumption | Durable SQLite-WAL edge spool and explicit ACK/resume |
| Physical sensor/robotics data | High | No direct robot, LiDAR, audio, video, or joint-state work | Portfolio evidence needed | Domain semantics and honest vocabulary | Simulate typed sensor envelopes; use MCAP; study ROS 2 QoS/time |
| Real-time telemetry/control data | Critical | High-volume streaming and ordered workflows are adjacent | Adjacent and transferable | Command safety and edge timing unproven | Separate telemetry and command channels; deduplicate commands |
| gRPC streaming, REST, WebSockets | High | gRPC and Socket.io are explicit; backend APIs are a strength | Direct but limited | Streaming flow control not explicitly demonstrated | Bidirectional gRPC ingest plus REST control/query API |
| Schema evolution | High | CDC/messaging implies schemas but no explicit evidence | Unknown | Compatibility policy | Protobuf compatibility tests and versioned envelope ADR |
| PostgreSQL and Redis | High | Both explicitly demonstrated | Direct and strong | None | Use metadata/control and ephemeral rate-limit state |
| ClickHouse/high-volume analytics | High | 50M records/month CDC; 15 TB/month logs; performance/cost improvements | Direct and strong | Telemetry schema specifics | Event/ingest timestamps, partition and retention design |
| Object storage/large sensor artifacts | Medium | Not supplied | Missing | Chunking, retention, integrity | MinIO/S3-compatible storage and MCAP references |
| Vector storage | Low–medium | OpenSearch hybrid semantic search | Adjacent and transferable | No valid Project 1 need yet | Do not add a vector DB without a retrieval use case |
| Kubernetes | Critical | Explicit production technology | Direct but limited | Depth and specific operational evidence unknown | k3d deployment, probes, resource limits, PDB, HPA |
| Docker | High | Not explicitly demonstrated | Unknown | CV cannot claim it | Containerize every service; add reproducible local deployment |
| Helm | High | Not explicitly demonstrated | Missing | Likely interview blocker | Tested chart with values/schema, hooks avoided unless justified |
| Terraform/OpenTofu | High | Not explicitly demonstrated | Missing | Likely interview blocker | Small OpenTofu module; local first, optional low-cost cloud |
| Autoscaling/failover/DR | High | Reliability work transfers; these mechanisms are not explicit | Adjacent and transferable | Concrete runbooks and tests | HPA, broker/consumer restart, backup/replay and DR procedure |
| Monitoring/alerting/incidents | Critical | Prometheus, OTel, Jaeger, Loki, ClickHouse observability redesign | Direct and strong | Grafana and SLO practice not explicit | RED/USE dashboards, burn alert, injected incident and postmortem |
| API authentication | High | No explicit implementation evidence | Unknown | Token lifecycle and service identity | OIDC/JWT validation; never build an identity provider |
| Authorization/access control | Critical | Tenant isolation and feature tiers transfer | Adjacent and transferable | Explicit permission model | Tenant-scoped RBAC enforced in API and storage queries |
| Rate limiting, quotas, metering | High | Feature-tier management is adjacent | Adjacent and transferable | Algorithms and durable billing events | Redis token bucket, quota policy, immutable usage event |
| Developer-platform/API product | High | Backend APIs and 1,000+ tenant onboarding/tiers | Direct but limited | External developer UX/SDK evidence | API contract, Go client example, error catalog, onboarding walkthrough |
| Model registry/versioning/rollout | Medium–high | No direct evidence | Missing | ML-platform support gap | MLflow aliases plus deterministic 10% canary router |
| Inference pipelines | Medium | No direct evidence | Missing | Not core to six-week milestone | Mock model artifact and rollout metadata; do not imply model serving |
| Training data/lineage | Medium | CDC/data pipelines transfer | Adjacent and transferable | Dataset lineage/quality | Versioned manifest linking MCAP objects, schema and source robot |
| Hardware-in-the-loop/simulation | Medium | No direct evidence | Missing | Real hardware inaccessible | Simulator and deterministic fault scenarios; label “simulation,” not HIL |
| Distributed training/GPU infrastructure | Low for initial candidacy | No evidence | Missing | Differentiator only | Defer unless a specific job makes it mandatory |

### Job A gap disposition

- **Application blocker only at some robotics-first employers:** real robot/edge operation.
- **Likely interview blockers:** intermittent-link design, event time, Helm/IaC delivery, secure API/quotas, and honest exactly-once reasoning.
- **Helpful differentiators:** ROS 2/MCAP fluency, model rollout metadata, a reproducible fault benchmark, and a strong incident postmortem.
- **Learnable after joining:** vendor hardware, deep perception formats, large simulation farms, distributed training, and a company-specific MLOps stack.
- **Unnecessary now:** autonomous navigation/control algorithms, CUDA, and building a vector service into telemetry without a use case.

## Job B — Senior Software Engineer, Agentic AI Systems

| Requirement | Importance | CV evidence | Evidence strength | Gap | Action |
|---|---|---|---|---|---|
| 5+ years software engineering | Critical | Approximately seven years; current Senior Software Engineer | Direct and strong | None | Lead with operated systems, not years alone |
| Strong Python and modern practices | Critical | Python is a primary language | Direct but limited | Depth of recent Python production evidence is unspecified | Project 2 typed Python, tests, linting, packaging and async service |
| Scalable distributed/cloud-native systems | Critical | Kafka/NATS, queues, CDC, Kubernetes, serverless, multi-tenant SaaS | Direct and strong | None | Map failure semantics to AI workflows |
| Large-scale production ownership | Critical | Multiple quantified systems and migrations | Direct and strong | Scope of team leadership unknown | Use precise “designed/built/operated” verbs; do not claim org leadership |
| Reliability, observability, performance | Critical | 15 TB/month observability and large latency/cost reductions | Direct and strong | AI-specific signals absent | Instrument model, retrieval, tool and workflow spans |
| LLM applications | Critical | No supplied evidence | Missing | Application blocker | Provider-neutral model adapter and tested production-style service |
| RAG/generated-answer retrieval | High | Hybrid keyword/semantic OpenSearch and relevance improvement | Adjacent and transferable | Chunking, grounding, citations and generation unproven | Build access-aware hybrid retrieval and citation validation |
| Agent state/planning/workflows | Critical | Ordered event workflows transfer conceptually | Adjacent and transferable | No agent workflow evidence | Explicit state machine; planning only where eval shows benefit |
| Durable execution | High | Queue/retry/idempotency patterns transfer | Adjacent and transferable | Workflow replay/versioning/cancellation | Temporal workflow, activities, signals, retries and cancellation |
| Tool calling and permissions | Critical | Backend APIs exist; no model-controlled tools | Portfolio evidence needed | Typed tools, authorization, side-effect safety | Read-only diagnostic registry; schema and policy checks outside prompts |
| Memory architectures | Medium | Redis/databases transfer | Adjacent and transferable | No justified agent memory | Persist workflow evidence; add long-term memory only with measured value |
| Multi-agent orchestration | Low–medium | No evidence | Missing | Not needed for initial proof | Defer; compare against one explicit workflow before adding |
| Model routing/fallback | High | General dependency fallback is adjacent | Portfolio evidence needed | Provider variance, budgets, context limits | Two adapters plus deterministic fake; bounded fallback policy |
| Vector databases/retrieval | High | OpenSearch hybrid search | Direct but limited | Production generated-answer integration absent | Reuse OpenSearch; evaluate Recall@k and ranking |
| Knowledge graphs | Low–medium | No evidence | Missing | Stand-out item, not core | Defer unless incident relations measurably need it |
| AI evaluation/benchmarking | Critical | No supplied evidence | Missing | Application and interview blocker | Curated task set, graders, repeated trials and regression gate |
| Task completion/correctness/safety metrics | Critical | General QA/reliability is not equivalent | Portfolio evidence needed | Outcome definitions and uncertainty | Deterministic outcome signals plus calibrated human/model review |
| LLM-as-judge limitations | High | No evidence | Missing | Bias/variance understanding | Blind order, rubric, calibration sample and human disagreement analysis |
| AI observability | Critical | OTel/trace platform is highly transferable | Adjacent and transferable | Tokens/cost/model/tool/eval semantics | OTel GenAI spans plus local MLflow trace/eval view |
| Prompt injection and guardrails | Critical | Multi-tenant isolation transfers; no LLM threat evidence | Portfolio evidence needed | Instructions can cross trust boundaries | OWASP-derived indirect-injection and tool-exfiltration suite |
| Multi-tenancy and access-aware retrieval | High | 1,000+ tenant SaaS and isolation | Direct and strong | Agent/tool/retrieval path enforcement | Tenant in signed identity, policy, query filter and audit event |
| Latency and cost management | High | Strong performance/cost record | Adjacent and transferable | Token/model-specific economics | Per-step latency/tokens/cost and end-to-end budget |
| Production deployment/overload | High | Kubernetes, queues, backpressure experience | Direct but limited | AI provider/queue overload scenarios | Container, K8s, admission limit, queue bound and load shedding |
| Human-in-the-loop | High | No supplied evidence | Missing | Approval and resumption semantics | Temporal signal/update; immutable approval record |
| Technical leadership | High | Major redesigns imply ownership; formal scope unknown | Direct but limited | AI architecture leadership absent | Publish ADRs, trade-offs, review rubric; state actual role precisely |
| Prototype-to-production modernization | High | Migrations and optimization demonstrate the pattern | Adjacent and transferable | No AI prototype example | Compare baseline to hardened system with measured regression report |
| Reduce operational complexity | High | Storage redesign and migrations show simplification/performance | Direct and strong | None, but explain mechanisms | Quantify components, failure modes and operator workflow before/after |

### Job B gap disposition

- **Application blockers for normal Senior Agentic AI roles:** no direct LLM/RAG/agent project and no AI evaluation evidence.
- **Likely interview blockers:** durable tool execution, outcome-based evals, retrieval evaluation, prompt-independent authorization, provider failure, model/token/cost observability, and nondeterministic incident response.
- **Helpful differentiators:** high-volume AI trace/evaluation storage, self-hosted small-model comparison, and a public benchmark with confidence intervals.
- **Learnable after joining:** a specific agent framework, provider API, knowledge-graph product, and company model gateway.
- **Unnecessary now:** multi-agent choreography, fine-tuning, reinforcement learning, foundation-model training, or GPU optimization.

## Current hiring validation: 21 first-party roles

**Fact, access date 16 July 2026.** This purposive sample tests whether the roadmap generalizes beyond the two targets. Every link is a company career page or company-controlled ATS page. Fourteen listings exposed a first-posted date within the 180-day window beginning 17 January 2026; Scale AI and Forter were older requisitions with official updates inside the window; five live pages exposed no publication date. An ATS update does not necessarily mean a newly opened role.

### Platform, robotics, edge, and data infrastructure

| Company and role | Location/date visible at research | Requirements that validate the plan |
|---|---|---|
| OpenAI — [Software Engineer, Distributed Data Systems – Robotics](https://openai.com/careers/software-engineer-distributed-data-systems-robotics-san-francisco/) | San Francisco; live, date not exposed | Distributed compute/orchestration/storage/streaming and ML infrastructure; reliability/security; multimodal training/evaluation data |
| Field AI — [Data Platform Engineer, Infrastructure](https://jobs.lever.co/field-ai/f41fb1ac-d266-4e2c-8879-2d88d6f890d4) | Irvine; posted 11 Jul 2026 | Kubernetes, Terraform, Python/Go, production operations, object/streaming data, IAM/network security; sensor/edge fleet preferred |
| Tutor Intelligence — [Robotics Infrastructure Engineer](https://jobs.lever.co/tutorintelligence/fdb1c47e-4685-4ac7-b57f-f1ba1077c3ec) | Watertown; posted 10 Apr 2026 | Systems Python, Linux/containers/networking, real sensors, CI/CD, simulation/telemetry, gRPC/Protobuf |
| Skip — [Backend Engineer](https://jobs.ashbyhq.com/skip/3235ed07-aa22-4309-a949-ca2504e95e8d/) | San Francisco; posted 31 Mar 2026 | Cloud/edge backend, telemetry, OTA/fleet management, Kubernetes/Terraform, reliability/latency/security |
| Dash0 — [Platform Engineer, Sydney](https://jobs.ashbyhq.com/dash0/c71c1a08-d9ea-4229-b7c9-a3ac9eabc95c/) | Sydney area; live, date not exposed | Production Go, Terraform, Docker/Kubernetes, CI/CD/cloud, security, observability/OTel and operational ownership |
| Anduril — [Platform/DevOps/Infrastructure/SRE](https://job-boards.greenhouse.io/andurilindustries/jobs/5176775007) | Sydney; published 30 Jun, updated 15 Jul 2026 | Terraform, Go/Python automation, Kubernetes/Docker/Linux/networking, cloud plus on-prem/air-gapped operations |
| WHOOP — [Senior Platform Engineer, Kubernetes/Application Infrastructure](https://jobs.lever.co/whoop/61862c63-b61e-4841-aad4-3a27f76377c8) | Boston; posted 20 Jan 2026 | Deep Kubernetes/networking, AWS/Terraform, performance incidents; Kafka, SLOs, RBAC and pod security |
| Gridware — [Senior Platform Engineer](https://jobs.lever.co/gridware/c01925b9-1458-4a12-a981-6fb6c6f8d968) | San Francisco; posted 7 May 2026 | Developer-platform tooling, EKS/GitOps/Terraform/Helm, IAM/VPC, Prometheus/Loki/Grafana/OTel; IoT helpful |
| OpenAI — [Software Engineer, Observability](https://openai.com/careers/software-engineer-observability-san-francisco/) | San Francisco; live, date not exposed | Large distributed log/metric/trace systems, Kubernetes/networking, Prometheus/OTel, AI-native incident tools |
| Scale AI — [Software Engineer, Frontier AI Infrastructure](https://job-boards.greenhouse.io/scaleai/jobs/4363623005) | Multiple US cities; updated 9 Jul 2026 | Secure scalable backend/inference, networking/latency/usage, Docker/Kubernetes/cloud, integration testing; clearance is role-specific |

### Agentic AI, AI infrastructure, and AI reliability

| Company and role | Location/date visible at research | Requirements that validate the plan |
|---|---|---|
| OpenAI — [Software Engineer, Agent Infrastructure](https://openai.com/careers/software-engineer-agent-infrastructure-san-francisco/) | San Francisco/New York; live, date not exposed | Large-scale ML/agent execution infrastructure, container orchestration, performance, Terraform/cloud, sandbox runtimes |
| Anthropic — [Staff Software Engineer, AI Reliability](https://job-boards.greenhouse.io/anthropic/jobs/5113224008) | SF/NYC/Seattle; updated 14 Jul 2026 | Distributed systems/SRE, LLM serving SLOs, token-path observability, multi-region reliability, incident leadership |
| Pleo — [Senior GenAI Platform Engineer](https://jobs.ashbyhq.com/pleo/934035cd-c8f1-4b93-b7ea-59e6d2f3ba0b) | European hubs; posted 10 Jul 2026 | Async/idempotent workflows, routing, RAG/MCP, eval/tracing/cost, multi-provider failure, injection/PII/credential safety |
| Kraken — [Site Reliability Engineer – AI Agents](https://jobs.ashbyhq.com/kraken.com/c7409ffc-4430-4cdd-906c-3a0487d3e780/) | Remote US; live, date not exposed | SRE/platform, ML infrastructure, Kubernetes/Terraform, agent guardrails/recovery, evals/model monitoring |
| Zanskar — [Platform Engineer, AI Agent Systems](https://jobs.lever.co/Zanskar/a8deddba-470c-4a12-a475-00f9fa42c304) | Salt Lake City; posted 26 Jun 2026 | LLM tool use, hallucinated-call/loop/context debugging, trust boundaries, revocable credentials, audit and sandboxing |
| LangChain — [Principal Software Engineer, AI Observability & Evals Platform](https://jobs.ashbyhq.com/langchain/d3f8de08-2e2b-4c3f-be1f-e63ca51f1d93/) | US hubs; posted 13 May 2026 | High-throughput trace/eval platform, Python/Go, ClickHouse/Postgres/Redis, query performance, testing and operations |
| Dashlane — [AI Deployment Software Engineer](https://job-boards.greenhouse.io/dashlane/jobs/8055239) | Paris; updated 10 Jul 2026 | LLM serving/evaluation, cloud/IaC, RAG/orchestration, latency/cost, prompt security, validation and HITL |
| Novara — [Senior Applied AI Engineer](https://jobs.lever.co/novara/4756bca8-fe07-411f-8904-ec8660090912) | Remote Canada; posted 22 Jun 2026 | LangGraph workflows, OpenSearch/pgvector RAG, OAuth/JWT/multi-tenancy, token/cost tracing, graceful degradation and HITL |
| Forter — [Senior Software Engineer II – Platform & AI](https://job-boards.greenhouse.io/forter/jobs/8289641002) | Tel Aviv; updated 7 Jul 2026 | Production LLM/agent workflows, distributed data systems, observability/guardrails, evals/regressions/MCP |
| White Circle — [ML Infrastructure Engineer](https://jobs.ashbyhq.com/whitecircle/9a66770a-f312-4cd7-8d83-60de8a01c61e/) | Paris/London; posted 6 Jul 2026 | Training/inference/evaluation pipelines, I/O/networking/scheduling, performance tracing, reproducible public benchmark work |
| Together AI — [AI Infrastructure Engineer](https://job-boards.greenhouse.io/togetherai/jobs/5138540007) | San Francisco; updated 10 Jul 2026 | Terraform/Kubernetes, monitoring, on-call, OS/storage/networking/distributed systems, availability and capacity |

### What the sample does—and does not—show

Within this 21-role sample, Kubernetes appeared explicitly in **11**, IaC tooling or experience in **12**, Python in **12**, Go in **5**, and IAM/access/secrets/isolation/guardrails in at least **14**. These are descriptive counts for this sample only, not labor-market prevalence estimates.

The recurring durable requirements are production ownership; failure-aware distributed design; platform-as-product thinking; containers/networking/IaC; high-volume data movement; SLOs/incidents; secure multi-tenancy; AI evaluation/trace/cost discipline; and technical leadership. Kubernetes, Terraform, LangGraph, Bedrock, vLLM, or a particular vector database are implementations of those durable concepts, not the organizing principles of the roadmap.

Rare but valuable signals include real robot hardware/edge fleet work, reproducible simulation, secure agent sandboxes with revocable credentials, high-volume AI trace/eval platforms, self-hosted inference benchmarking, GPU/RDMA experience, and strong public engineering artifacts. The plan pursues the first four only where affordable and honest; it defers the GPU-specific branch.

---

# Part 3 — Prioritized competency map

Depth means the level needed for the target interviews and role—not a claim about current depth. “Current” uses only supplied evidence.

## A. Shared foundation

| Skill | Priority | Required depth | Current evidence | Closure/verification |
|---|---|---|---|---|
| Distributed-systems failure models | P0 | Can design and lead | Strong operational adjacency | Failure matrix covering crash, omission, partition, duplication, reordering, slow dependency |
| Delivery semantics | P0 | Can design and lead | Direct and strong | Explain broker, application and sink guarantees separately |
| Idempotency | P0 | Can design and lead | Direct and strong | Ledger and duplicate/replay tests in both projects |
| Ordering | P0 | Can design and lead | Direct and strong | Partition-key and command-sequence invariants |
| Consistency | P0 | Can design and lead | Locking/outbox evidence | State which invariants need strong consistency and which tolerate lag |
| Consensus | P1 | Working knowledge | Unknown | Selected MIT 6.5840/Raft study; no implementation required |
| Replication | P1 | Can implement independently | Storage/messaging adjacency | Compare leader/quorum/object-store durability and recovery |
| Partitioning | P0 | Can design and lead | Kafka/OpenSearch/ClickHouse adjacency | Capacity model, hot-key test and repartition plan |
| Backpressure | P0 | Can design and lead | Queue/consumer evidence | Bounded queues and measured overload behavior |
| Load shedding | P0 | Can implement independently | Unknown | Priority classes, admission control, overload drill |
| Rate limiting | P0 | Can implement independently | Not explicit | Tenant token bucket with deterministic tests |
| Capacity planning | P0 | Can design and lead | Scale/performance evidence | Workload model, bottleneck estimate, measured saturation point |
| Tail latency | P0 | Can design and lead | Latency optimization evidence | p50/p95/p99, queueing analysis and deadline propagation |
| Linux | P1 | Can operate in production | Unknown from supplied profile | Diagnose sockets, file descriptors, CPU/memory/I/O in a lab |
| Networking | P0 | Can implement independently | gRPC/K8s adjacency | DNS/TLS/HTTP2/timeouts/keepalive/reconnect explanation |
| Kubernetes | P0 | Can operate in production | Direct but depth unknown | Probes, requests/limits, PDB, HPA, graceful shutdown and rollout |
| Performance engineering | P0 | Can design and lead | Direct and strong | Reproducible benchmark and profiler evidence |
| SLOs | P0 | Can design and lead | Observability adjacency | User-facing SLIs, error budget and burn-rate alert |
| Incident response | P0 | Can design and lead | Operational adjacency | Injected incident, timeline, mitigations, blameless postmortem |
| Security/threat modeling | P0 | Can implement independently | Multi-tenancy adjacency | Trust boundaries, least privilege, abuse cases, secret handling |
| Multi-tenancy | P0 | Can design and lead | Direct and strong | Identity propagated through API, storage, retrieval, tools and audit |
| API design | P0 | Can design and lead | Backend APIs/gRPC | Versioned contract, error model, pagination, idempotency, quotas |
| Testing distributed systems | P0 | Can implement independently | Reliability work adjacency | Deterministic fixtures, failure injection, property tests and replay tests |

## B. Platform and robotics-infrastructure specialization

| Skill | Priority | Required depth | Current evidence | Closure/verification |
|---|---|---|---|---|
| Edge computing | P0 | Can implement independently | Missing | Simulated edge process with local resource bounds |
| Cloud-edge synchronization | P0 | Can design and lead | Adjacent | ACK/resume protocol and reconciliation ADR |
| Intermittent connectivity | P0 | Can implement independently | Missing | Loss, jitter and 10-minute disconnect test |
| Store-and-forward | P0 | Can implement independently | Messaging adjacency | SQLite-WAL spool, priorities, eviction and corruption recovery |
| Sensor-data ingestion | P0 | Can implement independently | Adjacent streaming | Typed joint/pose/health/control/artifact envelopes |
| Video/audio streaming fundamentals | P1 | Working knowledge | Missing | Metadata/sample chunks, bitrate/latency/storage trade-off note |
| LiDAR/robotics data formats | P1 | Working knowledge | Missing | MCAP sample and point-cloud metadata; no perception algorithm work |
| Time synchronization | P0 | Can implement independently | Missing | robot/event/ingest timestamps, boot ID, skew fixture |
| Event-time processing | P0 | Can implement independently | Missing | Flink event-time window output |
| Out-of-order data | P0 | Can implement independently | Streaming adjacency | Watermark, allowed lateness and late side-output test |
| Kafka | P0 | Can design and lead | Direct and strong | Focus on trade-offs, not tutorials |
| Flink | P0 | Can implement independently | Missing | One bounded, tested PyFlink/Flink SQL job |
| NATS JetStream | P1 | Can design and lead | Direct and strong | Compare retention, consumers and replay to Kafka in ADR |
| Schema evolution | P0 | Can implement independently | Unknown | Protobuf compatibility CI and unknown-field test |
| gRPC streaming | P0 | Can implement independently | gRPC present | Flow control, deadlines, keepalive and reconnect benchmark |
| WebSockets | P1 | Working knowledge | Socket.io present | Explain browser fit versus gRPC robot link |
| Kubernetes operators | P2 | Awareness | Missing | Read concept; do not build one without lifecycle need |
| Helm | P0 | Can implement independently | Missing | Linted/tested chart and upgrade/rollback drill |
| Terraform/OpenTofu | P0 | Can implement independently | Missing | Small module with tests and encrypted/remote-state design note |
| Autoscaling | P0 | Can implement independently | Not explicit | HPA on backlog/custom metric; show stabilization behavior |
| Failover | P0 | Can design and lead | Reliability adjacency | Broker/consumer/API failure drill and recovery objective |
| PostgreSQL | P0 | Can design and lead | Direct and strong | Metadata/control state; no beginner study |
| Redis | P0 | Can implement independently | Direct and strong | Rate limit/ephemeral state; document loss semantics |
| ClickHouse | P0 | Can design and lead | Direct and strong | Telemetry schema, partitions, ordering and retention |
| Object storage | P0 | Can implement independently | Missing | MCAP object integrity, lifecycle and manifest |
| Vector storage | P2 | Awareness | OpenSearch adjacency | Add only for an actual robotics retrieval use case |
| API gateways | P1 | Can implement independently | Backend adjacency | TLS/auth/rate-limit boundary; local ingress acceptable |
| OAuth 2.0/OIDC | P0 | Can implement independently | Missing/unknown | Authorization-code concepts plus resource-server JWT validation |
| Authorization | P0 | Can design and lead | Tenant isolation adjacency | Tenant RBAC and deny-by-default tests |
| Rate limiting | P0 | Can implement independently | Missing | Redis token bucket with fail-open/fail-closed decision |
| Quotas | P0 | Can implement independently | Feature tiers adjacent | Daily tenant budget and enforcement tests |
| Usage metering | P0 | Can implement independently | Missing | Immutable deduplicated usage event and reconciliation |
| Model registries | P1 | Can implement independently | Missing | MLflow version/tags/aliases workflow |
| Model rollout | P1 | Can implement independently | Missing | Deterministic canary, rollback and audit metadata |
| ML metadata | P1 | Working knowledge | Missing | Link run, artifact, schema, dataset manifest and rollout |
| Training-data lineage | P1 | Can implement independently | Data pipeline adjacency | Dataset manifest and reproducible query/export |
| Hardware-in-the-loop simulation | P2 | Awareness | Missing | Software simulator only; describe limits |
| Robotics middleware/ROS 2 concepts | P1 | Working knowledge | Missing | Topics/services/actions, QoS, clock and rosbag/MCAP note |
| OpenTelemetry | P0 | Can design and lead | Direct and strong | Apply existing strength to edge-to-cloud trace correlation |
| Prometheus | P0 | Can operate in production | Direct and strong | SLI recording rules and actionable alerts |
| Grafana | P1 | Can operate in production | Unknown | Versioned dashboard screenshots/JSON |

## C. Agentic AI systems specialization

| Skill | Priority | Required depth | Current evidence | Closure/verification |
|---|---|---|---|---|
| Transformer/LLM engineering fundamentals | P0 | Working knowledge | Missing | Explain tokenization, attention limits, decoding, inference latency; no model training |
| Tokenization | P0 | Working knowledge | Missing | Token-budget tests across representative documents/tools |
| Context windows/context management | P0 | Can implement independently | Missing | Evidence selection, truncation policy and overflow test |
| Embeddings | P0 | Can implement independently | Semantic search adjacency | Versioned embedding pipeline and offline retrieval comparison |
| Retrieval | P0 | Can design and lead | Direct but limited | Reuse search depth; add answer-grounding path |
| Hybrid search | P0 | Can design and lead | Direct and strong | Preserve as differentiator; reproduce on incident corpus |
| Reranking | P0 | Can implement independently | Ranking adjacency | Compare lexical, hybrid and reranked results |
| RAG | P0 | Can implement independently | Missing | Access-aware retrieval, evidence bundle, generation and citations |
| Chunking | P0 | Can implement independently | Missing | Structure-aware baseline and ablation |
| Query transformation | P1 | Can implement independently | Missing | Only retain if eval improves recall/task success |
| Grounded generation | P0 | Can implement independently | Missing | Citation resolver and unsupported-claim grader |
| Structured output | P0 | Can implement independently | Missing | Strict Pydantic schema and retry/repair budget |
| Tool calling | P0 | Can implement independently | Missing | Typed registry and deterministic fake-model tests |
| Planning | P1 | Can implement independently | Missing | Bounded plan with max steps; compare to fixed workflow |
| Agent state machines | P0 | Can design and lead | Ordered workflow adjacency | Explicit states, transitions, invariants and terminal outcomes |
| Durable workflows | P0 | Can implement independently | Strong conceptual adjacency | Temporal replay/restart/versioning tests |
| Human in the loop | P0 | Can implement independently | Missing | Paused workflow, signed approval, expiry and resumption |
| Short-term state | P0 | Can implement independently | Database/Redis adjacency | Persist evidence and decisions outside prompt text |
| Long-term memory | P1 | Working knowledge | Missing | Add only with retention/provenance/deletion semantics |
| Agent orchestration | P0 | Can design and lead | Missing | One explicit workflow, bounded loop and failure policy |
| Multi-agent trade-offs | P2 | Awareness | Missing | Written comparison; no implementation unless measured gain |
| Model routing | P1 | Can implement independently | Missing | Capability/cost/latency policy and two adapters |
| Retries/fallbacks | P0 | Can design and lead | Direct systems evidence | Error taxonomy; retry only safe/transient steps |
| Idempotent tool execution | P0 | Can design and lead | Direct systems evidence | Invocation key and exactly-one external effect test |
| Sandboxing | P1 | Working knowledge | Missing | No shell; mock ticket tool; discuss stronger isolation |
| Prompt-injection defense | P0 | Can implement independently | Missing | Untrusted-content labeling, policy outside prompt, attack suite |
| Tool authorization | P0 | Can design and lead | Multi-tenancy adjacency | Per-tool/action/resource decision before execution |
| Evaluation datasets | P0 | Can implement independently | Missing | Versioned 30–50 task corpus with difficulty/tags |
| Offline evaluation | P0 | Can design and lead | Missing | Repeated trials, baselines, confidence intervals |
| Online evaluation | P1 | Working knowledge | Observability adjacency | Shadow/sampled design only; no fabricated production traffic |
| Task-completion evaluation | P0 | Can design and lead | Missing | Outcome signals independent of model self-report |
| LLM-as-judge limitations | P0 | Working knowledge | Missing | Calibrate to human labels; order/blinding/variance checks |
| Deterministic evaluators | P0 | Can implement independently | Testing adjacency | Schema, tool, citation, ACL and expected-signal graders |
| Groundedness | P0 | Can implement independently | Missing | Claim-to-evidence checks and human audit |
| Retrieval evaluation | P0 | Can design and lead | Search relevance adjacency | Recall@5, nDCG@10/MRR and failure slices |
| Regression testing | P0 | Can design and lead | Engineering adjacency | Versioned dataset and CI budget gate |
| Latency/cost evaluation | P0 | Can design and lead | Performance/cost strength | Per-step distributions and task-level budget |
| Agent tracing/AI observability | P0 | Can design and lead | OTel strength, AI layer missing | GenAI/model/retrieval/tool/workflow spans |
| Token/cost monitoring | P0 | Can implement independently | Missing | Provider usage capture and estimated/actual reconciliation |
| AI incident response | P0 | Can design and lead | Strong general adjacency | Provider outage, retrieval regression, unsafe tool attempt drills |
| Vector databases | P1 | Can operate in production | OpenSearch evidence | OpenSearch hybrid implementation; avoid tool collecting |
| Knowledge graphs | P2 | Awareness | Missing | Defer until relational retrieval has measured value |
| Semantic caching | P2 | Awareness | Search/cache adjacency | Threat/tenant invalidation design only |
| Model gateways | P1 | Can implement independently | API/platform adjacency | Minimal in-process adapter first; external gateway only if justified |
| Rate limiting | P0 | Can implement independently | Not explicit | Tenant/run/model/tool budgets |
| Multi-tenancy | P0 | Can design and lead | Direct and strong | Enforce through retrieval, cache, workflow and tools |
| Production deployment | P0 | Can operate in production | K8s present | Container/K8s, graceful shutdown, queue drain, rollback |

## Highest-leverage skills across both tracks

1. Explicit failure models and idempotent effects.
2. Backpressure, admission control, deadlines, and load shedding.
3. Tenant identity, authorization, quotas, and auditable decisions.
4. OpenTelemetry-based causal debugging and user-facing SLOs.
5. Reproducible containers, Helm, IaC, rollout, and rollback.
6. Event/retrieval/evaluation datasets with deterministic regression tests.
7. Capacity, tail-latency, and cost reasoning.
8. Durable state machines rather than implicit control flow.

---

# Part 4 — Ranked resource library

## Scoring and use

The score tuple is **R/D/P/E/C/M**: job relevance (25), depth/correctness (20), practical value (20), evidence potential (15), source credibility (10), and current access/maintenance (10). The total follows the slash-separated components. A canonical older work is not penalized merely for age.

“Must study” means study the exact excerpt, not finish the whole resource. “Strong” is used when the linked project task calls for it. “Reference” is consulted during design/debugging. The library is intentionally capped at 30; its hours are not additive—the 24-week plan schedules about 60 focused study hours.

| # | Resource; type; track | Author/date/level | Exact scope | Why selected; existing knowledge reused; gap addressed | Time and practical output | Score and label |
|---:|---|---|---|---|---|---|
| 1 | [Designing Data-Intensive Applications, 2nd ed.](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/); book; both | Martin Kleppmann and Chris Riccomini; Feb 2026; advanced | Ch. 2 nonfunctional requirements, 5 encoding/evolution, 9 distributed-system trouble, 10 consistency/consensus, 12 stream processing, 13 stream/batch philosophy | Connects direct Kafka/outbox/storage experience to formal failure, evolution and consistency reasoning; closes theory/interview precision gaps | 7h; six invariant cards plus two system-design trade-off notes | **98** (25/20/20/15/10/8); **must study**; paid, estimate USD 60–80 |
| 2 | [MIT 6.5840 Distributed Systems](https://pdos.csail.mit.edu/6.824/index.html) and [schedule](https://pdos.csail.mit.edu/6.824/schedule.html); university course; shared | MIT PDOS; Spring 2026; expert | RPC, GFS, Raft, ZooKeeper, transactions, Spanner, verification lectures/papers; skip full labs unless a concept remains weak | Reuses production distributed systems; closes consensus, replication and rigorous failure-model depth without reteaching brokers | 6h; Raft/lease/transaction interview notes and one fault timeline | **93** (22/20/16/15/10/10); **strong** |
| 3 | [Google SRE Workbook](https://sre.google/workbook/table-of-contents/), [handling overload](https://sre.google/sre-book/handling-overload/), and [AWS load shedding](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/); books/article; both | Google SRE authors and David Yanacek; maintained online; advanced | Workbook Ch. 2 SLOs, 5 alerting, 9 incident, 10 postmortem, 11 load, 13 pipelines, 16 canary, 17 overload; bounded queues/retry budgets | Reuses OTel/Prometheus/incident adjacency; closes explicit SLO, overload, canary and postmortem practice | 5h; SLO, burn alert, game day and postmortem template | **96** (25/19/20/14/10/8); **must study** |
| 4 | [The Dataflow Model](https://research.google/pubs/the-dataflow-model-a-practical-approach-to-balancing-correctness-latency-and-cost-in-massive-scale-unbounded-out-of-order-data-processing/); peer-reviewed paper; Platform | Akidau et al.; VLDB 2015, Test of Time award in 2026; expert | Event time, watermarks, triggers, accumulation and correctness/latency/cost trade-offs | Reuses streaming practice; closes conceptual event-time gap and supports the Flink ADR | 2h; one-page mapping from paper concepts to telemetry job | **94** (24/20/17/13/10/10); **strong** |
| 5 | [Streaming Systems](https://www.oreilly.com/library/view/streaming-systems/9781491983867/ch01.html); book; Platform | Akidau, Chernyak and Lax; 2018; advanced | Deep-read Ch. 2, 3, 5, 7; skim 1, 4, 9: what/where/when/how, watermarks, side effects and persistent state | Reuses Kafka/JetStream/ClickHouse; closes watermarks, late data, replay and end-to-end side-effect semantics | 7h; event-time/late-data ADR and golden tests | **96** (25/20/19/14/10/8); **must study**; paid, estimate USD 40–60 |
| 6 | [Apache Flink 2.3 streaming analytics](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/streaming_analytics/), [watermarks](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/event-time/generating_watermarks/), [backpressure](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/monitoring/back_pressure/), and [fault tolerance](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/); official docs/lab; Platform | Apache Software Foundation; 2.3.0 released 25 Jun 2026; advanced | Timestamps, bounded out-of-orderness, idle inputs/alignment, late side output, checkpoints/savepoints, Kafka source, backpressure metrics | Direct role requirement; reuses broker/data-pipeline depth; closes Flink operation and event-time implementation | 7h; PyFlink/Flink SQL job, restart test and backpressure capture | **98** (25/20/20/15/10/8); **must study** |
| 7 | [AWS IoT Greengrass Stream Manager](https://docs.aws.amazon.com/greengrass/v2/developerguide/manage-data-streams.html); official design reference; Platform | AWS; current Jul 2026; intermediate | Storage type/limit, retention, export priority/bandwidth/timeout, disconnected behavior and authorization | Provides concrete store-and-forward policies; reuses queue/retry work; closes bounded edge-spool/full-disk reasoning | 2h; spool policy ADR and disconnect/full-disk/priority tests; do not install Greengrass | **86** (22/16/17/13/10/8); **strong** |
| 8 | [ROS 2 support matrix](https://ros.org/reps/rep-2000.html), [interfaces](https://docs.ros.org/en/kilted/Concepts/Basic/Interfaces-Topics-Services-Actions.html), [sensor_msgs](https://docs.ros.org/en/kilted/p/sensor_msgs/), [clock/time design](https://design.ros2.org/articles/clock_and_time.html), [QoS design](https://design.ros2.org/articles/qos), and [rosbag2](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html); official packet; Platform | Open Robotics/ROS community; Jazzy LTS supported to May 2029; intermediate | Topics/services/actions, DDS/RMW, reliability/durability/history/deadline/liveliness; JointState/IMU/PointCloud2/Image; ROS/system/steady time, jumps and bag QoS | Prevents a generic IoT demo from being mislabeled robotics; closes vocabulary, timing and data-model gaps | 6h; Jazzy rclpy publisher, bag and QoS/time/skew ADR | **95** (25/18/19/14/10/9); **must study** |
| 9 | [MCAP specification/guides](https://mcap.dev/guides), [ROS 2 guide](https://mcap.dev/guides/getting-started/ros-2), and [repository](https://github.com/foxglove/mcap); format/docs/repo; Platform | Foxglove; CLI v0.3.0 released 15 Jul 2026; intermediate | Records, schemas/channels, chunks/indexes, compression/CRC, partial recovery, Go reader/writer and CLI validation | Reuses data-format/storage experience; closes robotics-native artifact/replay evidence | 3h; 60-second sensor file, manifest, validation and zstd/LZ4 comparison | **92** (24/18/18/14/9/9); **must study** |
| 10 | [Apache Kafka 4.2 design](https://kafka.apache.org/42/design/design/); official architecture docs; Platform | Apache Software Foundation; 4.2.0 released 17 Feb 2026; advanced refresher | Batching, ordering, consumer position/replay, replication/ISR, idempotence/transactions, compaction and quotas | Candidate already knows Kafka; this creates an explicit selection rationale and avoids beginner work | 2h; Kafka-versus-JetStream ADR | **89** (23/18/17/13/10/8); **strong** |
| 11 | [JetStream concepts](https://docs.nats.io/nats-concepts/jetstream), [streams](https://docs.nats.io/nats-concepts/jetstream/streams), [consumers](https://docs.nats.io/nats-concepts/jetstream/consumers), and [model deep dive](https://docs.nats.io/using-nats/developer/develop_jetstream/model_deep_dive); official docs; Platform | NATS/Synadia; nats-server 2.14.3 released 29 Jun 2026; advanced refresher | Retention/discard, dedup, durable pull consumers, ACK/redelivery/backoff, MaxAckPending, replay, mirrors and reconnect/slow consumers | Reuses direct JetStream migration; gap is choosing when not to use it | 2h; other half of broker ADR; do not run two brokers in MVP | **90** (23/18/18/13/9/9); **strong** |
| 12 | [gRPC Go basics](https://grpc.io/docs/languages/go/basics/), [flow control](https://grpc.io/docs/guides/flow-control/), [keepalive](https://grpc.io/docs/guides/keepalive/), [retry](https://grpc.io/docs/guides/retry/), and [deadlines](https://grpc.io/docs/guides/deadlines/); official docs; Platform | gRPC/CNCF; grpc-go 1.82.0 released 30 Jun 2026; advanced | Bidirectional streams, flow control, keepalive safety, deadline/cancellation, retry boundary, status and credentials | Reuses gRPC/Go; closes the distinction between transport flow control and durable application ACK | 4h; bounded stream, ACK/resume token, reconnect jitter and failure tests | **94** (25/19/19/14/9/8); **must study** |
| 13 | [Kubernetes probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/), [HPA](https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/), [PDB](https://kubernetes.io/docs/tasks/run-application/configure-pdb/), and [NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/); official docs; both | Kubernetes project; living docs updated through 2026; advanced | Probe semantics, requests/limits, rollout, HPA stabilization, PDB limitations, topology, security context and network policy | Reuses Kubernetes; closes inspectable production workload evidence | 4h; k3d hardening and rollout/failure tests | **91** (24/18/19/14/8/8); **must study** |
| 14 | [Helm chart best practices](https://docs.helm.sh/docs/chart_best_practices/), [topics](https://helm.sh/docs/topics/), and [repository](https://github.com/helm/helm); official docs/repo; both | Helm/CNCF; 4.2.3 released 9 Jul 2026; intermediate | Structure/templates/dependencies, values schema, hooks, tests, OCI/provenance, RBAC and deprecated APIs | Closes a named CV gap with small reviewable evidence | 3h; chart, lint/render snapshot, test, upgrade and rollback | **91** (24/17/19/14/9/8); **must study** |
| 15 | [OpenTofu modules](https://opentofu.org/docs/language/modules/), [testing](https://opentofu.org/docs/cli/commands/test/), [state encryption](https://opentofu.org/docs/language/state/encryption/), and [repository](https://github.com/opentofu/opentofu); docs/repo; both | Linux Foundation/OpenTofu; 1.12.4 released 13 Jul 2026; intermediate | Provider constraints, modules, plan/apply/destroy, state/locking/sensitive values/encryption and tests | Closes IaC/state-lifecycle evidence without mandatory cloud spend | 4h; small module, encrypted state, zero-diff second plan and clean destroy | **92** (24/18/19/14/9/8); **must study** |
| 16 | [OAuth 2.0 Security BCP, RFC 9700](https://datatracker.ietf.org/doc/html/rfc9700), [OIDC Core](https://openid.net/specs/openid-connect-core-1_0.html), and [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/); standards/security packet; both | IETF/OpenID/OWASP; Jan 2025/current errata; advanced | RFC §§2–4; OIDC §§3, 5, 9, 15, 16; OWASP API1/2/4/5/8 | Reuses tenant isolation; closes authn/authz/resource-ownership/exhaustion precision | 4h; identity sequence, authorization matrix and negative tests | **95** (25/19/19/14/10/8); **must study** |
| 17 | [MLflow Model Registry workflow](https://www.mlflow.org/docs/latest/ml/model-registry/workflow/), [model signatures](https://mlflow.org/docs/latest/ml/model/signatures/), and [deployment](https://mlflow.org/docs/latest/ml/deployment/index.html); official docs/repo; Platform | LF AI & Data; MLflow 3.14.0 released 17 Jun 2026; intermediate | Runs/artifacts, versions, aliases/tags, signatures/examples, lineage and local serving; stages are deprecated | Reuses data pipelines; closes model registry/provenance/canary/rollback evidence without GPU infrastructure | 4h; CPU model v1/v2, champion/candidate aliases and deterministic 10% canary | **90** (23/17/19/14/9/8); **strong** |
| 18 | [Stanford CS336: Language Modeling from Scratch](https://cs336.stanford.edu/); university course; Agentic AI | Hashimoto, Liang et al.; Spring 2026; advanced | Lectures 1 tokenization, 3 architecture/hyperparameters, 10 inference, 12 evaluation; skip GPU-heavy assignments | Reuses Python/systems skill; closes engineering-level LLM/token/context/inference limits without a training detour | 6h; LLM limits note and tokenizer/context/cost micro-benchmark | **87** (22/19/15/12/10/9); **strong** |
| 19 | [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) and [Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents); primary engineering articles; Agentic AI | Anthropic; Dec 2024/Sep 2025; advanced | Workflow versus agent, routing/parallel/evaluator patterns, tool design; system/tool/retrieval/history context and memory trade-offs | Reuses event-workflow/data-model thinking; closes pattern selection and context discipline | 3h; ADR rejecting unnecessary multi-agent design plus context budget | **93** (25/18/18/14/9/9); **must study** |
| 20 | [OpenAI Function Calling](https://developers.openai.com/api/docs/guides/function-calling) and [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs); official API docs; Agentic AI | OpenAI; current 16 Jul 2026; advanced | Tool lifecycle, strict schemas, parallel calls, refusals/incomplete/error handling; implement behind provider-neutral types | Reuses APIs/Python; closes structured output/tool use while making clear schema validity is not authorization/correctness | 3h; provider conformance and semantic-validation tests | **94** (25/18/19/14/10/8); **must study** |
| 21 | [Temporal Python SDK](https://github.com/temporalio/sdk-python), [message passing](https://docs.temporal.io/develop/python/workflows/message-passing), [testing](https://docs.temporal.io/develop/python/best-practices/testing-suite), and [error handling](https://docs.temporal.io/develop/python/best-practices/error-handling); docs/repo; both | Temporal; SDK 1.30.0 released 2 Jul 2026; expert | Deterministic workflows versus activities, retries/timeouts, signals/updates, approval, cancellation, replay/time skipping and OTel | Directly reuses queue/retry/idempotency knowledge; closes durable orchestration/recovery | 7h; crash-resumable approval workflow and replay tests | **97** (25/20/20/15/9/8); **must study** |
| 22 | [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview), [persistence](https://docs.langchain.com/oss/python/langgraph/persistence), and [Functional API](https://docs.langchain.com/oss/python/langgraph/functional-api); docs/repo; Agentic AI | LangChain; 1.2.9 released 10 Jul 2026; advanced | Checkpoints, pending writes, replay/time travel, interrupts/HITL and Postgres persistence | Reuses workflow design; closes framework comparison and provides completion fallback | 4h; same crash/HITL spike as Temporal and framework ADR | **91** (24/18/18/14/9/8); **must study for comparison** |
| 23 | [PydanticAI models](https://pydantic.dev/docs/ai/models/overview/), [Temporal integration](https://pydantic.dev/docs/ai/integrations/durable_execution/temporal/), [deferred tools](https://pydantic.dev/docs/ai/tools-toolsets/deferred-tools/), and [evals](https://pydantic.dev/docs/ai/evals/evals/); docs/repo; Agentic AI | Pydantic; 2.10.0 released 14 Jul 2026; advanced | Typed tools/results, provider profiles, TestModel/FunctionModel, fallback, Temporal Activities, deferred approval and evaluators | Reuses Python/API work; closes typed provider abstraction, routing/fallback and deterministic testing | 5h; adapter, fake model, fallback tests and custom evaluators | **94** (25/18/19/15/9/8); **must study**; pin versions due rapid releases |
| 24 | [OpenSearch hybrid search](https://docs.opensearch.org/latest/vector-search/ai-search/hybrid-search/index/), [reranking](https://docs.opensearch.org/latest/search-plugins/search-relevance/reranking-search-results/), and [rank evaluation](https://docs.opensearch.org/latest/api-reference/search-apis/rank-eval/); official docs; Agentic AI | OpenSearch; current 2026; advanced | BM25+dense pipeline, normalization/RRF, cross-encoder rerank and rank-eval API | Reuses strongest AI adjacency; closes RAG retrieval/rerank/evaluation evidence | 4h; BM25 versus hybrid versus reranked benchmark | **96** (25/19/20/15/9/8); **must study** |
| 25 | [BEIR paper/repository](https://github.com/beir-cellar/beir) and [Sentence Transformers Retrieve & Re-Rank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html); paper/lab; Agentic AI | Thakur et al./UKP; NeurIPS 2021, BEIR v2.2.0 Jun 2025; advanced | Paper §§3–5, evaluation code, bi-encoder retrieval/CrossEncoder rerank; use methods, not production dependency | Reuses search ranking; closes baselines, Recall/MRR/nDCG and quality/latency trade-offs | 4h; reusable retrieval evaluator and top-k/rerank experiment | **89** (24/18/18/13/9/7); **strong** |
| 26 | [Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents); primary engineering guide; Agentic AI | Anthropic; 9 Jan 2026; advanced | Task, trial, grader, transcript, outcome and harness; code/model/human graders; pass@k/pass^k; initial 20–50 tasks | Reuses measurement/observability; closes outcome-based agent eval design and vocabulary | 3h; evaluation specification and failure taxonomy | **98** (25/20/20/15/10/8); **must study** |
| 27 | [OpenAI Evaluation Best Practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices), [Working with Evals](https://developers.openai.com/api/docs/guides/evals), and [tau2-bench](https://github.com/sierra-research/tau2-bench); official docs/benchmark; Agentic AI | OpenAI and Sierra Research; current, tau3 1.0 Mar 2026; advanced | Objectives, representative data, deterministic/executable graders, human calibration; task/policy/tool schemas, final-state evaluation and repeated-run reliability | Reuses testing discipline; closes regression harness and task-completion benchmark design | 5h; incident task schema, 30-case dataset and CI gates | **95** (25/19/20/14/9/8); **must study** |
| 28 | [OpenTelemetry GenAI conventions](https://github.com/open-telemetry/semantic-conventions-genai), [May 2026 walkthrough](https://opentelemetry.io/blog/2026/genai-observability/), and [MLflow GenAI tracing](https://mlflow.org/docs/latest/genai/tracing); standard/docs; Agentic AI | OpenTelemetry and MLflow; semconv 1.43.0/MLflow 3.14 in 2026; expert | Agent/workflow/model/tool/retrieval/eval spans, tokens/latency/cost, sensitive-content controls, local trace/eval UI | Directly reuses OTel/ClickHouse/trace expertise; closes AI-specific telemetry and cost evidence | 4h; versioned telemetry contract, traces and dashboard | **96** (25/19/20/15/9/8); **must study**; GenAI conventions remain evolving, so wrap attributes |
| 29 | [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), [AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html), [AgentDojo](https://github.com/ethz-spylab/agentdojo), and [CaMeL](https://arxiv.org/abs/2503.18813); security guides/benchmark/paper; Agentic AI | OWASP/ETH Zurich/Google researchers; 2024–2026; expert | Goal hijack/tool misuse/privilege/memory/cascade, least privilege/audit; indirect-injection cases and control/data separation | Reuses multi-tenancy/policy thinking; closes injection, authorization and adversarial-testing gap | 5h; threat model, 20-case attack suite and control/data-flow diagram | **96** (25/19/20/15/9/8); **must study** |
| 30 | [JudgeBench](https://arxiv.org/abs/2410.12784) and [Judging the Judges: Position Bias](https://arxiv.org/abs/2406.07791); papers; Agentic AI | ScalerLab and other researchers; 2024; advanced | Objective factual/logical pairs, judge weakness, answer-order/position bias, repeated judging and calibration | Closes the risk of using an LLM judge as ground truth | 2h; blind/order-swapped judge protocol with human calibration sample | **83** (20/18/14/13/10/8); **reference** |

## Repository maintenance and source-reading audit

This is a 16 July 2026 snapshot. Release recency and issue/PR traffic show activity, not correctness or production readiness. Star counts were deliberately excluded. “Adoption” is recorded only at a cautious level; vendor case studies were not independently audited.

| Repository | Release/activity/license | Docs, examples, tests, issue/PR activity | Source worth reading | Adoption and realistic contribution |
|---|---|---|---|---|
| [apache/flink](https://github.com/apache/flink) | 2.3.0, 25 Jun; commits through 15 Jul; Apache-2.0 | Extensive docs/runtime/connector/integration tests; active review traffic | flink-runtime, flink-table, flink-connectors, docs | Established production stream processor. Docs, examples or focused connector test are realistic; scheduler/state internals are not a first contribution |
| [nats-io/nats-server](https://github.com/nats-io/nats-server) | 2.14.3, 29 Jun; active 15 Jul; Apache-2.0 | Extensive server tests; active issues/PRs | server, test, conf, doc | Established messaging system; docs/configuration or focused test realistic, Raft internals not initially |
| [foxglove/mcap](https://github.com/foxglove/mcap) | Go CLI 0.3.0, 15 Jul; active same day; MIT | Guides, multiple language libs, conformance tests/test data; active traffic | go/mcap, go/cli/mcap, tests, testdata | Used in robotics tooling including ROS integration; docs/examples/conformance fix realistic |
| [grpc/grpc-go](https://github.com/grpc/grpc-go) | 1.82.0, 30 Jun; active 15 Jul; Apache-2.0 | Examples, transport/integration tests and benchmarks; active traffic | examples/route_guide, stream.go, credentials, keepalive, stats, test | Established production transport; docs/example/test contribution realistic |
| [helm/helm](https://github.com/helm/helm) | 4.2.3, 9 Jul; active 15 Jul; Apache-2.0 | Docs, adopter list, test data and active issue/PR flow | cmd/helm, pkg/chart, pkg/action, pkg/release, testdata | Broad Kubernetes ecosystem adoption; docs/chart/test-data change realistic |
| [opentofu/opentofu](https://github.com/opentofu/opentofu) | 1.12.4, 13 Jul; active 15 Jul; MPL-2.0 | Tests, RFCs, docs and security process; active traffic | internal/terraform, backend, encryption, command, testing | Production adoption is visible through project ecosystem but not scored; docs or focused test realistic |
| [mlflow/mlflow](https://github.com/mlflow/mlflow) | 3.14.0, 17 Jun; active 15 Jul; Apache-2.0 | Large docs/examples/tests/charts surface and heavy issue/PR traffic | tracking, store/model_registry, models, genai, tests, charts | Widely reported production use; docs/eval example more realistic than core registry changes |
| [temporalio/sdk-python](https://github.com/temporalio/sdk-python) | 1.30.0, 2 Jul; active 15 Jul; MIT | SDK samples, replay/time-skipping/OTel tests; active issues/PRs | temporalio/workflow.py, activity.py, testing helpers, tests | Mature general workflow use; AI integration is newer. Docs/test fix realistic, internals steeper |
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | 1.2.9, 10 Jul; active 15 Jul; MIT | Checkpoint/graph/docs/tests with high issue/PR velocity | libs/langgraph, libs/checkpoint and tests | Vendor-published cases include major companies; treat as directional. Small test/docs fix realistic; pin version |
| [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) | 2.10.0, 14 Jul; active 15 Jul; MIT | pydantic_ai_slim, evals, graph, examples and extensive tests; high activity | pydantic_ai_slim, pydantic_evals, pydantic_graph, tests | Newer framework with rapid releases. Best contribution candidate here: typed Python docs/test/eval issue |
| [beir-cellar/beir](https://github.com/beir-cellar/beir) | 2.2.0, 4 Jun 2025; last observed push Oct 2025; Apache-2.0 | Clear evaluation/examples with moderate issue activity | beir/retrieval/evaluation.py and examples | Research benchmark, not production runtime; evaluator/documentation contribution plausible |
| [open-telemetry/semantic-conventions](https://github.com/open-telemetry/semantic-conventions) and [GenAI repo](https://github.com/open-telemetry/semantic-conventions-genai) | core 1.43.0, 3 Jul; active 15 Jul; Apache-2.0 | Specification/tests and active proposal/review flow | model/registry/gen-ai and generated docs | Standard is evolving; specification issue/example contribution realistic after project evidence |
| [sierra-research/tau2-bench](https://github.com/sierra-research/tau2-bench) | tau3 1.0, 18 Mar 2026; active research repo; MIT | Task/tool/evaluator schemas, docs/tests and active issue/PR flow | domains, environments, evaluators and tests | Benchmark methodology, not production dependency; incident-domain adapter should stay in candidate repo |

## Cost guidance

The plan is viable for **USD 70–220**, with a hard ceiling of USD 500:

- Books: USD 0 if library access exists; otherwise roughly USD 100–140 for DDIA 2e and Streaming Systems.
- Hosted-model calls: target USD 20–60 across development and eval; enforce a monthly and per-run cap. Prices are volatile, so record the provider’s current rate and actual token bill in the report rather than copying a static estimate here.
- Optional cloud benchmark: USD 15–25 using one ephemeral 4-vCPU/8-GB-class VM plus modest storage; local-only completion remains valid.
- Domain/API services: USD 0; use local Temporal, OpenSearch, ClickHouse, Kafka, Postgres, MLflow and MinIO.
- Reserve: USD 50 for one unexpectedly valuable book/API experiment. Do not spend merely to use the budget.

---

# Part 5 — Six-week Platform application sprint

**Milestone 1 date: 27 August 2026.** Applications begin in Week 1; Week 6 is the interview-conversion milestone. Every week totals 10 hours. I/L/W means implementation, learning, and interview/writing/application work.

| Week/date | Objective and exact study | Implementation | Deliverable and verification | Hours | Job link and interview question unlocked |
|---|---|---|---|---:|---|
| 1 — 17–23 Jul | Freeze system boundary. Streaming Systems Ch. 2; ROS topics/QoS/time; MCAP records/chunks | Repository scaffold; Protobuf envelope; Go fleet generator; one Jazzy rclpy publisher; one valid MCAP recording | README problem statement, context diagram, workload model, ADR-001 semantics. Decode/validate MCAP and run 100 simulated IDs | 6I/2.5L/1.5W | A: sensor vocabulary and schema evolution. “How would you model joint, health and artifact data without putting video in Kafka?” Apply to Job A and exact NVIDIA stretch |
| 2 — 24–30 Jul | Greengrass store-forward patterns; DDIA Ch. 5 excerpts; gRPC flow-control/deadline guide | SQLite-WAL edge spool, priority/cap policy, checksums, restart/full-disk behavior | Tests prove an accepted ID survives process restart; memory is bounded; disk-full refusal/shedding is explicit, never silent | 6I/2.5L/1.5W | A: intermittent connectivity. “What does accepted mean at the edge, and what happens when disk is full?” |
| 3 — 31 Jul–6 Aug | gRPC bidi stream, retry/keepalive; Kafka design ordering/replay; JetStream consumer refresher | Bounded gRPC send window, application ACK/resume, reconnect jitter; Go ingress commits to Kafka | Five-minute link cut resumes from highest contiguous ACK; trace shows write is not acknowledged before broker commit; Kafka/JetStream ADR | 6.5I/2L/1.5W | A: backpressure and broker choice. “Why not trust gRPC flow control as durability?” “Kafka or JetStream here?” |
| 4 — 7–13 Aug | Streaming Systems Ch. 3/5; Dataflow paper event-time sections; Flink watermark/fault docs | PyFlink/Flink SQL event-time job, five-second bounded watermark, explicit late route; ClickHouse raw and minute aggregate tables | Golden fixture injects duplicates, 10% out-of-order up to 5s and 1% later; within-bound aggregate matches oracle; late IDs remain inspectable; restart test passes | 6I/3L/1W | A: event time and exactly-once claims. “How do watermarks trade correctness, latency and cost?” |
| 5 — 14–20 Aug | RFC 9700 §§2–4; OIDC §§3/5/15/16; OWASP API1/2/4/5; SRE SLO chapter | Device register/query/command endpoints; JWT validation; tenant RBAC; Redis token bucket; deduplicated usage ledger; command outbox | Wrong audience/expiry, cross-tenant ID, viewer command and unknown device are denied. Retry/replay produces one usage event. SLI definitions committed | 6I/2.5L/1.5W | A: secure developer platform. “Where is tenant identity enforced?” “How do quota and metering differ?” |
| 6 — 21–27 Aug | SRE alert/postmortem/overload excerpts; selected Kubernetes probe concepts | Compose one-command demo; OTel async trace; Prometheus/Grafana dashboard; load/failure scripts; benchmark, limitation section and postmortem | Clean checkout runs. 100 robots × 5 events/s for 15 min; 5-min disconnect has zero missing IDs already accepted to edge spool; bounded memory; one cross-service trace; actual p50/p95/p99 and duplicates reported | 6I/1.5L/2.5W | A: SLO, incident and capacity. “What failed first, and how do you know?” Publish Project 1 MVP and run one 60-minute mock |

## Week-6 Project 1 minimum viable milestone

The milestone is complete only when all of these are reproducible:

1. A reviewer can clone and run the happy path plus disconnect test from one documented command sequence.
2. 100 robots × 5 events/s runs for 15 minutes on a named laptop configuration.
3. A five-minute disconnect keeps memory bounded and loses no identifier already committed to the local edge spool.
4. Transport duplicates are permitted and measured; the materialized aggregate is idempotent. The README does not claim end-to-end exactly-once.
5. Ten percent of events arrive up to five seconds out of order and one percent later; expected-window results match the deterministic oracle and irrecoverably late data is visible.
6. Cross-tenant, wrong-audience, expired-token, viewer-command and unregistered-device tests are denied.
7. One trace correlates gateway, ingress, broker processing and storage; dashboard shows spool age, reconnects, lag, watermark/late events and ingestion latency.
8. Architecture, at least four ADRs, workload/benchmark method, raw results, limitations and one injected-incident postmortem are present.
9. The portfolio says **simulated robot fleet**, not robotics production or hardware-in-the-loop.

If a performance target is missed but the run is reproducible and diagnosed, publish the result. If durability, authorization, or deterministic event-time correctness fails, the milestone is not complete.

## Six-week interview cadence

- Week 1: 30-minute experience inventory and truthful gap answer.
- Week 2: 45-minute cloud-edge design.
- Week 3: 30-minute Kafka/JetStream/gRPC failure drill.
- Week 4: 45-minute event-time and backpressure deep dive.
- Week 5: 45-minute API security/multi-tenancy design.
- Week 6: 60-minute full system design plus 30-minute project defense. Record it and score requirements, invariants, capacity, failure, security, observability and trade-offs separately.

---

# Part 6 — Sixteen-week Agentic AI transition plan

This is a **standalone 160-hour sequence** if Job B becomes the primary focus immediately. It ends 5 November 2026. In the recommended hybrid plan, the same dependency order begins after the Platform MVP and reaches an early gate on 19 November and full hardening on 17 December.

Every week defaults to 6 implementation, 2.5 focused learning and 1.5 evaluation-writing/interview hours. Framework setup never displaces the evaluation dataset.

| Week/date | Learning objective and exact resource | Implementation task | Deliverable and verification | Job B/interview question unlocked |
|---|---|---|---|---|
| 1 — 17–23 Jul | CS336 lectures 1 and 10; tokenizer/context/inference limits | Define incident domain, non-goals, model interface, cost/context budgets and deterministic fake model | Design brief, risk register and tokenizer/context/cost micro-benchmark | “What makes an LLM application reliable when the model is nondeterministic?” |
| 2 — 24–30 Jul | OpenSearch hybrid docs; BEIR §§3–5 | Create 20–30 runbooks, service/change catalog and first 10 golden retrieval queries; BM25 baseline | Versioned corpus/dataset; Recall@5, MRR/nDCG and latency baseline | “How would you build and evaluate incident-document retrieval?” |
| 3 — 31 Jul–6 Aug | OpenSearch normalization/RRF, rank-eval; SBERT rerank | Dense index, tenant/service/time/ACL prefilters, fusion and top-20→5 reranker | BM25 vs dense vs hybrid vs reranked table with failure slices and actual latency | “When does hybrid retrieval beat dense-only, and what did reranking cost?” |
| 4 — 7–13 Aug | OpenAI structured output/function lifecycle; PydanticAI model/test/fallback docs | Provider-neutral typed adapter, strict ProposedStep/report schemas, TestModel/FunctionModel, retry taxonomy | Schema, refusal, truncation, malformed and semantic-invalid tests; no credentials available to model | “Why is JSON-schema validity insufficient for a safe tool call?” |
| 5 — 14–20 Aug | Anthropic Effective Agents/context articles | Explicit InvestigationState and transitions; bounded evidence loop; fixed workflow baseline | State diagram, invariants and baseline that completes without an autonomous planner | “Workflow or agent? Why is multi-agent absent?” |
| 6 — 21–27 Aug | Temporal workflow/activity/message/testing docs; LangGraph persistence/interrupt docs | Implement identical crash/resume/approval spike in Temporal and LangGraph | Framework ADR scored on durability/debug/test/observability/lock-in/ops/maturity/HITL/recovery. Temporal chosen unless spike misses core recovery within about 12 orchestration hours | “What re-executes after replay, and where must side effects live?” |
| 7 — 28 Aug–3 Sep | Temporal determinism, retry/timeout/cancellation/time-skipping | Workflow per tenant/incident; LLM/retrieval as activities; stable workflow ID; persistent state | Kill worker mid-run and resume; replay tests; cancellation reaches terminal state; workflow code performs no I/O | “What guarantees does Temporal provide, and what does it not provide?” |
| 8 — 4–10 Sep | PydanticAI deferred tools; OWASP least-privilege preview | Typed metrics/log/trace/runbook/change tools; allowlisted templates; deadlines/result bounds; evidence ledger; idempotency key | Repeating an activity yields one logical side effect/evidence record; cross-tenant and unbounded-time queries denied | “How do you make an at-least-once tool activity safe?” |
| 9 — 11–17 Sep | Temporal signals/updates; Pydantic fallback warnings | Durable approval with identity/expiry; mocked ticket creation; two model adapters; bounded routing/fallback and budget terminal states | Pause survives restart; wrong approver/expired approval denied; provider timeout falls back once without retry multiplication | “How would you resume human approval after a deploy?” |
| 10 — 18–24 Sep | Anthropic eval task/trial/grader/outcome sections; OpenAI eval best practices | Expand to 30+ seeded incident scenarios, expected signals/tool constraints/citations, difficulty/tags | Dataset schema/version and coverage matrix; no prompts tuned on hidden test split | “What is the unit of an agent evaluation, and what outcome is independent of self-report?” |
| 11 — 25 Sep–1 Oct | tau2 task/final-state design; JudgeBench/position bias | Evaluation harness, deterministic graders, three trials/case, task/tool/retrieval/citation/unsupported-claim metrics; optional calibrated judge | Baseline report with uncertainty and slices; judge order swapped and checked against at least 20 human labels | “When can an LLM judge be useful, and what must it never decide?” |
| 12 — 2–8 Oct | OTel GenAI conventions; MLflow tracing/evaluation datasets | Model/retrieval/tool/state/approval/evaluator spans; token/cost capture; prompt/workflow/eval versions; content off by default | End-to-end traces, dashboard, per-task cost/latency distribution and actual-vs-estimated usage check | “How would you detect retrieval drift versus model drift?” |
| 13 — 9–15 Oct | OWASP agent guides; AgentDojo/CaMeL concepts | Threat model; indirect-injection, data exfiltration, confused deputy, tenant bleed, loop/budget and poisoned-memory tests | 20+ adversarial cases; 100% policy/state/tenant invariants; no unauthorized tool execution | “Why can’t a system prompt enforce authorization?” |
| 14 — 16–22 Oct | Kubernetes overload/deployment docs; SRE load shedding | Container/Compose persistent stack, then K8s worker/API; admission limit, bounded queue, graceful drain, circuit breaker; provider/tool outage | Kill/restart, queue overload, timeout, partial tool, cancellation and rollback drills with recovery times | “How does an agent service degrade safely when the provider is slow?” |
| 15 — 23–29 Oct | Review only the resources implicated by failures | Freeze versions; run 30+ scenarios × 3 trials; compare fixed baseline versus bounded agent, BM25 versus hybrid/rerank, default versus fallback | Evaluation, benchmark and cost reports with raw machine-readable output, confidence/variance and regression gate | “Which complexity improved task success enough to justify itself?” |
| 16 — 30 Oct–5 Nov | No new framework study | Close defects; architecture/state/data-flow diagrams; threat model, three failure demos, postmortem, limitations; CV/GitHub/demo | Clean-checkout reproduction, tagged release, 15-minute demo, 60-minute Job B mock, truthful post-project bullets | “What did you learn that a simple RAG demo would not show?” |

## Project 2 minimum credible milestone

The calendar date is secondary; all gates must pass:

- One bounded incident domain, at least four read-only diagnostic tools, 20–30 runbooks and **30 or more** golden scenarios.
- At least **30 scenarios × 3 trials**, with task outcome, required-signal/tool selection, retrieval Recall@5/MRR or nDCG, citation correctness, unsupported claims, p50/p95 latency, tokens, cost, retry/fallback and failure-class results.
- Worker kill/restart, model timeout, tool outage, cancellation and durable approval pause/resume tests.
- An application-level idempotency ledger; replay does not repeat a logical tool effect.
- Hybrid retrieval plus reranker compared against BM25-only.
- At least 20 injection/tenant/policy attacks and **zero unauthorized tool executions**.
- OTel trace examples, prompt/workflow/eval versions and content capture off by default.
- Architecture, state diagram, framework ADR, threat model, eval/benchmark/cost reports, failure scripts, postmortem and limitations.
- Compose is sufficient for the milestone; Kubernetes hardening follows if time remains.

Predeclare targets before the full run: 100% transition/tenant/authorization invariants; Recall@5 at least 0.90 on the controlled corpus; end-to-end completion at least 0.80; citation correctness at least 0.95; unsupported claims no more than 0.05; safety pass^3 100% on curated critical attacks; explicit p95 and cost caps based on the Week-11 baseline. Treat these as hypotheses until measured. A missed quality/latency target with honest analysis is acceptable; a failed authorization, durability or reproducibility gate is not.

---

# Part 7 — Full 24-week hybrid plan

## Integrated dependency order

The hybrid plan protects the near-term Platform opportunity, then builds AI evidence. Total: **240 hours**. Planned mix is **144 implementation/experimentation hours (60%), 60 learning hours (25%), and 36 interview/writing/application hours (15%)**; individual weeks flex by about one hour while the four-week totals preserve the mix.

| Hybrid week/date | Focus and dependency | Concrete output | Hours by track | Verification/decision point |
|---|---|---|---:|---|
| 1 — 17–23 Jul | P1 scope, robot schemas/formats | Go simulator, Jazzy publisher, MCAP, envelope/ADR | 10 P1 | Apply Job A now; exact NVIDIA stretch by 19 Jul |
| 2 — 24–30 Jul | Edge durability before networking | SQLite-WAL spool and capacity/failure tests | 10 P1 | Accepted IDs survive restart; disk-full behavior explicit |
| 3 — 31 Jul–6 Aug | Transport after persistence | gRPC ACK/resume, Kafka ingress, broker ADR | 10 P1 | Five-minute disconnect/reconnect |
| 4 — 7–13 Aug | Event-time correctness before dashboards | Flink watermark/late route and ClickHouse oracle | 10 P1 | Golden aggregate/restart passes |
| 5 — 14–20 Aug | Identity/policy before public API | Register/query/command, RBAC, limits, meter | 10 P1 | Negative tenant/authz/replay suite |
| 6 — 21–27 Aug | Evidence packaging | Compose demo, OTel/dashboard, benchmark/postmortem | 10 P1 | **Milestone 1.** If durability/authz/event-time gates fail, spend next week fixing rather than adding AI scope |
| 7 — 28 Aug–3 Sep | P2 LLM contract and incident domain | Fake model, typed provider boundary, context/cost policy | 10 P2 | Model can be replaced in tests; no framework lock-in |
| 8 — 4–10 Sep | Retrieval baseline before generation | Corpus, ten initial queries, BM25/hybrid/rerank/ACL | 10 P2 | Retrieval baseline and errors published |
| 9 — 11–17 Sep | Typed outputs/tools | Schemas, validators and read-only registry skeleton | 10 P2 | Malformed/semantic-invalid/unauthorized actions rejected |
| 10 — 18–24 Sep | Explicit state and framework choice | Fixed workflow, Temporal/LangGraph spikes, ADR | 10 P2 | **Framework gate:** Temporal must prove crash/resume, approval, cancellation and replay; otherwise choose LangGraph |
| 11 — 25 Sep–1 Oct | Durable outer workflow | Temporal workflow/activities/replay tests | 10 P2 | Worker kill/resume and deterministic replay |
| 12 — 2–8 Oct | Controlled diagnostic tools | Metrics/log/trace/runbook/change, evidence/idempotency ledger | 10 P2 | Repeat activity causes one logical effect |
| 13 — 9–15 Oct | Human approval, routing and fallback | Durable approval, mock ticket, two adapters and budgets | 10 P2 | Pause/restart/resume; no retry multiplication |
| 14 — 16–22 Oct | Evaluation data before optimization | 30-case dataset, expected evidence/actions and hidden split | 10 P2 | **Dataset freeze:** coverage matrix reviewed |
| 15 — 23–29 Oct | Outcome-based harness | Deterministic graders, 3 trials, calibrated optional judge | 10 P2 | Baseline with task/retrieval/tool/citation/cost metrics |
| 16 — 30 Oct–5 Nov | AI observability | OTel/MLflow trace and cost dashboard | 10 P2 | Trace explains a failed task without prompt-content capture |
| 17 — 6–12 Nov | Security boundary | Threat model and 20+ injection/tenant/policy tests | 10 P2 | Zero unauthorized tool execution |
| 18 — 13–19 Nov | Failure/evaluation release candidate | Provider/tool/worker failures and 30×3 run | 10 P2 | **Early Milestone 2:** apply broadly only if every minimum credible gate passes; otherwise keep bridge-role search and remediate |
| 19 — 20–26 Nov | P1 delivery hardening | Helm/k3d probes/limits/HPA/PDB/network policy/rollback | 10 P1 | Lint/schema/test; rollout/rollback and HPA evidence |
| 20 — 27 Nov–3 Dec | P1 IaC/ML lifecycle/hardening | OpenTofu module, MLflow aliases/canary, SLO/failure re-run | 10 P1 | Zero-diff plan, clean destroy, canary rollback and final P1 report |
| 21 — 4–10 Dec | P2 production hardening | K8s/API-worker scaling, queue admission/drain/circuit breaker | 10 P2 | Overload and provider outage degrade safely |
| 22 — 11–17 Dec | P2 final release | Frozen full eval, benchmark/cost/threat/postmortem/docs | 10 P2 | **Full Milestone 2 and Milestone 3 evidence gate.** Tagged reproducible release |
| 23 — 18–24 Dec | Gate-dependent | If both repos pass: thin read-only P2 tools query P1 telemetry and five new incidents. Otherwise fix the failed gate | 6 integration/4 writing | No autonomous robot control, no second agent and no shared deployment required |
| 24 — 25–31 Dec | Portfolio and interview conversion | Landing READMEs, two demos, CV/LinkedIn, three mocks, application tracker | 4 polish/6 interview | **Milestone 3.** Independent reviewer can reproduce both claims |

## Decision points

1. **Week 1:** freeze scope. Low-rate typed sensor samples and artifact metadata only; no full video/LiDAR pipeline.
2. **Week 6:** if Project 1 fails correctness/security gates, fix it. A screenshot is not a milestone.
3. **Week 10:** Temporal remains selected only if the small spike demonstrates the four required recovery behaviors inside the time box. LangGraph/Postgres is the completion fallback.
4. **Week 14:** freeze an evaluation split before tuning. Add new failure cases only as a versioned next dataset.
5. **Week 18:** begin broad Senior Agentic AI applications only when the evidence gates pass. The date alone grants nothing.
6. **Week 22:** capstone integration is allowed only if both repositories already stand alone. Otherwise use Weeks 23–24 for remediation and portfolio clarity.

## Milestone dates and application lanes

| Milestone | Earliest date | What becomes credible |
|---|---:|---|
| Platform applications | **Now, 16 Jul 2026** | Existing production achievements already justify applications |
| Platform interview-conversion milestone | **27 Aug 2026** | Simulated edge/robot vocabulary, event time, explicit ACK/replay, authz and a reproducible benchmark |
| Exact NVIDIA Job B stretch | **By 19 Jul 2026** | Truthful systems/retrieval/observability application; direct Agentic AI gap disclosed |
| Dedicated-AI minimum | **5 Nov 2026** | If following Part 6 full time and every Project 2 gate passes |
| Hybrid early AI minimum | **19 Nov 2026** | Gate-dependent release candidate after 120 hours; if incomplete, continue bridge-role applications only |
| Hybrid fully hardened AI evidence | **17 Dec 2026** | Durable/evaluated/secure/observable project plus production deployment/failure evidence |
| Strong hybrid portfolio | **31 Dec 2026** | Both repos, optional thin integration, interview narratives and truthful post-project CV |

---

# Part 8 — Project specifications

## Project 1: Cloud-edge robot telemetry platform

**Repository:** robot-fleet-telemetry-platform  
**Purpose:** turn existing streaming/reliability strength into honest evidence for edge buffering, robotics data vocabulary, event-time processing, reproducible delivery, API security and ML-platform support.  
**Not a claim of:** real robot operation, full-rate video/LiDAR transport, hard real-time control, hardware-in-the-loop, autonomous control, production cloud scale or end-to-end exactly-once.

### Architecture

~~~mermaid
flowchart LR
  subgraph Edge["Simulated robot / edge"]
    ROS["ROS 2 Jazzy publisher\nJointState, IMU, small PointCloud2"]
    GEN["Go fleet generator\nhealth, pose, command ACK"]
    GW["Go edge gateway\nbatch, compress, bounded send window"]
    WAL[("SQLite WAL spool\naccepted-event boundary")]
    MCAP["MCAP chunks + manifest"]
    ROS --> GW
    GEN --> GW
    GW <--> WAL
    ROS --> MCAP
  end

  GW -->|"bidirectional gRPC\nACK + selective gaps + resume"| ING["Go cloud ingress"]
  ING -->|"ACK edge only after commit"| K[("Kafka\nraw replay log")]
  K --> FL["Flink\nevent time, watermarks, late output"]
  FL --> CH[("ClickHouse\nraw + aggregates")]
  FL --> LATE[("late-event topic/table")]
  MCAP --> OBJ[("MinIO / S3\nbulk artifacts")]
  ING --> PG[("PostgreSQL\ndevices, commands, outbox, rollout")]
  ING --> REDIS[("Redis\nrate limit / ephemeral state")]
  ING --> USE[("immutable usage ledger")]
  MLF["MLflow\nmodel versions + aliases"] --> ROUTE["deterministic canary router"]
  ROUTE --> PG
  ID["OIDC users\nmTLS or signed device identity"] --> ING
  OTEL["OpenTelemetry Collector\nPrometheus + Grafana + traces"] --- GW
  OTEL --- ING
  OTEL --- FL
~~~

### Message and time model

The Protobuf envelope should include:

- tenant_id, robot_id, boot_id, stream and monotonically increasing sequence;
- event time from the simulated robot, monotonic uptime, edge-received time and cloud-ingest time;
- schema version, payload discriminator and payload metadata;
- trace context, checksum, priority and artifact reference where applicable.

The logical event key is (tenant_id, robot_id, boot_id, stream, sequence). A reboot starts a new boot_id; sequence alone is not globally unique. Store event time and ingest time separately. Never “correct” the source timestamp in place—retain the original and record the estimated skew.

### Delivery protocol and invariants

1. **Accepted at edge** means the event transaction is committed to SQLite WAL. A gRPC write alone is not acceptance.
2. The gateway keeps a bounded in-memory send window; durable backlog stays on disk.
3. Cloud ingress sends an application ACK only after Kafka has acknowledged the record. The ACK contains the highest contiguous sequence and optional gaps.
4. Reconnect uses exponential backoff with jitter and resumes from durable ACK state.
5. Kafka and activities are at-least-once. ClickHouse materialization deduplicates the logical key; every duplicate is counted.
6. Already accepted records are never silently deleted. At capacity the gateway explicitly refuses or sheds **new** low-priority artifacts, preserves health/control classes and emits a shed event.
7. Commands have their own ID/sequence, expiry and terminal ACK. An expired or repeated command cannot execute twice in the simulator.
8. “No missing IDs accepted to the edge spool in this test” is a valid benchmark result. “Zero data loss” without a specified boundary and failure model is not.

### Component choices and trade-offs

| Component | Choice | Reason | Rejected/limited option |
|---|---|---|---|
| Cloud event log | Kafka | Strong Flink integration, partition/replay semantics and candidate depth | JetStream is compared in an ADR, not run alongside Kafka |
| Stream processor | PyFlink or Flink SQL | Direct evidence for event time/watermarks/checkpoints without adding Java | A custom Go consumer would repeat existing skill and hide the gap |
| Edge durability | SQLite WAL | Inspectable transactions, bounded local footprint and easy failure tests | In-memory retry queue cannot satisfy disconnect/restart requirement |
| Sensor artifacts | MCAP in MinIO/S3 | Robotics-native heterogeneous records, indexes, compression and replay | Do not push full video/point clouds through the low-rate event path |
| Control metadata | PostgreSQL | Strong consistency for devices, command outbox and rollout state | Redis is not the source of truth |
| Analytics | ClickHouse | Direct candidate strength and high-rate time-oriented queries | Avoid adding another time-series database |
| Rate limit | Redis token bucket/Lua | Small, testable and demonstrates algorithm/atomicity | No gateway product required |
| Usage | Immutable deduplicated events plus reconciliation | Demonstrates the durable concept with low scope | OpenMeter is a design reference, not an MVP dependency |
| Identity/policy | Local OIDC provider/JWT validation; tenant RBAC | Separates authentication from prompt/client-supplied identity | OpenFGA is optional only if relationship complexity appears |
| Model lifecycle | MLflow aliases and deterministic hash canary | Shows registry, version, lineage, rollout and rollback on CPU | KServe/GPU serving is unnecessary for the evidence goal |

### APIs

- Device registration and credential rotation.
- Telemetry query with tenant filter, time range, stream and cursor pagination.
- Command dispatch with idempotency key, expiry and audit status.
- Artifact manifest/upload reference.
- Rollout assignment and model version query.
- Usage/limit status.
- REST for developer control/query; gRPC for device ingest. WebSockets are optional for a browser live view, not the robot link.

### Security controls and threat model

- Validate issuer, signature, audience, expiry and subject; tenant comes from trusted identity, never a request body.
- Roles: viewer, operator, admin. Enforce authorization in handler and storage query.
- Device identity is separate from human identity. A device can publish only for its registered robot/tenant.
- Deny-by-default network policy, non-root containers, read-only filesystem where feasible, secret references rather than committed secrets.
- Rate limits and quotas are per tenant and endpoint class; decide and document fail-open/fail-closed behavior if Redis is unavailable.
- Bound artifact size, decompression ratio, query time range, page size and stream count.
- Audit registration, command, policy denial, quota change, model assignment and usage reconciliation.
- Negative tests: cross-tenant object ID, confused deputy, expired/wrong-audience JWT, role escalation, duplicate command, decompression bomb metadata, replayed usage event and oversized query.

### Observability and SLO hypotheses

Metrics: edge spool bytes/oldest age, send-window use, ACK gap, reconnects, explicit shed reason/count, gRPC status, Kafka producer/consumer lag, Flink busy/backpressured time, watermark lag, late events, logical duplicates, ClickHouse insert/query latency, command latency, rate-limit denials and usage reconciliation difference.

Trace context crosses gRPC → Kafka headers → Flink/sink. Structured logs include tenant hash, robot/boot/sequence and trace ID but no secrets.

Predeclared hypotheses for the hardening run:

- Connected accepted-edge-to-raw-store latency: p95 under 2 seconds and p99 under 5 seconds.
- Five-minute outage backlog drains within 10 minutes while live traffic continues.
- Gateway RSS no more than 256 MiB and in-memory queue no more than 64 MiB during disconnect.
- Gateway stream resumes within 30 seconds of network return; processor within 60 seconds; broker restart recovery within 120 seconds.
- Zero missing IDs already accepted to the spool under the tested crash/network scenarios; zero duplicate logical aggregates after idempotent materialization.
- Query p95 under 250 ms on the published 24-hour/200-robot dataset.
- Availability/latency SLOs use multi-window burn alerts; exact objective is set from the benchmark rather than invented in advance.

These are targets, not CV bullets. Publish misses and analysis.

### Benchmark and failure matrix

| Test | Load/fault | Measure | Pass criterion |
|---|---|---|---|
| MVP steady | 100 robots × 5 events/s, 15 min | p50/p95/p99, CPU/RSS, lag, duplicates | Clean run, bounded resources and fully reconciled accepted IDs |
| Hardening steady | 200 × 5 Hz, 20 min; then 500 × 5 Hz, 15 min | Same plus storage growth/cost | Actual bottleneck and saturation point explained |
| Burst | 5,000 events/s for 1 min | queue depth, backpressure, shed/recovery | No unbounded memory or silent loss |
| Disconnect | 5 min network cut | spool age/bytes, recovery, missing/duplicate IDs | Bounds and drain objective above |
| Disorder | 10% up to 5s late; 1% beyond | watermark/late route/oracle equality | In-bound aggregate exact; later IDs visible |
| Process/broker faults | Kill gateway, ingress, Kafka, Flink and sink separately | RTO, duplicates, gaps and drain | Each recovery documented; no unsupported exactly-once claim |
| Full disk | Fill spool to configured 512 MiB | explicit refusal/shedding and priority | Already accepted events preserved; new loss visible |
| Schema | Compatible optional field and intentional breaking change | reader compatibility/CI | Optional passes; breaking change rejected |
| Security | Cross-tenant/role/token/device abuse suite | denials and audit | All critical negative tests denied |
| Meter | 10% retry/replay traffic | raw events versus aggregate | Exact reconciliation by usage ID |
| Model rollout | Deliberately regressed candidate at 10% | health metric and rollback time | Threshold trips and champion restored within declared target |

### Deployment and disaster recovery

- Compose for development and the Week-6 milestone; k3d/kind plus Helm during hardening.
- Probes reflect actual dependencies: startup for initialization, readiness for serving, liveness only for unrecoverable stuck state.
- Requests/limits, graceful termination/drain, PDB, HPA using backlog/custom metric, topology spread and NetworkPolicy.
- OpenTofu module demonstrates provider pinning, state encryption, plan/apply/destroy, zero-diff second plan and clean teardown. Cloud run is optional and capped at USD 25.
- Raw Kafka retention plus MCAP objects are recovery sources; derived ClickHouse aggregates can be deleted and reproduced with matching checksums. Document metadata backup, object integrity, replay order, RPO/RTO and the limitations of a single-laptop lab.

### Required repository evidence

Source and tests; one-command local demo; architecture diagram; six to eight concise ADRs; threat model; schema compatibility suite; load/failure scripts; raw and summarized benchmark results; dashboards and trace examples; SLO/alert rules; incident timeline/postmortem; Docker/Helm/OpenTofu; deployment/DR guide; cost note; demo video/script; and explicit limitations/future work.

### Resource-to-component map

| Component | Primary resources |
|---|---|
| Event time/replay | Streaming Systems, Dataflow Model, Flink docs, DDIA |
| Store-forward | Greengrass Stream Manager patterns, DDIA encoding, gRPC guides |
| Robotics formats/time | ROS 2 packet, MCAP |
| Broker decision | Kafka design, JetStream concepts |
| Delivery | gRPC, Helm, OpenTofu, Kubernetes workload docs |
| Security/metering | RFC 9700/OIDC/OWASP API; OpenMeter only as reference |
| Reliability | SRE Workbook/overload guidance, OTel conventions |
| ML support | MLflow Registry workflow |

## Project 2: Production-grade incident investigation agent

**Repository:** incident-investigation-agent  
**Purpose:** convert observability, distributed workflow and search experience into direct evidence for LLM tools, durable state, RAG, evaluation, security and AI observability.  
**Not a generic chatbot, autonomous operator, unrestricted shell, notebook demo or multi-agent showcase.**

### Selected architecture

~~~mermaid
flowchart LR
  U["Incident request\nsigned tenant identity"] --> API["FastAPI\nvalidate + admit"]
  API --> T["Temporal workflow\none incident / tenant"]
  T --> SM["Explicit typed state machine\nbudgets + invariants"]
  SM --> M["PydanticAI model adapter\nfake + provider A/B"]
  SM --> R["OpenSearch\nBM25 + dense + ACL + rerank"]
  SM --> AUTH["Deterministic policy engine\ntool/resource authorization"]
  AUTH --> TOOLS["Read-only adapters\nmetrics, logs, traces,\nrunbooks/catalog/changes"]
  AUTH --> APPROVE["Durable human approval\nmock ticket only"]
  TOOLS --> E[("PostgreSQL evidence,\nidempotency + audit ledger")]
  R --> E
  E --> REP["Evidence-linked report\ncitation validator"]
  T --> Q["Temporal task queue\nbounded workers"]
  O["OTel GenAI spans\nMLflow trace/eval view"] --- API
  O --- T
  O --- M
  O --- R
  O --- TOOLS
~~~

Use Temporal as the durable outer engine, an explicit Pydantic InvestigationState, PydanticAI inside activities for typed provider/model/tool results, direct OpenSearch retrieval, PostgreSQL for evidence/idempotency/audit and OTel instrumentation. The architecture is deliberately framework-light at the decision and policy boundaries.

### State machine

~~~mermaid
stateDiagram-v2
  [*] --> Received
  Received --> Validate
  Validate --> Retrieve
  Retrieve --> Plan
  Plan --> Authorize
  Authorize --> Execute: allowed read-only action
  Authorize --> AwaitApproval: consequential mocked action
  Authorize --> PolicyBlocked: denied
  AwaitApproval --> Execute: valid approval
  AwaitApproval --> Cancelled: reject / expiry / cancel
  Execute --> IngestEvidence
  IngestEvidence --> Assess
  Assess --> Retrieve: evidence insufficient and budgets remain
  Assess --> DraftReport: evidence sufficient
  Assess --> BudgetExceeded: step/time/token/cost cap
  DraftReport --> ValidateCitations
  ValidateCitations --> HumanReview
  HumanReview --> Finalize: accepted
  HumanReview --> Retrieve: bounded revision
  Finalize --> Complete
  Complete --> [*]
  PolicyBlocked --> [*]
  BudgetExceeded --> [*]
  Cancelled --> [*]
~~~

Terminal failure also includes FAILED with a classified reason. The model may propose a typed step with tool, arguments, evidence sought and rationale. Deterministic code—not prompt text—validates the transition, identity, permission, resource, rate/cost budget and allowed tool before execution.

### Framework comparison

Scores are 1–5. Weighted total: durability 15%; debug, test, observability, low lock-in, operational simplicity, maturity, recovery and production suitability 10% each; human approval 5%.

| Approach | Durability | Debug | Test | Observability | Low lock-in | Ops simplicity | Maturity | HITL | Recovery | Suitability | Weighted / judgment |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Temporal + explicit state + PydanticAI activities** | 5 | 4.5 | 5 | 4.5 | 4 | 2.5 | 5 | 4.5 | 5 | 5 | **90.5** — selected; strongest durable/recovery evidence, higher operational/determinism cost |
| **LangGraph + PostgreSQL checkpointer** | 4 | 5 | 4 | 4 | 3 | 4 | 4 | 5 | 4 | 4.5 | **82** — completion fallback; fast graph/HITL/debug, more ecosystem coupling |
| **Custom Pydantic/Postgres state machine + queue** | 3 | 4.5 | 4.5 | 4 | 5 | 3 | 4 | 4 | 3 | 4 | **77** — transparent but rebuilds timers, leases, replay, cancellation and operator tooling |
| **PydanticAI/Pydantic Graph without durable engine** | 2 | 4.5 | 5 | 4.5 | 4 | 5 | 3.5 | 4 | 2 | 3.5 | **74** — excellent types/test doubles; durability still delegated |
| **LlamaIndex Workflows** | 3 | 4 | 4 | 4 | 2.5 | 3.5 | 4 | 4.5 | 3 | 3.5 | **70.5** — capable retrieval/workflow system but broader dependency and weaker durability story |

Haystack is a useful modular RAG reference, not an outer workflow engine. Semantic Kernel adds unnecessary surface for a Python-first time box. Multiple agents are rejected unless a controlled evaluation later demonstrates a material advantage over the explicit single workflow.

**Decision gate:** after roughly 12 focused orchestration hours, Temporal must demonstrate worker crash/resume, durable approval, cancellation and replay tests. If not, switch to LangGraph/Postgres and preserve evaluation/security time.

### Durable execution semantics

- Stable workflow ID: tenant_id:incident_id; versioned InvestigationState.
- Workflow code is deterministic. LLM, retrieval, tools and clock/network I/O are activities.
- Activities are at-least-once. Every logical tool call uses (workflow_id, logical_tool_call_id) and a PostgreSQL ledger.
- Retry only classified transient failures. Never layer provider SDK, activity and application retries blindly.
- Timeouts exist at connection, request, activity, workflow and human-approval levels.
- Cancellation propagates; worker drain does not abandon an unrecorded external effect.
- Workflow/version migration and rollback are tested on saved histories.

### Tools and authorization

Initial read-only tools:

1. Metrics query against seeded Prometheus-compatible data.
2. Log query against seeded ClickHouse-style data.
3. Trace lookup against seeded Jaeger/OTel trace data.
4. Runbook, service-catalog and change-history retrieval.
5. Mock ticket creation only after durable approval; it is the only side-effecting demonstration.

Every adapter has typed input/output; allowlisted templates; bounded time range/result size; tenant/service scope; deadline/retry/circuit breaker; immutable response hash/provenance; read-only credentials outside model context; idempotency key; and audit event. Retrieved documents, logs, tickets and tool output are untrusted **data**, never instructions. There is no shell.

### Retrieval and citations

- Index 20–30 incident runbooks plus service/catalog/change documents with immutable document/chunk/version IDs.
- Apply tenant, service, time and ACL filters **before** ranking.
- Compare BM25, dense, hybrid fusion and top-20→5 cross-encoder rerank.
- Version chunking and embeddings; preserve source boundaries and headings.
- A citation resolver verifies that every report citation exists, is authorized and supports the referenced evidence span.
- Report Recall@5, MRR/nDCG, reranker latency, citation precision/correctness and failures by incident type. Existing semantic-search experience is the starting point, not proof that this work is already done.

### Model, context and memory

- Provider-neutral interface with strict typed outputs, deterministic fake and two real adapters only if budget permits.
- Cheap/default route; escalate only on a predefined complexity/evidence rule. Fallback only for classified retryable or semantic failures.
- Record model/provider/version, route reason, retries/fallbacks, input/output tokens, latency and estimated/actual cost.
- Context contains bounded task, trusted policy, typed tool definitions and selected evidence. Truncation/summarization has provenance.
- “Memory” in MVP means durable workflow state, immutable evidence ledger, retrieval corpus and bounded context summary. Do not build self-written long-term memory.
- A post-MVP experiment may index approved incident summaries with tenant namespace, provenance, TTL and deletion; keep it only if eval improves.

### Evaluation design

Create at least 30 seeded scenarios across bad deployment, dependency outage, queue lag, storage saturation, latency, error rate, authentication failure, clock skew and ambiguous/no-root-cause cases. Seed known metrics, logs, traces and changes so deterministic expected signals exist.

| Layer | Primary metrics | Deterministic first? |
|---|---|---|
| State/policy | valid transitions, terminal state, loop/budget, tenant/tool authorization | Yes |
| Tool use | required tool/signal, argument validity, scope, idempotent effect | Yes |
| Retrieval | Recall@5, MRR/nDCG, ACL leakage, rerank latency | Yes |
| Evidence/report | citation existence/correctness, required evidence, unsupported claim | Mostly; human/model rubric only for residual prose quality |
| Task | outcome completion, correct failure classification, pass@1 and repeated-run reliability/pass^k | Yes where seeded |
| Operations | p50/p95 latency, tokens, cost, retry/fallback/tool errors, queue time | Yes |
| Safety | injection success, unauthorized execution, cross-tenant disclosure, budget bypass | Yes |

Run three trials per scenario. Use deterministic graders before model graders. Calibrate any LLM judge on at least 20 human-scored examples, blind identity/order, swap answer order and report disagreement/variance. A judge never decides authorization, citation existence, tool success or database final state.

Compare:

- fixed deterministic workflow baseline versus bounded model-planned loop;
- BM25 versus hybrid versus hybrid+rerank;
- default route versus fallback;
- clean versus provider/tool failure;
- before versus after each prompt/workflow/model version.

### AI observability

Emit spans/events for workflow/state transition, model request, retrieval/rerank, authorization, tool execution, approval, evaluator and final task. Include model/provider, prompt/workflow/eval/dataset version, tokens, duration, queue time, retry/fallback, estimated cost, hashed tenant and result/failure class.

Prompt, document and tool content capture is disabled by default because it can contain sensitive data. Wrap the evolving OTel GenAI semantic attributes behind one internal telemetry module and pin a schema version. MLflow is a local trace/evaluation view, not the workflow engine.

Dashboard: task success and failure class; p50/p95 end-to-end/model/retrieval/tool latency; tokens/cost; retries/fallback; retrieval/citation quality; unsafe attempts/denials; queue/backlog; workflow age; prompt/workflow/model/eval version.

### Security and adversarial suite

Threats include indirect prompt injection in runbooks/logs/tickets; malicious tool arguments; confused deputy; credential request; cross-tenant retrieval/cache; unbounded loop; approval forgery/replay; sensitive trace content; poisoned memory; output rendered as executable markup; model/provider data retention; and denial-of-wallet.

Controls: data/control separation, prompt-independent policy, least privilege, read-only default, resource allowlists, signed identity, approval identity/expiry, bounded steps/time/tokens/cost, output encoding/validation, audit/evidence hashes, tenant-isolated indexes/keys, secrets never in prompts, content capture off and kill switch.

The 20+ attack cases must include direct and indirect instruction attacks, Unicode/obfuscation, tool exfiltration, cross-tenant IDs, long-result exhaustion, recursive loop, fake approval and malicious citation.

### Reliability and failure injection

Kill worker during model, tool and approval states; restart API/worker; make provider time out/rate-limit/malformed; make one tool slow/partial/unavailable; corrupt a retrieval document; overload task queue; cancel at each state; deploy a version change; and replay saved history. For each, record expected state, retry/fallback, user-visible status, RTO, duplicate effect and trace.

SLO hypotheses are set after baseline: admission success, time to first evidence, completion within a task-class deadline, authorization invariant, trace completeness and maximum cost/task. Model-quality SLOs use a frozen evaluation slice, not live subjective ratings.

### Acceptance gates

The minimum credible gates in Part 6 are binding. Additional hardening targets:

- 100% transition, tenant and authorization invariants across all tests.
- Zero critical unauthorized tool effects and zero cross-tenant retrieved chunks.
- Recall@5 at least 0.90, end-to-end completion at least 0.80, citation correctness at least 0.95 and unsupported claims no more than 0.05 on the controlled test version.
- Safety pass^3 100% for critical curated attacks.
- All 30+ scenarios run three times with raw output and version metadata.
- Worker crash, model outage, tool outage, cancellation, approval pause/resume and workflow replay are reproducible from scripts.
- Cost cap is predeclared; stop rather than silently exceed it.

Again, quality thresholds are hypotheses. Publish a miss honestly. Authorization/durability/reproducibility failures block completion.

### Required repository evidence

Source/tests; Compose and optional Kubernetes deployment; architecture/state/data-flow diagrams; framework and model/retrieval ADRs; versioned corpus/eval dataset; raw eval/benchmark/cost output and reports; OTel traces/dashboard; threat model and attack suite; failure scripts; three demo incidents; postmortem; README/deployment guide; limitations and future experiments.

### Resource-to-component map

| Component | Primary resources |
|---|---|
| LLM/context/tool contract | CS336 selections, Anthropic effective agents/context, OpenAI function/structured output docs |
| Durable state/HITL | Temporal docs/SDK, LangGraph comparison, PydanticAI integration |
| Retrieval/rerank | OpenSearch docs, BEIR, Sentence Transformers |
| Evaluation | Anthropic eval guide, OpenAI eval docs, tau2/tau3 methods, JudgeBench |
| Observability | OTel GenAI conventions, MLflow GenAI tracing |
| Security | OWASP Agentic Top 10/cheat sheet, AgentDojo, CaMeL |
| Deployment/reliability | SRE Workbook, Kubernetes docs, DDIA |

### Cost

Run Temporal, Postgres, OpenSearch and MLflow locally. Use the fake model for most tests. Budget USD 20–60 total for hosted-model development/evaluation; cache only where it does not invalidate repeated-trial measurement, set per-run/monthly hard limits and publish actual provider/model/token pricing at test time. A small local model is optional, not required.

## Optional capstone: observable AI operations for the simulated fleet

The capstone is worthwhile only as a **thin read-only adapter** after both repositories pass independently. In Week 23:

- expose Project 1 fleet health, ClickHouse telemetry, traces, change history and runbooks as five Project 2 read-only tools;
- add five seeded incidents: reconnect storm, clock-skew/late-data surge, Kafka lag, bad model canary and cross-tenant query attempt;
- run the existing authorization/evaluation/trace harness and publish the delta;
- require approval for a mocked remediation ticket only.

Do **not** merge repositories, deploy another agent, add autonomous command/control, change Project 1’s data plane, or weaken either independent README. If either project has an unmet durability/security/evaluation gate, skip the capstone and fix that gate. Two finished systems are stronger than one unfinished “robot AI platform.”

---

# Part 9 — Interview preparation

## How to answer at senior level

Use this order in system design: requirements and non-goals → workload/SLO → invariants → high-level design → data/partition model → failure behavior → security/tenancy → observability/operations → cost and trade-offs. Never begin by listing products.

For experience questions, distinguish “I did,” “my team did,” and “I would do.” For portfolio questions, distinguish measured result, test boundary and target. If production details are confidential, state the abstraction without inventing a number.

## Job A interview-area map

| Area | Core concepts and likely question | Strong-answer outline | Candidate evidence | Missing evidence and practice | Resource |
|---|---|---|---|---|---|
| Distributed correctness | Delivery boundary, ordering, idempotency, replication; “Can you guarantee exactly once?” | Define effect/invariant and each boundary; at-least-once transport + idempotent sink/outbox; name crash windows and reconciliation | Kafka manual offsets, virtual-currency idempotency/outbox, JetStream ACKs | Edge ACK/replay; draw five crash timelines and run duplicate tests | DDIA Ch. 9/12; Streaming Systems Ch. 5 |
| Edge/cloud | Intermittent links, local durability, sync and full disk; “Design upload from 10k robots” | Workload/priorities; WAL acceptance; bounded window; ACK/gap/resume; clock/boot IDs; capacity/eviction; reconnect jitter | Queue/retry/delivery experience transfers | No real edge; defend simulated spool and state limitations | Greengrass patterns; gRPC guides |
| Streaming/event time | Watermarks, windows, late data, backpressure; “Compute fleet health despite skew” | Separate event/ingest time; watermark policy, idle partitions, late route, checkpoint/replay; correctness oracle | Kafka/CDC/ClickHouse strong | Flink/event-time new; explain Project 1 test | Streaming Systems Ch. 2/3/7; Flink |
| Broker/transport | Kafka vs NATS; gRPC vs WebSockets; partitioning and recovery | Select by replay/integration/latency/ops; robot key ordering; avoid dual brokers; flow control is not durability | Kafka, NATS/JetStream, gRPC, Socket.io | Cloud-edge stream semantics | Kafka/NATS/gRPC docs and ADR |
| Storage/data | Postgres/Redis/ClickHouse/object store; schema evolution | Assign source-of-truth/analytics/ephemeral/blob roles; access paths, retention, partition/order, compatibility and replay | Direct strong evidence in all but object store | MCAP/object lifecycle; practice a 24-hour capacity estimate | DDIA Ch. 5; MCAP |
| Kubernetes/delivery | Probes, limits, rollout, HPA, PDB, Helm/IaC; “Why didn’t HPA help?” | Correct readiness/startup/liveness; queue metric; stabilization; drain; rollback; state/IaC lifecycle | Kubernetes explicit, depth unknown | Helm/OpenTofu/Docker claims unavailable until project | K8s, Helm, OpenTofu docs |
| API platform/security | OIDC, device identity, RBAC, rate, quota, metering | Separate authn/authz; trusted tenant context; per-resource check; token bucket vs quota; immutable usage/reconciliation | Multi-tenant SaaS and tier management adjacent | Direct implementation unknown | RFC 9700/OIDC/OWASP API |
| Reliability/performance | SLI/SLO, tail latency, capacity, alerts, incidents | User journey; histogram/tail; saturation; error budget; load shed; failure test; postmortem action | 15 TB/month observability and latency/cost optimization | Explicit SLO practice unknown | SRE Workbook/overload |
| Robotics/ML support | ROS QoS/time/formats, model registry/canary, training lineage | Working vocabulary; data manifest/provenance; immutable version; deterministic rollout/rollback; admit hardware limits | Data pipelines transfer | No direct robotics/MLOps | ROS 2/MCAP and MLflow |

## Job B interview-area map

| Area | Core concepts and likely question | Strong-answer outline | Candidate evidence | Missing evidence and practice | Resource |
|---|---|---|---|---|---|
| AI system architecture | LLM/retrieval/tools/state/feedback; “Design an incident agent” | Scope and measurable outcome; explicit state; trusted policy; evidence loop; bounded budgets; approval; failure/trace/eval | Distributed backend/observability directly transferable | Direct AI evidence after Project 2 only | Anthropic Effective Agents; Project 2 ADR |
| Retrieval/RAG | Chunking, hybrid, rerank, ACL, citations, eval | Corpus/version/query set; prefilter ACL; BM25/dense/fusion/rerank; Recall@k/MRR; citation/unsupported-claim checks | OpenSearch hybrid search and measured relevance | Generated-answer RAG absent now | OpenSearch, BEIR, SBERT |
| Structured tools | Schema, validation, permissions, idempotency | Model proposes typed intent; app validates semantics/policy/resource; credential outside model; audit; logical call ID | APIs/idempotency/outbox | Model-controlled tools absent now | OpenAI structured outputs; OWASP |
| Durable workflow | State machine, workflow/activity, replay, timeout, cancellation, HITL/versioning | Deterministic workflow; nondeterministic activity; retry taxonomy; signal/approval; idempotent effect; saved-history replay | Ordered queues/retry semantics transfer | Temporal evidence after project | Temporal/PydanticAI/LangGraph |
| Evaluation | Dataset, outcome, trials, graders, uncertainty, regression | Representative/versioned tasks; deterministic first; repeated trials; task/tool/retrieval/citation/safety/cost; judge calibration | Measurement discipline transfers | No current AI eval evidence | Anthropic evals; OpenAI evals; tau2 |
| AI observability/reliability | Model/retrieval/tool spans, tokens/cost, provider outage | Trace every state/dependency; version metadata; content privacy; SLO by outcome; fallback/load shed; failure class | Exceptional OTel/observability evidence | AI-specific semantics absent now | OTel GenAI; MLflow tracing |
| Security/tenancy | Indirect injection, confused deputy, tenant bleed, denial-of-wallet | Treat content as data; policy outside prompt; least privilege/read-only; identity propagation; allowlist; audit; budgets/approval | Multi-tenant isolation adjacent | Agent attack suite absent now | OWASP, AgentDojo, CaMeL |
| Model/context/routing | Tokenization, context budget, fallback, retries, latency/cost | Context sources/provenance/truncation; cheap default; explicit escalation; avoid retry multiplication; measure quality/cost | Performance/cost experience transfers | LLM mechanics new | CS336; PydanticAI model docs |
| Memory/multi-agent | Short/long-term state and coordination trade-offs | Persist business state/evidence, not hidden prompt state; provenance/TTL/deletion; add agents only after controlled baseline benefit | Data modeling/workflows transfer | Direct evidence absent | Anthropic context engineering |
| Productionization | API/queue/K8s, overload, version/rollback, incident | Admission, bounded queue, deadlines, drain, provider circuit, evaluation gate, shadow/canary, rollback and postmortem | Strong production systems evidence | AI production artifact pending | SRE/K8s plus Project 2 |

## Job A: 12 system-design prompts

For each, do a 35-minute design and 10-minute critique.

1. **Fleet telemetry for 100,000 robots:** cover workload classes, edge acceptance, partition key, broker/storage tiers, backpressure, tenant isolation, replay and SLO.
2. **Reliable command channel:** cover command ID/sequence/expiry, outbox, offline robot, acknowledgement state, duplicate suppression, emergency priority and audit.
3. **Intermittent factory connectivity:** cover bounded spool, priority, full disk, ACK/resume, bandwidth scheduling, reconnect storm and reconciliation.
4. **Video/LiDAR/audio artifact platform:** separate live metadata from bulk objects; chunking/checksum, resumable upload, index/catalog, retention, bandwidth and privacy.
5. **Event-time fleet-health stream:** timestamps/skew, watermark/idle sources, window/trigger, late route, state/checkpoint, oracle and correction.
6. **External robotics developer API:** registration, keys/OIDC, RBAC, quota/meter, idempotency, pagination/versioning, SDK/error model and abuse controls.
7. **Multi-region telemetry service:** ownership/affinity, replication, RPO/RTO, command consistency, regional outage, routing and cost.
8. **Replay and disaster recovery:** raw source, immutable artifacts, schema/version, derived rebuild, checkpoint/savepoint, verification checksum and operator runbook.
9. **Model registry and 10% policy rollout:** immutable artifact/signature, lineage, robot compatibility, deterministic cohort, health gate, rollback and audit.
10. **Simulation/test platform:** deterministic clock/faults, scenario/version, record/replay, parity limits, CI capacity and what true HIL would add.
11. **Quota/metering platform:** token bucket versus fixed budget, tenant tiers, durable usage event, dedup/reconciliation, late event and billing boundary.
12. **Telemetry observability/capacity:** SLIs, async trace, lag/watermark/spool age, alert symptoms, load model, saturation, load shed and game day.

## Job B: 12 system-design prompts

1. **Incident-investigation agent:** measurable task, evidence sources, explicit state, tools/policy, durable execution, eval, trace and human review.
2. **Secure multi-tenant RAG:** identity/ACL prefilter, chunk/version, hybrid/rerank, citations, cache isolation, deletion and retrieval evaluation.
3. **Durable tool workflow:** workflow/activity boundary, stable ID, idempotency ledger, retries/timeouts, cancellation, approval and replay/versioning.
4. **Agent evaluation platform:** dataset/version, task/trial/outcome, deterministic/model/human graders, repeated reliability, slices, CI and cost.
5. **Multi-provider model gateway:** capability/routing policy, context limits, rate/budget, retries/fallback, circuit, usage reconciliation and privacy.
6. **Evidence memory for engineering agents:** durable task state versus long-term memory, provenance, tenant namespace, TTL/deletion, poisoning and measured benefit.
7. **Agent platform for 1,000 tenants:** API/admission, queues/workers, isolation, tool credentials, quotas, trace storage, noisy neighbor and SLO.
8. **AI observability service:** semantic spans, high-volume storage/index, content privacy, tokens/cost, quality-version joins, sampling and incident queries.
9. **Prompt-injection-resistant tool agent:** trusted control/untrusted data, capabilities, allowlists, read-only default, output validation, approval, attack harness and kill switch.
10. **Prototype-to-production migration:** baseline behavior, contracts, state/durability, evaluation, security, deployment, canary, rollback, operator ownership and de-scoping.
11. **Retrieval/model change rollout:** frozen dataset, offline compare, slice regression, shadow/canary, live proxy metrics, stop condition and reproducibility.
12. **Single versus multi-agent architecture:** task decomposition, communication/error surface, latency/cost, independent evaluation and decision rule to reject added agents.

## Ten debugging scenarios

| Scenario | Investigation path a strong answer should show |
|---|---|
| 1. Kafka consumer lag rises while CPU is low | Confirm producer/partition distribution, blocked sink/I/O, consumer rebalance, fetch/batch settings, hot key, broker/storage latency; correlate lag with trace and queue time before scaling |
| 2. Average latency is flat but p99 triples | Check histograms by endpoint/tenant/partition, queueing/saturation, GC/I/O/DNS/TLS/retries, coordinated omission and downstream tail; avoid “add replicas” before cause |
| 3. Flink windows stop closing after one robot group disconnects | Inspect idle partition/watermark alignment, source timestamp/skew, backpressure/checkpoint; mark idle inputs carefully and retain late-data visibility |
| 4. A robot executes a command twice after reconnect | Trace command ID, outbox publish, ACK crash window, expiry and simulator ledger; make execution idempotent rather than trusting delivery once |
| 5. Reconnect storm overloads ingress | Jitter/backoff, admission and per-fleet rollout, edge send windows, priority, load shed, broker/DB limits and recovery SLO |
| 6. RAG answer quality drops after an embedding update | Freeze versions; separate retrieval from generation; compare query slices/Recall@k/rank distribution/chunk IDs/ACL/reranker; roll back via evaluated gate |
| 7. Temporal retries create two tickets | Activity is at-least-once; inspect logical call ID/ledger and ambiguous timeout; reconcile external result before retry; never claim workflow durability equals effect exactly once |
| 8. Provider timeout causes latency/cost explosion | Find nested SDK/activity/app retries, deadlines and fallback chain; cap attempts/budget, classify errors, circuit-break and expose partial status |
| 9. A runbook injection asks the agent to query another tenant | Treat content as untrusted; policy ignores document instruction; prefilter identity, validate tool resource, deny/audit and add fixture to security regression |
| 10. Token cost doubles with no task-success gain | Break down context/tool results/retries/planner loops/model route; compare versions and truncate/compress evidence with provenance; keep only changes improving frozen eval |

## Ten behavioral questions grounded in supplied evidence

Do not invent team size, title, incident severity or personal contribution. Fill those from memory before the interview.

| Question | Best truthful anchor | STAR outline to prepare |
|---|---|---|
| 1. Tell me about your highest-impact architecture change | Loki→ClickHouse plus hybrid trace storage | Situation: >15 TB/month and pain; Task: storage/query redesign; Action: selection/migration/validation/rollout; Result: ~75% latency and ~40% storage-cost reduction; trade-off/lesson |
| 2. Describe a reliability migration with risk | NATS Core→JetStream | Critical-stream loss risk; persistence/ACK design and migration safety; observed zero message loss for critical streams; state measurement boundary |
| 3. Tell me about correctness under retries | Virtual currency service | Monetary invariant; pessimistic lock, idempotency and outbox; failure windows/tests; avoid inventing financial scale |
| 4. Describe a difficult data migration | Go Kafka consumers moving millions of records | Batch/concurrency/manual offset design; loss/duplicate verification; rollback/monitoring; result |
| 5. How did you separate transactional and analytical workloads? | CDC→ClickHouse | OLTP contention/reporting need; CDC/schema/replay design; >50M records/month; ~60% reporting improvement |
| 6. Tell me about a performance bottleneck | OpenSearch async queue-driven reindex | Baseline/bottleneck; batching/concurrency/backpressure; ~10x result; consistency/operational trade-off |
| 7. How did you improve product quality using search? | Hybrid keyword/semantic candidate-job matching | Relevance problem and measurement; hybrid/ranking change; >50k daily searches and ~35% match-accuracy improvement; define metric precisely in interview |
| 8. Describe a high-throughput system | Distributed worker aggregation | Workload and partition/worker model; backpressure/correctness; >5M records under three minutes; bottleneck/lesson |
| 9. Describe multi-tenant platform ownership | SaaS >1,000 tenants | Onboarding/isolation/feature tiers; noisy-neighbor/security/operations choices; actual scope and result |
| 10. Tell me about ordered asynchronous workflows | Azure Service Bus workflow | Ordering requirement; sessions/keys if actually used, DLQ/retries and recovery; never name a mechanism not in the profile—clarify actual design |

## Ten project deep-dive questions

1. **Observability migration:** What workload measurements ruled out tuning Loki and justified ClickHouse? Show selection criteria, migration safety, query/retention design and cost calculation.
2. **Observability migration:** Which query-latency and storage-cost measurements produced the 75%/40% figures, and over what window? Bring the precise definition.
3. **JetStream migration:** What did “zero message loss” mean, how was it observed, and which crash/network scenarios were or were not tested?
4. **Kafka migration:** Where could a crash occur between database write and offset commit, and how did the implementation detect/prevent logical duplication?
5. **CDC pipeline:** How did schema change, initial snapshot, ordering, deletes and replay work? If a mechanism is unknown/unsupported, say so.
6. **OpenSearch:** How was “35% match accuracy” defined, what baseline/data set was used and how did latency/cost change?
7. **Multi-tenancy:** Which boundaries enforced isolation and how were onboarding/feature-tier changes kept consistent?
8. **Project 1, after milestone:** Why is cloud ACK after Kafka commit, and what failure remains between sink write and checkpoint?
9. **Project 1, after milestone:** How did watermark choice affect late-event correction, state and user-visible latency? Show golden data and actual plot.
10. **Project 2, after milestone:** Which framework/agent complexity improved a frozen metric, what failed under replay/injection and what was removed?

## Ten production-incident and trade-off questions

| Prompt | What a strong answer must make explicit |
|---|---|
| 1. Product asks for exactly-once telemetry | Which effect/invariant matters; end-to-end boundaries; at-least-once + idempotency/reconciliation; cost and residual failure |
| 2. Disk is full at an offline robot | Accepted-data promise; priorities; explicit refusal/shedding; operator signal; recovery and capacity policy |
| 3. Command traffic and bulk telemetry compete | Separate priority/resources, admission and deadlines; preserve safety/control, shed artifacts; prevent starvation and audit |
| 4. Redis rate-limit store is unavailable | Threat/business consequence; fail-open/closed by endpoint, local emergency bounds, reconciliation and clear degraded mode |
| 5. Region fails during a command | Robot/fleet ownership, command state consistency, expiry/fencing, RPO/RTO and why telemetry can tolerate different consistency |
| 6. Better model improves quality but doubles cost/p95 | Task-class/SLO/budget, route selectively, offline repeated eval, canary/stop rule and whether gain justifies complexity |
| 7. All model providers fail | Queue/admission, bounded wait, partial evidence mode, fallback/circuit, user status, recovery and no retry storm |
| 8. Human and LLM judge disagree | Ground truth limits, rubric/calibration/blinding/order, deterministic outcomes, uncertainty and escalation—not majority vote by models |
| 9. Model proposes an unauthorized but plausible action | Deterministic denial, no credential exposure, audit/alert, safe terminal state, adversarial regression and root-cause classification |
| 10. Deadline threatens the capstone | Protect acceptance gates, cut integration/multi-agent/extra tools, publish limitations; finished independent projects win |

## Mock-interview schedule and scorecard

| When | Mock | Evidence required |
|---|---|---|
| Platform Weeks 2, 4, 6 | Edge failure; event-time; full platform design | Diagram, workload, three invariants, capacity math and a failure timeline |
| AI Weeks 4, 8, 12, 16 | RAG; durable tools; eval/security; full AI system | Dataset/metric, state diagram, authorization boundary, trace and one measured trade-off |
| Hybrid Weeks 18, 22, 24 | Job B release defense; both project defenses; final loop | Tagged evidence, actual misses, 30-second intro, two-minute story and six behavioral STARs |

Use a 0–2 score for each: requirements/non-goals, capacity, invariants, data model, failure/recovery, security/tenancy, observability/SLO, cost, trade-offs, communication and evidence honesty. A mock “passes” at 16/20 with no zero in invariants, failure or security. Record one improvement action, then repeat the same prompt a week later.

---

# Part 10 — CV, LinkedIn, GitHub and application strategy

## Truth ledger

| Label | Claims that belong here |
|---|---|
| **Supported now** | Senior Software Engineer; approximately seven years; Go/Python/Node.js; distributed/event-driven systems; Kafka/NATS/JetStream/Azure Service Bus; gRPC; Kubernetes; PostgreSQL/Redis/ClickHouse/OpenSearch; multi-tenant SaaS; CDC; hybrid semantic search; Prometheus/OTel/Jaeger/Loki; the supplied quantified outcomes |
| **Supported after Project 1** | Simulated robot fleet; Go cloud-edge gateway; store-and-forward; application ACK/resume; MCAP/ROS 2 concepts used in a lab; Flink event time/watermarks/late data; Docker/Helm/OpenTofu; explicit OIDC/RBAC/rate/quota/metering; MLflow registry/canary—only the components and measured results that pass |
| **Supported after Project 2** | Production-style incident investigation agent; RAG with hybrid/reranked retrieval; typed tool calling; explicit/durable Temporal workflow; HITL; provider routing/fallback; AI eval/regression; OTel GenAI tracing; token/cost measurement; prompt-injection/tenant tests—only after all minimum gates |
| **Not currently supportable** | Robotics Engineer; production robot fleet; real LiDAR/video/control operation; HIL; production MLOps/model serving; distributed training; GPU/CUDA; experienced Agentic AI Engineer; production AI agents; multi-agent expert; LLM evaluation expert; AI safety expert; technical leadership of an AI organization |

## CV summaries

### Platform summary — Supported now

> Senior Software Engineer with approximately seven years of experience building and operating distributed, event-driven, data, search and observability systems in Go and Python. Delivered Kafka/NATS pipelines, multi-tenant services and ClickHouse/OpenSearch platforms at high volume, including an observability redesign handling more than 15 TB of logs per month that reduced query latency by approximately 75% and storage cost by approximately 40%. Seeking platform and infrastructure roles where streaming correctness, reliability, performance and developer-facing APIs matter.

### Agentic AI summary — Supported after Project 2

> Senior distributed-systems and observability engineer expanding into production AI systems. Built and evaluated a durable incident-investigation agent with access-controlled hybrid retrieval, typed read-only tools, explicit human approval, failure recovery and OpenTelemetry-based quality, latency and cost measurement. Brings seven years of production backend ownership and direct experience operating high-volume search, streaming and observability platforms.

Do not use the second summary merely because the repository exists. Use it only when the clean-checkout, evaluation, authorization and durability gates pass.

## Core skills ordering

### Job A — Supported now

**Distributed systems and streaming:** Go, Python, Kafka, NATS/JetStream, event-driven architecture, message delivery, idempotency, transactional outbox, DLQ/retries, concurrency  
**Data and storage:** ClickHouse, PostgreSQL, Redis, OpenSearch, CDC, high-volume data pipelines  
**Platform and APIs:** Kubernetes, gRPC, REST/backend services, multi-tenant SaaS  
**Reliability and observability:** OpenTelemetry, Prometheus, Jaeger, Loki, distributed tracing, performance optimization

Add **Flink, Docker, Helm, OpenTofu, event-time processing, edge store-and-forward, MCAP, OIDC/RBAC, quotas/metering and MLflow model rollout** only after Project 1 demonstrates each.

### Job B — Supported now, ordered for adjacency

**Production systems:** Python, Go, distributed systems, cloud-native/event-driven services, Kubernetes, concurrency, reliability and performance  
**Retrieval/data:** OpenSearch, hybrid keyword/semantic search, search relevance, ClickHouse, PostgreSQL, Redis, data pipelines  
**Operations:** OpenTelemetry, Prometheus, Jaeger, distributed tracing, high-volume observability, multi-tenancy and production ownership  
**Workflow correctness:** idempotency, outbox, locking, queues, retries, DLQ and ordered event processing

After Project 2 passes, add a separate first line: **Production AI systems: RAG, hybrid retrieval/reranking, structured tool calling, Temporal durable workflows, human approval, AI evaluation/regression, OTel GenAI tracing, prompt-injection testing, model routing/fallback.**

## Truthful CV bullets — Supported now

Use the actual employer/project context and dates from the real CV. These rewrites do not invent scope:

1. **Supported now:** Redesigned an observability platform by migrating log storage from Loki to ClickHouse and implementing hybrid trace storage, reducing query latency by approximately 75% and storage cost by approximately 40% while handling more than 15 TB of logs per month.
2. **Supported now:** Built a CDC pipeline that separated transactional and analytical workloads by replicating more than 50 million records per month into ClickHouse, improving reporting performance by approximately 60%.
3. **Supported now:** Migrated critical messaging from NATS Core to JetStream with persistent storage and acknowledgements, achieving zero observed message loss for critical streams within the measured production boundary.
4. **Supported now:** Built hybrid keyword-and-semantic search in OpenSearch for candidate-job matching, improving the stated match-accuracy metric by approximately 35% across more than 50,000 searches per day.
5. **Supported now:** Increased OpenSearch reindexing throughput by approximately 10x using an asynchronous, queue-driven batch pipeline.
6. **Supported now:** Built concurrent Go Kafka consumers with batching and manual offset management, migrating millions of records without observed loss or duplication.
7. **Supported now:** Designed a distributed queue/worker pipeline that aggregated more than 5 million records in under three minutes.
8. **Supported now:** Built a virtual-currency service using pessimistic locking, idempotency keys and the transactional outbox pattern to protect balance-update invariants under retries.
9. **Supported now:** Designed a multi-tenant SaaS platform supporting more than 1,000 tenants, including onboarding automation, data isolation and feature-tier management.
10. **Supported now:** Designed ordered event-processing workflows using Azure Service Bus, dead-letter queues and retry handling.

Before using “zero observed message loss” or “without observed loss or duplication,” confirm the original CV’s exact measurement language. If “zero” was not instrumented across a defined boundary, retain the supplied wording but be ready to explain its scope rather than broadening it.

## Conditional portfolio bullets

Replace brackets only with a committed report value. If the gate is not met, omit the bullet.

1. **Supported after Project 1:** Built a simulated cloud-edge robot telemetry platform in Go with a durable SQLite-WAL spool, bidirectional gRPC ACK/resume, Kafka and Flink event-time processing; sustained **[measured rate]** with **[measured p95/p99]** and recovered a **[duration]** disconnection with no missing IDs already accepted to the edge spool.
2. **Supported after Project 1:** Packaged the telemetry platform with Docker, Helm and OpenTofu and demonstrated OIDC/RBAC, per-tenant rate limits/usage reconciliation, Kubernetes rollout/rollback and **[measured recovery result]** under injected failures.
3. **Supported after Project 1:** Implemented an MLflow-backed champion/candidate model rollout for a simulated fleet with deterministic cohorts, health gating and a reproducible rollback drill. Use only if that component passes.
4. **Supported after Project 2:** Built and evaluated a durable incident-investigation agent in Python/Temporal with access-controlled hybrid OpenSearch retrieval, typed diagnostic tools and human approval; achieved **[task result]** across **[N scenarios × trials]** with **[retrieval/citation/safety metrics]**.
5. **Supported after Project 2:** Added OTel-based model/retrieval/tool/workflow traces, provider fallback, token/cost budgets and **[N]** injection/tenant-policy tests, with zero unauthorized tool executions in the published suite.

“Production-grade” is acceptable only as a design aspiration in the README. Prefer “production-style” on the CV because neither portfolio project has real users/on-call history.

## Achievement ordering

For Job A, move these highest: Kafka migration; JetStream reliability; observability platform; CDC/ClickHouse; distributed worker throughput; multi-tenancy. Put semantic search later.

For Job B, move these highest: observability platform; OpenSearch hybrid relevance; Kafka/JetStream correctness; multi-tenancy; virtual-currency invariants; CDC/ClickHouse. After Project 2 passes, place one Project 2 bullet immediately below the summary, then retain production achievements to prove depth.

Do not remove the production systems to make room for a stack list. The NVIDIA description explicitly values operating scalable, reliable software.

## Terms to add only when supported

| Timing | Terms |
|---|---|
| After Project 1 | Simulated cloud-edge telemetry, store-and-forward, event time/watermarks, Flink, MCAP, ROS 2 concepts, Docker, Helm, OpenTofu, OIDC/RBAC, rate limiting/quotas/metering, model registry/canary |
| After Project 2 | RAG, hybrid retrieval/reranking, structured tool calling, durable agent workflow, Temporal, PydanticAI, human-in-the-loop, AI evaluation, task-completion benchmark, AI observability, token/cost monitoring, prompt-injection testing, model routing/fallback |

Terms that must **not** be added yet: robotics engineer, edge-fleet production, HIL, autonomous robot control, production AI agents, multi-agent systems, model serving, distributed model training, foundation models, fine-tuning, GPU/CUDA, AI safety specialist or Staff/Principal title.

## GitHub presentation

Use exactly two primary repositories:

1. **robot-fleet-telemetry-platform**
2. **incident-investigation-agent**

Avoid names such as awesome-agent, ai-robot-platform, production-grade-everything or chatbot-demo.

Each landing README should answer, above the fold: problem/non-goals; one architecture image; what is actually implemented; one command to reproduce; three measured results with hardware/version; failure/security guarantees and limits; 10–15 minute demo path. Then link to ADRs, benchmark/eval raw data, threat model, dashboards/traces, postmortem and deployment guide.

Tag releases used in CV bullets. Preserve raw result JSON/CSV and the script/config/commit that generated it. Open issues for known limitations rather than hiding them. Pin Project 1 first during Platform search and Project 2 first only after its gate. A small, reviewed documentation/test contribution to PydanticAI, MCAP, Helm or OpenTofu is useful after the projects; do not chase an arbitrary contribution to a difficult core.

## LinkedIn

### Headline — Supported now

> Senior Software Engineer | Distributed Systems, Streaming & Observability | Go, Python, Kafka, Kubernetes, ClickHouse, OpenSearch

### Headline — Supported after Project 2

> Senior Distributed Systems Engineer | Platform & Production AI Systems | Go, Python, Streaming, Retrieval, Observability

### About — Supported now

> I am a Senior Software Engineer with approximately seven years of experience building distributed backend, streaming, search and observability systems.
>
> My work has included Kafka and NATS/JetStream reliability, CDC and ClickHouse analytics, OpenSearch hybrid search, multi-tenant SaaS and OpenTelemetry-based observability. Recent outcomes include an observability redesign handling more than 15 TB of logs per month that reduced query latency by approximately 75% and storage cost by approximately 40%, and a CDC pipeline processing more than 50 million records per month.
>
> I am targeting platform, distributed-systems and AI-infrastructure roles where correctness under failure, performance, observability and secure developer-facing systems matter. I am also building public evidence in simulated cloud-edge telemetry and evaluated AI workflows; I distinguish that portfolio work from production experience.

Add direct repository links to the final sentence only after the relevant milestone.

## Spoken introductions

### 30 seconds — Supported now

> I’m a Senior Software Engineer in Ho Chi Minh City with about seven years in distributed backend, streaming, search and observability systems, mainly in Go and Python. I’ve built reliable Kafka and JetStream workflows, ClickHouse platforms handling tens of millions of records and more than 15 terabytes of logs per month, and hybrid OpenSearch ranking. I’m now targeting platform and AI-infrastructure teams where that production reliability and data-systems depth is central.

### Two-minute strongest-project narrative — Supported now

> One of my strongest projects was redesigning an observability platform whose log-storage and query path had become costly and slow at more than 15 terabytes per month. My goal was not simply to replace a database; it was to preserve operational usefulness while reducing query latency and storage cost.
>
> I migrated log storage from Loki to ClickHouse and implemented a hybrid trace-storage approach. In the interview I would then explain the actual workload analysis, schema and partition choices, migration sequence, validation and rollback mechanisms that I personally used—without claiming details that were owned by someone else or are confidential.
>
> The measured result was approximately 75% lower query latency and 40% lower storage cost at the stated scale. The deeper lesson was that observability systems are themselves distributed data products: retention, cardinality, write amplification, query patterns and failure recovery must be designed together. That experience is directly relevant to robotics telemetry and AI observability, while I’m careful not to call it robotics or LLM experience.

### Project 2 narrative — Supported after Project 2

> I chose an incident-investigation agent because it uses my real observability background but forces me to prove the AI-specific parts I did not previously have. I built it as a durable workflow, not a chatbot: Temporal owns recovery and approval, typed activities call models and read-only tools, OpenSearch provides access-aware hybrid retrieval, and deterministic policy code owns authorization and budgets.
>
> The key artifact is the evaluation rather than the demo. I seeded **[actual number]** incident scenarios and ran **[actual trials]**, measuring task outcome, retrieval, tool choice, citations, unsupported claims, latency, cost and safety. I injected worker, provider and tool failures and **[state actual results]**. I selected Temporal over LangGraph after a small crash/replay/HITL comparison and retained a fallback if it did not justify its operational cost.
>
> The project did not give me years of production AI tenure. It gave me direct, reviewable evidence that I can apply distributed-systems, security and observability discipline to an LLM workflow and explain where the model remains unreliable.

### Transition explanation — Supported now

> I am not leaving backend and platform engineering behind. Agentic systems need the same disciplines I have used in high-volume production systems—durable state, idempotent effects, retrieval, multi-tenant authorization, backpressure, observability and incident response—plus new model, evaluation and security concerns. My semantic-search work is adjacent to retrieval but not RAG, so I am closing that gap with a production-style project whose outcomes, failures and costs are measured rather than presenting myself as an experienced AI-agent engineer prematurely.

## Application strategy: Job A

**Apply immediately.** The production-platform evidence is already strong. The six-week project is an interview-conversion accelerator, not an application prerequisite.

Before interviews, prioritize: (1) edge spool/ACK/resume and clock skew; (2) event time/Flink; (3) Docker/Helm/OpenTofu/Kubernetes workload evidence; (4) OIDC/RBAC/rate/quota/metering; and (5) one benchmark/postmortem. Real robot hardware, deep ROS application development, vendor HIL, distributed training, GPU operation and a company-specific model platform are reasonably learnable on the job unless marked mandatory.

### Honest robotics-gap answer

> My production experience is in high-volume cloud data, streaming and reliability rather than physical robots. The transferable part is explicit: Kafka/NATS delivery, gRPC, idempotency, ClickHouse analytics, multi-tenancy and observability. To learn the domain-specific failure modes, I built a simulated cloud-edge platform with a durable local spool, clock skew/out-of-order fixtures, ROS 2 message concepts and MCAP artifacts. I would not call that real fleet experience; I would pair with robotics engineers on hardware timing, safety and sensor semantics while contributing immediately on the platform layer.

### Translate prior work without exaggeration

Say: “A robot-health stream and my prior production event streams share partitioning, replay, backpressure and idempotency concerns. Robotics adds intermittent edge links, source clocks, physical sensor semantics and command safety; those are the new areas I tested in simulation.”

Do not say: “I operated robot telemetry at 15 TB/month.” The 15 TB/month figure belongs to logs. Do not relabel search vectors as robotics perception.

## Application strategy: Job B

For the exact live NVIDIA Vietnam role, send a transparent stretch application now because timing and location are unusually favorable. State the direct gap; lead with the systems half of the specification. For the broader Senior Agentic AI search, Project 2’s minimum credible gate should precede claims of direct fit.

### Minimum evidence before broad applications

Working durable workflow; four read-only tools; access-aware hybrid/reranked retrieval; 30+ scenarios × 3 trials; deterministic task/tool/citation/policy graders; OTel token/cost traces; worker/provider/tool failure tests; 20+ attack cases with no unauthorized execution; threat/eval/cost reports and reproducible release.

### Position semantic search accurately

> I have direct production experience with hybrid keyword and semantic retrieval in OpenSearch, including measured relevance improvement at more than 50,000 daily searches. That gives me retrieval, ranking and operations experience. It is adjacent to RAG, but it did not include LLM generation, grounding, citation evaluation or agent tools; Project 2 adds and measures those layers.

### Premature claims

Do not claim production LLMs, RAG, agents, multi-agent systems, model serving, AI evaluation expertise, memory architectures or AI technical leadership from the supplied employment evidence. After Project 2, claim one built/evaluated portfolio system—not production tenure.

### Differentiation from shallow demos

Emphasize explicit state and invariants, failure recovery, idempotent effects, prompt-independent authorization, tenant/ACL propagation, frozen evaluation data, repeated trials, retrieval/citation metrics, OTel traces, token/cost budgets, overload/provider failure and an honest postmortem. These are credible extensions of real production strengths.

## Target-company search

Prioritize roles that can employ someone in Vietnam, sponsor relocation, or are explicitly remote internationally. Do not spend the limited weekly budget on attractive US-only listings without a workable location path.

| Lane | Search titles | Company signals |
|---|---|---|
| Apply now | Platform Engineer, Distributed Systems Engineer, Data/Streaming Platform Engineer, Observability Engineer, Infrastructure Software Engineer, Backend Platform Engineer | Kafka/NATS/gRPC/Kubernetes/ClickHouse/OTel, high-volume APIs/data, developer platform; robotics/IoT as preferred rather than mandatory |
| Bridge lane | AI Platform Engineer, GenAI Platform Engineer, AI Reliability Engineer, AI Observability Engineer, ML Platform Engineer, LLM Infrastructure Engineer | Strong distributed/SRE/data requirements plus routing/eval/RAG; no mandatory years of model training/GPU |
| After Project 2 | Senior Software Engineer AI Systems, Applied AI Engineer, Agentic AI Engineer, AI Workflow/Orchestration Engineer | Production LLM/RAG/tools/eval with equal weight on backend reliability and operations |
| Deprioritize | Research Engineer foundation models, RL/post-training, CUDA/inference-kernel, robotics controls/perception | Requires evidence outside the plan and dilutes the narrative |

Use the 21-role sample as a vocabulary/requirement source, not a guaranteed application list. Set alerts for exact titles plus “Vietnam,” “Singapore,” “APAC,” “remote,” and relocation. Search company career pages weekly; ATS dates and status can change.

## Cadence and evidence tracker

- Weeks 1–6: three tailored Platform/bridge applications and two thoughtful networking contacts per week; one follow-up after 7–10 days.
- After Project 1: add the repository only when the Week-6 gates pass; send a short benchmark/failure insight rather than “please review my code.”
- AI Weeks 1–11: continue bridge roles; do not mass-apply as Agentic AI.
- At the Project 2 gate: five carefully matched Agentic/AI-platform applications per week for four weeks, each mapped to two production achievements and one portfolio artifact.
- Track role, location eligibility, source/date, top five requirements, evidence/gap, referral, version of CV, stage, feedback and next action. Review conversion by lane every two weeks; change targeting before rewriting identity.

## Networking topics

- Event-time correctness and replay for robot/edge telemetry.
- Operating ClickHouse for observability and the cost/latency trade-off.
- How AI platform teams evaluate task outcomes, not prompt screenshots.
- Durable tool execution and idempotency under retries.
- Access control and indirect prompt injection in multi-tenant agents.
- OTel GenAI conventions, content privacy and high-volume trace storage.
- Ask domain engineers what real robot/HIL failure most often invalidates cloud-only assumptions.

## Questions for hiring managers

1. Which boundaries does this team own: robot/edge, ingestion, developer API, data/ML platform or all of them?
2. What failure or capacity problem consumed the most engineering time in the last six months?
3. Which requirements are hard prerequisites on day one and which are domain knowledge learned on the team?
4. How are platform adoption, developer productivity and reliability measured?
5. For agent systems, what is the unit of evaluation and which outcomes are deterministic?
6. Who owns tool authorization, model/provider routing, incident response and cost budgets?
7. How are prompt/workflow/model/retrieval changes gated and rolled back?
8. What data may be captured in traces, and how is tenant/PII isolation enforced?
9. Where has multi-agent architecture demonstrably outperformed a simpler workflow?
10. What would an excellent first 90 days produce, and what operational burden would the new engineer inherit?

## Referral message

> Hi [Name] — I’m a Senior Software Engineer in Ho Chi Minh City with about seven years in distributed systems, streaming, search and observability. My background includes reliable Kafka/NATS workflows, ClickHouse platforms at high volume, hybrid OpenSearch retrieval and multi-tenant services. I’m interested in [role] because [one specific responsibility] closely matches [one supported achievement]. My direct gap is [robotics edge / production Agentic AI], which I’m addressing through [linked, passed project milestone] without presenting it as production experience. If you think the systems background fits the team, would you be comfortable referring me or sharing what the hiring manager values most? CV: [link]. Evidence: [link].

## Recruiter response

> Thanks for reaching out. I’m interested in [role]. I have about seven years of production backend and distributed-systems experience, with Go/Python, Kafka/NATS, Kubernetes, ClickHouse/OpenSearch, multi-tenancy and observability. The strongest match is [specific requirement + achievement]. I want to be transparent that [specific gap] is portfolio rather than production experience; here is the measured artifact: [link, only after gate]. I’m based in Ho Chi Minh City and would like to confirm the location/remote/relocation arrangement and the team’s top two day-one requirements before scheduling.

## Technical portfolio introduction

> These repositories test two explicit career gaps using the engineering disciplines I already use in production. The robot-fleet project tests intermittent edge delivery, event-time correctness, secure developer APIs and reproducible operations. The incident-agent project tests durable LLM/tool workflows, access-aware retrieval, outcome-based evaluation, AI observability and prompt-independent authorization. Each publishes raw benchmarks, failure injection, threat assumptions and limitations; neither is presented as real production robotics or AI tenure.

---

# Part 11 — Final prioritized actions

## 1. Five actions for the next seven days

| Deadline | Action | Done means |
|---:|---|---|
| 17 Jul | Create robot-fleet-telemetry-platform and freeze scope | Public/private repo, problem/non-goals, architecture context, workload assumptions, acceptance checklist and ADR-001 delivery boundary |
| 18 Jul | Produce two one-page CV variants and application tracker | Every bullet maps to supplied evidence; Platform ordering and AI-adjacent ordering; unsupported terms absent |
| 19 Jul | Apply | Menlo/closely matched Platform roles submitted; exact NVIDIA Vietnam role submitted as a transparent stretch if still live; location eligibility checked |
| 21 Jul | Commit the first runnable slice | Protobuf envelope, Go fleet generator, one ROS 2 Jazzy publisher and one MCAP file decoded/validated from a clean checkout |
| 23 Jul | Establish interview/evidence baseline | One recorded 35-minute fleet design, scored with the rubric; three gaps logged; Week-1 README and ADR reviewed against the truth ledger |

Keep the week to 10 hours: about six implementation, 2.5 focused study and 1.5 CV/application/interview. If applications take longer, reduce visual polish—not correctness work.

## 2. Top five resources to start, in order

1. **Streaming Systems:** Ch. 2, then 3/5/7 only when their project week arrives.
2. **Apache Flink event-time/watermark/fault documentation:** build the golden late-data job; do not take a general course.
3. **DDIA 2e:** Ch. 5, 9 and 12 first; use it to sharpen invariants/failure boundaries.
4. **Temporal Python SDK/testing/message passing:** start with the small crash/resume/HITL comparison, not a full agent.
5. **Anthropic Demystifying Evals for AI Agents:** define task/trial/outcome/grader before tuning Project 2.

Do not study all five in Week 1. This is the start order for the roadmap.

## 3. First GitHub deliverable

**robot-fleet-telemetry-platform, v0.1-design-and-envelope**

It contains:

- README with problem, explicit non-goals and “simulated—not production robotics” label;
- one context architecture diagram;
- docs/requirements.md with workload and Week-6 acceptance gates;
- docs/adr/0001-delivery-and-ack-boundary.md;
- api/telemetry.proto with tenant/robot/boot/stream/sequence and four timestamps;
- Go generator emitting health/joint/pose/command-ACK fixtures;
- one ROS 2 Jazzy sample recorded to MCAP plus a validation command;
- clean-checkout instructions and known limitations.

This is stronger than an empty multi-service scaffold because it makes the claims, invariants and test boundary reviewable before complexity arrives.

## 4. Earliest reasonable application dates

| Target | Date | Qualification |
|---|---:|---|
| Job A / adjacent Platform roles | **16 July 2026—now** | Existing production evidence is sufficient; Project 1 improves interview conversion |
| Exact NVIDIA Vietnam Job B | **By 19 July 2026** | Transparent stretch because the live local vacancy may close; do not claim direct experience |
| Broad Job B, dedicated AI plan | **5 November 2026** | Only if every Project 2 minimum gate passes |
| Broad Job B, hybrid plan | **19 November 2026 at the earliest; 17 December is safer** | Apply on 19 Nov only if the 120-hour release candidate already passes durability, authorization, evaluation and reproducibility; otherwise finish hardening |

## 5. Ten highest-priority skills

1. Cloud-edge store-and-forward, durable ACK/resume and reconnect/full-disk policy.
2. Event time, watermarks, late/out-of-order data and Flink recovery.
3. Backpressure, admission, bounded queues, load shedding and tail latency.
4. Docker/Helm/OpenTofu plus operational Kubernetes rollout, HPA and rollback.
5. Trusted identity, tenant authorization, rate limits, quotas and durable metering.
6. Hybrid retrieval/reranking with Recall@k/MRR/nDCG, citations and ACL prefilters.
7. Explicit state machines and durable workflows with idempotent tool effects, cancellation and approval.
8. Outcome-based AI evaluation: versioned scenarios, deterministic graders, repeated trials and regression gates.
9. Prompt-injection defense, prompt-independent tool authorization, isolation and audit.
10. AI observability: model/retrieval/tool/workflow traces, versioning, tokens, latency, cost and failure class.

## 6. Three activities to defer explicitly

1. **New language/GPU/model-training branch:** Rust, C++, CUDA, foundation-model training, fine-tuning, distributed training and a GPU cluster.
2. **Agent complexity without evidence:** multiple agents, knowledge graph, generic long-term memory, semantic cache or self-hosted inference until a frozen evaluation shows a need.
3. **Portfolio sprawl:** full-rate video/LiDAR, real-time robot control, claimed HIL, multi-region production emulation or a merged capstone before both independent acceptance gates pass.

## 7. Clearest professional positioning

> **A senior distributed-systems and observability engineer with proven high-volume streaming, search and multi-tenant platform experience, building verifiable cloud-edge and production AI-system evidence through durable workflows, security, evaluation and operations.**

The near-term hiring story is Platform/AI Infrastructure. The earned future story is Agentic AI Systems. The bridge is production engineering discipline—not a new title or a framework list.
