## Answer
Headline: 46.05 % (95% CI 45.93 to 46.17) — search CTR for 2026-10-05 to 2026-10-11, external (real-user) traffic only, defined as searches with a click ÷ searches.
Search CTR was about 46% for the week; including bots it would read 41.4%.
- Observed: 46.05 % (45.93 to 46.17), external traffic. Unfiltered it is 41.41 %, and excluding bots only it is 47.06 %. [measured]
- Adjusted: not computed (single-week level, no comparison)
- Causal effect: not identified (this is a level, not a change; no comparison period exists in the data)

## What it means for the weekly business review
Report about 46%. The interval is ±0.12 pt, but the definition choice moves the number by about 5 pt (41.4 to 47.1), which is far larger than the sampling noise. Pin the definition before comparing with past reviews.

## Why we believe it
- Alternatives considered:
  - Bot traffic inflating the denominator: ruled in. Bots are 12.5% of searches and click on only about 2% of them, so I excluded them. [measured]
  - Internal traffic: ambiguous. Internal CTR is about 67%, and it is 4.8% of searches. Including it gives 47.06%. I excluded it as non-customer traffic. [inferred]
  - Clicks÷searches instead of searches-with-click÷searches: it gives 64.5% for external traffic, which can exceed 100% in principle, so it is not a rate of searches. I did not use it. [inferred]
  - Platform mix: ruled out. Desktop (46.06%) and mobile (46.04%) are the same. [measured]
- Checks run:
  - Date coverage: pass. All 7 days × 6 platform/traffic segments are present (42 rows).
  - Daily stability: pass. Daily search volume ranges from 116.6k to 123.0k with no gaps.
  - Interval: pass. It is a binomial (Wald) interval on searches. It ignores day-to-day clustering, so it is somewhat optimistic.
  - Prior-week comparison: could not run. The table holds only this week.

## Caveats, and what would change the answer
- No metrics.json was provided, so the definition and the bot and internal exclusions are my choices. If the official definition is all traffic, the answer is 41.4%. If it is clicks÷searches, the answer is 64.5%.
- The interval is understated because it ignores day-level correlation.
- There is no baseline, so I can't say whether 46% is up or down.

## Provenance
- Metric: searches_with_click ÷ searches, external traffic only, stated here [guess]
- Data: search_daily_v, through 2026-10-11 (the full week is present)
- Reconciled: not done (no dashboard or reference figure available)
- Queries and checks: ad-hoc Python/sqlite3 queries run in this session. They are not saved to a file.