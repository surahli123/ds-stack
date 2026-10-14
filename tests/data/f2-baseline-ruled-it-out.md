## Answer
Headline: 54.98 % (95% CI 54.6 to 55.4)
The click-through rate of navigational queries in 2026-W40 was about 55.0 %, using each query's current intent label. [measured]
- Observed: 54.98 % (54.6 to 55.4). That is 32,878 clicks on 59,800 searches across 400 queries. The interval is a binomial approximation. A query-level bootstrap gave a much narrower 54.95 to 55.01, so I used the wider one. [measured]
- Adjusted: not computed (this is a descriptive rate for one week, with no comparison to adjust).
- Causal effect: not identified (this is a level, not an effect, so no causal question applies).

## What it means for the planning doc
Use about 55 %. The rate is the same to within a fraction of a point however it is averaged. The choice of label set matters far more than sampling noise: the old labels would give 45 %, a 10-point difference.

## Why we believe it
- Alternatives considered:
  - Using all label rows, including superseded ones, would double-count queries and give 45.0 %. I ruled it out because `is_current=1` gives exactly one label per query. [measured]
  - Averaging per-query CTRs instead of pooling clicks and searches would change the answer. I ruled it out because it gave 55.01 %, almost identical to the pooled figure. [measured]
  - Relabeling could change which queries count as navigational. It did: 300 queries have a current label that differs from their old one. I used current labels as the right basis. [measured] That current labels are the right basis is my judgment. [inferred]
- Checks run:
  - Label coverage: pass. Every query in `query_stats` has exactly one current label.
  - Data quality: pass. There are no nulls, no rows with clicks > searches, and no duplicate query-week rows. The table has only W40.
  - Interval: flag. The binomial and bootstrap intervals disagree in width.

## Caveats, and what would change the answer
- If marketing's definition of "navigational" is the old label version (v1), the figure is 45.0 %. [measured]
- A click is any recorded click per search. I don't know whether the CTR metric defines it differently. [guess]
- The data covers only W40, so I can't say anything about a trend.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), for queries whose current intent is navigational. There is no metrics.json, so this definition is stated here. [guess]
- Data: `query_stats` joined to `query_labels` on `is_current=1`, for the week 2026-W40.
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: run inline in the session via Python and sqlite3. They are not saved to a file.