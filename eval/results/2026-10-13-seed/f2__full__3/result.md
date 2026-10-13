## Answer
Headline: 55.0 % (54.6 % to 55.4 %) [q8]
Navigational queries had a click-through rate of 55.0% in 2026-W40: 32,878 clicks on 59,800 searches, using current labels only. [q8]

## What it means for the marketing planning doc
No decision threshold was given, so there is nothing to compare the interval to. The figure to quote is about 55%, and the interval is ±0.4 pp. [q8] Quoting the unfiltered join (45.0%) would understate it by about 10 pp. [q7]

## Why we believe it
- Alternatives considered:
  - Join to all label rows, including superseded labels: ruled out. It duplicates queries and gives 45.0%. [q7, check:fanout#2] [measured]
  - Label version 1 vs 2 changing the result: ruled out. Current navigational CTR is 55.0% in both versions. [q5] [measured]
  - Mix-shift, seasonality, day of week: not applicable. This is a single-week level and no comparison was made. [inferred]
- Checks run:
  - fanout (is_current=1 join): pass. 1000 rows in and out. [check:fanout#1]
  - fanout (all label rows join): fail. 500 duplicate-key rows; I discarded this join. [check:fanout#2]
  - completeness: could not run. There is only one week of data and no history. [check:completeness#1]
  - mix_shift: skipped. No rate change was reported.
  - srm: skipped. This is not an experiment.

## Caveats, and what would change the answer
- Only W40 exists in query_stats, so I couldn't verify that the week is complete. A partial week would change the level only if the missing rows have a different CTR.
- The interval is a binomial interval over searches. It treats searches as independent, but they cluster in 400 queries, so the true interval is wider.
- The definition (clicks / searches, summed over navigational queries, is_current=1 labels) is my guess. A weekly average of per-query CTR would differ.
- There is no dashboard to reconcile against.

## Provenance
- Metric: sum(clicks)/sum(searches) for queries with intent='navigational' and is_current=1, week 2026-W40, from stated here [guess]
- Data: query_stats, query_labels, through 2026-W40 (completeness unverified)
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (17 numbers on 7 lines; 3 queries, 3 checks, 0 given)