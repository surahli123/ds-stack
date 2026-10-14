## Answer
Headline: can't tell

Overall CTR fell 2.10 pp, but almost all of that is a shift toward mobile searches, which have a lower CTR. Within each platform, CTR is flat, and without a holdout we can't separate v2's effect from other changes that week.
- Observed: -2.10 pp (95% CI -2.25 to -1.95), from 30.42% to 28.32% [measured]
- Adjusted: -0.00 pp (95% CI -0.15 to +0.15), holding platform fixed. The mix effect is -2.09 pp, about 100% of the drop. [measured]
- Causal effect: not identified. All traffic moved to v2 on 09-28, so there is no concurrent control. A holdout, or a staged or randomised rollout, would identify it.

## What it means for the rollback decision
The 2.10 pp drop is not evidence against v2. The platform-adjusted effect is within ±0.15 pp of zero, so any v2 harm larger than about 0.15 pp is unlikely, assuming the mobile shift didn't come from v2 itself. I'd keep v2 rolled out and, if you need certainty, confirm with a holdout.

## Why we believe it
- Alternatives considered:
  - Platform mix shift: ruled in. Mobile's share of searches rose from 40.1% to 55.1%, and desktop CTR is about 36% against about 22% on mobile. [measured]
  - v2 lowering CTR within segments: mostly ruled out. Desktop moved -0.04 pp and mobile +0.03 pp. [measured]
  - Country mix: ruled out. US and other CTRs are flat between weeks within each platform. [measured]
  - v2 causing the mobile shift: not ruled out. A ranker is unlikely to change device mix, but nothing here tests it. [guess]
  - Seasonality or a concurrent campaign pushing mobile traffic: not ruled out. There is only one week of history before the change. [inferred]
- Checks run:
  - mix_shift: flag. The change is 100% mix and the within-segment effect is -0.004 pp. The interval assumes independent units, so it is probably a little too narrow. [check:mix_shift#1]
  - completeness: pass. 10-04 has 4 rows, 100% of the trailing median. [check:completeness#1]
  - srm: skipped. There was no experiment assignment.
  - fanout: skipped. There were no joins.

## Caveats, and what would change the answer
- Before and after is one week each, and the ranker is perfectly confounded with time.
- The adjusted estimate holds only if device mix is independent of v2.
- If a holdout or a long pre-period showed mobile share rising because of v2 or a seasonal cause, the interpretation would change.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), stated here [guess]. There is no metrics.json.
- Data: search_daily and release_log, through 2026-10-04, with all 14 days complete.
- Reconciled: not done (no dashboard or source to compare against).
- Queries and checks: the checks are logged in .ds-checks.log (mix_shift#1, completeness#1). The queries were run inline and not logged.