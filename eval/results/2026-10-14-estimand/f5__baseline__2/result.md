## Answer
Headline: can't tell. The observed CTR difference is +1.20 pp, but the arm sizes show the split was not a clean 50/50, so I can't call it a treatment effect.

Treatment's CTR was 31.20% against 30.00% for control, a gap of +1.20 pp. Treatment has about 5% fewer users than control, which a clean randomized split would almost never produce.
- Observed: +1.20 pp (95% CI +1.13 to +1.27) [measured]. This is clicks/searches, treatment minus control, over 2026-09-17 to 09-30. The interval treats searches as independent. Users repeat across searches and days, so the true interval is wider.
- Adjusted: not computed (the data is daily aggregates by arm only, with no user or segment attributes to hold fixed)
- Causal effect: not identified. It would need an explanation for the sample-ratio mismatch (SRM), such as an assignment or logging bug, followed by a clean re-run or a user-level analysis that corrects for it.

## What it means for the ranker_boost launch decision
I don't know how small a CTR change would alter the decision, so I can't say whether +1.2 pp clears it. The observed gain is stable and far from zero. But the SRM means the assignment mechanism is suspect, so I wouldn't use this number for launch until the mismatch is explained.

## Why we believe it
- Alternatives considered:
  - Chance difference in arm sizes: ruled out. Control has 51.2% of user-days (499,930 vs 475,990), z ≈ 24, and the gap repeats every day (about 35.7k vs 34.0k) [measured].
  - Treatment itself causing users to drop out or go unlogged: ruled in as plausible. If low-engagement users were lost from treatment, CTR would rise artificially [inferred].
  - Novelty effect or a one-day fluke: ruled out for the observed gap. The daily gap is +1.1 to +1.2 pp every day, with no trend [measured].
  - Differences in search volume per user: ruled out. Searches per user is exactly 6.0 in both arms [measured].
- Checks run:
  - SRM check, user counts against a 50/50 split: fail. See the numbers above.
  - Daily consistency of the CTR gap: pass. The gap is stable across all 14 days.
  - Searches per user balance: pass. It is 6.0 in both arms.
  - Covariate balance and user-level analysis: could not run. Only daily aggregates exist.

## Caveats, and what would change the answer
- The cause of the SRM is unknown. If it is explained as harmless, for example a known assignment cap, the +1.2 pp could become usable.
- The data looks unusually regular. Searches per user is exactly 6.0 and control CTR repeats at exact values. That suggests aggregated or synthetic data, so check the upstream pipeline.
- The CTR definition is my assumption.
- The intervals ignore within-user correlation.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) per arm [guess]. No metrics.json was present, so this definition is stated here, not taken from a file.
- Data: experiment_daily, 2026-09-17 to 2026-09-30, all 14 days (28 rows) [measured]
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: ad hoc Python/sqlite3 run inline in this session. No script or log was saved.