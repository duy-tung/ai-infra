"""Fixture-based eval for the deterministic correlator — fully offline.

Each fixture is an incident bundle plus the deploy that actually caused it
(`expected_suspect_deploy_id`, or null when no deploy is to blame). We grade
top-1 and top-3 suspect-deploy accuracy — the core "did the agent point at the
right change?" metric — with no API key.

    python -m evals.runner
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from incident_triage.correlate import correlate
from incident_triage.models import IncidentBundle

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def grade(path: Path, window_minutes: int = 60) -> tuple[bool, bool, str | None, str | None]:
    fx = json.loads(path.read_text(encoding="utf-8"))
    bundle = IncidentBundle.from_dict(fx)
    correlation = correlate(bundle, window_minutes=window_minutes)
    expected = fx.get("expected_suspect_deploy_id")  # may be None
    suspects = correlation.suspect_deploys
    top_id = suspects[0].deploy.id if suspects else None
    top3 = [s.deploy.id for s in suspects[:3]]
    if expected is None:
        top1 = top_id is None
        top3_ok = top_id is None
    else:
        top1 = top_id == expected
        top3_ok = expected in top3
    return top1, top3_ok, expected, top_id


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run incident-triage correlation evals.")
    parser.add_argument("--fixtures", default=str(FIXTURES_DIR))
    args = parser.parse_args(argv)

    fixtures = sorted(Path(args.fixtures).glob("*.json"))
    if not fixtures:
        print(f"no fixtures in {args.fixtures}")
        return 1

    top1_hits = top3_hits = 0
    for fp in fixtures:
        top1, top3_ok, expected, got = grade(fp)
        top1_hits += top1
        top3_hits += top3_ok
        mark = "PASS" if top1 else "FAIL"
        print(f"[{mark}] {fp.stem}: expected={expected} top1={got} (top3_ok={top3_ok})")

    n = len(fixtures)
    print(f"\ntop-1 accuracy: {top1_hits}/{n} = {top1_hits / n:.0%}")
    print(f"top-3 accuracy: {top3_hits}/{n} = {top3_hits / n:.0%}")
    return 0 if top1_hits == n else 1


if __name__ == "__main__":
    raise SystemExit(main())
