## Answer
Headline: 0.0 pp (95% CI −0.15 to +0.15 pp) attributable to v2. The overall change was −2.10 pp.
Overall CTR fell from 30.4% to 28.3% (−2.10 pp). Almost all of that is a shift in traffic mix toward mobile, which has a lower CTR. Within each platform and country, CTR did not change.

## What it means for the rollback decision
The interval rules out a v2 effect larger than about 0.15 pp in either direction. That is about 7% of the observed drop. A rollback would not recover the −2.1 pp. This data gives no reason to roll back for CTR. The smallest effect that would change the decision is the team's call; I don't have a threshold.

## Why we believe it
- Alternatives considered:
  - v2 lowered CTR: ruled out by within-segment CTR being flat across all four platform×country segments, with a standardized rate effect of −0.01 pp at week-1 mix [measured]
  - Traffic mix shift: ruled in. Mobile's share of searches rose from 40% to 55% (desktop-US 33%→25%, desktop-other 27%→20%, mobile-US 22%→30%, mobile-other 18%→25%), and mobile CTR is about 22% against about 36% on desktop [measured]
  - Why the mix shifted: not explained by this data. It could be a marketing push, seasonality, or v2 changing platform routing, which I can't check [guess]
  - Day-to-day noise: a week-over-week comparison, so day-of-week effects cancel. Daily CTR is stable within each week [measured]
- Checks run:
  - Mix/rate decomposition: pass. The rate effect is −0.01 pp at week-0 mix and +0.003 pp at week-1 mix, so it is robust to the choice of weights.
  - Binomial CI on the rate effect: pass. About ±0.15 pp. It ignores day-level overdispersion, so the true interval is somewhat wider [inferred].
  - Pre-trend or holdout: could not run. v2 went to 100% of traffic, so there is no concurrent v1 control. The v1/v2 split is perfectly confounded with the week.

## Caveats, and what would change the answer
- v2 coincides exactly with the week, so any other change that week is indistinguishable from v2 in this data. The within-segment comparison is only valid if segment membership itself isn't affected by v2.
- If v2 caused the mobile shift, for example through app or UI changes shipped with it, the mix change would count as a v2 effect. I found nothing in the release log supporting that; it only lists the v2 rollout.
- It covers one week on each side and four coarse segments. Finer segments, such as query type, could still hide effects.
- Finding out why mobile traffic grew would settle this.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), stated here [guess]. There is no metrics.json.
- Data: search_daily and release_log, through 2026-10-04 (both weeks complete)
- Reconciled: not done (no dashboard or reference figure available)
- Queries and checks: run inline in Python/sqlite3 and not saved to a file. They are the grouped sums by date/ranker and week/platform/country, plus the standardized decomposition, all reproducible from search_daily.