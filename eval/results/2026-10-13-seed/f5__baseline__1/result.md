## Answer
Headline: can't tell

Treatment's CTR is higher in the raw data, 31.20% vs 30.00%, which is +1.20 pp. The assignment is broken, though, so I can't say how much of that is the ranker. [measured]

## What it means for the launch decision
The naive interval is roughly +1.1 to +1.3 pp, but I wouldn't use it. Treatment has about 4.8% fewer users than a 50/50 split should give, and I can't tell whether the missing users would have clicked more or less. The data can't rule out an effect of that size coming from who was dropped.

## Why we believe it
- Alternatives considered:
  - Real ranker effect: not ruled out. The gap is consistent across all 14 days (+1.1 to +1.3 pp each day). [measured]
  - Biased assignment or logging that made the arms different: not ruled out. Treatment has 475,990 user-days vs 499,930 for control (48.8% vs 51.2%). That sample ratio mismatch is about 24 standard errors from 50/50. [measured]
  - Day-of-week or novelty effects: ruled out as a cause of the gap. The gap is stable day to day and shows no trend. [measured]
- Checks run:
  - Sample ratio (50/50 split): fail. The split is 48.8% treatment, z ≈ 24.
  - Daily consistency of the CTR gap: pass. Treatment is higher every day.
  - Per-user variance and a user-level interval: could not run. The table holds only daily arm totals, with no user or session rows.
  - Naive interval on searches as if independent: flag. It gives ±0.075 pp, which is too narrow because searches from the same user are correlated. [inferred]
  - Searches per user is exactly 6.0 in every arm and day: flag. That looks derived or modeled rather than raw logged data. [inferred]

## Caveats, and what would change the answer
- Find out why treatment lost users (eligibility filter, crashes or logging loss in the treatment path, bot filtering, or a bucketing change). If the cause is shown to be unrelated to click behavior, the +1.2 pp would be usable.
- Get user-level data for a correct interval.
- Confirm what the `users` column counts. About 35.7k per day suggests daily actives, not unique users in the experiment.
- Re-run after fixing the assignment issue.

## Provenance
- Metric: CTR = clicks / searches, pooled across the 14 days. This definition is [guess]. No metrics.json exists.
- Data: `experiment_daily` (28 rows, one per day and arm), 2026-09-17 to 2026-09-30.
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: run inline in Python/sqlite3 and not saved to a file. The queries were per-day and per-arm sums of users, searches and clicks, and the CTR derived from them.