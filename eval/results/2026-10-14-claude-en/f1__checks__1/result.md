## Answer
Headline: can't tell (the data can't separate v2 from the week-to-week change in platform mix)

Overall CTR fell about 2.1 pp, and almost all of that is a shift toward mobile traffic, which has a lower CTR. Within each platform×country segment, CTR didn't move.

- Observed: −2.10 pp (95% CI −2.25 to −1.95), from 30.42% to 28.32% [measured]
- Adjusted: −0.002 pp (95% CI −0.15 to +0.15), holding platform×country segment mix fixed [measured]. The mix shift accounts for −2.09 pp, which is 99.9% of the drop.
- Causal effect: not identified. A randomized holdout, or v1 and v2 serving at the same time, would identify it. Here every v1 row is in the first week and every v2 row is in the second, so v2 can't be told apart from anything else that changed that week.

## What it means for the rollback decision
Once mix is held fixed, any v2 effect on CTR is within about ±0.15 pp. That excludes a drop anywhere near the 2.1 pp the PM sees, so the observed drop is not evidence against v2. This is conditional on v2 not having caused the mobile shift itself, which I can't check from this data. I'd hold off on rolling back on the strength of this CTR drop alone.

## Why we believe it
- Alternatives considered:
  - v2 lowered CTR inside segments: ruled out as a large effect. Segment CTRs are flat: desktop/US 37.07% to 37.07%, mobile/US 22.66% to 22.71%, and the other two segments moved by less than 0.1 pp. [measured]
  - Traffic mix shifted toward mobile: ruled in. Mobile share of searches went from 40% to 55%. [measured]
  - v2 caused the shift to mobile, for example through changed entry points: not ruled out. This is the only path by which v2 could still explain the drop. [guess]
  - Seasonality or an external event, such as a marketing push to mobile: not ruled out. The release log shows only the v2 rollout. [inferred]
  - Incomplete data in the second week: ruled out. All 14 days have 4 rows each. [measured]
- Checks run:
  - mix_shift: flag. The change is mix-dominant (100% mix share) [check:mix_shift#1]. The standard errors assume independent units, so the intervals are probably a little too narrow.
  - completeness: pass. 2026-10-04 is fully loaded, with 4 rows, 100% of the trailing median [check:completeness#1].
  - srm: skipped. This is a before/after comparison, not an experiment with an assignment split.
  - fanout: skipped. No joins were used.

## Caveats, and what would change the answer
- The ranker is perfectly confounded with time, so the "adjusted" figure is an observational estimate and not a causal one.
- The data is daily aggregates with only platform and country. Any other change in the query mix (query type, new-user share) is invisible.
- A cause for the mobile surge would change the reading. If v2 drove it, the drop would partly be v2's. If it came from a campaign or a tracking change, v2 is cleared.
- A per-platform holdout (some traffic held on v1) would give a clean causal answer.

## Provenance
- Metric: CTR = clicks / searches, stated here [guess]. There is no metrics.json in the directory.
- Data: search_daily and release_log, through 2026-10-04 (last complete day).
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: the checks are logged in `.ds-checks.log` in the working directory. The queries were run inline and not saved. The segment aggregates came from a single query over search_daily (id q1), which the logged mix_shift check cites.