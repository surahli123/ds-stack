## Answer
Headline: can't tell
Overall CTR fell 1.83 pp week over week, but v3 launched to 100% of traffic with no holdout, so its share of that drop can't be separated from anything else that changed that week.
- Observed: −1.83 pp (−1.98 to −1.68), from 30.44% to 28.61% [measured]
- Adjusted: −1.82 pp (−1.97 to −1.67), holding platform × country mix fixed [measured]
- Causal effect: not identified (it would take a holdout or an A/B split of v2 vs v3 at the same time, or a staggered or partial rollout)

## What it means for the rollback decision
The drop is real, and it isn't explained by traffic mix. It is also entirely a desktop drop, which points at v3 or something that shipped with it. The data can't settle whether v3 caused it. A v3 effect anywhere from 0 to −1.8 pp is consistent with this comparison. I don't know your rollback threshold. I'd run a quick v2 holdout on a slice of desktop traffic before deciding, rather than rolling back blind.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform/country): ruled out. Mix explains −0.01 pp, about 1% of the drop [measured, check:mix_shift#1].
  - Partial or incomplete data: ruled out. All 14 days are present with 4 segment rows each [measured].
  - Desktop-specific cause (v3 or a coincident change): ruled in as the locus. Desktop fell −3.00 pp (±0.20), US −3.1 and other −2.9. Mobile was flat at −0.04 pp (±0.22) [measured]. Mobile is on v3 too, which weakly argues against a uniform ranker effect. This is an inference, since v3 might behave differently on desktop [inferred].
  - Other concurrent changes or seasonality: not ruled out. release_log lists only the v3 rollout, and there is no earlier history to check for week-to-week noise [inferred].
  - Pre-existing trend: not checkable. The data starts 08-31, and the daily CTR was flat within each week [measured].
- Checks run:
  - mix_shift: pass. Within-segment change is −1.82 pp and mix is −0.01 pp.
  - completeness: pass. 2026-09-13 has 100% of the expected rows.
  - srm: skipped. There is no experiment assignment.
  - fanout: skipped. No joins were used.

## Caveats, and what would change the answer
- Ranker is perfectly confounded with week: v2 ran in the first week and v3 in the second, with no overlap.
- The intervals treat searches as independent. Users with many searches would make the true intervals wider.
- Two weeks of data only. Any client, logging, or UI change on desktop that week would look identical to a v3 effect.
- Logging or UI changes missing from release_log would change the answer. A v2 holdout, or desktop-specific change logs, would identify the effect.

## Provenance
- Metric: CTR = clicks / searches, summed over segments, stated here [guess]. There is no metrics.json.
- Data: search_daily and release_log, through 2026-09-13.
- Reconciled: not done (no dashboard or source figure available).
- Queries and checks: the checks are logged in .ds-checks.log (mix_shift#1, completeness#1). The queries were run ad hoc and aren't logged.