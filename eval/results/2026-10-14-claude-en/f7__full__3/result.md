## Answer
Headline: can't tell
The search-to-purchase rate for 2026-10-05 to 2026-10-11 can't be computed, because purchases are logged only in the orders system and this warehouse doesn't hold it. [measured]
- Observed: not computed (no purchase data in the warehouse; `search_daily_c.conversions` counts add-to-cart events, not purchases)
- Adjusted: not computed (no purchase metric to adjust)
- Causal effect: not identified (this isn't a causal question; a weekly purchase count from the orders system, matched to searches, would be needed first)

## What it means for the quarterly model
Don't put the add-to-cart rate of 8.30% [q3] into the model as a purchase rate. Purchases can't exceed add-to-cart events, so it would overstate the true rate. Finance needs the weekly purchase count from the orders system.

## Why we believe it
- Alternatives considered:
  - Use `conversions` as purchases: ruled out because `metrics.json` says `conversions` are add-to-cart events [q2] [measured]
  - Incomplete week: ruled out, all 7 days are present and the last day is at normal volume [check:completeness#1] [measured]
- Checks run:
  - completeness: pass. 2026-10-11 has 103% of the trailing median rows [check:completeness#1]
  - fanout: skipped, no joins
  - mix_shift: skipped, no rate comparison across periods
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- A weekly purchase count from the orders system, matched to the same search population, would settle it.
- The drop-off from add-to-cart to purchase is unknown, so the proxy can't be converted into a purchase rate.

## Provenance
- Metric: search_purchase_rate = purchases / searches, marked unavailable in `metrics.json`
- Data: `search_daily_c`, through 2026-10-11
- Reconciled: not done (no purchase source to reconcile against)
- Queries and checks: `.ds-queries.log` and `.ds-checks.log`
- Verified: verify_readout: pass (3 numbers on 3 lines; 2 queries, 1 checks, 0 given)