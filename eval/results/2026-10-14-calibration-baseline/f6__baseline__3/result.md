```
## Answer
Headline: 46.0 % (95% CI 45.9 to 46.2), CTR for 2026-10-05 to 2026-10-11, external traffic only
Search CTR for the week was about 46%, defined as searches with at least one click divided by searches, with bots and internal traffic excluded.
- Observed: 46.05 % (45.93 to 46.17); the unfiltered figure including bots and internal traffic is 41.4 %. [measured]
- Adjusted: not computed (single week, no comparison being made)
- Causal effect: not identified (this is a level, not a change; no intervention is being evaluated)

## What it means for the weekly business review
This is a level, not a change, so there is no decision threshold to compare it with. The week-over-week comparison isn't possible because the table only holds this one week. The interval is about ±0.12 points, so only moves larger than that would show up against a future week.

## Why we believe it
- Alternatives considered:
  - Bot traffic inflating the denominator: ruled in. Bots are about 12.5% of searches and click on only about 2% of them, which pulls the unfiltered figure down to 41.4%. Excluding them is the standard choice. [measured]
  - Internal traffic: ruled in as an exclusion. Internal traffic clicks at about 67%, so including it lifts CTR to 47.1%. [measured]
  - Clicks per search (64.5%) as the CTR definition: ruled out. It can exceed 100% and isn't bounded like a rate. It is the alternative if the review defines CTR that way. [inferred]
  - Platform mix: ruled out as a driver. Desktop is 46.06% and mobile is 46.04%. [measured]
- Checks run:
  - Row coverage: pass. 42 rows = 7 days × 2 platforms × 3 traffic types, with no gaps. [measured]
  - Daily stability: pass. Daily totals are steady, between 116.6k and 123.0k searches. [measured]
  - Interval: the 95% CI is a binomial approximation that treats searches as independent. Repeat searches by the same user would widen it.
  - Reconciliation to a dashboard: could not run (no dashboard available).

## Caveats, and what would change the answer
- The CTR definition is my assumption. If the review uses clicks/searches, the figure is 64.5%. If it uses searches with results as the denominator, it is 50.1%.
- Whether to exclude bot and internal traffic is a judgment call. Check that it matches how earlier weeks were reported.
- Bot filtering depends on the `traffic_type` label being correct.
- The table has only this week, so no trend can be reported.

## Provenance
- Metric: sum(searches_with_click) / sum(searches) where traffic_type = 'external', stated here [guess]. No metrics.json was present.
- Data: search_daily_v, 2026-10-05 to 2026-10-11 (the full week; it is the only data in the table)
- Reconciled: not done (no dashboard or reference figure available)
- Queries and checks: ad hoc Python/sqlite3 queries run in this session; not saved to a file.
```