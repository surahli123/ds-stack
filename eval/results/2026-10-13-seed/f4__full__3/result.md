## Answer
Headline: 0.0 pp (-0.66 to +0.66 pp) [check:mix_shift#1]
The apparent drop is a partial-day artifact: 2026-10-07 has only hours 0-9 loaded (CTR 27.0% [q2]), and on the same hours the prior 6 days also ran 27.0% [q5], so there is no measurable change; the full-day comparison (27.0% vs 29.83% [q2, q6]) is not like for like.

## What it means for reporting the CTR drop to leadership
Do not report a drop: the interval of -0.66 to +0.66 pp [check:mix_shift#1] excludes the roughly -2.8 pp the naive comparison suggests [q2, q6], but it cannot rule out a real change of up to about 0.7 pp, and the rest of the day (hours 10-23) has not landed, so the full-day number can't be read yet.

## Why we believe it
- Alternatives considered:
  - Data completeness (partial day): ruled in as the explanation; 2026-10-07 has 10 of 24 hours while every prior day has 24 [q2], and hours 8-9 run at 31% CTR vs 24% for hours 0-7 so a partial day reads low [q4] [measured]
  - Mix-shift across hours: ruled out on matched hours, mix effect 0.0 pp, mix share 0% [check:mix_shift#1] [measured]
  - Day of week / seasonality: ruled out for the matched window, daily hour 0-9 CTR was 26.985-27.015% on all 7 days [q3] [measured]
  - Logging or definition change: no sign of it; clicks never exceed searches and no zero-search hours [q2], hourly CTR is identical across prior days [q4] [inferred]
  - Real behavioral decline in the morning: ruled out within +/-0.66 pp [check:mix_shift#1] [measured]
- Checks run:
  - completeness: fail 2026-10-07 is not fully loaded (10 of 24 hours) [check:completeness#1]
  - mix_shift: pass on hour-matched windows, change 0.00 pp, CI -0.66 to +0.66 [check:mix_shift#1]
  - fanout: skipped, no joins
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- Hours 10-23 of 2026-10-07 are missing; reload and rerun for a full-day number, which would settle whether the afternoon and evening moved.
- The interval assumes independent searches (per the check), so it is probably a bit too narrow; session-level data would fix that.
- Hourly data is a synthetic-looking, very regular series; confirm the table is the source of truth.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) from search_hourly, pooled over hours, stated here [guess] (no metrics.json; DS_OVERLAY_DIR unset)
- Data: search_hourly, through 2026-10-06 (2026-10-07 only hours 0-9 loaded)
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (38 numbers on 9 lines; 5 queries, 2 checks, 0 given)