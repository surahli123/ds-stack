## Answer
Headline: can't tell
Treatment's CTR is 1.20 pp higher in the raw data, but the arms fail the sample-ratio check, so that number can't be read as the effect of the ranker. [measured]
- Observed: +1.20 pp (95% CI +1.13 to +1.27), from 31.20% in treatment vs 30.00% in control, searches-weighted. This interval ignores the assignment problem, so it is too narrow to rely on. [measured]
- Adjusted: not computed (the data is daily aggregates by arm, with no user-level covariates or segments to hold fixed)
- Causal effect: not identified (we would need to find why treatment has about 4.8% fewer users than control, then re-run or correct the assignment)

## What it means for the launch decision
The raw interval of +1.13 to +1.27 pp sits well above zero, but the arms aren't comparable. If the missing treatment users differ from the rest, for example because low-engagement users were dropped or logging failed, the bias could be as large as the lift. I wouldn't launch on this number until the cause is found. I haven't set a minimum lift that would change the decision, so I can't compare the interval to one.

## Why we believe it
- Alternatives considered:
  - Chance imbalance in assignment: ruled out by the SRM test (p ≈ 1e-130, shares 51.2% control and 48.8% treatment against a planned 50/50). [measured]
  - Lift driven by a single day or a time trend: ruled out. Treatment is above control on all 14 days (about +1.1 to +1.3 pp), so the lift is stable. [measured]
  - Treatment losing users selectively (differential dropout or logging loss): not ruled out. It would explain both the SRM and an inflated CTR, but this data can't test it. [inferred]
- Checks run:
  - srm: fail. Users were 499,930 control vs 475,990 treatment, chi2 587, p ≈ 1e-130 [check:srm#1].
  - completeness: pass. 2026-09-30 has 2 rows, 100% of the trailing median [check:completeness#2]. The first attempt (completeness#1) could not run because I passed only one period, and the second used all 14 days.
  - mix_shift: skipped, because there are no segments in the table.
  - fanout: skipped, because I ran no joins.

## Caveats, and what would change the answer
- Find the cause of the SRM. Candidates are assignment or bucketing bugs, bot filtering applied unevenly between arms, and treatment errors or crashes that stop events being logged. Then re-run the analysis on a clean sample.
- Searches per user are identical in both arms (6.0), which suggests the aggregation is uniform and the loss is whole users.
- The CI treats searches as independent. Clicks cluster by user, so the true interval is wider. [inferred]
- The table has only arm-by-day aggregates, so I couldn't do a user-level analysis.

## Provenance
- Metric: CTR = clicks / searches, summed over the window. This is my own definition [guess]. There is no metrics.json in the directory.
- Data: experiment_daily in warehouse.db, 2026-09-17 to 2026-09-30, all 14 days present.
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: the check runs are logged in `.ds-checks.log`. The queries were run inline and not saved to a file.