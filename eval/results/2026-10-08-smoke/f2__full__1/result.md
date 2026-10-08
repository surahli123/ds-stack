## Answer
Headline: 55.0% (32,878 clicks / 59,800 searches)
The click-through rate of navigational queries in 2026-W40 was 55.0%, using each query's current intent label.

## What it means for the marketing planning doc
Use about 55% for navigational CTR in W40. This is one week only, so it gives no trend. Informational queries ran at 25.0% in the same week.

## Why we believe it
- Alternatives considered:
  - Duplicate label rows inflating the join: ruled out. `query_labels` keeps old label versions, so I joined on `is_current=1`, which gives exactly one label per query (1,000 queries, 1,000 joined rows) [measured].
  - Using the original v1 labels instead of current ones: ruled out as the answer, but it matters. It gives 43.0%, because 200 queries labeled navigational in v1 were relabeled and 100 informational queries became navigational in v2. The current labels are the better definition for a planning number [measured; inferred that current is preferred].
  - Averaging per-query rates instead of pooling clicks and searches: ruled out. I pooled clicks over searches, which weights by traffic [inferred].
  - Bad rows (clicks above searches, nulls, duplicate query-week rows): ruled out. There were none [measured].
  - Mix shift or seasonality: not applicable, since there is only one week and no comparison [measured].
- Checks run:
  - fanout: pass. The join to current labels left 1,000 rows as 1,000, many-to-one. My first run passed the unfiltered label table (1,300 rows) and failed, but the actual join used only current labels.
  - completeness: could not run. It needs at least 3 prior periods, and the table only contains W40. All 1,000 queries have a row, but I can't confirm the week is fully loaded.
  - mix_shift: skipped. No rate moved, and there is no comparison period.
  - srm: skipped. This isn't an experiment.

## Caveats, and what would change the answer
- The number depends on the label version. With the original v1 labels it is 43.0%. Check with whoever owns the labels that v2 is the intended definition.
- W40 completeness is unverified. If the week was only partly loaded, the rate could shift.
- Roughly 100 navigational queries carry v2 labels, and the relabeling changed the CTR by 12 points. The label quality is therefore worth confirming.