## Answer
Headline: 46.0 % (95% CI 45.9 to 46.2)
Search CTR for 2026-10-05 to 2026-10-11 was 46.0%. This counts external traffic only, with CTR defined as searches with a click divided by searches. [measured]
- Observed: 46.0 % (45.9 to 46.2), external traffic, 698,782 searches. The interval is a binomial approximation that treats searches as independent. [measured]
- Adjusted: not computed (there is no comparison period, so there is nothing to adjust)
- Causal effect: not identified (this is a single-week level, not a change; a causal claim would need a randomized experiment or a comparison period)

## What it means for the weekly business review
Report 46.0%. The definition matters far more than the sampling noise. Including bot and internal traffic gives 41.4%, and counting clicks instead of searches with a click gives 64.5%. The ±0.1 pp sampling interval is small next to those gaps. Do not compare this figure to a CTR that was defined differently.

## Why we believe it
- Alternatives considered:
  - All traffic, including bots: ruled out. Bots click on 2.0% of searches and internal traffic on 67.2%, so including them gives 41.4% and distorts the figure. [measured]
  - Clicks divided by searches: ruled out as the headline. It gives 64.5% on external traffic, and a rate above 100% for internal traffic, so it is not a per-search rate. [measured]
  - Searches with a click divided by searches with results: ruled out. It gives 50.1%. A denominator of all searches is the more standard definition for CTR. [inferred]
  - Platform difference: ruled out. Desktop is 46.06% and mobile is 46.04%. [measured]
- Checks run:
  - completeness: pass. 2026-10-11 has 6 rows (2 platforms × 3 traffic types), equal to the median of the prior days, so the week is fully loaded.
  - mix_shift: skipped, because there is no before/after period.
  - srm: skipped, because there is no experiment.
  - fanout: skipped, because no join was used.

## Caveats, and what would change the answer
- No metrics.json exists, so the CTR definition and the exclusion of bot and internal traffic are my choices, not an official definition. Confirm them with the metric owner. [guess]
- The warehouse holds only this one week, so I can't give a week-over-week change.
- The interval ignores correlation between searches from the same user or session, so the true interval is somewhat wider.

## Provenance
- Metric: sum(searches_with_click) / sum(searches), where traffic_type = 'external', from stated here [guess]
- Data: search_daily_v, 2026-10-05 through 2026-10-11 (the only data present, and complete)
- Reconciled: not done (no dashboard or other source was available)
- Queries and checks: the queries were run ad hoc and not saved. The completeness check is logged in .ds-checks.log as completeness#1.