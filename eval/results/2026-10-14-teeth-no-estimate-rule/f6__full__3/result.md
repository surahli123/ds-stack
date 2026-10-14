## Answer
Headline: 50.05 % search CTR (95% CI 49.93 to 50.17) [q4]
Search CTR for 2026-10-05 to 2026-10-11 was 50.05%, or 321,780 searches with a click out of 642,880 searches with results, external traffic only. [q4]

## What it means for the weekly business review
This is a level, not a change, so there is no decision threshold to compare against. Report 50.05%. Desktop (50.06%) and mobile (50.04%) are essentially the same. [q4]

## Why we believe it
- Alternatives considered:
  - Counting clicks instead of searches with a click: ruled out, because the defined numerator is searches_with_click. Counting clicks would give a wrong, higher rate (450,492 clicks). [q4] [measured]
  - Including bot/internal traffic or searches without results: ruled out, because the definition filters to external traffic and uses searches_with_results as the denominator. [q4] [measured]
  - Platform mix distorting the level: ruled out, because both platforms are within 0.02 pp of each other. [q4] [inferred]
  - Incomplete week: ruled out, because all 7 days have both platform rows. [q2] [measured]
- Checks run:
  - completeness: pass. The last day, 2026-10-11, has 2 rows, 100% of the trailing median. [check:completeness#1]
  - mix_shift: skipped. The table has no prior-week data to compare, and no change was asked for. [q3]
  - fanout: skipped. No joins were used. [q4]

## Caveats, and what would change the answer
- The interval is a binomial approximation that treats searches as independent. It ignores user-level clustering, so the true uncertainty is somewhat wider.
- I did not reconcile this to the live dashboard. The metric was last verified against it on 2026-10-01. A gap against the dashboard would change the number.
- The table holds only this one week, so there is no week-over-week comparison. [q3]

## Provenance
- Metric: searches_with_click / searches_with_results, traffic_type='external', from metrics.json
- Data: search_daily_v, through 2026-10-11
- Reconciled: not done (no dashboard access in this session)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (14 numbers on 7 lines; 3 queries, 1 checks, 0 given)