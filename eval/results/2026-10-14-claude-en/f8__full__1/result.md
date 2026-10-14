## Answer
Headline: +36.97 % click-through rate (95% CI 36.68 to 37.26) [q9]
Shopping-vertical CTR in 2026-W41 was 36.97% (39,857 clicks / 107,810 searches over 900 distinct queries) [q9]. The naive join gives 40.90%, inflated by duplicated category rows [q8, check:fanout#1].
- Observed: +36.97 % (95% CI 36.68 to 37.26), a level and not a change. The interval is binomial and ignores per-query clustering, so it is somewhat optimistic. [q9]
- Adjusted: not computed (single level, no comparison period)
- Causal effect: not identified (no intervention; the question asks for a level)

## What it means for merchandising citing the figure
Cite 36.97%, not 40.90%. The 3.9 pp gap from the duplicate-row join is far larger than the ±0.3 pp interval. [q8, q9]

## Why we believe it
- Alternatives considered:
  - Duplicate category rows inflating the join: ruled in. 250 queries have two identical-category loads, so the naive join overstated shopping CTR. I deduplicated by query_id. [q6, q7, check:fanout#1] [measured]
  - Queries re-categorised between loads (ambiguous vertical): ruled out. All 250 duplicate pairs have the same category. [q7] [measured]
  - Incomplete week: not ruled out. Only W41 exists, so there is no history to compare. [q2] [measured]
- Checks run:
  - fanout: fail. The naive join added 250 rows (2250 for 2000 keys). I resolved it by deduplicating through an IN-subquery, which leaves 900 shopping queries. [check:fanout#1]
  - completeness: could not run. The data has one week and no history. [check:completeness#1]
  - mix_shift: skipped. There is no second period, so no rate change to decompose.
  - srm: skipped. This is not an experiment.

## Caveats, and what would change the answer
- There is no metrics.json, so the CTR definition is my own. If the dashboard computes CTR per query (mean of ratios), the number will differ.
- W41 completeness is unverified. A partial week would change the level.
- The interval treats searches as independent. Clustering by query would widen it.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) for queries whose category maps to vertical 'shopping' (apparel, electronics, home), deduplicated by query_id, from table query_week [stated here, guess]
- Data: query_week, query_category, category_vertical, through 2026-W41 (completeness not verifiable)
- Reconciled: not done (no dashboard or source available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (21 numbers on 7 lines; 5 queries, 2 checks, 0 given)