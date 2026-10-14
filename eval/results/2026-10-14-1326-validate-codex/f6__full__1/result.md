## Answer
Headline: +50.05% (95% interval: 49.93%–50.18%) [q6] [measured]  
For the requested week, 321,780 of 642,880 eligible searches had a click, giving a CTR of 50.05%. [q4, q6] [measured]

- Observed: +50.05% (95% interval: 49.93%–50.18%) [q6] [measured]
- Adjusted: not computed (the request is for the weekly rate, not a change). [inferred]
- Causal effect: not identified (a defined intervention and randomized or credible quasi-experimental comparison would be needed). [inferred]

## What it means for the weekly business review
Report 50.05% as the weekly CTR; the interval is approximately ±0.12 pp under an independent-search model. [q6] [inferred] No decision threshold or comparison week was supplied, so whether this clears the smallest decision-changing difference cannot be assessed. [inferred]

## Why we believe it

- Alternatives considered:
  - Counting repeat clicks or including bot/internal traffic: ruled out by applying the documented search-level numerator and external-only filter. [q4] [measured]
  - Missing calendar days or duplicate daily segment cells: ruled out by seven days with six distinct cells each. [q3] [measured]
  - Partial loads or logging changes: ruled in as unresolved possibilities; calendar coverage cannot certify event completeness, and no load audit or logging history is available. [q1, q2, q3] [inferred]
  - Mix-shift, seasonality and day of week: ruled in as possible influences on the rate, but no change or cause was requested and no earlier week is available. [q3] [inferred]
- Checks run:
  - completeness: could not run could not run: need at least 3 earlier periods (trailing days (under 3 weeks of same-weekday history)) before 2026-10-05, got 0 [check:completeness#1] [measured]
  - completeness: could not run could not run: need at least 3 earlier periods (trailing days (under 3 weeks of same-weekday history)) before 2026-10-06, got 1 [check:completeness#2] [measured]
  - completeness: could not run could not run: need at least 3 earlier periods (trailing days (under 3 weeks of same-weekday history)) before 2026-10-07, got 2 [check:completeness#3] [measured]
  - completeness: pass 2026-10-08: 6 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (6) [check:completeness#4] [measured]
  - completeness: pass 2026-10-09: 6 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (6) [check:completeness#5] [measured]
  - completeness: pass 2026-10-10: 6 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (6) [check:completeness#6] [measured]
  - completeness: pass 2026-10-11: 6 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (6) [check:completeness#7] [measured]
  - Metric validity: pass no null or invalid numerator/denominator counts. [q4] [measured]
  - fanout: skipped no joins. [inferred]
  - mix_shift: skipped no change comparison. [inferred]
  - srm: skipped no experiment. [inferred]

## Caveats, and what would change the answer

- The interval is a Wilson interval assuming independent searches; repeated users may widen uncertainty. User-level data would support a clustered interval. The recorded weekly rate itself is an aggregate, not a sample estimate. [inferred]
- Earlier history and load-completion records would strengthen completeness verification; backfills or corrected logging could change the rate. [inferred]

## Provenance

- Metric: searches_with_click / searches_with_results × 100, summed over the requested dates, traffic_type = 'external', search grain, source search_daily_v; from metrics.json in $DS_OVERLAY_DIR. [measured]
- Data: search_daily_v, through 2026-10-11; full calendar coverage observed, load completion not independently certified. [q3] [measured]
- Reconciled: not done (no dashboard figure for this week was supplied; the metric file's historical verification does not reconcile this week). [inferred]
- Queries and checks: .ds-queries.log and .ds-checks.log; readout.md contains this readout. [measured]
- Verified: verify_readout: pass (36 numbers on 11 lines; 5 queries, 7 checks, 0 given)
