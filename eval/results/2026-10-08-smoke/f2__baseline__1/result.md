## Answer
Headline: 55.0 % (pooled clicks ÷ searches)
In 2026-W40, navigational queries (using each query's current label) had a click-through rate of 54.98%, or 4,000-ish queries' worth of searches pooled across 400 queries. [measured]

## What it means for the planning doc
Use about 55%. Using stale labels would understate it by roughly 10 points. [inferred]

## Why we believe it
- Alternatives considered:
  - Using all label rows, including superseded ones: ruled out. It double-counts queries and drops the rate to 45.0%. [measured]
  - Average of per-query CTRs instead of pooled: ruled out. It gives 55.0%, so the choice barely matters. [measured]
- Checks run:
  - One current label per query: pass. No query has more than one is_current=1 row. 
  - Coverage: pass. All 1000 W40 queries have a current label, and each appears once.
  - Data sanity: pass. No nulls, and no rows where clicks exceed searches.

## Caveats, and what would change the answer
- "Current" is taken from the is_current flag. I didn't check whether label_version 2 is the right source of truth.
- The 400 navigational queries include 100 relabeled to version 2. If the labels are wrong, the number shifts.
- Click-through rate here is clicks ÷ searches. Another definition, such as one based on impressions, would give a different value.