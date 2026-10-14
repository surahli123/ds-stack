## Answer
Headline: 55.0 % (54.6 to 55.4) [q5]
Navigational queries had a click-through rate of 55.0% in 2026-W40 (32,878 clicks on 59,800 searches), using each query's current label. [q5]
- Observed: 55.0 % (54.6 to 55.4) [q5]
- Adjusted: not computed (single week, no comparison, no change to decompose)
- Causal effect: not identified (this is a level, not an effect of anything)

## What it means for the marketing planning doc
Use about 55% for navigational CTR; the interval is under half a point wide, so it only matters if the plan hinges on differences under 0.4 pp. [q5] Navigational CTR is about 30 pp above informational (25.0%). [q5]

## Why we believe it
- Alternatives considered:
  - Join fan-out from historical label rows (1,300 rows if all label versions are joined vs 1,000 queries): ruled out by filtering is_current=1, which gives exactly one label per query [q4, q7] [measured]
  - Label version mix (v1 vs v2 labels give different navigational sets): ruled out as a driver of the level, since v1 labels are 300 queries and v2 labels 100 in current navigational, both at the same CTR (55.0%) [q6] [measured]
  - Zero-search or clicks>searches rows distorting the rate: ruled out, none exist [q8] [measured]
  - Seasonality / day of week: not testable, only one week in the table [q3] [measured]
- Checks run:
  - fanout: pass row counts consistent with a many_to_one left join [check:fanout#2]
  - completeness: could not run, only one week of history so no baseline [check:completeness#2]
  - mix_shift: skipped, no second period to compare

## Caveats, and what would change the answer
- Interval treats searches as independent; clicks cluster by query, so the true interval is somewhat wider. Query-level bootstrap would settle it.
- Completeness of W40 can't be verified against earlier weeks; if the week is partially loaded the figure could shift.
- Definition is CTR = clicks / searches (search-weighted), not the mean of per-query CTRs; the latter would differ.
- "Current" label is is_current=1; if marketing means the labels as of an earlier version, the set of navigational queries differs.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) over queries with current intent = navigational, week 2026-W40, from query_stats joined to query_labels on query_id with is_current=1; stated here [guess] (no metrics.json)
- Data: query_stats, query_labels, through 2026-W40
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (19 numbers on 6 lines; 6 queries, 2 checks, 0 given)