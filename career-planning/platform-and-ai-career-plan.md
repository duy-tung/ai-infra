# **Strategic Career Roadmap and Capability Development Plan for Distributed Systems and Applied AI Engineering**

## **Part 1: Executive Assessment**

An exhaustive evaluation of the candidate’s professional profile reveals a highly capable distributed systems engineer possessing a proven track record in high-volume data pipelines, backend architecture, and observability infrastructure. Demonstrating the capacity to process more than 50 million records monthly and manage 15 terabytes of logs with optimized query latency, the candidate’s foundational engineering skills in Go, Python, Kafka, and ClickHouse are unequivocally battle-tested. The overarching professional narrative for this candidate must be strictly positioned as: "A distributed-systems and observability engineer expanding into production AI infrastructure and agentic systems."  
This foundational strength provides a massive structural advantage. Modern robotics infrastructure and production-grade AI systems share a common underlying reality: they are fundamentally distributed computing problems operating under strict reliability constraints. The candidate's experience with message-delivery semantics, idempotency, vector-style retrieval via OpenSearch, and continuous platform ownership natively transfers to the architectural requirements of both target roles. Whether mitigating transient network failures for edge robotics or managing the non-deterministic output of a large language model through durable execution, the core engineering disciplines remain identical.

### **Fit Score and Assessment: Target Job A (Platform Engineer, Robotics)**

The current fit score for the Platform Engineer role is 72 out of 100, carrying a high confidence level based on the demonstrated production evidence. The analysis recommends an "apply while learning" strategy, targeting active applications within four to six weeks. The strongest matching signals include the candidate's deep expertise in high-throughput streaming (specifically Kafka and NATS JetStream), proven success in observability redesigns using ClickHouse and OpenTelemetry, native proficiency in Go and Python, and an established history of owning event-driven pipelines and backend APIs.  
Conversely, the largest gaps present in the profile center on domain-specific robotics paradigms. The candidate currently lacks exposure to edge-computing concepts, the handling of physical sensor data streams (such as LiDAR and joint states), awareness of C++ or ROS 2 middleware, hardware-in-the-loop (HIL) simulation pipelines, and modern continuous integration for embedded hardware targets1. However, because the target role focuses heavily on the cloud infrastructure supporting the fleet, these gaps can be systematically closed through a highly targeted portfolio project.

### **Fit Score and Assessment: Target Job B (Senior Software Engineer, Agentic AI Systems)**

The current fit score for the Agentic AI Systems role is 45 out of 100, carrying a high confidence level. The analysis recommends completing a substantial portfolio project first, targeting applications in 16 to 24 weeks. The strongest matches for this transition reside in the candidate's experience building hybrid keyword-and-semantic search in OpenSearch, a deep understanding of distributed processing reliability, strong Python proficiency, operational observability, and the architectural design of multi-tenant SaaS platforms.  
The largest gaps are significant and constitute application blockers. The candidate lacks production experience with LLM orchestration, familiarity with modern AI evaluation frameworks such as Ragas and DeepEval, knowledge of durable agent execution using engines like Temporal, safety mechanisms for tool-calling, and the lifecycle management of prompts and context windows4. Presenting the candidate as an Applied AI Engineer without closing these gaps would result in interview failures when probed on evaluation metrics or non-deterministic failure modes.  
The primary immediate track must be Platform Engineering, as the candidate's existing portfolio is highly adjacent to the cloud-infrastructure side of robotics fleets. The secondary, long-term track is Agentic AI Systems, requiring the candidate to build credible, production-style evidence before competing in a saturated market of AI developers.

## **Part 2: Requirement Matrices**

The following matrices provide an evidence-based fit assessment for each target role, mapping the candidate's demonstrated achievements directly to the core responsibilities of the jobs.

### **Job A: Platform Engineer (Robotics/Cloud-Edge)**

