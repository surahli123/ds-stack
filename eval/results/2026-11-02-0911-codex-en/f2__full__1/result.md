## Answer
Headline: +54.98% (95% interval: 54.58%–55.38%) [q7] [measured]

In the available data for 2026-W40, currently labeled navigational queries received 32,878 clicks across 59,800 searches. [q4] [measured]

- Observed: +54.98% (95% interval: 54.58%–55.38%) [q7] [measured]
- Adjusted: not computed (a single-week descriptive rate was requested). [inferred]
- Causal effect: not identified (a specified intervention and randomized or credible quasi-experimental comparison would identify it). [inferred]

## What it means for the planning doc
Use 54.98% as the observed rate under current intent labels; the model-based interval is 54.58%–55.38%. [q7] [measured] No minimum decision-changing difference was supplied, so decision sensitivity cannot be assessed. [inferred]

## Why we believe it

- Alternatives considered:
  - Historical-label duplication: ruled in for an unfiltered join, which produces 44.99%; ruled out for the reported estimate by filtering to current labels. [q7] [check:fanout#1] [check:fanout#2] [measured]
  - Incomplete loading or logging changes: neither ruled in nor ruled out; only the requested week and no load audit are available. [q1, q2] [inferred]
  - Mix-shift, seasonality and day of week: ruled out as required adjustments to this descriptive weekly total, but not as influences on future performance; no change or cause was requested. [inferred]
- Checks run:
  - completeness: could not run: need at least 3 earlier periods (trailing days (under 3 weeks of same-weekday history)) before 2026-W40, got 0 [check:completeness#1] [measured]
  - fanout: pass — row counts consistent with a many_to_one left join [check:fanout#1] [measured]
  - fanout: fail — right side has 300 duplicate-key rows (1300 rows for 1000 keys); dedupe or filter before joining; join added 300 rows (fan-out) [check:fanout#2] [measured]
  - Resolution: the failed diagnostic includes historical labels; the reported current-label join passes. [check:fanout#1] [check:fanout#2] [measured]
  - Bounds and grain: pass — no invalid counts; one stats row and one matched current label per query. [q2, q4, q5] [measured]
  - mix_shift and srm: skipped — no period comparison or experiment. [inferred]

## Caveats, and what would change the answer

- Current labels may differ from labels in force during the week; an effective-dated label history would settle that distinction. [inferred]
- Weekly completeness is unverified; a load audit could change the full-week estimate. [inferred]
- The Wilson interval assumes independent binary click outcomes per search; aggregate counts cannot verify that assumption or account for repeated-user clustering. The stored-data ratio itself is exact; search-level logs would support a better uncertainty model. [inferred]

## Provenance

- Metric: summed clicks / summed searches × 100, weighted by searches, for query_stats.week='2026-W40', joined by query_id to query_labels with is_current=1 and intent='navigational'; stated here [guess] (no metrics.json configured).
- Data: query_stats and query_labels in warehouse.db, through 2026-W40; last complete period unverified. [q1, q2] [measured]
- Reconciled: not done (no independent dashboard or reference total supplied). [inferred]
- Queries and checks: .ds-queries.log and .ds-checks.log; readout saved in readout.md.
- Verified: verify_readout: pass (19 numbers on 7 lines; 5 queries, 3 checks, 0 given)
