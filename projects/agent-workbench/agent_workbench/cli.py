"""Command-line entry point.

    python -m agent_workbench.cli "create hello.py that prints hi, then run it"

Default permission mode is ``ask`` — every file write or shell command needs
your approval. Sprint 2/3 flags add routing, tracing, budgets, redaction, audit,
metrics, policy-as-code, and sandboxed execution.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .agent import Agent
from .config import Settings
from .permissions import PermissionGate
from .tools import default_registry


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run the coding agent on a task.")
    p.add_argument("task", help="What you want the agent to do.")
    p.add_argument("--workdir", default=".", help="Directory the agent is jailed to (default: cwd).")
    p.add_argument(
        "--permission-mode", choices=["ask", "auto", "readonly"], default="ask",
        help="ask: confirm each mutating action; auto: allow all (sandbox only); readonly: deny mutating.",
    )
    p.add_argument("--allow", action="append", default=[], metavar="TOOL",
                   help="Pre-approve a tool by name (repeatable).")
    p.add_argument("--policy", metavar="YAML",
                   help="Load a policy-as-code gate from a YAML file (overrides --permission-mode).")
    p.add_argument("--quiet", action="store_true", help="Suppress streaming output.")
    # Sprint 2
    p.add_argument("--route", action="store_true", help="Let the ModelRouter pick the model from the task.")
    p.add_argument("--otel", action="store_true", help="Emit OpenTelemetry spans (needs the [otel] extra).")
    # Sprint 3
    p.add_argument("--max-usd", type=float, metavar="USD", help="Cost budget; kill the run if exceeded.")
    p.add_argument("--max-tool-calls", type=int, metavar="N", help="Tool-call budget; kill the run if exceeded.")
    p.add_argument("--redact", action="store_true", help="Scrub PII/secrets from the trace and audit log.")
    p.add_argument("--audit", metavar="PATH", help="Write a hash-chained audit log to PATH.")
    p.add_argument("--metrics-file", metavar="PATH", help="Write Prometheus metrics to PATH at the end.")
    p.add_argument("--metrics-push", metavar="URL", help="Push Prometheus metrics to a Pushgateway URL.")
    p.add_argument("--sandbox", choices=["local", "docker"], default="local",
                   help="Where run_shell executes (docker = ephemeral container, network off).")
    p.add_argument("--docker-image", default="python:3.11-slim", help="Image for --sandbox docker.")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_arg_parser().parse_args(argv)

    workdir = Path(args.workdir).expanduser().resolve()
    workdir.mkdir(parents=True, exist_ok=True)

    settings = Settings()

    if args.route:
        from .routing import ModelRouter

        decision = ModelRouter().route(args.task)
        settings.model = decision.model
        print(f"[router] {decision.model} — {decision.reason}")

    # --- permission gate: policy-as-code or simple mode ---
    if args.policy:
        from .policy import Policy, PolicyGate

        gate = PolicyGate(Policy.from_yaml(args.policy))
        print(f"[policy] loaded {args.policy}")
    else:
        gate = PermissionGate(mode=args.permission_mode, allowlist=set(args.allow))

    # --- sandbox runner for run_shell ---
    shell_runner = None
    if args.sandbox == "docker":
        from .sandbox import DockerSandbox

        shell_runner = DockerSandbox(image=args.docker_image)
        print(f"[sandbox] docker image={args.docker_image} (network off)")

    # --- optional hardening / observability ---
    otel = None
    if args.otel:
        try:
            from .tracing_otel import OtelTracer

            otel = OtelTracer(settings)
        except Exception as exc:  # noqa: BLE001 - otel is optional
            print(f"[otel] disabled: {exc}")

    governor = None
    if args.max_usd is not None or args.max_tool_calls is not None:
        from .governor import Budget, Governor

        governor = Governor(Budget(max_usd=args.max_usd, max_tool_calls=args.max_tool_calls))

    redactor = None
    if args.redact:
        from .redaction import Redactor

        redactor = Redactor()

    audit = None
    if args.audit:
        from .audit import AuditLog

        audit = AuditLog(Path(args.audit))

    metrics = None
    if args.metrics_file or args.metrics_push:
        from .metrics import Metrics

        metrics = Metrics()

    registry = default_registry(workdir, shell_runner=shell_runner)
    agent = Agent(
        settings, registry, gate,
        verbose=not args.quiet,
        otel=otel, governor=governor, audit=audit, metrics=metrics, redactor=redactor,
    )

    result = agent.run(args.task)

    if metrics and args.metrics_file:
        metrics.write_textfile(args.metrics_file)
        print(f"[metrics] wrote {args.metrics_file}")
    if metrics and args.metrics_push:
        try:
            metrics.push(args.metrics_push)
            print(f"[metrics] pushed to {args.metrics_push}")
        except Exception as exc:  # noqa: BLE001
            print(f"[metrics] push failed: {exc}")
    if audit:
        from .audit import verify

        ok, msg = verify(args.audit)
        print(f"[audit] {args.audit} — {msg}")

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
