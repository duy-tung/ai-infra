"""Format a guard report as a sticky PR comment.

The marker lets the CI step find and *update* its previous comment instead of
posting a new one on every push — one tidy, always-current review per PR. The
body is the same markdown the CLI prints, wrapped with the marker and a short
"automated / advisory" footer so reviewers know what it is.
"""

from __future__ import annotations

from .pipeline import GuardReport

MARKER = "<!-- fintech-guard -->"
FOOTER = (
    "\n---\n"
    "_🛡️ Automated review by **fintech-backend-guard-agent** — advisory only, "
    "does not block merge. Findings are heuristics; verify before acting._"
)


def to_comment(report: GuardReport) -> str:
    """Render the PR comment body: marker + report markdown + footer."""
    return f"{MARKER}\n{report.markdown()}{FOOTER}"


def is_guard_comment(body: str) -> bool:
    """True if `body` is one of our sticky comments (used by the CI updater)."""
    return MARKER in (body or "")
