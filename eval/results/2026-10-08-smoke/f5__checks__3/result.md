## Answer
Headline: can't tell
The raw CTR is higher in treatment (31.20% vs 30.00%, +1.20 pp, naive 95% CI ±0.07 pp). The arms fail the sample-ratio check, so I can't trust that number as a treatment effect.

## What it means for the launch decision
Don't use +1.2 pp for the launch decision yet. Users are split 51.2% control and 48.8% treatment instead of 50/50, and until the cause is found the arms aren't comparable. The lift could be real, partly biased, or zero. [inferred]

## Why we believe it
- Alternatives considered:
  - Real treatment effect: not ruled out. Raw CTR is 0.3000 for control and 0.3120 for treatment, and the gap is steady across all 14 days. [measured]
  - Biased assignment or logging, such as users dropped from treatment or bot filtering applied unevenly: not ruled out. The SRM check fails (499,930 vs 475,990 users, p≈1e-130). Control users per day are constant at about 35.7k and treatment at about 34.0k, which points to a systematic cause rather than noise. [measured, cause inferred]
  - Random noise: ruled out as the cause of the lift. The naive interval is tight (±0.07 pp), but it assumes valid randomization. [measured]
  - Searches per user differ between arms: ruled out. It is 6.0 in both. [measured]
- Checks run:
  - srm: fail. chi2 587, p≈1e-130, observed share 51.2/48.8.
  - completeness: could not run. The table has only the experiment window, so there is no prior-period series to test against. The 14 days all have rows for both arms.
  - mix_shift: skipped. There are no segment columns in the data.
  - fanout: skipped. I did no joins.

## Caveats, and what would change the answer
- CTR here is clicks divided by searches, pooled. I only have daily aggregates, so I can't compute user-level variance or clustered intervals. The real interval is wider than ±0.07 pp. [measured]
- If the data owners explain the SRM, for example by showing the missing treatment users are unrelated to CTR, or by fixing the logging, I can re-run the analysis. The +1.2 pp could then stand.
- Per-user or per-segment data would let me check which users are missing from treatment.