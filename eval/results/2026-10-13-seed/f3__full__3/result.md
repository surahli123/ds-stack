```
## Answer
Headline: -1.83 pp overall CTR change, week over week (95% interval -1.98 to -1.68) [check:mix_shift#1]
Overall CTR fell from 30.44% to 28.61% [check:mix_shift#1], and nearly all of it (-1.82 pp) is within-segment change, concentrated in desktop (-3.00 pp, 36.04% to 33.04%) while mobile was flat (-0.04 pp) [check:mix_shift#2]. The drop coincided with the v3 rollout; with a 100% rollout and no holdout, this is not an identified v3 effect.

## What it means for the rollback decision
The whole interval (-1.98 to -1.68 pp) is below the 0.1 pp smallest change the check treats as material [check:mix_shift#1], so the drop is real, but the data cannot separate v3 from anything else that changed on 2026-09-07; the only logged release that day is v3 [q2]. The desktop-only pattern is a lead worth checking before rolling back.

## Why we believe it
- Alternatives considered:
  - Mix-shift (platform x country): ruled out; mix effect is -0.01 pp, about 1% of the change, and a coarser grain (platform only) agrees [check:mix_shift#1, check:mix_shift#2] [measured]
  - Data completeness: ruled out; all 14 days have 4 rows each, and the last day is at 100% of baseline [q3, check:completeness#1] [measured]
  - Day of week / seasonality: ruled out as a main driver; both windows are full Mon-Sun weeks, and daily CTR sits at about 30-31% on every day before and 28-29% on every day after, with no overlap [q3] [measured]
  - Other release or logging change: no other release is in the release log [q2]; a desktop-only tracking change is not testable from this data [inferred]
  - PM's cause (v3 lowered CTR): consistent, since the shift is sharp at the rollout date, but not identified, as there is no holdout and the ranker is fully confounded with time [q3, q4] [inferred]
- Checks run:
  - mix_shift (platform x country): pass; within-segment -1.82 pp, mix -0.01 pp [check:mix_shift#1]
  - mix_shift (platform): pass; same result at the coarser grain [check:mix_shift#2]
  - completeness: pass; 2026-09-13 has 4 of 4 expected rows [check:completeness#1]
  - fanout: skipped; no joins were used
  - srm: skipped; not a randomized experiment

## Caveats, and what would change the answer
- The attribution to v3 is not identified: all traffic switched at once. A holdout or a staggered/partial rollback on a slice of traffic would settle it.
- Mobile unchanged while desktop dropped about 3 pp is unusual for a ranker change; check for a desktop-specific logging or UI change on 2026-09-07 or a desktop-specific v3 regression.
- The interval assumes independent searches; correlated users would widen it. Only 14 days, one week per side.
- CTR is searches with a click over searches (clicks/searches); whether the click count is deduplicated per search is unverified, and CTR is a proxy for result quality.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches), search_daily, all platforms and countries, stated here [guess] (no metrics.json)
- Data: search_daily, release_log, through 2026-09-13
- Reconciled: not done (no dashboard or reference figure available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (27 numbers on 8 lines; 3 queries, 3 checks, 0 given)
```