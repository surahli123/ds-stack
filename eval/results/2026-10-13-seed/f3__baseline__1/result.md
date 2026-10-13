## Answer
Headline: -1.83 pp (95% CI -1.98 to -1.68), the full week-over-week drop, with v3 the likely cause

Overall CTR fell from 30.44% to 28.61%. The whole drop is on desktop, where CTR fell about 2.9 pp in both US and other, and it began on the first v3 day. Mobile CTR did not change.

## What it means for the rollback decision
Even the optimistic end of the interval (-1.68 pp) is a clear loss. Unless a loss of about 1.7 pp overall (about 3 pp on desktop) is acceptable, this points toward rolling back, or at least rolling back desktop. That rests on v3 being the cause, which this data can't fully confirm. It is a before/after comparison with no concurrent control group.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform or country): ruled out. Searches per segment are within 1% between weeks (699,485 vs 699,266 total), and the within-segment CTR changes sum to the full drop. [measured]
  - Gradual or noisy trend: ruled out. Daily CTR was steady at 30.1–30.8% before and 28.3–28.9% after, with a step on 09-07. [measured]
  - An external shock that hit everything: partly ruled out. Mobile is flat (22.7% vs 22.6% in the US, 21.2% vs 21.2% elsewhere). [measured]
  - A desktop-only external event coinciding with the rollout: not ruled out. release_log lists only the v3 rollout, but it may not record other changes. [inferred]
  - Mobile as a control for v3: ruled out as a control. It also ran v3, so it shows v3 had no effect on mobile, not what desktop would have done without v3. [inferred]
- Checks run:
  - Segment decomposition by platform and country: pass. Desktop US 37.1% to 34.0%, desktop other 34.8% to 31.9%. [measured]
  - Interval: pass. Two-proportion standard error of 0.077 pp, treating searches as independent. [measured]
  - Ranker label vs date: pass. v2 appears only through 09-06 and v3 only from 09-07, with all 28 segment-days in each week. [measured]
  - Randomized or concurrent control: could not run. v3 went to 100% of traffic, so no v2 traffic remains.

## Caveats, and what would change the answer
- Before/after design: any desktop-specific change that week (UI, tracking, seasonality, a bot filter) would be folded into the -1.83 pp.
- The interval covers sampling noise only. Searches are not independent (repeat users), so the true interval is somewhat wider.
- Two weeks only, and no earlier weeks to show normal week-to-week CTR variation.
- A desktop-only effect from a ranker change is plausible but unexplained. Check whether v3 changed desktop layout or result types, or whether desktop click logging changed.
- A holdback test (for example 5% of desktop traffic on v2) would settle causality.

## Provenance
- Metric: overall CTR = sum(clicks) / sum(searches) over each week, stated here [guess]. No metrics.json was present.
- Data: search_daily and release_log in warehouse.db, covering 2026-08-31 to 2026-09-13, both weeks complete.
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: ad-hoc Python/sqlite3 run in this session. They are not saved to a file.