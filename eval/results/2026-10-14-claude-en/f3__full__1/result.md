## Answer
Headline: -1.82 pp (95% CI -1.97 to -1.67) [check:mix_shift#1]
Overall CTR fell from 30.44% to 28.61% week over week, and almost none of it is traffic mix; if v3 is the only thing that changed for desktop searches, this is v3's effect, but nothing here can separate it from other changes that week. [check:mix_shift#1]
- Observed: -1.83 pp (95% CI -1.98 to -1.68) [check:mix_shift#1]
- Adjusted: -1.82 pp (95% CI -1.97 to -1.67), holding platform x country mix fixed [check:mix_shift#1]
- Causal effect: not identified (v3 went to full traffic on 2026-09-07 with no holdout, so the ranker is perfectly confounded with the week; a v2 holdout or a staggered/randomized rollout would identify it) [q2]

## What it means for the rollback decision
The whole drop is on desktop (-3.00 pp, 36.04% to 33.04%) while mobile is flat (-0.04 pp, 22.02% to 21.98%) [q5, check:mix_shift#2]. No rollback threshold was given, so any change much beyond the 0.1 pp noise floor [check:mix_shift#1] would count; the interval (-1.97 to -1.67) is far outside it, so the drop is real, but whether v3 is the cause is not established.

## Why we believe it
- Alternatives considered:
  - Mix-shift (platform/country): ruled out, mix contributes -0.01 pp of -1.83 pp at both the 4-cell and 2-cell grain [check:mix_shift#1, check:mix_shift#2] [measured]
  - Data completeness: ruled out, all 14 days have 4 rows and search volume is flat (about 700k per week) [q3, q4, check:completeness#1] [measured]
  - Day of week/seasonality: weak evidence only, both windows are Mon-Sun with similar daily volumes, but there is only one week of history on each side [q3] [inferred]
  - Logging or definition change: not ruled out, release_log lists only the v3 rollout, but it may be incomplete and a desktop-only change could be a tracking or UI change [q2] [guess]
  - v3 caused the drop (the PM's view): consistent but not testable, since v3 coincided with the week boundary and the desktop-only pattern could also fit a desktop-specific change shipped the same day [q4, q5] [inferred]
- Checks run:
  - mix_shift (platform x country): pass, within-segment -1.82 pp, mix -0.01 pp [check:mix_shift#1]
  - mix_shift (platform): pass, same result at the coarser grain [check:mix_shift#2]
  - completeness: pass, 2026-09-13 has 4 of 4 expected rows [check:completeness#1]
  - fanout: skipped, no joins were used
  - srm: skipped, this is not a randomized experiment

## Caveats, and what would change the answer
- Interval treats searches as independent units; sessions/users clustering would widen it. Per-user data would settle this.
- Only one week on each side, with no earlier weeks to show normal week-to-week CTR variation. Several prior weeks would show it.
- The desktop-only drop points to a desktop-specific cause (v3 on desktop or something else). Desktop CTR by ranker in a holdout, or a changelog check for desktop changes on 09-07, would settle it.
- Observed, Adjusted and any v3 effect are descriptive: the data cannot attribute the drop to v3.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) over search_daily, all platforms and countries, weekly, from stated here [guess]
- Data: search_daily, release_log, through 2026-09-13
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (31 numbers on 9 lines; 4 queries, 3 checks, 0 given)