## Answer
Headline: can't tell (the raw gap is a partial-day artifact; the like-for-like gap is 0.0 pp, interval −0.7 to +0.7 pp)
Yesterday's data stops at 09:59, so the "drop" from 29.83% to 27.0% (−2.8 pp) comes from missing the high-CTR afternoon hours, not from a fall in CTR.
- Observed: −2.83 pp (27.00% for 10 hours of 10-07 vs 29.83% for the full previous 7 days, 09-30 to 10-06) [measured]. No interval is given because the comparison is invalid.
- Adjusted: 0.0 pp (−0.66 to +0.66), holding hours 00–09 fixed (same hours, previous 7 days) [measured]
- Causal effect: not identified (no experiment or intervention here; a real change would need a complete day of data)

## What it means for the CTR-drop decision
Once hours are matched, CTR is flat, and the interval rules out a drop larger than about 0.7 pp. I'd tell leadership there is no evidence of a CTR decline yet. Re-check once 10-07 has fully loaded, which should also settle why it stopped at hour 9.

## Why we believe it
- Alternatives considered:
  - Real CTR decline: ruled out for hours 00–09 (24% in hours 0–7 and 31% in hours 8–9, identical to the baseline) [measured]
  - Time-of-day mix: ruled in as the cause. Hours 8–22 run at 31% and hours 23 and 0–7 at 24%, so a partial day with only part of the high-CTR window lowers the blended rate [measured]
  - Mix vs within-hour change: all of the observed gap is mix, and the within-hour effect is 0.0 pp [measured]
  - Whether the hours after 09:59 are late-loading or truly missing: unknown [guess]
- Checks run:
  - completeness: fail. 10-07 has 10 of 24 hourly rows, 42% of the trailing median (checks/run.py log: completeness#1)
  - mix_shift: pass. Overall change +0.00 pp, entirely within-segment, with the 95% interval ±0.66 pp (mix_shift#1). I ran it on two bands (hours 0–7 and hours 8–9), not 10 separate hours.
  - fanout and srm: skipped. There were no joins and no experiment.

## Caveats, and what would change the answer
- Only hours 0–9 of 10-07 exist. A real drop in the afternoon or evening can't be seen yet.
- The interval treats searches as independent, so it is probably somewhat too narrow. It is also wide, about ±0.7 pp, because only 19.6k searches are in the window.
- The hourly CTR values look suspiciously constant (24% and 31% exactly), which suggests the data may be synthetic or aggregated. Worth confirming the source.
- A full 10-07 showing hours 10–23 below 31% would change the answer.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), from stated here [guess]. There is no metrics.json.
- Data: search_hourly, through 2026-10-06 (the last complete day)
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: the checks are logged in .ds-checks.log (completeness#1, mix_shift#1). The SQL queries were run inline and not logged.