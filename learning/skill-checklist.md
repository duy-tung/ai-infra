# Skill checklist — để đạt "loại 3"

Đánh dấu `[x]` khi bạn **làm được và có artifact chứng minh** (không phải "đã đọc").
Mỗi mục nên link tới commit/PR/file trong repo.

## 1. Agent infrastructure

- [ ] agent loop
- [ ] tool registry
- [ ] structured output
- [ ] MCP server/client
- [ ] permission model
- [ ] sandbox execution
- [ ] task boundary
- [ ] repo memory
- [ ] multi-session handoff
- [ ] reviewer/builder separation

> Phần lớn mục này có starter trong [`projects/agent-workbench/`](../projects/agent-workbench/).

## 2. Eval & verification

- [ ] fixture-based eval
- [ ] code execution metric
- [ ] golden test set
- [ ] regression test
- [ ] property-based testing
- [ ] severity rubric
- [ ] LLM-as-judge (có kiểm soát)
- [ ] eval dashboard
- [ ] false positive / false negative tracking

## 3. Observability

- [ ] OpenTelemetry traces cho agent runs
- [ ] token / cost / latency metrics
- [ ] tool-call success rate
- [ ] error taxonomy
- [ ] prompt / model / version tracking
- [ ] incident timeline
- [ ] agent failure replay

## 4. Security / compliance

- [ ] PII scrubbing
- [ ] secrets detection
- [ ] prompt injection defense
- [ ] tool permission
- [ ] audit log
- [ ] least privilege
- [ ] approval gate
- [ ] data retention policy
- [ ] SOC2 / GDPR / EU AI Act awareness (mức engineer)

## 5. Fintech domain moat

- [ ] idempotency
- [ ] ledger
- [ ] reconciliation
- [ ] transaction state machine
- [ ] settlement
- [ ] chargeback / refund
- [ ] audit trail
- [ ] fraud / risk
- [ ] precision / rounding
- [ ] compliance reporting

---

> Combo **(1–4) × (5)** = thứ làm bạn khác với "AI engineer chung chung".
> Đừng cố tick hết một lần — tick dần theo sprint, mỗi tick gắn 1 artifact thật.
