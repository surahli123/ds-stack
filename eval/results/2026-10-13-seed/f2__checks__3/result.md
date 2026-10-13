```
## Answer
Headline: 55.0 % (54.9 to 55.0 %)
Navigational queries in 2026-W40 had a click-through rate of 54.98%: 32,878 clicks on 59,800 searches across 400 queries. [measured]

## What it means for the planning doc
Use about 55%. The interval is very narrow, but it reflects only sampling noise across queries, and the label choice moves the number by about 10 points. I didn't know what size of change would alter the decision, so I couldn't compare the interval against one.

## Why we believe it
- Alternatives considered:
  - Using all label rows, including superseded ones: ruled out. It gives 45.0% (600 queries, 89,700 searches), because 200 queries carry an old label with is_current=0 and would be double-counted or mislabeled. [measured]
  - Using only current labels (is_current=1): ruled in. It gives exactly one label per query, and every one of the 1,000 queries has one. [measured]
  - Treating the rate as a pooled ratio (total clicks / total searches) rather than the average of per-query rates: ruled in. This matches the usual definition of click-through rate. [inferred]
- Checks run:
  - fanout: pass. Joining the stats to current labels gave 1,000 rows from 1,000 rows. [check:fanout#1]
  - completeness: could not run. There is only one week of data and no history to compare against, so I can't confirm W40 is fully loaded. [check:completeness#1]
  - srm and mix_shift: skipped. This is not an experiment and there is no before/after comparison.
  - Data sanity: pass. There are no null or zero search counts and no rows where clicks exceed searches. [measured]

## Caveats, and what would change the answer
- The number depends on the label version. Version 2 relabeled 300 queries: 200 informational and 100 navigational are version 2 and current, and 200 navigational labels are superseded. If the old labels were the right ones, the rate would be about 45%.
- W40 may be only partly loaded, and I couldn't verify this.
- The interval comes from resampling queries (bootstrap) and assumes queries are independent. It doesn't cover label error.
- I couldn't compare against a dashboard.

## Provenance
- Metric: clicks / searches, pooled across navigational queries with is_current=1 [guess]. There is no metrics.json in the directory.
- Data: query_stats and query_labels in warehouse.db, week 2026-W40 only. I couldn't confirm it is complete.
- Reconciled: not done (no dashboard or reference figure available)
- Queries and checks: the queries were run inline and aren't saved. The check results are in .ds-checks.log (fanout#1, completeness#1).
```