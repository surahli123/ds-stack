```
## Answer
Headline: 36.97 percent (36.7 to 37.3)
In 2026-W41 the shopping vertical's click-through rate was 36.97%: 39,857 clicks on 107,810 searches across 900 queries.
- Observed: 36.97 percent (36.68 to 37.26)
- Adjusted: not computed (a level for one week, with no comparison to adjust)
- Causal effect: not identified (this is a single-week level, not a change; no intervention was asked about)

## What it means for Merchandising
This is a point-in-time CTR you can cite as 37.0%. The interval is about ±0.3 points, so a quoted figure at that precision is stable. I wasn't given a threshold for a decision.

## Why we believe it
- Alternatives considered:
  - Duplicate rows in query_category inflate the result: ruled in. 250 queries were reloaded on 2026-10-09 with the same category, so a plain join counts them twice. A naive join gives 40.9% (56,422 / 137,945), which is wrong. I counted each query once. [measured]
  - Queries changing category between loads: ruled out. No query has more than one distinct category. [measured]
  - Categories mapping to more than one vertical, or queries missing a category: ruled out. Neither occurs. [measured]
- Checks run:
  - Row grain: pass. query_week has 2000 rows for 2000 distinct queries, all in W41.
  - Mapping coverage: pass. All 5 categories map to exactly one vertical; shopping = electronics, apparel, home.
  - Interval: flag. It is a binomial interval that treats searches as independent. Clustering by query would widen it somewhat. [inferred]

## Caveats, and what would change the answer
- The "shopping" definition comes from category_vertical. A different mapping would change the figure.
- CTR is pooled as total clicks over total searches, so it is search-weighted. The mean of per-query CTRs would differ.
- Only W41 exists in the data, so there is no trend or comparison.

## Provenance
- Metric: clicks / searches, summed over shopping queries. No metrics.json was present, so this definition is my own [guess].
- Data: query_week, query_category (deduplicated by query), category_vertical; week 2026-W41.
- Reconciled: not done (no dashboard or reference figure available).
- Queries and checks: run inline in Python/SQLite against warehouse.db; not saved to a file.
```