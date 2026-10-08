## Answer
Headline: can't tell
The raw CTF gap is +1.2 pp (treatment 31.2% vs control 30.0%, clicks per search). The assignment split failed its sample-ratio check, so I can't treat that gap as the effect of the ranker.

## What it means for the launch decision
Don't use the +1.2 pp number for the launch decision. Find out why treatment got about 4.8% fewer users than control, then re-read the result.

## Why we believe it
- Alternatives considered:
  - Real treatment effect: not ruled in. The arms aren't comparable, so the gap could come from who was assigned rather than from the ranker [inferred].
  - Random split noise: ruled out by the SRM test. Users were 499,930 control vs 475,990 treatment (51.2% vs 48.8%, planned 50/50), chi2 587, p≈1e-129 [measured].
  - Incomplete data for the last days: ruled out. All 14 days have both arms, and 2026-09-30 has 100% of the usual rows [measured].
  - Cause of the imbalance (for example, users dropped from treatment, or a logging or bucketing bug): not investigated. The table only has daily aggregates, so I can't test it [guess].
- Checks run:
  - srm: fail. p≈1e-129, treatment is short by about 24,000 users.
  - completeness: pass. 2026-09-30 is fully loaded.
  - mix_shift: skipped. There are no segment breakdowns in the data.
  - fanout: skipped. I ran no joins.

## Caveats, and what would change the answer
- The CTF figures are clicks/searches pooled over the 14 days. No variance or confidence interval is possible from daily aggregates, so I report none.
- Searches per user are identical in both arms (6.0), so the gap is not a heavier-searcher effect [measured].
- If the cause of the missing treatment users is found and is unrelated to click behavior, the +1.2 pp could stand. If treatment lost low-engagement users, the lift is overstated.
- User-level assignment logs would let me find the cause and recompute the lift properly.