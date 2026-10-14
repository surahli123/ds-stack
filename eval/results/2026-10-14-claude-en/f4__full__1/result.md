```
## Answer
Headline: can't tell
Yesterday (2026-10-07) is only partly loaded (hours 0-9 of 24), so the apparent drop is not a real day-level number. [check:completeness#2]
- Observed: -2.83 pp (-3.46 to -2.20) [q1]
- Adjusted: 0.00 pp (-0.66 to +0.66), holding hour of day fixed [check:mix_shift#1]
- Causal effect: not identified (no randomized test or intervention design; none was asked about)

## What it means for the CTR-drop decision
The -2.83 pp is a partial-day artifact: the loaded hours are mostly overnight, low-CTR hours (24% vs 31% in hours 8-9), and compared hour for hour yesterday matches the prior 7 days (27.0% vs 27.0% over hours 0-9) [q2, q3, q4]. The interval of -0.66 to +0.66 pp means a drop under about 0.7 pp can't be excluded, and the full day has not landed. [check:mix_shift#1]

## Why we believe it
- Alternatives considered:
  - Incomplete data for yesterday: ruled in; only 10 of 24 hourly rows exist, 42% of the usual 24 [q1, check:completeness#2] [measured]
  - Hour-of-day mix shift: ruled in as the explanation; the hours 0-9 profile is identical in both windows (24% for hours 0-7, 31% for hours 8-9) and the mix effect is 0.00 pp [q3, q4, check:mix_shift#1] [measured]
  - Real within-hour CTR decline: ruled out for hours 0-9 (within-segment 0.00 pp, CI -0.66 to +0.66) [check:mix_shift#1]; hours 10-23 are unobserved [inferred]
  - Day of week / seasonality: not separately tested, the 7 prior days are flat at about 29.83% daily [q1] [inferred]
  - Logging or definition change: no evidence, but cannot be excluded for the missing hours; the ingest may be delayed [guess]
- Checks run:
  - completeness: fail 2026-10-07 has 10 rows, 42% of the median 24 [check:completeness#2]
  - mix_shift: pass hour-matched change +0.00 pp, mix share 0% (hours 0-7 vs 8-9 segments) [check:mix_shift#1]
  - fanout: skipped, no joins used
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- Hours 10-23 for 2026-10-07 are missing; once loaded, rerun the comparison. A real drop would show in those hours.
- The observed interval is a two-proportion interval assuming independent searches; the mix_shift interval does the same.
- The mix_shift segments are only two coarse hour bands, and the per-hour rates are identical, so a finer grain would agree.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) over search_hourly, by date, stated here [guess] (no metrics.json; DS_OVERLAY_DIR is unset)
- Data: search_hourly, through 2026-10-06 complete (2026-10-07 only hours 0-9)
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (53 numbers on 10 lines; 4 queries, 2 checks, 0 given)
```