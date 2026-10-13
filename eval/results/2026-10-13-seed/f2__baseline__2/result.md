## Answer
Headline: 55.0 % (95% CI 54.9 to 55.0)
In 2026-W40, navigational queries (current labels) had 32,878 clicks on 59,800 searches, a click-through rate of 55.0%. [measured]

## What it means for the marketing planning doc
Use about 55%. The interval is only about ±0.1 pt wide, so sampling noise won't change the number. The real risk is the label definition: older label versions give 43–45%, a gap of 10 pts or more. [measured]

## Why we believe it
- Alternatives considered:
  - Include non-current or old label versions: ruled out. They would count the 300 queries (200 in the all-labels join) that v2 relabelled and that no longer count as navigational. That gives 45.0% (all rows) or 43.0% (v1 only). Only `is_current=1` rows describe today's labels. [measured]
  - Average of per-query CTRs instead of pooled clicks/searches: not computed. I used pooled clicks over searches. [guess]
- Checks run:
  - Duplicate current labels per query: pass. There are 0 duplicates, and every query has a current label.
  - Stats rows: pass. There are 1000 rows, one per query, in W40 only, with no clicks > searches.
  - Interval: pass. A bootstrap over 400 queries (4000 resamples) gave 54.95 to 55.01.
  - Reconciliation to a dashboard: could not run. No dashboard figure was available.

## Caveats, and what would change the answer
- The bootstrap treats queries as independent. Because the rate is pooled, high-volume queries carry more weight.
- The interval is narrow because query-level CTRs are very uniform. I didn't check that further.
- If marketing's definition of "navigational" is the v1 labels, the answer would be about 43%.
- There was no metrics.json, so "click-through rate" is my own definition: clicks divided by searches.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) over queries with a current navigational label, stated here [guess]
- Data: `query_stats` joined to `query_labels` on `is_current=1`, through 2026-W40
- Reconciled: not done (no dashboard or source figure provided)
- Queries and checks: ad-hoc Python/SQLite run in this session, not saved to a file