## Answer
Headline: can't tell
The naive CTR difference is +1.20 pp (95% CI +1.13 to +1.27; clicks/searches, 30.00% vs 31.20%). The assignment is badly imbalanced, so I can't treat that figure as the causal lift. [measured]

## What it means for the launch decision
I don't have a smallest change that would alter the decision, so I can't compare it with the interval. The +1.13 to +1.27 pp interval assumes the arms are comparable, and the sample ratio mismatch says they may not be. Don't use it for the launch until the cause of the imbalance is found.

## Why we believe it
- Alternatives considered:
  - Real treatment effect: not ruled out. The gap is stable every day (about +1.1 to +1.3 pp), which fits a real effect. [measured]
  - Assignment or logging bug, or differential exclusion in treatment: not ruled out. Treatment has 475,990 users against 499,930 in control (48.8% vs 51.2%, planned 50/50), about 24k fewer. If the missing users are non-random, for example low-engagement users dropped or filtered, CTR would be biased upward. [inferred]
  - Noise: ruled out as the cause of the imbalance by the SRM test (p≈1e-130). [measured]
- Checks run:
  - srm: fail. Chi2 587, p≈1e-130, shares 0.5123 vs 0.4877, so the arms are not comparable until the cause is found.
  - completeness: could not run. The table has only 2 rows per day over 14 days, and the check needs at least 3 earlier same-weekday periods before the target. Every day 09-17 to 09-30 is present for both arms, which I checked by eye.
  - fanout: skipped. I used a single table with no joins.
  - mix_shift: skipped. The table has no segment dimension.

## Caveats, and what would change the answer
- Find out why treatment has fewer users. If the cause is benign and independent of outcomes, the +1.2 pp would be credible. If it is not, the estimate is unreliable and the test needs a rerun.
- The interval treats searches as independent. Clicks are correlated within a user, so the true interval is wider. Only daily aggregates are available, so I couldn't cluster by user. [inferred]
- I used a per-search CTR, clicks over searches. [guess]
- Searches per user are identical across arms (6.0), so the lost users look like whole users, not partial sessions. [measured]

## Provenance
- Metric: CTR = clicks / searches, pooled across the 14 days, stated here [guess]. There is no metrics.json.
- Data: experiment_daily in warehouse.db, 2026-09-17 to 2026-09-30.
- Reconciled: not done (no dashboard or source to compare against).
- Queries and checks: the checks are logged in .ds-checks.log (srm#1, completeness#1). The queries were run inline in Python and aren't saved to a file.