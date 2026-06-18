# Progress tracker

Cập nhật mỗi **Chủ nhật** (1h review). Mục tiêu: nhìn 1 phát biết đang ở đâu.

## Mốc lớn (milestones)

| Mốc | Deliverable | Trạng thái | Ngày xong |
|-----|-------------|-----------|-----------|
| 0–30 ngày | agent-workbench (loop, registry, gate, trace, eval) | 🟡 Starter sẵn | — |
| 30–90 ngày | fintech-backend-guard-agent v1 | 🟡 Starter chạy được (14 checks, 45 test, 33 eval P/R=1.00, LLM reviewer, CLI, PR comment bot) | — |
| 3–6 tháng | + eval/sandbox/OTel/dashboard/PR bot | ⬜ | — |
| 6–9 tháng | ai-incident-triage-agent | 🟡 Starter chạy được (correlator + eval + LLM hypotheses + CLI, read-only) | — |
| 9–12 tháng | Agent Control Plane narrative | ⬜ | — |

Trạng thái: ⬜ chưa · 🟡 đang làm · ✅ xong.

## Sprint hiện tại

- **Sprint:** 1 — Agent foundations
- **Tuần:** 1 / 4
- **Mục tiêu sprint:** hiểu agent loop + tool calling + tracing + eval; mở rộng `agent-workbench`.

## Nhật ký tuần (week log)

> Thêm 1 dòng mỗi tuần. Giữ ngắn — đây là tracker, không phải nhật ký dài.

| Tuần | Học (đọc) | Build (commit/PR) | Viết (public) | Giờ |
|------|-----------|-------------------|---------------|-----|
| W1 (___) | | | | |
| W2 (___) | | | | |
| W3 (___) | | | | |
| W4 (___) | | | | |

## Artifacts đã tạo

| Ngày | Artifact | Repo/path | Link public |
|------|----------|-----------|-------------|
| | agent-workbench starter (loop, registry, gate, trace, eval) | `projects/agent-workbench/` | |
| | Sprint 2 scaffold: MCP server + client bridge | `agent_workbench/mcp_server.py`, `mcp_bridge.py` | |
| | Sprint 2 scaffold: OpenTelemetry GenAI tracing + Jaeger stack | `agent_workbench/tracing_otel.py`, `observability/` | |
| | Sprint 2 scaffold: LLM routing layer | `agent_workbench/routing.py` | |
| | Sprint 3 scaffold: cost governor + kill switch | `agent_workbench/governor.py` | |
| | Sprint 3 scaffold: PII/secrets redaction | `agent_workbench/redaction.py` | |
| | Sprint 3 scaffold: policy-as-code gate | `agent_workbench/policy.py`, `policy.example.yaml` | |
| | Sprint 3 scaffold: hash-chained audit log | `agent_workbench/audit.py` | |
| | Sprint 3 scaffold: Prometheus metrics | `agent_workbench/metrics.py` | |
| | Sprint 3 scaffold: sandbox runner (local/docker) | `agent_workbench/sandbox.py` | |
| | Sprint 4: fintech-backend-guard-agent (static checks + eval + LLM reviewer + CLI) | `projects/fintech-backend-guard-agent/` | |
| | Project #3: ai-incident-triage-agent (correlator + eval + LLM hypotheses + CLI, read-only) | `projects/ai-incident-triage-agent/` | |

> Trạng thái: cả 3 repo chạy được + test xanh. agent-workbench (60), fintech-guard
> (48: 14 checks, 33 eval P/R=1.00, PR bot, OTel), incident-triage (26: correlator,
> 3 eval top-1=100%, OTel). Cả 3 đều có OpenTelemetry GenAI spans + cost.
> Việc của bạn: **đọc hiểu + chạy thật (`--llm` với key) + viết README/blog tiếng
> Anh** (điền "What I learned / Failure modes / Eval methodology" cho portfolio).

## Blockers / câu hỏi mở

- (ghi các thứ đang kẹt để hỏi mentor / tự research)
