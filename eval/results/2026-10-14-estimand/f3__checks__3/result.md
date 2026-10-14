## Answer
Headline: can't tell
Overall CTR fell 1.83 pp week over week, and the drop is entirely on desktop. The data can't separate v3 from anything else that changed that week. [measured]
- Observed: −1.83 pp (95% CI −1.98 to −1.68), from 30.44% to 28.61% [measured]
- Adjusted: −1.82 pp (−1.97 to −1.67), holding platform×country mix fixed [measured]. Mix explains about 1% of the drop.
- Causal effect: not identified. This needs a holdout, a staggered rollout, or a v2 vs v3 split at the same time. v3 went to 100% on one day, so no v2 traffic ran alongside it.

## What it means for the rollback decision
The drop is real and large: the whole interval sits well below zero, and far from the 0.1 pp threshold the mix check uses as a minimum effect. But the data can't say that v3 caused it. If v3 caused all of it, the effect would be about −1.8 pp. A rollback is therefore a reasonable test, but it isn't proven to be the fix. Ideally, hold back a v2 slice first and compare.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift: ruled out. Segment weights moved by under 0.5 pp, and mix contributes −0.01 pp. [measured]
  - Incomplete data in the new week: ruled out. All 14 days have 4 segment rows, and search volume is flat (~100k per day). [measured]
  - A desktop-only change unrelated to v3 (tracking, UI, seasonality): not ruled out. The drop is desktop-only (−3.00 pp, CI −3.20 to −2.80; mobile −0.04 pp, CI −0.26 to +0.18). That fits a platform-specific v3 effect, but it also fits any other desktop change that week. [inferred]
  - Normal week-to-week noise: ruled out. The noise floor is about 0.15 pp, and the drop is more than 10 times that. [measured]
- Checks run:
  - mix_shift: pass. Within-segment change is −1.82 pp and mix is −0.01 pp [check:mix_shift#1].
  - completeness: pass. The last day, 2026-09-13, is 100% of the trailing median [check:completeness#1].
  - fanout: skipped. No joins were used.
  - srm: skipped. There was no experiment split to check.

## Caveats, and what would change the answer
- The data is daily and aggregated, so the intervals treat searches as independent. They are probably a little too narrow, since clicks cluster by user.
- Any desktop-side change in the week of 2026-09-07 would confound this. `release_log` lists only the v3 rollout, which doesn't prove nothing else shipped.
- A v2 holdout, or desktop CTR on traffic that never saw v3, would identify the effect.

## Provenance
- Metric: CTR = clicks / searches, stated here [guess]. There is no metrics.json.
- Data: `search_daily` and `release_log`, through 2026-09-13.
- Reconciled: not done (no dashboard or other source provided).
- Queries and checks: the checks are logged in `.ds-checks.log`. The ad-hoc SQL and Python were not saved to a file.