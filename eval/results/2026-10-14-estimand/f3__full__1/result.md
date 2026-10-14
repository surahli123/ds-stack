## Answer
Headline: -1.82 pp (-1.97 to -1.67) [check:mix_shift#1]
Overall CTR fell from 30.44% to 28.61% week over week, and nearly all of that is a within-segment drop concentrated in desktop; it coincided with the v3 rollout but the data cannot show v3 caused it. [check:mix_shift#1, q4]
- Observed: -1.83 pp (-1.98 to -1.68) [check:mix_shift#1]
- Adjusted: -1.82 pp (-1.97 to -1.67), holding platform mix fixed [check:mix_shift#1]
- Causal effect: not identified (v3 went to all traffic at once, so ranker is fully confounded with week; a holdout or staggered/split rollout would identify it)

## What it means for the rollback decision
The drop is far larger than the 0.1 pp minimum effect the check treats as material [check:mix_shift#1], and the whole interval is below zero; desktop fell -1.80 pp while mobile moved -0.02 pp [check:mix_shift#1]. Rollback is plausible, but the interval measures the week-over-week change, not v3's effect; a short v2 holdout on desktop would settle it.

## Why we believe it
- Alternatives considered:
  - Platform/country mix shift: ruled out; mix effect is -0.01 pp (1% of the change) at platform grain and at platform x country grain [check:mix_shift#1, check:mix_shift#2] [measured]
  - Data completeness: ruled out for row coverage; both weeks have 4 segment rows on all 14 days [q3] [measured]
  - Day of week: ruled out; both windows are 7 full days, Mon-Sun [q3] [inferred]
  - Logging/definition change: not ruled out; release_log lists only the v3 rollout, but a tracking change in desktop is untested [q2] [guess]
  - Seasonality or other concurrent change: not ruled out; only two weeks of data, no earlier baseline [q3] [inferred]
  - v3 caused the drop (PM's view): consistent, not confirmed; the drop is desktop-only, v2 only appears before and v3 only after [q4] [inferred]
- Checks run:
  - completeness: could not run, only 1 earlier week of history, needs 3 [check:completeness#1]
  - mix_shift (platform): pass, within-segment -1.82 pp, mix -0.01 pp [check:mix_shift#1]
  - mix_shift (platform x country): pass, same split at finer grain [check:mix_shift#2]
  - fanout: skipped, no joins used
  - srm: skipped, not a randomized experiment

## Caveats, and what would change the answer
- No concurrent control: ranker equals week, so any desktop-specific change that week is inseparable from v3. A v2 holdout would settle it.
- Intervals assume independent searches (the check says so); day-level correlation would widen them.
- Only two weeks of data, so normal week-to-week variation is unknown; earlier weeks would give that.
- The desktop-only pattern could be a v3 desktop effect or a desktop logging change; engineering confirmation of click tracking would help.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) over search_daily, all platforms and countries, from stated here [guess]
- Data: search_daily, release_log, through 2026-09-13
- Reconciled: not done (no dashboard figure or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (23 numbers on 10 lines; 3 queries, 3 checks, 0 given)