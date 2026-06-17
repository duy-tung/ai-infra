"""Central configuration for the agent workbench.

Everything that you might want to tune without editing code lives here or is
read from environment variables. Keep it boring and explicit — this file is the
single source of truth for which model runs, what it costs, and where traces go.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

# --- Models & pricing -------------------------------------------------------
# Pricing is USD per 1,000,000 tokens. Source: Anthropic pricing (cached
# 2026-06). Update when prices change — the trace cost numbers depend on it.
#
# We default to Opus 4.8 because it is the most capable model. For tight agent
# loops where cost matters more than peak intelligence, set AGENT_MODEL to
# claude-sonnet-4-6 (5x cheaper output) or claude-haiku-4-5 (cheapest).
PRICING: dict[str, dict[str, float]] = {
    "claude-opus-4-8": {"input": 5.00, "output": 25.00},
    "claude-opus-4-7": {"input": 5.00, "output": 25.00},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    "claude-haiku-4-5": {"input": 1.00, "output": 5.00},
}

# Cache reads are ~0.1x input price; cache writes ~1.25x. We price them so the
# cost log stays honest once you start using prompt caching.
CACHE_READ_MULTIPLIER = 0.1
CACHE_WRITE_MULTIPLIER = 1.25

DEFAULT_MODEL = "claude-opus-4-8"


def _env_flag(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class Settings:
    """Runtime settings resolved from the environment with sane defaults."""

    model: str = field(default_factory=lambda: os.environ.get("AGENT_MODEL", DEFAULT_MODEL))
    max_tokens: int = field(default_factory=lambda: int(os.environ.get("AGENT_MAX_TOKENS", "16000")))
    # Effort is a cost/quality knob you control (not a model downgrade).
    # high is the API default; use xhigh for heavy coding, low for cheap loops.
    effort: str = field(default_factory=lambda: os.environ.get("AGENT_EFFORT", "high"))
    # Adaptive thinking lets the model decide how much to reason. "summarized"
    # shows a readable summary so you can watch the agent think.
    thinking: bool = field(default_factory=lambda: _env_flag("AGENT_THINKING", True))
    # Hard stop on the agent loop so a misbehaving run can't spin forever.
    max_turns: int = field(default_factory=lambda: int(os.environ.get("AGENT_MAX_TURNS", "20")))
    # Where to write JSONL traces (one file per run).
    trace_dir: Path = field(
        default_factory=lambda: Path(os.environ.get("AGENT_TRACE_DIR", "traces")).expanduser()
    )

    def price(self, model: str | None = None) -> dict[str, float]:
        model = model or self.model
        if model not in PRICING:
            # Unknown model: cost will show as 0 rather than crash. Add it to
            # PRICING to get accurate numbers.
            return {"input": 0.0, "output": 0.0}
        return PRICING[model]
