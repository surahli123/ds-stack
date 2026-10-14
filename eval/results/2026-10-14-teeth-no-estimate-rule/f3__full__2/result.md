## Answer
Headline: -1.83 pp (95% CI -1.98 to -1.68) [check:mix_shift#1]
Overall CTR fell from 30.44% to 28.61% between the two weeks, and almost all of it is a desktop drop that starts on the v3 rollout day; the change coincided with v3, but with a 100% rollout and no holdout the data cannot isolate v3's share exactly [check:mix_shift#2, q6].

## What it means for the rollback decision
The whole interval (-1.98 to -1.68 pp) is far beyond the 0.1 pp smallest change the check treats as meaningful [check:mix_shift#1], so the drop is real; whether v3 is responsible rests on timing and the desktop-only pattern, not on a randomized comparison. A rollback or a small holdout of v2 on desktop would confirm it.

## Why we believe it
- Alternatives considered:
  - Mix-shift (platform/country mix): ruled out, mix effect is -0.01 pp of -1.83 pp (about 1%) at platform x country and at platform grain [check:mix_shift#1, check:mix_shift#2] [measured]
  - Data completeness: ruled out, all 14 days have 4 rows and the last day is complete [q3, check:completeness#1] [measured]
  - Day of week / seasonality: ruled out as a main driver, both windows are Mon-Sun, and daily clicks are flat within week 1 and step down on 2026-09-07 [q3] [inferred]
  - Logging or definition change: not ruled out, release_log lists only the v3 rollout but the log may be incomplete [q2] [inferred]
  - v3 caused the drop (PM view): ruled in as most plausible, not proven; desktop CTR fell 36.04% to 33.04% while mobile was flat, 22.02% to 21.98%, and v3 was the only logged change [q4, q2, check:mix_shift#2] [inferred]
- Checks run:
  - completeness: pass 2026-09-13 has 4 rows, 100% of the median [check:completeness#1]
  - mix_shift (platform x country): pass within-segment -1.82 pp, mix -0.01 pp [check:mix_shift#1]
  - mix_shift (platform): pass same result at coarser grain [check:mix_shift#2]
  - fanout: skipped, no joins were used
  - srm: skipped, not a randomized experiment

## Caveats, and what would change the answer
- v3 went to 100% at once, so there is no concurrent control; any desktop-specific change on 2026-09-07 (client release, tracking) would look the same. Settle it with a v2 holdout or a check of desktop client/logging changes.
- Interval assumes independent searches (check note); real uncertainty is wider.
- Only two weeks compared; the effect could drift (novelty).
- Clicks per search may not reflect result quality; a lower CTR can occasionally mean users find answers faster.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), all platforms and countries, from search_daily, stated here [guess] (no metrics.json available)
- Data: search_daily, release_log, through 2026-09-13
- Reconciled: not done (no dashboard or source figure available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (23 numbers on 9 lines; 4 queries, 3 checks, 0 given)