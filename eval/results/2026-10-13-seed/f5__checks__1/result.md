## Answer
Headline: can't tell
The raw treatment-minus-control CTR gap is +1.20 pp (95% CI +1.13 to +1.27, measured). The 51.2/48.8 user split fails the sample-ratio check, so I can't treat that gap as a causal lift.

## What it means for the ranker_boost launch decision
The interval excludes zero, but only if the arms are comparable, and the SRM failure says they may not be. I don't know the smallest lift that would change the decision. Until the cause of the imbalance is found, the +1.2 pp shouldn't go into the launch decision.

## Why we believe it
- Alternatives considered:
  - Real lift from the ranker: not ruled out. CTR is higher in treatment on every one of the 14 days, by about 1.2 pp (0.312 vs 0.300) [measured].
  - Assignment or logging bias: not ruled out. Treatment has about 4.8% fewer users than expected at a 50/50 split. If the missing users are non-random, for example users dropped because of the treatment, the gap could be biased [inferred].
  - Random noise: ruled out. The interval is narrow and the effect is consistent across days [measured].
- Checks run:
  - srm: fail. Control had 51.2% of users and treatment 48.8%, chi2 587, p≈1e-130 [check:srm#1].
  - completeness: could not run. The table has only 14 days and the check needs at least 3 earlier same-weekday periods. The 28 rows cover every date from 09-17 to 09-30 with both arms, so it looks complete [inferred].
  - mix_shift and fanout: skipped. There are no segment columns, and I ran no joins.

## Caveats, and what would change the answer
- Find the cause of the SRM, such as an assignment bug, bot filtering, or a logging gap in treatment. If the cause is benign and random, the +1.2 pp holds. If it is selective, the lift could be biased in either direction.
- The interval treats searches as independent. Clicks are summed per search, but the same users repeat across searches and days, so the real interval is wider. I only have daily aggregates, so I can't compute a user-level interval.
- There is no segment or user-level data, so I can't re-weight or check heterogeneity.
- CTR is clicks per search, and the unit is percentage points.

## Provenance
- Metric: CTR = clicks / searches, summed over the window [guess]. metrics.json doesn't exist here.
- Data: experiment_daily (experiment = ranker_boost), 2026-09-17 to 2026-09-30.
- Reconciled: not done (no dashboard or source to compare against).
- Queries and checks: the queries were run inline and not logged. Check output is in `.ds-checks.log` (srm#1, completeness#1).