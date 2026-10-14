## Answer
Headline: 38.3 % (95% CI 37.5 to 39.1)
Shopping-vertical queries had a click-through rate of 38.3% in 2026-W41: 41,300 clicks on 107,810 searches.
- Observed: 38.3 % (37.5 to 39.1), clicks ÷ searches, each query counted once [measured]
- Adjusted: not computed (this is a single-period level, with nothing to compare against)
- Causal effect: not identified (this is a descriptive rate, so there is no intervention to estimate)

## What it means for the merchandising citation
Cite 38.3%. Joining query_week to the category tables without removing duplicates gives 42.5%, which is wrong. The gap is about 4 points, far wider than the ±0.8-point interval.

## Why we believe it
- Alternatives considered:
  - Double counting from multi-category queries: ruled in as a problem and fixed by counting each query once. 300 of the 2,000 queries have more than one category. A plain join gives 143,720 searches and 42.5% CTR, because queries in several shopping categories are counted repeatedly [measured].
  - Averaging per-query CTRs instead of dividing total clicks by total searches: ruled out. I used the total-clicks ÷ total-searches definition. This is a guess about which definition merchandising expects [guess].
  - Queries with no category: ruled out. There are none in W41 [measured].
- Checks run:
  - Duplicate (query, category) rows: pass, none.
  - Data validity: pass. Clicks never exceed searches, and there are no nulls or zero-search rows.
  - Week coverage: pass. Only W41 exists, with 2,000 rows and one row per query.
  - Deduplicated count: pass. 900 distinct shopping queries, and two query forms gave the same result.
  - Interval: a bootstrap over queries, 2,000 resamples, seed 1.

## Caveats, and what would change the answer
- A queries that belongs to both a shopping and an info category is counted as shopping. If merchandising wants an exclusive split, the number would change. I did not compute that split.
- The data has only one week, so I could not check whether W41 is complete or typical.
- If merchandising defines CTR as the mean of per-query rates, the number would differ. I did not compute it.

## Provenance
- Metric: CTR = sum(clicks) ÷ sum(searches), which is my own definition [guess]. There is no metrics.json in the directory.
- Data: query_week, query_category and category_vertical, week 2026-W41 (the only week in the table).
- Reconciled: not done (no dashboard or reference figure available).
- Queries and checks: run inline in the session as Python/SQLite one-liners; no script files were saved.