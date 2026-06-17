# Sprint 3 — Production infra (Tuần 9–13)

**Mục tiêu:** biến agent từ demo → **production discipline**: sandbox, metrics,
caching, security, cost governance. Đây là phần biến bạn thành "loại 3" thật sự.

## Lessons (đọc — 20%)

**Phase 17 — Infrastructure & Production**
- Inference Metrics
- LLM Observability Stack Selection
- Prompt / Semantic Caching
- Model Routing · AI Gateways
- Shadow / Canary Deployment
- Load Testing LLM APIs
- SRE for AI
- Security — Secrets, PII, Audit Logs
- FinOps for LLMs

**Phase 15 — Autonomous Systems (chọn lọc)**
- Permission model · Rollback · Kill switch · Cost governor · Failure modes

## Build (70%)

- [ ] **Sandbox runner**: chạy `run_shell` trong container/VM ephemeral (không phải host).
- [ ] **Prometheus metrics** endpoint: agent runs, tool-call success rate, cost, latency histogram.
- [ ] **Prompt caching**: cache system prompt + tool defs; verify `cache_read_input_tokens` > 0.
- [ ] **Cost governor**: hard cap USD/run + token budget; kill switch khi vượt.
- [ ] **PII/secrets scrubbing** trên trace + tool I/O (regex + entropy detector).
- [ ] **Audit log** append-only cho mọi mutating tool call + permission decision.
- [ ] **Policy-as-code**: permission rules ra file YAML thay vì hardcode.
- [ ] **Load test**: chạy N agents song song, đo p50/p95 latency + cost.

## Deliverable cuối sprint

- agent-workbench có sandbox + Prometheus + Grafana dashboard (Docker Compose).
- Bài viết: **"Production hardening an agent: sandbox, metrics, cost governors, audit."**

## Tick skill checklist

sandbox execution · Prometheus metrics · error taxonomy · secrets detection ·
PII scrubbing · audit log · least privilege · data retention · cost governor (kill switch).
