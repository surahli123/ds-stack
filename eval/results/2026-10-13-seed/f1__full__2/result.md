## Answer
Headline: -0.00 pp attributable to v2 within segments (95% CI -0.15 to +0.15 pp) [check:mix_shift#1]
Overall CTR fell from 30.42% to 28.32% (-2.10 pp, CI -2.25 to -1.95). About 100% of that is a shift in platform mix toward lower-CTR mobile, not a change in CTR within desktop or mobile. [check:mix_shift#1]

## What it means for the rollback decision
The v2 effect interval (-0.15 to +0.15 pp) excludes the -2.10 pp overall drop, so the drop is not evidence that v2 hurts CTR. A within-segment loss of up to 0.15 pp can't be excluded, and I don't have a threshold for how small a loss would justify rollback. [check:mix_shift#1]

## Why we believe it
- Alternatives considered:
  - Mix shift (mobile share of searches 40.1% to 55.1%; desktop CTR 36.05% before vs 36.01% after, mobile 22.02% before vs 22.06% after): ruled in as the explanation, mix effect -2.09 pp [q4, check:mix_shift#1] [measured]
  - Finer grain, platform x country, gives the same result: within-segment -0.00 pp (CI -0.15 to +0.15), mix share 100% [q5, check:mix_shift#3] [measured]
  - v2 lowered CTR (the PM's cause): ruled out as the main driver by the near-zero within-segment effect [check:mix_shift#1] [measured]. The rollout was 100% with no holdout, so this is a before/after comparison, not a causal test [inferred]
  - Data completeness: ruled out, all 14 days have 4 rows [q3, check:completeness#1] [measured]
  - Day of week and seasonality: ruled out for window shape, since both windows are Mon to Sun and 7 days [q3] [measured]. Seasonal effects on the platform mix itself are not tested [guess]
  - Other concurrent changes: release_log lists only the v2 rollout [q2] [measured]
- Checks run:
  - completeness: pass. 2026-10-04 has 4 rows, 100% of the trailing median [check:completeness#1]
  - mix_shift (platform): flag. Mix-dominant, mix -2.09 pp, within-segment -0.00 pp [check:mix_shift#1]
  - mix_shift (platform x country, before/after swapped by mistake): flag. The sign is inverted, so ignore it [check:mix_shift#2]
  - mix_shift (platform x country, rerun correctly): flag. Same conclusion as the platform grain [check:mix_shift#3]
  - fanout: skipped, no joins
  - srm: skipped, not a randomized experiment

## Caveats, and what would change the answer
- The cause of the jump in mobile share is unknown. If v2 itself pushed users to mobile (for example through latency or UI), the mix effect would be partly v2-driven. Daily mobile search volume around the rollout would help show this.
- The intervals assume independent searches, so they are somewhat too narrow. Clicks are correlated within users.
- With no holdout, any concurrent change to platform traffic mix is confounded with v2. A holdout or staged rollout would identify the effect.
- Only two platforms and two country buckets were checked.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), from search_daily, stated here [guess]
- Data: search_daily, release_log, through 2026-10-04
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (32 numbers on 10 lines; 4 queries, 4 checks, 0 given)