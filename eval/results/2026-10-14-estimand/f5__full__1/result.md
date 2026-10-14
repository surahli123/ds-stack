## Answer
Headline: can't tell
Treatment's CTR is +1.20 pp higher than control's in the raw data, but the arms fail the sample-ratio check (51.2% / 48.8% users vs the planned 50/50), so the comparison can't be trusted as a randomized lift. [q5, check:srm#1]
- Observed: +1.20 pp (95% CI +1.13 to +1.27 pp) [q5]
- Adjusted: not computed (no segment columns in experiment_daily to hold fixed, and the cause of the imbalance is unknown)
- Causal effect: not identified (find and fix the cause of the user-count imbalance, for example assignment or logging differences between arms, then re-read on balanced data)

## What it means for the ranker_boost launch decision
The raw +1.13 to +1.27 pp interval is only a sampling interval and does not cover bias from the broken split; no launch threshold was given, so I can't say whether it clears one. [q5, check:srm#1]

## Why we believe it
- Alternatives considered:
  - Assignment or logging bias in one arm (SRM): ruled in by 499,930 control vs 475,990 treatment users, chi2 587, p 1e-129 [q2, check:srm#1] [measured]
  - Incomplete data or missing days: ruled out, all 14 days present with 2 arm-rows each [q3, check:completeness#1] [measured]
  - Day-of-week or seasonality: ruled out as the source of the gap, the CTR gap is the same on every day sampled (0.300 vs 0.312) and both arms cover identical dates [q4] [measured]
  - Mix-shift across segments: could not be tested, the table has no segment columns [q1] [inferred]
  - Treatment really improved CTR (requester's hypothesis): not ruled out or in; the raw gap is consistent with it but the SRM means arms may differ in who they contain [check:srm#1] [inferred]
- Checks run:
  - srm: fail, users 51.2% control vs 48.8% treatment against 50/50 [check:srm#1]
  - completeness: pass, 2026-09-30 has 2 rows, 100% of the trailing median [check:completeness#1]
  - mix_shift: skipped, no segment dimension in the data
  - fanout: skipped, no joins were used

## Caveats, and what would change the answer
- The SRM failure is unexplained; if engineering finds a benign cause that can be corrected (for example a logging bug that dropped treatment users independent of behavior), the +1.20 pp could be re-read.
- If users were dropped from treatment based on their behavior, such as bots or non-searchers, CTR could be inflated or deflated by selection alone.
- Daily "users" are summed across days, so they aren't unique users, and the interval treats searches as independent, which understates uncertainty because clicks cluster within users.
- No launch threshold was provided.

## Provenance
- Metric: CTR = clicks / searches, summed over the 14 days per arm, from experiment_daily [guess]
- Data: experiment_daily, through 2026-09-30
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (25 numbers on 8 lines; 5 queries, 2 checks, 0 given)