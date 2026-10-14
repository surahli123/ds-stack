## Answer
Headline: 8.30 % of searches led to a purchase (95% CI 8.24 to 8.36)

In 2026-10-05 to 2026-10-11, 70,030 of 843,738 searches ended in a conversion, which is 8.30%.
- Observed: 8.30 % (8.24 to 8.36), a binomial interval treating searches as independent
- Adjusted: not computed (single descriptive rate, nothing to adjust for)
- Causal effect: not identified (this is a level, not a comparison, so there is no effect to estimate)

## What it means for the quarterly model
Use about 8.3% for this week. The interval is ±0.06 pp, but it only covers sampling noise. Whether one week represents the quarter is a bigger question, because the table has no other weeks. A change smaller than the roughly 0.1 pp precision won't matter, and a seasonal shift would.

## Why we believe it
- Alternatives considered:
  - Purchase counted per click rather than per search: ruled out, because the question asks per search. Conversions per click is 26.7% [measured].
  - Searches with multiple conversions, or conversions that can't be tied to a search, inflating the rate: not ruled out, because the table has no session-level detail [guess].
- Checks run:
  - Completeness: pass. All 7 days are present, with no gaps or duplicates.
  - Daily stability: flag. The daily rate is 8.2996% to 8.3002%, with a standard deviation of 0.0002 pp. Binomial noise alone would give about 0.08 pp. That is implausibly smooth, so the data may be modelled, allocated or pre-processed rather than raw events.
  - Reconciliation to a dashboard: could not run, because no other source is available.

## Caveats, and what would change the answer
- The table is called `search_daily_c`, and I don't know what the "c" means. It could be a cleaned, capped or cohort subset, not all traffic.
- The interval is probably too narrow, because the daily smoothness suggests the data isn't independent events.
- Only this one week is in the table, so there is no trend or seasonality context.
- If conversions are attributed with a lag, the most recent days could be undercounted. The days look uniform, so I don't see this in the data.

## Provenance
- Metric: conversions / searches, summed over the week. This is stated here [guess], because there is no metrics.json.
- Data: `search_daily_c` in warehouse.db, through 2026-10-11, which is the last day in the table.
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: ran inline in Python against warehouse.db. They are not saved to a file.