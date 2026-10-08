## Answer
Headline: can't tell
Treatment's raw CTR is 31.20% against 30.00% for control, a gap of +1.20 percentage points. The arms failed the sample-ratio check, so I can't treat that gap as the effect of the ranker.

## What it means for the ranker_boost launch decision
Don't use +1.2 pp as the launch number yet. Find out why treatment has about 4.8% fewer users than control, then re-read the lift.

## Why we believe it
- Alternatives considered:
  - Real ranker effect: not ruled in. The gap is stable, +1.1 to +1.3 pp every day, so it isn't noise, but the arms aren't comparable. [measured]
  - Assignment or logging problem that drops treatment users: not ruled out. Users split 499,930 vs 475,990 (51.2% / 48.8%) against a planned 50/50. If the missing users are non-random, for example low-engagement users or users who bounce, CTR in treatment is inflated. [measured for the split; inferred for the mechanism]
  - Day-of-week or seasonality: ruled out. Both arms have the same daily pattern, and the gap is similar on every day. [measured]
  - Incomplete data: ruled out. All 14 days have both arms, and the last day is 100% of the trailing median. [measured]
  - Mix shift across segments: could not assess. The table has no segment columns. [measured]
- Checks run:
  - srm: fail. chi2 587, p ≈ 1e-129. Arms are not comparable until the cause is found.
  - completeness: pass. 2 of 2 expected rows on 2026-09-30, so the period is complete.
  - fanout: skipped. No joins were done.
  - mix_shift: skipped. There are no segment dimensions in the data.

## Caveats, and what would change the answer
- The table is aggregated daily by arm. It has no user-level or assignment-level data, so I can't see who is missing from treatment.
- If the cause is benign and unrelated to CTR (for example, a logging bug that drops users at random), the +1.2 pp would stand. That needs confirming.
- To settle it: check the assignment and exposure logs for treatment-only drops, and rerun the comparison on the users who were assigned, not the users who were logged. A corrected rerun is also an option.