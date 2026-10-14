## Answer
Headline: can't tell
Treatment's CTR is higher than control's by about 1.2 pp, but the arms are badly unbalanced (a sample-ratio mismatch), so the data can't show that the ranker caused the gap.
- Observed: +1.20 pp (95% CI +1.12 to +1.27), 31.20% vs 30.00% clicks per search
- Adjusted: not computed (the table is daily arm-level aggregates with no user or segment covariates, so there is nothing to hold fixed)
- Causal effect: not identified (it would need a diagnosed and fixed assignment or logging problem, then a re-run or a user-level analysis showing which users are missing from treatment)

## What it means for the launch decision
I don't know the smallest lift that would change the decision. The observed interval is far above zero, but it is not a valid estimate of the effect. I would hold the launch until the imbalance is explained.

## Why we believe it
- Alternatives considered:
  - Chance or noise in the CTR gap: ruled out by the interval, which excludes 0 by a wide margin, and by the gap being the same size every day (+1.1 to +1.2 pp) [measured]. The interval treats searches as independent. Users repeat, so the true interval is wider. The aggregates can't show how much wider [inferred].
  - Clean 50/50 randomization: ruled out. Control has 499,930 users and treatment 475,990, so control is 51.2% of the total. The z-score is about 24, far beyond chance, and the ratio is nearly identical every day [measured].
  - Treatment losing users selectively, such as low-engagement users dropping out through bucketing, logging or exposure filtering, which would inflate its CTR: plausible but untested, because there is no user-level data [guess].
  - Searches per user: ruled out as a cause. It is exactly 6.0 in both arms [measured].
- Checks run:
  - Sample-ratio mismatch: fail. The 50/50 split is violated (z of about 24).
  - Day-by-day consistency: pass. The lift is stable across all 14 days, with no novelty or ramp pattern.
  - Searches per user balance: pass, 6.0 in both arms.
  - Covariate balance and adjusted analysis: could not run, no covariates in the data.
  - User-level clustering of the standard error: could not run, no user-level data.

## Caveats, and what would change the answer
- The 1.2 pp gap could be partly or entirely a selection artifact from the user imbalance.
- The searches-per-user figure of exactly 6.0 looks synthetic or imputed, which makes me doubt how these aggregates were built.
- User-level assignment logs, or the cause of the roughly 24k-user shortfall in treatment, would settle whether the effect can be trusted.
- If the missing users turn out to be random, the lift would stand at about +1.2 pp. I can't confirm that from this data.

## Provenance
- Metric: CTR = clicks / searches, summed over the experiment window, stated here [guess]. There is no metrics.json in the directory.
- Data: `experiment_daily` (28 rows, 2 arms × 14 days), 2026-09-17 to 2026-09-30.
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: inline Python/sqlite3 run in this session. Nothing was saved to a file.