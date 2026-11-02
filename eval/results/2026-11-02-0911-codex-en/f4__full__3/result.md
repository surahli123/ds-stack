## Answer
Headline: can't tell [inferred]

The apparent drop is −2.83 pp, but October 7 contains only hours 00–09, so the full-day change is unknown. [q2, q4] [measured]

- Observed: −2.83 pp (95% interval: −3.47 to −2.20), comparing the partial day with the full prior week; not a valid full-day comparison. [q4] [measured]
- Adjusted: +0.00 pp (95% interval: −0.66 to +0.66), holding hour mix fixed within hours 00–09 only; this does not estimate the missing hours. [check:mix_shift#1] [measured]
- Causal effect: not identified (a randomized intervention or credible controlled design would identify an intervention’s effect). [inferred]

## What it means for leadership's morning report

Report “full-day change unavailable: incomplete data,” rather than a confirmed decline. [inferred] No decision threshold was supplied; the matched-hours interval includes zero and declines up to 0.66 pp, while no full-day interval is identifiable from these data. [check:mix_shift#1] [inferred]

## Why we believe it

- Alternatives considered:
  - Incomplete day: ruled in by 10 loaded hours versus 24 on every baseline day. [q2] [measured]
  - Hour composition: ruled in for the apparent decline; prior-week CTR is 29.83% across all hours but 27.00% in matching hours, equal to the partial target day. [q3, q4] [measured]
  - Lower CTR within observed hours: ruled out descriptively; each observed hour matches its prior-week rate exactly. [q3] [measured]
  - Seasonality or weekday effects: not ruled out for the missing hours; the short history cannot establish recurring patterns. [q2] [inferred]
  - Logging or definition changes, or platform/country/source mix: not ruled out; the table lacks those dimensions and logging metadata. [q1] [inferred]
- Checks run:
  - completeness: fail incomplete: 2026-10-07: 10 rows = 42% of the trailing days (under 3 weeks of same-weekday history) median (24) [check:completeness#2] [measured]
  - completeness: pass 2026-10-06: 24 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (24) [check:completeness#1] [measured]
  - mix_shift: pass overall change +0.00 pp = within-segment +0.00 pp (95% CI -0.66 to +0.66) + mix +0.00 pp (mix share 0%) [check:mix_shift#1] [measured]
  - mix_shift: pass overall change +0.00 pp = within-segment +0.00 pp (95% CI -0.66 to +0.66) + mix +0.00 pp (mix share 0%) [check:mix_shift#2] [measured]
  - Aggregate integrity: pass unique hourly rows per date, no null/negative counts or clicks exceeding searches. [q2] [measured]
  - fanout: skipped (no joins). [measured]
  - srm: skipped (no experiment). [measured]

## Caveats, and what would change the answer

- Reload hours 10–23 and confirm ingestion completion before reporting the full-day drop. Hour presence alone does not certify ingestion completeness. [inferred]
- Intervals assume independent binary click outcomes per search; user clustering or multiple clicks per search would require a different uncertainty model. [inferred]
- Both mix checks use matching hours only; the second groups them into broader time bands. Neither extrapolates missing hours. [measured]
- Confirm the metric definition, reporting timezone, and smallest actionable change with the metric owner. [inferred]

## Provenance

- Metric: SUM(clicks)/SUM(searches); pooled September 30–October 6 baseline versus October 7, all records, hourly source grain; from stated here [guess]. No configured metrics.json.
- Data: search_hourly; hourly coverage complete through 2026-10-06, partial through hour 09 on 2026-10-07. [q2] [measured]
- Reconciled: not done (no dashboard or independent source supplied). [measured]
- Queries and checks: .ds-queries.log and .ds-checks.log; external interval calculation in ctr_checks.py. [measured]
- Verified: verify_readout: pass (37 numbers on 10 lines; 4 queries, 4 checks, 0 given)
