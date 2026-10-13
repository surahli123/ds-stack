## Answer
Headline: 55.0 % (95% CI 54.97 to 55.03 %)
In 2026-W40, navigational queries got 32,878 clicks on 59,800 searches, a click-through rate (CTR) of 55.0% [measured].

## What it means for the marketing planning doc
Use about 55%. The interval is only ±0.03 points, so sampling noise doesn't matter here. The label definition is the bigger risk: if the old v1 labels were used, the figure would be about 43% [measured].

## Why we believe it
- Alternatives considered:
  - Using all label rows, or only v1 labels: ruled out. Each query has exactly one `is_current=1` label (1000 labels for 1000 queries), and I used those. The v1-only figure of 43.0% mixes in superseded labels [measured].
  - Averaging per-query CTRs instead of dividing total clicks by total searches: not computed. I used clicks/searches summed over the week, which is the usual definition [inferred].
- Checks run:
  - fanout: pass. The join of `query_stats` to current labels stayed at 1000 rows, one label per query.
  - completeness: could not run. The table holds only 2026-W40, so there is no earlier history to compare against. I can't confirm W40 was fully loaded.
  - mix_shift: skipped. There is no comparison period.
  - srm: skipped. This isn't an experiment.

## Caveats, and what would change the answer
- The interval comes from a ratio estimator over 400 queries. It is unusually narrow, which suggests clicks scale almost exactly with searches. Treat it as a sampling interval only, not a measure of definition risk [inferred].
- If W40 is only partly loaded, the number could shift. I couldn't check this.
- If marketing uses a different intent labeling, such as v1 labels, the number changes materially.
- I didn't check the CTR definition against `metrics.json` or any dashboard.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) for queries with a current label of navigational [guess]. No `metrics.json` was found.
- Data: `query_stats` and `query_labels` (`is_current=1`), through 2026-W40, the only week present.
- Reconciled: not done (no dashboard or reference source available).
- Queries and checks: the queries were inline Python run in the shell and are not saved to a file. The check results are logged in `.ds-checks.log` (fanout#1 and completeness#1).