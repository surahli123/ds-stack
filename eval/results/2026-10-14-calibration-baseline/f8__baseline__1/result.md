## Answer
Headline: 38.3 % (95% CI 37.5 to 39.1)
Shopping-vertical queries had a click-through rate of 38.3% in 2026-W41. That is 900 queries, with clicks divided by searches.
- Observed: 38.3 % (37.5 to 39.1)
- Adjusted: not computed (this is a single level, not a comparison)
- Causal effect: not identified (nothing is being compared, so there is no causal question)

## What it means for Merchandising's citation
Cite 38.3%. The interval is about ±0.8 points, so a change smaller than that is not distinguishable. The naive join gives 42.5%, which would overstate the rate by about 4 points.

## Why we believe it
- Alternatives considered:
  - Joining query_week to query_category and then to category_vertical, so a query that sits in several categories is counted more than once: ruled out. 300 queries have 2 categories, and the join gives 42.5% over 1,200 rows. All 300 of those queries are in shopping categories (1,200 − 900 = 300), so each was counted twice. [measured]
  - The mapping table having duplicate or non-shopping rows that distort the result: ruled out. category_vertical has 5 distinct rows, and there are no duplicate (query, category) pairs. [measured]
  - Counting a query as shopping if any of its categories is shopping: this is the definition I chose. Clicks and searches are counted once per query, and "any category" was my reading of "queries in the shopping vertical." A different rule, such as primary category only, would change the number, but the data has no primary-category field. [inferred]
- Checks run:
  - Row uniqueness: pass. query_week has one row per (query, week), and W41 has 2,000 queries.
  - Data sanity: pass. There are no nulls and no row where clicks exceed searches.
  - Coverage: pass. Every W41 query has a category.
  - Interval: pass. It comes from a 2,000-draw bootstrap that resamples queries, so it allows for variation between queries.
  - Trend check: could not run. W41 is the only week in the table, so there is no prior week and no way to tell whether the period is complete.

## Caveats, and what would change the answer
- The rate is pooled: total clicks divided by total searches. The average of per-query rates would differ.
- No dashboard or `metrics.json` was available, so the definition is my own.
- If Merchandising wants a different rule for queries with several categories, the number changes.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), for queries with at least one category mapped to vertical "shopping", from the definition stated here [guess]
- Data: query_week, query_category and category_vertical in warehouse.db, for 2026-W41 only
- Reconciled: not done (no dashboard or metrics.json provided)
- Queries and checks: run inline in Python/sqlite3; not saved to a file.