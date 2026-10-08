## Answer
Headline: about 0.0 pp attributable to v2 (within-segment effect −0.0001 pp, rounds to zero), against an overall CTR change of −2.10 pp (30.42% → 28.32%) [measured]
Overall CTR fell 2.10 pp because traffic shifted from desktop, which has a high CTR, to mobile, which has a low CTR. CTR within every platform×country segment is unchanged.

## What it means for the rollback decision
The data gives no reason to roll back v2 on CTR grounds, because rolling back would not recover the drop [inferred]. Why mobile's share of searches jumped from 40% to 55% is still unexplained, and that is where to look next.

## Why we believe it
- Alternatives considered:
  - v2 lowered CTR within segments: ruled out. All four platform×country segments have the same CTR before and after, with differences under 0.01 pp (e.g. desktop-US 37.08% → 37.08%, mobile-other 21.23% → 21.23%) [measured].
  - Mix shift: ruled in. Mix accounts for −2.10 pp of the −2.10 pp change (about 100%). Mobile's share went from 40% to 55% of searches [measured].
  - What caused the mix shift: not determined. It coincides with the v2 rollout, so v2 could have changed mobile vs desktop traffic, for example through UI or routing differences, but that is not testable with this data [guess].
  - Incomplete data in the later week: ruled out. Both weeks have 7 days with 4 rows per day [measured].
- Checks run:
  - mix_shift: fail. The overall change splits into −2.10 pp from mix and −0.00 pp within segments. A "fail" here means the mix share is above its 0.3 threshold, so it confirms the drop comes from mix.
  - completeness: pass. 2026-10-04 has 4 rows, 100% of the trailing median.
  - srm: skipped. This is not an experiment with randomized arms. v2 went to 100% of traffic, so there is no control group.
  - fanout: skipped. No joins were used.

## Caveats, and what would change the answer
- This is a before/after comparison with no control group, so it cannot rule out something else that changed in the same week [inferred].
- Only platform and country are available. If v2 affected a finer segment that is not in the data, it would not show up here [inferred].
- If the mobile surge is itself caused by v2, for example by drawing in low-intent mobile searches, then v2 is indirectly responsible for the overall drop. Checking where the extra mobile traffic comes from would settle this.
- The results table has no confidence interval because the within-segment differences are essentially zero.