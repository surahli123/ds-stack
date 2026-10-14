## Answer
Headline: 36.97 % (95% CI 36.68 to 37.26)
Click-through rate in 2026-W41 for shopping-vertical queries was 36.97%, from 39,857 clicks on 107,810 searches across 900 queries.
- Observed: 36.97 % (36.68 to 37.26) [measured]
- Adjusted: not computed (this is a single-period level, not a comparison)
- Causal effect: not identified (this is a descriptive rate, with no intervention or comparison group)

## What it means for the merchandising citation
You can cite about 37.0% for W41. The interval is about ±0.3 points, so quote it as "about 37%" and it will hold. A decision that turns on a difference of less than 0.3 points would not be supported by this number.

## Why we believe it
- Alternatives considered:
  - Duplicate category rows double-counting queries: ruled out. `query_category` has 2,250 rows for 2,000 queries, because 250 queries were reloaded on 2026-10-09. I de-duplicated by query. All 250 reloads map to the same category as the original load (all shopping categories), so the choice of load date doesn't change the result [measured].
  - Queries missing a category: ruled out. All 2,000 W41 queries have a category [measured].
  - Averaging per-query CTRs instead of pooling: not used. I computed clicks divided by searches, summed over queries, which weights each query by its search volume. I assumed this is the intended definition [guess].
- Checks run:
  - Join fan-out: pass. There are 900 distinct shopping queries, and the original-load and latest-load results are identical.
  - `category_vertical` mapping: pass. Shopping covers electronics, apparel and home.
  - Week coverage: pass. `query_week` holds only W41, with 2,000 rows and one per query.
  - Reconciliation against a dashboard: could not run, because no dashboard figure was provided.

## Caveats, and what would change the answer
- The interval treats searches as independent binomial trials. It ignores variation between queries, so the true interval is somewhat wider.
- There is no `metrics.json`, so the CTR definition is my assumption. If "CTR" means the mean of per-query rates, the number would differ.
- Only W41 is in the data, so I can't say whether 37% is high or low relative to other weeks.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) over shopping-vertical queries, stated here [guess]. The interval is a Wald binomial interval.
- Data: `query_week`, `query_category` and `category_vertical`, through 2026-W41, the only week present.
- Reconciled: not done (no reference figure available).
- Queries and checks: run inline in ad-hoc Python/sqlite3 commands and not saved to a file. The SQL is joins on `query_id` and `category`, restricted to `vertical = 'shopping'`.