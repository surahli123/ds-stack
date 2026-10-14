## Answer
Headline: can't tell

Treatment's CTR is higher than control's in the data, but the 50/50 split failed its integrity check, so I can't say the ranker caused the difference.

- Observed: +1.20 pp (95% CI +1.13 to +1.27). Control CTR is 30.00% (899,874 / 2,999,580) and treatment is 31.20% (891,051 / 2,855,940). [measured]
- Adjusted: not computed (the data has no segment or user-level columns, and the assignment imbalance has no known cause to adjust for)
- Causal effect: not identified (it would need a split with no sample ratio mismatch, or an explanation of why treatment lost about 4.8% of its users)

## What it means for the ranker_boost launch decision
The observed interval of +1.13 to +1.27 pp sits well above zero, but that interval assumes a valid randomization, and this one failed. I can't compare it with your minimum worthwhile lift, because the bias from the imbalance is unknown and could be larger than the whole 1.2 pp. Hold the decision until the cause of the mismatch is found.

## Why we believe it
- Alternatives considered:
  - Real ranker improvement: not ruled out. The gap is stable across all 14 days and about 17 standard errors wide, so it isn't noise [measured]. But the SRM means it may not be causal.
  - Differential user loss or filtering in treatment, such as logging or bot filtering, biasing who gets counted: not ruled out. Treatment has 475,990 users against control's 499,930, a 48.8% share, and every day shows the same gap. This pattern points to a systematic assignment or logging problem, not chance [measured; cause inferred].
  - Random chance: ruled out as the cause of the user imbalance (p ≈ 1e-130) [measured].
  - Novelty or day-of-week effects: not ruled out, but the daily lift looks flat, so I see no sign of them [inferred].
- Checks run:
  - srm: fail. Control has 51.23% of users against a planned 50%. chi2 is 587 and p is about 1e-130 [check:srm#1].
  - completeness: could not run. The tool needs at least 3 prior periods and the data has only 14 days of two rows each. All 14 days are present in both arms, and the user counts are stable [measured].
  - mix_shift and fanout: skipped. There are no segments, and I ran no joins on this single table.

## Caveats, and what would change the answer
- Find the cause of the SRM: assignment bug, exposure or logging filter, or bot or eligibility exclusion that differs by arm. If it is fixed or shown to be unrelated to clicks, the +1.2 pp could be trusted.
- The daily table has no user-level data, so I couldn't compute user-level CTR or test whether the lost users were heavy or light clickers.
- The interval treats searches as independent. Searches from the same user are correlated, so the true interval is wider than +1.13 to +1.27.

## Provenance
- Metric: CTR = clicks / searches, stated here [guess]. No metrics.json exists. Lift is treatment minus control, in percentage points.
- Data: experiment_daily (ranker_boost), 2026-09-17 to 2026-09-30, with 14 days present in both arms.
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: the check outputs are logged in `.ds-checks.log` in the working directory. The warehouse queries ran inline in Python and aren't saved in a file.