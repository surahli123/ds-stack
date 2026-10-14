## Answer
Headline: 46.0 % (95% CI 45.9 to 46.2), search CTR for 2026-10-05 to 2026-10-11 on external (real-user) traffic, defined as searches with ≥1 click ÷ searches.

About 46 in 100 real-user searches got a click that week. Including bot and internal traffic, the figure is 41.4 %.
- Observed: 46.0 % (45.9 to 46.2), external traffic only (321,780 / 698,782). The interval is binomial on searches and ignores day-to-day clustering. [measured]
- Adjusted: 46.0 % (45.9 to 46.2), holding traffic type fixed to external, which excludes bots and internal. This is the same number as Observed. Bots are 12.5 % of searches and click about 2 % of the time. [measured]
- Causal effect: not identified. This is a level, not a change, and there is no intervention.

## What it means for the weekly business review
Report 46.0 % and label it external-only. If the review's usual definition counts all traffic, the figure is 41.4 %, a 4.6-point gap that is larger than any plausible week-to-week noise. Confirm which definition the review uses before presenting.

## Why we believe it
- Alternatives considered:
  - Bots dragging down CTR: ruled in. Bot CTR is 2.0 % on 105k searches, so excluding them moves the figure by about 4.6 points. [measured]
  - Clicks ÷ searches (58.2 % all traffic, 64.5 % external) as the definition: not chosen because it counts multiple clicks per search and is not a rate of searches. [inferred]
  - Clicks ÷ searches with results (44.5 % all traffic): not chosen. [guess]
  - Internal traffic: its CTR is 67 % on 35k searches. It is excluded as non-customer traffic, and including it would barely move the number. [inferred]
- Checks run:
  - Data completeness: pass. All 7 days are present, with 2 platforms × 3 traffic types each.
  - Row sanity: pass. There are no nulls, and clicked searches never exceed searches with results, which never exceed searches.
  - Prior week: could not run. The table only covers 10-05 to 10-11.
  - Platform split: skipped. Desktop and mobile volumes are nearly identical.

## Caveats, and what would change the answer
- The CTR definition is my assumption, because there is no metrics.json. A different definition would change the headline (41.4 %, 44.5 % or 58–64 %).
- Excluding bots relies on the traffic_type labels being correct.
- The interval treats searches as independent, so the true uncertainty is somewhat wider.
- The week ends 10-11 and the data is complete through that day.

## Provenance
- Metric: searches_with_click ÷ searches, external traffic_type only, [guess] (no metrics.json found).
- Data: search_daily_v, 2026-10-05 to 2026-10-11 (the only dates in the table).
- Reconciled: not done (no dashboard or reference figure available).
- Queries and checks: run inline with Python sqlite3 in this session. No log file was saved.