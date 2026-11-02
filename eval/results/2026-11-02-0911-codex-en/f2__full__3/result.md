## Answer
Headline: +54.98 percent (no interval: stored totals; sampling model unspecified) [q4] [measured]

Navigational queries in 2026-W40 recorded 32,878 clicks across 59,800 searches using current intent labels. [q4] [measured]

- Observed: +54.98 percent (no interval: stored totals; sampling model unspecified) [q4] [measured]
- Adjusted: not computed (requested the observed weekly rate) [inferred]
- Causal effect: not identified (would require a specified intervention and a randomized or credible comparison design) [inferred]

## What it means for the marketing planning doc
Use this as the descriptive rate for the stored week, conditional on current labels and complete loading. No decision threshold was supplied, and no uncertainty interval is justified by the available sampling information, so decision sensitivity cannot be assessed. [inferred]

## Why we believe it

- Alternatives considered:
  - Historical labels duplicating searches: ruled out for this calculation by filtering current labels and verifying unique, complete matches. [q3, q4, q5] [measured]
  - Incomplete loading: ruled in as unresolved; only the requested week is available and no load-status source exists in the database. [q1, q2] [inferred]
  - Mix, seasonality, and day-of-week effects: ruled in as limits on extrapolation; the data provide no comparison weeks or daily breakdown. [q1, q2] [inferred]
  - Label-definition changes: ruled in by historical and current label versions; this estimate uses current classifications, not necessarily classifications at the time of each search. [q3] [inferred]
- Checks run:
  - completeness: could not run: need at least 3 earlier periods (trailing days (under 3 weeks of same-weekday history)) before 2026-W40, got 0 [check:completeness#1] [measured]
  - fanout: pass — row counts consistent with a many_to_one left join [check:fanout#1] [measured]
  - Count validity: pass — no missing, negative, or clicks-above-searches counts; query IDs are unique within the week. [q2] [measured]
  - mix_shift and srm: skipped — no rate change or experiment requested. [inferred]

## Caveats, and what would change the answer

- Confirm the load is complete before treating the result as the full-week population rate. [inferred]
- Historical intent assignments could change the cohort; effective-date labels would establish the contemporaneous rate. [inferred]
- Confirm whether clicks count clicked searches or individual clicks; event semantics and a sampling/dependence model would determine an appropriate interval. [inferred]

## Provenance

- Metric: sum(clicks) / sum(searches) × 100, weighted by searches, for query_stats.week = '2026-W40', matched by query_id to query_labels with is_current = 1 and intent = 'navigational'; from stated here [guess].
- Data: query_stats and query_labels; available through 2026-W40, last complete period unverified. [q1, q2] [measured]
- Reconciled: not done (no independent dashboard or reference total provided). [inferred]
- Queries and checks: .ds-queries.log and .ds-checks.log; readout saved in readout.md. [measured]
- Verified: verify_readout: pass (7 numbers on 4 lines; 5 queries, 2 checks, 0 given)
