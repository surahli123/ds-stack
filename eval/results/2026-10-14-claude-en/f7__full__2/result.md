```
## Answer
Headline: can't tell
The search-to-purchase rate for 2026-10-05 to 2026-10-11 can't be computed here, because purchases are logged only in the orders system, which this warehouse doesn't hold.
- Observed: not computed (no purchase data; `conversions` in search_daily_c is add-to-cart, which was 8.30% of searches that week, not purchases) [q3]
- Adjusted: not computed (no purchase data)
- Causal effect: not identified (no intervention in question; this is a descriptive rate)

## What it means for the quarterly model
Don't put 8.30% into the model as a purchase rate: it is add-to-cart, and the purchase share is lower by an unknown amount [q3]. Finance needs the orders-system purchase count joined to the same 7 days of searches (843,738) [q3].

## Why we believe it
- Alternatives considered:
  - Use `conversions` as purchases: ruled out because metrics.json says it counts add-to-cart events, not purchases [q3] [measured]
  - Incomplete week: ruled out, last day has full row count [check:completeness#1] [measured]
- Checks run:
  - completeness: pass 2026-10-11 has 100% of trailing median rows [check:completeness#1]
  - fanout: skipped, no joins
  - mix_shift: skipped, no rate comparison
  - srm: skipped, no experiment

## Caveats, and what would change the answer
- Purchase counts from the orders system for 2026-10-05 to 2026-10-11 would settle it; the rate would be purchases divided by the 843,738 searches [q3].
- Add-to-cart to purchase drop-off is unknown, so no scaling of 8.30% is valid [q3].

## Provenance
- Metric: search_purchase_rate, marked available: false in metrics.json (numerator purchases from orders system, not in warehouse), from metrics.json
- Data: search_daily_c, through 2026-10-11
- Reconciled: not done (no purchase figure available to reconcile)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (5 numbers on 3 lines; 1 queries, 1 checks, 0 given)
```