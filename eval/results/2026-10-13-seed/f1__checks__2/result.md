## Answer
Headline: about 0.0 pp (95% interval −0.15 to +0.15 pp) attributable to v2. [measured]
Overall CTR fell 2.10 pp, from 30.42% to 28.32%. Almost all of that (−2.09 pp) comes from traffic shifting toward mobile, which has a lower CTR. Within-segment CTR didn't move (−0.00 pp). [measured]

## What it means for the rollback decision
v2's effect on CTR is statistically indistinguishable from zero. The interval's worst case is −0.15 pp, which is about 7% of the observed drop. Unless a loss of 0.15 pp or more would justify a rollback, the CTR drop is not a reason to roll back. Rolling back would not recover the 2.1 pp. [inferred]

## Why we believe it
- Alternatives considered:
  - v2 lowered CTR within segments: ruled out. Each of the four platform×country segments has the same CTR before and after, within ±0.02 pp [measured].
  - Platform/country mix shift: ruled in. It explains 99.9% of the drop. Mobile's share of searches rose from 40% to 55% [measured].
  - Whether the mix shift was caused by v2 (for example, v2 pushing users to mobile): not tested. The data can't separate this from an independent traffic change [guess].
  - Day-to-day trend or seasonality: partly checked. Every v1 day is higher than every v2 day, but the dataset covers only two weeks [inferred].
- Checks run:
  - mix_shift: flag. The drop is mix-dominant, with mix at −2.09 pp and within-segment at −0.00 pp (95% interval −0.15 to +0.15). The check assumes independent units, so the interval may be slightly narrow [check:mix_shift#1].
  - completeness: pass. 2026-10-04 has 4 of 4 expected rows, so the week is fully loaded [check:completeness#1].
  - srm: skipped. This is a before/after comparison with no randomized split.
  - fanout: skipped. No joins were used.

## Caveats, and what would change the answer
- This is a before/after comparison, not an A/B test. v2 went to 100% of traffic at once, so v2 is confounded with anything else that changed that week. release_log lists only the v2 rollout.
- Mobile traffic grew sharply. If v2 caused that (for example through UI or routing changes), part of the 2.1 pp drop would count as a v2 effect. Check why mobile volume rose.
- Only coarse segments were available (platform × country). Effects inside finer segments would be missed.
- Only two weeks of data, and no per-user data for variance estimates.

## Provenance
- Metric: CTR = clicks / searches, summed over the week. This definition is stated here [guess]; no metrics.json exists.
- Data: search_daily and release_log, through 2026-10-04 (complete).
- Reconciled: not done (no dashboard or reference figure available).
- Queries and checks: the checks are logged in .ds-checks.log in the analysis directory. The aggregation queries were run inline and not saved.