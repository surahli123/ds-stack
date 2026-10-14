## Answer
Headline: 37.0 % (95% CI 36.2 to 37.8)
The click-through rate for shopping queries in 2026-W41 was 37.0%: 39,857 clicks on 107,810 searches across 900 queries. [measured]
- Observed: 37.0 % (36.2 to 37.8)
- Adjusted: not computed (single-week level, no comparison)
- Causal effect: not identified (no intervention or comparison was asked about)

## What it means for the merchandising citation
Cite about 37.0%, give or take 0.8 points. If you join without deduplicating, the figure comes out at 40.9%, which is wrong and would overstate CTR by about 3.9 points.

## Why we believe it
- Alternatives considered:
  - Duplicate category rows inflating the join: ruled in as a real problem. 250 queries were reloaded on 2026-10-09 with the same category, so a naive join double-counts them. I deduplicated on (query_id, category). [measured]
  - Queries with conflicting categories: ruled out. No query has more than one distinct category. [measured]
  - Averaging per-query CTRs instead of pooling: not used. I defined CTR as total clicks over total searches. [inferred]
- Checks run:
  - Join coverage: pass. All 2000 queries have a category, and each appears once in W41.
  - Row sanity: pass. There are no cases of clicks > searches, zero searches, or null clicks.
  - Interval: pass. It is a ratio-estimator interval clustered by query, using a normal approximation.
  - Vertical mapping: pass. Electronics, apparel and home map to shopping.

## Caveats, and what would change the answer
- I took CTR to mean clicks divided by searches, pooled. A per-query average or a click-per-impression definition would give a different number.
- Categories are as of the loads on 2026-09-01 and 2026-10-09, which are not W41 exactly. A re-categorised query would shift the result.
- There is no metrics.json in the directory, so the definition is my assumption.

## Provenance
- Metric: sum(clicks)/sum(searches), pooled over deduplicated shopping queries, stated here [guess]
- Data: query_week, query_category and category_vertical, through 2026-W41 (the only week in the table)
- Reconciled: not done (no dashboard or source figure available)
- Queries and checks: run inline in Python against warehouse.db; they were not saved to a file.