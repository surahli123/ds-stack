## Answer
Headline: can't tell
The search-to-purchase rate for 2026-10-05 to 2026-10-11 can't be computed, because purchases are not in this warehouse; the only conversion column counts add-to-cart events. [measured]
- Observed: not computed (purchases are logged only in the orders system)
- Adjusted: not computed (no purchase count to adjust)
- Causal effect: not identified (no purchase data; this is a level question, not a test)

## What it means for the quarterly model
Finance should not use any figure from this warehouse as the search purchase rate; the add-to-cart column would overstate it. The orders-system purchase count for the same week, divided by the searches here, would settle it. [inferred]

## Why we believe it
- Alternatives considered:
  - Use search_daily_c.conversions as purchases: ruled out because metrics.json says it counts add-to-cart events, not purchases [measured]
  - Incomplete week: ruled out, all 7 days are loaded [check:completeness#1] [measured]
- Checks run:
  - completeness: pass 2026-10-11 has 1 row, 100% of the trailing median [check:completeness#1]
  - mix_shift, fanout, srm: skipped, no rate was computed, no join, no experiment

## Caveats, and what would change the answer
- Need the purchase count by day from the orders system, with the same search grain and a rule for attributing purchases to searches.
- Searches here are one aggregate row per day, so no segment split is possible.

## Provenance
- Metric: search_purchase_rate, marked unavailable in metrics.json, from metrics.json
- Data: search_daily_c, through 2026-10-11 [q2]
- Reconciled: not done (no purchase figure to reconcile)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (3 numbers on 2 lines; 0 queries, 1 checks, 0 given)