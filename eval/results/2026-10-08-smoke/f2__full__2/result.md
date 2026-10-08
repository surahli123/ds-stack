## Answer
Headline: can't tell
Using current labels, navigational queries in 2026-W40 had a CTR of 54.98% (32,878 clicks on 59,800 searches, 400 queries). I can't confirm that W40 is a complete week, so I'm not stating it as the answer.

## What it means for the planning doc
Treat about 55% as a provisional figure until someone confirms W40 is fully loaded. Don't use 45%, which is what you get from a naive join to the labels table.

## Why we believe it
- Alternatives considered:
  - Duplicate label rows (1,300 rows for 1,000 queries across label versions) inflating or diluting the rate: ruled in as a real trap. Joining without `is_current=1` gives 45.0% over 600 query rows. Filtering to current labels gives exactly one label per query, with no unlabeled queries. [measured]
  - Relabeling between label versions: the 400 current navigational queries are 300 on v1 and 100 on v2. The v1 queries alone give 54.98%, so v2 relabeling doesn't move the number. [measured]
  - Bad rows (clicks above searches, nulls): ruled out, none found. [measured]
  - Mix shift and seasonality: not applicable, because there is only one week and no comparison period. [inferred]
- Checks run:
  - fanout: pass for the current-label join (1,000 rows in, 1,000 out). It fails for the unfiltered join (1,000 rows became 1,300, +300 from duplicates), which is why I filtered to current labels.
  - completeness: could not run. It needs at least 3 prior periods, and the table holds only 2026-W40, with no daily rows to test.
  - mix_shift: skipped, since no rate moved.
  - srm: skipped, since this isn't an experiment.

## Caveats, and what would change the answer
- If earlier weeks, or daily rows for W40, show the week is fully loaded, the answer becomes 54.98%.
- If W40 is partial, the figure could be biased.
- "Navigational" here means the current label (`is_current=1`). If marketing means the label as of an older version, the number differs. That is the 45% join, which mixes old and new labels and isn't a valid definition.
- CTR here is total clicks divided by total searches (a search-weighted rate), not the average of per-query CTRs.