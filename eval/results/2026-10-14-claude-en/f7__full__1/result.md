## Answer
Headline: can't tell
The search-to-purchase rate for 2026-10-05 to 2026-10-11 can't be computed: purchases aren't in this warehouse, and the only conversion column counts add-to-cart events.
- Observed: not computed (purchases are logged only in the orders system; `conversions` is add-to-cart). The nearest proxy, add-to-cart per search, was 8.30% (no interval: proxy, not the requested metric) [q3]
- Adjusted: not computed (no purchase metric to adjust)
- Causal effect: not identified (no intervention in the question; a purchase rate needs the orders system)

## What it means for the quarterly model
Don't enter 8.30% as the purchase rate; it is add-to-cart, and purchases will be lower by an unknown amount. [q3] Finance needs the orders-system purchase count joined to the same week's searches.

## Why we believe it
- Alternatives considered:
  - `conversions` is purchases: ruled out by metrics.json, which says it counts add-to-cart events and that purchases are not in this warehouse [inferred]
  - Week incomplete: all 7 days are present [q4] [measured]
- Checks run:
  - completeness: could not run, no earlier periods in the table to compare against [check:completeness#1]
  - fanout: skipped, no joins
  - mix_shift: skipped, no rate comparison and no segments in the table
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- Table has only the 7 target days, so completeness can't be benchmarked; days look uniform at about 8.3% add-to-cart each [q2].
- Getting purchases from the orders system, with a definition of which searches count as leading to a purchase (same session? attribution window?), would settle it.

## Provenance
- Metric: search_purchase_rate, marked unavailable in metrics.json; add-to-cart per search shown only as a proxy, from metrics.json
- Data: search_daily_c, through 2026-10-11
- Reconciled: not done (no purchase source or dashboard available)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (3 numbers on 3 lines; 2 queries, 1 checks, 0 given)