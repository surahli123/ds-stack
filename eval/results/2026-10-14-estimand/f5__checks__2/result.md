```
## Answer
Headline: can't tell
Treatment's CTR is higher by 1.2 pp in the raw data, but the arms fail the sample-ratio check, so I can't tell you whether that is a real lift. [measured]
- Observed: +1.20 pp (95% CI +1.13 to +1.27), from 31.20% treatment vs 30.00% control, clicks/searches [measured]
- Adjusted: not computed (the table has only daily arm totals, with no user-level or segment columns to adjust on)
- Causal effect: not identified (we need to find why assignment is 51.2/48.8 instead of 50/50, then re-check or re-run. Without that, the arms may not be comparable.)

## What it means for the ranker_boost launch decision
I'd hold the launch decision until the split problem is explained. Nothing here tells me the smallest lift that would change the decision. The raw interval is well above zero, but it is only valid if the arms are comparable, and the SRM check says they may not be.

## Why we believe it
- Alternatives considered:
  - Real treatment effect: not ruled out. The raw gap is large relative to its noise (CI excludes 0), but SRM undermines the comparison [measured]
  - Biased or dropped assignment, such as treatment losing users or a logging/filtering difference: not ruled out, and it is the likely reason for the SRM. The treatment arm has about 24k fewer users than control. If the missing users were disproportionately low-clickers, the raw lift would be inflated. [inferred]
  - Incomplete data for the last day: ruled out, since 2026-09-30 is fully loaded [measured]
- Checks run:
  - srm: fail. Shares are 51.23% control vs 48.77% treatment, chi2 587, p≈1e-129 (id srm#1)
  - completeness: pass. 2026-09-30 has 2 rows, 100% of the trailing median (id completeness#1)
  - fanout: skipped, because I ran no joins
  - mix_shift: skipped, because there is no segment data and I'm not comparing periods

## Caveats, and what would change the answer
- The interval is a simple two-proportion interval on searches. It treats searches as independent, but searches from the same user are correlated, so the true interval is wider. [inferred]
- The daily split is almost identical each day (control about 35.7k users, treatment about 34.0k). This points to a systematic cause, such as assignment or logging, and not random noise. [inferred]
- The lift could change a lot once the SRM cause is found. User-level data and the assignment logs would let me check this.
- The clicks and searches definitions are assumed, because there is no metrics file.

## Provenance
- Metric: CTR = clicks / searches, summed over the 14 days and each arm, stated here [guess]. No metrics.json exists.
- Data: experiment_daily, 2026-09-17 to 2026-09-30, all 14 days complete
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: the checks are logged in .ds-checks.log (srm#1, completeness#1). The queries and CI calculation were ad hoc Python against warehouse.db and are not logged.
```