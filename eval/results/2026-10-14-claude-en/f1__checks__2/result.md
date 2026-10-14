## Answer
Headline: can't tell
Overall CTR fell 2.10 pp, but almost all of that is a shift toward mobile traffic, which has a lower CTR. Within each platform and country, CTR did not change. The data can't separate v2's effect from anything else that changed at the same time.
- Observed: −2.10 pp (−2.25 to −1.95) (30.42% → 28.32%) [measured]
- Adjusted: −0.00 pp (−0.15 to +0.15), holding platform × country mix fixed [measured]
- Causal effect: not identified (v2 went to 100% on 09-28 with no holdout or concurrent v1 traffic. A staggered rollout, a holdout, or an A/B on v1 vs v2 within a platform would identify it.)

## What it means for the rollback decision
The within-segment interval of ±0.15 pp rules out any v2 CTR harm larger than about 0.15 pp, assuming the traffic mix itself isn't an effect of v2. The 2.1 pp drop is not evidence against v2, so it doesn't justify a rollback on its own.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift to mobile: ruled in. Mobile's share of searches rose from about 40% to about 55%, and mobile CTR is about 22% against about 36% on desktop. The mix effect is −2.09 pp, or 99.9% of the drop. [measured]
  - v2 lowering CTR within segments: not supported. The within-segment effect is −0.002 pp, and every segment moved by less than 0.02 pp. [measured]
  - v2 causing the mobile shift (for example by changing which users search): can't rule out. There is no counterfactual, but I see no mechanism for it. [guess]
  - Incomplete data for the new week: ruled out. Every day has all 4 segment rows. [measured]
- Checks run:
  - mix_shift: flag. It is mix-dominant at 100% mix share [check:mix_shift#1].
  - completeness: pass. 2026-10-04 has 4 rows, 100% of the trailing median [check:completeness#1].
  - srm: skipped. There was no experiment assignment.
  - fanout: skipped. No joins were used.

## Caveats, and what would change the answer
- The analysis covers only two weeks and has no concurrent control, so anything else that changed on 09-28 is confounded with v2. The release_log lists only the v2 rollout.
- The mix_shift check's intervals assume independent units. Daily search counts are autocorrelated, so the real intervals are probably somewhat wider.
- The segments are only platform and country. Within-segment effects could be hidden by finer cuts, such as query type.
- If the mobile surge is a data or traffic-source change, such as a campaign or app launch, find out what caused it. If v2 caused it, the conclusion changes.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), from stated here [guess]
- Data: search_daily and release_log, through 2026-10-04 (last complete day)
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: the queries were ad hoc Python against SQLite and are not logged. The checks are logged in .ds-checks.log (mix_shift#1, completeness#1).