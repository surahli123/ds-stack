## Answer
Headline: can't tell
Treatment's CTR is higher on its face, 31.20% against 30.00% for control, which is +1.20 percentage points. But the arms fail the sample-ratio check, so I can't trust that number as a causal lift.

## What it means for the ranker_boost launch decision
Don't use +1.2 pp as the launch number yet. First find out why treatment got about 4.8% fewer users than a 50/50 split should give. If that cause is related to the ranker or to who gets counted, the CTR gap may partly or wholly reflect which users ended up in each arm.

## Why we believe it
- Alternatives considered:
  - Real ranker effect: still possible, not ruled in. The raw gap is +1.20 pp (899,874/2,999,580 clicks per search in control vs 891,051/2,855,940 in treatment) [measured]. It's also stable every day, between +1.1 and +1.3 pp [measured]. The SRM failure means the arms aren't comparable, so this stays unconfirmed [inferred].
  - Selection or assignment bias from the user imbalance: not ruled out. Treatment has 475,990 users and control has 499,930, a 48.8/51.2 split with p≈1e-130 [measured]. I don't know which users are missing, so I can't say which way the CTR gap is biased [guess].
  - Day-of-week or seasonality: ruled out as the driver. Both arms follow the same day pattern, and the gap is the same on every day [measured].
  - Incomplete data: ruled out. All 14 days have both arms, and the last day is 100% of the trailing median [measured].
  - Mix shift across segments: could not be tested. The table has no segment columns [measured].
- Checks run:
  - srm: fail. Observed shares were 51.23% control and 48.77% treatment against a planned 50/50 (chi2 587, p≈1e-130). The arms aren't comparable until the cause is found.
  - completeness: pass. 2026-09-30 had 2 rows, 100% of the trailing median.
  - mix_shift: skipped. There is no segment breakdown in the data.
  - fanout: skipped. I ran no joins.
  - A first completeness run targeted 2026-10-01, which is outside the experiment window, so it failed. That was my mistake in picking the target and not a data problem. The run with the correct target passed.

## Caveats, and what would change the answer
- The data is daily aggregates only, so I can't compute a confidence interval. The rate is clicks per search, not per user, so it doesn't account for correlation within a user.
- Treatment has fewer users but a similar number of searches per user (6.0 per user in both arms). That points to users being dropped or not assigned, not to a change in behaviour [inferred].
- What would settle it: an assignment log showing why treatment lost users (for example, a logging or exposure filter that depends on the ranker, or a bucketing bug). With a fixed or explained split, I could re-read the lift. If the cause is unrelated to the ranker, the +1.2 pp would likely hold.