"""Command-line entry point.

    python -m agent_workbench.cli "create hello.py that prints hi, then run it"

Flags let you choose the working directory and permission mode. Default mode is
``ask`` so every file write or shell command needs your approval.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .agent import Agent
from .config import Settings
from .permissions import PermissionGate
from .tools import default_registry


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the coding agent on a task.")
    parser.add_argument("task", help="What you want the agent to do.")
    parser.add_argument(
        "--workdir",
        default=".",
        help="Working directory the agent is jailed to (default: current dir).",
    )
    parser.add_argument(
        "--permission-mode",
        choices=["ask", "auto", "readonly"],
        default="ask",
        help="ask: confirm each mutating action; auto: allow all (sandbox only); "
        "readonly: deny mutating actions.",
    )
    parser.add_argument(
        "--allow",
        action="append",
        default=[],
        metavar="TOOL",
        help="Pre-approve a tool by name (repeatable). e.g. --allow read_file",
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress streaming output.")
    parser.add_argument(
        "--route",
        action="store_true",
        help="Let the ModelRouter pick the model from the task (overrides AGENT_MODEL).",
    )
    parser.add_argument(
        "--otel",
        action="store_true",
        help="Emit OpenTelemetry spans (needs the [otel] extra + an OTLP endpoint).",
    )
    args = parser.parse_args(argv)

    workdir = Path(args.workdir).expanduser().resolve()
    workdir.mkdir(parents=True, exist_ok=True)

    settings = Settings()

    if args.route:
        from .routing import ModelRouter

        decision = ModelRouter().route(args.task)
        settings.model = decision.model
        print(f"[router] {decision.model} — {decision.reason}")

    otel = None
    if args.otel:
        try:
            from .tracing_otel import OtelTracer

            otel = OtelTracer(settings)
        except Exception as exc:  # noqa: BLE001 - otel is optional
            print(f"[otel] disabled: {exc}")

    registry = default_registry(workdir)
    gate = PermissionGate(mode=args.permission_mode, allowlist=set(args.allow))
    agent = Agent(settings, registry, gate, verbose=not args.quiet, otel=otel)

    result = agent.run(args.task)
    print(f"\n=== {result.status} ===")
    print(result.final_text)
    print(
        f"\ncost=${result.totals.cost_usd:.4f}  "
        f"llm_calls={result.totals.llm_calls}  "
        f"tool_calls={result.totals.tool_calls}  "
        f"trace={result.trace_path}"
    )
    return 0 if result.status == "completed" else 1


if __name__ == "__main__":
    sys.exit(main())
