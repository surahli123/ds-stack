## Answer
Headline: can't tell. The like-for-like change is 0.0 pp (95% interval about −0.66 to +0.66 pp). [measured]
The apparent drop (27.0% vs 29.8%, about −2.8 pp) doesn't come from searches getting worse. 2026-10-07 only has hours 0–9 loaded, and those are the low-CTR overnight hours. [measured]

## What it means for reporting a CTR drop to leadership
Don't report a drop. For hours 0–9, CTR on 10-07 matches the prior 7 days exactly (27.0% vs 27.0%). The interval is about ±0.66 pp, so it can't rule out a real change of up to roughly that size. It would take a full day of data to see anything smaller. [measured]

## Why we believe it
- Alternatives considered:
  - Real CTR decline: ruled out for hours 0–9. Hours 0–7 are 24.0% on both sides and hours 8–9 are 31.0% on both sides. Hours 10–23 aren't loaded yet, so a decline there is untested. [measured]
  - Partial-day / time-of-day mix artifact: ruled in. The prior-7-day figure of 29.83% covers all 24 hours. Hours 10–23 carry higher CTR, so the 10-07 figure is lower only because those hours are missing. [measured]
  - Tracking or logging change in the data: ruled out for hours 0–9. Hourly searches and clicks on 10-07 equal the 09-30 values exactly (for example, 1,400/336 and 4,200/1,302), and the other days show the same hourly pattern. [measured]
- Checks run:
  - completeness: fail. 10-07 has 10 of 24 hourly rows, 42% of the trailing median.
  - mix_shift (hour buckets 0–7 and 8–9, same hours across both periods): pass. Overall change is 0.0 pp, mix effect is 0.0 pp, and the noise floor is 0.68 pp.
  - fanout and srm: skipped. There were no joins and no experiment.

## Caveats, and what would change the answer
- Only hours 0–9 of 10-07 exist. Once the full day loads, rerun the comparison. A drop that starts after hour 9 would show up then. [inferred]
- The interval treats searches as independent, which is a rough assumption. It also rests on only about 19,600 searches on 10-07. [measured]
- The prior-7-day window is 09-30 to 10-06. I assumed it includes no unusual days. [guess]
- The first mix_shift run used hand-estimated baseline counts, which I then corrected. The corrected run is the one reported. [measured]

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), stated here [guess]. There is no metrics.json.
- Data: search_hourly, through 2026-10-06 (the last complete day).
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: the checks are logged in `.ds-checks.log` in the working directory. The queries were run inline and not saved to a file.