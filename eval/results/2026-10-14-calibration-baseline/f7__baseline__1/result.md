## Answer
Headline: can't tell. Purchases aren't logged in this warehouse, so the purchase rate can't be computed.

The closest available figure is add-to-cart, which was 8.30% of searches (70,030 of 843,738) in the week of 2026-10-05 to 2026-10-11. It is an upper-bound proxy for purchase, not the purchase rate.

- Observed: +8.30 % of searches ended in an add-to-cart in the same session (95% CI 8.24 to 8.36, binomial). This is the add-to-cart rate, not purchase.
- Adjusted: not computed (the question is descriptive and nothing needs adjusting)
- Causal effect: not identified (this is a single-week rate, with no intervention to compare)

## What it means for the quarterly model
Don't enter 8.30% as the search-to-purchase rate. Every purchase should be preceded by an add-to-cart, so the true rate is at most about 8.3%. Cart-to-purchase conversion is unknown and typically well below 100%. Finance needs purchase or order events joined to searches to get the real number. The proxy's interval of ±0.06 points is negligible next to that gap.

## Why we believe it
- Alternatives considered:
  - Treat add-to-cart as purchase: ruled out. column_notes says "purchases are not logged in this warehouse" [measured].
  - Clicks as the numerator: ruled out. A click is further from purchase than add-to-cart [inferred].
  - Cart abandonment is small, so the proxy is close to the real rate: not supported by any data here [guess].
- Checks run:
  - Coverage: pass. All 7 days of the week are present, one row per day, and the table ends on 10-11.
  - Reconciliation to a dashboard: could not run. No other source was available.
  - Daily stability: skipped. I did not compute a daily series. The binomial interval also treats searches as independent, which is optimistic.

## Caveats, and what would change the answer
- A purchase or orders table joined to search sessions would give the real figure.
- Searches here are those "with at least one result shown", so zero-result searches are excluded from the denominator. Finance's definition may differ.
- The add-to-cart events are counted within the same session as the search. Whether they are deduplicated per search is unknown.

## Provenance
- Metric: add-to-cart conversions ÷ searches (a proxy). No metrics.json was present, so this definition is stated here [guess].
- Data: search_daily_c and column_notes, through 2026-10-11.
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: ad hoc Python sqlite3 calls in this session. Nothing is saved to a file.