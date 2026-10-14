## Answer
Headline: 8.30 % of searches led to a purchase (95% CI 8.24 to 8.36)
In 2026-10-05 to 2026-10-11, 70,030 conversions came from 843,738 searches, which is 8.30%.
- Observed: 8.30 % (8.24 to 8.36)
- Adjusted: not computed (this is a level, not a comparison, so there is nothing to adjust)
- Causal effect: not identified (this is a descriptive rate; no intervention is being evaluated)

## What it means for the quarterly model
Use 8.3% as the one-week conversion rate per search. The interval is about ±0.06 points wide, but it only reflects sampling noise. The real uncertainty is whether one week represents the quarter, and that depends on seasonality.

## Why we believe it
- Alternatives considered:
  - Different definition (a purchase counted per click, or per unique user): ruled out, because the table only has search-level counts, so the metric is conversions divided by searches [inferred]
  - Incomplete week: ruled out, because all 7 days are present and the table ends 2026-10-11 [measured]
  - Day-level anomalies: ruled out, because the daily rate is 8.30% every day, from 8.2997% to 8.3002% [measured]
- Checks run:
  - Row coverage: pass. 7 distinct dates, one row each, with no gaps.
  - Daily consistency: flag. The daily rates are almost identical, with a spread of about 0.0003 points. Binomial noise alone would give about ±0.08 points per day, so this is much steadier than real traffic. The data may be synthetic, modeled, or allocated from a weekly total.
  - Interval: pass. It is a binomial (Wald) interval on the pooled counts. It assumes independent searches, which understates the width if searches cluster by user.

## Caveats, and what would change the answer
- The very flat daily rate suggests the table may not be raw events. If conversions are allocated or modeled upstream, the true rate could differ.
- "Conversion" is not defined here. I assumed the `conversions` column means a purchase, and no `metrics.json` was available to confirm it.
- Whether conversions are attributed to the search day or to the purchase day is unknown. This could shift the rate slightly near the week's edges.
- The table is named `search_daily_c`. I did not check whether other versions exist or whether bots or internal traffic are filtered out.
- This is a single week, so it says nothing about the rate for the quarter.

## Provenance
- Metric: sum(conversions) / sum(searches) [guess: the definition was assumed, no metrics.json]
- Data: `search_daily_c`, through 2026-10-11
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: run inline with Python and sqlite3. They are not saved to a file.