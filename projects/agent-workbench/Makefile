.PHONY: install test eval demo mcp-server otel-up otel-down clean

install:
	python -m pip install -e ".[dev]"

# Unit + integration tests run offline (no API key) — scripted fake LLM, and a
# real in-process MCP client⇄server round-trip. MCP/OTel tests skip if not installed.
test:
	python -m pytest -q

# Evals call the real API — needs ANTHROPIC_API_KEY.
eval:
	python -m agent_workbench.evals.runner

# Interactive demo in a sandbox dir, auto-approving tools (safe: throwaway dir).
demo:
	rm -rf .sandbox && mkdir -p .sandbox
	python -m agent_workbench.cli --workdir .sandbox --permission-mode auto \
		"create greet.py that prints hello, then run it and report the output"

# Run the MCP server over stdio, jailed to ./.sandbox (for MCP Inspector/clients).
mcp-server:
	mkdir -p .sandbox
	AGENT_MCP_WORKDIR=.sandbox python -m agent_workbench.mcp_server

# Local OpenTelemetry → Jaeger stack (UI at http://localhost:16686).
otel-up:
	docker compose -f observability/docker-compose.yml up -d

otel-down:
	docker compose -f observability/docker-compose.yml down

# Hardened demo: policy-as-code gate + redaction + audit + cost budget (Sprint 3).
harden-demo:
	rm -rf .sandbox && mkdir -p .sandbox
	python -m agent_workbench.cli --policy policy.example.yaml --redact \
		--audit audit.jsonl --max-usd 0.50 --workdir .sandbox \
		"create greet.py that prints hello, then run it"

clean:
	rm -rf .sandbox traces/*.jsonl .pytest_cache **/__pycache__ *.prom audit*.jsonl
