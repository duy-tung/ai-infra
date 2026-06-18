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

    triage = Triage(generator=generator, window_minutes=args.window, otel=otel)
    report = triage.triage(bundle)

    print(report.json() if args.json else report.markdown())
    return 0  # read-only: triage never fails a gate


if __name__ == "__main__":
    sys.exit(main())