| Requirement | Importance | CV Evidence | Evidence Strength | Gap | Action |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Distributed Infrastructure** | High | Built multi-tenant SaaS (1000+ tenants); 50M records CDC pipeline. | Direct and strong | None (Application blocker if missing). | Emphasize scale and multi-tenancy in CV. |
| **Go & Python Proficiency** | High | Primary languages used in Kafka consumers, async processing pipelines. | Direct and strong | None. | Continue primary use of Go and Python in portfolio projects. |
| **Streaming / Edge to Cloud** | High | NATS Core to JetStream migration (achieving zero loss); Kafka manual offset management. | Direct but limited | Cloud-to-cloud is proven; edge-to-cloud (intermittent connectivity) is missing3. | Build a store-and-forward edge gateway simulating connectivity drops. |
| **Robotics Data/Sensor APIs** | High | Processed transactional data; no physical telemetry or sensor handling. | Missing | Robotics telemetry payload formats, video/LiDAR chunking1. | Likely interview blocker. Simulate joint-state and LiDAR data in Project 1\. |
| **Observability & Reliability** | High | Loki to ClickHouse migration; 75% latency reduction; OpenTelemetry tracing. | Direct and strong | None. | Highlight as a major differentiator for operational fleet health. |
| **Kubernetes & Docker** | High | Kubernetes noted in CV; Docker not explicitly listed but implied. | Direct but limited | Helm chart creation and Infrastructure as Code (Terraform) are missing or implicit. | Portfolio evidence needed. Integrate Terraform and Helm into Project 1\. |
| **Hardware-in-the-loop (HIL)** | Medium | None demonstrated. | Missing | Software-in-the-loop (SIL) and HIL simulation pipelines1. | Can reasonably be learned on the job. Defer deep dive unless explicitly required. |
| **API Auth & Rate Limiting** | High | Multi-tenant SaaS with feature-tiers; pessimistic locking. | Adjacent and transferable | Explicit API metering, quota enforcement, and OAuth2/OIDC implementation. | Portfolio evidence needed. Add API gateway logic with strict rate limits. |

The gaps for the Platform Engineer role are primarily domain-specific rather than foundational. The lack of robotics data exposure can be mitigated by demonstrating a robust understanding of how to ingest massive, out-of-order time-series data from intermittent edge devices.

### **Job B: Senior Software Engineer, Agentic AI Systems**

| Requirement | Importance | CV Evidence | Evidence Strength | Gap | Action |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Python & Backend Services** | High | Python listed as primary; virtual currency outbox pattern implementation. | Direct and strong | None. | Leverage heavily for AI orchestration backend. |
| **LLM Applications & RAG** | High | None demonstrated. | Missing | Core LLM APIs, prompt management, context window optimization. | Application blocker. Must build via Project 2\. |
| **Semantic Search / Vector DB** | High | Built hybrid keyword-and-semantic search in OpenSearch. | Direct and strong | Understanding chunking strategies specifically optimized for LLM consumption. | Leverage existing OpenSearch knowledge; shift focus entirely to retrieval evaluation5. |
| **Agent Orchestration** | High | None demonstrated. | Missing | State machines, multi-step planning, tool protocols7. | Application blocker. Implement PydanticAI combined with Temporal. |
| **Durable Execution & State** | High | Event-driven Azure Service Bus; queue/worker architecture. | Adjacent and transferable | Adapting event-driven logic to AI state machines (e.g., Temporal)8. | High-leverage gap. Maps perfectly to existing asynchronous skills. |
| **AI Evaluation & Benchmarking** | High | None demonstrated. | Missing | LLM-as-a-judge, deterministic evaluation, groundedness testing10. | Application blocker. Implement DeepEval and Ragas frameworks. |
| **AI Observability** | Medium | Built OpenTelemetry/Jaeger tracing; Loki/ClickHouse logs. | Adjacent and transferable | Token tracking, cost monitoring, hallucination tracing spans4. | Helpful differentiator. Adapt existing tracing skills specifically to LLM spans. |
| **Productionizing Prototypes** | High | Migrated message infrastructure; achieved 10x OpenSearch reindexing performance. | Direct and strong | None. | Frame as the core value proposition differentiating the candidate from researchers. |

For the Agentic AI role, the absence of evaluation methodology is the most critical blocker. Modern applied AI engineering focuses less on prompt engineering and more on building rigorous testing harnesses to ensure models behave predictably5.

## **Part 3: Prioritized Competency Map**

The following map defines the specific skills necessary to bridge the gap between traditional backend engineering and the specialized requirements of Robotics Platforms and Agentic AI Systems. By branching from a shared foundation, the candidate can maximize learning efficiency.

