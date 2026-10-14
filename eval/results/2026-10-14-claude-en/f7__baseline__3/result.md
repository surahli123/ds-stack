## Answer
Headline: 8.30 % of searches led to a purchase (95% CI 8.24 to 8.36)
In the week of 2026-10-05 to 2026-10-11, 70,030 of 843,738 searches ended in a conversion, which is 8.30%.
- Observed: 8.30 % (8.24 to 8.36), a binomial interval that treats each search as independent
- Adjusted: not computed (this is a level, not a comparison, so there is nothing to adjust for)
- Causal effect: not identified (this is a descriptive rate, and no causal question was asked)

## What it means for the quarterly model
Use 8.30% for this week. The interval is about ±0.06 points, so it only matters if the model is sensitive to changes smaller than that. One week doesn't show whether the rate holds across the quarter.

## Why we believe it
- Alternatives considered:
  - Purchase counted per search session or per user instead of per search event: not ruled out. The table only has daily counts, so I can't test it. [inferred]
  - Conversions that aren't tied to a search in the same day: not ruled out. The table doesn't link conversions to individual searches. [guess]
- Checks run:
  - Completeness: pass. All 7 days are present with no gaps or duplicates, and the table contains only this week.
  - Daily stability: flag. Every day's rate rounds to 8.30%, with essentially zero day-to-day variance. That is unusually flat for real traffic, so the data may be modelled or smoothed rather than raw. The day-to-day interval is a negligible ±0.0002 points. I used the wider binomial interval.
  - Consistency of counts: pass. Conversions are below clicks, and clicks are below searches, on every day.

## Caveats, and what would change the answer
- "Purchase" here means the `conversions` column. Its definition and attribution window aren't documented, and there is no metrics.json.
- If the flat daily rate comes from an aggregation or ETL artifact, the true uncertainty is larger than the interval shown.
- If Finance defines the metric differently (for example, per session, or only searches with a click), the number changes. Clicks to conversions would be 70,030 / 263,036 = 26.6% [measured].

## Provenance
- Metric: conversions / searches, summed over the week, from stated here [guess]
- Data: `search_daily_c`, through 2026-10-11 (the full week)
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: ad hoc Python/sqlite3 run in the session; not saved to a file