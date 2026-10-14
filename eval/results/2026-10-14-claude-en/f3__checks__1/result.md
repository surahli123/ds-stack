## Answer
Headline: can't tell

Overall CTR fell 1.83 pp week over week, and v3 is the only logged change that week. Every user moved to v3 on the same day, so there is no control group and the data can't separate v3 from anything else that changed that week.
- Observed: -1.83 pp (95% CI -1.98 to -1.68), from 30.44% to 28.61% [measured]
- Adjusted: -1.82 pp (95% CI -1.97 to -1.67), holding platform × country mix fixed [measured]
- Causal effect: not identified (it would take a holdout or staged rollout with concurrent v2 traffic, or an A/B test of v3 against v2)

## What it means for the rollback decision
The drop is real and far larger than the 0.15 pp noise floor, and the whole interval lies below zero. If v3 caused even half of it (about 0.9 pp), that is a material loss. The data can't separate v3 from other causes, so only a concurrent v2 holdout can settle whether to roll back. If a quick holdout is possible, that is the cleanest way to decide.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform or country): ruled out. Mix explains -0.01 pp of the -1.83 pp, and search volume is flat (699k vs 699k) [measured].
  - Partial or missing data: ruled out. All 14 days have all 4 segments, through 2026-09-13 [measured].
  - Drop spread across all segments: ruled out. Desktop CTR fell 3.00 pp (CI -3.20 to -2.80); mobile was flat at -0.04 pp (CI -0.26 to +0.18) [measured]. Desktop US and desktop other both fell about 3 pp.
  - Other concurrent changes (desktop UI, logging or tracking, seasonality): not ruled out. release_log lists only v3, but it may be incomplete [inferred].
  - v3 causing the drop: plausible but unproven. The drop starts exactly on 2026-09-07 with no pre-trend, and the daily rates show a step change [measured]. A v3 effect confined to desktop is possible, for example a ranking or layout interaction. Mobile being flat is a hint, not proof, because v3 launched everywhere at once [inferred].
- Checks run:
  - mix_shift: pass. Mix is 1% of the change.
  - completeness: pass. The target date 2026-09-13 has 4 of 4 expected rows.
  - srm: skipped. There is no randomized assignment.
  - fanout: skipped. No joins were used.

## Caveats, and what would change the answer
- The intervals treat searches as independent. Clicks within a user or session are correlated, so the true intervals are somewhat wider.
- Only 2 weeks of data, one pre-period week, and no same-weekday history.
- A holdout, a desktop UI or tracking change log, or a mobile-vs-desktop v3 design explanation would change the answer.

## Provenance
- Metric: CTR = clicks / searches, stated here [guess]. There is no metrics.json.
- Data: search_daily and release_log, through 2026-09-13.
- Reconciled: not done (no dashboard or source to compare against).
- Queries and checks: ad hoc queries are not logged. Check outputs are in `.ds-checks.log` (mix_shift#1, completeness#1).