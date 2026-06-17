# projects/ — portfolio

Three repos that, together, tell one story: **an Agent Control Plane for
AI-native software engineering**, grounded in fintech backend production.

| # | Project | What it is | Status | Sprint |
|---|---------|------------|--------|--------|
| 1 | [`agent-workbench/`](agent-workbench/) | Minimal coding-agent harness: loop, tool registry, permission gate, tracing, eval runner. The foundation everything else builds on. | ✅ Runnable starter | [1](../learning/sprints/sprint-1-agent-foundations.md) |
| 2 | [`fintech-backend-guard-agent/`](fintech-backend-guard-agent/) | PR-review agent for fintech backends — idempotency, migrations, ledger, audit, PII. The headline portfolio piece. | 🔜 Spec ready | [4](../learning/sprints/sprint-4-capstone.md) |
| 3 | [`ai-incident-triage-agent/`](ai-incident-triage-agent/) | Incident assistant for Go/Postgres services — parse logs/traces, correlate deploys, suggest root cause + rollback. | 🔜 Spec ready | post-month-6 |

## How they relate

```
agent-workbench  ──provides──▶  agent loop · tool registry · permission gate
   (foundation)                 sandbox · eval runner · tracing/cost
        │
        ├──▶ fintech-backend-guard-agent   (reuses the harness; adds fintech checks + reviewer)
        └──▶ ai-incident-triage-agent      (reuses the harness; adds log/trace/deploy correlation)
```

Build #1 first and well. #2 and #3 are not green-field — they *consume* the
harness, which is exactly the "platform vs app" distinction that signals a
"type 3" engineer.

## Every portfolio repo must have

(See each README — these sections are the highest-signal part of the portfolio.)

- README in English · architecture diagram · demo (GIF/video)
- **What I learned** · **Production considerations** · **Failure modes**
- **Security model** · **Evaluation methodology**

> Mỗi repo, khi public, anonymize mọi thứ thuộc về công ty. Dùng synthetic
> fixtures cho eval, không dùng data thật của fintech employer.