The shared foundation represents high-leverage skills that benefit both roles and predominantly draw upon the candidate's existing strengths. Distributed systems reliability operates as a Priority 0 (P0) requirement, demanding a working knowledge of delivery semantics, idempotency, backpressure, and capacity planning. The candidate's background in mitigating message loss during NATS migrations explicitly validates this competency. Similarly, performance engineering, infrastructure platform operations (Kubernetes), and observability (OpenTelemetry) remain P0 skills where the candidate has already demonstrated the ability to operate in production and lead design initiatives.  
Transitioning to the Platform Engineer specialization requires acquiring edge computing and telemetry concepts as a P0 competency. The candidate must learn to implement store-and-forward patterns, handle intermittent connectivity gracefully, and reconcile out-of-order data3. A critical P0 addition is a working knowledge of next-generation messaging protocols utilized in robotics, specifically evaluating Kafka against the Zero Overhead Network Protocol (Zenoh)13. Zenoh has emerged as a dominant protocol for robot-to-robot and edge-to-cloud communication due to its minimal 5-byte wire overhead and ability to run efficiently on highly constrained microcontrollers14. Securing platform APIs with OAuth 2.0, OIDC, and explicit rate limiting operates as a strong differentiator (P1), while Infrastructure as Code (Terraform) is elevated to a P1 working knowledge requirement. General robotics concepts like ROS 2 and HIL simulation remain P2 awareness goals, deferred until the cloud infrastructure elements are mastered1.  
The Agentic AI Systems branch requires a distinct set of P0 competencies. LLM engineering fundamentals, including tokenization, context window management, and structured output parsing, demand immediate working knowledge5. Crucially, the candidate must master durable workflow orchestration using Temporal (Go or Python) to manage agent state, enforce retries, and handle human-in-the-loop execution8. Unlike standard stateless APIs, AI agents require mechanisms to pause and resume execution without suffering from transient network failures or model timeouts. Agent architecture utilizing PydanticAI for strict tool calling and dependency injection acts as a P0 implementation requirement16. The candidate must also achieve P0 proficiency in AI evaluation and observability, implementing deterministic evaluators and frameworks like DeepEval and Ragas to measure task completion, faithfulness, and answer relevancy while tracking token costs4. Retrieval Augmented Generation (RAG) acts as a P1 implementation requirement, allowing the candidate to adapt their strong OpenSearch background to advanced chunking and reranking methodologies5.

## **Part 4: Ranked Resource Library**

The research identified a curated list of resources tailored to the candidate's requirement to bypass introductory material and focus heavily on distributed systems correctness, robotics data layers, and production AI evaluation. The resource budget allocates the permitted USD 500 strictly to cloud infrastructure provisioning (AWS/GCP), Temporal Cloud developer tiers, and LLM API costs for portfolio projects, relying entirely on free official documentation and academic papers for theoretical learning.

| Name | Type | Track | Source | Depth | Exact Scope | Gap Addressed | Score | Label |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Designing Data-Intensive Applications** | Book | Shared | Official text (Kleppmann) | Expert | Ch 10 (Batch), Ch 11 (Stream), Ch 8 (Distributed Troubles). | Distributed correctness, event-time, consistency. | 98/100 | Must study |
| **Temporal Go SDK Documentation** | Docs | Shared | docs.temporal.io/develop/go | Advanced | Workflows, Activities, Selectors, Observability9. | Durable execution, human-in-the-loop orchestration8. | 95/100 | Must study |
| **Zenoh Protocol Specification** | Docs | Platform | zenoh.io/docs/overview/what-is-zenoh/ | Advanced | Key Expressions, Pub/Sub, Zenoh for ROS 213. | Edge-to-cloud networking, low-overhead robotics13. | 92/100 | Strong Rec |
| **PydanticAI Documentation** | Docs | AI | ai.pydantic.dev | Advanced | Agents, Dependencies, Structured Results, Multi-agent16. | Agent state, tool calling, type-safe LLM outputs. | 94/100 | Must study |
| **DeepEval Official Repository** | Repo | AI | github.com/confident-ai/deepeval | Advanced | Metrics (Faithfulness, Relevancy), Test Cases, CI/CD4. | AI Evaluation, LLM-as-a-judge, CI regression testing. | 92/100 | Must study |
| **Automated Evaluation of RAG (Ragas)** | Paper | AI | arxiv.org/abs/2309.15217 | Expert | Sections on Faithfulness, Answer Relevance, Context Precision10. | Reference-free evaluation metrics for retrieval. | 90/100 | Strong Rec |
| **PydanticAI & Temporal Integration** | Repo | AI | github.com/pydantic/pydantic-ai-temporal-example | Advanced | Full source code, Slack integration8. | Combining durable workflows with LLM agents. | 95/100 | Must study |
| **ROS 2 rmw\_zenoh Design** | Repo | Platform | github.com/ros2/rmw\_zenoh/blob/rolling/docs/design.md | Advanced | Serialization (CDR), Topic mapping, Discovery22. | Translating cloud pub/sub to robotics middleware. | 88/100 | Strong Rec |
| **OpenTelemetry for Generative AI** | Docs | Shared | OTel Semantic Conventions | Inter. | GenAI traces, token counting, latency metrics. | AI observability, hallucination tracking. | 85/100 | Reference |
| **Streaming Systems** | Book | Platform | Official text (Akidau et al.) | Expert | Event time vs Processing time, Watermarks, Windowing. | Out-of-order sensor telemetry handling. | 88/100 | Strong Rec |
| **LangGraph Documentation** | Docs | AI | github.com/langchain-ai/langgraph | Inter. | State machines, durable execution comparison24. | Agent orchestration trade-offs vs Temporal. | 85/100 | Reference |
| **Anthropic Applied AI Engineering** | Blog | AI | getperspective.ai/blog/anthropic-applied-ai-engineers... | Inter. | Tool use, system prompts, Claude Enterprise patterns25. | Market context for Applied AI roles. | 88/100 | Strong Rec |

