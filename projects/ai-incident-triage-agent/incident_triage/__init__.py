"""incident_triage — a read-only incident-triage assistant for Go/Postgres services.

Given an incident bundle (alert + deploys + logs + optional metrics/diff/runbook),
it correlates the alert with recent changes and proposes ranked root-cause
hypotheses, a blast radius, an advisory rollback candidate, queries to run, the
owner to page, and a timeline. Deterministic correlation core + optional LLM
hypothesis layer. The agent only reasons — it never mutates anything.

Read order: models -> signatures -> correlate -> hypotheses -> report -> pipeline.
"""

from .hypotheses import Hypothesis, HypothesisGenerator
from .models import IncidentBundle
from .pipeline import Triage, TriageReport

__all__ = ["IncidentBundle", "Triage", "TriageReport", "Hypothesis", "HypothesisGenerator"]
