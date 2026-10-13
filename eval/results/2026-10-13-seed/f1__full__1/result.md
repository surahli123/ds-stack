```
## Answer
Headline: -0.00 pp (95% interval -0.15 to +0.15 pp) attributable to v2, within-segment [check:mix_shift#1]
Overall CTR fell 2.10 pp (30.42% to 28.32%) [check:mix_shift#1], but about 2.09 pp of that is a shift in traffic toward mobile, which has a much lower CTR, and the like-for-like change within desktop and within mobile is about zero [check:mix_shift#1].

## What it means for the rollback decision
The drop is not evidence against v2: the within-segment effect interval of -0.15 to +0.15 pp [check:mix_shift#1] is small next to the 2.10 pp drop, so a rollback would not recover it. No rollback threshold was given, so a harm of 0.1 pp or more cannot be fully excluded by this interval [check:mix_shift#1].

## Why we believe it
- Alternatives considered:
  - Mix shift (mobile share 40.1% to 55.1%; mobile CTR 22.0% vs desktop 36.0%): ruled in as the explanation by the decomposition, mix effect -2.09 pp, share 99.8% [check:mix_shift#1] [measured]
  - v2 degraded relevance (PM's cause): ruled out as the main driver, since desktop moved 36.05% to 36.01% and mobile 22.02% to 22.06% [q6, check:mix_shift#1] [measured]
  - Finer grain (platform x country) disagrees: ruled out, it gives the same split, within-segment -0.00 pp and mix -2.09 pp [q5, check:mix_shift#2] [measured]
  - Incomplete data or logging change: ruled out, all 14 days have 4 rows and the last day is at 100% of the median [q3, check:completeness#1, check:completeness#2] [measured]
  - Seasonality or day of week: ruled out, both windows are Mon-Sun and the daily CTR steps down on 09-28 and stays level [q3] [inferred]
  - Other concurrent change: ruled out as far as the log shows, which lists only the v2 rollout [q2] [measured]
- Checks run:
  - mix_shift (platform): flag, mix-dominant, within-segment -0.00 pp [check:mix_shift#1]
  - mix_shift (platform x country): flag, same result at a finer grain [check:mix_shift#2]
  - completeness (post week): pass [check:completeness#1]
  - completeness (pre week): pass [check:completeness#2]
  - fanout: skipped, no joins were used
  - srm: skipped, this is not an experiment

## Caveats, and what would change the answer
- 100% rollout with no holdout, so the within-segment effect is a before/after comparison, not a causal estimate. A holdout or a v1/v2 split would confirm it.
- The interval assumes independent searches (flagged by the check), so it is likely a little narrow.
- Why mobile share rose is unknown. If v2 itself shifted traffic to mobile, the mix part would be indirectly due to v2. Nothing here suggests it, but traffic-source data would settle it.
- Platform and country are the only segments available; other unseen mix changes (query type) are not covered.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) over search_daily, all platforms and countries, weekly window, from stated here [guess]
- Data: search_daily, release_log, through 2026-10-04
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (29 numbers on 9 lines; 4 queries, 4 checks, 0 given)
```