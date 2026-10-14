```
## Answer
Headline: 46.0 % (95% CI 45.9 to 46.2)
Search CTR for 2026-10-05 to 2026-10-11 was 46.0%, counting external (real-user) traffic only and defining CTR as searches with a click divided by searches. [measured]
- Observed: 46.0 % (45.9 to 46.2), external traffic only. The all-traffic figure is 41.4%, and it is dragged down by bots. [measured]
- Adjusted: not computed (single week, no comparison asked for)
- Causal effect: not identified (this is a level, not a change; no intervention is in question)

## What it means for the weekly business review
Report 46.0% for the week. No decision threshold was given. The interval is about ±0.1 pt wide, so any week-over-week move larger than about 0.3 pt would be real. The data holds no prior week, so I can't say whether this week moved. [inferred]

## Why we believe it
- Alternatives considered:
  - Include bots and internal traffic (41.4%): ruled out. Bots click at about 2% and internal traffic at about 67%, which is not real-user behaviour. [measured]
  - CTR as searches with a click / searches with results (50.1%): not chosen. It is a defensible variant, but "per search" is the common default. [guess]
  - CTR as clicks / searches (64.5%): ruled out. It counts multiple clicks per search, so it is not a rate that stays within 0 to 100%. [inferred]
  - Platform mix driving the result: ruled out. Desktop is 46.06% and mobile is 46.04%. [measured]
- Checks run:
  - Data completeness: pass. 42 rows cover 7 days × 2 platforms × 3 traffic types. [measured]
  - Daily stability: pass. External CTR ranged from 45.88% to 46.16% across the days. [measured]
  - Interval: pass. It is a binomial normal approximation on 698,782 searches (±0.117 pt). It ignores day-to-day clustering. [measured]

## Caveats, and what would change the answer
- There is no metrics.json, so the CTR definition is my assumption. If the review uses clicks over searches with results, the figure is 50.1%.
- Excluding bots and internal traffic is my judgment. Whether the dashboard does the same is unknown.
- Bot and internal filtering depends on the `traffic_type` labels being correct.
- Only one week of data is available, so there is no trend or week-over-week comparison.

## Provenance
- Metric: CTR = searches_with_click / searches, external traffic only, stated here [guess]
- Data: search_daily_v, 2026-10-05 to 2026-10-11 (the only data present)
- Reconciled: not done (no dashboard or reference figure available)
- Queries and checks: ad hoc Python/sqlite3 run in this session; not saved to a file
```