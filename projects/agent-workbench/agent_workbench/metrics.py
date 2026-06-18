"""Prometheus metrics for agent runs.

Counters and histograms for the things you actually alert on: run outcomes,
LLM/tool call rates, error rate, cost, and latency. Uses a private
`CollectorRegistry` so it composes cleanly (and tests can inspect it).

Two ways to ship the numbers:
- `start_server(port)` — for a long-running service form of the agent.
- `write_textfile(path)` — for one-shot CLI runs (node_exporter's textfile
  collector pattern): write `.prom` files a sidecar scrapes.

`prometheus_client` is optional: pip install -e ".[metrics]"
"""

from __future__ import annotations

from typing import Any


class Metrics:
    def __init__(self, registry: Any | None = None) -> None:
        from prometheus_client import CollectorRegistry, Counter, Histogram

        self.registry = registry or CollectorRegistry()
        self.runs = Counter(
            "agent_runs_total", "Agent runs by terminal status", ["status"], registry=self.registry
        )
        self.llm_calls = Counter(
            "agent_llm_calls_total", "LLM calls made", registry=self.registry
        )
        self.tool_calls = Counter(
            "agent_tool_calls_total", "Tool calls by tool and outcome",
            ["tool", "outcome"], registry=self.registry,
        )
        self.cost = Counter(
            "agent_cost_usd_total", "Cumulative USD cost", registry=self.registry
        )
        self.llm_latency = Histogram(
            "agent_llm_latency_seconds", "LLM call latency", registry=self.registry
        )
        self.tool_latency = Histogram(
            "agent_tool_latency_seconds", "Tool call latency", ["tool"], registry=self.registry
        )

    def record_llm(self, latency_s: float, cost_usd: float) -> None:
        self.llm_calls.inc()
        self.cost.inc(cost_usd)
        self.llm_latency.observe(latency_s)

    def record_tool(self, name: str, is_error: bool, latency_s: float) -> None:
        self.tool_calls.labels(tool=name, outcome="error" if is_error else "ok").inc()
        self.tool_latency.labels(tool=name).observe(latency_s)

    def record_run(self, status: str) -> None:
        self.runs.labels(status=status).inc()

    def render(self) -> bytes:
        from prometheus_client import generate_latest

        return generate_latest(self.registry)

    def write_textfile(self, path: str) -> None:
        from prometheus_client import write_to_textfile

        write_to_textfile(path, self.registry)

    def push(self, gateway: str, job: str = "agent-workbench") -> None:
        from prometheus_client import push_to_gateway

        push_to_gateway(gateway, job=job, registry=self.registry)

    def start_server(self, port: int = 9464) -> Any:
        from prometheus_client import start_http_server

        return start_http_server(port, registry=self.registry)
