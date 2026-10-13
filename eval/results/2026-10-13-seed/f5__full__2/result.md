```
## Answer
Headline: can't tell
The raw CTR is 31.2% in treatment vs 30.0% in control (+1.2 pp) [q4], but the 50/50 split failed the sample-ratio check, so the arms are not comparable and that gap can't be read as a treatment effect [check:srm#1].

## What it means for the ranker_boost launch decision
No launch-grade lift can be given: the raw +1.2 pp gap [q4] rests on arms that don't match the planned 50/50 split (control share 51.2% vs 48.8%) [check:srm#1]. Hold the launch until the cause of the imbalance is found. No minimum worthwhile lift was given for this decision.

## Why we believe it
- Alternatives considered:
  - Real treatment effect (the requester's reading): not ruled in; the arms differ in size and so possibly in who is in them, so a gap in CTR could come from who was assigned or logged rather than from the ranker [check:srm#1] [inferred]
  - Incomplete data / missing days: ruled out, both arms have all 14 days and the last day is fully loaded [q2, check:completeness#1] [measured]
  - Day of week / seasonality: ruled out as the main driver, the two arms cover identical dates and daily user counts are near-constant [q2] [measured]
  - Mix-shift across segments: could not be assessed, the table has no platform/country/source breakdown [q1] [measured]
  - Logging or definition change: not testable here; a treatment-only drop in assigned users could come from logging or assignment filtering, which is unverified [check:srm#1] [guess]
- Checks run:
  - srm: fail, observed shares 0.512 / 0.488 vs expected 0.5 / 0.5, p about 1e-130 [check:srm#1]
  - completeness: pass, 2026-09-30 has 2 rows, 100% of the trailing median [check:completeness#1]
  - mix_shift: could not run, no segment columns in experiment_daily [q1]
  - fanout: skipped, no joins were used

## Caveats, and what would change the answer
- The cause of the SRM is unknown. If it is traced to a harmless issue (e.g. a bot filter applied to one arm) and the affected users can be removed or reweighted, the lift could be re-estimated with an interval.
- "users" is a daily sum, not unique users, and the table has no per-user rows, so a user-level interval can't be built.
- CTR is defined here as clicks / searches, and a clicks-per-user reading gives a different number [q4].
- Searches per user is identical in both arms [q4], which is unusual for real data and worth checking for how the table was built.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), arm-level over 2026-09-17 to 2026-09-30, from stated here [guess]
- Data: experiment_daily (experiment = ranker_boost), through 2026-09-30
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (19 numbers on 5 lines; 3 queries, 2 checks, 0 given)
```