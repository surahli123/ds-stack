```
## Answer
Headline: 55.0 % click-through rate for navigational queries in 2026-W40 (95% CI 54.6 to 55.4) [q6]
Clicks divided by searches for navigational queries, using each query's current label, was 32,878 clicks on 59,800 searches across 400 queries [q6]. The interval is a binomial approximation on searches, so it is probably slightly narrow [q6].

## What it means for the marketing planning doc
No decision threshold was given, so the interval of 54.6 to 55.4 cannot be compared with one [q6]. Joining all label versions instead of only the current one gives 43.0%, which is wrong because of duplicated labels [q7, check:fanout#2].

## Why we believe it
- Alternatives considered:
  - Joining every label row (old and current versions): ruled out because 100 navigational queries have a stale label as well as a current one, which inflates the join to 600 queries and pulls CTR down to 43.0% [q7, q2] [measured]
  - Label version 1 vs 2 giving different CTR: ruled out because the current-label CTRs are 55.0% and 55.0% for the two versions [q5] [measured]
  - Seasonality, day of week, mix-shift: not testable, only one week exists in the table and nothing is being compared across periods [q3] [inferred]
- Checks run:
  - fanout (current-label join): pass, 1000 rows in and 1000 out [check:fanout#1]
  - fanout (all-label join): fail, adds 300 rows, which is why is_current=1 is required [check:fanout#2]
  - completeness: could not run, no earlier weeks to compare against [check:completeness#1]
  - mix_shift: skipped, no before/after comparison is being made

## Caveats, and what would change the answer
- Only W40 is loaded, so completeness is unverified. A partially loaded week would change the number; settle it with prior weeks' row counts.
- Metric definition is my guess (no metrics.json). A per-search-session CTR or a query-averaged CTR would give a different value.
- The interval ignores variation between queries, so the true interval is wider; a cluster-by-query interval would settle it.
- Label quality is unaudited; label_version 2 relabels a subset of queries.

## Provenance
- Metric: sum(clicks)/sum(searches) for queries whose current label (is_current=1) is navigational, week 2026-W40, from query_stats joined to query_labels on query_id, stated here [guess]
- Data: query_stats, query_labels, through 2026-W40 (completeness not verifiable)
- Reconciled: not done (no dashboard or source figure available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (20 numbers on 7 lines; 5 queries, 3 checks, 0 given)
```