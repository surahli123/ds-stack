## Answer
Headline: -1.83 pp (95% CI -1.98 to -1.68) [check:mix_shift#1]
Overall CTR fell from 30.44% to 28.61% week over week. The whole drop is in desktop (36.0% to 33.0%) and mobile is flat (22.0% to 22.0%). This coincided with the v3 rollout, but v3 went to 100% of traffic on the same day, so the drop can't be separated from anything else that changed that day. [check:mix_shift#2, q4]

## What it means for the rollback decision
The whole -1.83 pp is a within-segment drop. The interval excludes zero and is far above the 0.1 pp noise threshold the check uses [check:mix_shift#1]. v3 is the only logged change on 2026-09-07 [q2], so it is the leading suspect, but this data can't prove it. The request gave no rollback threshold, so judge -1.98 to -1.68 pp against your own tolerance. A v2 holdout would settle causality.

## Why we believe it
- Alternatives considered:
  - Mix-shift (platform, country): ruled out. The mix effect is -0.01 pp, about 1% of the change, and the coarse (platform) and fine (platform x country) grains agree. [check:mix_shift#1, check:mix_shift#2] [measured]
  - Day of week / seasonality: mostly ruled out. Both windows are Mon–Sun. Daily CTR was 30.1–30.8% on every day before and 28.3–28.9% on every day after, with no overlap. [q3] [measured] There is no longer history, so yearly effects aren't excluded. [inferred]
  - Data completeness / logging change: ruled out for volume. Searches are flat (699,485 vs 699,266) and all 14 days are present. [q4, q3, check:completeness#3] [measured] A desktop tracking change can't be tested here. [guess]
  - Other releases: ruled out as far as logged. release_log has one entry on 2026-09-07. [q2] [measured]
  - PM's cause (v3): ruled in as consistent, not proven. The drop is desktop-only [q4] and starts the day v3 is on [q3], but ranker is perfectly confounded with week (no v2 in week 2). [inferred]
- Checks run:
  - mix_shift (platform x country): pass. Within-segment -1.82 pp, mix -0.01 pp. [check:mix_shift#1]
  - mix_shift (platform): pass. Same result at the coarser grain. [check:mix_shift#2]
  - completeness: pass for 2026-09-13, at 101% of trailing days. [check:completeness#3] An earlier weekly-grain call could not run (too little history). [check:completeness#1] Another call failed because my spec omitted the target day. [check:completeness#2]
  - fanout: skipped, no joins used.
  - srm: skipped, not a randomized experiment.

## Caveats, and what would change the answer
- There is no holdout or staggered rollout, so v3 is not isolated. A v2 holdout or a desktop-specific change log would settle it.
- The interval assumes independent searches, so it is probably somewhat too narrow.
- There are only two weeks of data, so a novelty effect or later recovery isn't visible.
- CTR is a proxy. I didn't look at downstream outcomes such as conversions or satisfaction.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches), search_daily, all platforms and countries, stated here [guess]
- Data: search_daily, release_log, through 2026-09-13
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (27 numbers on 9 lines; 3 queries, 5 checks, 0 given)