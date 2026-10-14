## Answer
Headline: can't tell

The raw CTR is higher in treatment, but the 50/50 split didn't hold. Treatment has about 4.8% fewer users than control, so I can't treat the gap as an effect of the ranker.

- Observed: +1.20 pp (±0.07 pp), treatment 31.20% vs control 30.00% CTR. [measured] The interval treats each search as independent. Users are the randomization unit, so the true interval is wider. I can't compute it from daily aggregates.
- Adjusted: not computed (the table has only arm-by-day totals, with no user-level or segment covariates to hold fixed)
- Causal effect: not identified (it would need a diagnosed and fixed assignment or exposure problem, then a rerun or a user-level analysis showing the missing treatment users are unrelated to CTR)

## What it means for the launch decision
The data can't support a launch call yet. The +1.2 pp is large against any plausible launch threshold. But the sample-ratio mismatch (SRM) could create or hide a gap of that size, depending on who is missing from treatment. Fix the assignment problem and rerun before deciding.

## Why we believe it
- Alternatives considered:
  - Clean randomization: ruled out. Users are 499,930 control vs 475,990 treatment, a 51.2/48.8 split, about z ≈ 24 against 50/50. [measured]
  - Differential user loss or filtering in treatment, such as logging drops, bot filtering, or exposure triggers: could explain the SRM, and I can't test it with this table. [guess]
  - Novelty or day-of-week effects: mostly ruled out. The daily gap is stable at about 1.1–1.3 pp, with no trend. [measured]
  - Real ranker improvement: not ruled out, but not separable from the SRM. [inferred]
- Checks run:
  - SRM on users: fail. The mismatch is far beyond chance.
  - Daily consistency of the CTR gap: pass. Every day shows treatment above control.
  - Searches per user: flag. It is exactly 6.0 on every row of both arms, which looks modeled or imputed rather than observed, so I can't use it to judge the user mismatch.
  - User-level variance and clustering: could not run, because only aggregates are available.

## Caveats, and what would change the answer
- Find the cause of the SRM, such as assignment, logging, or filtering differences between arms. Then rerun or reanalyze at user level.
- User-level data would give a correct clustered interval.
- I found no metrics.json, so the CTR definition is my assumption.

## Provenance
- Metric: CTR = clicks / searches, summed over the period [guess]. No metrics.json was found.
- Data: experiment_daily, 2026-09-17 to 2026-09-30, all 14 days, both arms.
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: ad hoc Python/sqlite3 run in this session, not saved to a file.