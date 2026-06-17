# Sprint 2 — Tools & Protocols (Tuần 5–8)

**Mục tiêu:** chuẩn hoá tool surface qua **MCP**, và gắn **OpenTelemetry GenAI**
vào agent runs (nâng trace JSONL → spans thật).

## Lessons (đọc — 20%)

**Phase 13 — Tools & Protocols**
- Function Calling Deep Dive
- Tool Schema Design
- MCP Fundamentals
- Building an MCP Server
- MCP Security
- OpenTelemetry GenAI
- LLM Routing Layer
- Skills & Agent SDKs

## Build (70%)

- [ ] **MCP server** expose tool registry của workbench (read_file/write_file/run_shell)
      qua MCP. Client = workbench agent.
- [ ] **MCP security**: auth, allowed paths, rate limit — viết threat model ngắn.
- [ ] **OpenTelemetry GenAI**: thay (hoặc bổ sung) Tracer JSONL bằng OTel spans —
      span cho mỗi LLM call (token/cost attributes) và mỗi tool call.
- [ ] Export spans tới 1 collector local (Jaeger/Tempo) qua Docker Compose; xem trace.
- [ ] **LLM routing layer** nhỏ: chọn model theo task (haiku cho task nhẹ, opus cho nặng) — đo cost chênh lệch.

## Deliverable cuối sprint

- `agent-workbench` có **MCP server** + **OTel tracing** + Docker Compose để xem traces.
- Bài viết: **"Wrapping an agent's tools in an MCP server + tracing it with OpenTelemetry GenAI."**

## Tick skill checklist

MCP server/client · tool schema design · OTel traces · prompt/model/version
tracking · tool-call success rate · prompt injection defense (MCP security).
