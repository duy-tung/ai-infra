"""Tool contract.

A tool is anything the agent can call. Each tool declares a JSON schema (what
the model sees) and a `run` method (what your harness executes). Two metadata
flags drive the harness:

- `mutating`: the action changes state (write a file, run a command). The
  permission gate guards these; read-only tools run freely.
- `parallel_safe`: the harness could run several of these at once without them
  interfering. We don't parallelize in this starter, but the flag is here so
  the scheduling decision lives with the tool, not guessed from a command string.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class ToolResult:
    """Result of running a tool, ready to hand back to the model."""

    content: str
    is_error: bool = False


class Tool(ABC):
    """Base class for every tool in the registry."""

    name: str
    description: str
    mutating: bool = False
    parallel_safe: bool = True

    @property
    @abstractmethod
    def input_schema(self) -> dict[str, Any]:
        """JSON schema for the tool's input (the `input_schema` field the API expects)."""

    @abstractmethod
    def run(self, **kwargs: Any) -> ToolResult:
        """Execute the tool. Should never raise for expected failures — return a
        ToolResult with is_error=True and a helpful message instead, so the
        model can recover."""

    def to_api_schema(self) -> dict[str, Any]:
        """Render the tool definition in the shape the Messages API expects."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }
