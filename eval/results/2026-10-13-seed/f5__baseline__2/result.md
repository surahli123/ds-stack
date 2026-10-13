## Answer
Headline: can't tell
Treatment's raw CTR is 31.20% against 30.00% for control, a gap of +1.20 pp. The arms are not a clean 50/50 split, so I can't trust that number as the effect of the ranker.

## What it means for the launch decision
The naive interval is +1.13 to +1.27 pp, but it is not valid here. The assignment problem could by itself produce a gap of the same size as the one seen. I can't say whether the true effect clears your minimum worthwhile lift, or whether it is positive at all. Don't launch on this number.

## Why we believe it
- Alternatives considered:
  - Real ranker effect: not ruled out. The gap is consistent every day, at +1.1 to +1.3 pp. [measured]
  - Biased assignment or logging: not ruled out, and the sample ratio mismatch (SRM) below points to it. Treatment has about 4.8% fewer users (475,990 vs 499,930; 48.77% share against the expected 50%). If the missing users were low-clickers dropped from treatment, CTR in that arm would rise. [inferred]
  - Random noise: ruled out. A mismatch this large (chi-square ≈ 587 on 1 df) is far beyond chance. [measured]
  - Day-of-week or novelty effects: ruled out as the cause of the gap. It is steady across all 14 days, and the user counts in each arm barely move from day to day. [measured]
- Checks run:
  - Sample ratio mismatch (users by arm): fail. 48.77% in treatment against 50% expected.
  - Daily consistency of the gap: pass. Treatment is above control on every day.
  - Naive interval on clicks per search: flag. It treats each search as independent. Searches from the same user are correlated, so the interval is too narrow, and I only have daily aggregates and can't correct for it.
  - Searches per user: pass. It is 6.0 in both arms, so the user shortfall is not offset by heavier use. [measured]

## Caveats, and what would change the answer
- Find out why treatment is missing about 24k users. Possible causes are a bucketing bug, a crash or logging loss in the new ranker, bot filtering that hits one arm harder, or a late ramp-up. Rerunning after a fix, or getting user-level data to see who is missing, would settle it.
- User-level data would let me compute a proper interval clustered by user.
- I don't know what lift would be needed to justify launch. No threshold was given.

## Provenance
- Metric: CTR = clicks / searches, pooled over the 14 days. This is my own definition [guess]. No metrics.json was present.
- Data: `experiment_daily` in warehouse.db, 2026-09-17 to 2026-09-30, all 14 days present.
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: run inline in Python (sqlite3) and not saved to a file. They are the pooled sums by arm, a two-proportion z-interval, and a chi-square test of the user split.