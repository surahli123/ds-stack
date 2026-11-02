## Answer
Headline: +54.98% (95% interval: 54.58%–55.38%) [q4, q6] [measured]

Navigational queries in 2026-W40 recorded 32,878 clicks across 59,800 searches, using current intent labels. [q4] [measured]

- Observed: +54.98% (95% interval: 54.58%–55.38%) [q4, q6] [measured]
- Adjusted: not computed (a single-week descriptive rate was requested). [inferred]
- Causal effect: not identified (an intervention and randomized or credible quasi-experimental comparison would be needed). [inferred]

## What it means for the planning doc
Use 54.98% as the observed baseline under the stated definition; the model-based interval is 54.58%–55.38%. [q4, q6] [inferred]
No smallest decision-changing difference was supplied, so whether this precision is sufficient for planning cannot be assessed. [inferred]

## Why we believe it

- Alternatives considered:
  - Duplicate historical labels: ruled out for this calculation by filtering to current labels and confirming a unique, fully matched join. [q3, q5] [check:fanout#1] [measured]
  - Incomplete data or logging changes: ruled in as unresolved possibilities; only the requested week and no load or logging audit are available. [q1, q2] [inferred]
  - Mix-shift, seasonality and day-of-week effects: ruled in as possible limits on future extrapolation; these data do not provide a time comparison or daily breakdown. [q1, q2] [inferred]
- Checks run:
  - fanout: pass — row counts consistent with a many_to_one left join. [check:fanout#1] [measured]
  - completeness: could not run: need at least 3 earlier periods (trailing days (under 3 weeks of same-weekday history)) before 2026-W40, got 0. [check:completeness#1] [measured]
  - Count validity: pass — no null, negative, or clicks-above-searches rows. [q2] [measured]
  - mix_shift: skipped (no rate change requested). [inferred]
  - srm: skipped (no experiment). [inferred]

## Caveats, and what would change the answer

- Current labels may differ from labels effective during the requested week; dated label history would settle that distinction. [inferred]
- The Wilson interval assumes independent searches with binary click outcomes; it excludes label errors and missing data. Event-level documentation would validate these assumptions. [inferred]
- This is the recorded-data rate; confirmed load completion and an approved CTR definition would strengthen its use as the full-week baseline. [inferred]

## Provenance

- Metric: 100 × SUM(clicks) / SUM(searches), at query-week grain in query_stats, filtering week='2026-W40' and joining query_labels on query_id with is_current=1 and intent='navigational'; stated here [guess].
- Data: query_stats and query_labels, through 2026-W40; last complete period unverified. [measured]
- Reconciled: not done (no dashboard or independent source supplied). [inferred]
- Queries and checks: .ds-queries.log and .ds-checks.log; interval calculation logged as q6. [measured]
- Verified: verify_readout: pass (14 numbers on 5 lines; 6 queries, 2 checks, 0 given)
