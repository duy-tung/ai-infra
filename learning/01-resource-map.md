# 01 — Resource map: học gì, skip gì

Nguồn: [`rohitg00/ai-engineering-from-scratch`](https://github.com/rohitg00/ai-engineering-from-scratch)
— ~20 phases, ~503 lessons, ~320 giờ. Mỗi lesson tạo artifact (prompt, skill,
agent, hoặc MCP server).

> ⚠️ **Đừng học tuyến tính 503 lessons.** Với profile của bạn, học tuyến tính sẽ
> loãng và mất 6–12 tháng chưa tạo được signal career. Dùng nó như **menu chọn
> module để build portfolio.** Skip có chủ đích.

## Phase ưu tiên cao nhất (xương sống)

| Ưu tiên | Phase | Học vì | Map tới sprint |
|---------|-------|--------|----------------|
| 1 | **14 — Agent Engineering** | agent loop, tool use, memory, LangGraph, Agent SDKs, observability, eval-driven dev, verification gates, reviewer agent, workbench trên repo thật | [Sprint 1](sprints/sprint-1-agent-foundations.md) |
| 2 | **13 — Tools & Protocols** | function calling, tool schema, MCP server/client, MCP security, OTel GenAI, LLM routing | [Sprint 2](sprints/sprint-2-tools-protocols.md) |
| 3 | **17 — Infrastructure & Production** | inference metrics, LLM observability stack, caching, model routing, AI gateway, canary, load testing, SRE for AI, security/PII/audit, FinOps | [Sprint 3](sprints/sprint-3-production-infra.md) |
| 4 | **19 — Capstone** | build portfolio: observability/eval dashboard, issue→PR agent, MCP registry+governance, code migration agent | [Sprint 4](sprints/sprint-4-capstone.md) |
| 5 | **11 — LLM Engineering** | structured output, function calling, eval & testing, caching/cost, guardrails, RAG | Sprint 1 (nền) |
| 6 | **15 — Autonomous Systems** | permission model, rollback, kill switch, cost governor, failure modes | Sprint 3–4 |

## Phase học CHỌN LỌC (không học hết)

- **Phase 10 — LLMs from Scratch:** chỉ tokenizer, evaluation, inference
  optimization, quantization — **ở mức hiểu**, không build.
- **Phase 7 — Transformers:** chỉ attention, KV cache, speculative decoding — nếu
  muốn hiểu inference. Không cần code transformer from scratch.
- **Phase 16 — Multi-Agent:** chỉ supervisor/orchestrator-worker,
  planner/critic/executor/verifier, failure modes.
- **Phase 18 — Safety:** prompt injection, PII, audit, red-team tooling, compliance.

## Phase BỎ QUA tạm thời

Vision · Speech/audio · Diffusion/video · RL sâu · Training from scratch ·
Multimodal nâng cao.

> Những phần này hay, nhưng **không trực tiếp** giúp bạn thành AI infra / agent
> platform engineer trong fintech/backend. Quay lại sau nếu cần.

## Nguyên tắc khi học mỗi lesson

1. **Build artifact** thật (commit vào repo này), đừng chỉ đọc.
2. Ghi note ngắn vào [`notes/`](notes/) theo phase (dùng [`_template.md`](notes/_template.md)).
3. Nối artifact vào portfolio: nó phục vụ project nào trong `projects/`?
4. Áp tỉ lệ **70% build / 20% đọc / 10% viết-public**.

## Thứ tự đọc → build (tóm tắt)

```
Sprint 1 (Agent foundations) → build agent-workbench
Sprint 2 (Tools/Protocols)   → thêm MCP server + OTel vào workbench
Sprint 3 (Production infra)   → eval harness, sandbox, metrics, security
Sprint 4 (Capstone)           → fintech-backend-guard-agent + observability dashboard
```
