## Answer
Headline: can't tell
The raw CTR gap is +1.20 pp for treatment, but the arms fail the sample ratio check, so it can't be read as the effect of the ranker. [q3, check:srm#1]
- Observed: +1.20 pp (+1.13 to +1.27) [q4]
- Adjusted: not computed (no segment columns in the data; the table has only arm-by-day totals)
- Causal effect: not identified (needs a split that passes SRM, or the cause of the user imbalance found and fixed, then re-analysis)

## What it means for the launch decision
No launch threshold was provided. The observed interval excludes zero, but the randomization is broken, so the launch call shouldn't rest on it. [q4, check:srm#1]

## Why we believe it
- Alternatives considered:
  - Broken or biased assignment (users dropped or filtered differently by arm): ruled in by user shares 51.2% control vs 48.8% treatment against a planned 50/50 [check:srm#1] [measured]
  - Day of week or seasonality: ruled out as a driver of the gap, since both arms cover the same 14 complete days and the user counts are near-constant daily [q2, q3] [inferred]
  - Data completeness: ruled out, all 14 days have both arms [check:completeness#1] [measured]
  - Real ranker effect: not separable from the assignment problem [check:srm#1] [inferred]
- Checks run:
  - srm: fail chi2 587, p<0.001, arms not comparable [check:srm#1]
  - completeness: pass 2026-09-30 has both arms, 100% of the trailing median [check:completeness#1]
  - mix_shift: skipped, no segment dimension in the table
  - fanout: skipped, no joins used

## Caveats, and what would change the answer
- Control CTR is exactly 0.3000 over 2,999,580 searches [q3], which is unusually round and may mean synthetic or modeled data. Check the logging pipeline.
- If the missing treatment users were dropped for a reason unrelated to clicks, the lift may hold. That needs user-level assignment logs to show.
- CTR here is clicks/searches, not clicks/users. Confirm that is the intended definition.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) per arm over the whole window, from stated here [guess]
- Data: experiment_daily, through 2026-09-30
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (13 numbers on 7 lines; 3 queries, 2 checks, 0 given)