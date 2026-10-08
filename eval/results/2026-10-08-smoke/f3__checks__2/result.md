## Answer
Headline: -1.80 pp (overall CTR 30.42% → 28.62%; no interval, since the data is daily aggregates with no sampling-error model)
Overall CTR fell 1.80 pp week over week. None of the drop comes from traffic mix. All of it is a desktop CTR drop (about -3.1 pp on desktop) that began the day v3 launched. Mobile CTR did not change at all. [measured]

## What it means for the rollback decision
v3 is the most likely cause of the desktop drop, so it is plausible that most or all of the -1.8 pp is attributable to v3. This is inferred, not proven, because 100% of traffic moved at once and there was no holdout. If the desktop CTR loss matters more than whatever v3 is meant to gain, a rollback or a desktop-only rollback is justified. A short desktop holdout on v2 would confirm it.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform or country share): ruled out. Searches per segment are identical across the two weeks and the mix effect is 0.00 pp. [measured]
  - Mobile or country-specific problem: ruled out. Mobile clicks are identical week to week and the drop is spread across desktop US (-3.1 pp) and desktop other (-2.9 pp). [measured]
  - A coincident non-v3 cause (seasonality, a desktop outage, tracking change): not ruled out. The release log has only the v3 entry and there is no control group. A drop confined to desktop, starting on the rollout day, fits v3 well. I could not separate it from a desktop-specific coincident event. [inferred]
  - Mobile is unaffected by v3 (so the effect is desktop-only): this is a guess. It would be odd for the ranker to change only one platform, so the mobile data may be flat for another reason, such as a logging quirk. [guess]
- Checks run:
  - mix_shift: pass. The -1.80 pp change is entirely within-segment and mix contributes 0%.
  - completeness: could not run. It needs at least 3 prior periods and the data has only 2 weeks. Both weeks have all 14 days and all 4 segments each day (56 rows), so they look complete. [measured]
  - srm: skipped. This is not a randomized experiment, so there is no assignment split to test.
  - fanout: skipped. No joins were used.

## Caveats, and what would change the answer
- With no concurrent control, "attributable to v3" is a before/after comparison and cannot be tested statistically here.
- Two weeks of data only. Any pre-existing desktop trend or weekly pattern can't be assessed.
- A v2 holdout, or desktop logs from other weeks, would change the answer. Evidence of a desktop-specific event around 2026-09-07 would lower the share attributable to v3.
- The mobile result is suspiciously identical week to week (the same clicks every day). That deserves a check of the data pipeline.