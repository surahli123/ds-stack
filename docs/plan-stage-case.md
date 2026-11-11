# Plan-stage eval case: a framing disagreement (2026-11-11)

The first recorded plan-stage incident for the archive rule in `plan-critique.md`; one more wires plan-critique into the method. It came from a real framing session, reviewed adversarially afterwards, and its outcome is known.

## Task

A PM reads customer feedback as "CJK search quality is poor". The analyst's quality metric (keyword and AI search) says otherwise: one CJK language is clearly worse but small and concentrated in a few large accounts, while a larger, dispersed group of European languages sends little feedback. Asked: how should the analyst frame and research the disagreement?

## What the reply missed

The agent answered with no lookups and no questions. It got the framing right: split measurement, weighting and unit of analysis; account clustering; suppressed demand. It missed four things the plan-critique questions ask:
- it never asked what decision was on the table;
- its headline test validated the metric only on complained-about queries;
- it assumed tenant data could be replayed and shown to raters;
- it asked seven questions.

The decision actually made matched none of the three outcomes its decision rule offered (Korean-specific work, a platform fix, neither): prioritize the top five languages, split by region.

## Fixture

A task file and an overlay naming the metric and the judge's known bias. No warehouse is needed. Grade by script, not by a model:

| Item | Pass if the plan |
|---|---|
| Decision first | asks, or states as `[guess]`, which decision the work feeds, and lists scope options (which languages, which regions) |
| Overlay used | names the overlay's metric and judge bias instead of hedging on them |
| Control sample | validates the metric on a sample drawn independently of complaints |
| Access | names data access or reproducibility as a gating step |
| Size | asks at most three questions |

The 2026-10-30 reply fails all five; on the first, it named a decision as fact and offered no scope options. Calibrate on plain prompting first, as for the analysis cases.
