## Answer
Headline: -1.82 pp (-1.97 to -1.67) [check:mix_shift#1]
Overall CTR fell from 30.44% to 28.61% week over week. Nearly all of that is a within-segment drop, concentrated on desktop, that coincided with the v3 rollout. If v3 did not change the traffic mix or anything else at the same time, that drop is the share attributable to it. [check:mix_shift#1, q4]
- Observed: -1.83 pp (-1.98 to -1.68) [check:mix_shift#1]
- Adjusted: -1.82 pp (-1.97 to -1.67), holding platform x country mix fixed [check:mix_shift#1]
- Causal effect: not identified (v3 went to all traffic at once, so there is no concurrent control; a holdout or randomized split of v2 vs v3 would identify it)

## What it means for the v3 rollback decision
The whole interval (-1.97 to -1.67 pp) is far below zero and well beyond the 0.1 pp minimum effect the check uses, so the drop is real and not noise, but without a control it cannot be called caused by v3. The drop is entirely on desktop (-3.0 pp, mobile -0.04 pp), so check desktop tracking before rolling back. [check:mix_shift#1, check:mix_shift#2]

## Why we believe it
- Alternatives considered:
  - Mix-shift (platform/country traffic mix): ruled out, mix is -0.01 pp of -1.83 pp (1%), the same at both grains [check:mix_shift#1, check:mix_shift#2] [measured]
  - Data completeness / missing days: ruled out, all 14 days present with steady volume (~100k searches/day) [q3, check:completeness#1] [measured]
  - Day of week / seasonality: ruled out as a main driver, both windows are full Mon-Sun weeks and daily CTR is flat within each week with a step on 09-07 [q3] [inferred]
  - Requester's cause (v3): ruled in as coincident, the step lines up with the rollout and is the only release_log entry [q2, q3] [measured]; causation itself is not established [inferred]
  - Desktop-only logging or definition change coinciding with the release: not ruled out, the drop is only on desktop (-1.80 pp of -1.82 pp) and mobile is flat, which a ranker would not obviously do [check:mix_shift#2] [inferred]
- Checks run:
  - completeness: pass last day 2026-09-13 has 101528 rows, 101% of the trailing median [check:completeness#1]
  - mix_shift: pass, platform x country grain, mix is 1% of the change [check:mix_shift#1]
  - mix_shift: pass, platform grain agrees with the finer grain [check:mix_shift#2]
  - fanout: skipped, no joins were used
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- No metrics.json was provided, so the CTR definition is my guess; the owner confirming it would settle this.
- No control group: only a v3 holdout, or a desktop tracking audit, can say whether v3 caused the drop.
- Intervals assume independent searches (se_assumes_independent_units), so they are somewhat too narrow if clicks cluster by user.
- Only two weeks of data; one week of before-baseline cannot show normal week-to-week variation.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) over search_daily, all platforms and countries, from stated here [guess]
- Data: search_daily, release_log, through 2026-09-13
- Reconciled: not done (no dashboard or trusted source available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (28 numbers on 11 lines; 3 queries, 3 checks, 0 given)