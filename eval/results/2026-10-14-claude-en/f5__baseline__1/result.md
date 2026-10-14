## Answer
Headline: can't tell
Treatment's CTR is higher in the data, by about 1.2 points. But the arms are badly unbalanced, so I can't say that gap is the effect of the ranker change.
- Observed: +1.20 pp (95% CI +1.12 to +1.27), treatment 31.20% vs control 30.00% [measured]. The interval treats each search as independent. Clustering by user would widen it, but there is no user-level data to correct for that.
- Adjusted: not computed (the table has only daily arm totals, so there are no covariates to hold fixed)
- Causal effect: not identified (it would need a working randomization. That means finding and fixing whatever caused the allocation mismatch, then re-running or re-deriving the assignment from the raw assignment logs.)

## What it means for the launch decision
The interval, +1.1 to +1.3 pp, is far above any plausible minimum worthwhile lift. But the sample ratio mismatch (SRM) means the assignment was not a clean 50/50 randomization, so that interval does not support a launch decision. I would not launch on this readout until the SRM is explained.

## Why we believe it
- Alternatives considered:
  - Chance imbalance in arm sizes: ruled out. Control has 499,930 user-days and treatment has 475,990, a 51.2/48.8 split. That is z ≈ 24 against 50/50, and the gap is the same size every day [measured].
  - Selective loss or exclusion of treatment users (for example, a bug or filter that drops users in treatment): ruled in as the likely cause. If those users differ, for example by dropping low-engagement ones, CTR is inflated [inferred].
  - Novelty effect or time trend: weakly ruled out. The treatment lift is stable at about 1.1 to 1.2 pp across all 14 days [measured].
  - A real ranker improvement: still possible, but not separable from the allocation problem [guess].
- Checks run:
  - Sample ratio mismatch: fail. See the split above.
  - Searches per user: pass. It is 6.0 in both arms, so there is no engagement-volume difference [measured].
  - Daily consistency of the lift: pass. The sign is the same on every day [measured].
  - Covariate balance, user-level variance, and a segment breakdown: could not run. The table is aggregate only.

## Caveats, and what would change the answer
- Find the cause of the SRM: a bug in assignment, logging, bot filtering, or exposure triggering that applies only to treatment. If it is fixed and the lift persists, the answer becomes usable.
- User-level data would allow clustered intervals and checks on who is missing from treatment.
- "Users" is a sum of daily counts, and I don't know how it was defined. The mismatch is in that count.

## Provenance
- Metric: CTR = clicks / searches, pooled across the 14 days [stated here; guess]. There is no metrics.json.
- Data: experiment_daily (28 rows), 2026-09-17 to 2026-09-30, all days complete.
- Reconciled: not done (no dashboard or source to compare with)
- Queries and checks: ad hoc Python/sqlite3 run inline in this session; not saved to a file.