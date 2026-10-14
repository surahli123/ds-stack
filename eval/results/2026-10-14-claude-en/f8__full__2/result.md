## Answer
Headline: 36.97 % (36.68 to 37.26) [q9]
Shopping-vertical click-through rate in 2026-W41 is 36.97% (39,857 clicks on 107,810 searches across 900 queries), after removing duplicate category rows that would otherwise inflate it to 40.90%. [q9, q10]
- Observed: 36.97 % (36.68 to 37.26) [q9]
- Adjusted: not computed (single week, no comparison)
- Causal effect: not identified (this is a level, not a change; no intervention to attribute)

## What it means for merchandising's citation
Cite 36.97%; the naive join figure of 40.90% is wrong by about 3.9 pp because of duplicated category rows. [q9, q10] No decision threshold was given, so the interval is only a precision statement.

## Why we believe it
- Alternatives considered:
  - Duplicate category rows inflating the rate: ruled in; 250 shopping queries have two identical-category rows, and deduplicating moves the rate from 40.90% to 36.97% [q6, q7, q9, q10] [measured]
  - Queries mapped to multiple categories: ruled out; every duplicated query has one distinct category [q6] [measured]
  - Unmapped or missing queries: ruled out; all 900 shopping queries have a W41 row [q11] [measured]
  - Clicks exceeding searches (bad logging): ruled out; zero rows [q8] [measured]
  - Mix-shift, seasonality, day of week: not applicable, since no comparison period exists in the data [inferred]
- Checks run:
  - fanout (naive join): fail, join added 250 rows, 1150 rows for 900 keys [check:fanout#1]
  - fanout (deduplicated join): pass, 900 rows for 900 queries [check:fanout#2]
  - completeness: could not run, only one week in the table, so no history to compare [check:completeness#1]
  - mix_shift: skipped, no second period
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- Only W41 is in query_week and no earlier weeks exist, so completeness is unverified; a partially loaded week would change the rate. Row counts per week from earlier weeks would settle it.
- Duplicates are in query_category (loaded_at 2026-09-01 to 2026-10-09); I assumed they are accidental reloads and not reclassifications. They are identical in category, so the result holds either way.
- Rate is pooled clicks over searches (search-weighted), not the mean of per-query rates.
- The interval is a binomial approximation that treats searches as independent; clustering by query would widen it.
- No metrics.json and no dashboard to reconcile against.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) for queries whose category maps to vertical 'shopping', week 2026-W41, from query_week joined to deduplicated query_category and category_vertical [guess]
- Data: query_week, query_category, category_vertical, through 2026-W41 (completeness unverified)
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (23 numbers on 8 lines; 6 queries, 3 checks, 0 given)