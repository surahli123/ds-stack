## Answer
Headline: 55.0% (click-through rate of navigational queries, 2026-W40)
In W40, the 400 queries currently labeled navigational got 32,878 clicks on 59,800 searches, which is 54.98%, or about 55.0%.

## What it means for the planning doc
Use about 55% as the W40 navigational CTR. It counts each query once, under its current intent label.

## Why we believe it
- Alternatives considered:
  - Joining all label rows, including superseded ones: ruled out. It gives 45.0%, but it counts 200 queries that were relabeled as navigational under an old label version, and it double-counts rows. Each query has exactly one `is_current=1` label. [measured]
  - Incomplete or missing data for W40: ruled out for missing queries. All 1,000 queries have a current label, with no null or zero searches and no clicks above searches. [measured]
  - Mix shift or seasonality: not applicable. This is a single-week level and not a change over time. [inferred]
- Checks run:
  - fanout: pass. A 1000-row left join to the 1000 distinct current labels gives 1000 rows.
  - completeness: could not run. The table holds only W40, and the check needs at least 3 earlier periods.
  - mix_shift: skipped. No rate change is being explained.
  - srm: skipped. This is not an experiment.

## Caveats, and what would change the answer
- I can't check that W40 is fully loaded, because there are no other weeks to compare against.
- The answer depends on using the current label version. Under the older labels the number would differ. The 45.0% figure above is not the same as old-label-only.
- CTR here is total clicks divided by total searches, which weights busy queries more. An average of per-query CTRs would be different.