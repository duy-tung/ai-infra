# Báo cáo Deep Research: Thẩm định kỹ thuật kế hoạch 24 tuần chuyển sang AI Infrastructure / Inference Platform

**Ngày nghiên cứu:** 2026-07-08
**Phương pháp:** Deep-research workflow đa agent (105 agents, 5 hướng tìm kiếm độc lập, 23 nguồn fetch, 89 claims trích xuất, 25 claims đưa vào adversarial verification 3 phiếu — 24 claims được xác nhận 3-0, 1 claim bị bác bỏ 0-3). Code citations được đối chiếu trực tiếp với `vllm-project/vllm` main branch tại thời điểm 2026-07-08.

**Quy ước phân loại độ tin cậy (dùng xuyên suốt báo cáo):**

| Nhãn | Ý nghĩa |
|---|---|
| **[FACT]** | Đã xác minh qua adversarial verification 3-0, đối chiếu nguồn gốc (paper, source code, official docs) |
| **[CLAIM]** | Trích từ nguồn có thẩm quyền nhưng chưa qua vòng verify độc lập, hoặc là self-reported của vendor |
| **[SUY LUẬN]** | Suy luận kỹ thuật của người viết từ các facts đã xác minh |
| **[KHUYẾN NGHỊ]** | Đề xuất hành động — có thể tranh luận, dựa trên kinh nghiệm và ràng buộc thời gian |
| **[CHƯA XÁC MINH]** | Kiến thức nền phổ biến nhưng workflow chưa verify — phải tự kiểm chứng trước khi dựa vào |

**Cảnh báo phạm vi bằng chứng (quan trọng, đọc trước):**

1. Toàn bộ bằng chứng đã xác minh nghiêng nặng về **vLLM**. Không có claim nào về SGLang runtime, Triton Inference Server, TensorRT-LLM, llama.cpp, TGI, Ray Serve, KServe được verify độc lập — các phần so sánh framework liên quan được ghi rõ mức tin cậy thấp hơn.
2. Một claim quan trọng đã bị **bác bỏ 0-3**: "prefix-cache-aware load balancing, fairness/priority, disaggregated serving vẫn là roadmap items chưa ship ở tầng gateway chuẩn". Thực tế: **chúng đã shipped** (Gateway API Inference Extension GA v1.5.0, llm-d KV-cache-aware routing đang chạy production). Không gian khác biệt hóa của dự án **hẹp hơn giả định ban đầu** — điều này thay đổi cách định vị dự án (xem Section 1).
3. Hệ sinh thái thay đổi nhanh: vLLM async scheduling chỉ bật mặc định từ ~11/2025; builtin-hash cho prefix caching đã deprecated sang SHA-256; Endpoint Picker (EPP) đang migrate từ `kubernetes-sigs/gateway-api-inference-extension` sang `llm-d/llm-d-router`. Mọi trích dẫn code trong báo cáo đúng tại 2026-07-08 — hãy re-verify khi bắt đầu code.

---

## Section 1: Executive architecture verdict

### 1.1. Dự án flagship có credible không?

**CÓ — nhưng chỉ khi tái định vị.** Kết luận này dựa trên hai nhóm facts đối lập:

**[FACT] Mặt bằng cạnh tranh đã chuẩn hóa hơn kế hoạch giả định:**

- **LiteLLM** (52.9k stars, v1.91.0 phát hành 2026-07-04, rất active) đã chiếm trọn product space "OpenAI-compatible self-hosted multi-backend gateway": virtual keys, per-tenant spend/cost tracking, budgets với `budget_duration`, TPM/RPM limits per key/user/team, load balancing, fallbacks, guardrails, admin dashboard — và route được tới cả vLLM/Ollama. **[CLAIM]** LiteLLM tự công bố gateway overhead 8ms P95 tại 1,000 RPS (vendor self-report — đây là baseline có thể falsify mà benchmark của bạn nên so sánh).
- **Kubernetes SIG Gateway API Inference Extension** đã GA (v1.5.0, 4/2026): biến các ext-proc capable proxies (Envoy Gateway, kgateway, GKE Gateway) thành "inference gateways". Inference-aware scheduling nằm trong **Endpoint Picker (EPP)** — data-plane component giao tiếp với proxy qua Envoy external processing protocol, thuật toán chọn endpoint extensible, **KV-cache aware và request-cost aware**.
- **llm-d** (IBM/Google/Red Hat) implement KV-cache-aware routing NGOÀI engine: KV cache indexer duy trì "global, near-real-time view of KV cache block locality" trên fleet vLLM pods, cập nhật qua **KVEvents** do vLLM emit; scheduler viết bằng Go (~96.5%), score pods theo prefix-cache hits. **[CLAIM]** blog llm-d báo cáo ~3x giảm mean TTFT ở 4 QPS.

**[FACT] Nhưng ranh giới trách nhiệm mà kế hoạch của bạn đặt ra là ĐÚNG về mặt kiến trúc:** continuous batching, token-granularity scheduling, KV-cache management là internals không thể tách khỏi inference engine (chi tiết Section 2). Một Go gateway đứng TRƯỚC các cơ chế đó — admission control, tenant quota, routing, đo lường — là đúng chỗ.

**[SUY LUẬN] Hệ quả định vị:** dự án KHÔNG credible nếu pitch là "tôi xây một LLM gateway" (câu trả lời của hiring manager: "sao không dùng LiteLLM?"). Dự án RẤT credible nếu pitch là **"depth artifact"**: *"Tôi xây gateway từ đầu để chứng minh tôi hiểu chính xác cái gì thuộc về gateway, cái gì thuộc về engine, và tôi đo được từng quyết định — token-aware admission control gắn với backend batching state, TTFT/ITL đo nghiêm ngặt, failure injection có postmortem — những thứ LiteLLM không làm (TPM limit của LiteLLM là control-plane per-minute quota; scheduler priority của nó là beta Redis-polling)."* Sự khác biệt nằm ở **độ sâu data-plane + bằng chứng đo lường + tường thuật reliability**, không phải ở sự tồn tại của feature list.

### 1.2. Các phán quyết chính

| Câu hỏi | Phán quyết |
|---|---|
| Chuyên môn hóa | **Inference Platform / AI Platform Engineer** — tận dụng 6 năm Go/distributed-systems, KHÔNG cạnh tranh ở kernel layer trong 24 tuần |
| Phạm vi dự án | 1 flagship repo (gateway + benchmark + reliability evidence), 1 mini-eval harness bên trong repo đó. Loại bỏ: Triton, TensorRT-LLM, Ray Serve, KServe, agent runtime, full eval platform |
| Backend đầu tiên | **Mock backend → llama.cpp (local, không GPU) → vLLM (GPU thuê, backend "thật" duy nhất)** |
| Backend so sánh | SGLang — chỉ ở mức benchmark comparison trên prefix-heavy workload (stretch goal), không tích hợp sâu |
| Ngôn ngữ | **Go ~75–80%** (gateway, control plane, load generator), **Python ~20–25%** (đọc vLLM internals, script benchmark/eval, glue). **C++/CUDA: KHÔNG code trong 24 tuần đầu** — chỉ literacy đọc hiểu + GPU profiling khái niệm (Section 10) |
| Rủi ro kỹ thuật lớn nhất | (1) Scope explosion — feature list đề xuất là ~3 năm công việc; (2) benchmark không hợp lệ làm hỏng credibility; (3) chi phí/tiếp cận GPU; (4) vô tình duplicate chức năng engine (double-queueing) |
| Đơn giản hóa chủ lực | Single-node gateway (multi-replica chỉ ở mức thiết kế tài liệu); PostgreSQL cho mọi state bền; không message queue trong request path; 2 backends thực tế thay vì 5 |

### 1.3. Vì sao vẫn đáng xây thay vì dùng LiteLLM/GAIE rồi viết blog?

**[SUY LUẬN]** Với hồ sơ của bạn, giá trị tuyển dụng nằm ở chỗ chứng minh **chuyển giao được** kỹ năng distributed-systems sang ngữ cảnh inference. Fork LiteLLM không chứng minh được điều đó — LiteLLM là Python (~85.7% codebase **[FACT]**), và đóng góp vào đó không phô diễn được Go concurrency, backpressure, cancellation semantics là thế mạnh của bạn. Gateway API Inference Extension thì ngược lại: **nên đọc source (Go) và so sánh thiết kế** — nó là "đáp án chuẩn của ngành" để đối chiếu với thiết kế của bạn (Section 7).

---

## Section 2: Architecture review

### 2.1. Ranh giới đã bị engine quyết định sẵn — gateway không có lựa chọn

Đây là nhóm facts quan trọng nhất của toàn bộ nghiên cứu, vì nó xác định **nơi trách nhiệm của Go gateway kết thúc**:

**[FACT] vLLM V1 scheduler xóa bỏ phân biệt prefill/decode và scheduling ở granularity token:**
- Scheduler trộn cả prefill và decode requests trong cùng một engine step; quyết định scheduling biểu diễn dưới dạng dict `{request_id: num_tokens}` với token budget cố định (`token_budget = self.max_num_scheduled_tokens`), hỗ trợ natively chunked prefill, prefix caching, speculative decoding.
- Code main branch: `vllm/v1/core/sched/scheduler.py` có comment nguyên văn *"There's no 'decoding phase' nor 'prefill phase' in the scheduler"*; `vllm/v1/core/sched/output.py` khai báo `num_scheduled_tokens: dict[str, int]`.
- Scheduler ưu tiên decode requests trong running queue trước khi nhận prefill từ waiting queue.
- Async single-step scheduling (scheduler lập kế hoạch step n+1 trong khi worker thực thi step n) — RFC #8779, implement qua PR #19970, bật mặc định từ ~11/2025 (PR #27614).

