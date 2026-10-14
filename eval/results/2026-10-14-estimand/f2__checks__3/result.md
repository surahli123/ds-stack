Checks are done. The current-label join returns 54.98%, and the one that includes stale labels returns 44.99%, so I'm writing up the readout now.

## Answer
Headline: 54.98 percent (interval not computed: the data is weekly aggregates with no per-query variance)
Navigational queries in 2026-W40 had 59,800 searches and 32,878 clicks, a click-through rate of about 55.0%.
- Observed: 54.98 percent (no interval available), 400 navigational queries using current labels
- Adjusted: not computed (single week, no comparison or confounder in question)
- Causal effect: not identified (this is a descriptive rate, not a treatment effect)

## What it means for the marketing planning doc
Use roughly 55%. A single descriptive number was requested, and no decision threshold was given. The label choice moves the number by about 10 points, which is larger than any rounding.

## Why we believe it
- Alternatives considered:
  - Join to all label rows (including superseded versions): ruled out. It gives 44.99% because 300 queries have a stale label that differs from their current one, and those queries get counted under the wrong intent. [measured]
  - Duplicate current labels fanning out rows: ruled out. There are 1000 current labels for 1000 distinct queries, and all 1000 W40 queries have exactly one current label. [measured]
  - Zero-search rows or clicks greater than searches: ruled out. There are none among navigational rows. [measured]
- Checks run:
  - fanout (current-label join): pass. 1000 left rows, 1000 joined rows.
  - completeness: could not run. The table holds only W40, so there is no history to compare. Whether W40 is fully loaded is unverified.
  - mix_shift and srm: skipped. There is no before/after period and no experiment.

## Caveats, and what would change the answer
- The answer assumes `is_current=1` is the right label. If marketing wants the labels as they stood at the time, the answer differs (45% is the all-versions figure, not a valid alternative).
- W40 completeness is unverified, and a partial week could shift the rate. [inferred]
- The rate is click-weighted (sum of clicks over sum of searches). An unweighted average of per-query rates would differ.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), stated here [guess]. There is no metrics.json.
- Data: `query_stats` joined to `query_labels` (is_current=1, intent='navigational'), W40 only.
- Reconciled: not done (no dashboard or reference source available).
- Queries and checks: checks are logged in `.ds-checks.log` (fanout#1, completeness#1). The queries were ad hoc inline Python and are not saved to a file.