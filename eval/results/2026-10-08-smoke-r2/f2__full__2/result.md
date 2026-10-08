## Answer
Headline: 55.0 % click-through rate for navigational queries in 2026-W40 (32,878 clicks / 59,800 searches, 400 queries)
Navigational queries got clicks on 55.0% of searches in W40. This uses only each query's current label (`is_current=1`).

## What it means for the marketing planning doc
Use about 55%. Joining all label versions gives 45.0%, which is wrong because it double-counts queries and includes labels that are no longer current.

## Why we believe it
- Alternatives considered:
  - Join to all label rows without filtering: ruled out. `query_labels` has 1,300 rows for 1,000 queries because of relabeling (versions 1 and 2). That join gives 600 "navigational" rows and 45.0% [measured].
  - Stale or duplicate labels: ruled out by filtering to `is_current=1`. This leaves exactly one label per query, and every query in `query_stats` has one [measured].
  - Averaging per-query CTRs instead of pooling clicks and searches: not used. I report the pooled rate, which is the usual definition of CTR [inferred].
  - Bad stats data: ruled out. There are no nulls, searches is at least 50 for every query, and clicks never exceed searches [measured].
- Checks run:
  - fanout: pass for the current-label join (1,000 rows in, 1,000 out). A fail on the unfiltered join (1,300 rows, +300 from duplicate keys) is what showed the 45.0% figure was wrong.
  - completeness: could not run. It needs at least 3 earlier periods, and the table holds only W40.
  - mix_shift: skipped. Nothing moved, because this is a single-week level.
  - srm: skipped. This is not an experiment.

## Caveats, and what would change the answer
- Only W40 is in the data, so I can't confirm the week is fully loaded. All 1,000 queries are present, which suggests it is.
- The answer depends on the current label version. A different definition of "navigational", such as the label as of that week, could change it. Version 2 relabeled some queries.
- No interval is given. This is a population total over all W40 queries, not a sample estimate.