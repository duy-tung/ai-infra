"""Thin wrapper around the Anthropic Messages API.

Why a wrapper: the agent loop shouldn't care how thinking, effort, and tool
schemas are wired — it just wants "send these messages, get a response." The
`anthropic` package is imported lazily so the rest of the harness (registry,
permissions, tracing, tests) works without the SDK or an API key installed.
"""

from __future__ import annotations

from typing import Any

from .config import Settings


class LLMClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client = None  # created on first use

    def _ensure_client(self) -> Any:
        if self._client is None:
            try:
                import anthropic
            except ImportError as exc:  # pragma: no cover - depends on env
                raise RuntimeError(
                    "the 'anthropic' package is required to run the agent. "
                    "Install it with: pip install anthropic"
                ) from exc
            # Resolves ANTHROPIC_API_KEY (or an `ant auth login` profile) from env.
            self._client = anthropic.Anthropic()
        return self._client

    def create(
        self,
        system: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> Any:
        client = self._ensure_client()
        params: dict[str, Any] = {
            "model": self.settings.model,
            "max_tokens": self.settings.max_tokens,
            "messages": messages,
            "tools": tools,
            "output_config": {"effort": self.settings.effort},
        }
        if self.settings.cache:
            # Cache the stable prefix (tools render before system; a breakpoint on
            # the last system block caches tools+system together). Stable across
            # turns in a run, so turns 2+ get cache reads.
            params["system"] = [
                {"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}
            ]
        else:
            params["system"] = system
        if self.settings.thinking:
            # Adaptive thinking: the model decides how much to reason. "summarized"
            # gives a readable summary so the trace shows the agent's reasoning.
            params["thinking"] = {"type": "adaptive", "display": "summarized"}
        return client.messages.create(**params)
