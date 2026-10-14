## Answer
Headline: can't tell
Treatment shows a higher CTR in the raw data, but the arms fail the sample-ratio check, so the gap can't be read as an effect of the ranker. [check:srm#1]
- Observed: +1.20 pp (+1.13 to +1.27 pp), CTR 31.20% treatment vs 30.00% control, two-proportion interval on summed searches and clicks [q2]
- Adjusted: not computed (no segment columns in experiment_daily, so there is nothing to hold fixed)
- Causal effect: not identified (needs the SRM cause found and fixed, or a re-run with an even split)

## What it means for the ranker_boost launch decision
No smallest launch-relevant change was given, so none is assumed. The raw interval of +1.13 to +1.27 pp [q2] would clear any small threshold, but with the split at 48.8% treatment against a planned 50% [check:srm#1], it can't support a launch call.

## Why we believe it
- Alternatives considered:
  - Assignment or logging defect (the arms are not comparable): ruled in by the treatment share of 48.8% vs a planned 50%, p far below 0.001 [check:srm#1] [measured]
  - Mix-shift or segment composition: could not be tested, since the table has no segment columns [q1] [measured]
  - Seasonality and day of week: ruled out as a driver of the gap, since both arms cover the same 14 days and the daily split stays near 51/49 [q3] [inferred]
  - Data completeness: ruled out, all 14 days present with 2 arm rows each [check:completeness#1] [measured]
  - Real ranker improvement (requester's hypothesis): not ruled out or confirmed; it can't be separated from the assignment defect [check:srm#1] [inferred]
- Checks run:
  - srm: fail, 499,930 vs 475,990 user-days, chi2 587, p 9.9e-130 [check:srm#1]
  - completeness: pass, 2026-09-30 has 2 rows, 100% of the trailing median [check:completeness#1]
  - mix_shift: skipped, no segment dimension is available
  - fanout: skipped, no joins were run

## Caveats, and what would change the answer
- The cause of the SRM is unknown. If it is benign, such as a dropped bucket unrelated to behavior, the +1.20 pp could stand. If treatment lost low-engagement users, it would be biased upward.
- Users are summed daily counts (user-days), not unique users. Per-user assignment can't be checked.
- Intervals treat searches as independent, but they cluster within users, so the true interval is wider.
- Searches per user-day are 6.0 in both arms [q2], so the gap comes from clicks per search, not volume.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), by arm, over all days, from experiment_daily, stated here [guess]
- Data: experiment_daily (ranker_boost), through 2026-09-30
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (24 numbers on 7 lines; 3 queries, 2 checks, 0 given)