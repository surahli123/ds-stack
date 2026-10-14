## Answer
Headline: 36.97 % (95% CI 36.68 to 37.26)

The click-through rate for shopping-vertical queries in 2026-W41 was 36.97 % (39,857 clicks on 107,810 searches, across 900 queries). A naive join gives 40.9 %, which is wrong. [measured]
- Observed: 36.97 % (36.68 to 37.26)
- Adjusted: not computed (this is a single level, not a comparison)
- Causal effect: not identified (this is a descriptive rate, so there is nothing to identify)

## What it means for Merchandising's citation
Cite 36.97 %, not 40.9 %. The two differ by about 3.9 points, far more than the ±0.3 point interval. I don't know of a decision threshold smaller than that gap.

## Why we believe it
- Alternatives considered:
  - Plain join of `query_week` to `query_category`: ruled out. `query_category` has 250 queries loaded twice (2026-09-01 and 2026-10-09), so the join double-counts them and inflates the rate to 40.9 % on 137,945 searches [measured].
  - Duplicates reassigning queries to a different vertical: ruled out. None of the 2,000 queries has more than one distinct category, so the reloads are exact repeats [measured].
  - Averaging each query's own rate instead of pooling: not used. Pooled clicks over searches is the standard CTR definition [inferred].
- Checks run:
  - Key uniqueness in `query_week`: pass. There is one row per query per week, and W41 is the only week in the table.
  - Coverage: pass. All 2,000 W41 queries have a category, and no row has clicks above searches.
  - Dedup: pass. I took each query's latest `loaded_at`, which gives 900 shopping queries.
  - Interval: flag. It is a binomial approximation that ignores clustering by query, so it is somewhat too narrow.

## Caveats, and what would change the answer
- The CTR definition is assumed (clicks / searches, pooled). A different definition would change the number.
- The interval treats searches as independent. Heavy query-level variation would widen it.
- The query-to-category mapping is as of the latest load. Both loads agree, so the choice doesn't matter here.

## Provenance
- Metric: clicks / searches, summed over the vertical, stated here [guess]. There is no metrics.json in the directory.
- Data: `query_week`, `query_category` (deduped to latest `loaded_at`) and `category_vertical`, through 2026-W41.
- Reconciled: not done (no dashboard or source to compare against).
- Queries and checks: ad hoc Python/SQLite run in this session. They are not saved to a file.