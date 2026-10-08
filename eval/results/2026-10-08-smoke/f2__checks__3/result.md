## Answer
Headline: 55.0% click-through rate for navigational queries in 2026-W40
Navigational queries got 32,878 clicks on 59,800 searches in 2026-W40, which is 54.98% (measured). This uses each query's current intent label across 400 queries.

## What it means for the marketing planning doc
Use about 55%. Two earlier-label versions of navigational queries sit in the data, and the label version you use changes the number a lot. The 55% figure is for the current labeling (inferred).

## Why we believe it
- Alternatives considered:
  - Include superseded labels (`is_current=0`): ruled out. Those rows are old labels that were replaced. Including them would count queries twice or under the wrong intent. Only the current rows give one label per query (1,000 current rows for 1,000 queries) [measured].
  - Label version 1 only: ruled out as the headline. Its current v1 navigational queries, plus the superseded ones, give about 43.0% on 74,850 searches. That mixes stale and current labels [measured]. Version 2 alone gives 54.99% on 14,850 searches [measured].
  - Intent could have been mislabeled: not tested. I can't verify label quality from this data [guess].
- Checks run:
  - fanout: pass. The join of stats to current labels kept 1,000 rows and every W40 query has exactly one current label.
  - completeness: could not run. The table holds only W40, and the check needs at least 3 earlier periods. I could not confirm that W40 is fully loaded.
  - mix_shift: skipped. There is no prior period to compare against.
  - srm: skipped. This is not an experiment.

## Caveats, and what would change the answer
- Only W40 is in the table, so I could not confirm the week is fully loaded. A partial load would change the rate.
- The rate depends on the label version. Under the old v1 labels the rate is about 43%.
- This is clicks divided by searches, summed over queries (a pooled rate). The average of per-query rates would differ.