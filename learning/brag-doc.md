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

<!-- Thêm entry mới phía trên (newest first). -->
