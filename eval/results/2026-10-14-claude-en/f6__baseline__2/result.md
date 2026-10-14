## Answer
Headline: 46.0% (95% CI 45.9% to 46.2%)
Search CTR for 2026-10-05 to 2026-10-11 was 46.0%. That is searches with at least one click divided by searches, counting external traffic only.
- Observed: 46.0% (45.9% to 46.2%), measured. The interval is a binomial sampling interval only. If the weekly figure is a full census, it is exact.
- Adjusted: not computed (single week, no comparison asked)
- Causal effect: not identified (no comparison or intervention was asked about)

## What it means for the weekly business review
This is a level for the week, not a change, so it supports no go or no-go call. Only a prior-week figure under the same definition would show whether anything moved. The table has no earlier weeks.

## Why we believe it
- Alternatives considered:
  - Include bot and internal traffic (41.4%): ruled out because bots are not users (2,074 clicks on 105k searches) and internal staff clicks differ (67% of internal searches click). [measured] Treating them as non-user traffic is my judgment. [inferred]
  - Clicks per search (64.5%): ruled out because it can exceed 100% and is not a rate of searches that got a click. [inferred]
  - Click rate among searches with results (50.1%): a plausible alternative definition. I did not use it because the question says search CTR. [inferred]
  - Platform mix: desktop and mobile are near equal in volume, and the headline pools them. [measured]
- Checks run:
  - Coverage: pass. 7 of 7 days are present, each with 6 platform-by-traffic-type rows.
  - Duplicates: pass. No repeated date, platform and traffic-type keys.
  - Daily stability: pass. Daily searches are 117k to 123k.
  - Reconcile to a dashboard: could not run. No dashboard figure or metrics.json is available.

## Caveats, and what would change the answer
- The definition is my assumption. If your review uses all traffic, the figure is 41.4%. If it uses searches with results as the denominator, it is 50.1%.
- The table holds only this one week, so there is no trend or week-over-week comparison.
- The external filter is based on the `traffic_type` label, which I did not validate.

## Provenance
- Metric: searches_with_click / searches, external traffic only, summed over both platforms, stated here [guess]. There is no metrics.json.
- Data: search_daily_v, 2026-10-05 to 2026-10-11 (all of it, complete).
- Reconciled: not done (no dashboard figure or metrics.json to compare against).
- Queries and checks: run inline in Python against warehouse.db. They are not saved to a file.