Overall CTR fell 2.10 pp, but almost all of that is a shift in traffic toward mobile, where CTR is lower. Within each platform and country, CTR didn't change.

## Answer
Headline: can't tell
Overall CTR fell about 2.1 pp, and that drop is a traffic-mix shift toward mobile. Within-segment CTR is flat, but without a concurrent v1 control the data can't say whether v2 caused the mix shift.
- Observed: −2.10 pp (−2.25 to −1.95), from 30.42% to 28.32% [measured]
- Adjusted: −0.00 pp (−0.15 to +0.15), holding the platform × country mix fixed [measured]
- Causal effect: not identified (v2 went to 100% of traffic at once, so there is no concurrent v1 holdout. A holdout or a staged rollout would identify it.)

## What it means for the rollback decision
The pre/post comparison gives no evidence that v2 lowers CTR within any segment. The adjusted interval (±0.15 pp) excludes any within-segment drop larger than about 0.15 pp. The mix shift, about −2.09 pp, is the only large move. Rolling back would be justified only if v2 itself pulled traffic toward mobile, and that is untested. [inferred]

## Why we believe it
- Alternatives considered:
  - Mix shift (mobile share rose from 40% to 55%): ruled in. It explains 99.9% of the drop (−2.09 pp) [measured].
  - v2 lowering CTR within segments: mostly ruled out. The within-segment effect is −0.002 pp, and each of the four segments moved less than 0.02 pp [measured].
  - v2 causing the mix shift (for example through routing or surfacing): not ruled out, because no data here separates it [inferred].
  - Other same-week changes: release_log lists only the v2 rollout, so I found none, but the log may be incomplete [guess].
- Checks run:
  - mix_shift: flag. Mix-dominant, with a within-segment effect of −0.00 pp (CI −0.15 to +0.15) and a mix effect of −2.09 pp (check id mix_shift#1).
  - completeness: pass. 2026-10-04 has 4 rows, 100% of the trailing median (check id completeness#1).
  - srm: skipped. There is no randomized split to test.
  - fanout: skipped. I used no joins.

## Caveats, and what would change the answer
- The two weeks are a single before/after pair with no control. Any other change at the same time is confounded with v2.
- The intervals treat searches as independent. Repeat searches by the same user would widen them.
- The weekday mix is identical across the two weeks, so day-of-week effects don't explain the drop.
- Data shows desktop volume fell and mobile volume rose. Checking why would settle the question: a traffic-source change (such as a mobile campaign or app release) would clear v2, while a ranker-driven change would implicate it. A holdout of v1 would settle it directly.

## Provenance
- Metric: CTR = clicks / searches. metrics.json does not exist, so this is stated here [guess].
- Data: search_daily and release_log, through 2026-10-04 (complete).
- Reconciled: not done (no dashboard or reference figure available).
- Queries and checks: the check outputs are logged in .ds-checks.log in the analysis directory. The queries were run inline and not saved.