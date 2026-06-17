# Sprint 4 — Capstone (Tuần 14+)

**Mục tiêu:** dùng nền đã build (workbench + MCP + OTel + sandbox + metrics) để
ra **portfolio project gắn fintech**.

## Lessons (đọc — 20%)

**Phase 19 — Capstone Projects.** Chọn **2 trong các capstone**:
1. LLM Observability & Eval Dashboard ⭐
2. GitHub Issue-to-PR Autonomous Agent ⭐
3. DevOps Troubleshooting Agent for Kubernetes
4. MCP Server with Registry and Governance
5. Code Migration Agent

> Gợi ý cho profile của bạn: **(1) Observability & Eval Dashboard + (2) Issue-to-PR Agent**,
> rồi biến thành **fintech-flavored PR Review / Incident Agent**.

Deep-build track (Phase 19): tool registry · verification gates · sandbox runner ·
eval harness · OTel GenAI spans · Prometheus metrics · end-to-end coding agent.

## Build (70%) → [`projects/fintech-backend-guard-agent/`](../../projects/fintech-backend-guard-agent/)

Theo spec trong README của project đó. Tối thiểu cho v1:

- [ ] Context loader: đọc Git diff + migration SQL + test output.
- [ ] Fintech risk classifier (rule + LLM).
- [ ] Static checks (idempotency, money precision, migration lock, audit, PII).
- [ ] LLM reviewer với severity rubric (structured output).
- [ ] Eval set 30–50 fixture PRs (mỗi loại rủi ro ≥ 1 fixture).
- [ ] Human approval gate (advisory only lúc đầu).
- [ ] Report: severity + suggested patch + confidence.
- [ ] Dashboard: runs, pass/fail, cost, latency, risk categories.

## Deliverable cuối sprint

- Repo `fintech-backend-guard-agent` public/anonymized, README tiếng Anh đầy đủ.
- Observability/eval dashboard.
- Bài viết: **"An AI PR-review agent for fintech backends: idempotency, migrations, ledgers, audit."**
- Cập nhật CV bullet (xem [`../03-career-path-3-years.md`](../03-career-path-3-years.md)).

## Tick skill checklist

severity rubric · eval dashboard · false positive/negative tracking · reviewer/builder
separation + toàn bộ **fintech domain moat** (idempotency, ledger, reconciliation, ...).