**[FACT] Ranh giới process bên trong vLLM:** API server process tự làm input processing (tokenization, multi-modal loading) và streaming kết quả về client, giao tiếp với **EngineCore process** (chỉ chứa scheduler + model executor, chạy busy loop — `EngineCoreProc`, docstring *"ZMQ-wrapper for running EngineCore in background process"*) qua ZMQ sockets. Kể cả single-GPU deployment cũng chạy tối thiểu 2 processes. Động cơ (RFC #8779, simon-mo, 2024-09-24): *"De-tokenization is expensive. For every step, vLLM de-tokenizes the generated output token IDs and checks the stop criteria"* — tối thiểu hóa GPU idle time do CPU-side work. (Caveat: mô tả này áp dụng cho serving path `AsyncLLM`; offline `LLM` class có thể chạy in-process qua `InprocClient`.)

**[FACT] vLLM đã tự làm load balancing nội bộ giữa data-parallel replicas:** `DPLBAsyncMPClient` chọn engine có score tối thiểu với công thức nguyên văn trong `vllm/v1/engine/core_client.py`: `score = len(waiting) * 4 + len(running)`, dựa trên queue-state do `DPCoordinator` process publish qua ZMQ XPUB (~100ms interval).

**[SUY LUẬN] Ba hệ quả kiến trúc bắt buộc:**
1. Queue ở Go gateway chỉ đứng **TRƯỚC** continuous batching: admission, ordering, priority hint (truyền qua request parameter), quota. Nó **không thể tham gia** hình thành batch mỗi step — và không được cố.
2. Tokenization/detokenization/token streaming là trách nhiệm nội bộ runtime. Gateway chỉ **relay SSE** và **ước lượng** token count cho quota (đếm chính xác lấy từ `usage` field trong response).
3. Health-aware routing của gateway hoạt động ở mức **deployment/replica** (chọn giữa các vLLM deployments), không ở mức DP-rank bên trong một deployment — vLLM tự làm việc đó rồi.

### 2.2. Kiến trúc đã hiệu chỉnh

```text
                              CONTROL PLANE (Go + PostgreSQL)
                    ┌────────────────────────────────────────────┐
                    │  Admin API (gRPC/REST):                    │
                    │   - Tenant / API key CRUD                  │
                    │   - Model registry (model -> backend map)  │
                    │   - Quota & priority policy                │
                    │   - Config version publish                 │
                    │  PostgreSQL: tenants, keys, models,        │
                    │   quotas, usage rollups, config versions   │
                    └───────────────┬────────────────────────────┘
                                    │ config snapshot (poll /
                                    │ LISTEN-NOTIFY, versioned,
                                    │ atomic swap in-memory)
                                    ▼
Clients ──HTTP/SSE──▶ ┌────────────────────────────────────────────┐
                      │  DATA PLANE: Go Gateway (single binary)    │
                      │  1. AuthN (API key -> tenant, cache)       │
                      │  2. Request validation + size limits       │
                      │  3. Token estimation (input) + quota check │
                      │  4. Token-aware rate limit (per tenant)    │
                      │  5. Admission control + bounded queue      │
                      │     (per model-pool, priority + fairness,  │
                      │      queue timeout, shed on overflow)      │
                      │  6. Router: model -> backend pool,         │
                      │     health/load-aware pick, fallback       │
                      │  7. Reliability: retry budget (pre-stream  │
                      │     only), circuit breaker, timeouts       │
                      │  8. SSE relay + per-token timestamps       │
                      │     (TTFT/ITL đo tại gateway)              │
                      │  9. Usage accounting (async, batched       │
                      │     write-behind -> PostgreSQL)            │
                      │  10. OTel traces + Prometheus metrics      │
                      └───────┬──────────────┬─────────────────────┘
                              │ HTTP/SSE     │ HTTP/SSE
                              ▼              ▼
                   ┌──────────────┐  ┌──────────────────────────┐
                   │ Mock backend │  │ vLLM (OpenAI-compatible  │
                   │ (Go, cho dev │  │  API server + EngineCore │
                   │  + fault inj)│  │  + /metrics)             │
                   └──────────────┘  │ llama.cpp llama-server   │
                                     │  (local dev, CPU)        │
                                     └──────────────────────────┘
```

Khác biệt so với kiến trúc đề xuất ban đầu:

| Đề xuất ban đầu | Hiệu chỉnh | Lý do |
|---|---|---|
| "Go Gateway / Control Plane" là một khối | Tách control plane (admin API + Postgres) khỏi data plane (request path), dù cùng binary lúc đầu | Ranh giới này là câu hỏi phỏng vấn kinh điển; GAIE cũng tách EPP (data plane) khỏi CRD/config (control plane) **[FACT]** |
| 4–5 backends (llama.cpp, vLLM, Triton, SGLang/Ray Serve) | Mock + llama.cpp + vLLM; SGLang chỉ để benchmark so sánh | Mỗi backend tích hợp sâu tốn 15–25h; giá trị học giảm dần mạnh sau backend thứ 2 |
| Message queue trong hệ thống | **Không MQ trong request path.** Tùy chọn: NATS JetStream cho usage-event pipeline (async accounting) — stretch | Request inference là request/response streaming đồng bộ; MQ ở giữa phá hỏng cancellation và thêm latency vô nghĩa. Usage events thì hợp — và chơi đúng thế mạnh CDC/JetStream của bạn |
| Kubernetes + autoscaling là hạng mục lớn | K8s deploy cơ bản (manifests, HPA demo trên mock backend); autoscaling GPU thật: chỉ tài liệu thiết kế | Autoscaling GPU thật cần fleet GPU — ngoài ngân sách; HPA trên metric tùy chỉnh với mock backend đủ để nói chuyện phỏng vấn |

### 2.3. Sở hữu state

| State | Nơi sống | Ghi chú |
|---|---|---|
| Tenants, API keys (hash), quota policies | PostgreSQL | Nguồn chân lý; cache read-through trong gateway với TTL + version check |
| Model registry (model name → backend pool, context limits, giá) | PostgreSQL | Config version tăng đơn điệu; gateway giữ snapshot immutable trong memory, swap nguyên tử |
| Usage/cost accounting | PostgreSQL (rollup); ghi async batched | KHÔNG ghi đồng bộ trong request path. Chấp nhận mất ≤ vài giây usage khi crash — ghi rõ trade-off này trong docs (hiring manager thích sự trung thực này hơn exactly-once giả) |
| Rate-limit counters, queue state, circuit-breaker state, backend health | In-memory (gateway process) | Single-node: đúng đắn tuyệt đối. Multi-replica: ghi tài liệu thiết kế (per-replica quota chia theo tỷ lệ, hoặc Redis token bucket) — KHÔNG implement |
| KV cache, batch state, per-step scheduling | **Bên trong vLLM** — gateway không nhìn thấy, không sao chép | **[FACT]** — xem 2.1 |

**[SUY LUẬN] Tính năng nào cần distributed coordination → loại khỏi phạm vi 24 tuần:** global exact rate limiting giữa nhiều gateway replicas, distributed queue với thứ tự toàn cục, leader election cho config push. Tất cả có thể (và nên) ở lại single-node cho portfolio; tài liệu "cách tôi sẽ scale ra N replicas" là artifact phỏng vấn tốt hơn một implementation Redis-lock lỗi.

### 2.4. Request flow / Failure flow / Cancellation flow / Configuration flow

**Request flow (happy path):** nhận HTTP → auth (cache hit) → validate + ước lượng input tokens (tokenizer offline hoặc heuristic bytes/4, ghi rõ sai số) → check quota + token-bucket → enqueue vào bounded queue của model pool (nếu đầy: 429 kèm `Retry-After` hoặc shed theo priority) → dequeue theo priority + fairness → router chọn backend healthy (least-inflight, sau này cân nhắc queue-depth từ backend metrics) → forward, relay SSE từng chunk, đóng dấu timestamp mỗi chunk (TTFT = chunk đầu có content; ITL = hiệu giữa các chunk) → khi stream kết thúc, đọc `usage` từ chunk cuối (vLLM trả usage khi `stream_options.include_usage=true` — **[CHƯA XÁC MINH]** verify tuần 1) → ghi usage async → emit metrics + trace.

**Failure flow:** phân loại lỗi làm ba lớp — (a) **lỗi trước khi gửi backend** (auth, quota, queue full): trả 4xx/429 ngay, rẻ; (b) **lỗi trước first token** (connect refused, timeout, 5xx từ backend): đủ điều kiện retry sang backend khác trong retry budget; (c) **lỗi giữa stream** (backend chết giữa chừng): **KHÔNG retry tự động** — client đã nhận partial tokens, retry sẽ tạo duplicate content và tính phí đôi; trả SSE error event chuẩn + đóng stream, để client quyết. Circuit breaker mở theo backend khi tỷ lệ lỗi lớp (b) vượt ngưỡng — bảo vệ pool khỏi backend chết, KHÔNG đếm lỗi lớp (c) đơn lẻ vào breaker (một stream đứt không có nghĩa backend chết; connect failures liên tiếp mới có nghĩa).

**Cancellation flow:** client đóng connection → Go `context.Context` cancel lan qua toàn bộ chain → gateway đóng upstream HTTP request tới vLLM → vLLM abort request đang chạy, giải phóng KV blocks. **[SUY LUẬN]** đây là nơi nền tảng WebSocket-gateway của bạn tỏa sáng và là demo phỏng vấn rất mạnh: chứng minh bằng metric rằng cancel ở client giải phóng slot ở backend trong <100ms (quan sát `num_requests_running` giảm — **[CHƯA XÁC MINH]** tên metric, verify tuần 1). Trường hợp cạnh phải xử lý: request đã vào bounded queue nhưng client hủy trước khi dequeue — phải remove khỏi queue (lazy remove với tombstone hoặc check `ctx.Err()` lúc dequeue).

**Configuration flow:** admin ghi Postgres → tăng `config_version` → gateway poll mỗi 2–5s (hoặc `LISTEN/NOTIFY`) → build snapshot mới → validate → atomic pointer swap → request mới dùng snapshot mới, request đang bay giữ snapshot cũ (immutability = không cần lock trong request path). Đây là mô hình GAIE/Envoy xDS thu nhỏ và là câu chuyện phỏng vấn tốt về config consistency.

---

## Section 3: MVP và kế hoạch milestone (12 × 2 tuần)

Ngân sách giờ dự án: **~200h** trong tổng 480h (xem Section 14 cho phân bổ tổng). Mỗi milestone kết thúc bằng demo chạy được + artifact viết.

| # | Tuần | Tính năng | Mục tiêu học | Bằng chứng/artifact | Tiêu chí chấp nhận | Giờ | Rủi ro chính |
|---|---|---|---|---|---|---|---|
| M1 | 1–2 | Go gateway skeleton + **mock backend** (Go): `/v1/chat/completions` OpenAI-compatible, SSE streaming, context cancellation end-to-end | Anatomy của OpenAI API + SSE semantics; prefill/decode ở mức khái niệm | Repo + demo `curl` streaming; sequence diagram request path | Stream hoạt động; hủy client → goroutine + upstream đóng ≤100ms (test tự động chứng minh) | 18 | SSE chunk format sai chuẩn OpenAI → client libs không parse được |
| M2 | 3–4 | AuthN (API key), tenant model, PostgreSQL registry (tenants/keys/models/quotas), usage accounting async | State ownership; write-behind accounting | Schema + ERD; integration tests | Key sai → 401; usage khớp ±1 request khi tải 100 RPS lên mock | 16 | Ghi usage đồng bộ lẻn vào request path làm hỏng latency |
| M3 | 5–6 | Token-aware rate limiting (token bucket theo tokens/phút mỗi tenant), admission control, bounded queue + queue timeout, load shedding | Vì sao RPS limit thất bại với LLM; token estimation và sai số | Blog note "Token-aware rate limiting: input estimate vs usage reconcile"; load test cho thấy 429 sạch dưới quá tải | Quá tải 5x: p99 của request được nhận vẫn ổn định; requests bị shed nhận 429+`Retry-After` <5ms | 18 | Ước lượng token sai lệch lớn → quota vô nghĩa; phải reconcile bằng usage thật |
| M4 | 7–8 | Backend thật #1: **llama.cpp** (`llama-server`, CPU local); đo TTFT/ITL tại gateway; OTel tracing xuyên suốt | TTFT/ITL/TPOT định nghĩa chuẩn; trace model đúng cho streaming | Grafana dashboard v1; trace mẫu có span queue/backend/stream | TTFT, ITL p50/p95/p99 per model hiển thị đúng (so chéo với đo client-side, sai số <5%) | 18 | Buffering ẩn (Go bufio, proxy) làm sai TTFT — phải flush mỗi chunk |
| M5 | 9–10 | Backend thật #2: **vLLM trên GPU thuê** (1× A10/A100/4090, ~20–40h GPU); scrape `/metrics` của vLLM; health-aware routing v1 (least-inflight + health check) | vLLM V1 architecture (đọc code tuần này — Section 7); metrics engine phơi bày gì | Ghi chú "vLLM /metrics catalog" (đóng open question); routing quyết định có log lý do | Gateway route giữa 2 vLLM replicas; kill 1 replica → traffic chuyển ≤2s, không request nào treo quá timeout | 18 | Chi phí GPU; version drift vLLM; **mở open question #1 (metrics) — phải verify thực nghiệm** |
| M6 | 11–12 | Priority (2–3 lớp) + fairness giữa tenants (weighted round-robin theo token đã dùng trong cửa sổ trượt) + chống starvation (aging) | Scheduling policy vs mechanism; DRF ở mức khái niệm | Thí nghiệm: tenant tham lam không chiếm >X% khi có cạnh tranh (đồ thị) | Với 3 tenants (1 spam), fairness giữ tỷ lệ phục vụ ±10% mục tiêu; không starvation (max wait có bound) | 18 | Over-engineering thành scheduler thứ hai — chỉ reorder TRƯỚC khi gửi backend **[FACT constraint]** |
| M7 | 13–14 | Reliability: retry budget (chỉ pre-first-token, budget 10–20% có metric), circuit breaker per-backend, graceful shutdown (drain streams có deadline), model fallback | Retry semantics cho streaming; breaker bảo vệ cái gì | Bảng error taxonomy; test fault: kill backend giữa stream → error event sạch, không retry đôi | Shutdown dưới tải: 0 request rơi (drain ≤30s); breaker mở/đóng đúng kịch bản | 18 | Retry giữa stream lẻn vào (duplicate tokens) — phải có test khẳng định KHÔNG retry |
| M8 | 15–16 | Benchmark suite v1: Go load generator (Poisson arrivals, phân phối prompt/output cấu hình được) HOẶC dùng `vllm bench serve`; concurrency sweep; đo **gateway overhead** (có/không gateway) | Phương pháp benchmark chuẩn (Section 8); vì sao mean là dối trá | Báo cáo benchmark v1 (markdown + đồ thị): TTFT/ITL/goodput theo concurrency; overhead gateway p50/p99 so với direct | Kết quả tái lập được (3 runs, median±range); overhead gateway được số hóa và so được với LiteLLM 8ms claim | 18 | Benchmark theater — đo sai còn tệ hơn không đo (Section 13) |
| M9 | 17–18 | Failure injection campaign + SLO doc + **incident postmortem** (viết như thật) | Overload detection; shedding order; SLO cho streaming | 5 thí nghiệm fault có kịch bản + kết quả + đồ thị; postmortem 1 sự cố tự gây | Mỗi fault: hành vi đúng dự đoán hoặc bug được fix + regression test | 16 | Fault experiments không có giả thuyết trước → thành "chọc cho vui" không có giá trị chứng minh |
| M10 | 19–20 | Kubernetes deploy (k3s/kind local + 1 GPU node cloud cho vLLM): manifests, probes, HPA demo trên mock backend, config reload dưới tải | K8s cơ bản cho GPU workloads (device plugin, resource limits) ở mức vận hành | Helm chart/manifests; runbook triển khai; demo config đổi model routing không rớt request | Rolling restart gateway: 0 lỗi client (nhờ drain M7); HPA scale mock pool theo custom metric | 16 | Chìm vào YAML — timebox chặt; GPU node K8s chỉ cần chạy được, không cần đẹp |
| M11 | 21–22 | Thí nghiệm so sánh: vLLM vs SGLang (hoặc vLLM có/không prefix caching) trên workload prefix-heavy vs không chia sẻ prefix; capacity planning doc | RadixAttention vs PagedAttention prefix caching; vì sao workload quyết định kết quả **[FACT: 6.4x của SGLang chỉ trên multi-call/prefix-heavy]** | Báo cáo so sánh có kiểm soát prefix-sharing ratio; capacity model (tokens/s/GPU → cost/1M tokens) | Kết luận nêu rõ điều kiện đúng; capacity estimate đối chiếu số đo thật ±30% | 14 | SGLang setup ngốn giờ — fallback: so vLLM prefix-caching on/off vẫn đạt mục tiêu học |
| M12 | 23–24 | Portfolio packaging: README kiến trúc (diagrams), 2–3 bài viết kỹ thuật, demo video 5', benchmark report cuối, "design for scale-out" doc | Kể chuyện kỹ thuật bằng tiếng Anh | Repo public hoàn chỉnh; bài viết đăng | Người lạ clone chạy được demo trong 15' (docker compose); README trả lời "why not LiteLLM" ngay đầu | 12 | Viết lách bị bỏ đói giờ — đây là thứ hiring manager đọc ĐẦU TIÊN, không được cắt |

**Tổng: ~200h.** Mỗi milestone lẻ (M5, M7, M9) tạo demo "wow" cho phỏng vấn: routing failover, drain-under-load, fault campaign.

**MVP nhỏ nhất có credibility** (nếu mọi thứ trượt): M1–M5 + M8 = gateway streaming đa tenant, quota token-aware, một backend GPU thật, benchmark có phương pháp. ~106h. Dưới mức đó dự án không đủ khác biệt với "proxy cuối tuần".

---

## Section 4: Bảng ưu tiên phạm vi

| Tính năng đề xuất | Phân loại | Ghi chú |
|---|---|---|
| OpenAI-compatible API (chat completions + streaming) | **Must have** | Bề mặt chuẩn de-facto; vLLM/llama.cpp/SGLang đều nói được **[FACT cho vLLM]** |
| Streaming SSE + cancellation propagation | **Must have** | Điểm phô diễn thế mạnh WebSocket/Go của bạn |
| Tenant + API key + quota (PostgreSQL) | **Must have** | Multi-tenancy là chữ ký của đề bài |
| Token-aware rate limiting (estimate + reconcile) | **Must have** | Khác biệt hóa thật so với RPS limiter; LiteLLM TPM là per-minute control-plane quota **[FACT]** |
| Bounded queue + queue timeout + load shedding | **Must have** | Đất diễn backpressure — thế mạnh sẵn có |
| Health-aware routing + failover giữa replicas | **Must have** | Ở mức deployment/pool; per-DP-rank đã có vLLM lo **[FACT]** |
| TTFT/ITL/queue-wait/tail-latency metrics + OTel traces | **Must have** | Đây là "sản phẩm" thật của dự án |
| Benchmark suite + báo cáo có phương pháp | **Must have** | Không có nó, mọi claim khác vô giá trị |
| Retry budget (pre-first-token only) + circuit breaker | **Strong signal** | Semantics đúng quan trọng hơn feature |
| Priority + fairness + chống starvation | **Strong signal** | Giới hạn: reorder trước backend, không "scheduler thứ hai" |
| Graceful shutdown drain long generations | **Strong signal** | Demo phỏng vấn mạnh, chi phí thấp |
| Failure injection + postmortem | **Strong signal** | Hiếm trong portfolio → nổi bật |
| Model fallback (model A lỗi → model B) | **Nice to have** | Dễ làm sau routing; cẩn thận semantics (model khác = kết quả khác, phải ghi vào response) |
| Config hot reload (versioned snapshot) | **Nice to have** | Rẻ nếu làm từ M2 đúng cách |
| Usage/cost accounting + cost per request | **Nice to have** | Bảng giá tĩnh × usage; đủ cho demo |
| Kubernetes deployment cơ bản | **Nice to have** | Manifests + probes + runbook; đừng chìm sâu |
| Batching experiments (ảnh hưởng gateway concurrency lên batch của vLLM) | **Nice to have** | Một thí nghiệm trong benchmark report là đủ |
| SGLang so sánh benchmark | **Postpone → stretch M11** | Không có verified claims về runtime; fallback là vLLM prefix on/off |
| NVIDIA Triton integration | **Postpone** | Không GPU + không TensorRT-LLM thì Triton chỉ còn là generic server — giá trị học thấp cho gateway này; đọc docs kiến trúc là đủ **[SUY LUẬN]** |
| TensorRT-LLM | **Reject (trong 24 tuần)** | Cần GPU NVIDIA + C++ depth; thuộc lộ trình NVIDIA-style sau tuần 24 |
| Ray Serve / KServe integration | **Reject** | Lớp orchestration khác bài toán; đọc khái niệm 2h là đủ |
| Autoscaling GPU thật | **Reject → design doc** | Cần fleet; HPA demo trên mock + tài liệu thiết kế thay thế |
| Message queue trong request path | **Reject** | Phá cancellation, thêm latency; chỉ dùng cho usage events nếu dư giờ |
| Distributed rate limiting / multi-replica gateway | **Reject → design doc** | Single-node + tài liệu scale-out |
| Agent runtime, full eval platform | **Postpone** | Section 11 |
| Semantic caching, guardrails/content filtering | **Reject** | Product feature, không phải systems depth |

---

## Section 5: So sánh framework (decision matrix)

**Mức tin cậy:** hàng vLLM dựa trên **[FACT]** đã verify; các hàng khác là **[CHƯA XÁC MINH]** — kiến thức nền + docs chính thức, chưa qua adversarial verification (caveat #1 của nghiên cứu). Điểm 1–5 là đánh giá tổng hợp của người viết cho MỤC ĐÍCH DỰ ÁN NÀY (không phải chất lượng tuyệt đối).

| Tiêu chí | vLLM | SGLang | Triton | TensorRT-LLM | llama.cpp | TGI | Ray Serve | KServe |
|---|---|---|---|---|---|---|---|---|
| Primary abstraction | Continuous-batching engine per-request | "LM program" (multi-call + control flow) **[FACT theo paper]** | Đa-framework model server (backend plugins) | Compiled engine + batch manager | Single-model CPU/GPU inference lib + server | Serving engine (Rust router + Python shards) | Generic service graph trên Ray | K8s CRD serving orchestration |
| Scheduling/batching | Token-budget unified scheduler, chunked prefill **[FACT]** | Cache-aware scheduling, RadixAttention **[FACT theo paper]** | Delegate cho backend | In-flight batching (C++) | Batch nhỏ, đơn giản | Continuous batching | Không có (delegate) | Không có (delegate) |
| KV-cache mgmt | PagedAttention, block 16 tokens, SHA-256 prefix hash **[FACT]** | Radix tree + LRU **[FACT theo paper]** | Theo backend | Paged KV (C++) | Đơn giản, per-slot | PagedAttention-derived | N/A | N/A |
| OpenAI-compatible API | Có, + Anthropic Messages API + gRPC **[FACT]** | Có | Không trực tiếp (cần adapter) | Qua Triton/NIM | Có (`llama-server`) | Có (subset) | Tự viết | Tự viết |
| Yêu cầu phần cứng | GPU (có CPU mode x86/ARM **[FACT]**, chậm) | GPU | GPU/CPU | GPU NVIDIA | **CPU OK** | GPU | Bất kỳ | Cluster |
| Local dev không GPU | Trung bình (CPU mode chậm) | Kém | Trung bình | Không | **Xuất sắc** | Kém | Tốt | Kém |
| Độ phức tạp vận hành | Trung bình | Trung bình | Cao | Cao | **Thấp** | Trung bình | Cao | Cao |
| Observability sẵn | Prometheus /metrics **[CHƯA XÁC MINH chi tiết]** | Có | Tốt | Qua Triton | Cơ bản | Tốt | Ray dashboard | K8s-native |
| Benchmark tooling | **`vllm bench {serve,latency,throughput}` first-party [FACT]** | Có script | perf_analyzer | Có | Có | Có | Không chuyên | Không |
| Maintenance (7/2026) | **Rất active: v0.24.0 (2026-06-29), ~85.7k stars, ~2.9k contributors [FACT]** | Active **[CHƯA XÁC MINH]** | Active (NVIDIA) | Active (NVIDIA) | Rất active | Chậm lại **[CHƯA XÁC MINH]** | Active | Active |
| Đọc source dễ | **Cao — scheduler/engine là Python thuần [FACT: 84.5% Python]** | Cao (Python) | Thấp (C++) | Thấp (C++) | Trung bình (C, một file lớn) | Trung bình (Rust+Python) | Trung bình | Trung bình (Go) |
| Giá trị cho dự án | **5** | 3 | 1 | 1 | **4 (local dev)** | 2 | 1 | 1 |
| Giá trị phỏng vấn | **5** | 4 | 2 | 3 (NVIDIA path) | 2 | 2 | 2 | 2 |

**Kết luận:**
- **Backend đầu tiên để implement:** **vLLM** — ba lý do đã verify: (1) OpenAI-compatible + Anthropic + gRPC nghĩa là gateway front nó không cần sửa runtime, đúng pattern production (LiteLLM, Envoy AI Gateway, GAIE đều làm vậy); (2) scheduler + engine internals là Python thuần (`vllm/v1/core/sched/`, `vllm/v1/engine/`) — đọc được mà không cần C++/CUDA; (3) `vllm bench` cho sẵn phương pháp benchmark chuẩn. **[FACT cả ba]**
- **Backend phụ trợ dev:** llama.cpp `llama-server` để phát triển local không GPU (mock backend vẫn là công cụ chính cho fault injection).
- **Backend thứ hai để so sánh:** SGLang — chỉ benchmark trên prefix-heavy workload, vì **[FACT theo paper]** con số 6.4x của SGLang chỉ đúng trên multi-call/prefix-heavy/structured workloads; so sánh không kiểm soát prefix-sharing ratio là so sánh không hợp lệ. Fallback ít rủi ro hơn: vLLM prefix-caching on/off.
- **Học nhưng không implement:** Gateway API Inference Extension + llm-d (đọc Go source — Section 7), Triton (đọc kiến trúc backend/model-repository), DistServe (paper).
- **Hoãn hẳn:** TensorRT-LLM, Ray Serve, KServe, TGI.

---

## Section 6: Paper deep dives (5 papers chính + 2 phụ, tổng ~20–24h đọc)

### P1. "Efficient Memory Management for Large Language Model Serving with PagedAttention" (Kwon et al., SOSP 2023; arXiv:2309.06180) — BẮT BUỘC, đọc đầu tiên

- **Vấn đề chính xác:** hệ thống serving pre-vLLM cấp phát KV cache theo buffer contiguous max-length; **[FACT]** chỉ 20.4%–38.2% KV-cache memory thực sự chứa token states — phần còn lại mất vào reservation, internal/external fragmentation → giới hạn batch size → giới hạn throughput.
- **Đóng góp then chốt:** PagedAttention — chia KV cache thành fixed-size blocks lưu non-contiguous, analogy OS paging (**[FACT]** nguyên văn: "blocks as pages, tokens as bytes, requests as processes"); loại bỏ external fragmentation; cho phép KV sharing granularity block (parallel sampling, prefix sharing).
- **Kiến trúc:** centralized scheduler + block manager (logical→physical block table) + distributed workers; co-design memory management với preemptive request scheduling (all-or-nothing eviction: swap hoặc recompute).
- **Thuật toán/data structures quan trọng:** block table per request; copy-on-write khi share block; preemption policy (victim = request đến sau).
- **Đánh giá:** **[FACT]** 2–4x throughput cùng mức latency vs FasterTransformer và Orca; lợi thế tăng với sequence dài hơn, model lớn hơn, decoding phức tạp hơn.
- **Giới hạn & những gì đã bị vượt qua:** Orca baseline là reimplementation của chính tác giả (Orca không open-source); FasterTransformer đã deprecated. **[CLAIM]** vAttention (arXiv:2405.04437) chỉ ra paged decode kernel tự thân chậm hơn 20–26% so với non-paged — critique kernel-level, không phủ nhận kết quả end-to-end. vLLM V1 hiện tại đã thay đổi nhiều chi tiết: **[FACT]** swap preemption chỉ còn ở V0, V1 dùng recompute; prefix caching giờ bật mặc định (constant-time LRU eviction, <1% throughput loss kể cả 0% hit rate).
- **Còn giá trị hôm nay:** toàn bộ mô hình mental về paging, fragmentation, block-granularity sharing; DEFAULT_BLOCK_SIZE=16 vẫn đúng trong code **[FACT: `vllm/config/cache.py`]**.
- **Hàm ý dự án:** gateway không bao giờ thấy blocks — nhưng hiểu paging giải thích VÌ SAO backend từ chối request (hết blocks → preemption → TTFT tăng vọt), tức là tín hiệu overload thật sự của backend.
- **Hàm ý phỏng vấn:** câu hỏi #1 của mọi vòng AI-infra. Phải nói được: con số 20.4–38.2%, cơ chế block table, vì sao 2–4x là con số 2023 với baseline lịch sử (nuance này ăn điểm Staff).
- **Đọc:** Sections 1–4 (motivation, PagedAttention, KV Cache Manager), 6.1–6.2 (eval chính). **Bỏ qua:** phần kernel implementation chi tiết, các decoding algorithm phụ (beam search — vLLM V1 đã bỏ beam search khỏi engine **[FACT]**). **Thời gian: 4–5h.**

### P2. "Orca: A Distributed Serving System for Transformer-Based Generative Models" (Yu et al., OSDI 2022) — BẮT BUỘC

- **Vấn đề:** request-level (static) batching — request xong sớm không rời batch được, request mới phải đợi cả batch xong.
- **Đóng góp:** **[FACT]** (1) *iteration-level scheduling* — scheduler gọi engine chạy đúng MỘT iteration mỗi lần, request join/leave batch mỗi iteration → tổ tiên trực tiếp của "continuous batching" trong vLLM/SGLang/TGI/TensorRT-LLM; (2) *selective batching* — chỉ batch các phép toán không phụ thuộc token-count (Linear, GeLU...), attention chạy per-sequence vì KV tensors độ dài khác nhau không coalesce được cho `torch.bmm`.
- **Đánh giá:** **[FACT]** 36.9x throughput vs FasterTransformer trên GPT-3 175B cùng mức latency.
- **Giới hạn/superseded:** Orca reserve KV memory theo `max_tokens` từ trước → internal fragmentation (chính là cái PagedAttention sửa); không open-source; con số 36.9x trên baseline 2022.
- **Hàm ý dự án:** đây là lý do **gateway không được re-implement batching** — mọi batching ở tầng HTTP phía trước iteration-level scheduler chỉ có thể làm hại.
- **Hàm ý phỏng vấn:** "vì sao prefill và decode không batch ngây thơ với nhau được" — selective batching là câu trả lời gốc; nối tiếp bằng chunked prefill của vLLM V1 là câu trả lời hiện đại.
- **Đọc:** Sections 1–3 (motivation, iteration-level scheduling, selective batching), lướt 6 (eval). **Bỏ:** phần distributed execution chi tiết (tensor/pipeline setup đã lỗi thời). **Thời gian: 3h.**

### P3. "SGLang: Efficient Execution of Structured Language Model Programs" (Zheng et al., NeurIPS 2024; arXiv:2312.07104) — NÊN ĐỌC

- **Vấn đề:** hệ thống serving 2023–2024 thiếu hỗ trợ hiệu quả cho ứng dụng multi-call có cấu trúc (agent, few-shot, JSON, multi-turn) — đúng loại workload mà gateway đa tenant sinh ra.
- **Đóng góp:** **[FACT theo paper]** RadixAttention — KV cache reuse tự động qua radix tree + LRU eviction + cache-aware scheduling; compressed FSM cho structured output; primary abstraction là "LM program" (frontend DSL + runtime co-design).
- **Đánh giá & giới hạn:** **[FACT theo paper]** claim 6.4x throughput CHỈ trên multi-call/prefix-heavy/structured workloads — không phải generic single-turn serving. Mọi benchmark trích số này phải kiểm soát prefix-sharing ratio.
- **Hàm ý dự án:** prefix-cache-aware routing ở gateway chỉ là *routing hint* — cache thật sống trong runtime; đây là ranh giới trách nhiệm đúng. Định hình thí nghiệm M11.
- **Hàm ý phỏng vấn:** so sánh RadixAttention (radix tree, tự động, cross-request) vs vLLM prefix caching (hash-chained block, block-aligned **[FACT]**) là câu hỏi phân biệt senior/staff.
- **Đọc:** Sections 1–3 (motivation, RadixAttention), lướt eval. **Bỏ:** compressed FSM chi tiết, frontend language. **Thời gian: 2–3h.**

### P4. "DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving" (Zhong et al., OSDI 2024) — NÊN ĐỌC (chọn lọc)

- **Vấn đề:** **[FACT theo paper]** colocate prefill + decode trên cùng GPU (kiểu continuous batching) tạo interference giữa hai phase và ép cả hai chung một resource-allocation/parallelism plan.
- **Đóng góp:** tách prefill và decode sang GPU vật lý khác nhau; tối ưu từng phase theo SLO riêng — **TTFT cho prefill, TPOT cho decode**; định nghĩa mục tiêu là **goodput** (requests đạt SLO mỗi giây) thay vì raw throughput. Chi phí: KV-cache transfer giữa hai pool — khả thi phụ thuộc interconnect bandwidth (NVLink/intra-node).
- **Đánh giá:** **[FACT theo paper]** tới 7.4x số request phục vụ được hoặc 12.6x SLO chặt hơn vs colocated (gồm vLLM baseline), >90% requests trong latency constraints.
- **Hàm ý dự án:** KHÔNG implement disaggregation (single-GPU vô nghĩa; vLLM Connector interface cho disagg còn "not yet stable" **[CLAIM tại commit 8/2025]**). NHƯNG lấy **định nghĩa goodput theo cặp SLO TTFT/TPOT** làm ngôn ngữ chuẩn cho benchmark của bạn — `vllm bench serve --goodput` dùng đúng định nghĩa DistServe **[FACT]**.
- **Hàm ý phỏng vấn:** "prefill vs decode khác nhau thế nào và vì sao người ta tách chúng" — compute-bound vs memory-bandwidth-bound, interference, SLO per-phase.
- **Đọc:** Sections 1–3 + định nghĩa goodput. **Bỏ:** placement algorithm chi tiết, simulator. **Thời gian: 2–3h.**

### P5. "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness" (Dao et al., 2022; arXiv:2205.14135) — ĐỌC KHÁI NIỆM

- **Vấn đề & đóng góp:** **[FACT theo paper]** attention chuẩn bị nghẽn ở memory traffic HBM↔SRAM chứ không phải FLOPs; FlashAttention là exact attention (không xấp xỉ) dùng tiling + online softmax để giảm HBM accesses (IO-complexity O(N²d²/M) vs O(N²), có chứng minh optimal theo dải SRAM size).
- **Giới hạn cho mục đích của bạn:** **[FACT theo paper]** headline numbers là TRAINING speedups (15% BERT-large MLPerf, 3x GPT-2 seq 1K, Path-X 61.4% ở seq 16K) — không phải inference latency claims. FlashAttention-2/3 đã cải tiến tiếp (không cần đọc để phỏng vấn platform).
- **Hàm ý dự án/phỏng vấn:** đây là paper "GPU fundamentals" tốt nhất cho hồ sơ của bạn: dạy memory hierarchy (HBM vs SRAM), roofline thinking, vì sao decode là memory-bandwidth-bound — nền cho mọi câu trả lời về GPU utilization mà không cần viết CUDA.
- **Đọc:** Sections 1–2 + Figure 1 + 3.1 (thuật toán mức ý tưởng). **Bỏ:** toàn bộ chứng minh, block-sparse extension. **Thời gian: 2h.**

### Phụ (đọc lướt nếu còn giờ)

- **P6. "Fast Inference from Transformers via Speculative Decoding" (Leviathan et al.; arXiv:2211.17192), 1–2h:** draft model đề xuất, target model verify song song, rejection sampling bảo toàn phân phối; 2–3x speedup. Lưu ý thực tế **[CLAIM tại commit 8/2025]**: vLLM V1 không hỗ trợ draft-LLM cổ điển — chỉ n-gram, EAGLE, Medusa. Đủ để trả lời phỏng vấn ở mức khái niệm + trạng thái triển khai thực.
- **P7. Critique về SLO/goodput metrics (arXiv:2410.14257), 1–2h:** **[FACT theo paper]** các metric SLO/goodput chuẩn có thể bị "game": cố ý delay token delivery có thể TĂNG SLO attainment đo được; drop sớm request sắp trượt SLO tăng goodput hệ thống. TBT quá chặt (stall ngắn vô hình với người đọc có buffer), TPOT/E2E quá lỏng (che stall giữa stream). Đề xuất "smooth goodput" theo tốc độ tiêu thụ của người dùng. **Hàm ý trực tiếp cho Section 8: báo cáo cả phân phối ITL/stall, không chỉ mean TPOT.**

**Thứ tự đọc gắn milestone:** P1+P2 trong tuần 1–4 (trước khi chạm vLLM thật), P5 tuần 5–6, P4+P7 trước M8 (benchmark), P3 trước M11.

---

## Section 7: Kế hoạch đọc source code

### Repo 1: `vllm-project/vllm` — chính, ~12–14h tổng, tách 2 đợt

**Định hướng repo [FACT]:** Python 84.5% / Rust 5.5% / CUDA 5.0% / C++ 3.6%; build `setuptools` + CMake cho phần native (không cần build từ source — dùng pip/container). Process model serving path: API server process (AsyncLLM: input processing, tokenization, detokenization, streaming) ↔ ZMQ ↔ EngineCore process per DP rank (scheduler + executor, busy loop) → worker process per GPU (`tensor_parallel_size × pipeline_parallel_size`; tổng process = A + DP + N, +1 coordinator nếu DP>1 — 4-GPU tp=4 chạy 6 processes **[FACT]**, con số này dùng cho K8s CPU sizing). Config model: engine args CLI/env. Điểm vào request: `vllm/entrypoints/openai/api_server.py`.

**Bản đồ đọc code (các đường dẫn xác minh tại 2026-07-08):**

| Đường dẫn | Đối tượng | Vì sao quan trọng | Câu hỏi phải trả lời khi đọc |
|---|---|---|---|
| `vllm/entrypoints/openai/api_server.py` | FastAPI app, route `/v1/chat/completions` | Bề mặt mà gateway của bạn nói chuyện | SSE chunks được sinh và flush thế nào? `usage` trả ở đâu khi stream? |
| `vllm/v1/engine/async_llm.py` | `AsyncLLM` | Frontend: nơi tokenization + OutputProcessor sống | Cái gì chạy ở frontend process vs EngineCore? Abort request đi đường nào? |
| `vllm/v1/engine/core.py` | `EngineCoreProc`, `run_busy_loop` | Trái tim data plane của engine | Một "step" gồm những pha nào? Vòng lặp nhận request mới từ ZMQ ở điểm nào? |
| `vllm/v1/core/sched/scheduler.py` | `Scheduler` | Scheduling token-budget, không phân biệt phase | Decode được ưu tiên trước prefill ở đâu? `token_budget` trừ thế nào? Preemption (recompute) kích hoạt khi nào? |
| `vllm/v1/core/sched/output.py` | `SchedulerOutput`, `num_scheduled_tokens: dict[str, int]` | Bằng chứng "quyết định = dict request→tokens" | Worker nhận gì mỗi step? (diffs, không full state **[FACT]**) |
| `vllm/v1/core/kv_cache_manager.py`, `block_pool.py` | `KVCacheManager`, `free_block_queue`, `allocate_slots` | PagedAttention trong đời thực | Khi nào allocate fail → request nào bị preempt? |
| `vllm/v1/core/kv_cache_utils.py` | `hash_block_tokens(hash_fn, parent_block_hash, curr_block_token_ids, extra_keys)` | Prefix caching hash-chained (SHA-256 mặc định hiện nay; block chưa đầy KHÔNG cache) | Vì sao prefix reuse chỉ xảy ra tại block-aligned boundaries? extra_keys (LoRA ID, cache salt) để làm gì? |
| `vllm/v1/engine/core_client.py` | `DPLBAsyncMPClient` | Load balancing nội bộ: `score = waiting*4 + running` | Gateway của tôi nên duplicate hay delegate công thức này? (trả lời: delegate ở DP-rank level, tự làm ở deployment level) |
| `vllm/v1/engine/coordinator.py` | `DPCoordinator` | Queue-state publish ~100ms qua ZMQ XPUB | Độ trễ thông tin load này ảnh hưởng routing thế nào? |
| `vllm/benchmarks/serve.py` + `vllm/entrypoints/cli/benchmark/` | benchmark CLI | Phương pháp chuẩn cho Section 8 | Poisson/Gamma arrivals sinh thế nào (`np.random.gamma(shape=burstiness, ...)`) ? goodput keys giới hạn ttft/tpot/e2el ra sao? |

**Trace vòng đời request (viết ra như bài tập):** HTTP arrival (`api_server.py`) → validation + tokenize (AsyncLLM, frontend process) → ZMQ đến EngineCore → vào waiting queue → `Scheduler` cấp token budget + `allocate_slots` → worker execute step → sampled tokens về qua ZMQ → OutputProcessor detokenize + check stop → SSE chunk về client → (cancel: client đóng → AsyncLLM abort → EngineCore giải phóng blocks) → metrics.

**Bài tập giới hạn (chọn 1, 3–5h):**
1. **Sequence diagram** "một request streaming qua vLLM V1: 2 processes, ZMQ hops, các điểm phát sinh TTFT và ITL" — artifact dùng thẳng vào README dự án và câu trả lời phỏng vấn. (Khuyến nghị chính.)
2. Hoặc: chạy vLLM CPU mode/GPU nhỏ, bật log scheduler, ghi chú thực nghiệm "điều gì xảy ra khi 20 requests cùng vào với `max_num_scheduled_tokens` nhỏ" — quan sát chunked prefill và decode-first policy.

### Repo 2: `kubernetes-sigs/gateway-api-inference-extension` (+ llm-d) — Go, ~5–6h

**Vì sao:** đây là "đáp án chuẩn của ngành" cho đúng bài toán bạn xây, viết bằng ngôn ngữ của bạn. **[FACT]** EPP = data-plane component nói ext-proc với Envoy; thuật toán chọn endpoint extensible, KV-cache và request-cost aware. **Cảnh báo currency [FACT]:** EPP package đang migrate sang `llm-d/llm-d-router`; API đã đổi từ InferenceModel+InferencePool sang InferenceObjective+InferencePool — xác định vị trí code hiện hành trước khi đọc, đừng tin đường dẫn trong blog cũ.

**Bản đồ đọc:** (1) README + docs kiến trúc InferencePool/EPP; (2) scheduler/scorer plugins trong EPP (tìm thư mục `pkg/epp/scheduling` hoặc tương đương ở vị trí hiện hành — các scorer: queue-depth, KV-cache utilization, prefix-affinity, LoRA-affinity); (3) `llm-d/llm-d-kv-cache-manager`: `kvblock.Index` — **[FACT]** đường đọc: tokenize prompt → sinh deterministic KV block keys khớp block-hashing của vLLM → query index → score pod theo run dài nhất các block khớp liên tiếp từ đầu prompt; index cập nhật qua KVEvents do vLLM emit — bằng chứng rằng **cache-aware routing đòi hỏi engine hợp tác phơi bày state, gateway không thể tự suy từ HTTP**.

**Bài tập giới hạn (4–6h):** viết **design comparison note** 2–3 trang: "Router của tôi vs GAIE EPP" — bảng so sánh tín hiệu routing (mine: least-inflight + health; EPP: queue-depth + KV-cache + LoRA affinity), chi phí lấy mỗi tín hiệu, và điều kiện nào mỗi thiết kế thắng. Artifact này trả lời trực tiếp câu phỏng vấn "thiết kế router cho LLM backends".

### Repo 3 (nhẹ, 2h): `BerriAI/litellm` — KHÔNG đọc sâu code

Chỉ đọc docs bề mặt sản phẩm (virtual keys, budgets, TPM/RPM, scheduler beta) để viết chính xác mục "why not LiteLLM" trong README và để không mô tả sai đối thủ trong phỏng vấn. **[FACT]** scheduler priority của LiteLLM là beta, Redis-polling — điểm tương phản tốt với queue in-process của bạn.

**Tổng ngân sách đọc code: ~20h.** Không đọc: Triton (C++ core — chỉ đọc trang docs kiến trúc model-repository/backends, 1h), TensorRT-LLM, TGI, Ray Serve, KServe, Temporal, K8s scheduler.

---

## Section 8: Thiết kế benchmark

Nguyên tắc gốc: **mô phỏng theo phương pháp first-party của vLLM** (`vllm bench serve`) thay vì tự chế — **[FACT]** nó sample inter-arrival times từ Poisson (tổng quát hóa Gamma qua `burstiness`, =1.0 là Poisson), đo TTFT/TPOT/ITL/E2EL (mean/median/std/percentiles), throughput và goodput (`--goodput` nhận cặp KEY:VALUE giới hạn ở `ttft`/`tpot`/`e2el` theo định nghĩa DistServe), hỗ trợ max concurrency qua semaphore.

1. **Định nghĩa workload (3 loại, cố định seed):**
   - W1 "chat": prompt ~256–1024 tokens (phân phối từ ShareGPT-like), output ~128–512, không chia sẻ prefix.
   - W2 "prefix-heavy": system prompt chung 1–2K tokens + phần riêng ngắn — để lộ prefix caching/RadixAttention (bắt buộc cho M11; **[FACT]** không kiểm soát prefix-sharing ratio thì so sánh SGLang vs vLLM vô hiệu).
   - W3 "fixed-length synthetic": input/output cố định (vd. 512/128) cho các phép đo overhead và sweep sạch. (Tham chiếu: `vllm bench latency` mặc định 32 input/128 output/batch 8; `throughput` mặc định 1000 ShareGPT samples ở QPS=Inf **[FACT]**.)
2. **Ghi phần cứng & phiên bản (bắt buộc mỗi báo cáo):** GPU model + VRAM, driver + CUDA version, vLLM version + engine args đầy đủ (`max_num_seqs`, `max_num_batched_tokens`, `gpu_memory_utilization`, prefix caching on/off), model + dtype + quantization, gateway commit hash, network topology (cùng máy? cùng AZ?). **[CLAIM — BentoML handbook]** khác biệt nhỏ trong các biến này thay đổi kết quả mạnh.
3. **Warm-up:** loại bỏ N requests đầu (model load, CUDA graphs, cache nguội) — quy ước: chạy ≥50 requests warm-up hoặc 2 phút, không tính vào số liệu; ghi rõ trong report.
4. **Concurrency sweep:** trục X = request rate (Poisson λ) hoặc max concurrency; sweep từ thấp đến quá bão hòa; vẽ TTFT p50/p99 và goodput theo λ — điểm gãy (knee) là output chính của capacity planning.
5. **Cô lập hiệu ứng batching:** so sánh cùng workload ở concurrency 1 vs N; và gateway-on vs gateway-off (đo trực tiếp vLLM) để tách **gateway overhead** (báo cáo delta p50/p99 — đối chiếu với **[CLAIM]** LiteLLM 8ms P95 @ 1k RPS).
6. **Metrics & báo cáo:** TTFT, ITL (phân phối, không chỉ mean), TPOT, E2EL, goodput theo SLO tuyên bố trước, token throughput (in/out riêng), error/shed rate. Luôn báo p50/p95/p99 + phân phối; **không bao giờ chỉ mean** — **[FACT theo P7]** TPOT/E2E trung bình che stall giữa stream; báo cáo thêm "max stall" (ITL max) per request.
7. **Xử lý thống kê:** ≥3 lần chạy mỗi cấu hình, báo median ± range; không claim khác biệt nhỏ hơn variance giữa runs.
8. **Tái lập:** mọi benchmark là script trong repo (`make bench-w1`), config + seed + raw data (JSONL) commit kèm; đồ thị sinh từ raw data bằng script.
9. **Failure tests trong benchmark:** đo hành vi dưới quá tải 2x–5x điểm knee: shed rate, p99 của requests ĐƯỢC nhận (phải ổn định nếu admission control đúng), thời gian hồi phục sau spike.
10. **Quy tắc diễn giải (chống benchmark theater):** (a) mọi kết luận kèm điều kiện workload; (b) không so cross-tool vì các tool định nghĩa metric khác nhau **[CLAIM — BentoML]**; (c) số của mình đo trên phần cứng nào chỉ đại diện phần cứng đó; (d) **[FACT theo P7]** goodput có thể bị game bằng cách drop sớm — báo cáo shed rate cạnh goodput, không bao giờ tách rời; (e) claim tương đối ("gateway thêm ≤X ms p99 tại λ=Y") bền hơn claim tuyệt đối.

---

## Section 9: Thiết kế reliability và SLO

**SLI (đo tại gateway, per model-pool):**
- Availability: tỷ lệ request kết thúc thành công (không 5xx do hệ thống; 4xx client không tính).
- TTFT: thời gian nhận→first content chunk (tách riêng: queue wait ∥ backend TTFT).
- Streaming smoothness: ITL p95 và **stall rate** (tỷ lệ request có ITL max > 1s) — **[FACT theo P7]** mean TPOT không đủ.
- Queue wait: thời gian trong bounded queue (tách khỏi thời gian backend — bắt buộc để trả lời "chậm do ai").
- Shed rate + retry-budget consumption.

**SLO ứng viên (tuyên bố trước, đo sau — con số sẽ hiệu chỉnh theo phần cứng thật):** ví dụ khởi điểm: 99.5% availability; TTFT p95 ≤ 2s cho W1 tại λ ≤ 80% knee; stall rate < 1%; queue wait p95 ≤ 500ms tại tải danh định. Giá trị nằm ở việc CÓ SLO và đo được compliance, không phải ở con số đẹp.

**Error taxonomy (map thẳng vào HTTP + SSE):**

| Lớp | Ví dụ | Mã trả về | Retry? |
|---|---|---|---|
| Client error | schema sai, context quá dài | 400/413 | Không |
| Quota/rate | vượt token budget | 429 + `Retry-After` | Client tự |
| Overload (shed) | queue full/timeout | 429 hoặc 503 + `Retry-After` | Client tự, có jitter |
| Backend pre-stream | connect fail, 5xx trước token đầu | retry nội bộ trong budget → 502 nếu cạn | **Có** (an toàn — chưa có side effect tới client) |
| Mid-stream failure | backend chết giữa generation | SSE error event + đóng stream | **Không tự động** — client đã nhận partial tokens |
| Cancel | client đóng | log 499-style | N/A |

**Retry policy:** chỉ retry pre-first-token; budget dạng tỷ lệ (retries ≤ 10–20% requests trong cửa sổ trượt, có metric riêng) để tránh retry storm khuếch đại quá tải — khi budget cạn, fail fast. Hedging (gửi song song 2 backend): **reject** — đắt gấp đôi GPU-time cho inference, khác hẳn hedging RPC rẻ.

**Overload policy & shedding order:** tín hiệu quá tải = queue depth + queue wait tăng + (stretch: backend `num_requests_waiting` từ /metrics — **[CHƯA XÁC MINH]**, đóng ở M5). Shed theo thứ tự: (1) tenant vượt quota mềm, (2) priority thấp nhất, (3) request có estimated cost lớn nhất (prompt dài) khi cần giải phóng nhanh. Ghi lý do shed vào response header để debug được.

**Graceful shutdown:** ngừng nhận (fail readiness probe) → drain queue (hoặc trả 503 cho phần chưa dequeue) → chờ streams đang bay tối đa `drain_deadline` (30–60s — generation dài có thể vượt; chính sách: quá deadline thì gửi SSE error event có mã riêng rồi đóng, KHÔNG cắt cụt im lặng) → flush usage buffer → thoát. Test bắt buộc: rolling restart dưới tải, 0 lỗi client.

**Failure injection (5 thí nghiệm, mỗi cái có giả thuyết viết trước):**
1. Kill vLLM pod giữa 50 streams → kỳ vọng: 50 SSE error events sạch ≤2s, breaker mở, traffic sang replica còn lại, KHÔNG retry đôi.
2. Backend latency +2s (toxiproxy/tc) → kỳ vọng: TTFT SLO vỡ có cảnh báo, queue không tràn vô hạn nhờ bounded queue.
3. Slowloris client (đọc SSE 1 byte/s × 200 connections) → kỳ vọng: per-connection write deadline + buffer bound bảo vệ memory gateway (đây là fault ít ai làm — điểm sáng portfolio).
4. Quá tải 5x knee trong 60s → kỳ vọng: shed đúng thứ tự, p99 của requests được nhận ổn định, hồi phục ≤10s sau spike.
5. Config reload xấu (model trỏ backend không tồn tại) → kỳ vọng: validation chặn, giữ snapshot cũ, không rớt request nào.

**Incident postmortem:** chọn 1 thí nghiệm phát hiện bug thật, viết postmortem chuẩn (timeline, impact, root cause, action items) — artifact hiếm gặp trong portfolio và ăn điểm behavioral interview.

---

## Section 10: Quyết định ngôn ngữ và độ sâu kỹ năng

**Go — dùng cho:** toàn bộ gateway data plane, control plane/admin API, load generator, mock backend, K8s tooling. **[SUY LUẬN + bằng chứng sinh thái]** đây là lựa chọn đúng và được ngành xác nhận: GAIE EPP và llm-d scheduler viết bằng Go (~96.5% **[FACT]**) — bạn đang dùng đúng ngôn ngữ của tầng hạ tầng này.

**Python — dùng cho (mục tiêu: đọc/viết thành thạo mức "systems engineer", KHÔNG cần production Python framework):** đọc vLLM internals (bắt buộc — 84.5% Python **[FACT]**), script phân tích benchmark (pandas/matplotlib), tokenizer offline cho token estimation, mini-eval harness, thí nghiệm nhỏ với PyTorch (1 notebook forward pass + đo KV cache size để hiểu con số — 4–6h, đủ).

**C++ — phán quyết theo role:**
- AI Platform / ML Platform / AI Reliability: **không cần** trong 24 tuần. Không role nào trong nhóm này phỏng vấn C++.
- Inference Platform (gateway/serving layer): **literacy đọc** (đọc hiểu một header + flow, không viết) — 0–10h, chỉ khi JD nhắc.
- NVIDIA-style System Software: **bắt buộc thật sự** — nhưng là lộ trình 6–12 tháng SAU tuần 24, không nhồi được vào 480h này. Ghi rõ trong kế hoạch là mục tiêu giai đoạn 2.

**CUDA — phán quyết:** KHÔNG viết kernel trong 24 tuần. Độ sâu tối thiểu hữu ích (~8–12h trong ngân sách learning): memory hierarchy HBM/SRAM/registers, vì sao decode memory-bandwidth-bound còn prefill compute-bound (qua P5 FlashAttention), đọc hiểu output `nvidia-smi` + khái niệm những gì Nsight Systems cho thấy, arithmetic intensity/roofline ở mức vẽ tay. **GPU profiling literacy > kernel implementation** cho mọi role mục tiêu trừ NVIDIA-style **[SUY LUẬN]**: một kernel vector-add trong portfolio không thuyết phục được ai, nhưng giải thích được "vì sao GPU util 40% mà throughput không tăng" (câu trả lời: memory-bound, batch nhỏ, CPU overhead — dẫn **[FACT]** V1 tăng 1.7x vs V0 gần như thuần nhờ giảm CPU overhead, kernels gần như y hệt) thì thuyết phục ở mọi vòng.

**Tóm tắt theo role:**

| Role | Go | Python | C++ | CUDA |
|---|---|---|---|---|
| AI Platform Engineer | Chuyên sâu (đang có) | Đọc + script | Không | Khái niệm |
| Inference Platform Engineer | Chuyên sâu | Đọc engine code tốt | Literacy đọc | Khái niệm + profiling literacy |
| NVIDIA-style System SW | Phụ | Phụ | **Cần thật — giai đoạn 2** | **Cần thật — giai đoạn 2** |

---

## Section 11: Quyết định về Evaluation platform và Agent runtime

**LLM Evaluation Platform → thu nhỏ thành "mini-eval harness" BÊN TRONG repo flagship (không phải platform riêng).** Lý do **[SUY LUẬN]**: một eval platform đầy đủ (dataset versioning, LLM-as-judge, pairwise, human review, CI gates) là dự án 150h+ và kéo positioning sang ML Engineering — sai trọng tâm inference-systems. Nhưng một harness nhỏ lại củng cố flagship: **thiết kế tối thiểu (~15–20h, nằm trong M8/M11):** bộ prompt cố định có version (JSONL + git), chạy qua gateway với seed/temperature=0 (lưu ý: determinism không tuyệt đối khi batching thay đổi — chính nuance này là điểm phỏng vấn tốt, ghi vào docs), so sánh quality-latency-cost giữa 2 cấu hình backend (exact-match/regex trên bộ task đơn giản — KHÔNG LLM-as-judge trong 24 tuần), xuất bảng vào benchmark report; một job CI làm regression gate cho TTFT/ITL của gateway (fail nếu p95 tệ đi >X% so với baseline commit trước — regression gate cho HIỆU NĂNG, khả thi hơn gate cho quality).

**Durable Agent Execution Runtime → POSTPONE (sau tuần 24).** Đánh giá thẳng: dự án này chơi đúng thế mạnh của bạn (Temporal-style durable execution, replay, idempotency — bạn đã làm CDC/DLQ/replay), NHƯNG (1) nó phân tán positioning — hiring manager đọc 2 dự án lớn sẽ hỏi "rốt cuộc bạn chuyên gì?"; (2) không có claim nào về agent-runtime được nghiên cứu này verify; (3) flagship + interview prep đã tiêu hết 480h. **Nếu sau này làm (giai đoạn 2, phạm vi tối thiểu):** tool-execution workflow trên Temporal với idempotent tool calls, approval step, audit log — 60–80h — và pitch là "reliability engineer cho agent workloads", một positioning đang lên. Trong 24 tuần: chỉ giữ 1 đoạn trong README flagship nói gateway phục vụ agent workload thế nào (multi-call, prefix-heavy — nối với thí nghiệm M11/W2).

---

## Section 12: Bản đồ phỏng vấn (câu hỏi → câu trả lời Senior/Staff → artifact)

Chọn 12 câu đại diện phủ các cụm; mỗi câu: Senior cần có / Staff thêm gì / trả lời yếu thường gặp / artifact chứng minh.

1. **"Giải thích prefill vs decode."** Senior: prefill xử lý toàn bộ prompt song song (compute-bound), decode sinh từng token tuần tự phụ thuộc KV cache (memory-bandwidth-bound); TTFT ≈ queue + prefill, ITL ≈ decode step. Staff: chunked prefill trộn hai loại trong một step với token budget (**[FACT]** V1 xóa phân biệt phase — dict `{request_id: num_tokens}`); interference và lý do DistServe tách phase theo SLO TTFT/TPOT. Yếu: "prefill nhanh decode chậm" không nói được vì sao theo roofline. Artifact: sequence diagram Repo-1 + benchmark tách TTFT/ITL.
2. **"KV cache là gì, vì sao PagedAttention quan trọng?"** Senior: cache K/V per token per layer; contiguous max-length allocation lãng phí — **[FACT]** chỉ 20.4–38.2% hữu dụng; paging block 16 tokens loại external fragmentation. Staff: hash-chained prefix caching (SHA-256, block-aligned only **[FACT]**), copy-on-write, recompute preemption V1, nuance vAttention critique. Yếu: mô tả như "cache HTTP". Artifact: ghi chú đọc `kv_cache_utils.py` + thí nghiệm prefix on/off M11.
3. **"Continuous batching hoạt động thế nào?"** Senior: iteration-level scheduling từ Orca — request join/leave batch mỗi step; vì sao throughput tăng bậc so với static batching. Staff: selective batching (attention không batch ngây thơ được), token budget của V1, async scheduling giấu CPU sau GPU (**[FACT]** RFC #8779). Yếu: nhầm với micro-batching ở gateway. Artifact: câu chuyện "vì sao gateway tôi KHÔNG batch".
4. **"Thiết kế multi-tenant LLM gateway."** Senior: auth→quota→admission→bounded queue→routing→streaming relay; token-aware limits; tách control/data plane. Staff: ranh giới với engine (cái gì engine đã làm — DP load balancing `waiting*4+running` **[FACT]**), fairness + starvation, so sánh có ý thức với LiteLLM/GAIE và nói được mình khác gì. Yếu: liệt kê feature không có ranh giới trách nhiệm. Artifact: chính flagship + design comparison note (Repo 2).
5. **"Retry inference request khi nào an toàn?"** Senior: chỉ pre-first-token; mid-stream không retry tự động (partial output + double billing); retry budget chống storm. Staff: phân tích idempotency — inference không idempotent theo nội dung (sampling) nhưng idempotent theo billing nếu có request ID; hedging bị loại vì chi phí GPU. Yếu: "retry 3 lần với backoff" phản xạ. Artifact: error taxonomy + fault test #1.
6. **"Đo TTFT/ITL thế nào cho đúng?"** Senior: timestamp mỗi SSE chunk tại gateway; tách queue wait khỏi backend time; percentiles không mean. Staff: **[FACT theo P7]** metrics gameable — delay token có thể tăng SLO đo được; stall rate; goodput phải đi kèm shed rate. Yếu: lấy trung bình tokens/s. Artifact: benchmark report + dashboard.
7. **"Backend chậm dần — hệ thống của bạn làm gì?"** Senior: health check + least-inflight routing, breaker theo lỗi pre-stream, shed theo priority khi queue đầy. Staff: tín hiệu load nào có độ trễ nào (DPCoordinator publish ~100ms **[FACT]**; /metrics scrape 5–15s) và tác động lên quyết định; gray failure (chậm nhưng không chết) khó hơn crash. Yếu: chỉ nói circuit breaker như thần chú. Artifact: fault test #2 + routing decision logs.
8. **"Fairness giữa tenants?"** Senior: weighted round-robin theo token consumption cửa sổ trượt; bounded queue per tenant/pool. Staff: DRF ở khái niệm, aging chống starvation, trade-off fairness vs utilization, và vì sao fairness token-level cuối cùng vẫn bị giới hạn bởi batch formation của engine. Yếu: "dùng priority queue" không nói chống đói. Artifact: thí nghiệm M6 với đồ thị.
9. **"Capacity planning cho 1000 concurrent users?"** Senior: từ benchmark knee → tokens/s/GPU → số GPU + headroom; phân biệt concurrent users vs concurrent requests. Staff: goodput theo SLO thay vì raw throughput; ảnh hưởng phân phối prompt length; chi phí/1M tokens làm đơn vị so sánh. Yếu: nhân chia tuyến tính từ một số liệu quảng cáo. Artifact: capacity doc M11 đối chiếu số đo thật.
10. **"Graceful shutdown với generation dài?"** Senior: fail readiness → drain có deadline → xử lý stream vượt deadline có chủ đích. Staff: tương tác với autoscaler (scale-in event), connection draining ở LB phía trước, chi phí recompute nếu backend restart (không có swap trong V1 **[FACT]**). Yếu: "SIGTERM rồi chờ". Artifact: rolling-restart-under-load test M10.
11. **Coding: "Viết concurrent rate limiter / worker pool / streaming fan-out với cancellation."** Senior: channels, context, select với timeout, không leak goroutine. Staff: chứng minh bằng test (race detector, leak test), nói được trade-off token bucket vs sliding window. Artifact: chính code gateway — trích module làm bài mẫu.
12. **"Vì sao không dùng LiteLLM/GAIE mà tự xây?"** (câu hỏi bẫy positioning). Senior: nắm chính xác hai hệ đó làm gì (**[FACT]** như Section 1) và nói mục tiêu là depth artifact. Staff: chỉ ra khoảng trống thật cụ thể mình lấp (token-aware admission gắn backend state; đo lường streaming nghiêm ngặt) và khi nào NÊN dùng đồ có sẵn trong production thật. Yếu: chê đồ có sẵn hoặc không biết chúng tồn tại. Artifact: mục "why not X" trong README.

---

## Section 13: Rủi ro và anti-patterns

1. **Overengineering phân tán:** distributed rate limiting, multi-replica coordination, MQ trong request path — với single-node portfolio, mỗi cái vừa tốn giờ vừa LỘ việc không hiểu khi nào cần phân tán. Thay bằng design doc.
2. **Benchmark theater:** số đẹp không phương pháp (không warm-up, không percentiles, không hardware record, so cross-tool, mean-only) — hiring manager giỏi phát hiện trong 5 phút và mất niềm tin toàn repo. Section 8 là thuốc.
3. **Retry semantics sai:** retry mid-stream tạo duplicate content + double billing; retry không budget khuếch đại quá tải. Phải có test khẳng định hành vi KHÔNG retry.
4. **Duplicate queues / scheduler thứ hai:** xây "batching" hay per-step scheduling ở gateway trước continuous batching của engine — **[FACT]** engine đã quyết ranh giới này; vi phạm nó là red flag kiến thức nặng nhất có thể phạm trong domain này.
5. **Hidden buffering phá streaming:** Go `bufio`, reverse proxy mặc định, nginx phía trước — TTFT đo được đẹp giả tạo hoặc tệ giả tạo. Kiểm tra flush per-chunk ở mọi hop; viết test đo ITL qua toàn chain.
6. **High-cardinality metrics:** label per-request-id/per-user trên Prometheus histogram → nổ TSDB. Label whitelist: tenant (bounded), model, backend, outcome class. Trace mới là nơi chứa per-request.
7. **Capacity estimate không đối chiếu:** con số suy từ spec sheet không đối chiếu đo thật. Mọi capacity claim trong repo phải trace về một benchmark run.
8. **Quá nhiều framework:** 5 backends hời hợt < 1 backend sâu + 1 so sánh có kiểm soát. Đã cắt ở Section 4.
9. **C++/CUDA trang trí:** kernel vector-add trong repo gateway gây tác dụng ngược (mời câu hỏi CUDA mà bạn chưa trả lời được). Để giai đoạn 2 làm tử tế.
10. **Kiến trúc không có bằng chứng chạy:** diagram đẹp + code không chạy demo được là pattern thất bại phổ biến nhất của portfolio đổi ngành. Quy tắc: mỗi milestone kết thúc bằng demo tái lập được bằng `docker compose up` + script.
11. **Rủi ro tiến độ thực tế (từ ràng buộc 20h/tuần):** GPU access trục trặc (M5) và viết lách bị bỏ đói (M12) là hai điểm gãy lịch phổ biến nhất — cả hai đã có fallback trong Section 3 (CPU mode/llama.cpp; M12 khóa cứng 12h).

---

## Section 14: Phán quyết khả thi cuối cùng

**Phân bổ 480h [KHUYẾN NGHỊ]:**

| Hạng mục | Giờ |
|---|---|
| Dự án flagship (12 milestones, Section 3) | ~200 |
| Learning: papers (~22h) + đọc source (~20h) + GPU/inference fundamentals + Python (~35h) | ~77 |
| Coding interview (Go + một phần Python, LeetCode-style + concurrency) | ~55 |
| System design + AI systems interview (mock, viết đáp án chuẩn từ chính dự án) | ~60 |
| English + behavioral (kể chuyện STAR từ thành tích cũ + dự án mới) | ~40 |
| Portfolio, networking, apply, blog | ~28 |
| Buffer (ốm, việc công ty dồn, GPU trục trặc) | ~20 |
| **Tổng** | **480** |

**Làm được thật trong 480h:** gateway đa tenant streaming hoàn chỉnh trước vLLM + llama.cpp, token-aware admission, priority/fairness, reliability semantics đúng (retry/breaker/drain), benchmark có phương pháp với báo cáo tái lập được, fault-injection campaign + postmortem, K8s deploy cơ bản, 5–7 papers nắm chắc, 2 codebase đọc có bản đồ, bộ đáp án phỏng vấn gắn artifact.

**Phải cắt (đã cắt ở Section 4):** Triton, TensorRT-LLM, Ray Serve/KServe, agent runtime, full eval platform, autoscaling GPU thật, mọi thứ distributed-coordination, C++/CUDA hands-on.

**Nên kéo dài sau tuần 24 (giai đoạn 2 tự nhiên):** (1) NVIDIA-style path: C++ + CUDA nghiêm túc 6–12 tháng, bắt đầu bằng đọc TensorRT-LLM batch manager; (2) Durable Agent Runtime trên Temporal (60–80h) nếu thị trường kéo về hướng agent infra; (3) đóng góp ngược một PR nhỏ cho GAIE/llm-d hoặc vLLM (docs/tests trước) — giá trị tín nhiệm cao hơn mọi side project.

**Mức sẵn sàng nghề nghiệp mà dự án này chống lưng được một cách TRUNG THỰC:**
- **Đủ sức cạnh tranh:** AI Platform Engineer, Inference Platform Engineer (tầng gateway/serving-platform), ML Platform, AI Reliability/Observability, Distributed Systems Engineer tại AI company, Forward Deployed với systems depth — vì các role này phỏng vấn đúng những gì dự án chứng minh: systems design, reliability, đo lường, và hiểu đúng ranh giới engine.
- **Chưa đủ:** vai trò làm việc BÊN TRONG engine (viết kernel, tối ưu TensorRT-LLM, NVIDIA System Software) — cần giai đoạn 2. Nói thẳng điều này trong phỏng vấn ("tôi vận hành và xây quanh engine; tôi đọc được scheduler của nó; tôi chưa viết kernel") là câu trả lời mạnh, không phải điểm yếu.
- **Xác suất thành công [SUY LUẬN, không phải số đo]:** với 6 năm nền distributed systems + kỷ luật 20h/tuần, phần rủi ro lớn nhất KHÔNG phải kỹ thuật mà là scope control và độ bền — kế hoạch này được thiết kế để cả hai có cơ chế kiểm soát (milestone 2 tuần có demo, bảng cắt phạm vi, fallback cho GPU).

---

## Phụ lục A: Nguồn chính đã dùng

**Primary (đã verify):** arXiv:2309.06180 (PagedAttention, SOSP 2023) · Orca (OSDI 2022, usenix.org) · arXiv:2312.07104 (SGLang, NeurIPS 2024) · DistServe (OSDI 2024, usenix.org) · arXiv:2205.14135 (FlashAttention) · arXiv:2211.17192 (Speculative Decoding) · arXiv:2410.14257 (SLO/goodput critique) · vllm-project/vllm main branch @ 2026-07-08 (scheduler.py, output.py, core.py, core_client.py, coordinator.py, block_pool.py, kv_cache_utils.py, cache.py, benchmarks/) · blog.vllm.ai "Anatomy of vLLM" (2025-09-05, pinned commit 42172ad) · blog.vllm.ai V1 alpha (2025-01-27) · docs.vllm.ai arch_overview · vLLM RFC #8779 · kubernetes-sigs/gateway-api-inference-extension · BerriAI/litellm (v1.91.0) · llm-d-kv-cache-manager, llm-d-inference-scheduler · Red Hat Developers llm-d KV-cache routing (2025-10-07).

**Secondary/blog (dùng có dán nhãn):** BentoML LLM inference handbook · insujang.github.io continuous batching/PagedAttention walkthrough (2024-01-07, pinned vLLM v0.2.7) · jimmysong.io GAIE deep-dive (2025-11-14).

**Nguồn bị loại vì không đạt chuẩn trích claim:** GKE Inference Gateway concept page, TrueFoundry rate-limiting blog, NVIDIA benchmarking blog (fetch fail), techinterview.org, aitechconnect.in — phần interview/career trong báo cáo này do đó là [SUY LUẬN/KHUYẾN NGHỊ] từ kinh nghiệm domain, không phải facts đã verify.

## Phụ lục B: Bốn câu hỏi mở cần tự đóng trong quá trình thực hiện

1. **(Đóng ở M5)** vLLM phơi bày chính xác metrics nào qua `/metrics` (queue depth waiting/running, KV cache utilization, prefix hit rate?) đủ cho health/load-aware routing không cần ext-proc/KVEvents — quyết định thiết kế router v2.
2. **(Đóng ở M11)** SGLang vs vLLM V1 khác gì thực nghiệm về scheduler/prefix caching trên workload có kiểm soát prefix-sharing ratio.
3. **(Đóng ở M5/M8)** Ngưỡng phần cứng tối thiểu để số TTFT/ITL có giá trị thuyết phục — A10 thuê theo giờ có đủ không, hay cần A100.
4. **(Đóng ở tuần đọc Repo 2)** Cơ chế flow-control/fairness/priority đã shipped ở GAIE v1.5.0 hoạt động chính xác thế nào, và khoảng trống fairness đa tenant nào còn thật sự trống cho dự án cá nhân khác biệt hóa.
