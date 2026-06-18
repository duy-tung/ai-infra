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

> 💡 Đã có **starter chạy được** trong `fintech-backend-guard-agent/` (diff parser,
> static checks, secret/PII scrubbing, LLM reviewer structured-output, report +
> severity gate, CLI, eval 7 fixture P/R=1.00, 31 test). Việc của bạn: **đọc hiểu,
> chạy `make eval` + `--llm` với key thật, và mở rộng** các mục dưới.

Theo spec trong README của project đó. Tối thiểu cho v1:

- [x] Context loader: đọc Git diff + migration SQL _(starter: `diff.py`, `pipeline.py`)_
- [x] Static checks (idempotency, money precision, migration lock, audit, PII) _(starter: `checks.py`)_
- [x] LLM reviewer với severity rubric (structured output) _(starter: `reviewer.py`)_
- [x] Report: severity + suggested patch + confidence; human approval gate (advisory) _(starter: `report.py`)_
- [x] Eval set 33 fixture PRs / 14 risk categories (P/R=1.00) — `evals/fixtures/*.json` _(target 30–50: đã đạt 33; thêm nữa khi gặp case thật)_
- [ ] Context loader: đọc thêm test output + service ownership doc.
- [ ] PR comment bot (GitHub Action chạy trên PR → post review).
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
