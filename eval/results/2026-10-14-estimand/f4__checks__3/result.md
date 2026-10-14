## Answer
Headline: 0.0 pp (95% interval −0.7 to +0.7), measured on hours 00–09 only. Hours 10–23 of 2026-10-07 are not in the data.

The apparent drop is a partial-day artifact: the day has only hours 0–9 loaded, and those hours have a lower CTR every day. Compared on the same hours, CTR is unchanged. [measured]
- Observed: −2.83 pp (27.00% for partial 10-07 vs 29.83% for the full-day average of 09-30 to 10-06). This number is misleading because the hours covered differ. [measured]
- Adjusted: 0.00 pp (−0.66 to +0.66), holding hours of day fixed (hours 0–9, 10-07 vs the same hours over 09-30 to 10-06; 27.00% vs 27.00%). [measured]
- Causal effect: not identified (this is a before/after comparison with no control, and a null result here wouldn't need one).

## What it means for the search CTR decision
There is no evidence of a drop. The interval of ±0.66 pp rules out a decline larger than about 0.7 pp in hours 0–9, but it says nothing about hours 10–23, which hold most of the traffic. Don't report a drop or raise an alarm. Re-check once the full day has loaded. [inferred]

## Why we believe it
- Alternatives considered:
  - Real CTR decline: ruled out for hours 0–9 by the hour-matched comparison, 0.00 pp [measured]. Not testable for hours 10–23.
  - Time-of-day mix shift: this explains the whole gap. Hours 0–7 run at 24% and hours 8–23 at 31% every day. The partial day contains only the low hours, with 57% of its searches in hours 0–7 vs 43% in hours 8–9. [measured]
  - Late-loading data (the pipeline hasn't finished 10-07): likely cause of the missing hours, but I can't confirm it from this database. [inferred]
  - Day-of-week effect: not checked, since the data has only 7 prior days. [guess]
- Checks run:
  - completeness: fail. 10-07 has 10 of 24 hourly rows (42% of the trailing median) [check:completeness#1].
  - mix_shift: pass. Within-segment change is +0.00 pp (95% CI −0.66 to +0.66) and the mix effect is 0.00 pp, using hours 0–7 and 8–9 as segments [check:mix_shift#1]. The interval assumes independent searches.
  - srm, fanout: skipped. This is not an experiment and there are no joins.

## Caveats, and what would change the answer
- The data stops at hour 9 on 10-07. If the later hours load and CTR is lower in them, there could still be a real drop.
- The interval treats searches as independent, so it is probably somewhat too narrow.
- The previous-7-day baseline is perfectly flat (29.83% daily, identical per-hour rates), which looks synthetic or pre-aggregated. Worth confirming the source.
- Dashboard definitions of CTR (for example, per-session or deduplicated clicks) could differ from clicks divided by searches.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), from the table columns. No metrics.json exists, so this definition is stated here [guess].
- Data: search_hourly in warehouse.db. The last complete period is 2026-10-06; 10-07 is partial (hours 0–9).
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: the checks are logged in `.ds-checks.log` (completeness#1, mix_shift#1). The SQL was ad hoc and is not saved to a file.