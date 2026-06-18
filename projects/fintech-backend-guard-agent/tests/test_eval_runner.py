"""Sanity: the shipped fixtures all pass the static-check eval (exit code 0)."""

from evals.runner import main


def test_all_fixtures_pass():
    assert main([]) == 0
