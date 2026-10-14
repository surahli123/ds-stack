## Answer
Headline: 36.97 % (no interval: this is a full count, not a sample)
Shopping-vertical click-through rate in 2026-W41 was 36.97%: 39,858 clicks on 107,810 searches across 900 queries. The 36.97% figure is computed and should be checked against the dashboard before Merchandising cites it. The clicks figure is back-calculated from the rate, not read from the data.
- Observed: 36.97 % (no sampling interval; full population)
- Adjusted: not computed (single descriptive rate, nothing to adjust for)
- Causal effect: not identified (this is a descriptive level, not an effect; no comparison was asked for)

## What it means for the Merchandising citation
Cite 36.97%. A naive join of the tables gives 40.90%, which is 3.9 points too high. The two figures differ by more than any rounding, so the join method matters.

## Why we believe it
- Alternatives considered:
  - Duplicate category rows double-counting queries: ruled in as the cause of the inflated 40.90% [measured]. 250 queries have two identical category rows, reloaded 2026-10-09 with the same category, all in shopping. A plain join counts their searches twice (137,945 searches over 1,150 rows).
  - Queries moving between verticals: ruled out [measured]. Every duplicated pair has the same category and the same vertical.
  - Using the earliest versus the latest category row: no difference [measured]. Both give 36.97%.
  - Averaging per-query CTRs instead of pooling: not computed. I used clicks divided by searches, which is the standard definition [inferred].
- Checks run:
  - Weekly coverage: pass. The table holds only 2026-W41, with 2,000 unique query-week rows.
  - Data quality: pass. There are no nulls and no rows where clicks exceed searches.
  - Mapping completeness: pass. All 5 categories map to a vertical.
  - Dedup before join: pass. Each query has one category row, 900 shopping queries in total.

## Caveats, and what would change the answer
- The CTR definition is my assumption: sum of clicks divided by sum of searches. A mean of per-query rates would give a different number.
- The category assignment is a snapshot. A query's vertical in W41 may differ from the one used in other reports.
- There is no week-over-week context, because the table has only one week.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), stated here [guess]. No metrics.json was present.
- Data: query_week, query_category (deduplicated on query_id, latest loaded_at) and category_vertical, covering 2026-W41 only.
- Reconciled: not done (no dashboard or source figure available). The naive-join 40.90% versus the deduplicated 36.97% is a difference of 3.93 points [measured].
- Queries and checks: ad hoc Python/sqlite3 run in the session; not saved to a file.