Studying the integration of Zenoh with ROS 2 through the rmw\_zenoh repository provides the candidate with the precise terminology required to pass robotics platform interviews22. Zenoh bridges ROS 2 communications over DDS, allowing for a better integration of the ROS graph and easier integration with native applications by mapping services to Zenoh Queryables27. Similarly, mastering the Ragas paper ensures the candidate can speak authoritatively on how to evaluate retrieval generation using reference-free metrics, penalizing redundant information through Context Relevance scoring and ensuring answers infer directly from provided contexts via Faithfulness scoring10.

## **Part 5: Six-Week Platform Application Sprint**

This initial sprint leverages the candidate's deep Go, Kafka, and OpenTelemetry background, methodically closing the gaps regarding edge-connectivity, infrastructure-as-code, and robotics data paradigms. By week six, the candidate will be ready to begin interviewing for Platform roles.  
Week 1 focuses heavily on intermittent connectivity and the edge-to-cloud paradigm. The objective is to understand robotics telemetry formats and store-and-forward architectures. The candidate will utilize *Designing Data-Intensive Applications* and *Streaming Systems* to grasp the distinction between event time and processing time. The implementation task requires building a Go-based mock robot telemetry generator that emits JSON joint-states and synthetic LiDAR metadata, featuring a local buffer that simulates network disconnections and resumes transmission without dropping data. This directly prepares the candidate to discuss out-of-order event reconciliation in interviews.  
Week 2 shifts to evaluating next-generation robotics messaging, specifically comparing Zenoh against Kafka. The objective is to evaluate lightweight edge protocols against heavy cloud brokers. Utilizing the Zenoh Protocol Specification, the candidate will build an Edge Gateway in Go, implementing Zenoh to receive the robot data, buffer it, and bridge it to a cloud-based Kafka or JetStream cluster13. This phase builds the narrative around delivery semantics, brokerless versus brokered messaging, and maximizing bandwidth via low wire-overhead14.  
Week 3 involves constructing idempotent ingestion and storage routing within the cloud layer. Reusing their ClickHouse and PostgreSQL knowledge, the candidate will consume from the cloud broker, routing raw high-volume telemetry to ClickHouse and control-state to PostgreSQL. A critical requirement is ensuring strict idempotency using message identifiers, proving exactly-once processing claims and demonstrating an understanding of database partitioning for time-series data.  
Week 4 focuses on Platform APIs, authentication, and rate limiting. The objective is to expose the ingested data securely to external developers. Using Go, the candidate will build a gRPC/REST API implementing JWT-based authentication, a Redis-backed sliding window rate limiter, and usage metering middleware. This exercise closes the gap on API security and multi-tenancy isolation required by modern robotics developer platforms.  
Week 5 introduces Infrastructure as Code (IaC) and modern deployment practices. The candidate will containerize the platform by writing optimized Dockerfiles, creating Terraform scripts to provision a minimal cloud cluster, and writing a Helm chart for the ingestion pipeline. This results in a fully automated infrastructure deployment repository, preparing the candidate for interview questions regarding Kubernetes autoscaling, failover, and blast-radius mitigation.  
Week 6 culminates in observability polish and achieving Milestone 1\. The candidate will instrument the entire pipeline from the simulated robot through Zenoh, Kafka, and Go, all the way to ClickHouse, using OpenTelemetry. Creating Grafana dashboards that map queue lag against end-to-end ingestion latency will finalize the Minimum Viable Milestone for Project 1\. The immediate action is updating the CV and LinkedIn profile to begin submitting applications to Robotics Platform Engineer roles.

## **Part 6: Sixteen-Week Agentic AI Transition Plan**

