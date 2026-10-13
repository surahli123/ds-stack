## Answer
Headline: −1.83 pp overall CTR (95% interval −1.98 to −1.68) is the observed week-over-week change. At most about −1.8 pp of it can be attributed to v3, and that is an upper bound on v3's effect, not a clean estimate of it. [measured for the change; inferred for the attribution]
Overall CTR fell from 30.44% to 28.61%. Almost all of the drop is on desktop (about −3 pp in both US and other). Mobile is flat (about −0.03 pp).

## What it means for the rollback decision
The interval is far from zero, and it is well above the 0.1 pp smallest change the mix_shift check treats as meaningful. A real, roughly 1.8 pp CTR loss coincided with the v3 rollout, so it is worth treating as a v3 regression on desktop. However, this is a before/after comparison with no control group, so I can't separate v3 from anything else that changed that week. If your rollback threshold is anything above about 0.15 pp (the noise floor), the data points toward rolling back or at least holding v3 on desktop. [inferred]

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform or country share): ruled out. Mix contributes −0.01 pp (about 1% of the change) and the within-segment effect is −1.82 pp [measured].
  - Incomplete data for either week: ruled out. All 14 days have 4 rows each, and the last day is complete [measured].
  - Volume change: ruled out. Searches were 699,485 before and 699,266 after [measured].
  - Other concurrent changes (a desktop-only tracking, UI or seasonal change): not ruled out. release_log lists only the v3 rollout, but the rollout was at 100% with no holdout. The mobile-flat pattern could mean v3 only hurts desktop, or that something desktop-specific changed that week [guess].
  - Day-of-week effects: ruled out, since both periods are full Monday-to-Sunday weeks [measured].
- Checks run:
  - mix_shift: pass. Within-segment −1.82 pp (95% CI −1.97 to −1.67), mix −0.01 pp.
  - completeness: pass. 2026-09-13 has 4 of 4 rows, 100% of the trailing median.
  - srm: skipped. There is no randomized assignment, so there is no split to check.
  - fanout: skipped. No joins were used.

## Caveats, and what would change the answer
- There is no concurrent control, so v3 is confounded with anything else that changed that week. A holdout or a staged rollback on a slice of desktop traffic would give a causal estimate.
- The interval assumes independent searches. Repeated searches by the same user would widen it, but the effect is about 10 times the noise floor, so the conclusion is unlikely to flip.
- Only one pre-period week was used, so there is no estimate of normal week-to-week CTR variation.
- Desktop-only impact suggests checking for a desktop-specific cause, such as a client or logging change, before blaming the ranker.

## Provenance
- Metric: CTR = clicks / searches, pooled across segments, stated here [guess]. There is no metrics.json in the directory.
- Data: search_daily and release_log in warehouse.db, 2026-08-31 to 2026-09-13 (last complete day 2026-09-13).
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: the ad-hoc queries were run inline and not logged. Check output is in .ds-checks.log as mix_shift#1 and completeness#1.