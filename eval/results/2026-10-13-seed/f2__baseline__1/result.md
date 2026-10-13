## Answer
Headline: 55.0 % (95% CI 54.9 to 55.0)
Navigational queries had a click-through rate of 55.0% in 2026-W40: 32,878 clicks on 59,800 searches across 400 queries. [measured]

## What it means for the marketing planning doc
Use about 55%. The interval is only ±0.03 points wide, so sampling noise won't change the number. The label choice does: using superseded labels would give about 45%, so the doc should say it uses current labels. [measured]

## Why we believe it
- Alternatives considered:
  - Including superseded labels (is_current=0): ruled out. It adds 200 stale v1 navigational rows and gives 44.99%. Only is_current=1 gives one label per query. [measured]
  - Averaging per-query CTRs instead of pooling clicks over searches: not run. I used pooled clicks/searches, which is the usual definition of CTR. [guess]
- Checks run:
  - Duplicate current labels: pass. No query has more than one is_current=1 label. [measured]
  - Join coverage: pass. All 1000 stats rows have a current label. [measured]
  - Data sanity: pass. There are no null or zero searches, and no rows with clicks above searches. [measured]
  - Interval: flag. I used a delta-method ratio estimator that treats queries as independent. It is very narrow, which suggests the data is synthetic or very uniform. It also ignores any week-to-week variation. [inferred]

## Caveats, and what would change the answer
- The label version matters. Of the 400 current navigational queries, 100 come from v2 relabeling. If marketing wants a different labeling, the figure changes (45% on a naive join over all labels).
- Only W40 data exists in the table, so there is no trend or comparison.
- There is no metrics.json, so the CTR definition is my own.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) over queries whose current label is navigational, stated here [guess]
- Data: query_stats and query_labels (is_current=1), 2026-W40 (the only week present)
- Reconciled: not done (no dashboard or reference figure available)
- Queries and checks: run inline in Python against warehouse.db; no log file saved