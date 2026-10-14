## Answer
Headline: can't tell (the arms are unbalanced, so the +1.20 pp gap can't be credited to the ranker)

Treatment's CTR was 31.20% against 30.00% for control, but the 50/50 split didn't hold. Treatment has about 5% fewer users than control, which points to a broken assignment or logging process.

- Observed: +1.20 pp (95% CI +1.13 to +1.27), clicks/searches pooled over 09-17 to 09-30 [measured]. The interval treats searches as independent and ignores clustering by user, so it is too narrow.
- Adjusted: not computed (the table has only daily arm-level totals, with no user-level covariates or segments to adjust on)
- Causal effect: not identified (it would need an explanation for the sample ratio mismatch, and then either a corrected re-analysis or a rerun with user-level data)

## What it means for the launch decision
The decision hinges on whether the true lift clears your minimum worthwhile threshold, which I don't have. The observed +1.13 to +1.27 pp would clear any threshold below about 1 pp if it were causal. With the sample ratio mismatch, I wouldn't base the launch on this number until the cause is found.

## Why we believe it
- Alternatives considered:
  - Chance imbalance: ruled out. Users are 499,930 control vs 475,990 treatment (51.2% / 48.8%), z ≈ 24 against an expected 50/50 split. The gap is also stable every day, from 35.7k vs 34.0k on 09-17 through 09-30. [measured]
  - Treatment losing or dropping users, for example by excluding low-engagement users or through a logging or eligibility bug: plausible, and it would inflate treatment CTR. I can't test it without user-level data. [guess]
  - Novelty effect or time trend: unlikely. The daily lift is flat at about 1.2 pp across the 14 days. [measured]
  - Different search intensity per user: ruled out. Searches per user are 6.0 in both arms. [measured]
- Checks run:
  - Sample ratio (SRM) check: fail. See the numbers in the first alternative above.
  - Daily consistency of the lift: pass. The lift is positive every day, between 1.1 and 1.2 pp.
  - Covariate balance and user-level variance: could not run. The table has only daily aggregates.

## Caveats, and what would change the answer
- If the SRM is traced to a benign cause, such as a logging gap unrelated to behavior, the observed lift could stand as causal. If it comes from selective dropping, the true effect could be much smaller or zero.
- User-level assignment and click data would allow a proper clustered interval and a check of who is missing.
- The CTR definition is assumed, not documented.

## Provenance
- Metric: CTR = clicks / searches, pooled over days, from stated here [guess]. There is no metrics.json.
- Data: experiment_daily (28 rows, 2 arms × 14 days), through 2026-09-30
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: inline Python/sqlite queries in this session only; no log file was saved.