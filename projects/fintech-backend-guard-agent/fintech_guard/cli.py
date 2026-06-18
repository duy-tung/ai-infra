"""Command-line entry point.

    # review a diff file (static checks only, no API key)
    python -m fintech_guard.cli --diff pr.diff

    # review the working tree against a git ref, with the LLM reviewer
    git diff main | python -m fintech_guard.cli --llm

    # enforce a gate (exit 1 if any finding >= threshold)
    python -m fintech_guard.cli --diff pr.diff --enforce --threshold high
"""

from __future__ import annotations

import argparse
import subprocess
import sys

from .findings import Severity
from .pipeline import Guard


def _read_diff(args: argparse.Namespace) -> str:
    if args.diff:
        with open(args.diff, encoding="utf-8") as fh:
            return fh.read()
    if args.git:
        return subprocess.run(
            ["git", "diff", args.git], capture_output=True, text=True, check=True
        ).stdout
    return sys.stdin.read()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Review a backend diff for fintech risk.")
    src = p.add_argument_group("diff source (default: stdin)")
    src.add_argument("--diff", metavar="FILE", help="Read the unified diff from FILE.")
    src.add_argument("--git", metavar="REF", help="Run `git diff REF` and review that.")
    p.add_argument("--migration", metavar="FILE", help="Also review this migration .sql file.")
    p.add_argument("--llm", action="store_true", help="Run the LLM reviewer (needs ANTHROPIC_API_KEY).")
    p.add_argument("--threshold", choices=[s.value for s in Severity], default="high",
                   help="Severity at/above which findings would block (default: high).")
    p.add_argument("--enforce", action="store_true", help="Enforce the gate (exit 1 if blocked). Default is advisory.")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of markdown.")
    p.add_argument("--comment", action="store_true",
                   help="Emit a sticky PR-comment body (markdown + marker) for the CI bot.")
    p.add_argument("--otel", action="store_true",
                   help="Emit OpenTelemetry spans (needs the [otel] extra + an OTLP endpoint).")
    p.add_argument("--metrics-file", metavar="PATH",
                   help="Write Prometheus metrics to PATH (textfile-collector pattern).")
    p.add_argument("--metrics-push", metavar="URL",
                   help="Push Prometheus metrics to a Pushgateway URL.")
    args = p.parse_args(argv)

    diff_text = _read_diff(args)
    migration_sql = None
    if args.migration:
        with open(args.migration, encoding="utf-8") as fh:
            migration_sql = fh.read()

    reviewer = None
    if args.llm:
        from .reviewer import LLMReviewer

        reviewer = LLMReviewer()

    otel = None
    if args.otel:
        try:
            from .tracing import OtelTracer

            otel = OtelTracer()
        except Exception as exc:  # noqa: BLE001 - otel is optional
            print(f"[otel] disabled: {exc}")

    metrics = None
    if args.metrics_file or args.metrics_push:
        try:
            from .metrics import Metrics

            metrics = Metrics()
        except Exception as exc:  # noqa: BLE001 - metrics are optional
            print(f"[metrics] disabled: {exc}")

    guard = Guard(reviewer=reviewer, threshold=Severity(args.threshold),
                  advisory=not args.enforce, otel=otel, metrics=metrics)
    report = guard.review_diff(diff_text, migration_sql=migration_sql)

    if metrics and args.metrics_file:
        metrics.write_textfile(args.metrics_file)
        print(f"[metrics] wrote {args.metrics_file}")
    if metrics and args.metrics_push:
        try:
            metrics.push(args.metrics_push)
            print(f"[metrics] pushed to {args.metrics_push}")
        except Exception as exc:  # noqa: BLE001
            print(f"[metrics] push failed: {exc}")

    if args.comment:
        from .pr_comment import to_comment

        print(to_comment(report))
    elif args.json:
        print(report.json())
    else:
        print(report.markdown())
    return 1 if report.gate_result.blocked else 0


if __name__ == "__main__":
    sys.exit(main())
