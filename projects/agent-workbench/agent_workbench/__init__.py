"""agent_workbench: a minimal coding-agent harness with verification gates.

A teaching/portfolio implementation of the core pieces every agent platform
needs: an agent loop, a tool registry, a permission gate, trace + cost logging,
and an eval runner. Read the modules in this order to learn the moving parts:

    config -> tools/base -> tools/registry -> permissions -> tracing
    -> llm -> agent -> evals/runner
"""

from .agent import Agent, AgentResult
from .config import Settings
from .permissions import Decision, PermissionGate, PermissionRequest
from .tools import ToolRegistry, default_registry
from .tracing import Tracer, Usage

__all__ = [
    "Agent",
    "AgentResult",
    "Settings",
    "PermissionGate",
    "PermissionRequest",
    "Decision",
    "ToolRegistry",
    "default_registry",
    "Tracer",
    "Usage",
]
