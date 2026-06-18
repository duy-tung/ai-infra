"""Fixture-based eval for the static checks — fully offline (no API key).

Each fixture is a PR (a diff, optional migration SQL) plus the categories the
guard *should* flag. We run the deterministic checks and compare flagged vs
expected, exact-match per fixture, and report precision/recall per category.

This is the eval-driven-development backbone: add a fixture for every risk you
care about, and every real miss becomes a permanent regression test.

    python -m evals.runner
    python -m evals.runner --fixtures path/to/fixtures
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path

from fintech_guard.findings import Severity
from fintech_guard.pipeline import Guard

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@dataclass
class Tally:
    tp: int = 0
    fp: int = 0
    fn: int = 0

    def precision(self) -> float:
        return self.tp / (self.tp + self.fp) if (self.tp + self.fp) else 1.0

    def recall(self) -> float:
        return self.tp / (self.tp + self.fn) if (self.tp + self.fn) else 1.0


def load_fixtures(path: Path) -> list[dict]:
    """A fixture file is either one fixture (dict) or a list of fixtures."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else [data]


def grade_fixture(fx: dict, guard: Guard) -> tuple[bool, set[str], set[str]]:
    report = guard.review_diff(fx["diff"], migration_sql=fx.get("migration_sql"))
    flagged = {f.category for f in report.findings}
    expected = set(fx.get("expected_categories", []))
    return flagged == expected, flagged, expected


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run fintech-guard static-check evals.")
    parser.add_argument("--fixtures", default=str(FIXTURES_DIR))
    args = parser.parse_args(argv)

    # Static-only (no reviewer) so the eval is deterministic and offline.
    guard = Guard(reviewer=None, threshold=Severity.HIGH, advisory=True)
    files = sorted(Path(args.fixtures).glob("*.json"))
    fixtures = [(fp, fx) for fp in files for fx in load_fixtures(fp)]
    if not fixtures:
        print(f"no fixtures in {args.fixtures}")
        return 1

    by_category: dict[str, Tally] = {}
    passed = 0
    for fp, fx in fixtures:
        ok, flagged, expected = grade_fixture(fx, guard)
        passed += ok
        mark = "PASS" if ok else "FAIL"
        if not ok:
            print(f"[{mark}] {fp.stem}:{fx.get('id', '?')}")
            print(f"    expected: {sorted(expected) or '∅'}")
            print(f"    flagged : {sorted(flagged) or '∅'}")
        for cat in expected | flagged:
            t = by_category.setdefault(cat, Tally())
            if cat in expected and cat in flagged:
                t.tp += 1
            elif cat in flagged:
                t.fp += 1
            else:
                t.fn += 1

    print(f"\n{passed}/{len(fixtures)} fixtures passed")
    print("\nper-category precision / recall:")
    for cat in sorted(by_category):
        t = by_category[cat]
        print(f"  {cat:24s} P={t.precision():.2f} R={t.recall():.2f}  (tp={t.tp} fp={t.fp} fn={t.fn})")
    return 0 if passed == len(fixtures) else 1


if __name__ == "__main__":
    raise SystemExit(main())
