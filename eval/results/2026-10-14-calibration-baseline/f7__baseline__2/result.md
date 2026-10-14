## Answer
Headline: can't tell
The warehouse doesn't log purchases, so the search-to-purchase rate can't be computed. The closest thing it has is search-to-add-to-cart, which was 8.30% for the week.
- Observed: not a purchase rate. Add-to-cart per search was 8.30% (70,030 / 843,738), with no interval. [measured]
- Adjusted: not computed (no purchase data, and nothing to adjust)
- Causal effect: not identified (this is a descriptive rate, with no intervention or comparison)

## What it means for the quarterly model
I can't give Finance a purchase-conversion input from this data. The 8.30% add-to-cart rate is an upper bound on the purchase rate only if every purchase is preceded by an add-to-cart in the same session as the search. Even then, the real rate is lower by the share of carts that are abandoned, and that share is unknown. Don't enter 8.30% as a purchase rate.

## Why we believe it
- Alternatives considered:
  - Treat `conversions` as purchases: ruled out because `column_notes` defines it as "add-to-cart events in the same session as the search; purchases are not logged in this warehouse" [measured]
  - Apply a typical cart-to-purchase ratio: ruled out because I have no data for it and any ratio would be a guess [guess]
- Checks run:
  - Schema and column notes: pass. The only data table is `search_daily_c` (7 daily rows, 2026-10-05 to 2026-10-11), and no purchase or order table exists.
  - Date coverage: pass. All 7 days are present.
  - Daily stability: pass. Daily add-to-cart per search ran about 8.2–8.4%, which I eyeballed from the daily rows. No outlier days.
  - Metric definition: flag. There is no `metrics.json`, so no official definition of "purchase" to check against.
  - Interval: could not run. There are only daily aggregates, with no session-level data to base an interval on.

## Caveats, and what would change the answer
- A table of orders or purchases, joined to sessions or searches, would give the real rate. Ask the data owner whether one exists outside this warehouse.
- Searches here are "with at least one result shown", so zero-result searches are excluded. A different denominator would change the rate.
- Conversions are same-session only, so purchases made later would be missed even with purchase data.

## Provenance
- Metric: conversions ÷ searches (add-to-cart per search), a stand-in for purchase rate. The definition is stated here [guess]; no metrics.json was found.
- Data: `search_daily_c` and `column_notes`, through 2026-10-11.
- Reconciled: not done (no dashboard or other source provided)
- Queries and checks: ad-hoc Python/sqlite3 queries run in this session. They were not saved to a file.