Following the completion of the Platform project, the focus shifts entirely to Python, durable execution, and production AI. This track transforms the candidate's existing observability mindset into a rigorous AI evaluation mindset.  
Weeks 7 through 9 are dedicated to LLM engineering fundamentals and PydanticAI. The objective is to master LLM APIs, structured outputs, and type-safe agent design. Utilizing PydanticAI documentation, the candidate will build a baseline Python API that interacts with a hosted LLM, enforces output schemas using Pydantic, and utilizes basic tool calling capabilities to fetch a mocked operational runbook16. This results in a stateless, functional AI assistant that serves as the foundation for the subsequent weeks.  
Weeks 10 through 12 focus on advanced retrieval and Ragas evaluation. The objective is to adapt the candidate's OpenSearch experience specifically to RAG architectures and learn reference-free evaluation methodologies. Drawing heavily from the Ragas paper10, the candidate will index synthetic system documentation in OpenSearch using embeddings, implement hybrid search, and evaluate the entire RAG pipeline using Ragas metrics such as Faithfulness and Answer Relevance. This delivers an evaluated RAG pipeline demonstrating measurable recall and precision.  
Weeks 13 through 15 tackle the critical challenge of durable orchestration using Temporal. The goal is to solve the transient failure and state management problems inherent in multi-step AI agents. Using the Temporal Python SDK and integration patterns8, the candidate will refactor the stateless agent into a Temporal Workflow. This involves defining explicit Activities for tool execution and implementing a human-in-the-loop signal that pauses the workflow to require manual approval before executing a mocked infrastructure change. The deliverable is a highly resilient, stateful AI agent capable of surviving complete process restarts.  
Weeks 16 through 18 integrate AI Observability and the DeepEval framework. The objective is to measure and monitor agent tasks as they would operate in production. The candidate will instrument the Temporal workflow with OpenTelemetry for GenAI, write comprehensive DeepEval test cases evaluating Task Completion and Tool Correctness, and run them locally in a Pytest suite4. This establishes a CI/CD-ready evaluation harness designed to fail the build if agent performance degrades below acceptable thresholds.  
Weeks 19 through 22 represent the final polish of Project 2, synthesizing all components into the "Incident Operations Agent." The candidate will merge the Temporal workflow, PydanticAI agent logic, OpenSearch RAG retrieval, and DeepEval testing suite into a single cohesive repository. A critical addition during this phase is threat modeling, specifically adding prompt injection tests and strict tool authorization boundaries. The completion of this phase marks Milestone 2, creating a highly credible body of evidence for Agentic AI roles.

## **Part 7: Full 24-Week Hybrid Plan**

The integrated 24-week schedule demands approximately 10 hours per week, balancing implementation with theory and interview preparation.

* **Phase 1 (Weeks 1–6): Cloud-Edge Robotics Telemetry (60 hours).** This phase culminates in Milestone 1\. A key decision point occurs here: the candidate must evaluate if the hardware and edge networking aspects of robotics hold long-term interest. If so, they should immediately begin applying to Platform roles.  
* **Phase 2 (Weeks 7–12): LLM Foundations & RAG Evaluation (60 hours).** This phase shifts to Python and AI integration. The candidate should assess if the AI tooling ecosystem feels natural. If it proves frustrating, they can pivot entirely to applying for standard Go/Backend roles using the momentum from Phase 1\.  
* **Phase 3 (Weeks 13–18): Durable AI Agents (60 hours).** This phase merges the candidate's deep distributed systems knowledge with AI workflows through Temporal, establishing the primary differentiator for Job B.  
* **Phase 4 (Weeks 19–22): Project 2 Polish & AI Evals (40 hours).** This phase finalizes Milestone 2, ensuring the Agentic AI portfolio project is production-grade, evaluated, and observable. The candidate is now credible for Job B applications.  
* **Phase 5 (Weeks 23–24): Capstone & Interview Prep (20 hours).** This final phase establishes Milestone 3, ensuring hybrid readiness through intense mock interviews, architectural design practice, and final CV tuning.

## **Part 8: Project Specifications**

### **Project 1: Cloud-Edge Robot Telemetry Platform**

This project demonstrates mastery of high-throughput data pipelines, edge constraints, and infrastructure architecture, directly addressing gaps for the Platform Engineer role.  
The architecture begins with an Edge Simulator written in Go, which generates mock telemetry such as joint-states, battery health, and LiDAR metadata. Crucially, it must include a local buffer to simulate offline and online transitions, retaining data during simulated network drops. The Edge Gateway uses the Zenoh protocol for minimal overhead communication to the cloud, bridging the gap between constrained devices and the wider network13.  
In the cloud ingestion layer, the candidate will utilize Kafka or NATS JetStream, acting as the main message bus. A Go consumer will write the heavy telemetry payload to ClickHouse for analytical querying and operational state to PostgreSQL. The Platform API consists of gRPC and REST endpoints for device registration and telemetry querying, secured by JWT and metered using a Redis sliding-window implementation. The entire infrastructure must be deployable via Docker Compose locally or via Terraform to a low-cost cloud provider.  
Acceptance criteria require zero silent data loss when the Edge Simulator disconnects for five minutes and subsequently reconnects. A Grafana metrics dashboard must demonstrate end-to-end ingestion latency under 500 milliseconds at the 99th percentile. Finally, the repository must include a documented Architecture Decision Record (ADR) justifying the use of Zenoh over MQTT or Kafka for the specific edge link13.

### **Project 2: Production-Grade Agentic AI System**

This project builds an autonomous incident investigation agent to prove competence in durable execution, retrieval, and AI evaluation, directly addressing the core requirements of an Applied AI Engineer.

