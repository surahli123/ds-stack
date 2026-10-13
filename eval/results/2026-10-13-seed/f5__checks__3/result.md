## Answer
Headline: can't tell
Treatment's CTR is 1.20 pp higher than control's in the raw data (31.20% vs 30.00%). The arms fail the sample-ratio check, so I can't treat that gap as a causal lift.

## What it means for the launch decision
The naive interval is +1.13 to +1.27 pp, but it is not trustworthy because assignment was not 50/50. Treatment has about 4.8% fewer users than control, and I don't know which users are missing. If they are disproportionately low-clicking users, the lift is overstated by an unknown amount. Until the cause is found, the data doesn't show whether the effect clears any launch threshold.

## Why we believe it
- Alternatives considered:
  - Real effect of the ranker: not ruled out. The gap is consistent across all 14 days, so it is not noise [measured].
  - Random imbalance in the split: ruled out by the SRM test, chi2 587, p≈1e-129 [measured].
  - Missing or dropped treatment users, such as an exposure or logging bug, or a filter that removes some users: possible and not tested; the data has no user-level detail [guess].
  - Day-to-day or weekday mix shifts: ruled out as the driver, since the lift is stable every day [measured].
- Checks run:
  - srm: fail. Observed shares were 51.2% control and 48.8% treatment against a planned 50/50 [check:srm#1].
  - completeness: could not run. It needs at least 3 earlier periods and I only have the experiment window. All 14 days have rows for both arms, which I checked by eye.
  - mix_shift and fanout: skipped. There are no segment columns and no joins.

## Caveats, and what would change the answer
- The interval comes from a two-proportion z-test on searches, treating searches as independent. Searches from the same user are correlated, so the real interval is wider. This is a minor point next to the SRM failure.
- CTR is clicks/searches. Per-user data would let me use a user-level analysis.
- Finding the cause of the SRM would change the answer. If the missing users are random or can be corrected for, the +1.2 pp could stand. If they are non-random, the lift could be smaller or even reversed.

## Provenance
- Metric: CTR = clicks / searches, summed across days per arm [guess]. There is no metrics.json.
- Data: experiment_daily, 2026-09-17 to 2026-09-30, both arms present on all 14 days.
- Reconciled: not done (no dashboard or source figure available).
- Queries and checks: the checks are logged in .ds-checks.log, and the aggregate queries were run inline and not saved.