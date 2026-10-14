## Answer
Headline: can't tell
The warehouse doesn't log purchases, so I can't give the share of searches that led to a purchase. The closest thing it has is add-to-cart, and that was 8.30% of searches in the week.
- Observed: +8.30 % of searches with an add-to-cart in the same session (95% CI 8.24 to 8.35, treating each search as independent) [measured]. This is add-to-cart, not purchase.
- Adjusted: not computed (no purchase data, and nothing to adjust for)
- Causal effect: not identified (this is a descriptive rate, and no intervention is involved)

## What it means for the quarterly model
Don't enter 8.3% as a purchase rate. Add-to-cart is an upper bound on purchases [inferred], because some carts are abandoned. The true purchase share is lower by an unknown amount. Finance needs the cart-to-purchase rate, or order data joined to search sessions, before the model can use this number.

## Why we believe it
- Alternatives considered:
  - Treat `conversions` as purchases: ruled out by `column_notes`, which says "add-to-cart events in the same session as the search; purchases are not logged in this warehouse" [measured]
  - Apply a typical cart-to-purchase rate to get a purchase share: ruled out because any such rate would be made up and I have no data for it [guess]
- Checks run:
  - Schema and notes review: pass. There is one table, `search_daily_c`, with 7 daily rows covering 2026-10-05 to 2026-10-11.
  - Daily stability: pass. The daily add-to-cart rate stays in a narrow band around 8.3%.
  - Reconciliation to a dashboard: could not run (no source provided).

## Caveats, and what would change the answer
- The interval ignores clustering by session or user, and conversions may count several add-to-cart events per session, so the real interval is wider.
- "Searches" counts only searches that showed at least one result.
- Purchase data (orders joined to sessions) would let me compute the real figure.

## Provenance
- Metric: add-to-cart conversions ÷ searches, stated here [guess]. No metrics.json was present.
- Data: `search_daily_c` and `column_notes`, through 2026-10-11 (the week is complete).
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: run inline in this session and not saved to a file. The weekly total is 70,030 add-to-carts over 843,738 searches.