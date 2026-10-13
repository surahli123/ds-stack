## Answer
Headline: -1.83 pp overall CTR, week of 09-07 vs week of 08-31 (95% CI -1.98 to -1.68) [check:mix_shift#1]
CTR fell from 30.44% to 28.61%. All of the drop is within-segment (mix effect -0.01 pp). It is concentrated in desktop (-3.0 pp), while mobile is flat (-0.04 pp). This coincided with the v3 rollout, but this design cannot isolate v3 as the cause [check:mix_shift#2, q6].

## What it means for the rollback decision
The interval (-1.98 to -1.68 pp) is far beyond the 0.1 pp smallest effect the check treats as material [check:mix_shift#1], so the drop is real. Whether v3 is responsible is not identified. v3 went to 100% of traffic with no holdout, so the week-over-week change is the most v3 could account for, not a measured v3 effect [q4].

## Why we believe it
- Alternatives considered:
  - Mix shift (platform/country): ruled out. Mix explains 1% of the change, and the platform-only and platform×country grains agree [check:mix_shift#1, check:mix_shift#2] [measured]
  - Data completeness: ruled out. All 14 days have 4 rows (2 platforms × 2 countries) [check:completeness#1, q3] [measured]
  - Day of week/seasonality: partly ruled out. Both windows are full Mon–Sun weeks and daily searches are stable (~96–103k) across both [q3]. There are only two weeks of history, so seasonality is not fully excluded [inferred]
  - Logging/definition change: not ruled out. release_log lists only the v3 rollout, but it may be incomplete [q2] [inferred]
  - v3 caused it (PM's view): consistent with the data but not identified. The drop is desktop-only (36.0% to 33.0%) while mobile is unchanged (22.0% to 22.0%) [q6]. So either v3 hurts desktop only, or a desktop-specific change coincided with it [inferred]
- Checks run:
  - mix_shift: pass. Within-segment -1.82 pp, mix -0.01 pp [check:mix_shift#1]
  - mix_shift (coarser grain, platform): pass. Agrees with the finer grain [check:mix_shift#2]
  - completeness: pass. 2026-09-13 is at 100% of the usual rows [check:completeness#1]
  - fanout: skipped. No joins were used.
  - srm: skipped. This is not an experiment.

## Caveats, and what would change the answer
- There is no holdout, so ranker is perfectly confounded with week. A v2 holdout or a desktop-only A/B on v3 would identify the effect.
- Check the desktop client/UI, tracking and traffic-source changes for 09-07. They are not in release_log.
- The interval assumes independent searches. Clustering by user would widen it.
- The metric definition is my guess (see Provenance).

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) from search_daily, all platforms and countries, from stated here [guess]
- Data: search_daily, release_log, through 2026-09-13
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (30 numbers on 9 lines; 4 queries, 3 checks, 0 given)