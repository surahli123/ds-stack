## Answer
Headline: +8.30 % of searches led to a purchase (8.24% to 8.36%) [q4]
In 2026-10-05 to 2026-10-11, 70,030 purchases came from 843,738 searches, which is 8.30% [q3].
- Observed: +8.30 % (8.24% to 8.36%) [q4]
- Adjusted: not computed (no segment breakdown in the table, and this is a level, not a change)
- Causal effect: not identified (this is a descriptive rate, no intervention to estimate)

## What it means for the quarterly model
Use about 8.3% as the search-to-purchase rate for this week; the interval is about ±0.06 pp [q4], and daily rates ranged only 8.2997% to 8.3002% [q3]. No decision threshold was given, so I can't say what change would matter.

## Why we believe it
- Alternatives considered:
  - Incomplete week: ruled out, all 7 days present, last day is in line with the others [q3] [measured]
  - Different definition (clicks-based purchase rate): ruled in as a caveat, clicks-to-conversion would be a different number [q2] [guess]
  - Day-of-week or mix effects: not testable, one week and no segments, and daily rates are nearly identical [q3] [inferred]
- Checks run:
  - completeness: pass 2026-10-11 has the same row count as earlier days, but this only checks row presence [check:completeness#1]
  - mix_shift: skipped, no segment columns and no comparison period
  - fanout: skipped, no joins
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- Definition is mine: conversions / searches, summed over the week. If Finance means purchases per click or per unique searching user, the answer changes.
- The interval is a simple binomial one that treats searches as independent. Repeat searches by the same user would widen it.
- The completeness check only counted rows, with no earlier history. Confirm the 2026-10-11 totals are final.

## Provenance
- Metric: conversions / searches, from stated here [guess]
- Data: search_daily_c, through 2026-10-11
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (14 numbers on 5 lines; 3 queries, 1 checks, 0 given)