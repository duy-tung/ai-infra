# Brag doc

Ghi lại **impact ngay khi nó xảy ra** — đừng đợi tới review/CV mới nhớ lại. Mỗi
mục viết được thành 1 CV bullet hoặc 1 talking point khi phỏng vấn.

Format mỗi mục: **Situation → Action → Result (có số liệu nếu được)** — viết bằng
**tiếng Anh** (luyện luôn cho CV/phỏng vấn global).

---

## Template

```
### [YYYY-MM] Tiêu đề ngắn
- Situation: bối cảnh / vấn đề.
- Action: bạn làm gì (kỹ thuật cụ thể).
- Result: kết quả + số liệu (bugs caught, cost/PR, latency, time saved, %...).
- Link: PR / repo / dashboard / doc.
- Skills: agent infra / eval / observability / security / fintech.
```

---

## Entries

### [2026-__] Built a minimal coding-agent harness
- Situation: needed to understand agent internals (loop, tools, permissions) before building higher-level agents.
- Action: built `agent-workbench` — manual agent loop, tool registry, path-jailed file/shell tools, permission gate (ask/auto/readonly), JSONL tracing with token+USD cost accounting, and a fixture-based eval runner. 20 offline unit tests.
- Result: _(add: # fixtures passing, cost/run, demo link)_
- Link: `projects/agent-workbench/`
- Skills: agent infra, eval, observability, security.

### [2026-__] Built an AI PR-review agent for fintech backends  _(draft)_
- Situation: generic AI code review misses the risks that actually cause fintech incidents.
- Action: built `fintech-backend-guard-agent` — a deterministic 14-category risk checker (idempotency, money precision, migration locks, ledger imbalance, audit gaps, secrets/PII) + an LLM reviewer (structured output) + severity gate + a GitHub Action that posts a sticky advisory PR comment. Diffs scrubbed before reaching the model; OpenTelemetry spans with token/cost.
- Result: 48 tests; 33 eval fixtures across 14 categories at precision/recall = 1.00; eval-driven development surfaced 2 real regex bugs unit tests missed.
- Link: `projects/fintech-backend-guard-agent/`
- Skills: eval, security, observability, fintech domain.

### [2026-__] Built a read-only incident-triage agent  _(draft)_
- Situation: the slow part of an incident is "what changed and what broke?".
- Action: built `ai-incident-triage-agent` — deterministic correlation (suspect deploys by time proximity, normalized error signatures, blast radius, timeline, rollback candidate, confidence) + an LLM hypothesis layer; read-only by design; OpenTelemetry spans with cost.
- Result: 26 tests; top-1 suspect-deploy accuracy = 100% on the fixture set (incl. ambiguous + no-deploy cases).
- Link: `projects/ai-incident-triage-agent/`
- Skills: observability, eval, agent infra.

<!-- Thêm entry mới phía trên (newest first). -->
