# ai-infra — Agent Platform / AI Infrastructure learning + build workspace

> Mục tiêu: trở thành **"loại 3"** — kỹ sư xây *platform / eval / observability /
> security layer* để nhiều AI agent làm việc trong codebase thật, **có kiểm soát,
> có đo lường, có rollback, có audit**. Không phải "biết dùng Claude Code giỏi",
> mà là **người xây hạ tầng cho agent**.
>
> Goal: become a **"type 3" engineer** — someone who builds the platform, eval,
> observability, and security layers that let many AI agents work safely in a
> real codebase. Target roles: AI Platform Engineer, Agent Infrastructure
> Engineer, Evaluation Infrastructure Engineer, Observability Platform Engineer.

This repo is **not** a copy of a course. It's a workspace that turns the
`rohitg00/ai-engineering-from-scratch` curriculum into a **menu** (we use Phases
13, 14, 17, 19 as the backbone and deliberately skip the academic parts) and
drives toward **2–3 portfolio projects** tied to fintech backend production.

Cách dùng tài nguyên đúng: **70% build, 20% đọc, 10% viết/public.** Đọc course mà
không build artifact thì giá trị thấp.

---

## Repo map

```
ai-infra/
├── README.md                     ← bạn đang ở đây (the hub)
├── learning/                     ← roadmap, sprints, schedule, trackers, notes
│   ├── 00-goal-and-target-roles.md     định nghĩa "loại 3" + target roles
│   ├── 01-resource-map.md              dùng resource thế nào: học gì, skip gì
│   ├── 02-roadmap-12-months.md         lộ trình 12 tháng (0–30 / 30–90 / ...)
│   ├── 03-career-path-3-years.md       career path 3 năm
│   ├── weekly-schedule.md              lịch tuần 8–10h, rule 70/20/10
│   ├── skill-checklist.md              checklist kỹ năng để đạt "loại 3"
│   ├── progress-tracker.md             theo dõi tiến độ hàng tuần
│   ├── brag-doc.md                     ghi lại impact (cho CV + review)
│   ├── sprints/                        4 sprint map tới phases cụ thể
│   └── notes/                          ghi chú học theo phase (+ template)
└── projects/                     ← portfolio (3 repo)
    ├── agent-workbench/                ✅ RUNNABLE (Sprint 1–3)
    ├── fintech-backend-guard-agent/    ✅ RUNNABLE starter (Sprint 4)
    └── ai-incident-triage-agent/       ✅ RUNNABLE starter (read-only)
```

---

## Bắt đầu từ đâu (start here)

1. Đọc [`learning/00-goal-and-target-roles.md`](learning/00-goal-and-target-roles.md)
   — chốt lại "loại 3" là gì và bạn nhắm role nào.
2. Đọc [`learning/01-resource-map.md`](learning/01-resource-map.md) — học phase nào,
   skip phase nào (đừng học tuyến tính 503 lessons).
3. Đọc [`learning/02-roadmap-12-months.md`](learning/02-roadmap-12-months.md) — kế hoạch theo mốc.
4. Bắt đầu **Sprint 1** ngay: [`learning/sprints/sprint-1-agent-foundations.md`](learning/sprints/sprint-1-agent-foundations.md)
   và build trên [`projects/agent-workbench/`](projects/agent-workbench/) (đã chạy được).

Lịch học: [`learning/weekly-schedule.md`](learning/weekly-schedule.md) (8–10h/tuần, đều đặn).
Theo dõi tiến độ: [`learning/progress-tracker.md`](learning/progress-tracker.md).

---

## The 3 portfolio projects (đích đến)

| # | Repo | Vai trò | Trạng thái |
|---|------|---------|-----------|
| 1 | `agent-workbench` | Agent harness: loop, tool registry, permission/policy, sandbox, eval, tracing+OTel, MCP, governor, redaction, audit, metrics | ✅ Chạy được (Sprint 1–3) |
| 2 | `fintech-backend-guard-agent` | PR-review agent cho backend fintech (idempotency, migration, ledger, audit, PII) | ✅ Starter chạy được (Sprint 4) |
| 3 | `ai-incident-triage-agent` | Incident assistant: correlate alert↔deploy↔errors, ranked root cause, blast radius, rollback, timeline | ✅ Starter chạy được (read-only) |

Sau 12 tháng, gom lại thành narrative: **"Agent Control Plane for AI-native
Software Engineering"** (harness + tool registry + permission/sandbox + eval +
PR review + incident triage + observability + policy/audit).

---

## Phase priority (xương sống)

| Ưu tiên | Phase | Vì sao |
|---------|-------|--------|
| 1 | 14 — Agent Engineering | Xương sống của agent platform |
| 2 | 13 — Tools & Protocols | MCP, tool schema, tracing, routing |
| 3 | 17 — Infrastructure & Production | Production, observability, security, cost |
| 4 | 19 — Capstone | Build portfolio |
| 5 | 11 — LLM Engineering | Eval, guardrails, caching, RAG, structured output |
| 6 | 15 — Autonomous Systems | Permission, rollback, kill switch, cost governor |

**Skip tạm thời:** Vision, Speech/audio, Diffusion/video, RL sâu, training from
scratch, multimodal nâng cao. Hay, nhưng không trực tiếp đưa bạn tới
AI infra/agent platform trong fintech/backend.

---

## Tech stack (theo profile fintech backend)

- **Go** cho backend service (sát profile fintech).
- **Python** cho agent harness / eval / LLM tooling (ecosystem mạnh nhất — xem `agent-workbench`).
- **Postgres** lưu runs. **OpenTelemetry + Prometheus/Grafana** cho observability.
- **GitHub Actions** + **Docker Compose**. **MCP** server cho repo/tools (Phase 13).
- LLM: **Claude** (Anthropic SDK), default model Opus 4.8, configurable.

---

_Nguồn curriculum: [rohitg00/ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch).
Tài nguyên rất đáng học — nhưng dùng như **menu chọn module để build portfolio**,
không học tuyến tính._
