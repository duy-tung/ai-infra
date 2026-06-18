"""Cost governor + kill switch.

An autonomous agent that loops can also loop *expensively*. The governor is the
hard ceiling: a per-run budget on dollars, tokens, and tool calls. The agent
checks it after every LLM call and every tool result; once any limit is
exceeded, the run stops with status ``budget_exceeded`` instead of grinding on.

This is distinct from `max_turns` (a loop counter) — the governor bounds
*spend*, which is what actually hurts. Set generous limits for open-ended tasks,
tight ones for untrusted or latency-sensitive runs.
"""

from __future__ import annotations

from dataclasses import dataclass

from .tracing import RunTotals


@dataclass
class Budget:
    max_usd: float | None = None
    max_total_tokens: int | None = None
    max_tool_calls: int | None = None


@dataclass
class BudgetStatus:
    exceeded: bool
    reason: str = ""


class Governor:
    """Checks running totals against a budget. Stateless beyond the budget —
    pass it the current RunTotals and it tells you whether to stop."""

    def __init__(self, budget: Budget) -> None:
        self.budget = budget

    def check(self, totals: RunTotals) -> BudgetStatus:
        b = self.budget
        if b.max_usd is not None and totals.cost_usd > b.max_usd:
            return BudgetStatus(True, f"cost ${totals.cost_usd:.4f} exceeded budget ${b.max_usd:.4f}")
        total_tokens = totals.input_tokens + totals.output_tokens
        if b.max_total_tokens is not None and total_tokens > b.max_total_tokens:
            return BudgetStatus(True, f"tokens {total_tokens} exceeded budget {b.max_total_tokens}")
        if b.max_tool_calls is not None and totals.tool_calls > b.max_tool_calls:
            return BudgetStatus(True, f"tool calls {totals.tool_calls} exceeded budget {b.max_tool_calls}")
        return BudgetStatus(False)
