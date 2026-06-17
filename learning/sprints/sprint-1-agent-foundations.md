# Sprint 1 — Agent foundations (Tuần 1–4)

**Mục tiêu:** hiểu sâu agent loop + tool calling + tracing + eval, và mở rộng
[`projects/agent-workbench/`](../../projects/agent-workbench/) (đã có starter chạy được).

## Lessons (đọc — 20%)

**Phase 14 — Agent Engineering**
- The Agent Loop
- Tool Use and Function Calling
- Failure Modes — Why Agents Break
- Eval-Driven Agent Development
- Verification Gates
- Reviewer Agent: Separate Builder from Marker
- The Workbench on a Real Repo

**Phase 11 — LLM Engineering (nền)**
- Structured outputs · Function calling · Eval & testing · Caching/cost · Guardrails

**Phase 13 — (mở đầu)**
- Tool interface & schema design · OpenTelemetry GenAI (đọc lướt, build kỹ ở Sprint 2)

## Build (70%) — mở rộng agent-workbench

Starter đã có: agent loop · tool registry · file read/write · shell tool ·
permission gate · trace log · cost/token log · eval runner. Việc của sprint này
là **hiểu từng dòng** rồi thêm:

- [ ] Đọc & giải thích được toàn bộ `agent.py` (vì sao replay assistant turn verbatim với thinking blocks).
- [ ] Thêm 1 tool mới (vd: `list_dir` hoặc `grep`) qua `ToolRegistry` — đánh dấu `parallel_safe`.
- [ ] Thêm 5–10 eval fixtures mới vào `agent_workbench/evals/fixtures/` (golden path + 1 fixture cho mỗi bug bạn gặp).
- [ ] Thêm `final_matches_regex` check vào eval runner.
- [ ] Chạy `make eval` với ANTHROPIC_API_KEY thật, xem cost/latency trong trace JSONL.
- [ ] Thử nghiệm: so sánh `AGENT_MODEL=claude-sonnet-4-6` vs `opus-4-8` về cost & chất lượng trên cùng eval set.

## Deliverable cuối sprint

- agent-workbench public trên GitHub, README tiếng Anh hoàn chỉnh.
- Demo GIF (asciinema/terminal recording).
- Bài viết tiếng Anh: **"Building a minimal coding agent harness with verification gates"**
  — giải thích loop, permission gate, eval methodology.

## Tick skill checklist sau sprint

agent loop · tool registry · structured output · permission model · fixture-based
eval · token/cost/latency metrics → [`../skill-checklist.md`](../skill-checklist.md).
