## Answer
Headline: 0.0 pp (-0.66 to +0.66 pp) [check:mix_shift#1]
There is no measurable CTR drop. 2026-10-07 has only hours 0-9 loaded, and on those same hours the prior 7 days had the same CTR (27.0% on both sides) [q3, check:mix_shift#1]. The naive 27.0% vs 29.83% (about -2.83 pp) is a partial-day artifact [q2, q4].

## What it means for the decision to escalate or act on a CTR drop
The interval (-0.66 to +0.66 pp) is centered on zero [check:mix_shift#1]. A 0.1 pp change would be the smallest of interest [check:mix_shift#1], and the interval is too wide to exclude that, but nothing points to a real drop. Re-check once the full day lands.

## Why we believe it
- Alternatives considered:
  - Data completeness (partial day): ruled in by 10 of 24 hourly rows loaded for 2026-10-07, 42% of normal [q2, check:completeness#1] [measured]
  - Hour-of-day mix (hours 0-7 run 24% CTR, hours 8-9 run 31%; a day missing the high-CTR late hours looks lower): ruled in as the cause of the naive gap, since like-for-like mix share is 0% and within-hour change is 0.0 pp [q3, check:mix_shift#1] [measured]
  - Real within-segment CTR decline: ruled out, rate effect 0.0 pp (-0.66 to +0.66) [check:mix_shift#1] [measured]
  - Day of week / seasonality: not separately tested; the prior 7 days are flat at 29.83% daily [q2] [inferred]
  - Logging or definition change: no evidence in the data; only one table is available [q1] [inferred]
- Checks run:
  - completeness: fail 2026-10-07 has 10 rows, 42% of the trailing median of 24; yesterday is not usable as a full day [check:completeness#1]
  - mix_shift: pass on hour groups 0-7 and 8-9, overall change 0.00 pp, mix share 0% [check:mix_shift#1]
  - mix_shift on full-day aggregate: could not run, needs 2 segments [check:mix_shift#2]
  - fanout: skipped, no joins used
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- Hours 10-23 of 2026-10-07 are not loaded. If CTR is low in those hours, a real drop could still appear. Rerun after the load completes.
- The interval treats hourly searches as independent and is conservative. It is based on counts from only 10 hours.
- The prior-7-day baseline is only one week, so a weekday effect cannot be separated.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches), from search_hourly, all hours, [guess]. No metrics.json was available (DS_OVERLAY_DIR unset), so this definition is stated here [guess]
- Data: search_hourly, through 2026-10-06 (last complete day; 2026-10-07 partial)
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (39 numbers on 10 lines; 4 queries, 3 checks, 0 given)