## Answer
Headline: can't tell. Overall CTR fell 1.83 pp, but a before/after comparison can't separate v3 from anything else that changed that week.
Overall CTR fell from 30.44% to 28.61% week over week, and all of the drop is on desktop. Mobile is flat.
- Observed: -1.83 pp (-1.98 to -1.68), pooled searches and clicks, 08-31..09-06 vs 09-07..09-13 [measured]. The interval is a two-proportion normal approximation that treats searches as independent.
- Adjusted: -1.83 pp (about the same, interval not recomputed), holding platform × country mix fixed [measured]. The mix is nearly unchanged between weeks, so mix shift explains none of the drop.
- Causal effect: not identified. v3 went to 100% of traffic at once, so no v2 traffic was left as a control. A holdout, an A/B split, or a staggered rollout by platform or country would identify it.

## What it means for the rollback decision
The observed drop of -1.98 to -1.68 pp is far larger than any plausible noise. The open question is whether v3 caused it. I can't attribute it to v3 from this data. If a loss of even 0.5 pp would justify a rollback, the data is consistent with that. But a rollback decision should wait for a causal test: re-run v2 on a slice of desktop traffic, or check what else shipped to desktop that week.

## Why we believe it
- Alternatives considered:
  - Mix shift across platform or country: ruled out. Segment search volumes are within about 1% between weeks [measured].
  - Daily noise: ruled out. Every v2 day is 30.1–30.8% and every v3 day is 28.3–28.9%, with a clean step on 09-07 [measured].
  - A desktop-only cause other than v3 (UI change, logging or tracking change, seasonality, a school or holiday effect): not ruled out. Desktop CTR fell about 3 pp in both US (37.1% to 34.0%) and other countries (34.8% to 31.9%), while mobile moved by under 0.05 pp [measured]. v3 could behave differently on desktop. A desktop-specific instrumentation or UI change would look the same. I can't tell which from this data [inferred].
  - Anything else that changed on 09-07: not ruled out. The release_log has only the v3 entry, which doesn't mean nothing else changed [inferred].
- Checks run:
  - Segment mix stability: pass.
  - Daily series step: pass. The step lines up with the 09-07 rollout date.
  - Control group available: fail. All traffic switched to v3 on 09-07.
  - Pre-trend: could not run. Only one prior week was provided.
  - Reconciliation to a dashboard: skipped. No other source was available.

## Caveats, and what would change the answer
- A holdout or A/B arm on v2 would give the causal number.
- Check the desktop client and logging release notes for 09-07.
- More pre-period weeks would show whether week-to-week swings of this size happen normally. The pre-week days vary little, so that seems unlikely [guess].
- The data covers a single week on each side.

## Provenance
- Metric: CTR = clicks / searches, pooled across rows. This is stated here [guess], because no metrics.json was present.
- Data: search_daily (56 rows, covering 2026-08-31..2026-09-13) and release_log, through 2026-09-13.
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: ad hoc Python/sqlite queries run in this session. They are not saved to a file.