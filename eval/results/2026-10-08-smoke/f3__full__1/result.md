## Answer
Headline: -1.80 pp (overall CTR 30.42% → 28.62%; no interval, because the data has no sampling-variance measure)
Overall CTR fell 1.80 points week over week. All of the fall is desktop CTR, which dropped about 3.0 points. Mobile CTR didn't move at all. I attribute essentially all of the 1.80 points to v3, and that attribution is an inference.

## What it means for the rollback decision
v3 is the only logged change, and the drop starts on the day it went to 100%. So the data points toward v3 hurting desktop, at roughly -3.0 pp on desktop and -1.8 pp overall. There was no holdout group, though, so this can't be proven here. Before rolling back, check why mobile is exactly flat. If v3 reached mobile and mobile didn't move, that would be unusual.

## Why we believe it
- Alternatives considered:
  - Mix shift (platform/country share of searches): ruled out. Segment weights are identical across the two weeks (33/27/22/18%), so mix effect = +0.00 pp and within-segment change = -1.80 pp [measured]
  - Day of week / seasonality: ruled out, mostly. Both weeks cover Monday to Sunday, and daily volumes repeat exactly week to week. Daily CTR steps down on 09-07 (30.4% on 09-06 → 28.6% on 09-07) with no earlier drift. A seasonal effect that starts exactly on rollout day is unlikely, but I only have two weeks of history [measured for the step, inferred for the seasonality conclusion]
  - Data completeness / logging change: ruled out. All 14 days are present with 4 segment rows each, and volumes are 97–103k per day. This doesn't rule out a logging change that affects clicks only [measured for completeness, inferred for the rest]
  - Other releases: ruled out. `release_log` lists only v3 [measured]. It may not capture every change, such as UI or traffic-source changes [guess]
  - PM's cause (v3): ruled in, as the best-supported explanation. The drop is confined to desktop (US -3.1 pp, other -2.9 pp), and mobile is identical to the click in both weeks (34,899 and 26,751 clicks). I can't separate v3's effect from anything else that changed that week [inferred]
- Checks run:
  - completeness: pass. 2026-09-13 has 102% of the trailing median row count.
  - mix_shift: pass. The change is 0% mix and 100% within-segment.
  - fanout: skipped. I ran no joins.
  - srm: skipped. This is a before/after comparison, not a randomized experiment.

## Caveats, and what would change the answer
- It's a pre/post comparison with no concurrent control. A holdout or a staged rollout by traffic share would give a causal number.
- Mobile CTR being identical to the click, in both weeks and in both countries, is implausible for real traffic. It could mean mobile data is carried over or not logged separately, or that v3 doesn't apply to mobile. If mobile data is bad, the -1.80 pp overall figure is understated or mis-weighted.
- There's no variance estimate, so I can't give an interval. The per-day step is consistent (about -1.7 to -2.0 pp every day), which suggests the drop is real rather than noise.
- Only one week of v3 data. A novelty effect or a learning curve could change the long-run effect.
- CTR is only a click metric. It says nothing about relevance, conversion or revenue, which should weigh in the rollback decision.