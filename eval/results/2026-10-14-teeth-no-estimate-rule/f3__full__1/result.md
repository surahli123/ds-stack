## Answer
Headline: -1.83 pp (95% CI -1.98 to -1.68) overall CTR change, week over week; this is the total change that coincided with v3, not a v3 effect isolated by a control [q5, check:mix_shift#1]
Overall CTR fell from 30.4% to 28.6%, and essentially all of it is a within-segment drop on desktop (US about -3.1 pp, other about -2.9 pp), while mobile is flat [q5, check:mix_shift#1].

## What it means for the rollback decision
The whole interval (-1.98 to -1.68 pp) is far beyond the check's 0.1 pp minimum effect, so the drop is real; but v3 went to 100% with no holdout, so whether v3 accounts for all of it, rather than coinciding with it, is unconfirmed. Desktop CTR stepped down on 2026-09-07 exactly, from about 0.36 to about 0.33 daily, with mobile unchanged [q6, check:mix_shift#1].

## Why we believe it
- Alternatives considered:
  - Mix-shift (platform/country): ruled out, mix effect -0.01 pp, about 1% of the change [check:mix_shift#1] [measured]
  - Data completeness: ruled out, all 14 days have 4 rows and the last day is full [q3, check:completeness#1] [measured]
  - Seasonality / day of week: ruled out as the main driver, both windows are Mon-Sun, and the desktop step lands on a single day with no drift in the prior week [q6] [inferred]
  - Logging or definition change: not ruled out, release_log lists only the v3 rollout, but a desktop-only drop could also be desktop-side tracking [q2, q6] [inferred]
  - v3 (the PM's cause): ruled in as the most likely cause, since the timing is exact and nothing else is logged, but not isolated from other changes [q2, q6] [inferred]
- Checks run:
  - completeness: pass 2026-09-13 full [check:completeness#1]
  - mix_shift: pass mix about 0 pp, within-segment -1.82 pp [check:mix_shift#1]
  - fanout: skipped, no joins were used
  - srm: skipped, not an experiment; v3 was a full rollout

## Caveats, and what would change the answer
- No concurrent control: ranker is perfectly confounded with week. A desktop holdout on v2 or an A/B on a slice would give a causal number.
- Interval assumes independent searches (se_assumes_independent_units); real intervals are wider if users repeat.
- Why mobile is unaffected is unexplained; confirm with the ranker team that v3 differs by platform, and with logging owners that desktop click tracking did not change on 09-07.
- Only 2 weeks of data, so no seasonality baseline.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) over search_daily, all platforms and countries, from stated here [guess]
- Data: search_daily, release_log, through 2026-09-13
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (19 numbers on 6 lines; 4 queries, 2 checks, 0 given)