.PHONY: install test eval triage triage-llm clean

install:
	python -m pip install -e ".[dev]"

# Unit tests + offline eval are deterministic (no API key needed).
test:
	python -m pytest -q

# Grade suspect-deploy correlation over fixture incidents (offline).
eval:
	python -m evals.runner

# Triage a sample incident (deterministic only). Override: make triage INCIDENT=path
INCIDENT ?= evals/fixtures/deploy_caused_errors.json
triage:
	python -m incident_triage.cli --incident $(INCIDENT)

# Add the LLM hypothesis layer (needs ANTHROPIC_API_KEY).
triage-llm:
	python -m incident_triage.cli --incident $(INCIDENT) --llm

clean:
	rm -rf .pytest_cache **/__pycache__ *.egg-info
