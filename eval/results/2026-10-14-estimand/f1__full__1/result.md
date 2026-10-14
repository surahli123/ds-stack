## Answer
Headline: -0.00 pp (-0.15 to +0.15) [check:mix_shift#1]
Overall CTR fell 2.10 pp, but essentially all of it is a shift in traffic toward lower-CTR mobile; within-platform CTR did not change, assuming v2 did not itself cause the mobile shift [check:mix_shift#1].
- Observed: -2.10 pp (-2.25 to -1.95) [check:mix_shift#1]
- Adjusted: -0.00 pp (-0.15 to +0.15), holding platform mix fixed [check:mix_shift#1]
- Causal effect: not identified (no randomized holdout; the rollout was all-at-once, so the ranker change is confounded with the calendar week. A holdout or staggered rollout would identify it)

## What it means for the rollback decision
The within-platform effect is -0.00 pp with an interval of -0.15 to +0.15 pp, so a within-platform loss larger than about 0.15 pp is unlikely [check:mix_shift#1]; the data show no sign that v2 lowered CTR, so the drop alone is not a reason to roll back. No business threshold for the smallest harmful change was provided, so that is for you to set.

## Why we believe it
- Alternatives considered:
  - Mix-shift: ruled in. Mobile share of searches rose from 40.1% to 55.1% while mobile CTR (22.0%) is far below desktop (36.0%); mix effect is -2.09 pp of -2.10 pp [q4, check:mix_shift#1] [measured]
  - Finer grain (platform x country): agrees, within-segment -0.00 pp (-0.15 to +0.15), mix -2.09 pp [q5, check:mix_shift#2] [measured]
  - v2 lowered CTR (PM's cause): not supported; desktop CTR 36.05% to 36.01%, mobile 22.02% to 22.06% [check:mix_shift#1] [measured]
  - Data completeness: ruled out, all 14 days have 4 platform x country rows [q6, check:completeness#1] [measured]
  - Day of week/seasonality: not ruled out; both windows are full Mon-Sun weeks, but only 2 weeks exist so no seasonal baseline [q3] [inferred]
  - v2 caused the mobile traffic shift: not ruled out; the shift began on the rollout date, and nothing in the data separates it from other changes. Release log shows only the v2 rollout that day [q2, q4] [inferred]
- Checks run:
  - completeness: pass, 2026-10-04 has 4 rows, 100% of trailing median [check:completeness#1]
  - mix_shift (platform): flag, mix-dominant, mix share 100% [check:mix_shift#1]
  - mix_shift (platform x country): flag, same conclusion [check:mix_shift#2]
  - fanout: skipped, no joins were used
  - srm: skipped, not a randomized experiment

## Caveats, and what would change the answer
- Mix shift to mobile coincided with the v2 rollout; if v2 caused it (e.g. a UI change driving mobile traffic), then v2 would be indirectly responsible for the overall drop. Check the traffic source/mobile marketing calendar to settle that.
- Only two weeks of data; no seasonality baseline. Earlier weeks would show whether the mobile share was already trending up.
- Intervals assume independent searches; user-level clustering would widen them.
- Before/after comparison with no control; a small v2 effect under 0.15 pp cannot be excluded.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) from search_daily, all platforms and countries, daily rows summed per week [guess]; no metrics.json available (DS_OVERLAY_DIR unset)
- Data: search_daily, release_log, through 2026-10-04
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (34 numbers on 12 lines; 5 queries, 3 checks, 0 given)