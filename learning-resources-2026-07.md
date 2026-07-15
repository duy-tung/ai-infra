# Danh sách tài nguyên học tập — 2026-07 (bám audit Rev 3 + study track sẵn có)

Nguyên tắc kế thừa từ `portfolio-planning/08-study-track.md`: **không học vì học** — mỗi tài
nguyên phải có (a) repo/task tiêu thụ, (b) artifact đầu ra, (c) điều kiện dừng. Tracker trạng
thái: `inference-lab/study/tracker.md`. Cột "Phase" trỏ tới prompt remediation
(`portfolio-planning/prompts/06-audit-remediation.md`).

Ưu tiên tổng thể theo audit: **B (reliability/benchmark) → A (serving platform) → C (runtime)
→ D (K8s/GPU)** — nhưng gap chí mạng nhất là C/D substrate, nên track C/D học *song song* ở
mức nền tảng.

## 1. BẮT ĐẦU TẠI ĐÂY (tuần 1–2, phục vụ phỏng vấn + Phase R0/R1)

| # | Tài nguyên | Loại | Vì sao / artifact | Phase |
|---|---|---|---|---|
| 1 | Gil Tene — **"How NOT to Measure Latency"** (talk, tìm trên YouTube/InfoQ) | Talk | Nền tảng coordinated-omission — chính là điểm mạnh nhất của inferbench; phải nói trôi chảy khi phỏng vấn | R0, §9 Q8 |
| 2 | **Google SRE Book** (sre.google/books — miễn phí): chương *Handling Overload*, *Addressing Cascading Failures* | Sách | Ngôn ngữ chuẩn cho admission/retry-budget/shed — đối chiếu với IG-T010/T013 | R1.3 |
| 3 | **Orca** (OSDI'22) — đọc sâu §1–3 | Paper | Cơ sở của ADR-0005 "gateway must not batch" — câu hỏi phỏng vấn chắc chắn gặp | §11.2-2 |
| 4 | **PagedAttention / vLLM** (SOSP'23, arXiv 2309.06180) — §1–4, §6.1–6.2, bỏ kernel | Paper | Hiểu KV-cache để trả lời "vì sao chưa có KV work là gap" | R3 chuẩn bị |
| 5 | Brendan Gregg — **Systems Performance 2e**: chương Methodology + Latency (kèm brendangregg.com/usemethod) | Sách | USE method — checklist review benchmark của chính mình | R1 |

## 2. Track B — Reliability / Benchmark / Release (điểm mạnh, cần đào sâu)

| Tài nguyên | Loại | Ghi chú / artifact | Phase |
|---|---|---|---|
| Google **SRE Workbook** (miễn phí, sre.google) — SLO chương 2, alerting chương 5 | Sách | Viết lại SLO doc của portfolio bằng error-budget đúng nghĩa | R0.7 |
| Michael Nygard — **Release It! 2e** | Sách | Circuit breaker, bulkhead, timeout patterns — đối chiếu code infergate/reliability | R1.3 |
| **Jepsen analyses** (jepsen.io/analyses) — đọc 2–3 bài (Postgres, etcd) | Blog | Cách viết báo cáo phá-hệ-thống chuẩn mực; nâng chất fault campaign | R1.4 |
| **HdrHistogram** docs + Tene's latency talks tiếp theo | Tool/Docs | Percentile đúng cách; đối chiếu pooled_table | — |
| Charity Majors / **Honeycomb blog** — observability, SLO thực chiến | Blog | Nâng dashboard/alert từ "có" lên "vận hành được" | R2 |
| **Chaos Engineering** (Principles of Chaos + Netflix tech blog các bài Chaos Monkey/FIT) | Blog | Đưa fault campaign lên chuẩn có giả thuyết + steady-state | R1.4 |
| **100 Go Mistakes** (100go.co) — phần concurrency (#55–#72) | Sách/Web | Race grant/cancel của admission chính là mistake loại này; đọc trước khi fix R1.3 | R1.3 |
| Go blog: **"Go Concurrency Patterns: Context"** + pipelines/cancellation | Blog | Chuẩn hoá cancellation semantics khi sửa relay/slow-client | R1.4, R2.3 |

## 3. Track C — Inference runtime / LLM serving (gap chí mạng #1)

| Tài nguyên | Loại | Ghi chú / artifact | Phase |
|---|---|---|---|
| **vLLM docs** (docs.vllm.ai) + vLLM blog — bắt đầu: serving args, metrics, scheduler | Docs | Chuẩn bị trực tiếp cho R3 (GPU slice); đọc kèm source-reading plan §4 của study track | R3 |
| **Source reading vLLM V1** theo đúng plan sẵn có: `vllm/v1/engine/async_llm.py`, `core.py`, `v1/core/sched/scheduler.py`, `kv_cache_manager.py` — vẽ "life of a streaming request" | Source | Artifact đã định nghĩa sẵn trong track §4: sequence diagram + 3 boundary tests | R3 |
| **BentoML — LLM Inference Handbook** (bentoml.com/llm) | Handbook | Tổng quan serving/batching/KV/quantization theo góc infra — đúng level cần | R3 |
| kipply — **"LLM Parameter Counting / Inference Arithmetic"** (kipp.ly blog) | Blog | Bảng tính capacity bằng tay: bandwidth-bound vs compute-bound | R6 |
| Horace He — **"Making Deep Learning Go Brrrr From First Principles"** (horace.io) | Blog | Trực giác memory-bandwidth/overhead — nền cho profiling | R3 |
| **Modal GPU Glossary** (modal.com/gpu-glossary) | Docs | Từ vựng GPU chuẩn (SM, HBM, occupancy) — đọc 1 buổi | R3 |
| Papers theo track §3 (đọc theo depth đã định): **Sarathi-Serve** (2403.02310), **DistServe** (2401.09670), **SGLang/RadixAttention** (2312.07104), **Mooncake** (2407.00079), **FlashAttention** (2205.14135, skim), **Pope et al.** (2211.05102, skim), **speculative decoding** (2211.17192, skim) | Papers | Artifact + stop condition đã ghi trong tracker — giữ nguyên | R3/R6 |
| **GPU MODE** lectures (github.com/gpu-mode/lectures + Discord) — 3–4 bài đầu | Course | Chỉ đến mức đọc hiểu profile/kernel-name; KHÔNG sa đà viết kernel (ngoài scope audit) | R3 |
| PMPP — **Programming Massively Parallel Processors** (chọn chương memory hierarchy) | Sách | Chỉ nếu GPU MODE thấy hổng nền; artifact-or-drop | stretch |
| **Anyscale/Baseten blog** — các bài benchmark LLM serving (continuous batching, TTFT/ITL) | Blog | So chuẩn phương pháp đo của mình với industry | R3 |

## 4. Track D — Kubernetes / hạ tầng GPU (gap chí mạng #2)

| Tài nguyên | Loại | Ghi chú / artifact | Phase |
|---|---|---|---|
| **Kubernetes docs — Concepts** (kubernetes.io): Pod lifecycle, probes, Deployment/rollout, HPA, PDB, scheduler | Docs | Đọc đúng các mục audit chấm 0–1 điểm; mỗi mục 1 lab kind | R4 |
| Kelsey Hightower — **Kubernetes the Hard Way** (github) | Lab | Hiểu control plane bằng tay — 1 lần, không lặp lại | R4 |
| **kind / k3d** docs + lab: dựng cluster CÓ agent, schedule đúng stack Kustomize sẵn có | Lab | Đây chính là Phase R4; học = làm luôn trên manifests thật của inferops | R4 |
| **KWOK** (kwok.sigs.k8s.io) — giả lập node/scheduling không cần máy thật | Tool | Thí nghiệm scheduler/HPA logic rẻ tiền trước khi thuê máy | R4 |
| **KEDA docs** (keda.sh) — scalers, cooldown | Docs | ADR-0003 đã reject KEDA; giờ học để *thực thi* nó có căn cứ | R4 |
| **NVIDIA GPU Operator + device plugin docs** (docs.nvidia.com) | Docs | Đường từ "limits: nvidia.com/gpu" tới pod thật trên node GPU | R4/R3 |
| **Kubebuilder book** (book.kubebuilder.io) — tutorial 1 controller | Course | Chỉ khi nhắm role D thật sự; nếu không, dừng ở đọc concepts | stretch |
| **Production Kubernetes** (O'Reilly, Rosso et al.) — chương rollout/multi-tenancy | Sách | Đọc chọn lọc sau khi R4 chạy được | stretch |

## 5. Nền tảng distributed systems / DB (đã có trong track, giữ nguyên)

| Tài nguyên | Phạm vi đã chọn trong track | Artifact/consumer |
|---|---|---|
| **MIT 6.5840** (pdos.csail.mit.edu/6.5840) | RPC semantics, at-most-once, linearizability, fault tolerance — KHÔNG làm full Raft lab | 6 artifact ADR/experiment infergate (tracker §1) |
| **CMU 15-445** (15445.courses.cs.cmu.edu) | MVCC, logging, crash recovery | ledger/recovery designs (tracker §2) |
| **DDIA** — Kleppmann | Chương consistency/replication/transactions | input cho IG-T015/T018 ADRs |
| **Database Internals** — Petrov | Storage/recovery | ledger design |
| **AI Engineering** — Chip Huyen | Chương serving/inference | review cấu trúc capacity report |
| Murat Demirbas blog + Aleksey Charapko **DistSys Reading Group** | Blog | Duy trì nhịp đọc paper 1 bài/tuần sau khi xong track |

## 6. Blog / Newsletter / Podcast theo dõi định kỳ

- **vLLM blog** + release notes — bắt buộc (substrate mục tiêu).
- **SGLang blog** — đối chiếu scheduler/radix cache.
- **Baseten blog + guides**, **Modal blog**, **Anyscale blog** — serving infra thực chiến.
- **SemiAnalysis** — kinh tế GPU/hardware (đọc bài free).
- **Interconnects** (Nathan Lambert) — bức tranh model/ecosystem.
- **Chip Huyen**, **Eugene Yan**, **Lilian Weng** — tổng hợp ML systems.
- **Simon Willison** — cập nhật ứng dụng LLM hằng ngày, nhanh.
- **Latent Space podcast** — phỏng vấn founder/infra engineers.
- **Brendan Gregg blog**, **Netflix TechBlog**, **Cloudflare blog** (systems), **Honeycomb blog** (observability), **Uber/Meta engineering** — hệ thống lớn.
- **Jepsen** — mỗi bài mới là một bài học fault-finding.
- **The Pragmatic Engineer** — thị trường + practices (phục vụ chuyển việc).

## 7. Lộ trình gợi ý 12 tuần (song song với remediation)

| Tuần | Học | Làm (phase) |
|---|---|---|
| 1–2 | Mục 1 (Tene, SRE overload, Orca, PagedAttention, USE method) | R0 + R1.1/R1.2 |
| 3–4 | 100 Go Mistakes concurrency, Go context patterns, Release It! | R1.3 (admission race) + R1.4 (scenario-4) |
| 5–6 | vLLM docs + source reading V1 (sequence diagram), BentoML handbook, kipply, Modal glossary | R1.5–R1.9, chuẩn bị R2 |
| 7–8 | SRE Workbook SLO, Honeycomb, Jepsen ×2 | R2 (N-backend, readyz, slow-client) |
| 9–10 | K8s concepts + Hard Way + kind/KWOK labs, KEDA, GPU Operator docs | R4 chạy thử trên kind |
| 11–12 | Sarathi/DistServe/Mooncake + GPU MODE 1–4, Horace He | R3 (GPU vLLM slice — nếu ngân sách được duyệt) |
| liên tục | 1 paper/tuần (mục 5), blogs mục 6 | cập nhật `study/tracker.md` mỗi buổi |

**Quy tắc dừng (giữ nguyên từ track):** tài nguyên nào sau 2 buổi không tạo ra artifact nằm
trong register/remediation thì đánh `dropped (reason)` trong tracker và bỏ, không tiếc.
