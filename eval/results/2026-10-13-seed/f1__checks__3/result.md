## Answer
Headline: about 0.0 pp attributable to v2 (95% interval −0.15 to +0.15 pp) [measured]
Overall CTR fell 2.10 pp (30.42% → 28.32%), but essentially all of that (−2.09 pp) is a shift in traffic toward mobile, which has a lower CTR. Within-segment CTR under v2 is flat (−0.00 pp). [measured]

## What it means for the rollback decision
The check's minimum effect of interest is 0.1 pp, and the interval (±0.15 pp) is slightly wider than that. So this data rules out v2 causing anything like the 2.1 pp drop. It can't rule out a harm of 0.1–0.15 pp. Rolling back would not recover the drop. [inferred]

## Why we believe it
- Alternatives considered:
  - v2 lowered CTR: ruled out as the cause of the 2.1 pp drop. Within-segment effect is −0.002 pp, and all four platform×country segments are flat (changes within ±0.08 pp). [measured]
  - Traffic mix shift: ruled in. Mobile share of searches rose from 40% to 55%, and mobile CTR (~22%) is far below desktop (~35%). Mix accounts for 99.9% of the change. [measured]
  - Cause of the mobile shift: not determined. It could be a campaign, seasonality or a logging change. It could also be v2 itself, if v2 pulled in mobile traffic. [guess]
  - Time or seasonality: not separable here. Before/after is a single week each, and v2 launched on all traffic at once. [inferred]
- Checks run:
  - mix_shift: flag. Mix-dominant (mix share 100%). Within-segment −0.002 pp, CI −0.15 to +0.15. The interval assumes independent units, so it may be somewhat too narrow. [check:mix_shift#1]
  - completeness: pass. 2026-10-04 has 4 rows, 100% of the trailing median. [check:completeness#1]
  - srm: skipped. This is a before/after rollout with no concurrent control arm.
  - fanout: skipped. No joins were used.

## Caveats, and what would change the answer
- There is no concurrent holdout. Every row is v1 before 09-28 and v2 after, so v2 is confounded with the date. A holdout or A/B arm would settle it.
- If the mobile surge was caused by v2, the mix effect is partly attributable to v2. Check the traffic source for that week.
- Segments are only platform×country. Query type, user cohort or other splits could hide effects.
- The intervals treat searches as independent. Clicks within a user or day are correlated, so the real interval is probably wider.

## Provenance
- Metric: CTR = clicks / searches, summed across segments. This is stated here [guess]; there is no metrics.json.
- Data: search_daily and release_log, through 2026-10-04. That day is complete.
- Reconciled: not done (no dashboard or source to compare against).
- Queries and checks: checks are logged in `.ds-checks.log` in the analysis directory. The aggregation queries were run inline and are not logged. The check inputs are in /tmp/mix.json and /tmp/comp.json.