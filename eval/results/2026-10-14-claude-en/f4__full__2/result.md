## Answer
Headline: +0.0 pp (-0.66 to +0.66) [check:mix_shift#1]
There is no measurable CTR drop: 2026-10-07 is only partly loaded (hours 0-9), and over those same hours CTR was 27.0% on both 10-07 and the previous 7 days [q4, check:mix_shift#1].
- Observed: -2.83 pp (-3.46 to -2.20) [q2, q4] (naive 10-07 partial-day CTR of 27.0% vs 29.83% for the full previous 7 days; this is a time-of-day artifact, not a real drop)
- Adjusted: +0.0 pp (-0.66 to +0.66), holding hour of day fixed [check:mix_shift#1]
- Causal effect: not identified (no intervention; observational comparison only)

## What it means for the decision to treat the CTR "drop" as real
The like-for-like interval of -0.66 to +0.66 pp includes zero, so there is no evidence of a drop; a real drop would need to be larger than about 0.7 pp to show up with data this thin [check:mix_shift#1]. Re-check once 10-07 has fully loaded.

## Why we believe it
- Alternatives considered:
  - Partial-day / data completeness: ruled in as the source of the apparent drop; 10-07 has 10 of 24 hours while every prior day has 24 [q2] [measured]
  - Mix-shift (time of day): ruled in for the naive number, because 10-07 holds only low-CTR early hours (24% in hours 0-7, 31% in hours 8-9); matched on hour the change is 0.00 pp [q3, check:mix_shift#1] [measured]
  - Seasonality / day of week: not separable; the comparison is 1 partial day vs 7 days, and the previous 7 days vary little (29.83% to 29.84% daily) [q2] [inferred]
  - Logging or definition change: no sign in hourly data, since each hour's CTR on 10-07 equals its 7-day value [q3] [inferred]
  - A real product-driven drop: ruled out for hours 0-9 by the matched comparison [check:mix_shift#1] [measured]; hours 10-23 are not observed [inferred]
- Checks run:
  - completeness: fail 2026-10-07 is incomplete (10 of 24 hours loaded) [check:completeness#1]
  - mix_shift: pass hour-bucket matched change +0.00 pp, mix share 0% [check:mix_shift#1]
  - fanout: skipped no joins
  - srm: skipped not an experiment

## Caveats, and what would change the answer
- Hours 10-23 of 10-07 are not loaded, so full-day CTR is unknown; reload and rerun to settle it.
- The interval treats each search as independent, so it is likely too narrow; hourly counts are identical day to day, which suggests the data may be synthetic or smoothed.
- Hours were grouped into two buckets (0-7, 8-9) because the data show two distinct levels; per-hour grain gives identical rates [q3].
- The naive interval was computed by hand from q2/q4 totals with a normal approximation; it is not a logged check.

## Provenance
- Metric: Search CTR = sum(clicks) / sum(searches), from search_hourly, daily grain [guess] (no metrics.json; DS_OVERLAY_DIR unset)
- Data: search_hourly, through 2026-10-06 (last complete day; 10-07 only hours 0-9)
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (55 numbers on 12 lines; 3 queries, 2 checks, 0 given)