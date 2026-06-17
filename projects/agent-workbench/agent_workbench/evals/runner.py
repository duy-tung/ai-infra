"""Fixture-based eval runner.

Eval-driven development is the difference between "the demo worked once" and "I
can change the prompt and know whether I broke anything." Each fixture is a task
plus checks on the outcome. We run the agent in a throwaway sandbox (permission
mode ``auto``), then grade with deterministic checks — no LLM-as-judge here, so
results are reproducible and free to verify.

    python -m agent_workbench.evals.runner
    python -m agent_workbench.evals.runner --fixtures path/to/fixtures

Fixture schema (JSON):
    {
      "id": "write_and_run",
      "prompt": "Create greet.py that prints 'hello' and run it.",
      "setup": {"files": {"notes.txt": "optional seed content"}},
      "checks": [
        {"type": "file_exists",   "path": "greet.py"},
        {"type": "file_contains", "path": "greet.py", "substring": "print"},
        {"type": "final_contains", "substring": "hello"}
      ]
    }
"""

from __future__ import annotations

import argparse
import json
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..agent import Agent, AgentResult
from ..config import Settings
from ..permissions import PermissionGate
from ..tools import default_registry

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@dataclass
class CheckResult:
    description: str
    passed: bool
    detail: str = ""


@dataclass
class FixtureResult:
    fixture_id: str
    checks: list[CheckResult]
    agent: AgentResult

    @property
    def passed(self) -> bool:
        return bool(self.checks) and all(c.passed for c in self.checks)


def _run_check(check: dict[str, Any], workdir: Path, result: AgentResult) -> CheckResult:
    ctype = check.get("type")
    if ctype == "file_exists":
        path = workdir / check["path"]
        return CheckResult(f"file_exists {check['path']}", path.is_file())
    if ctype == "file_contains":
        path = workdir / check["path"]
        if not path.is_file():
            return CheckResult(f"file_contains {check['path']}", False, "file missing")
        text = path.read_text(encoding="utf-8", errors="replace")
        ok = check["substring"] in text
        return CheckResult(f"file_contains {check['path']!r}~{check['substring']!r}", ok)
    if ctype == "final_contains":
        ok = check["substring"].lower() in result.final_text.lower()
        return CheckResult(f"final_contains {check['substring']!r}", ok)
    return CheckResult(f"unknown check {ctype}", False, "unknown check type")


def run_fixture(path: Path, settings: Settings) -> FixtureResult:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="eval-") as tmp:
        workdir = Path(tmp)
        for rel, content in fixture.get("setup", {}).get("files", {}).items():
            target = workdir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

        registry = default_registry(workdir)
        gate = PermissionGate(mode="auto")  # sandboxed temp dir — safe to auto-allow
        agent = Agent(settings, registry, gate, verbose=False)
        result = agent.run(fixture["prompt"])

        checks = [_run_check(c, workdir, result) for c in fixture.get("checks", [])]
    return FixtureResult(fixture["id"], checks, result)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run agent evals against fixtures.")
    parser.add_argument("--fixtures", default=str(FIXTURES_DIR), help="Fixtures directory.")
    args = parser.parse_args(argv)

    settings = Settings()
    fixtures = sorted(Path(args.fixtures).glob("*.json"))
    if not fixtures:
        print(f"no fixtures found in {args.fixtures}")
        return 1

    results: list[FixtureResult] = []
    total_cost = 0.0
    for fpath in fixtures:
        fr = run_fixture(fpath, settings)
        results.append(fr)
        total_cost += fr.agent.totals.cost_usd
        mark = "PASS" if fr.passed else "FAIL"
        print(f"[{mark}] {fr.fixture_id}  (cost=${fr.agent.totals.cost_usd:.4f}, "
              f"status={fr.agent.status})")
        for c in fr.checks:
            cmark = "  ok " if c.passed else "  X  "
            print(f"   {cmark}{c.description}{(' — ' + c.detail) if c.detail else ''}")

    passed = sum(1 for r in results if r.passed)
    print(f"\n{passed}/{len(results)} fixtures passed   total_cost=${total_cost:.4f}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
