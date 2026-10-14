I've got the number and the checks done, so I'm writing the readout now.

## Answer
Headline: 36.97 % (95% CI 36.68 to 37.26)
Shopping-vertical click-through in 2026-W41 was 36.97% (39,857 clicks on 107,810 searches, 900 queries).
- Observed: 36.97 % (36.68 to 37.26), measured. This is total clicks divided by total searches, after deduplicating the category table.
- Adjusted: not computed (single week and nothing to adjust for)
- Causal effect: not identified (this is a level for one week, not a comparison; there is nothing to estimate causally)

## What it means for merchandising's citation
Cite about 37.0%. The interval is ±0.3 points. A figure of roughly 40.9% would come out if the category duplicates were left in, so the dedupe moves the number by about 4 points.

## Why we believe it
- Alternatives considered:
  - Joining the raw category table gives 40.9% (56,422 / 137,945): ruled out. `query_category` has 2,250 rows for 2,000 queries, so the join double-counts 250 queries [measured].
  - Duplicates that assign a query to different categories: ruled out. Every duplicated query has the same category in each row, so `distinct (query_id, category)` gives exactly 2,000 rows [measured].
  - Queries without a category or vertical mapping: ruled out. All 2,000 queries have a category, and every category maps to a vertical [measured].
  - Averaging per-query rates instead of pooling: not used. The metric is pooled clicks over searches [inferred].
- Checks run:
  - fanout, on the raw join: fail. It added 250 duplicate-key rows (`fanout#2`).
  - fanout, on the deduplicated join: pass. 2,000 rows in and 2,000 out (`fanout#1`). The 900 shopping queries come from the deduplicated join, not from this check.
  - completeness: could not run. The data holds only W41, and the check needs at least 3 prior periods. W41 (Oct 5–11) has ended and the latest category load is Oct 9, so I infer it is complete. [inferred]
  - mix_shift and srm: skipped. There is no comparison period and no experiment.

## Caveats, and what would change the answer
- The interval is a binomial approximation. It treats searches as independent, so it is probably a little too narrow because clicks cluster within queries.
- A query's category is whatever `query_category` holds. I did not check whether the latest load differs from earlier ones (duplicates were identical).
- There is no `metrics.json`. I defined CTR as clicks/searches myself. If merchandising uses a different definition, such as unique-click or per-session CTR, the figure would differ.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), stated here [guess]. There is no `metrics.json`.
- Data: `query_week`, `query_category` (deduplicated), `category_vertical`, W41 only, assumed complete.
- Reconciled: not done (no dashboard or reference figure available)
- Queries and checks: the SQL was run inline and not saved to a file. The check results are in `.ds-checks.log` (`fanout#1`, `fanout#2`, `completeness#1`).