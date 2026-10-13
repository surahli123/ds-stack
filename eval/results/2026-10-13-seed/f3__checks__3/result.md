## Answer
Headline: can't tell
Overall CTR fell 1.83 pp (30.44% → 28.61%) [measured]. About 1.82 pp of that is within-segment change and all of it is on desktop. Because v3 went to 100% of traffic at once, there is no concurrent control, so I can't separate v3's share from anything else that changed that day.

## What it means for the rollback decision
The before/after change is −1.82 pp (95% CI −1.97 to −1.67), which is far larger than the 0.1 pp noise floor. That interval is the maximum v3 could account for, not an estimate of its effect. If the roughly 1.8 pp loss is real, it is large enough to justify a rollback or a holdout test. Nothing here shows how much of it is v3's.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (desktop vs mobile): ruled out. Mix contributes −0.01 pp (about 1% of the change) [measured].
  - Data incomplete in the later week: ruled out. 2026-09-13 has all 4 rows, same as the baseline days [measured].
  - Pre-existing downtrend: ruled out as the cause. Daily CTR was flat at about 30.0–30.8% through 09-06, then stepped down to about 28.3–28.9% from 09-07 on [measured]. The step lines up with the v3 rollout [inferred].
  - v3 as the cause: neither in nor out. The only logged change is the v3 rollout, but desktop fell about 3.0 pp (36.0% → 33.0%) while mobile was flat (22.02% → 21.98%) [measured]. The drop is similar in the US and other countries [measured]. If v3 also serves mobile, a desktop-only effect is unexplained. A desktop-specific event such as a UI, tracking or traffic change could produce the same pattern [guess].
  - Any other change that day: not ruled out, because release_log has a single entry and there is no concurrent v2 holdout.
- Checks run:
  - completeness: pass. The last day is 100% of the trailing median.
  - mix_shift: pass. Within-segment change is −1.82 pp (CI −1.97 to −1.67) and mix is −0.01 pp. The CI assumes independent units, so it is likely somewhat too narrow.
  - srm: skipped. There was no randomized assignment, since v2 and v3 never ran side by side.
  - fanout: skipped. No joins were used.

## Caveats, and what would change the answer
- A holdout, a staged rollout, or per-platform ranker config would settle attribution. Roll v3 back for a few days on a slice of desktop traffic and compare.
- Check whether v3 actually serves mobile, and look for desktop instrumentation, UI or traffic-source changes around 09-07.
- Only two weeks of data, and CTR is not a quality measure on its own. Fewer clicks could mean better answers on the results page itself.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches), stated here [guess]. No metrics.json exists.
- Data: search_daily and release_log, through 2026-09-13 (complete).
- Reconciled: not done (no dashboard or source to compare against).
- Queries and checks: the queries were run inline and not logged to a file. The check outputs are in `.ds-checks.log` as completeness#1 and mix_shift#1.