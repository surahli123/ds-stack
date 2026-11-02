## Answer
Headline: +36.97 percent (95% interval: 36.68–37.26 percent) [q8] [measured]
Shopping queries had 39,857 recorded clicks across 107,810 searches in week 2026-W41. [q8] [measured]

- Observed: +36.97 percent (95% interval: 36.68–37.26 percent) [q8] [measured]
- Adjusted: not computed (a single week's rate was requested). [inferred]
- Causal effect: not identified (would require a specified intervention and randomized or credible quasi-experimental comparison). [inferred]

## What it means for merchandising's citation
Cite the recorded shopping CTR as 36.97%; the model-based interval is 36.68–37.26%. [q8] [measured] No decision threshold was supplied, so comparison with the smallest meaningful change cannot be assessed. [inferred]

## Why we believe it
- Alternatives considered:
  - Duplicate category weighting: ruled in for a direct join, which yields 40.90%; counting each query once gives 36.97%. [q5, q7, q8] [measured]
  - Conflicting categories or missing mappings: ruled out in these records; all queries map without conflicting categories. [q5, q6] [measured]
  - Incomplete loading or logging changes: ruled in as unresolved possibilities; historical periods and load certification are unavailable. [q1, q2] [inferred]
  - Mix-shift, seasonality and day of week: ruled out as necessary adjustments to this descriptive weekly rate; their influence on comparisons was not tested. [inferred]
- Checks run:
  - completeness: could not run: need at least 3 earlier periods (trailing days (under 3 weeks of same-weekday history)) before 2026-W41, got 0 [check:completeness#1] [measured]
  - fanout: pass row counts consistent with a many_to_one left join [check:fanout#1] [measured]
  - fanout: pass row counts consistent with a many_to_one left join [check:fanout#2] [measured]
  - Metric validity: pass no null, negative, or clicks-above-searches totals. [q2] [measured]
  - Independent aggregation: pass membership filtering reproduces deduplicated-join totals. [q6, q8] [measured]
  - mix_shift: skipped no change between periods requested. [inferred]
  - srm: skipped no experiment supplied. [inferred]

## Caveats, and what would change the answer
- The Wilson interval assumes independent binary click outcomes per search. Repeated clicks or correlated searches would require event-level data and a different interval. [inferred]
- Week completeness is unverified; late-arriving records could change the rate. Load certification would resolve this limitation. [inferred]
- An authoritative CTR definition could change the numerator or denominator. [inferred]

## Provenance
- Metric: total clicks / total searches × 100 for 2026-W41 shopping queries, counting each query-week once using category membership; no metrics.json configured, definition stated here [guess].
- Data: query_week, query_category, category_vertical; available through 2026-W41, ending 2026-10-11; last complete period unverified. [q1, q2] [measured]
- Reconciled: not done (no dashboard or independent source supplied). [inferred]
- Queries and checks: `.ds-queries.log` and `.ds-checks.log`; saved readout in `readout.md`. [measured]
- Verified: verify_readout: pass (16 numbers on 6 lines; 6 queries, 3 checks, 0 given)
