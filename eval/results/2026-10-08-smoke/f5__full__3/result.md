Both checks are back. The sample-ratio check failed, so I'm writing the readout now.

## Answer
Headline: can't tell
The raw treatment CTR is 31.20% against 30.00% for control, which is +1.20 pp (measured). The arms fail the sample-ratio check, so I can't treat that gap as the effect of the ranker.

## What it means for the ranker_boost launch decision
Don't use +1.2 pp in the launch decision yet. The arms are not comparable until we know why treatment got about 4.8% fewer users than control, and the missing users could be inflating or deflating the lift.

## Why we believe it
- Alternatives considered:
  - Real lift from the ranker: not ruled out. The raw gap is steady every day, +1.1 to +1.3 pp (measured), but a biased split can produce a steady gap too. [inferred]
  - Biased assignment or logging, where treatment loses users: ruled in as a live problem. Treatment has 475,990 users and control has 499,930, a 48.8/51.2 split against the planned 50/50 (measured). The shortfall is the same every day, which points to a systematic cause such as a dropped user segment, a bot filter or a logging gap. [inferred]
  - Day-of-week or seasonality: ruled out as the source of the gap. Both arms follow the same weekly pattern and treatment is above control on all 14 days (measured).
  - Incomplete data: ruled out. All 14 days are present with both arms (measured).
  - Mix shift across segments: could not be checked. The table has no platform, country or source breakdown.
  - Searches per user: treatment and control both run at 6.0 (measured), so the CTR gap is not explained by a difference in search volume per user. [inferred]
- Checks run:
  - srm: fail. chi2 587, p ≈ 1e-129, observed share 0.512 vs 0.488.
  - completeness: pass. 2026-09-30 has 2 rows, 100% of the trailing median.
  - mix_shift: could not run. There are no segment columns in `experiment_daily`.
  - fanout: skipped. I ran no joins.

## Caveats, and what would change the answer
- The only table is `experiment_daily`, with daily aggregates and no user-level or segment data. That means I can't find which users are missing from treatment.
- Find out why treatment has fewer users: assignment logic, exposure logging, filters applied to one arm only, or a crash or redirect in the treatment path. If the cause is benign and unrelated to CTR, the +1.2 pp is probably usable. If the missing users would have clicked less, the true lift is smaller.
- Rerun the experiment, or get user-level data with a segment breakdown, to settle it.
- The +1.2 pp is a raw difference in clicks per search, with no confidence interval. I didn't compute one because the arms aren't comparable.