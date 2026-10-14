## Answer
Headline: 36.97 % (no interval: this is a full-population rate, not a sample estimate)
Click-through rate for shopping-vertical queries in 2026-W41 was 36.97% (39,857 clicks / 107,810 searches, 900 queries).
- Observed: 36.97 % (no interval; complete count)
- Adjusted: not computed (no comparison or confounder in the question)
- Causal effect: not identified (descriptive question, no intervention)

## What it means for the merchandising citation
Cite about 37.0%. The naive join gives 40.90%, which is wrong. No decision threshold was given, so I can't compare an interval to a minimum meaningful change.

## Why we believe it
- Alternatives considered:
  - Naive join of query_category: ruled out. 250 queries were loaded twice (2026-09-01 and 2026-10-09) with identical categories, which double-counts them. It inflates shopping to 1,150 rows and 40.90% [measured].
  - Queries with conflicting categories: ruled out. Reloaded rows agree, and each query maps to exactly one category after dedupe [measured].
  - Unmapped categories: ruled out. All 5 categories map to a vertical [measured].
- Checks run:
  - fanout (raw join): fail. Right side has 250 duplicate-key rows, so the join added rows. I fixed this by deduping on (query_id, category).
  - fanout (deduped): pass. 2000 rows in, 2000 out.
  - completeness: could not run. The table holds only W41 and no prior weeks, so there is no history to compare against. The last category load was 2026-10-09, so W41 may be partial if the week ended 10-11 [guess].
  - srm, mix_shift: not applicable (no experiment, no comparison).

## Caveats, and what would change the answer
- Completeness of W41 is unverified. A partial week would change the numerator and denominator.
- The CTR is clicks/searches pooled across queries (searches-weighted), not a mean of per-query CTRs.
- The category is the latest load, but reloads were identical, so no query changed category.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches), stated here [guess]. There is no metrics.json.
- Data: query_week, query_category (deduped), category_vertical; W41 only.
- Reconciled: not done (no dashboard or source available).
- Queries and checks: checks logged in .ds-checks.log; the SQL was run inline and not saved.