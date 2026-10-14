## Answer
Headline: can't tell. The −2.8 pp drop is an artifact of comparing a partial day with full days, so there is no evidence of a real drop yet.

Yesterday's data stops at 09:59 (hours 0–9 only), and a like-for-like comparison shows no change in CTR (0.0 pp).
- Observed: −2.8 pp (about −3.5 to −2.2): yesterday's 27.0% (hours 0–9 only) against 29.84% for the full prior days. The interval is a rough normal approximation [inferred].
- Adjusted: 0.0 pp (about −0.7 to +0.7), holding hour of day fixed. Hours 0–9 on 2026-10-07 gave 27.0% (5,292 clicks / 19,600 searches). The same hours over 09-30 to 10-06 gave 27.0%. The interval is a rough normal approximation [inferred].
- Causal effect: not identified (nothing was changed or randomized, and there's no comparison group. A change log or experiment record would be needed).

## What it means for the "CTR is down" escalation
The honest answer to leadership is that no drop is visible in the data so far. The matched-hours interval of about ±0.7 pp excludes the reported −2.8 pp. It does not rule out a smaller real decline of under 1 pp, and the afternoon and evening hours (10–23) haven't been observed. Re-check once the full day has loaded.

## Why we believe it
- Alternatives considered:
  - Real CTR drop: ruled out for hours 0–9, since matched-hour CTR is 27.0% vs 27.0% [measured]. Not testable for hours 10–23 because there's no data [measured].
  - Hour-of-day mix (partial day): ruled in as the cause. Overnight hours 0–7 run at 24% CTR and hours 8+ at 31%. Yesterday's data is weighted toward overnight hours, which pulls the day's CTR down [measured].
  - Pipeline or ingestion delay: ruled in as the likely reason the data stops at hour 9 [inferred]. The data can't confirm the cause.
  - Day-of-week effect: not tested, since 7 days is too short to separate it [guess].
- Checks run:
  - Row completeness per date: flag. 10-07 has only 10 of 24 hours; every other date has 24.
  - Matched-hours comparison (hours 0–9): pass. 27.0% vs 27.0%.
  - Hours 0–7 and hours 8–9 separately: pass. 24.0% vs 24.0% and 31.0% vs 31.0%.
  - Nulls and clicks > searches: pass. None found.

## Caveats, and what would change the answer
- Hours 10–23 of 10-07 are missing. A real drop there would change the answer.
- The data look unusually smooth (identical values across hours), so they may be modeled or aggregated rather than raw events. That affects how much to trust the interval.
- The baseline is only 7 days.
- I assumed hours are in one consistent timezone.

## Provenance
- Metric: CTR = clicks / searches, summed over the window (not an average of hourly rates), stated here [guess]. There is no metrics.json.
- Data: search_hourly, through 2026-10-06 (the last complete day). 2026-10-07 is partial, hours 0–9 only.
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: ad-hoc Python/SQLite run inline in this session. Nothing was saved to a file.