The implementation relies on Temporal's Python SDK to serve as the workflow engine, handling retries, timeouts, and sleep states9. This ensures that a multi-step agent does not crash halfway through an investigation due to a transient API failure. Agent logic is managed by PydanticAI, enforcing strict structured inputs and outputs for the LLM to prevent formatting hallucinations16. Retrieval utilizes OpenSearch hybrid search for querying mocked incident runbooks. A critical component is the human-in-the-loop mechanism, implemented via a Temporal Signal, which pauses the workflow and demands manual human approval before the agent can execute any write-actions. Evaluation is conducted via DeepEval and Ragas, running offline batch evaluations on a dataset of mocked incidents to measure Task Completion and Context Precision7.  
The choice of framework requires explicit justification. While LangGraph is highly popular for AI workflows, it is tightly coupled to the LangChain ecosystem and primarily focused on the orchestration of the prompts themselves. Temporal, conversely, provides superior, language-agnostic durable execution, better handling of arbitrary asynchronous events (like waiting hours for human approval), and robust failure recovery deeply rooted in distributed systems principles8. Given the candidate's backend systems background, combining Temporal for state management with PydanticAI for LLM logic is the superior architectural choice, demonstrating a profound understanding of production reliability.  
An optional capstone combining both projects into an "Observable AI Operations for a Robot Fleet" is explicitly deferred. Integrating the two massive scopes within a 240-hour budget would inevitably result in compromised quality. Keeping the robotics pipeline and the AI incident agent as distinct, highly polished repositories allows the candidate to target specific hiring managers with relevant, focused codebases.

## **Part 9: Interview Preparation**

