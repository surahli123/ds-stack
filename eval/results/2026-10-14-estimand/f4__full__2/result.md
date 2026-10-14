## Answer
Headline: 0.00 pp (-0.66 to +0.66) [check:mix_shift#1]
There is no measurable CTR drop: 2026-10-07 has only hours 0-9 loaded, and the apparent fall is the low-CTR overnight hours being overrepresented in that partial day; hour-for-hour CTR is 27.0% on both sides [q4, check:mix_shift#1].
- Observed: -2.83 pp (-3.46 to -2.20), 27.0% for the partial day vs 29.83% for the prior 7 full days [q2, q5]
- Adjusted: 0.00 pp (-0.66 to +0.66), holding hour-of-day mix fixed (hours 0-9 only, both sides) [check:mix_shift#1]
- Causal effect: not identified (no randomized test or intervention is involved; the question is descriptive)

## What it means for the CTR report to leadership
Do not report a drop: the interval of -0.66 to +0.66 pp on the like-for-like comparison [check:mix_shift#1] is consistent with no change, and only a change larger than that could be called real. Hours 10-23 of 2026-10-07 are missing, so the full-day figure can't be known yet [check:completeness#1].

## Why we believe it
- Alternatives considered:
  - Hour-of-day mix (partial day): ruled in by hours 0-7 run at 24% CTR and hours 8-23 at 31% in the prior week, and yesterday has only hours 0-9 [q3, q4] [measured]
  - Data completeness: ruled in, 10 of 24 hourly rows loaded [check:completeness#1] [measured]
  - A real within-hour CTR decline: ruled out to within about 0.7 pp, since hour-matched CTR is 27.0% vs 27.0% [q4, check:mix_shift#1] [measured]
  - Day-of-week/seasonality: not ruled out separately; daily CTR for the prior 7 days is flat at 29.83-29.84% [q2] [inferred]
  - Logging or definition change: no sign in the data, but only one table was available [guess]
- Checks run:
  - completeness: fail 2026-10-07 has 10 rows = 42% of the usual 24 [check:completeness#1]
  - mix_shift: pass hour-matched change +0.00 pp (95% CI -0.66 to +0.66), mix share 0% [check:mix_shift#1]
  - fanout: skipped, no joins
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- Yesterday is only hours 0-9 (about 19,600 searches). Reload the pipeline and rerun with the full day to confirm.
- The mix check used two hour bands (0-7, 8-9) from q3. The band rates are exactly constant across days, so a finer grain would give the same answer.
- Interval assumes independent searches; it ignores clustering by user and is likely too narrow.
- No metrics.json was available, so the CTR definition is my own.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) over search_hourly, pooled, not an average of hourly rates, stated here [guess]
- Data: search_hourly, through 2026-10-06 (2026-10-07 is incomplete, hours 0-9 only)
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (44 numbers on 11 lines; 4 queries, 2 checks, 0 given)