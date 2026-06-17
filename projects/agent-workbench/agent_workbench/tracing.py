"""Tracing and cost accounting.

Every run writes a JSONL trace: one line per event (run start, each LLM call
with token usage and computed cost, each tool call with its permission decision
and result, run end with totals). This is the observability spine — the same
shape you will later push as OpenTelemetry GenAI spans. Keeping it as plain
JSONL first means you can build evals and dashboards before adding an OTel
collector.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .config import CACHE_READ_MULTIPLIER, CACHE_WRITE_MULTIPLIER, Settings


@dataclass
class Usage:
    """Token counts for one LLM call (mirrors response.usage)."""

    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_input_tokens: int = 0
    cache_creation_input_tokens: int = 0


@dataclass
class RunTotals:
    llm_calls: int = 0
    tool_calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    cost_usd: float = 0.0


def cost_of(usage: Usage, price: dict[str, float]) -> float:
    """Compute USD cost for one call from token usage and a per-1M price table."""
    per_in = price.get("input", 0.0) / 1_000_000
    per_out = price.get("output", 0.0) / 1_000_000
    return (
        usage.input_tokens * per_in
        + usage.output_tokens * per_out
        + usage.cache_read_input_tokens * per_in * CACHE_READ_MULTIPLIER
        + usage.cache_creation_input_tokens * per_in * CACHE_WRITE_MULTIPLIER
    )


@dataclass
class Tracer:
    settings: Settings
    run_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    totals: RunTotals = field(default_factory=RunTotals)
    _fh: Any = field(default=None, init=False, repr=False)
    _path: Path = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.settings.trace_dir.mkdir(parents=True, exist_ok=True)
        self._path = self.settings.trace_dir / f"run-{self.run_id}.jsonl"
        self._fh = self._path.open("w", encoding="utf-8")

    @property
    def path(self) -> Path:
        return self._path

    def _emit(self, event: str, **fields: Any) -> None:
        record = {"ts": round(time.time(), 3), "run_id": self.run_id, "event": event, **fields}
        self._fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        self._fh.flush()

    def run_start(self, task: str) -> None:
        self._emit(
            "run_start",
            task=task,
            model=self.settings.model,
            effort=self.settings.effort,
            thinking=self.settings.thinking,
        )

    def llm_call(self, usage: Usage, stop_reason: str | None, latency_s: float) -> float:
        price = self.settings.price()
        cost = cost_of(usage, price)
        self.totals.llm_calls += 1
        self.totals.input_tokens += usage.input_tokens
        self.totals.output_tokens += usage.output_tokens
        self.totals.cache_read_tokens += usage.cache_read_input_tokens
        self.totals.cache_write_tokens += usage.cache_creation_input_tokens
        self.totals.cost_usd += cost
        self._emit(
            "llm_call",
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            cache_read_input_tokens=usage.cache_read_input_tokens,
            cache_creation_input_tokens=usage.cache_creation_input_tokens,
            stop_reason=stop_reason,
            latency_s=round(latency_s, 3),
            cost_usd=round(cost, 6),
        )
        return cost

    def tool_call(
        self,
        name: str,
        tool_input: dict[str, Any],
        decision: str,
        reason: str,
        result_preview: str,
        is_error: bool,
        latency_s: float,
    ) -> None:
        self.totals.tool_calls += 1
        self._emit(
            "tool_call",
            name=name,
            input=tool_input,
            permission=decision,
            permission_reason=reason,
            is_error=is_error,
            latency_s=round(latency_s, 3),
            result_preview=result_preview[:500],
        )

    def run_end(self, status: str, final_text: str) -> None:
        self._emit(
            "run_end",
            status=status,
            final_text=final_text[:2000],
            totals={
                "llm_calls": self.totals.llm_calls,
                "tool_calls": self.totals.tool_calls,
                "input_tokens": self.totals.input_tokens,
                "output_tokens": self.totals.output_tokens,
                "cache_read_tokens": self.totals.cache_read_tokens,
                "cache_write_tokens": self.totals.cache_write_tokens,
                "cost_usd": round(self.totals.cost_usd, 6),
            },
        )
        if self._fh:
            self._fh.close()
            self._fh = None
