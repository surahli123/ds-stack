## Answer
Headline: can't tell
Treatment shows a higher CTR (+1.20 pp), but the arms are not comparable because the user split is off (51.2/48.8 instead of 50/50), so I can't call it a real lift.
- Observed: +1.20 pp (95% CI +1.13 to +1.27), CTR 30.00% control vs 31.20% treatment [measured]
- Adjusted: not computed (the data has only daily arm totals, with no user-level or segment fields to hold fixed)
- Causal effect: not identified (it would need the cause of the 24k-user shortfall in treatment found and fixed, or a re-run with a clean split)

## What it means for the launch decision
The interval excludes zero, but that only describes the observed gap. The sample ratio mismatch (SRM) means that gap could come from who was assigned or logged, not from the ranker. I'd hold the launch decision until the cause is found. I wasn't given a minimum lift that would change the decision, so I can't compare the interval against one.

## Why we believe it
- Alternatives considered:
  - Chance in the split: ruled out by the SRM test, chi² 587, p≈1e-130 [measured]
  - Treatment dropping or filtering users, for example users with poor or failed sessions, or a logging or bucketing bug: ruled in as plausible, not tested [inferred]
  - Treatment users searching more: ruled out, since searches per user are 6.0 in both arms [measured]
  - Daily noise or a novelty effect: not tested; the daily data has no obvious spike, but I didn't check trends [guess]
- Checks run:
  - srm: fail. Observed shares were 0.5123 control and 0.4877 treatment (499,930 vs 475,990 users) [check:srm#1]
  - completeness: could not run. The check needs at least 3 earlier periods of history and this table has only 14 days per arm. All 14 days (09-17 to 09-30) are present for both arms.
  - mix_shift: skipped. There are no segment breakdowns in the data.
  - fanout: skipped. I ran no joins.

## Caveats, and what would change the answer
- Finding why treatment has about 24k fewer users would change the answer. If it's a bug that is independent of user quality, a corrected comparison could support the lift.
- The standard error treats searches as independent. Clicks are clustered by user, so the real interval is wider than the one above.
- The SRM check ran on user totals. The daily user counts are nearly constant, which suggests an assignment or logging issue rather than a drift over time [inferred].

## Provenance
- Metric: CTR = clicks / searches, summed over the 14 days [stated here, guess]. There is no metrics.json in the directory.
- Data: experiment_daily (experiment = ranker_boost), 2026-09-17 to 2026-09-30
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: the SQL and the arithmetic were run inline and not saved. Check results are in .ds-checks.log (srm#1, completeness#1).