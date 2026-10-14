Both checks are done, so I'm writing up the result now.

## Answer
Headline: can't tell (a causal effect isn't identified, but the within-segment change is -0.01 pp, 95% interval -0.16 to +0.14)
Overall CTR fell about 2.1 pp, but nearly all of that is a shift in traffic toward mobile, which has a much lower CTR. CTR within each platform and country segment didn't move.
- Observed: -2.10 pp (-2.25 to -1.95), from 30.42% to 28.32% [measured]
- Adjusted: -0.01 pp (-0.16 to +0.14), holding platform × country mix fixed at the prior-week mix [measured]. The mix effect is -2.09 pp, about 100% of the drop [measured].
- Causal effect: not identified (v2 went to 100% of traffic at once, with no concurrent v1 holdout. A holdout, or a staggered or geo rollout, would identify it. The mix shift happened in the same week as the rollout, so the two can't be separated by design.)

## What it means for the rollback decision
The 2.1 pp drop shouldn't be blamed on v2 or used to justify a rollback. The within-segment interval rules out a v2 effect larger than about 0.15 pp in either direction, assuming the segments are otherwise comparable week to week. Whether a drop that small matters is your call. If you need a sharper answer, the next step is a v1 holdout.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift toward mobile: ruled in. The mobile share of searches rose from 40% to 55%, while mobile CTR is about 22% against about 36% on desktop [measured].
  - A v2 effect on ranking quality within segments: mostly ruled out. The within-segment change is about 0 in all four segments [measured]. The week-over-week comparison can't separate v2 from other time-varying factors, though [inferred].
  - Incomplete data for the latest week: ruled out. 2026-10-04 has the expected 4 rows [measured].
  - Why mobile traffic grew (a campaign, seasonality or a logging change): not investigated [guess].
- Checks run:
  - mix_shift: flag. Mix accounts for -2.09 pp and the rate effect is -0.00 pp (-0.15 to +0.15) [check:mix_shift#1].
  - completeness: pass. The last day is fully loaded [check:completeness#1].
  - srm and fanout: skipped. There is no experiment split and no joins.

## Caveats, and what would change the answer
- The intervals assume independent searches, which is likely too narrow because searches cluster within users and days.
- Only platform and country were available to adjust for. Other unobserved mix changes could still hide a v2 effect.
- A v2 effect could be hidden if v2 itself caused the mobile shift, for example through UI or latency changes. That seems unlikely but isn't tested.
- Two weeks of data with no pre-trend. A v1 holdout would settle it.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), stated here [guess]. No metrics.json was present.
- Data: search_daily and release_log, through 2026-10-04.
- Reconciled: not done (no dashboard or source to compare against).
- Queries and checks: the check results are logged in `.ds-checks.log` in the working directory. The queries ran inline and aren't saved as separate files.