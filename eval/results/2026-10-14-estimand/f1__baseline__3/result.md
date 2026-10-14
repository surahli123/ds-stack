## Answer
Headline: can't tell
Overall CTR fell 2.10 pp, but almost all of it comes from a shift in traffic to mobile, which has a lower CTR. Within each platform and country, CTR did not change, so the data show no v2 effect on ranking quality.
- Observed: −2.10 pp (−2.25 to −1.95) [measured]. CTR went from 30.42% to 28.32%.
- Adjusted: +0.00 pp (−0.15 to +0.15), holding platform × country fixed at the week-2 mix [measured]. Segment CTRs were flat: desktop US 37.1% in both weeks, mobile US 22.7% vs 22.7%, and similar for the other two segments.
- Causal effect: not identified. A holdout or A/B arm running v1 alongside v2 would identify it. A same-day v1-vs-v2 split would be best.

## What it means for the rollback decision
Rolling back is not supported. The within-segment effect is about 0 ± 0.15 pp, while the 2.10 pp drop is explained by the traffic mix. A rollback would only be justified if the mobile shift were itself caused by v2, and these data can't show that.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (mobile share 40.1% → 55.1%): ruled in as the mechanical driver of the drop, because the adjusted effect is about 0 [measured].
  - v2 caused the mobile shift (for example through a UI or latency change): not ruled out. Ranker and week are perfectly confounded, with no concurrent v1 traffic [inferred].
  - A concurrent marketing, app-release or seasonal change: not ruled out. The release log has only one entry, and I have no other data [guess].
  - A daily pattern before the rollout: ruled out. CTR was stable at 30.1–30.8% daily in week 1 and 28.1–28.6% in week 2, with a step on 09-28 [measured].
- Checks run:
  - Rate/mix decomposition by platform × country: pass. The adjusted effect is about 0.
  - Interval widths: pass. They use a normal approximation on the binomial counts, treating searches as independent. This ignores user-level clustering, so the intervals may be somewhat too narrow.
  - Reconciliation against a dashboard: skipped (none available).

## Caveats, and what would change the answer
- Why mobile share jumped is unknown. Total searches were flat, but desktop fell about 25% and mobile rose about 37%. If v2 caused that, for example through a changed mobile UI, it would count as a v2 effect.
- This is a pre/post comparison of two weeks with no control group.
- Check with the team for any other release, tracking change or campaign on 09-28.

## Provenance
- Metric: CTR = clicks / searches, summed over rows, from stated here [guess]. No metrics.json was present.
- Data: search_daily and release_log, covering 2026-09-21 to 2026-10-04 (both weeks complete).
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: run inline in Python against warehouse.db. They were not saved to a file.