## Answer
Headline: can't tell

Treatment's raw CTR is higher, 31.20% against 30.00%, a gap of +1.20 pp. The arms are badly unbalanced, so I can't trust that number as the causal effect of the ranker. [measured]

## What it means for the launch decision
The raw gap is about +1.2 pp, with a naive interval of roughly ±0.08 pp that treats every search as independent. The sample-ratio failure could plausibly account for a gap of this size, so the data doesn't show whether the true lift clears your launch threshold. Don't launch on this number. Find out why the arms differ in size, then re-run or re-analyze.

## Why we believe it
- Alternatives considered:
  - Real ranker effect: not ruled out. It is consistent with the data, but the unbalanced arms leave it unconfirmed. [inferred]
  - Differential exposure or eligibility between arms (a bug, a filter, or logging loss in treatment): not ruled out. Treatment has 4.8% fewer users and searches, and a loss like that is often not random. [inferred]
  - Random chance causing the user imbalance: ruled out. The arms hold 499,930 control user-days against 475,990 treatment (51.2% / 48.8%). Under a true 50/50 split that is z≈24. [measured]
  - Day-to-day or novelty swings driving the gap: ruled out. The per-day user counts are almost constant and the CTR gap shows up on every day. I did not fit a time trend. [measured]
- Checks run:
  - Sample-ratio check (50/50 as designed): fail. See the user counts above.
  - Searches per user: pass. It is exactly 6.0 in both arms, so the imbalance is in who is counted, not in how active they are. [measured]
  - Date coverage: pass. 14 complete days per arm, 2026-09-17 to 2026-09-30.
  - Interval for the raw lift: flag. The ±0.08 pp is a two-proportion z-test on searches. Searches cluster within users, and I only have daily aggregates, so the true interval is wider. I did not compute a clustered one.
  - Pre-experiment (A/A) balance, segment breakdowns, user-level data: could not run. The database has only the one aggregate table.

## Caveats, and what would change the answer
- If the cause of the user imbalance is found and the arms are shown to be comparable, for example by fixing a logging bug or reweighting, the +1.2 pp could stand. A user-level re-analysis would then give a proper interval.
- If treatment lost users non-randomly, such as dropping low-engagement users or failing to log searches, the true lift could be smaller, zero, or negative.
- The "users" column looks like daily active users, not unique users, so I can't tell whether the same users are counted across days.
- I had no stated launch threshold. I'm assuming any real lift would need to be well above 0.

## Provenance
- Metric: CTR = clicks / searches, summed over the 14 days per arm, from stated here [guess]. No metrics.json was present.
- Data: `experiment_daily` in warehouse.db (28 rows), through 2026-09-30.
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: ad-hoc Python/sqlite3 run in this session. No log file was saved.