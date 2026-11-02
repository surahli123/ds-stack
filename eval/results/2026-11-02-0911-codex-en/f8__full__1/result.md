## Answer
Headline: +36.97% (95% interval: 36.18%–37.76%) [q10] [measured]  
In the supplied data for 2026-W41, shopping queries generated 39,857 clicks from 107,810 searches, a CTR of 36.97%. [q7] [measured]

- Observed: +36.97% (95% interval: 36.18%–37.76%) [q10] [measured]
- Adjusted: not computed (a single-period rate was requested; duplicate category records were removed from membership counting). [inferred]
- Causal effect: not identified (an intervention and a randomized or credible comparison design would be needed). [inferred]

## What it means for Merchandising’s citation
Cite 36.97% as the shopping CTR in the supplied extract, conditional on the metric definition and load completeness. [q7] [inferred]  
The interval is 36.18%–37.76%; no smallest decision-changing difference was supplied, so its adequacy for a decision cannot be assessed. [q10] [inferred]

## Why we believe it
- Alternatives considered:
  - Duplicate category weighting: ruled in by repeated labels; the direct join gives 40.90%, while counting each query once gives 36.97%. [q5, q10] [measured]
  - Conflicting or missing category assignments: ruled out in this extract by no conflicting categories and no unmapped queries. [q5, q8] [measured]
  - Incomplete loading or logging changes: ruled in as unresolved possibilities; no historical periods or load audit exist in the supplied tables. [q1, q2] [inferred]
  - Mix-shift, seasonality and day-of-week effects: ruled out as explanations being tested here; this is a weekly level, with no change or causal claim. Their influence on the level remains untested. [inferred]
- Checks run:
  - completeness: could not run: need at least 3 earlier periods (trailing days (under 3 weeks of same-weekday history)) before 2026-W41, got 0 [check:completeness#1] [measured]
  - fanout: fail join added 250 rows (fan-out); resolved by existence-based membership. [check:fanout#1] [q7] [measured]
  - fanout: pass row counts consistent with a many_to_one inner join [check:fanout#2] [measured]
  - fanout: pass row counts consistent with a many_to_one left join [check:fanout#3] [measured]
  - Validity: pass unique query-week records and no null, negative or above-search click counts. [q2] [measured]
  - mix_shift: skipped (no rate change requested). [inferred]
  - srm: skipped (no experiment). [inferred]

## Caveats, and what would change the answer
- The interval uses a query-cluster delta method, assuming independent queries; it describes sampling uncertainty, not missing data or classification errors. The extract’s ratio itself is exact. [q9, q10] [inferred]
- Confirm the load audit before presenting this as a verified complete-week figure. [inferred]
- Confirm that clicks means clicked searches; multiple clicks per search would make this clicks per search instead. [guess]

## Provenance
- Metric: total clicks / total searches × 100, at query-week grain in query_week, filtered to 2026-W41 and shopping membership via query_category and category_vertical; each query counted once. No configured metrics.json; stated here [guess].
- Data: query_week, query_category, category_vertical; available through 2026-W41; last complete period unverified. [q1, q2] [measured]
- Reconciled: not done (no independent dashboard or trusted metric source supplied). [inferred]
- Queries and checks: .ds-queries.log and .ds-checks.log; readout saved in readout.md. [measured]
- Verified: verify_readout: pass (18 numbers on 8 lines; 6 queries, 4 checks, 0 given)
