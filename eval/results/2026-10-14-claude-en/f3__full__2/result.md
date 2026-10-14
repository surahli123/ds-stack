## Answer
Headline: -1.82 pp (-1.97 to -1.67) [check:mix_shift#1]
Overall CTR fell from 30.44% to 28.61% week over week, and almost all of the fall is within-segment change rather than traffic mix, assuming v3 did not change who searches; the drop sits entirely in desktop (-3.0 pp) while mobile is flat [check:mix_shift#2].
- Observed: -1.83 pp (-1.98 to -1.68) [check:mix_shift#1]
- Adjusted: -1.82 pp (-1.97 to -1.67), holding platform x country mix fixed [check:mix_shift#1]
- Causal effect: not identified (v3 went to 100% on 2026-09-07 with no holdout, so ranker is perfectly confounded with week; a v2 holdout or a staggered/randomized rollout would identify it) [q4]

## What it means for the rollback decision
The whole interval is far below the 0.1 pp materiality floor used by the check [check:mix_shift#1], so the drop is real and not noise, but the data cannot say v3 caused it; the timing coincides with v3 and the drop is concentrated in desktop, which is consistent with a ranker effect but equally with any desktop-specific change on 09-07 [q5, check:mix_shift#2].

## Why we believe it
- Alternatives considered:
  - Traffic mix shift: ruled out, mix contributes -0.01 pp of -1.83 pp (about 1%), and a coarser grain agrees [check:mix_shift#1, check:mix_shift#2] [measured]
  - Incomplete data / day of week: ruled out, all 14 days have 4 of 4 segment rows and both windows are Monday-Sunday [q3, check:completeness#1] [measured]
  - Logging or definition change: not ruled out, release_log has only the v3 entry and cannot show tracking changes; a desktop-only step on 09-07 would fit either a tracking change or the ranker [q2, q5] [inferred]
  - v3 caused the drop (the PM's view): not ruled in or out, no concurrent v2 traffic exists so v3 is indistinguishable from anything else that changed on 09-07 [q4] [inferred]
  - Seasonality: not ruled out beyond same-weekday windows, only two weeks of data [q3] [inferred]
- Checks run:
  - mix_shift (platform x country): pass, within-segment -1.82 pp, mix -0.01 pp [check:mix_shift#1]
  - mix_shift (platform): pass, same result at coarser grain [check:mix_shift#2]
  - completeness: pass, 2026-09-13 has 4 rows, 100% of the trailing median [check:completeness#1]
  - fanout: skipped, no joins were used
  - srm: skipped, not a randomized experiment

## Caveats, and what would change the answer
- Intervals assume independent searches (se_assumes_independent_units), so they are somewhat too narrow; user-level clustering would settle it.
- The causal share of v3 is unknown: a v2 holdout, or desktop tracking and release changes on 2026-09-07 from engineering, would settle it.
- Only two weeks of data; the longer history would show normal week-to-week CTR variation.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) over search_daily, all platforms and countries, per week, stated here [guess]
- Data: search_daily, release_log, through 2026-09-13
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (30 numbers on 12 lines; 4 queries, 3 checks, 0 given)