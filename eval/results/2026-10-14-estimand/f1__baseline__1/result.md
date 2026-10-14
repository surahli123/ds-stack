## Answer
Headline: −0.01 pp (±0.16 pp) is the mix-adjusted change in CTR. This is not a causal estimate of v2.
Overall CTR fell about 2.1 points, but almost all of it comes from a shift in traffic toward mobile, which has lower CTR. Within each platform and country, CTR did not change.
- Observed: −2.10 pp (−2.25 to −1.95), from 30.42% to 28.32% [measured]
- Adjusted: −0.01 pp (−0.16 to +0.15), holding platform × country mix fixed at the prior-week mix [measured]
- Causal effect: not identified. Everything switched to v2 on one day with no holdout, so v2 can't be separated from the traffic shift. What would identify it is a v1 holdout or a staggered rollout.

## What it means for the rollback decision
The mix-adjusted interval (−0.16 to +0.15 pp) says v2 has no CTR effect within any platform/country segment, to within about 0.15 pp. The observed ~2.1 pp drop is not evidence against v2 on this data, so the drop alone is not a reason to roll back. If a v2 harm below roughly 0.2 pp would change the decision, this data can't rule it out.

## Why we believe it
- Alternatives considered:
  - Traffic-mix shift to mobile: ruled in. Mobile share of searches went from 40% to 55% (desktop US 33%→25%, mobile US 22%→30%), while segment CTRs were flat (e.g. desktop US 37.07% vs 37.07%, mobile US 22.66% vs 22.71%) [measured]
  - v2 lowering CTR within segments: ruled out to within ±0.16 pp [measured]
  - Why mobile share jumped on 09-28: unexplained. It could be a coincidence (a campaign, seasonality or an app release), or v2 changing who searches, which would be a real v2 effect [guess]
  - Day-to-day noise: ruled out. Daily CTR is stable at 30.1–30.8% before and 28.1–28.6% after, so the step is sharp and coincides with the rollout [measured]
- Checks run:
  - Standardization (direct, fixed prior-week mix): pass, −0.008 pp. The decomposition holds across all four segments [measured]
  - Interval method: flag. These are binomial normal approximations, so they ignore day-level clustering. Daily variation is small, but they may be slightly narrow [inferred]
  - Complete weeks and coverage: pass. 7 days each, 4 segments, v1 only before and v2 only after [measured]
  - Holdout or concurrent control: could not run. There was no v1 traffic after 09-28.

## Caveats, and what would change the answer
- The mobile shift is not explained. If v2 caused it, for example by changing mobile usage, part of the observed drop would belong to v2.
- Only one week on each side, and the segments are coarse. Effects on query type or novelty are not visible here.
- release_log has only the v2 entry, so I can't tell whether anything else shipped that week, such as a mobile or app change.
- Checking what drove the mobile traffic shift would settle the open question.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), pooled over days. No metrics.json was present, so this definition is stated here [guess]
- Data: search_daily (platform × country × ranker × date) and release_log, 2026-09-21 to 2026-10-04
- Reconciled: not done (no dashboard or reference figure available)
- Queries and checks: ad hoc Python/sqlite3 run inline. No script file was saved.