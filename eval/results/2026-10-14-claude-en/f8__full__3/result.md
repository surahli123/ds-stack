## Answer
Headline: +36.97 % click-through rate (36.68 to 37.26) [q7]
Shopping-vertical CTR in 2026-W41 was 36.97%: 39,857 clicks on 107,810 searches across 900 queries. [q7] (measured)
- Observed: +36.97 % (36.68 to 37.26) [q7] (measured)
- Adjusted: not computed (single week, no comparison asked)
- Causal effect: not identified (this is a level for one week, not a change, so there is nothing to attribute)

## What it means for merchandising's citation
The figure is a one-week level with a binomial interval of about ±0.29 pp, which treats searches as independent. [q7] No decision threshold was given, so I can't say whether the interval matters for the decision. [given]

## Why we believe it
- Alternatives considered:
  - Join fan-out inflating the number: ruled out. `query_category` has 250 duplicate rows (queries reloaded on 2026-10-09 with the same category), so a naive join returns 2,250 rows and 269,375 searches. I deduplicated to 2,000 rows. [q3, q5, q8, q9] [measured]
  - Queries mapped to more than one category: ruled out, 0 such queries. [q6] [measured]
  - A different definition of "shopping": the vertical named "shopping" in `category_vertical` covers apparel, electronics and home. [q7] [inferred]
- Checks run:
  - fanout (raw join): fail, 250 extra rows from the duplicate category rows. [check:fanout#1]
  - fanout (deduplicated join): pass, 2,000 rows in and 2,000 out. [check:fanout#2]
  - completeness: could not run, because the table holds only one week and gives no history to compare against. [check:completeness#1]

## Caveats, and what would change the answer
- There is no `metrics.json`, so the CTR definition is my own. A click-per-session or unique-click definition would give a different number.
- I couldn't verify that W41 is fully loaded. A partial load would change the level.
- The interval ignores clustering by query, so the true interval is somewhat wider.
- I didn't reconcile the number against a dashboard.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) over `query_week` for W41, restricted to the shopping vertical via deduplicated `query_category` and `category_vertical`, stated here [guess]
- Data: `query_week`, `query_category`, `category_vertical`, through 2026-W41
- Reconciled: not done (no dashboard or reference figure available)
- Queries and checks: `.ds-queries.log` and `.ds-checks.log`
- Verified: verify_readout: pass (18 numbers on 8 lines; 6 queries, 3 checks, 1 given)