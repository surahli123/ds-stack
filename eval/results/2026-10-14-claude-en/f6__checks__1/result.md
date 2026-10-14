## Answer
Headline: 46.0 % (95% CI 45.9 to 46.2), search CTR for 2026-10-05 to 2026-10-11, counting external traffic only and treating a search as clicked if it had at least one click.

Search CTR was about 46.0 % that week. The number depends on two choices that I made without a metric definition: whether bots are excluded, and whether CTR counts searches or clicks.
- Observed: 46.0 % (45.9 to 46.2) [measured]. This is external traffic, searches with a click divided by searches. The interval is a binomial approximation that treats searches as independent.
- Adjusted: not computed (there is no prior period or comparison to adjust).
- Causal effect: not identified (this is a single-week level, so there is no intervention to identify).

## What it means for the weekly business review
This is a level, not a change, so there is no decision threshold to compare it with. The sampling interval is about ±0.1 pt, which is far smaller than the 5 to 20 pt spread between the definitions below. The definition matters much more than the sampling noise, so confirm it before the number is quoted or trended.

## Why we believe it
- Alternatives considered:
  - Include bot and internal traffic (all rows): 41.4 %. Ruled out because bot CTR is about 2 %, and bots are 12.5 % of searches, so they drag the rate down [measured].
  - Exclude bots only (external plus internal): 47.1 %. Not chosen because internal is likely staff traffic. The external-only figure is cleaner for a business review [inferred].
  - Clicks divided by searches: 64.5 % for external. Ruled out as the headline because it can exceed 100 % and counts repeat clicks. It is the likely alternative definition if the dashboard uses it [measured, inferred].
  - Platform mix: external desktop and mobile have almost identical volume and CTR, so mix does not drive the figure [measured].
- Checks run:
  - completeness: pass. 2026-10-11 has 6 of 6 expected rows (100 % of the trailing median), and every day in the week has 6 rows [check:completeness#1].
  - mix_shift: skipped. There is no before/after period to compare.
  - fanout: skipped. I used no joins.
  - srm: skipped. This is not an experiment.

## Caveats, and what would change the answer
- No metrics.json exists, so the CTR definition and the traffic filter are my guesses. Using clicks/searches or including bots changes the figure to 64.5 % or 41.4 %.
- The data covers only this one week (42 rows), so I could not compare it with other weeks or reconcile it with a dashboard.
- The interval assumes independent searches. Searches from the same user are correlated, so the true interval is wider.

## Provenance
- Metric: external-traffic searches_with_click / searches, from stated here [guess].
- Data: search_daily_v, through 2026-10-11 (complete).
- Reconciled: not done (no dashboard or metric spec available).
- Queries and checks: the checks log is in .ds-checks.log (completeness#1). The queries were run inline and were not logged.