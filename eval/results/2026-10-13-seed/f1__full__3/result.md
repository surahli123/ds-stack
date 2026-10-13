## Answer
Headline: -0.00 pp attributable to v2 (95% interval -0.15 to +0.15 pp) [check:mix_shift#1]
Overall CTR fell 2.10 pp (30.42% to 28.32%) [check:mix_shift#1], but about 2.09 pp of that is a shift in traffic toward lower-CTR mobile (mobile share of searches 40% to 55%) [q5, check:mix_shift#2]; CTR within each platform/country segment did not change [check:mix_shift#1].

## What it means for the rollback decision
The within-segment (v2-attributable) interval of -0.15 to +0.15 pp [check:mix_shift#1] sits well inside the 2.10 pp drop [check:mix_shift#1], so the data give no support for rolling back on the basis of the CTR drop. No rollback threshold was given, so I used 0.1 pp, the check's minimum effect [check:mix_shift#1]. The interval is slightly wider than that, so a small v2 effect of ±0.15 pp can't be excluded.

## Why we believe it
- Alternatives considered:
  - Ranker v2 lowered CTR (PM's view): ruled out as the main driver; within-segment effect is -0.00 pp at segment grain [check:mix_shift#1] and -0.00 pp at platform grain [check:mix_shift#2] [measured]
  - Mix shift (platform/country): ruled in, about 100% of the drop at both grains [check:mix_shift#1, check:mix_shift#2] [measured]
  - Day of week / seasonality: ruled out for weekday composition, both windows are 7 full days Mon-Sun [q3] [inferred]; a week-over-week seasonal change in mobile share can't be excluded from 2 weeks of data [guess]
  - Data completeness: ruled out, 4 segment rows every day through 2026-10-04 [q3, check:completeness#1] [measured]
  - Logging or definition change: no entry in release_log other than the v2 rollout [q2] [measured]; unlogged tracking changes can't be excluded [guess]
- Checks run:
  - mix_shift (platform x country): flag, mix share 100%, within-segment -0.00 pp [check:mix_shift#1]
  - mix_shift (platform, coarser): flag, agrees with finer grain [check:mix_shift#2]
  - completeness: pass, last day 4 rows = 100% of trailing median [check:completeness#1]
  - fanout: skipped, no joins used
  - srm: skipped, not a randomized experiment, full rollout

## Caveats, and what would change the answer
- 100% rollout with no holdout: v2 and the mobile mix shift coincide in time, so I can't prove v2 did not cause the traffic shift (e.g. via latency or app behavior); a pre-rollout traffic-source breakdown or a v1 holdout would settle this.
- Intervals assume independent searches (clustering by user would widen them).
- Why mobile share rose 15 points in one week is unexplained; check marketing or app-release calendars.
- Only 2 weeks of data; no pre-period history to judge normal week-to-week mix variation.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) over search_daily, all platforms and countries, from stated here [guess]
- Data: search_daily, release_log, through 2026-10-04
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (24 numbers on 9 lines; 3 queries, 3 checks, 0 given)