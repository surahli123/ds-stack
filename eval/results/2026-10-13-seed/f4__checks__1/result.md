## Answer
Headline: can't tell. The 2026-10-07 data is only partly loaded. On a like-for-like basis the drop is 0.0 pp (95% interval about ±1.2 pp).

The apparent drop is a partial-day artifact, not a real fall in CTR. Yesterday has only hours 0–9, and those are low-traffic, low-CTR hours. [measured]

## What it means for the decision
There is no evidence of a CTR decline. For hours 0–9, yesterday matches the prior 7 days at 27.0% vs 27.0%. The interval would still hide a drop of about 1.2 pp or less, so I can't call it fully safe until the rest of the day loads.

## Why we believe it
- Alternatives considered:
  - Real CTR drop: ruled out for hours 0–9 by yesterday's 27.0% (5,292 of 19,600) matching the prior-7-day 27.0% (37,044 of 137,200) for the same hours [measured]. Hours 10–23 are not loaded, so they can't be assessed.
  - Day-vs-day comparison (about 27.0% vs 29.8%, a 2.8 pp "drop"): ruled out because yesterday has 10 of 24 hours. Night hours 0–7 run about 24% and daytime hours about 31% [measured].
  - Segment mix shift: not run, because the table has no segment dimension. Hour of day is the mix that explains the gap, and the same-hours comparison controls for it [inferred].
  - Late-evening or later-hours issue: can't be excluded, since those hours are missing [guess].
- Checks run:
  - completeness: fail. 2026-10-07 has 10 rows, 42% of the 24-row median.
  - same-hours comparison: pass. The difference is 0.0 pp.
  - mix_shift: skipped. There are no segments in the data, so I used the hour-matched comparison instead.
  - fanout and srm: skipped. There are no joins or experiments.

## Caveats, and what would change the answer
- Rerun once all 24 hours of 2026-10-07 are loaded, and ask the pipeline owner why the load stopped at hour 9.
- The ±1.2 pp interval is a simple binomial approximation on pooled counts. It ignores day-to-day variation, which is small here (prior days all sit at 29.83%).
- The data is hourly aggregates, so I couldn't look for user-level or segment effects.

## Provenance
- Metric: CTR = clicks / searches, summed over the period, from stated here [guess]. There is no metrics.json.
- Data: search_hourly, through 2026-10-06 (last complete day). 2026-10-07 is partial, hours 0–9 only.
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: the checks log is in `.ds-checks.log` (completeness#1). The queries were run inline and are not saved to a file.