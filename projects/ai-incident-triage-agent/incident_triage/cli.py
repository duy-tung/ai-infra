"""Command-line entry point.

    # triage an incident bundle (deterministic correlation only, no API key)
    python -m incident_triage.cli --incident incident.json

    # add the LLM hypothesis generator (needs ANTHROPIC_API_KEY)
    python -m incident_triage.cli --incident incident.json --llm

    # JSON for a bot / dashboard
    python -m incident_triage.cli --incident incident.json --json
"""

from __future__ import annotations

import argparse
import json
import sys

from .models import IncidentBundle
from .pipeline import Triage


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Triage an incident bundle (read-only).")
    p.add_argument("--incident", metavar="FILE", help="Incident bundle JSON (default: stdin).")
    p.add_argument("--window", type=int, default=60, help="Correlation window in minutes (default: 60).")
    p.add_argument("--llm", action="store_true", help="Add the LLM hypothesis generator (needs ANTHROPIC_API_KEY).")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of markdown.")
    p.add_argument("--otel", action="store_true",
                   help="Emit OpenTelemetry spans (needs the [otel] extra + an OTLP endpoint).")
    p.add_argument("--metrics-file", metavar="PATH",
                   help="Write Prometheus metrics to PATH (textfile-collector pattern).")
    p.add_argument("--metrics-push", metavar="URL",
                   help="Push Prometheus metrics to a Pushgateway URL.")
    args = p.parse_args(argv)

    raw = open(args.incident, encoding="utf-8").read() if args.incident else sys.stdin.read()
    bundle = IncidentBundle.from_dict(json.loads(raw))

    generator = None
    if args.llm:
        from .hypotheses import HypothesisGenerator

        generator = HypothesisGenerator()

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

    triage = Triage(generator=generator, window_minutes=args.window, otel=otel, metrics=metrics)
    report = triage.triage(bundle)

    if metrics and args.metrics_file:
        metrics.write_textfile(args.metrics_file)
        print(f"[metrics] wrote {args.metrics_file}")
    if metrics and args.metrics_push:
        try:
            metrics.push(args.metrics_push)
            print(f"[metrics] pushed to {args.metrics_push}")
        except Exception as exc:  # noqa: BLE001
            print(f"[metrics] push failed: {exc}")

    print(report.json() if args.json else report.markdown())
    return 0  # read-only: triage never fails a gate


if __name__ == "__main__":
    sys.exit(main())
