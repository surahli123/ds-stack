## Answer
Headline: can't tell
Overall CTR fell 1.83 pp (30.44% → 28.61%, 95% CI −1.98 to −1.68) week over week, but v3 went to 100% of traffic on the same day, so there is no control group and the data can't separate v3 from anything else that changed that week.

## What it means for the rollback decision
The drop is real, and almost all of it (−1.82 pp) is within-segment rather than mix. But it's a before/after comparison, so the interval describes the change and not v3's effect. Any drop above about 0.1 pp would matter for this decision, and the interval is far beyond that. What's missing is a holdout or a staggered rollout, and this data can't supply either.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform/country): ruled out. Mix explains −0.01 pp of the −1.83 pp (1%) [measured, check:mix_shift#1].
  - Random week-to-week noise: ruled out as the full explanation. The noise floor is 0.15 pp against a 1.83 pp drop [measured]. This assumes independent searches.
  - v3 as the cause: not ruled in or out. The drop is concentrated in desktop (US −3.1 pp, other −2.9 pp) while mobile is flat (about −0.03 pp and −0.04 pp). That fits a v3 effect on desktop, but it equally fits a desktop-specific change such as UI, logging, or an event on the same date [inferred].
  - Seasonality or trend: not testable. Only two weeks of data exist, so there is no baseline [measured].
- Checks run:
  - mix_shift: pass. Within-segment −1.82 pp, mix −0.01 pp.
  - completeness: could not run. It needs at least 3 earlier periods and the table has only 2 weeks. Both weeks have all 28 expected rows (7 days × 4 segments) [measured].
  - srm: skipped. There is no randomized assignment.
  - fanout: skipped. No joins were used.

## Caveats, and what would change the answer
- Any of these would make the answer a number: a v3 holdout, per-request ranker logs from a partial-rollout period, or several weeks of earlier desktop CTR history.
- Check whether anything else shipped on desktop on 2026-09-07. `release_log` lists only the v3 rollout, so other changes may simply not be logged.
- If the desktop-only pattern is real, a desktop-only rollback test would answer this directly.

## Provenance
- Metric: CTR = clicks / searches, summed over the week. This is stated here [guess]; `metrics.json` does not exist in this directory.
- Data: `search_daily` and `release_log`, through 2026-09-13 (both weeks have all 28 rows).
- Reconciled: not done (no dashboard or reference source available).
- Queries and checks: the queries were run ad hoc in Python and are not saved. Check output is in `.ds-checks.log` (mix_shift#1, completeness#1).