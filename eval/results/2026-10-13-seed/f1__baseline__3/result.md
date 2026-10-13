## Answer
Headline: +0.00 pp (95% CI −0.15 to +0.15) from v2's effect on CTR within platform and country segments. Overall CTR fell 2.10 pp (30.42% → 28.32%) (measured).
Overall CTR fell about 2.1 pp, and that drop comes from a jump in mobile traffic share, which has lower CTR on either ranker. CTR within each platform and country segment did not change.

## What it means for the rollback decision
v2 has no detectable effect on CTR within segments, and the interval rules out a harm larger than about 0.15 pp. The −2.1 pp headline drop is mostly mix shift. Rolling back would not recover it, unless v2 itself caused the mobile shift (not testable here). A rollback would only be justified if v2 were shown to hurt by more than about 0.15 pp.

## Why we believe it
- Alternatives considered:
  - v2 lowered CTR: ruled out as a within-segment effect. The segment CTRs match week over week: desktop-US 37.07% vs 37.07%, desktop-other 34.79% vs 34.71%, mobile-US 22.66% vs 22.71%, mobile-other 21.24% vs 21.25% [measured].
  - Traffic mix shift (Simpson's paradox): ruled in. Mobile share of searches went from 40% to 55%, which accounts for −2.10 pp of the −2.10 pp change [measured].
  - v2 caused the mobile shift (for example by changing logging or routing): not ruled out. Nothing in the data tests it [guess].
- Checks run:
  - Decomposition into a within-segment rate effect and a mix effect, using week-2 weights: pass. Rate effect +0.003 pp, mix effect −2.100 pp.
  - Interval: pass. Binomial standard errors per segment give ±0.149 pp. This ignores day-to-day variance beyond binomial.
  - Daily series: pass. Overall CTR steps down on 9/28 and stays flat (28.1% to 28.6%) afterwards. Week 1 was flat at about 30.2% to 30.8%.
  - Concurrent control: could not run. v2 went to 100% of traffic, so there was no holdout and the comparison is before/after only.
  - Release log: flag. It has a single entry (v2 at 100% on 9/28), so it can't explain the mobile jump.

## Caveats, and what would change the answer
- Before/after with no holdout. Anything else that changed on 9/28 is confounded with v2 (inferred).
- Find out why mobile share jumped on 9/28: a mobile release, a marketing push, or an instrumentation change. If v2 caused it, the answer changes.
- Only 7 days per arm, and segment-level CTR was not checked for novelty effects.

## Provenance
- Metric: CTR = clicks / searches, stated here [guess]. No metrics.json was present.
- Data: search_daily and release_log in warehouse.db, 2026-09-21 through 2026-10-04.
- Reconciled: not done (no dashboard or source figure to compare against).
- Queries and checks: ad hoc inline Python against warehouse.db; they were not saved to a file.