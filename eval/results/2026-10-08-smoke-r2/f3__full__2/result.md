Checking is done. I ran the completeness and mix-shift checks, and the numbers are below.

## Answer
Headline: -1.80 pp (week-over-week CTR change, 30.42% → 28.62%). This is the whole change. Attributing all of it to v3 is an inference.

Overall CTR fell 1.80 pp. All of the drop is in desktop (US -3.1 pp, other -2.9 pp). Mobile CTR is unchanged. The step happens on 2026-09-07, the day v3 went to 100% [measured].

## What it means for the rollback decision
v3 is the likeliest cause, because the drop starts on rollout day, nothing else is logged that day, and the mix of traffic didn't change. The data has no control group, though. If the roughly -1.8 pp loss is unacceptable, rolling back is justified. A short holdback of v2 on desktop would confirm the cause.

## Why we believe it
- Alternatives considered:
  - Mix shift (platform or country share): ruled out. Segment weights are identical across the two weeks (33/27/22/18%), so mix effect is 0.00 pp and the within-segment effect is -1.80 pp [measured].
  - Seasonality or day of week: ruled out. Both weeks cover Monday to Sunday. Daily CTR was steady at 30.1–30.7% before 09-07, then 28.3–28.9% on every day after it [measured]. A one-week-earlier baseline isn't available, so seasonality across weeks is not tested [inferred].
  - Incomplete data: ruled out. Every day has all 4 segment rows, and search volumes match day for day across the two weeks [measured].
  - Logging or definition change: not ruled out. Mobile CTR is exactly the same in both weeks (clicks 34,899 and 26,751 both weeks). Real behaviour is rarely that stable, so this may be a data artifact [inferred]. The release log has only the v3 entry [measured].
  - PM's cause (v3): consistent with the data but not isolated. v3 replaced v2 everywhere at once, so there is no concurrent control [measured]. The desktop-only drop could mean v3 hurts desktop only, or that something else changed on desktop [inferred].
- Checks run:
  - completeness: pass. 2026-09-13 has 4 rows, 100% of the trailing median.
  - mix_shift: pass. Change of -1.80 pp splits into -1.80 pp within-segment and +0.00 pp mix.
  - fanout: skipped. No joins were done.
  - srm: skipped. This was not a randomized experiment.

## Caveats, and what would change the answer
- Without a holdback, the -1.80 pp is a before/after change and not a causal estimate. A desktop-specific event on 09-07 other than v3 would change the attribution.
- The identical mobile figures need checking with whoever owns the logging. If mobile is stale or broken, the true overall change could differ.
- I have only two weeks of data, so there is no interval and no estimate of normal week-to-week variation.
- CTR is only a proxy. Check downstream outcomes such as conversion or satisfaction before deciding on rollback.