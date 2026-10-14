## Answer
Headline: 8.30 % (95% interval 8.24 to 8.36 %)
In 2026-10-05 to 2026-10-11, 70,030 of 843,738 searches led to a purchase, which is 8.30%.
- Observed: 8.30 % (8.24 to 8.36 %)
- Adjusted: not computed (this is a single-week level, not a comparison, so there is nothing to adjust)
- Causal effect: not identified (this is a descriptive rate. Identifying an effect would need a randomized or comparison design.)

## What it means for the quarterly model
Use about 8.3% as the base conversion rate for this week. The interval is only ±0.06 points wide, so sampling noise won't move the model. The risk is whether one week represents the quarter, and I have no data on that.

## Why we believe it
- Alternatives considered:
  - Incomplete week or late-loading days: ruled out by all 7 days being present with similar volumes (115k–125k searches per day) [measured]
  - Different definition of "led to a purchase" (for example, a click-then-purchase funnel, or user-level conversion): not ruled out. I used conversions divided by searches [inferred]
- Checks run:
  - completeness: pass. 2026-10-11 has 123,422 rows, which is 103% of the median of the other days.
  - fanout, mix_shift and srm: skipped. There were no joins, no comparison between periods, and no experiment.

## Caveats, and what would change the answer
- The interval is a binomial interval that treats each search as independent. Repeat searches by the same user would widen it, and I can't measure that from daily aggregates.
- The table `search_daily_c` is pre-aggregated. I can't check whether `conversions` counts purchases or something else, such as attributed or same-session conversions.
- If Finance defines conversion differently, such as purchasers per searcher, the number changes.
- Every day in the week is within a narrow range, but this is one week only. Seasonality across the quarter is not covered.

## Provenance
- Metric: conversions ÷ searches, summed over the week, stated here [guess]. There is no metrics.json in the directory.
- Data: `search_daily_c` (date, searches, clicks, conversions), through 2026-10-11.
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: the queries were run inline and not logged. The check result is in `.ds-checks.log` as completeness#1.