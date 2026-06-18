"""Sanity: shipped fixtures all get top-1 correct (exit 0)."""

from evals.runner import main


def test_all_fixtures_top1():
    assert main([]) == 0
