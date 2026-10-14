Readout is written and verified. I'm sending it as the final reply.

## Answer
Headline: -0.00 pp (-0.15 to +0.15) attributable to v2, as the within-platform CTR change [check:mix_shift#1]
Overall CTR fell 2.10 pp (30.42% to 28.32%) [check:mix_shift#1], but about 2.09 pp of that is a shift toward mobile (40% to 55% of searches), which has a lower CTR; within desktop and mobile CTR did not move [check:mix_shift#1, q6].

## What it means for the rollback decision
The v2-attributable interval (-0.15 to +0.15 pp) [check:mix_shift#1] rules out any within-segment loss larger than about 0.15 pp; the minimum effect the check treats as material is 0.1 pp [check:mix_shift#1], so a small loss near that size is not fully excluded. The 2.10 pp drop is not evidence against v2, and rolling back would not be expected to restore it. [check:mix_shift#1]

## Why we believe it
- Alternatives considered:
  - Mix-shift (platform): ruled in as the main explanation, mix effect -2.09 pp of -2.10 pp [check:mix_shift#1] [measured]
  - Mix-shift at finer grain (platform x country): agrees, mix -2.09 pp, within-segment -0.00 pp [check:mix_shift#2] [measured]
  - v2 lowered CTR (PM's view): ruled out as the source of the headline drop, within-segment effect -0.00 pp (-0.15 to +0.15) [check:mix_shift#1] [measured]
  - Data completeness: ruled out, all 7 days of the later week have the full 4 rows [check:completeness#1] [measured]
  - Day of week/seasonality: ruled out for composition, both windows are 7 full days covering each weekday once [q3] [inferred]
  - Logging/definition change: ruled out only for the release log, which lists v2 as its single entry [q2] [measured]; unknown beyond that [guess]
  - v2 caused the mobile traffic shift: not ruled out, no data on why mobile share rose [q6] [guess]
- Checks run:
  - mix_shift (platform): flag, mix-dominant, overall -2.10 pp = within -0.00 + mix -2.09 [check:mix_shift#1]
  - mix_shift (platform x country): flag, same split at finer grain [check:mix_shift#2]
  - completeness: pass, 2026-10-04 has 4 rows = 100% of the trailing median [check:completeness#1]
  - fanout: skipped, no joins were used
  - srm: skipped, v2 rolled out to all traffic at once, so there is no randomized assignment

## Caveats, and what would change the answer
- This is a before/after comparison with no concurrent v1 control, so v2 is not identified causally; a holdout or A/B on v1 vs v2 would settle it.
- If v2 itself drove the shift of searches to mobile (e.g. changed traffic routing or query mix), part of the mix effect would be v2's; product/traffic-source data on the mobile increase would settle it.
- Interval assumes independent searches (daily clustering ignored), so it is likely somewhat too narrow [check:mix_shift#1].
- Only one week per side; no metrics.json was available, so the CTR definition is my own.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) over all rows of search_daily, per week, stated here [guess]
- Data: search_daily, release_log, through 2026-10-04
- Reconciled: not done (no dashboard or reference figure available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (29 numbers on 10 lines; 3 queries, 3 checks, 0 given)