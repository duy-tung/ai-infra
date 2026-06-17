.PHONY: install test eval demo clean

install:
	python -m pip install -e ".[dev]"

# Unit tests run offline (no API key needed) — they use a scripted fake LLM.
test:
	python -m pytest -q

# Evals call the real API — needs ANTHROPIC_API_KEY.
eval:
	python -m agent_workbench.evals.runner

# Interactive demo in a sandbox dir, auto-approving tools (safe: throwaway dir).
demo:
	rm -rf .sandbox && mkdir -p .sandbox
	python -m agent_workbench.cli --workdir .sandbox --permission-mode auto \
		"create greet.py that prints hello, then run it and report the output"

clean:
	rm -rf .sandbox traces/*.jsonl .pytest_cache **/__pycache__
