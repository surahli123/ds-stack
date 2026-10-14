## Answer
Headline: 55.0 % (54.6 % to 55.4 %) [q5]
Navigational queries had a click-through rate of 55.0% in 2026-W40 (32,878 clicks on 59,800 searches). [q5]
- Observed: 55.0 % (54.6 % to 55.4 %) [q5]
- Adjusted: not computed (single week, no comparison, so no mix question)
- Causal effect: not identified (no change or intervention is being measured)

## What it means for the marketing planning doc
Use about 55% for navigational CTR; the interval is under ±0.4 pp wide, so rounding to 55% is safe for planning. [q5] [given]

## Why we believe it
- Alternatives considered:
  - Relabelled queries (label v1 vs v2) changing the navigational set: ruled out, CTR is 55.0% under v1 and 55.0% under v2 labels [q6] [measured]
  - Join duplicating rows via multiple labels: ruled out, one current label per query and 1000 rows before and after the join [q4, check:fanout#1] [measured]
  - Bad rows (clicks above searches, zero searches): ruled out, none found [q7] [measured]
- Checks run:
  - fanout: pass row counts consistent with a many_to_one inner join [check:fanout#1]
  - completeness: could not run, only one week in the table, so there is no history to compare [check:completeness#1]
  - mix_shift: skipped, one week only, no change to decompose
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- No metrics.json was available; CTR is defined as total clicks / total searches (search-weighted), not the average of per-query CTRs.
- "Current" labels mix label versions 1 and 2 (is_current=1 for both); I used all current labels. Using only v2 labels gives a similar rate but covers only 100 queries.
- Interval is a plain binomial interval on searches; it ignores clustering by query, so the true interval is somewhat wider.
- Week completeness could not be verified; if W40 is partly loaded the figure could shift.

## Provenance
- Metric: navigational CTR = sum(clicks) / sum(searches) over queries with intent = 'navigational' and is_current = 1, week 2026-W40, stated here [guess]
- Data: query_stats joined to query_labels, through 2026-W40
- Reconciled: not done (no dashboard or other source provided)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (15 numbers on 6 lines; 4 queries, 2 checks, 1 given)