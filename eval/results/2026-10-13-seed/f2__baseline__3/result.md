## Answer
Headline: 55.0 % (95% CI 54.9 to 55.0, query-level bootstrap)
In 2026-W40, navigational queries (current labels) had 32,878 clicks on 59,800 searches, a click-through rate of 54.98%. [measured]

## What it means for the planning doc
Use about 55%. The interval is about 0.1 pp wide, so sampling noise won't change the number. The label choice does: using every label row instead of only current ones gives 45.0%, a 10 pp difference. [measured]

## Why we believe it
- Alternatives considered:
  - Include all label rows, including superseded ones: ruled out. It double-counts queries that were relabeled, giving 600 query rows and 45.0%. Only `is_current=1` gives one label per query. [measured]
  - Mean of per-query CTRs instead of clicks over searches: ruled out as the headline. It gives 55.0% anyway, so the choice doesn't matter here. [measured]
- Checks run:
  - Duplicate current labels: pass. No query has more than one current label. [measured]
  - Coverage: pass. All 1,000 queries have a current label. [measured]
  - Data sanity: pass. There are no null clicks, no clicks above searches, and no searches at or below 0. [measured]
  - Week coverage: pass. The table holds only W40, with 1,000 unique queries. [measured]
  - Uncertainty: pass. The bootstrap resamples queries (2,000 draws). [measured]

## Caveats, and what would change the answer
- "Current" means `is_current=1`. If marketing wants the labels as they stood at the time (version 1), the number changes. 200 queries were relabeled from navigational to something else in version 2, and 100 came the other way. [measured]
- Click-through rate is clicks divided by searches. Whether the dashboard counts sessions or de-duplicated clicks is unknown. [guess]
- The very narrow interval reflects low query-to-query variation in this data. It says nothing about labeling accuracy. [inferred]

## Provenance
- Metric: clicks / searches, summed over navigational queries with current labels. This is stated here [guess]. No metrics.json exists in the directory.
- Data: `query_stats` joined to `query_labels` on `query_id` with `is_current=1`, covering 2026-W40 only.
- Reconciled: not done (no dashboard or reference figure available).
- Queries and checks: run inline in Python/sqlite3 in this session. No script files were saved.