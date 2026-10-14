```
## Answer
Headline: can't tell
Treatment's CTR is 1.20 pp higher than control's in the raw data, but the 50/50 split failed its balance check, so I can't call that a causal lift.
- Observed: +1.20 pp (95% CI +1.13 to +1.27), treatment 31.20% vs control 30.00% CTR, clicks/searches [measured]
- Adjusted: not computed (the table has no user-level or segment columns, so there is nothing to hold fixed)
- Causal effect: not identified (we need the assignment-log cause of the 51.2/48.8 user imbalance, and ideally a re-run or an analysis restricted to correctly assigned users)

## What it means for the launch decision
The raw interval (+1.13 to +1.27 pp) is well above zero. I can't say whether it reflects the ranker or whichever users were lost or misassigned. I'd hold the decision until the SRM is explained. If the cause turns out to be harmless, the roughly +1.2 pp would stand. I have no launch threshold, so I can't say whether it clears the bar.

## Why we believe it
- Alternatives considered:
  - Chance imbalance in assignment: ruled out by SRM chi2 587, p≈1e-129 [measured]
  - Treatment losing or excluding low-engagement users (for example, a crash or logging loss), which would inflate CTR: ruled in as plausible, not tested because there is no user-level data [inferred]
  - Mix shift across segments: not testable, no segment columns [measured]
  - Day-to-day noise: unlikely, since the gap is +1.1 to +1.3 pp on all 14 days [measured]
- Checks run:
  - srm: fail. Users were 499,930 control vs 475,990 treatment (51.23% / 48.77%) against a planned 50/50 [check:srm#1]
  - completeness: could not run. It needs at least 3 earlier periods and the table only holds the 14 experiment days. All 14 days have both arms present and no gaps.
  - mix_shift: skipped, no segment data
  - fanout: skipped, no joins used

## Caveats, and what would change the answer
- The interval is a naive two-proportion CI on searches. It treats searches as independent, so the true interval is wider because searches cluster within users. [inferred]
- If the SRM cause is found and fixed, or the affected users can be identified, the lift could shrink, vanish, or stay near +1.2 pp.
- Searches per user are 6.0 in both arms, so the drop in treatment users looks like whole users missing, not lighter use. [measured]

## Provenance
- Metric: CTR = clicks / searches, summed over the period; stated here [guess], because there is no metrics.json
- Data: experiment_daily, 2026-09-17 through 2026-09-30 (all 14 days present for both arms)
- Reconciled: not done (no dashboard or source to compare against)
- Queries and checks: the queries ran inline and were not logged. The check results are in .ds-checks.log.
```