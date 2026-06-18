.PHONY: install test eval review review-llm clean

install:
	python -m pip install -e ".[dev]"

# Unit tests + the offline eval are fully deterministic (no API key needed).
test:
	python -m pytest -q

# Run the static-check eval over the fixture PRs (offline).
eval:
	python -m evals.runner

# Review a sample fixture diff (static only). Override with: make review DIFF=path
DIFF ?= evals/fixtures/missing_idempotency.json
review:
	python -c "import json,sys; print(json.load(open('$(DIFF)'))['diff'])" | python -m fintech_guard.cli

# Review the working tree against a git ref with the LLM reviewer (needs ANTHROPIC_API_KEY).
REF ?= main
review-llm:
	git diff $(REF) | python -m fintech_guard.cli --llm

clean:
	rm -rf .pytest_cache **/__pycache__ *.egg-info
