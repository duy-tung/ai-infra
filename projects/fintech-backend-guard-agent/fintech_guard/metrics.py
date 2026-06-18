"""Prometheus metrics for guard runs.

One-shot CLI runs don't fit Prometheus's scrape model, so we ship metrics the
two batch-friendly ways:
- `write_textfile(path)` — node_exporter textfile-collector pattern.
- `push(gateway)` — Prometheus Pushgateway (the standard for batch jobs); the
  shared observability stack scrapes the gateway.

`prometheus_client` is optional: pip install -e ".[metrics]".
"""

from __future__ import annotations

from typing import Any

from .tracing import cost_of


class Metrics:
    def __init__(self, registry: Any | None = None) -> None:
        from prometheus_client import CollectorRegistry, Counter, Histogram

        self.registry = registry or CollectorRegistry()
        self.reviews = Counter(
            "fintech_guard_reviews_total", "Reviews by verdict", ["verdict"], registry=self.registry
        )
        self.findings = Counter(
            "fintech_guard_findings_total", "Findings by severity", ["severity"], registry=self.registry
        )
        self.llm_calls = Counter(
            "fintech_guard_llm_calls_total", "LLM reviewer calls", registry=self.registry
        )
        self.cost = Counter(
            "fintech_guard_cost_usd_total", "Cumulative USD cost", registry=self.registry
        )
        self.latency = Histogram(
            "fintech_guard_review_seconds", "Review latency", registry=self.registry
        )

    def record_review(self, verdict: str, counts: dict[str, int], duration_s: float) -> None:
        self.reviews.labels(verdict=verdict).inc()
        for sev, n in counts.items():
            if n:
                self.findings.labels(severity=sev).inc(n)
        self.latency.observe(duration_s)

    def record_llm(self, model: str, input_tokens: int, output_tokens: int) -> None:
        self.llm_calls.inc()
        self.cost.inc(cost_of(model, input_tokens, output_tokens))

    def render(self) -> bytes:
        from prometheus_client import generate_latest

        return generate_latest(self.registry)

    def write_textfile(self, path: str) -> None:
        from prometheus_client import write_to_textfile

        write_to_textfile(path, self.registry)

    def push(self, gateway: str, job: str = "fintech-guard") -> None:
        from prometheus_client import push_to_gateway

        push_to_gateway(gateway, job=job, registry=self.registry)
