## Answer
Headline: 55.0 % (54.6 to 55.4 %)
Navigational queries had a click-through rate of 55.0% in 2026-W40: 32,878 clicks on 59,800 searches across 400 queries. [measured]
- Observed: 55.0 % (54.6 to 55.4 %) [measured]
- Adjusted: not computed (this is a single-week level, not a comparison, so there is nothing to adjust)
- Causal effect: not identified (this is a descriptive rate, and no causal question was asked)

## What it means for the planning doc
Use about 55%. The interval is ±0.4 points, so unless the doc needs better than about 1 point of precision, the sampling noise doesn't matter. The label definition matters far more: see the caveats.

## Why we believe it
- Alternatives considered:
  - Using all version-1 navigational labels, including superseded ones: ruled out. It gives 43.0% (32,186 clicks on 74,850 searches). It includes 200 queries whose label is no longer current, and some of those are now labeled informational. [measured]
  - Duplicate current labels, or a join that multiplies rows: ruled out. Each query has exactly one current label, and all 1,000 stats rows matched once. [measured]
  - Zero-search rows or clicks greater than searches: ruled out. There are none. [measured]
- Checks run:
  - fanout: pass. The join is many-to-one with 1,000 rows in and 1,000 rows out (fanout#1).
  - completeness: could not run. The table holds only W40, so there are no earlier weeks to compare against. I can't confirm W40 is fully loaded.
  - mix_shift: skipped. It needs a comparison between two periods, and there is only one week.
  - srm: skipped. This is not an experiment.

## Caveats, and what would change the answer
- The label version matters: 300 of the 400 navigational queries carry v1 labels and 100 carry v2. I used the current label (`is_current=1`). Using the older v1 labels gives about 43%. [measured]
- The interval treats each search as independent. That is conservative: when I clustered by query, the interval was narrower (±0.03 points). [measured]
- W40 completeness is unverified, and no other weeks exist to trend against. [inferred]

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) over navigational queries, using current labels. No metrics.json exists, so this definition is stated here. [guess]
- Data: `query_stats` joined to `query_labels` (`is_current=1`), through 2026-W40, the only week present.
- Reconciled: not done (no dashboard or reference figure available)
- Queries and checks: the queries were run inline and not saved to a file. Check results are in `.ds-checks.log`.