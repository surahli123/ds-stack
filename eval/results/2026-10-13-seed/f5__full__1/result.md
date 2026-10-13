```
## Answer
Headline: can't tell
The sample-ratio check failed (51.2% control vs 48.8% treatment users, planned 50/50), so the arms aren't comparable; the raw CTR gap of +1.20 pp (naive 95% interval ±0.07 pp) can't be trusted as a treatment effect. [check:srm#1, q5]

## What it means for the ranker_boost launch decision
The naive interval is far above zero, but the mismatch means the lift could be partly or wholly an artifact of who landed in each arm, so it doesn't support a launch call yet. No minimum worthwhile lift was stated in the request, so the interval can't be compared with one; even a small threshold would still need a valid split first. [q5]

## Why we believe it
- Alternatives considered:
  - Real treatment effect: not ruled out, but not shown; the raw gap is +1.20 pp (30.00% vs 31.20%) and consistent every day [q4, q5] [measured]
  - Biased assignment or logging (cause of SRM): ruled in as the open issue; users split 499,930 vs 475,990 with p≈1e-129 [check:srm#1] [measured]
  - Incomplete data: ruled out; all 14 days present with 2 arm rows each [check:completeness#1, q3] [measured]
  - Day-of-week/seasonality: ruled out as a driver of the gap; treatment beats control on every one of 14 days [q4] [measured]
  - Mix shift across segments: could not be examined; the table has no platform/country/source breakdown [q1] [inferred]
- Checks run:
  - srm: fail 51.23% / 48.77% vs 50/50, chi2 587, p≈1e-129 [check:srm#1]
  - completeness: pass 2026-09-30 has 2 rows = 100% of trailing median [check:completeness#1]
  - mix_shift: could not run, no segment-level data in experiment_daily [q1]
  - fanout: skipped, no joins used

## Caveats, and what would change the answer
- Find the cause of the SRM (assignment bug, bot filtering, or logging loss in one arm); a corrected or re-run valid split would give a usable lift.
- The naive interval treats searches as independent; user-level clustering would widen it. Only daily aggregates exist.
- Treatment has fewer users but the same searches per user (6.0), so the loss looks like users, not activity.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) per arm, over experiment_daily; lift = treatment minus control in pp, stated here [guess]
- Data: experiment_daily (experiment = ranker_boost), through 2026-09-30
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (25 numbers on 7 lines; 4 queries, 2 checks, 0 given)
```