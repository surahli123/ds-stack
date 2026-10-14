## Answer
Headline: 46.1 % (95% CI 45.9 to 46.3)
Search CTR for 2026-10-05 to 2026-10-11 was 46.1% for external (real-user) traffic. That is the share of searches that got at least one click. Including bots would give 41.4%.
- Observed: 46.05 % (45.93 to 46.17), external traffic only. The interval is binomial and treats searches as independent, so it is probably a little too narrow.
- Adjusted: not computed (a single-week level has nothing to adjust for)
- Causal effect: not identified (this is a level, not a change. Measuring an effect would need a comparison week or an experiment.)

## What it means for the weekly business review
Use 46.1% as the week's CTR. The definition changes the number by far more than the sampling noise does. Bot traffic alone moves it about 5 points, and the clicks-per-search definition gives 64.5%. Pick one definition and keep it fixed week to week.

## Why we believe it
- Alternatives considered:
  - Include bots (41.4%): ruled out. Bots are about 13% of searches and click about 2% of the time, so they drag CTR down without reflecting user behavior. [inferred]
  - Include internal traffic (47.1% with internal, excluding only bots): ruled out. The `internal` label suggests employee traffic, though the data doesn't confirm that. Internal is about 5% of searches and clicks at about 67%, so it moves the figure by about 1 point. [inferred]
  - Clicks ÷ searches (64.5%): ruled out. It counts multiple clicks per search, so it measures clicks per search, not CTR. [inferred]
  - Searches with a click ÷ searches with results (50.1%): not chosen. It is a legitimate variant, but searches that returned nothing can't be clicked, so I kept all searches in the denominator. [guess]
  - Platform mix driving the number: ruled out. External CTR is 46.06% on desktop and 46.04% on mobile. [measured]
- Checks run:
  - Data completeness: pass. 42 rows, 7 days × 2 platforms × 3 traffic types, and no gaps.
  - Daily stability: pass. Daily total searches stay within about 117k to 123k.
  - Trend vs prior weeks: could not run. The table only covers this one week.

## Caveats, and what would change the answer
- No metrics.json was present, so the CTR definition is my assumption. If the business review defines CTR differently, such as including bots or using clicks ÷ searches, the number changes (41.4% and 64.5% respectively).
- I can't tell whether the `internal` and `bot` labels are accurate, or how they are assigned.
- There is no prior-week data, so I can't say whether 46.1% is high or low.

## Provenance
- Metric: searches_with_click ÷ searches, with traffic_type = 'external', from stated here [guess]
- Data: `search_daily_v`, 2026-10-05 through 2026-10-11 (the full week)
- Reconciled: not done (no dashboard or reference figure available)
- Queries and checks: run inline with Python and sqlite3 in this session. They are not saved to a file.