## Answer
Headline: 55.0 % (54.6 to 55.4 %)
Navigational queries in 2026-W40 had a click-through rate of about 55.0 %, which is 32,878 clicks on 59,800 searches. [measured]
- Observed: 55.0 % (54.6 to 55.4 %). This is a binomial interval on searches, so it ignores clustering by query and is probably slightly too narrow. [measured]
- Adjusted: not computed (a single descriptive rate, no comparison)
- Causal effect: not identified (this is a level, not an effect, and there is no intervention to evaluate)

## What it means for the planning doc
Quote about 55 %. Any planning threshold that moves the number by less than about 0.5 pp is within the noise.

## Why we believe it
- Alternatives considered:
  - Using all label versions: ruled out. This gives 45.0 % because it counts 600 queries, including superseded labels. [measured]
  - Averaging per-query CTRs instead of dividing total clicks by total searches: ruled out. It gives 55.0 %, so the choice doesn't matter. [measured]
- Checks run:
  - One current label per query: pass. No query has two current labels, and every query in the stats has one.
  - Data sanity: pass. The week has 1,000 rows for 1,000 distinct queries, no row has clicks above searches, and no searches value is null.

## Caveats, and what would change the answer
- I used the current label (`is_current=1`), which is 300 queries from label v1 and 100 from v2. If marketing means the labels as they were at the time, the number would differ. [inferred]
- CTR is defined as clicks divided by searches, summed over queries. There is no metrics.json, so this definition is my assumption. [guess]

## Provenance
- Metric: sum(clicks) / sum(searches) for queries whose current intent is navigational, stated here [guess]
- Data: query_stats and query_labels in warehouse.db, week 2026-W40 (the only week in the table)
- Reconciled: not done (no dashboard or reference figure available)
- Queries and checks: run inline in the shell; they are not saved to a file.