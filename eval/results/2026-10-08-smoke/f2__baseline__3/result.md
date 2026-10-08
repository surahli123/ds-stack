## Answer
Headline: 55.0 % click-through rate for navigational queries in 2026-W40
Across the 400 queries currently labelled navigational, clicks divided by searches is 54.98%. [measured]

## What it means for the planning doc
Use about 55%. This is clicks divided by searches, pooled across all navigational queries. The average of per-query rates is almost identical at 55.0%. [measured]

## Why we believe it
- Alternatives considered:
  - Counting every label row, including superseded ones: ruled out. It gives 45.0% because it pulls in 200 stale labels (is_current=0). That count includes queries whose current label is informational, and some are counted twice. [measured]
  - Averaging per-query CTRs instead of pooling: ruled out as a concern, because it gives 55.0%, almost the same. [measured]
- Checks run:
  - Duplicate current labels: pass. No query has more than one is_current=1 label.
  - Label coverage: pass. All 1000 query_stats rows have a current label.
  - Row uniqueness: pass. There is one row per query in W40, and no rows have clicks greater than searches or null values.

## Caveats, and what would change the answer
- The 55% depends on using the current label version (is_current=1). Using all label rows would give 45%.
- I can't check how accurate the intent labels are. I also can't say whether the clicks column counts all clicks or only unique ones.