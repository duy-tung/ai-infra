"""LLM routing layer.

A router picks which model to use for a given task. The cheapest way to cut LLM
cost without hurting quality is to *not* send every request to the most
expensive model: classification and extraction run fine on Haiku; heavy coding
and agentic work want Opus. This is a deliberately simple, **deterministic**
rule-based router so it's cheap to reason about and easy to test — swap in an
embedding/classifier-based router later if you outgrow keywords.

    router = ModelRouter()
    decision = router.route("refactor the payment service")
    # -> RoutingDecision(model="claude-opus-4-8", reason="...")
"""

from __future__ import annotations

from dataclasses import dataclass

from .config import PRICING

# Tasks that want the strongest model: code, agentic, multi-step reasoning.
# Note: on a keyword collision (e.g. "classify this PR review") the heavy match
# wins — intentional, since in an agent-platform context "review"/"migrate" are
# code actions, not the noun. This is a deliberately simple heuristic; for finer
# routing, replace `route()` with an embedding/classifier-based decision.
HEAVY_KEYWORDS = (
    "refactor", "migrate", "migration", "debug", "fix", "implement", "build",
    "design", "architect", "optimize", "root cause", "review", "diagnose",
    "rewrite", "port ", "trace through",
)
# Short, well-scoped tasks the cheapest model handles well.
CHEAP_KEYWORDS = (
    "classify", "label", "categorize", "tag", "summarize", "extract",
    "translate", "sentiment", "yes or no", "is this", "detect language",
)
CHEAP_MAX_LEN = 160  # only route short prompts to the cheap model


@dataclass
class RoutingDecision:
    model: str
    reason: str


class ModelRouter:
    def __init__(
        self,
        heavy: str = "claude-opus-4-8",
        balanced: str = "claude-sonnet-4-6",
        cheap: str = "claude-haiku-4-5",
    ) -> None:
        self.heavy = heavy
        self.balanced = balanced
        self.cheap = cheap

    def route(self, task: str) -> RoutingDecision:
        t = task.lower()
        if any(k in t for k in HEAVY_KEYWORDS):
            return RoutingDecision(self.heavy, "code/agentic task -> heavy model")
        if len(task) <= CHEAP_MAX_LEN and any(k in t for k in CHEAP_KEYWORDS):
            return RoutingDecision(self.cheap, "short classification/extraction -> cheap model")
        return RoutingDecision(self.balanced, "general task -> balanced model")

    @staticmethod
    def blended_price(model: str) -> float:
        """A rough 'how expensive is this model' number (input+output per 1M),
        handy for logging the cost lever the router is pulling."""
        p = PRICING.get(model, {"input": 0.0, "output": 0.0})
        return p["input"] + p["output"]
