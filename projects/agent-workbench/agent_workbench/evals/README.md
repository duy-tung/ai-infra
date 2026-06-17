# Evals

Fixture-based evaluation for the agent. Each fixture is one task plus checks on
the outcome. The runner executes the agent in a throwaway temp directory
(permissions `auto`) and grades deterministically.

## Run

```bash
# from projects/agent-workbench, with ANTHROPIC_API_KEY set
python -m agent_workbench.evals.runner
python -m agent_workbench.evals.runner --fixtures path/to/other/fixtures
```

Exit code is 0 only if every fixture passes — wire it into CI.

## Fixture schema

```json
{
  "id": "unique_name",
  "prompt": "what to ask the agent",
  "setup": { "files": { "relative/path.txt": "seed content" } },
  "checks": [
    { "type": "file_exists",    "path": "out.py" },
    { "type": "file_contains",  "path": "out.py", "substring": "print" },
    { "type": "final_contains", "substring": "done" }
  ]
}
```

- `setup.files` (optional): files written into the sandbox before the run.
- `checks`: all must pass for the fixture to pass.
  - `file_exists` — a file was created at `path`.
  - `file_contains` — `path` exists and contains `substring`.
  - `final_contains` — the agent's final answer contains `substring` (case-insensitive).

## Why deterministic checks (not LLM-as-judge)

A regression suite has to be reproducible and cheap to trust. Deterministic
checks give a hard pass/fail you can run in CI without a second model in the
loop. Add LLM-as-judge later, as a *separate* graded dimension, once you have a
reason to — and keep it isolated so a judge change can't silently move your
baseline.

## Add your own

Drop a new `*.json` file in `fixtures/`. Start with the behaviors you care most
about (the agent's "golden path"), then add a fixture each time you find a bug —
that bug becomes a permanent regression test.
