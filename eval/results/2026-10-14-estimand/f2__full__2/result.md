```
## Answer
Headline: 54.98 % (54.58 to 55.38) [q5]
Navigational queries had a click-through rate of 54.98% in 2026-W40 (32,878 clicks / 59,800 searches, 400 queries), using each query's current label; the interval is a binomial approximation on searches. [q5]
- Observed: 54.98 % (54.58 to 55.38) [q5]
- Adjusted: not computed (single level, not a change over time; no comparison to adjust)
- Causal effect: not identified (this is a level, not an effect of anything)

## What it means for the marketing planning doc
Use roughly 55% for navigational CTR; the interval is about ±0.4 pp wide, and no decision threshold was given, so any planning change smaller than that is within noise. [q5]

## Why we believe it
- Alternatives considered:
  - Label-version duplication (a naive join to query_labels gives 1300 rows for 1000 queries, double-counting relabelled queries): ruled out by joining only is_current=1, which gives exactly 1000 rows [q7, q8] [measured]
  - Label version 1 vs 2 differing in meaning: ruled out, navigational CTR is 54.98% under v1 and 54.99% under v2 among current labels [q6] [measured]
  - Bad rows (clicks > searches or searches <= 0): ruled out, 0 rows [q9] [measured]
  - Mix-shift / seasonality: not applicable, single week and single level requested [inferred]
- Checks run:
  - fanout: pass current-label join is many_to_one, 1000 rows in and out [check:fanout#1]
  - completeness: could not run, only one week exists in query_stats, no history to compare [check:completeness#1]
  - mix_shift: skipped, no change over time is being reported
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- Week completeness is unverified (only W40 in the table); a partially loaded week would change the number. Confirm with the data owner.
- "Current label" (is_current=1) is assumed to be the intended intent label; using superseded labels (is_current=0) would give a different set of queries.
- CTR is pooled (total clicks / total searches), so high-volume queries dominate; an average of per-query CTRs would differ.
- Interval treats searches as independent; per-query clustering would widen it.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches), week 2026-W40, queries with current intent label = navigational, from stated here [guess]
- Data: query_stats, query_labels (is_current=1), through 2026-W40 (completeness unverified)
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (23 numbers on 8 lines; 5 queries, 2 checks, 0 given)
```