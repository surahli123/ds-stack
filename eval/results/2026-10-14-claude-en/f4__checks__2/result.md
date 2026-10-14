Yesterday's CTR is not down. The apparent drop comes from yesterday being only partly loaded, and the number leadership wants is 0.0 pp.

## Answer
Headline: 0.0 pp (95% interval -0.7 to +0.7 pp), like-for-like on hours 0–9

Yesterday's data stops after hour 9, and those hours are the low-traffic, low-CTR ones. Compared against the same hours of the previous 7 days, CTR is unchanged at 27.0%. The raw "drop" of about 2.8 pp is an artifact of the incomplete day. [measured]
- Observed: -2.83 pp (27.00% vs 29.83%), but this compares 10 hours of 2026-10-07 with 24 full hours per day for 09-30 to 10-06. Not a valid comparison. [measured]
- Adjusted: 0.0 pp (95% interval -0.66 to +0.66), holding hour-of-day fixed (hours 0–9 only). [measured]
- Causal effect: not identified (this is a before/after observation with no experiment or control group; nothing here suggests a change to explain anyway).

## What it means for the CTR-drop decision
There is no evidence of a real drop, and the interval rules out any decline larger than about 0.7 pp. I would not act on the 2.8 pp figure. Re-check after the full day of 10-07 loads.

## Why we believe it
- Alternatives considered:
  - Real CTR decline: ruled out by the like-for-like hours 0–9 match, 27.0% vs 27.0%. [measured]
  - Partial-day and hour-mix artifact: ruled in. Hours 0–7 run at 24% CTR and hours 8–9 at 31%. Hours 10–22 run at 31% but are missing from yesterday, so the daily average sits near 29.8%. [measured]
  - Hour-mix shift within the loaded hours: ruled out. Mix effect is 0.00 pp, and the share of traffic in hours 8–9 is 42.9% in both periods. [measured]
  - Tracking or logging change: not tested, but nothing in the data points to one. [inferred]
- Checks run:
  - completeness: fail. 2026-10-07 has 10 of 24 hourly rows, 42% of the baseline median. [check:completeness#1]
  - mix_shift: pass. Overall change +0.00 pp, with mix 0.00 pp and within-hour rate 0.00 pp (95% interval -0.66 to +0.66). [check:mix_shift#1]
  - srm and fanout: skipped. There is no experiment and no join.

## Caveats, and what would change the answer
- Hours 10–23 of 10-07 are not loaded, so I can't say whether CTR dropped later in the day. If the load completes, rerun the full-day comparison.
- The interval assumes independent searches, so it is probably a little too narrow.
- The baseline is the previous 7 days (09-30 to 10-06) only, with no same-weekday history.
- The ±0.66 pp interval is sampling noise on 10 hours of data; a drop smaller than that can't be excluded.

## Provenance
- Metric: CTR = clicks / searches, stated here [guess]. There is no metrics.json.
- Data: `search_hourly` in warehouse.db, complete through 2026-10-06. 2026-10-07 is partial (hours 0–9).
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: check results are in `.ds-checks.log`, written by `checks/run.py`. The ad-hoc SQL queries were run inline and not logged.