# fintech-backend-guard-agent — an AI PR reviewer that understands money

> **Draft — personalize before publishing.**

A generic "AI code reviewer" is a commodity. A reviewer that flags
**idempotency, money precision, migration locks, ledger/audit gaps, and
secrets** is a moat — it pairs AI-infrastructure skill with fintech domain
knowledge. That's what this project is: given a PR diff (plus migrations and a
runbook), it reviews for *risk*, not style, and posts a single sticky PR comment
with severity-ranked findings and suggested fixes.

## Architecture: a workflow, not an agent loop

PR review is well-specified, so the pipeline is code-orchestrated:

```
diff → parse → static checks (deterministic) → scrub → LLM reviewer
     → merge/dedupe → severity gate → report (markdown / JSON / PR comment)
```

The deterministic static checks are the core: 14 risk categories implemented as
pattern matching over the lines a PR *adds* — high precision, no API key, and
they make the eval suite offline. The LLM reviewer (structured output) covers
the fuzzy risks the patterns can't: a transaction boundary split across two
writes, a reconciliation path that's silently missing.

## Eval-driven development paid for itself

I started with 7 fixtures and exact-match grading, then expanded to **33
fixtures across 14 categories** in thematic files, reporting per-category
precision/recall. Expanding the set immediately caught two bugs that all the
unit tests had passed:

1. The "ledger table" regex matched `account` but not `accounts` — `\baccount\b`
   breaks on the plural `s`, so writes to `accounts`/`transactions` were
   silently not counted. Real risk findings were being dropped.
2. A case-insensitive `POST` handler pattern matched the word "post" inside
   `audit.record("post")`, producing a false "missing idempotency" finding.

Neither shows up in hand-written unit tests, because unit tests encode the cases
you already imagined. A broad, realistic fixture set encodes what the system
*should* do — and the gap is where the bugs were. That single experience did
more to convince me of eval-driven development than any blog post.

## Prompting the reviewer for recall

Recent models follow "be conservative, only report high-severity issues" quite
literally, which silently drops findings. So the reviewer prompt asks it to
**report everything with a confidence and severity**, and the gate filters
afterward. Coverage at the finding step, filtering downstream.

## Safety and rollout

The diff is **scrubbed** (emails, cards via Luhn, AWS/JWT/`sk-` tokens, private
keys) before it ever reaches the model — no customer PII or live credential
leaves the process. The gate is **advisory by default**: it computes what
*would* block but never fails the merge, matching a sane rollout ("advisory
first, enforce later"). A GitHub Action posts one sticky comment per PR, found
and updated by a marker so it doesn't spam on every push.

## Failure modes

Pattern-based checks have false positives and negatives by nature; the
advisory gate, a clean-PR fixture set as a precision guard, and the LLM layer
all mitigate that. The diff parser is minimal (added lines only). These are
documented, not hidden.

**Repo:** `projects/fintech-backend-guard-agent` · 14 checks, 48 tests, 33 eval
fixtures at precision/recall = 1.00, OpenTelemetry + cost, PR comment bot.
