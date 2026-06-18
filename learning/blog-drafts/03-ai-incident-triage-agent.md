# ai-incident-triage-agent — a read-only on-call assistant

> **Draft — personalize before publishing.**

At 2am, the slow part of an incident is often the same: *what changed, and what
broke?* This agent answers that from telemetry. Given an incident bundle (the
alert plus recent deploys, error logs, optional metrics, the suspect diff, a
runbook, and service ownership), it correlates everything and proposes a ranked
root cause, blast radius, an advisory rollback candidate, the queries to run
next, who to page, and a timeline.

It is **read-only by design**: it reasons, it never acts. Every output is
advisory; a human runs the query or the rollback.

## Deterministic correlation is the moat

Like the PR guard, this is a **workflow** with a deterministic core and an
optional LLM layer. The correlator does the structured reasoning with no API
key:

- **Suspect deploys** — rank deploys shortly before the alert by time proximity,
  with a bonus when the deploy is to the alerting service.
- **Error signatures** — cluster error logs by a *normalized* message (ids,
  numbers, and uuids stripped), so "user 4821 not found" and "user 9930 not
  found" collapse into one signature you can count and rank.
- **Blast radius, timeline, rollback candidate, owner, suggested queries**, and
  a **confidence** score that drops when several deploys are equally plausible.

The LLM layer then proposes additional ranked hypotheses from the *normalized*
correlation summary (not raw logs — which also limits PII egress), with the diff
and runbook for context.

## Evaluating "did it point at the right change?"

The eval grades **top-1 / top-3 suspect-deploy accuracy** over fixture incidents
— a clear root-cause metric — fully offline. The fixtures deliberately include
the hard cases: a clear single deploy, two close deploys (ambiguity → lower
confidence), and no recent deploy at all (no suspect → low confidence rather
than a confident wrong answer).

## What I learned

**Most of incident triage is correlation, and correlation is deterministic.**
Lining up alert time ↔ deploy time ↔ error onset gets you most of the way to a
hypothesis without a model. The LLM adds value on the ambiguous cases, but
anchoring on a reproducible correlation keeps the whole thing honest and cheap.

**Read-only is a feature, not a limitation.** Making the agent incapable of
acting removes the scariest failure mode in incident response and makes it
something an on-call engineer will actually trust.

**Normalize before you cluster.** Raw error lines never group; normalized
signatures do — and the normalization doubles as light PII reduction before the
text reaches the model.

## Failure modes

Correlation isn't causation — the top suspect is a *candidate*, surfaced with a
confidence score, not a verdict. Signature normalization can over- or
under-cluster. When no deploy is in the window, it says so (low confidence)
rather than inventing a culprit.

## Next

Live connectors (Prometheus/Loki/Tempo/GitHub) instead of a JSON bundle,
metric-shift detection on the series, and a small dashboard.

**Repo:** `projects/ai-incident-triage-agent` · 26 tests, top-1 = 100% on the
fixture set, OpenTelemetry + cost, read-only.
