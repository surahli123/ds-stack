## Answer
Headline: 38.3 % (95% CI 37.5 to 39.1)
In 2026-W41, shopping-vertical queries had 41,300 clicks on 107,810 searches, a click-through rate of 38.3%. [measured]
- Observed: 38.3 % (37.5 to 39.1)
- Adjusted: not computed (this is a single-week level, not a comparison)
- Causal effect: not identified (this is a descriptive rate, with no intervention or comparison)

## What it means for Merchandising
Merchandising can cite 38.3%, give or take about 0.8 points. If they compare it with another week or vertical, only a difference larger than about 1 point would be distinguishable from noise.

## Why we believe it
- Alternatives considered:
  - Joining query_category to category_vertical directly gives 42.5%: ruled out. 300 queries carry more than one category, and the join counts each of them twice (1,200 rows against 900 distinct queries). [measured]
  - Some queries are in both shopping and info categories: inferred. I counted each query once if any of its categories is shopping, which is the reading that matches "queries in the shopping vertical". The data doesn't say how to treat a query in both. [inferred]
  - CTR as the mean of per-query CTRs instead of total clicks over total searches: not used. I used the pooled ratio, which is the usual CTR definition. [guess]
- Checks run:
  - Row counts: pass. The table has 2,000 rows, one per query, all in W41, and no nulls or rows with clicks above searches.
  - Fan-out dedup: pass. Counting each query once (via `IN` or `DISTINCT`) gives 900 queries, 107,810 searches and 41,300 clicks.
  - Interval: pass. It is a ratio-estimator standard error clustered by query (SE 0.42 points, so ±0.83).

## Caveats, and what would change the answer
- If Merchandising wants the per-category-row method, where a multi-category query counts once per category, the figure would be 42.5%. I don't recommend it.
- The definition of CTR is assumed. No metrics.json was provided.
- The interval treats queries as a random sample of a larger population. If the 900 queries are the whole population, the true uncertainty is smaller.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) over distinct shopping-vertical queries, stated here [guess]
- Data: query_week, query_category, category_vertical in warehouse.db, through 2026-W41 (the only week present)
- Reconciled: not done (no dashboard or source figure available)
- Queries and checks: run inline with Python and sqlite3; no script file saved.