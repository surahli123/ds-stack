## Answer
Headline: 55.0 % (95% CI 54.9 to 55.0)
Navigational queries had a click-through rate of 55.0% in 2026-W40: 32,878 clicks on 59,800 searches across 400 queries.
- Observed: 55.0 % (54.9 to 55.0), clicks ÷ searches over queries whose current label is navigational
- Adjusted: not computed (this is a descriptive rate, not a comparison)
- Causal effect: not identified (this is a single-week level, not an effect, so there is nothing to identify)

## What it means for the marketing planning doc
Use about 55%. The interval is only about 0.1 points wide, so sampling noise won't change any planning figure. The label definition matters far more than sampling noise: an alternative label choice moves the number by 10 points or more (see below).

## Why we believe it
- Alternatives considered:
  - Joining all label versions: ruled out. `query_labels` holds several rows per query (1,300 rows for 1,000 queries), so a plain join double-counts and gives 45.0% [measured].
  - Using only the original (version 1) navigational labels: ruled out. That gives 43.0%, but those labels include ones that have since been superseded [measured].
  - Missing or duplicate current labels: ruled out. Every query has exactly one `is_current=1` label [measured].
- Checks run:
  - Label uniqueness: pass. 1,000 queries in W40, each with one current label.
  - Data sanity: pass. There are no nulls and no rows where clicks exceed searches.
  - Interval: pass. A query-level bootstrap with 2,000 resamples gave 54.9 to 55.0. The interval is narrow, which assumes queries are independent [inferred].
  - Reconciliation to a dashboard: could not run, because no dashboard figure is available.

## Caveats, and what would change the answer
- The number depends on the "current" label snapshot. If marketing uses an older labeling, the figure differs (43% with version 1 labels).
- "CTR" here is pooled clicks ÷ searches. An average of per-query CTRs would differ slightly.
- The data covers W40 only, so there is no trend or comparison.

## Provenance
- Metric: CTR = sum(clicks) ÷ sum(searches), filtered to `intent='navigational'` and `is_current=1`. Stated here [guess]; there is no metrics.json.
- Data: `query_stats` joined to `query_labels`, for 2026-W40 (the only week in the table).
- Reconciled: not done (no dashboard or source figure to compare against).
- Queries and checks: ran inline in Python against warehouse.db. They are not saved to a file.