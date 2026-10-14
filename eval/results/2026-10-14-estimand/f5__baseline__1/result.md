## Answer
Headline: can't tell

Treatment's CTR is 1.20 pp higher than control's in the raw data, but the arms are not a valid 50/50 split, so I can't attribute that gap to the ranker.

- Observed: +1.20 pp (95% CI +1.13 to +1.27). CTR is 31.20% in treatment vs 30.00% in control. [measured] The interval treats each search as independent. Per-user data would likely widen it, so it is too narrow. [inferred]
- Adjusted: not computed (the table has only daily arm-level totals, with no user or segment attributes to hold fixed)
- Causal effect: not identified (it needs a fix for the assignment or logging problem that caused the user-count imbalance, then a re-run or a user-level re-analysis)

## What it means for the launch decision
The raw gap of +1.2 pp is large against any plausible minimum worthwhile lift, and its interval excludes zero. But that interval only covers sampling noise, not the biased assignment. I don't recommend treating +1.2 pp as the launch number until the sample-ratio mismatch (SRM) is explained.

## Why we believe it
- Alternatives considered:
  - Real ranker effect: still possible, and the gap is consistent across all 14 days. Not ruled out. [measured]
  - Biased or lossy assignment or logging (SRM): ruled in. Treatment has 475,990 user-days vs control's 499,930, which is 48.8% vs 51.2%, z ≈ -24. A true 50/50 split would not produce this. [measured]
  - If the missing treatment users are disproportionately low-clicking (for example, a crash or a filter that drops them), CTR rises with no real improvement. [guess]
  - Day-of-week or novelty effects: the lift is stable at about 1.2 pp each day, with no visible trend. Weakly ruled out. [measured]
- Checks run:
  - SRM on users: fail. The shortfall is 5% of control users, about 24k user-days per day.
  - Daily consistency: pass. The mean daily lift is 1.20 pp (CI 1.20 to 1.20 using n=14 days). The days are suspiciously uniform: users and searches repeat the same values in a 3-day cycle, and every user has exactly 6 searches. This looks synthetic or pre-aggregated. [measured]
  - User-level variance and clustering: could not run, because only aggregates are available.
  - Pre-period A/A check: could not run, because there is no pre-period data.

## Caveats, and what would change the answer
- The answer would change if the SRM cause is found. If the dropped users are random, the +1.2 pp is probably real. If they are selected, the lift could be much smaller or zero.
- Counts here are user-days, not unique users, and I can't confirm who was dropped.
- The CI ignores within-user correlation.
- Only one experiment, ranker_boost, is in the table, and I didn't check for other concurrent changes.

## Provenance
- Metric: CTR = clicks / searches, pooled over the period, with lift as treatment minus control in percentage points. This is stated here [guess]. No metrics.json exists.
- Data: `experiment_daily`, 2026-09-17 to 2026-09-30 (all 14 days, both arms)
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: ran inline in Python against warehouse.db. Nothing was saved to a file.