"""Prometheus metrics for triage runs.

One-shot CLI runs are batch jobs: ship metrics via `write_textfile(path)`
(node_exporter textfile collector) or `push(gateway)` (Prometheus Pushgateway).
`prometheus_client` is optional: pip install -e ".[metrics]".
"""

from __future__ import annotations

from typing import Any

from .tracing import cost_of

CONFIDENCE_BUCKETS = (0.1, 0.3, 0.5, 0.7, 0.9, 1.0)


class Metrics:
    def __init__(self, registry: Any | None = None) -> None:
        from prometheus_client import CollectorRegistry, Counter, Histogram

        self.registry = registry or CollectorRegistry()
        self.runs = Counter(
            "incident_triage_runs_total", "Triage runs by outcome", ["outcome"], registry=self.registry
        )
        self.llm_calls = Counter(
            "incident_triage_llm_calls_total", "LLM hypothesis calls", registry=self.registry
        )
        self.cost = Counter(
            "incident_triage_cost_usd_total", "Cumulative USD cost", registry=self.registry
        )
        self.latency = Histogram(
            "incident_triage_seconds", "Triage latency", registry=self.registry
        )
        self.confidence = Histogram(
            "incident_triage_top_confidence", "Top-hypothesis confidence",
            buckets=CONFIDENCE_BUCKETS, registry=self.registry,
        )

    def record_triage(self, has_suspect: bool, top_confidence: float, duration_s: float) -> None:
        self.runs.labels(outcome="has_suspect" if has_suspect else "no_suspect").inc()
        self.latency.observe(duration_s)
        self.confidence.observe(top_confidence)

    def record_llm(self, model: str, input_tokens: int, output_tokens: int) -> None:
        self.llm_calls.inc()
        self.cost.inc(cost_of(model, input_tokens, output_tokens))

    def render(self) -> bytes:
        from prometheus_client import generate_latest

        return generate_latest(self.registry)

    def write_textfile(self, path: str) -> None:
        from prometheus_client import write_to_textfile

        write_to_textfile(path, self.registry)

    def push(self, gateway: str, job: str = "incident-triage") -> None:
        from prometheus_client import push_to_gateway

        push_to_gateway(gateway, job=job, registry=self.registry)
