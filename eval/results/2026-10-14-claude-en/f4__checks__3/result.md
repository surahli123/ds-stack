Yesterday's CTR didn't actually drop. The apparent drop comes from yesterday being a partial day.

## Answer
Headline: can't tell
Yesterday's data stops at hour 9, and on a like-for-like basis (hours 0–9) CTR is flat versus the previous 7 days, so the "drop" is an artifact of the partial day.
- Observed: −2.83 pp (27.00% vs 29.83%), but the data for 2026-10-07 covers only 10 of 24 hours [measured]
- Adjusted: +0.00 pp (95% interval −0.66 to +0.66), holding hour-of-day mix fixed (hours 0–9: 27.0% yesterday vs 27.0% for the prior 7 days) [measured]
- Causal effect: not identified (no intervention or experiment in this data; a full day of data would be needed to say anything about the whole day)

## What it means for the decision
There is no evidence of a CTR problem, and the like-for-like interval of ±0.66 pp rules out drops larger than about 0.7 pp in hours 0–9. Hours 10–23 aren't loaded yet, so I can't say anything about the rest of the day. Re-check once the day completes.

## Why we believe it
- Alternatives considered:
  - Real CTR decline: ruled out for hours 0–9 by identical hourly rates, 24% in hours 0–7 and 31% in hours 8–9, on both sides [measured]. Hours 10–23 are untested [measured].
  - Hour-of-day mix: ruled in as the cause. The loaded hours are low-CTR overnight hours (0–7 run at 24%) plus only 2 daytime hours, whereas a full day is mostly 31% hours [measured].
  - Tracking or pipeline issue behind the missing hours: inferred as the cause of the missing rows. The data just stops at hour 9, so it is probably a load that hasn't finished, but I haven't confirmed that [inferred].
- Checks run:
  - completeness: fail. 2026-10-07 has 10 rows, which is 42% of the 24 expected [check:completeness#1].
  - mix_shift: pass. The change is +0.00 pp, all of it within-segment, with a 95% CI of ±0.66 pp. The CI assumes independent searches [check:mix_shift#1].
  - fanout and srm: skipped, since there were no joins or experiments.

## Caveats, and what would change the answer
- The conclusion covers only hours 0–9. A real drop in hours 10–23 can't be ruled in or out.
- The ±0.66 pp interval treats searches as independent, so it is probably somewhat optimistic.
- If the full day loads and still comes in below about 29.8%, this answer changes.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), stated here [guess]. There is no metrics.json.
- Data: search_hourly, through 2026-10-06 (the last complete day); 2026-10-07 is partial (hours 0–9).
- Reconciled: not done (no dashboard or source provided)
- Queries and checks: ad hoc SQL from this session; checks are logged in `.ds-checks.log` (completeness#1, mix_shift#1)