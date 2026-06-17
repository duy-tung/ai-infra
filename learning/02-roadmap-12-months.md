# 02 — Roadmap 12 tháng

Mỗi mốc có: **mục tiêu**, **học gì**, **build gì**, **output để public**.

---

## 0–30 ngày — Dựng nền agent workbench

**Mục tiêu:** hiểu agent loop + tool calling + tracing + eval cơ bản.

**Học:** Phase 11 (structured output, function calling, eval, caching/cost,
guardrails) · Phase 13 (tool interface, schema, MCP fundamentals, OTel GenAI) ·
Phase 14 (agent loop, tool use, failure modes, eval-driven dev, verification gates).

**Build → [`projects/agent-workbench/`](../projects/agent-workbench/) (đã có starter chạy được):**
- agent loop · tool registry · file read/write tool · shell tool · permission gate
- trace log · cost/token log · simple eval runner.

**Output cuối tháng:**
- GitHub repo public.
- README tiếng Anh.
- Demo video/GIF ngắn.
- 1 bài viết: *"Building a minimal coding agent harness with verification gates."*

---

## 30–90 ngày — Build "Fintech Backend Guard Agent" (project chính)

**Mục tiêu:** một agent review PR/Git diff cho backend fintech — **không chỉ
review style code**, mà review rủi ro fintech.

**Build → [`projects/fintech-backend-guard-agent/`](../projects/fintech-backend-guard-agent/)** (spec sẵn).
Agent check: idempotency · retry double-charge · transaction boundary · decimal/money
precision · ledger imbalance · reconciliation missing path · SQL migration lock risk ·
audit log · PII/secrets · missing metric/span · rollback plan · test coverage cho failure case.

**Output cuối 90 ngày:**
- Repo `fintech-backend-guard-agent`.
- Dashboard: agent runs, pass/fail, cost, latency, risk categories.
- Eval set 30–50 fixture tasks.
- README rất kỹ bằng tiếng Anh.

---

## 3–6 tháng — Production discipline

**Mục tiêu:** không chỉ demo — có kỷ luật production.

**Thêm:** eval harness với fixture tasks · regression tests · sandbox runner ·
denylist/path jail · policy-as-code · PR comment bot · OTel spans · Prometheus
metrics · canary mode · human-in-the-loop approval · audit log.
(Match Phase 19 deep-build track.)

**KPI cần đo:** review precision · false positives · bugs caught · cost/PR ·
median review latency · % PR auto-classify risk đúng · time saved · escaped bugs.

Nếu công ty cho phép: đề xuất dùng nội bộ ở mode **"advisory only"** (không
auto-block merge lúc đầu).

---

## 6–9 tháng — Build "AI Incident Triage Agent" (project 2)

**Mục tiêu → [`projects/ai-incident-triage-agent/`](../projects/ai-incident-triage-agent/):**
Incident triage cho Go/Postgres services.

**Input:** alert · logs · traces · recent deploys · Git diff · runbook · DB metrics · SLO dashboard.
**Output:** suspected root cause · blast radius · rollback suggestion · queries nên chạy ·
service owner · confidence score · timeline incident.

Dùng Phase 17 (LLM observability stack, AI gateway, canary, load testing,
multi-agent incident response, chaos engineering, security, compliance, FinOps)
để nâng từ demo → production-grade.

---

## 9–12 tháng — Đóng gói "Agent Control Plane"

Gom 2 project thành 1 narrative: **Agent Control Plane for AI-native Software Engineering.**

```
1. Agent Harness            5. PR Review Agent
2. Tool Registry            6. Incident Triage Agent
3. Permission & Sandbox     7. Observability Dashboard
4. Eval Runner              8. Policy/Audit Layer
```

Đây là thứ tách bạn khỏi người chỉ "dùng AI code nhanh".

---

## Tóm tắt mốc

| Mốc | Deliverable |
|-----|-------------|
| 90 ngày | Fintech Backend Guard Agent bản đầu |
| 6 tháng | + eval, sandbox, OTel, dashboard, PR bot |
| 12 tháng | Agent Control Plane portfolio + impact nội bộ |
| 24 tháng | Chuyển scope sang platform / nhảy fintech-global |
| 36 tháng | Apply AI Platform / Agent Infra / Evals / Observability |

→ Career path chi tiết: [`03-career-path-3-years.md`](03-career-path-3-years.md).
