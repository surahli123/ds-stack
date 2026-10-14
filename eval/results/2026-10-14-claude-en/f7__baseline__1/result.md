```
## Answer
Headline: 8.30 % of searches led to a purchase (95% CI 8.24 to 8.36)
In 2026-10-05 to 2026-10-11, 70,030 conversions came from 843,738 searches, which is 8.30%.
- Observed: 8.30 % (8.24 to 8.36), binomial interval on pooled counts
- Adjusted: not computed (this is a level, not a comparison, so there is nothing to adjust for)
- Causal effect: not identified (this is a descriptive rate, and no causal question was asked)

## What it means for the quarterly model
Use 8.3% as the one-week conversion rate. The interval is about ±0.06 points wide, but it covers sampling noise only. Finance should decide whether one week is enough to represent the quarter, since the data can't show that.

## Why we believe it
- Alternatives considered:
  - Conversions counted per click instead of per search: ruled out. The question asks about searches, so the denominator is searches. Clicks-to-purchase would be about 27%. [measured]
  - A different definition of "led to a purchase", such as session-level or attributed within a window: not ruled out. The table has no session or attribution fields. [inferred]
  - Duplicate or missing days: ruled out. There are 7 distinct dates, one per day, with no gaps. [measured]
- Checks run:
  - Completeness: pass. The table holds exactly the 7 days of the target week and nothing else.
  - Day-to-day stability: flag. The daily rate is 8.2997 to 8.3002% every day, which is unusually constant for real traffic. That points to synthetic or modelled data, or a pipeline that applies a fixed rate. The binomial interval is therefore probably conservative, since day-to-day variation is far smaller than it implies.
  - Cross-check against a source system: could not run. No other source is available.

## Caveats, and what would change the answer
- The table is named `search_daily_c`, and I don't know what the "_c" suffix means (for example, cleaned or a copy). If conversions are attributed differently upstream, the figure changes.
- The near-constant daily rate suggests the data may not be raw event counts. Confirm the source with the data owner before finance relies on it.
- A single week may not reflect seasonality across the quarter.

## Provenance
- Metric: conversions ÷ searches, summed over the week (ratio of totals). Stated here [guess]. No metrics.json was present.
- Data: `search_daily_c` in warehouse.db, 2026-10-05 to 2026-10-11, all 7 days complete.
- Reconciled: not done (no dashboard or second source available)
- Queries and checks: ad hoc Python/sqlite3 run inline in this session. No log file was saved.
```