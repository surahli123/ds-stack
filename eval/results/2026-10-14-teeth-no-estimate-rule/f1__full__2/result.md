I've finished the analysis and verified the readout. Here it is:

## Answer
Headline: -0.00 pp (-0.15 to +0.15) attributable to v2 after holding platform mix fixed [check:mix_shift#1]
Overall CTR fell 2.10 pp (30.42% to 28.32%, 95% CI -2.25 to -1.95) [check:mix_shift#1], but about 2.09 pp of that is a shift in traffic toward mobile, where CTR is about 22% versus about 36% on desktop; within-platform CTR did not move [check:mix_shift#1, q4].

## What it means for the rollback decision
The v2-attributable interval of -0.15 to +0.15 pp [check:mix_shift#1] is small against the 2.10 pp headline drop [check:mix_shift#1]; no rollback threshold was given, so I used the check's 0.1 pp minimum effect, which the interval spans, so a small v2 effect in either direction cannot be excluded [check:mix_shift#1]. The drop itself does not point to v2 as its cause.

## Why we believe it
- Alternatives considered:
  - Mix-shift (mobile share rose from 40.1% to 55.1% of searches): ruled in as the main driver, mix effect -2.09 pp [check:mix_shift#1, q4] [measured]
  - Finer grain (platform x country) disagreeing: ruled out, within-segment effect -0.00 pp, mix -2.09 pp [check:mix_shift#2, q5] [measured]
  - v2 lowering CTR (the PM's cause): ruled out as a large effect by flat within-platform rates (desktop 36.05% to 36.01%, mobile 22.02% to 22.06%) [check:mix_shift#1, q4] [measured]; a small effect is not excluded [inferred]
  - Data completeness: ruled out, all 14 days have 4 rows [check:completeness#1, q6] [measured]
  - Day of week: ruled out, both windows are full Monday-Sunday weeks [q3] [inferred]
  - Concurrent release or tracking change: ruled out only for logged changes, release_log lists only the v2 rollout [q2] [measured]; unlogged changes are not excluded [guess]
- Checks run:
  - completeness: pass 2026-10-04 has 4 rows, 100% of the trailing median [check:completeness#1]
  - mix_shift (platform): flag mix-dominant, within-segment -0.00 pp, mix -2.09 pp [check:mix_shift#1]
  - mix_shift (platform x country): flag same result at finer grain [check:mix_shift#2]
  - fanout: skipped, no joins were used
  - srm: skipped, not a randomized experiment; v2 went to all traffic

## Caveats, and what would change the answer
- No concurrent control: v2 is 100% from 2026-09-28, so it is confounded with date; a holdout on v1 or a staggered rollout would identify the v2 effect.
- The rise in mobile share is unexplained. If v2 itself pushed users to mobile, which I have no evidence for, part of the mix effect would be v2-related. Traffic-source or app-release data would settle it.
- Intervals assume independent searches; user-level clustering would widen them.
- Only one week on each side; the 0.1 pp materiality threshold is the check default, not a stated requirement.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), from search_daily, all platforms and countries, weekly [guess] (no metrics.json; DS_OVERLAY_DIR unset)
- Data: search_daily, release_log, through 2026-10-04
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (30 numbers on 9 lines; 5 queries, 3 checks, 0 given)