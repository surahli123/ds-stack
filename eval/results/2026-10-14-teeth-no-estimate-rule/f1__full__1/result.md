## Answer
Headline: -0.00 pp (-0.15 to +0.15) within-segment change, the part of the CTR move that v2 could account for [check:mix_shift#1]
Overall CTR fell 2.10 pp (30.42% to 28.32%, CI -2.25 to -1.95), but 2.09 pp of that is a shift toward mobile, which has a lower CTR; within platform×country CTR did not change [check:mix_shift#1, q3].

## What it means for the rollback decision
The v2 interval (-0.15 to +0.15 pp) excludes a loss as large as the observed 2.10 pp drop [check:mix_shift#1]; the smallest change that would justify a rollback was not given, but a loss above 0.15 pp is not supported by this data [check:mix_shift#1]. Mobile's share of searches rose from 40% to 55% [check:mix_shift#2], and that shift, not v2, accounts for the drop.

## Why we believe it
- Alternatives considered:
  - Mix-shift (platform/country): ruled in by mix share 99.9% at platform×country and 99.8% at platform alone, with the two grains agreeing [check:mix_shift#1, check:mix_shift#2] [measured]
  - v2 lowered CTR (the PM's cause): ruled out as the main driver because within-segment CTR is flat in all 4 segments (e.g. mobile-US 22.66% to 22.71%) [check:mix_shift#1, q4] [measured]
  - Day of week/seasonality: ruled out for the weekday pattern, since both windows are Mon-Sun and daily CTR is stable within each week [q3] [inferred]; longer seasonality can't be seen with 2 weeks of data [guess]
  - Data completeness: ruled out; 4 rows per day on all 14 days [q3] [measured]
  - Logging or definition change: ruled out as far as the release_log shows, since it lists only the v2 rollout [q2] [inferred]
- Checks run:
  - completeness: could not run; needs 3 earlier weeks of history, only 2 available, so row counts were checked by hand [check:completeness#1]
  - mix_shift (platform×country): flag, mix -2.09 pp, within-segment -0.00 pp [check:mix_shift#1]
  - mix_shift (platform): flag, mix -2.09 pp, within-segment -0.00 pp [check:mix_shift#2]
  - fanout: skipped, no joins were used
  - srm: skipped, this is not a randomized experiment

## Caveats, and what would change the answer
- v2 went to 100% of traffic with no holdout, so there is no concurrent control. "No within-segment effect" is a before/after comparison; a holdout or a staggered rollout would confirm it.
- Why mobile share rose is unknown. If v2 itself pushed users to mobile it would be an indirect effect, which seems unlikely but isn't tested; a traffic-source breakdown would settle it.
- Only 2 weeks and 4 coarse segments are available; the interval assumes independent units, so it is probably somewhat too narrow.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches), from search_daily, all platforms and countries [guess]; no metrics.json (DS_OVERLAY_DIR unset)
- Data: search_daily, release_log, through 2026-10-04
- Reconciled: not done (no dashboard figure available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (29 numbers on 10 lines; 3 queries, 3 checks, 0 given)