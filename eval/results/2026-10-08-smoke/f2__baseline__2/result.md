## Answer
Headline: 55.0 % click-through rate for navigational queries in 2026-W40

Across the 400 queries currently labeled navigational, there were 32,878 clicks on 59,800 searches, which is 54.98%. [measured]

## What it means for the planning doc
Use about 55% for navigational CTR. This is searches-weighted (total clicks divided by total searches), and it uses only the current label for each query.

## Why we believe it
- Alternatives considered:
  - Counting all label rows, including old versions: ruled out. It double-counts queries that were relabeled and gives 45.0% on 89,700 searches. [measured]
  - Label version 1 only: ruled out. 100 queries were relabeled in version 2, and the `is_current` flag marks the latest label. [inferred]
  - Averaging per-query CTRs instead of pooling: not computed. The pooled figure is the standard definition of CTR. [guess]
- Checks run:
  - One current label per query: pass. All 1,000 queries have exactly one `is_current=1` row.
  - Join coverage: pass. Every query in `query_stats` has a label.
  - Data sanity: pass. There are no nulls, no rows where clicks exceed searches, and only W40 data, with one row per query.

## Caveats, and what would change the answer
- The answer depends on trusting `is_current` as the right label. Using the old labels gives about 45% instead.
- CTR here is clicks divided by searches. If the planning doc defines it differently (for example, per-session or per-impression), the number could differ.