## Answer
Headline: 36.97 % (interval not computed; this is a full count of the data, not a sample)
The click-through rate for shopping-vertical queries in 2026-W41 was 36.97% (39,857 clicks on 107,810 searches, 900 queries).
- Observed: 36.97 % (no interval; full population)
- Adjusted: not computed (no comparison or confounder in the question)
- Causal effect: not identified (this is a single-week descriptive rate, not an effect)

## What it means for merchandising
There is no decision threshold to compare against. Cite 36.97%, not the 40.90% that a naive join gives. Check for double-counting before quoting any other figure from this join.

## Why we believe it
- Alternatives considered:
  - Naive join of query_week to query_category to category_vertical: ruled out. It gives 40.90% on 137,945 searches because 250 queries have a second category row loaded on 2026-10-09. That inflates the row count from 900 to 1,150 [measured].
  - Queries with conflicting categories: ruled out. No query has more than one distinct category, so the duplicates are exact repeats and de-duplicating by query_id is safe [measured].
  - Dirty click data: ruled out. No rows have clicks above searches or zero searches [measured].
- Checks run:
  - fanout (naive join): fail. The right side had 250 duplicate-key rows (2,250 rows for 2,000 keys) and the join added 250 rows [check:fanout#1].
  - fanout (de-duplicated, using `IN` on distinct queries): pass. 900 rows in, 900 rows out [check:fanout#2].
  - completeness: could not run. The data holds only W41, and the check needs at least 3 earlier periods. Whether W41 is fully loaded is unverified [check:completeness#1].
  - mix_shift and srm: skipped. Nothing is being compared over time and there is no experiment.

## Caveats, and what would change the answer
- W41 may be partial. All 2,000 queries have a row, but I couldn't confirm the week is complete.
- I define the rate as total clicks divided by total searches (searches-weighted). The mean of per-query rates would differ.
- I assumed a query's category is its current one. The 2026-10-09 rows duplicate the 2026-09-01 rows exactly, so this makes no difference here.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), stated here [guess]. There is no metrics.json.
- Data: query_week, query_category and category_vertical in warehouse.db, covering W41 only. The shopping categories are electronics, apparel and home.
- Reconciled: not done (no dashboard or source figure was available). The naive-join figure of 40.90% differs from the de-duplicated figure by 3.93 percentage points.
- Queries and checks: the queries were run inline and not saved to a file. The check results are appended to .ds-checks.log.