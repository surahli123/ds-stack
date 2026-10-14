## Answer
Headline: can't tell
Treatment's raw CTR is higher by 1.20 pp, but the arms fail the sample-ratio check, so the comparison can't be trusted as a randomized result [q5, check:srm#1].
- Observed: +1.20 pp (95% CI +1.13 to +1.27) [q5]
- Adjusted: not computed (the data has only daily arm totals, with no segments to hold fixed, and the cause of the SRM is unknown)
- Causal effect: not identified (needs the cause of the 51.2% / 48.8% user split found and fixed, or a rerun with a clean split) [check:srm#1]

## What it means for the ranker_boost launch decision
The observed interval (+1.13 to +1.27 pp) is a precision interval on a biased comparison [q5]. No launch threshold was given, so I can't say whether it clears the bar, and the SRM means I can't call it either way [check:srm#1].

## Why we believe it
- Alternatives considered:
  - Real ranker effect: not ruled out, since the observed lift is consistent with it, but the SRM means it can't be separated from selection effects [q4, check:srm#1] [inferred]
  - Differential assignment, logging or exposure loss in treatment (treatment has 475,990 users vs 499,930): ruled in as a possible cause. The split is the same every day, which points to a systematic assignment or logging issue [q2, q3, check:srm#1] [inferred]
  - Data completeness: ruled out, all 14 days present for both arms [check:completeness#1] [measured]
  - Day of week and seasonality: ruled out as a driver of the arm gap, because both arms run the same days. Searches and clicks per user in each arm barely vary across days [q2] [inferred]
  - Mix-shift: not testable, since there are no segment breakdowns [q3] [measured]
  - Per-user volume: searches per user are identical in the two arms (6.0), so the lift comes from clicks per search, not more searching [q4] [measured]
- Checks run:
  - srm: fail, observed shares 0.512 / 0.488 vs 0.5 / 0.5, p about 1e-129 [check:srm#1]
  - completeness: pass, 2026-09-30 has 2 rows, matching the baseline of 2 [check:completeness#1]
  - mix_shift: skipped, no segment data
  - fanout: skipped, no joins

## Caveats, and what would change the answer
- The SRM fail is unresolved. If the assignment or logging owner shows the missing treatment users are unrelated to click propensity, the observed lift could stand.
- No metrics.json was available, so the CTR definition is my guess.
- No launch threshold was given.
- The data is daily aggregates only, so no user-level or segment analysis is possible.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) per arm, in experiment_daily, 2026-09-17 to 2026-09-30, stated here [guess]
- Data: experiment_daily (experiment = ranker_boost), through 2026-09-30
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (20 numbers on 9 lines; 4 queries, 2 checks, 0 given)