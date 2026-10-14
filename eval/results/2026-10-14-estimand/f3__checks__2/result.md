Checking is done. The mix-shift and completeness checks both passed, and here is the readout.

```
## Answer
Headline: can't tell
Overall CTR fell 1.83 pp week over week, entirely on desktop, and the timing fits v3. But v3 went to 100% at once, so there is no control group to confirm it caused the drop.
- Observed: -1.83 pp (95% CI -1.98 to -1.68) [measured]. CTR went from 30.44% to 28.61%.
- Adjusted: -1.82 pp (95% CI -1.97 to -1.67), holding platform × country mix fixed [measured]
- Causal effect: not identified (it needs a concurrent control, such as a holdout on v2 or a staggered rollout. Without one, a before/after comparison cannot separate v3 from anything else that changed on 2026-09-07.)

## What it means for the rollback decision
The whole 1.7–2.0 pp interval is far above the 0.1 pp smallest effect the mix_shift check treats as meaningful, so the drop is real. The open question is attribution, not size. If v3 is the cause, the harm is about 1.8 pp, concentrated on desktop. A rollback, or better a small v2 holdout, would settle it.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform or country): ruled out. The mix effect is -0.01 pp, about 1% of the change, and search volume is flat (699k vs 699k) [measured].
  - Incomplete data in the latest week: ruled out. 2026-09-13 has 4 of 4 expected rows and every day in both weeks is present [measured].
  - Ordinary day-to-day noise: ruled out. Daily CTR sat at 30.0–30.8% for all 7 days before and 28.3–28.9% for all 7 days after, with a clean step on 09-07 [measured].
  - A change that hit only desktop and happened to land on 09-07: not ruled out. Desktop US fell 3.1 pp and desktop other fell 2.9 pp. Mobile moved by -0.03 and -0.04 pp. v3 may behave differently on desktop, or something else may have hit desktop that day. release_log lists only v3, but that log may be incomplete [inferred].
  - Seasonality or a calendar effect: not testable. The data has only the two weeks, so there is no prior-year or earlier-week baseline [measured].
- Checks run:
  - mix_shift: pass. Within-segment -1.82 pp plus mix -0.01 pp equals -1.83 pp.
  - completeness: pass. 2026-09-13 is at 100% of the trailing median.
  - srm: skipped. There is no randomized assignment; v3 went to all traffic.
  - fanout: skipped. No joins were used.

## Caveats, and what would change the answer
- The before/after design cannot separate v3 from other changes made on 2026-09-07. A holdout or staggered rollback would.
- The intervals treat searches as independent. Repeat users would widen them somewhat.
- The data covers only 2 weeks and 4 segments. A v3 effect that differs by query type or user cohort is not visible here.
- Clicks per search is the only outcome. Satisfaction, or whether v3 reduced the need to click, is not measured.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), from stated here [guess]. There is no metrics.json in the directory.
- Data: search_daily and release_log, through 2026-09-13.
- Reconciled: not done (no dashboard or reference figure available).
- Queries and checks: the queries were run inline, with no query log. The check specs were /tmp/mix.json and /tmp/comp.json, run through checks/run.py.
```