Interview preparation must focus on translating the candidate's existing achievements into the vocabulary of the target roles.  
For Job A (Platform Engineer), system design questions will focus heavily on streaming architecture and edge-to-cloud design. A likely prompt is: "Design a telemetry ingestion system for a fleet of 100,000 delivery drones. How do you handle 10-minute connectivity dropouts?" A strong answer will discuss store-and-forward mechanisms at the edge, watermarking for event-time processing, and the utilization of partitioned logs in the cloud. The candidate must utilize their experience in manual Kafka offset management to discuss the trade-offs between exactly-once and at-least-once delivery semantics. When asked about messaging infrastructure, the candidate should contrast the broker mechanics of NATS JetStream and Kafka, drawing heavily on their CV migration achievement (Achievement \#5). When discussing API security, explaining sliding window algorithms in Redis ties directly back to their multi-tenant SaaS experience (Achievement \#12).  
For Job B (Agentic AI Systems), system design shifts to durable execution and evaluation. A likely prompt is: "Design an AI system that autonomously triages and resolves customer support tickets. How do you prevent it from taking destructive actions?" A strong answer proposes a Temporal-backed durable workflow utilizing PydanticAI for strict tool schemas, explicitly designing a state machine where destructive tools require a Human-in-the-Loop approval signal. When asked about evaluating RAG pipelines, the candidate must discuss building a golden dataset and using Ragas metrics (Context Precision, Context Recall) alongside DeepEval (Answer Relevancy) in a CI/CD pipeline, rather than relying on subjective human vibe-checks4. For AI observability, the candidate must leverage their Loki-to-ClickHouse redesign (Achievements \#3 & \#4) to explain how to store and query immense volumes of OTel traces emitted by multi-agent LLM systems.

## **Part 10: CV, LinkedIn, and Application Strategy**

The candidate must be positioned truthfully as an elite backend systems engineer who builds the resilient platforms required to make AI and Robotics run securely at scale. They must not be rewritten as an AI researcher or a hardware robotics engineer. The market for Applied AI Engineers5 heavily favors individuals who can ship reliable systems over those who merely write clever prompts in notebooks.  
For Platform roles, the revised professional summary should state: "Senior Software Engineer specializing in high-throughput distributed systems, event-driven architecture, and observability. Proven track record of scaling Kafka and ClickHouse pipelines to handle tens of millions of records with zero data loss. Passionate about applying cloud-native reliability to edge computing and robotics telemetry."  
After completing Milestone 2, the summary for Agentic AI roles should state: "Senior Software Engineer specializing in durable distributed systems, observability, and AI infrastructure. Combines deep backend expertise (Temporal, Kafka, OpenSearch) with production AI evaluation frameworks (DeepEval, Ragas) to build reliable, scalable, and observable agentic workflows."  
Claims regarding Kafka, JetStream, ClickHouse, OpenSearch, CDC pipelines, and multi-tenancy are fully supported now. Claims regarding edge-to-cloud telemetry sync, Terraform, and API Gateway rate-limiting will be supported after Project 1\. Claims regarding durable AI execution, agent orchestration, and AI evaluation will be supported after Project 2\. The candidate must strictly avoid unsupportable claims regarding ROS 2 C++ development, deep neural network training, embedded hardware programming, or CUDA optimization.  
The application strategy advises applying immediately to cloud-adjacent robotics roles (e.g., Data Platform Engineer for Robotics). The candidate should use their high-volume pipeline work as direct proof of capability for telemetry ingestion, explaining the lack of hardware robotics experience by emphasizing a desire to own the complex cloud-side of the fleet. Conversely, the candidate should *not* apply to Agentic AI roles yet. The market is currently saturated with developers offering shallow LLM wrappers. By completing Project 2—specifically featuring Temporal and DeepEval—the candidate will distinguish themselves as one of the few engineers who treats AI as a distributed systems reliability problem7. Applications for Job B should begin around Week 18\.

## **Part 11: Final Prioritized Actions**

The execution of this roadmap begins immediately with highly specific tasks.  
**The Five Actions to Complete in the Next Seven Days:**

1. Read Chapter 11 (Stream Processing) of *Designing Data-Intensive Applications*.  
2. Set up the local Go environment and initialize the GitHub repository for Project 1 (Edge Simulator).  
3. Read the Zenoh Protocol Specification overview to understand its 5-byte wire overhead and routing capabilities13.  
4. Rewrite the CV summary to highlight the Loki-to-ClickHouse and NATS-to-JetStream migrations as core architectural scaling wins.  
5. Search LinkedIn for "Data Platform Engineer Robotics" or "Streaming Platform Engineer" to identify target companies and networking opportunities.

**The Top Five Resources to Start Immediately:**

1. *Designing Data-Intensive Applications* (Kleppmann)  
2. Zenoh Protocol Specification  
3. *Streaming Systems* (Akidau et al.)  
4. Terraform Up & Running  
5. Temporal Go SDK Quickstart15

**The First GitHub Deliverable:** A Go binary (edge-simulator) that generates mock JSON telemetry at a configurable rate, accompanied by a thoroughly documented README.md explaining the payload structure and simulating network disconnection logic.  
**Earliest Reasonable Application Dates:**

* **Job A (Platform):** Four weeks from today, upon completion of the Zenoh-to-Kafka bridge.  
* **Job B (Agentic AI):** Eighteen weeks from today, upon completion of the DeepEval and Temporal integration.

**The Ten Highest-Priority Skills:**

1. Durable Execution (Temporal)  
2. High-throughput Streaming (Kafka/JetStream)  
3. Agent Orchestration (PydanticAI)  
4. AI Evaluation (DeepEval/Ragas)  
5. Edge protocols (Zenoh)  
6. Event-time processing (Watermarks)  
7. Vector/Hybrid Search (OpenSearch)  
8. Distributed Observability (OpenTelemetry)  
9. Infrastructure as Code (Terraform)  
10. API Security & Metering

**Three Activities to Explicitly Defer:**

1. Learning C++ or Rust. The candidate must stick to Go and Python to maximize learning velocity and leverage existing strengths.  
2. Fine-tuning LLMs. The focus must remain on orchestration, RAG, and evaluation using existing hosted models.  
3. Learning ROS 2 in depth. The focus must remain on the cloud-side network boundaries where the telemetry lands, rather than the on-robot control loops.

**Clearest Professional Positioning Statement:** "I am a distributed systems engineer who builds the highly reliable, observable infrastructure required to run autonomous fleets and production AI agents at scale."

#### **Works cited**

1. Robotics Platform Engineer (DevOps) \- Jobs in Robotics, AI & Autonomy, [https://www.autonomywork.com/robotics-platform-engineer-devops-fieldai-579](https://www.autonomywork.com/robotics-platform-engineer-devops-fieldai-579)  
2. Software Engineer, Robotics Infrastructure \- Autonomy & Robotics Job in San Francisco, CA at DoorDash \- ZipRecruiter, [https://www.ziprecruiter.com/c/DoorDash/Job/Software-Engineer,-Robotics-Infrastructure-Autonomy-&-Robotics/-in-San-Francisco,CA?jid=63f3015325cc0945](https://www.ziprecruiter.com/c/DoorDash/Job/Software-Engineer,-Robotics-Infrastructure-Autonomy-&-Robotics/-in-San-Francisco,CA?jid=63f3015325cc0945)  
3. Job Application for Senior Robot Infrastructure Engineer at Skild AI \- Greenhouse, [https://job-boards.greenhouse.io/skildai-careers/jobs/5222931008](https://job-boards.greenhouse.io/skildai-careers/jobs/5222931008)  
4. Introduction to DeepEval | DeepEval \- The LLM Evaluation Framework, [https://deepeval.com/docs/introduction](https://deepeval.com/docs/introduction)  
5. Applied AI Engineer Career Path (2026) \- Rockstar Developer University, [https://rockstardeveloperuniversity.com/career-path/applied-ai-engineer-career-path/](https://rockstardeveloperuniversity.com/career-path/applied-ai-engineer-career-path/)  
6. Applied AI Engineer in Irvine, CA, United States \- Qcells Careers, [https://careers.qcells.com/jobs/17819540-applied-ai-engineer](https://careers.qcells.com/jobs/17819540-applied-ai-engineer)  
7. confident-ai/deepeval: The LLM Evaluation Framework \- GitHub, [https://github.com/confident-ai/deepeval](https://github.com/confident-ai/deepeval)  
8. pydantic/pydantic-ai-temporal-example \- GitHub, [https://github.com/pydantic/pydantic-ai-temporal-example](https://github.com/pydantic/pydantic-ai-temporal-example)  
9. Selectors \- Go SDK | Temporal Platform Documentation, [https://docs.temporal.io/develop/go/workflows/selectors](https://docs.temporal.io/develop/go/workflows/selectors)  
10. arXiv:2309.15217v2 \[cs.CL\] 28 Apr 2025, [https://arxiv.org/pdf/2309.15217](https://arxiv.org/pdf/2309.15217)  
11. RAGAS: Automated Evaluation of Retrieval Augmented Generation | by Himanshu Bajpai, [https://bajpaihimanshu.medium.com/papermadeeasy-ragas-automated-evaluation-of-retrieval-augmented-generation-ccfe5ea50db0](https://bajpaihimanshu.medium.com/papermadeeasy-ragas-automated-evaluation-of-retrieval-augmented-generation-ccfe5ea50db0)  
12. DeepEval \- The LLM Evaluation Framework, [https://deepeval.com/](https://deepeval.com/)  
13. What is Zenoh? · Zenoh, [https://zenoh.io/docs/overview/what-is-zenoh/](https://zenoh.io/docs/overview/what-is-zenoh/)  
14. Zenoh \- The Zero Overhead, Pub/Sub, Store, Query, and Compute Protocol., [https://zenoh.io/](https://zenoh.io/)  
15. Go SDK developer guide | Temporal Platform Documentation, [https://docs.temporal.io/develop/go](https://docs.temporal.io/develop/go)  
16. Create llms.txt and llms-full.txt · Issue \#1028 · pydantic/pydantic-ai \- GitHub, [https://github.com/pydantic/pydantic-ai/issues/1028](https://github.com/pydantic/pydantic-ai/issues/1028)  
17. pydantic/pydantic-ai-harness: Batteries for your Pydantic AI agent. \- GitHub, [https://github.com/pydantic/pydantic-ai-harness](https://github.com/pydantic/pydantic-ai-harness)  
18. Observability \- Go SDK | Temporal Platform Documentation, [https://docs.temporal.io/develop/go/platform/observability](https://docs.temporal.io/develop/go/platform/observability)  
19. Zenoh Slides, Videos, Papers and More, [https://zenoh.io/media/](https://zenoh.io/media/)  
20. Abstractions \- Zenoh, [https://zenoh.io/docs/manual/abstractions/](https://zenoh.io/docs/manual/abstractions/)  
21. \[2309.15217\] Ragas: Automated Evaluation of Retrieval Augmented Generation \- arXiv, [https://arxiv.org/abs/2309.15217](https://arxiv.org/abs/2309.15217)  
22. rmw\_zenoh/docs/design.md at rolling \- GitHub, [https://github.com/ros2/rmw\_zenoh/blob/rolling/docs/design.md](https://github.com/ros2/rmw_zenoh/blob/rolling/docs/design.md)  
23. rmw\_zenoh \- ROS Repository Overview, [https://index.ros.org/r/rmw\_zenoh/](https://index.ros.org/r/rmw_zenoh/)  
24. langchain-ai/langgraph: Build resilient agents. \- GitHub, [https://github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)  
25. Anthropic's Applied AI Engineers: The Forward-Deployed Function Behind Claude's Enterprise Strategy | Blog | Perspective AI, [https://getperspective.ai/blog/anthropic-applied-ai-engineers-forward-deployed-claude-enterprise](https://getperspective.ai/blog/anthropic-applied-ai-engineers-forward-deployed-claude-enterprise)  
26. GitHub \- ros2/rmw\_zenoh: RMW for ROS 2 using Zenoh as the middleware, [https://github.com/ros2/rmw\_zenoh](https://github.com/ros2/rmw_zenoh)  
27. eclipse-zenoh/zenoh-plugin-ros2dds: A Zenoh plug-in for ROS2 with a DDS RMW. See https://discourse.ros.org/t/ros-2-alternative-middleware-report/ for the advantages of using this plugin over other DDS RMW implementations. · GitHub \- GitHub, [https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds](https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds)  
28. Unit Testing in CI/CD | DeepEval \- The LLM Evaluation Framework, [https://deepeval.com/docs/evaluation-unit-testing-in-ci-cd](https://deepeval.com/docs/evaluation-unit-testing-in-ci-cd)  
29. About Temporal SDKs | Temporal Platform Documentation, [https://docs.temporal.io/encyclopedia/temporal-sdks](https://docs.temporal.io/encyclopedia/temporal-sdks)
