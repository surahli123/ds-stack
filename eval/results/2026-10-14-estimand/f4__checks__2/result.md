## Answer
Headline: can't tell. The "drop" is a partial-day artifact, and the like-for-like change is 0.0 pp.

Yesterday (2026-10-07) is only partly loaded, with hours 0–9 of 24. Over those same hours, CTR was 27.0%, and it was also 27.0% over the same hours in the previous 7 days.

- Observed: −2.83 pp (27.0% for the partial day vs 29.83% for the previous 7 full days). No interval, because the comparison is invalid. [measured]
- Adjusted: 0.00 pp, holding hour-of-day fixed (hours 0–9 on both sides, 5,292/19,600 vs 37,044/137,200). Every hour matches exactly, so I did not compute an interval. [measured]
- Causal effect: not identified. No intervention or experiment is in the data.

## What it means for the decision
Don't report a CTR drop to leadership. The apparent −2.8 pp is the daily CTR mixing hours 0–7, which run at 24% CTR, with hours 8–9, which run at 31%, so a partial day looks low. Re-check once hours 10–23 have loaded. Any change much smaller than the 2.8 pp "drop" would be invisible at this point, because the hour-matched difference is zero.

## Why we believe it
- Alternatives considered:
  - Real CTR decline: ruled out by hour-matched rates being identical (24% for hours 0–7, 31% for hours 8–9, in both periods) [measured]
  - Time-of-day mix from the partial day: ruled in as the cause of the gap [measured]
  - Pipeline or data-loading lag: ruled in as the reason the day is partial [inferred]
- Checks run:
  - completeness: fail. 2026-10-07 has 10 rows, 42% of the 24-row median [check:completeness#1]
  - mix_shift: skipped. I compared hour by hour directly, and the within-hour change is zero
  - srm and fanout: skipped. There is no experiment and no join

## Caveats, and what would change the answer
- Hours 10–23 for 10-07 are not loaded. A real drop in the later hours would not show up here.
- Hours 0–9 of the baseline are identical across the 7 days (the per-hour sums are exactly equal). That looks synthetic or smoothed, so I would verify the source.
- Only the pooled 7-day baseline was compared. Per-day variation is tiny (29.83–29.84%).

## Provenance
- Metric: CTR = clicks / searches, summed over hours [guess; no metrics.json exists]
- Data: search_hourly, with full days through 2026-10-06 and 10-07 partial (hours 0–9)
- Reconciled: not done (no dashboard or source given)
- Queries and checks: the checks are logged in .ds-checks.log. The queries were run inline and are not logged.