## Answer
Headline: can't tell
Treatment's raw CTR is higher than control's, but the arms fail the sample-ratio check, so the comparison can't be trusted as a randomized result. [check:srm#1]
- Observed: +1.20 pp (+1.13 to +1.27 pp) [q3, q4] (measured)
- Adjusted: not computed (no segment columns in the table, and the cause of the imbalance is unknown)
- Causal effect: not identified (needs the cause of the assignment imbalance found and fixed, or a re-run with a clean split)

## What it means for the launch decision
The raw gap of +1.20 pp [q4] is far outside its naive interval, but the arm sizes are 51.2% vs 48.8% instead of the planned even split [check:srm#1]. The gap can't be used to launch until the imbalance is explained. The request gave a 50/50 split and no launch threshold [given].

## Why we believe it
- Alternatives considered:
  - Assignment or logging imbalance (users dropped or filtered differently by arm): ruled in, the arms fail srm, 499,930 vs 475,990 user-days [check:srm#1] [measured]
  - Incomplete data: ruled out, the last day has the expected 2 rows (control and treatment) [check:completeness#1] [measured]
  - Day-of-week or seasonality: ruled out as a driver of the gap, because both arms cover the same 14 days [q2] [measured]
  - Mix-shift: could not be tested, the table has no segment columns [q1] [inferred]
  - Real ranker effect: not ruled out or in, since arm comparability is broken [check:srm#1] [inferred]
- Checks run:
  - srm: fail, shares 51.23% vs 48.77%, p ≈ 1e-129 [check:srm#1]
  - completeness: pass, 2026-09-30 is fully loaded [check:completeness#1]
  - mix_shift: skipped, no segment dimension available
  - fanout: skipped, no joins were used

## Caveats, and what would change the answer
- The interval treats searches as independent. Searches are clustered within users, so the true interval is wider.
- The table has only daily arm totals, so no user-level analysis or segment cuts are possible. The imbalance could be selective user loss that correlates with CTR.
- If the owner of the assignment service shows the imbalance is benign (for example a bot filter applied evenly), the +1.20 pp would become usable.
- Users are summed across days (user-days), so the srm counts are not unique users.

## Provenance
- Metric: CTR = clicks / searches, summed over the window, per arm, from experiment_daily [guess]
- Data: experiment_daily, through 2026-09-30
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (16 numbers on 6 lines; 4 queries, 2 checks, 1 given)