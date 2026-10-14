## Answer
Headline: can't tell

Treatment's CTR is 1.20 pp higher than control's, but the arms fail the sample-ratio check, so I can't call that a treatment effect.

- Observed: +1.20 pp (95% CI +1.13 to +1.27) [measured]. Treatment CTR is 31.20% and control is 30.00%, from clicks/searches pooled over 14 days. The interval is a naive two-proportion one that ignores clustering by user, so it is too narrow.
- Adjusted: not computed (the data has only daily arm totals, so there are no segments or user-level covariates to hold fixed, and the cause of the imbalance is unknown).
- Causal effect: not identified. It would need either the cause of the user imbalance found and fixed, or a rerun with a clean 50/50 assignment. User-level assignment logs would let me check which users are missing.

## What it means for the launch decision
The naive +1.2 pp is steady across all 14 days, so it is unlikely to be noise. The arms are not comparable, though, so I can't say whether the true effect clears your minimum worthwhile lift. I'd hold the launch decision until the imbalance is explained.

## Why we believe it
- Alternatives considered:
  - Assignment bias or logging loss: ruled in. Treatment has 475,990 users against control's 499,930 (48.8% vs 51.2%). Treatment's searches per user are the same as control's (6.0), so the shortfall is in users, not activity. [measured]
  - The 4.8% of users missing from treatment are low-CTR users, such as users who bounced or errored. That would inflate treatment CTR. It is plausible but untestable here. [inferred]
  - Random day-to-day noise: ruled out. Treatment is above control on every one of the 14 days (+1.1 to +1.2 pp). [measured]
  - Novelty effect or a time trend: no sign of one in the daily series. [measured]
- Checks run:
  - srm: fail. Observed share is 51.23% / 48.77% against the planned 50/50, chi2 587, p≈1e-129 [check:srm#1].
  - completeness: could not run. It needs at least 3 earlier periods. By hand, all 14 days (09-17 to 09-30) are present for both arms, with 28 rows. [measured]
  - fanout: skipped, because I ran no joins.
  - mix_shift: skipped, because the data has no segments.

## Caveats, and what would change the answer
- The SRM failure invalidates the arm comparison until its cause is found.
- The standard error is naive. User-level variance would widen the interval.
- Per-user CTR or retention data would help show who is missing from treatment.
- If the cause of the imbalance turns out to be harmless and independent of the outcome, the observed +1.2 pp could stand as the effect.

## Provenance
- Metric: CTR = clicks / searches, pooled over the period. Stated here [guess]; no metrics.json exists.
- Data: `experiment_daily`, 2026-09-17 to 2026-09-30, all 14 days present.
- Reconciled: not done (no dashboard or other source was provided).
- Queries and checks: the check results are logged in `.ds-checks.log` in the analysis directory. The queries were run inline and are not saved to a file.