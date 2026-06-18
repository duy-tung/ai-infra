"""Minimal unified-diff parser.

The static checks reason about the lines a PR *adds* (that's where new risk is
introduced), keyed by file and new-file line number. This parses `git diff`
output into that shape. It's intentionally small — enough for review heuristics,
not a full patch applier.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


@dataclass
class FileDiff:
    path: str
    # Added lines as (new_line_number, text_without_leading_plus).
    added: list[tuple[int, str]] = field(default_factory=list)

    @property
    def added_text(self) -> str:
        return "\n".join(t for _, t in self.added)

    def is_sql(self) -> bool:
        p = self.path.lower()
        return p.endswith(".sql") or "migration" in p or "migrate" in p


def parse_unified_diff(diff_text: str) -> list[FileDiff]:
    files: list[FileDiff] = []
    current: FileDiff | None = None
    new_lineno = 0

    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None  # path comes from the +++ line below
            continue
        if raw.startswith("+++ "):
            path = raw[4:].strip()
            if path.startswith("b/"):
                path = path[2:]
            if path == "/dev/null":
                current = None
                continue
            current = FileDiff(path=path)
            files.append(current)
            continue
        if raw.startswith("--- "):
            continue
        m = HUNK_RE.match(raw)
        if m:
            new_lineno = int(m.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            current.added.append((new_lineno, raw[1:]))
            new_lineno += 1
        elif raw.startswith("-"):
            # removed line — does not advance the new-file counter
            continue
        else:
            # context line
            new_lineno += 1

    return files
