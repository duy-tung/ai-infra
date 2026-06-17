# 00 — Mục tiêu "loại 3" & target roles

## "Loại 3" là gì?

Loại 1: biết dùng AI để code nhanh (Copilot/Cursor user).
Loại 2: biết tích hợp LLM vào sản phẩm (gọi API, RAG, chatbot).

> **Loại 3 = Engineer xây platform / eval / observability / security layer để
> nhiều AI agent có thể làm việc trong codebase thật — có kiểm soát, có đo lường,
> có rollback, có audit.**

Khác biệt cốt lõi: bạn **không phải người dùng agent**, bạn là **người xây hạ tầng
cho agent** — giống như khác biệt giữa "dùng Kubernetes" và "xây control plane".

## Target title (sau 2–3 năm)

- AI Platform Engineer
- Agent Infrastructure Engineer
- Evaluation Infrastructure Engineer
- Developer Productivity / AI Workbench Engineer
- Observability Platform Engineer
- Senior Backend Engineer, AI-native Platform
- Staff Backend/Platform, Fintech AI Systems

Các công ty đang tuyển đúng hướng này (tham khảo): OpenAI (Agent Infrastructure,
Evals, Observability, Developer Productivity, Core Services, Database Systems),
Anthropic (Research Tools, AI Observability, Safeguards Infrastructure, Inference
Systems), và các fintech/platform (Stripe, Airwallex, Wise, ZaloPay, MoMo, TCBS).

## Định nghĩa "done" cho 6 tháng đầu

> Có **một agent platform / eval / observability project** đủ mạnh để đưa vào CV
> hoặc dùng nội bộ trong fintech team.

Không phải "biết toàn bộ AI". Mục tiêu hẹp và sâu, gắn với **fintech backend
production** — đó là moat của bạn so với "AI engineer chung chung".

## Moat = AI infra × fintech domain

Bạn ghép **AI infrastructure** với **fintech domain** để khác biệt:

| AI infra | Fintech domain moat |
|----------|---------------------|
| agent loop, tool registry | idempotency |
| eval, verification gates | ledger, reconciliation |
| observability (OTel, metrics) | transaction state machine, settlement |
| security (PII, audit, least privilege) | chargeback/refund, audit trail |
| permission/sandbox, rollback | precision/rounding, compliance reporting |

→ Xem chi tiết checklist ở [`skill-checklist.md`](skill-checklist.md).

## Cách đo bản thân đang đi đúng hướng

Mỗi quý tự hỏi 3 câu:
1. Tôi đã **build** được artifact gì mới (không phải đọc)?
2. Artifact đó có **số liệu impact** không (bugs caught, cost/PR, time saved)?
3. Tôi có **viết lại bằng tiếng Anh** (README/blog/design doc) chưa?

Nếu 3 câu đều "có" → đang đi đúng. Nếu chỉ "đọc course" → giá trị career thấp.
