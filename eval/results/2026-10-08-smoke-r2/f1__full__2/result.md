## Answer
Headline: -0.00 pp attributable to v2 (within-segment effect -0.0001 pp; overall CTR fell 2.10 pp, from 30.42% to 28.32%)
Overall CTR fell 2.1 pp week over week. Essentially all of that is a shift in traffic toward mobile, which has a lower CTR. CTR within every platform and country segment is unchanged.

## What it means for the rollback decision
This data gives no reason to roll back v2: it shows no CTR harm to v2 in any segment. Rolling back would not restore the overall CTR, because the drop comes from the mix of traffic and not from the ranker.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift: ruled in. Mobile's share of searches rose from 40% to 55%, and desktop's fell from 60% to 45%. The decomposition gives mix -2.10 pp and within-segment -0.00 pp, so mix accounts for 99.99% of the change. [measured]
  - v2 caused the drop (the PM's hypothesis): ruled out as a driver of the drop. CTR is flat to 3 decimal places in all 4 platform×country segments: desktop-US 37.08%, desktop-other 34.74%, mobile-US 22.66%, mobile-other 21.23%. [measured]
  - Seasonality and day of week: ruled out. Both weeks contain all 7 days, daily volume is similar (about 97k–103k searches), and the per-segment rates don't move. [measured]
  - Data completeness or logging change: ruled out. Every day has all 4 segment rows, and total volume is the same across the two weeks. [measured]
  - Ranker v2 caused the mix shift (for example, by changing which users search on mobile): not ruled out. v2 went to 100% of traffic on the same day, so there was no concurrent control. Nothing in the data points to this, and it is unlikely for a ranker change. [guess]
- Checks run:
  - mix_shift: fail. Overall change was -2.10 pp, made up of -2.10 pp mix and -0.00 pp within-segment (mix share 100%). The fail flags that the change is mix-driven, and the headline reflects that.
  - completeness: pass. The last day, 2026-10-04, has 4 rows, which is 100% of the trailing median.
  - fanout: skipped. No joins were used.
  - srm: skipped. This is not an experiment, because v2 went to 100% of traffic with no holdout.

## Caveats, and what would change the answer
- This is a before/after comparison with no control group. It shows that CTR didn't change within segments, but it can't rule out an effect hidden by a coincident change in the opposite direction.
- The segments are only platform and country. A within-segment effect on a finer dimension, such as query type, would not show up here.
- The cause of the mobile shift is unknown (a campaign, a product change, or a tracking change). Finding it would explain the drop, and it would change the answer only if it traced back to v2.
- A v2 holdout or an A/B test would give a clean causal estimate.