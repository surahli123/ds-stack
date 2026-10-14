## Answer
Headline: can't tell. Overall CTR fell 1.83 pp (95% CI −2.06 to −1.59), but this data can't show how much of that v3 caused.

Overall CTR fell from 30.44% to 28.61%. The whole drop is on desktop, and it began the day v3 shipped. Rollout was to 100% of traffic at once, so no group was left on v2 to compare against.

- Observed: −1.83 pp (−2.06 to −1.59), 30.44% → 28.61%. The interval comes from a t-test on the 7 daily CTRs per week. [measured]
- Adjusted: −1.81 pp, no interval, holding the platform × country mix at last week's weights. The mix barely moved, so this is almost the same as the observed change. [measured]
- Causal effect: not identified. A holdout, a staged rollout, or a per-user v2/v3 split would identify it. A pre/post comparison alone can't separate v3 from anything else that changed that week.

## What it means for the rollback decision
Say the smallest drop that would justify a rollback is about 0.5 pp. The observed interval is well beyond that, but it is a before/after change, not a v3 effect. The pattern points at v3, but it isn't proof. If a rollback or a 10–50% holdout is cheap, run that as the test.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform or country): ruled out. Search volumes per segment are nearly identical across the two weeks (about 700k searches each week). [measured]
  - Mobile also dropping: ruled out. Mobile CTR is flat (US 22.66% → 22.63%, other 21.23% → 21.19%). [measured]
  - Desktop-only drop: desktop US went 37.1% → 34.0% and desktop other 34.8% → 31.9%, so the whole decline is on desktop. [measured]
  - v3 causing the desktop drop: plausible, since the timing matches. Mobile doesn't show it, so v3 would need to affect desktop only. A desktop-specific change shipped the same day would look identical. [inferred]
  - Noise: ruled out. Every day of week 2 is below every day of week 1, and week-1 daily CTR stays in a tight 30.1–30.8% band. [measured]
  - Seasonality or a coincident event: not testable. There is only one prior week and the release log lists nothing else. [guess]
- Checks run:
  - Segment mix stability: pass. Mix is unchanged between the weeks.
  - Daily consistency: pass. The drop appears on all 7 days.
  - Holdout or concurrent control: could not run. v3 went to 100% of traffic on the same day.
  - Longer pre-period trend: could not run. The table only covers these 2 weeks.

## Caveats, and what would change the answer
- The 1.83 pp figure is the change in overall CTR, not the v3 effect. If something else hit desktop that week, v3's share would be smaller.
- Because mobile is flat, any v3 effect on mobile is roughly zero. Mobile can't serve as a control, since mobile also ran v3.
- Data covers only 2026-08-31 to 2026-09-13. More weeks of history, plus other releases or incidents from that week, would help.
- A holdout or staged rollout would turn this into an actual effect estimate.

## Provenance
- Metric: CTR = clicks / searches, summed over segments. Stated here [guess]. There is no metrics.json.
- Data: `search_daily` (56 rows) and `release_log`, through 2026-09-13.
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: run inline in Python/sqlite and not saved to a file. They are the segment, daily and t-test queries above.