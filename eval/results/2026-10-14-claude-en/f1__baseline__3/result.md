## Answer
Headline: can't tell
Overall CTR fell 2.10 pp week over week, but the drop comes almost entirely from a shift in traffic toward mobile, which has lower CTR. Within each platform×country segment, CTR is unchanged after v2 (about −0.01 pp), so the data gives no sign that v2 lowered CTR.
- Observed: −2.10 pp (95% CI −2.25 to −1.95); CTR went from 30.42% to 28.32%.
- Adjusted: −0.01 pp (95% CI −0.16 to +0.15), holding the platform×country mix fixed at last week's. Method: week-2 segment CTRs reweighted to week-1 traffic shares.
- Causal effect: not identified. v2 went to 100% of traffic, so there is no concurrent control group. Identifying it would take a holdback or A/B slice on v1, or a reason for the mobile shift that is independent of v2.

## What it means for the rollback decision
The adjusted interval rules out a within-segment loss larger than about 0.16 pp. The 2.1 pp drop is therefore not evidence that v2 hurts CTR, so rolling back on this number is unsupported. If the team's smallest meaningful loss is under about 0.15 pp, the data can't rule it out. If the mobile shift turns out to be caused by v2, the rollback question changes.

## Why we believe it
- Alternatives considered:
  - Traffic-mix shift (Simpson's paradox): ruled in. Mobile's share of searches rose from 40.2% to 55.0% (computed from the weekly search counts), while each segment's CTR is flat (for example desktop US 37.07% in both weeks and mobile US 22.66% → 22.71%) [measured]
  - v2 lowering CTR within segments: ruled out at the ±0.16 pp level, since every segment's CTR is within about 0.1 pp of last week's [measured]
  - Mobile growth caused by v2 (for example a v2-driven redirect of traffic): not ruled out. The data has no acquisition or source information, and the shift is a step on 09-28 that coincides with the rollout [inferred]
  - Seasonality, other releases, or a logging change: not ruled out. release_log lists only v2, and there is no earlier history to compare against [inferred]
- Checks run:
  - Daily CTR series: pass. The shift is a clean step at 09-28 with low day-to-day noise inside each week.
  - Segment-level before/after table: pass. All four segments are flat.
  - Standard-error check on the adjusted estimate: pass. The delta method treats the segment CTRs as binomial, giving SE 0.08 pp.
  - Pre-trend or placebo week: could not run. The data covers only 2 weeks.
  - Reconciliation to a dashboard: skipped. No dashboard or metrics.json was provided.

## Caveats, and what would change the answer
- Only two weeks of data, and a before/after design with no control group.
- The adjustment covers only platform and country. Other mix changes, such as query type, are not observed.
- If v2 itself drove the mobile traffic increase, part of the drop would be v2's doing. This could be checked with traffic-source data or a holdback.
- The intervals treat searches as independent, so they ignore user-level clustering and are probably a little too narrow.

## Provenance
- Metric: CTR = clicks / searches, summed across segments and days [guess]. No metrics.json was found.
- Data: search_daily and release_log, through 2026-10-04.
- Reconciled: not done (no dashboard or metrics.json available).
- Queries and checks: ad hoc Python/sqlite3 run inline in this session; not saved to a file.