Decision: No effect found

# Ranker v7 readout

**Bottom line:** Ranker v7 did not move the primary metric, and the pre-registered ship bar was not met. There is nothing here to justify a launch. I found no evidence that it harms anything either.

## Primary metric: Successful Search Rate
| | Control | Test | Change | 95% CI | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4125 | +0.00049 abs (+0.12% rel) | −0.0015 to +0.0025 abs (−0.36% to +0.60% rel) | 0.62 |

- The pre-registration says to ship only if the point estimate reaches the bar of 0.005. The point estimate is +0.0005 absolute (+0.12% relative), so it falls short whichever way the bar is read.
- The prereg doesn't say whether 0.005 is absolute or relative.
  - Read as absolute (0.5 percentage points), the CI upper bound of +0.0025 rules out reaching the bar.
  - Read as relative (0.5%), the CI upper bound of +0.60% does not rule it out, but the point estimate is still well below it.
- Either way, the result is consistent with zero. Effects much larger than about +0.25 percentage points (+0.6% relative) are unlikely.

## Test validity
- The experiment ran the planned 14 days, with 1.0M units per arm against 0.9M planned.
- The split is 50/50 and the exposure-balance health check passed.
- The audit log is empty, so no config changes were made mid-test.
- Only the intended parameter (`ranker_model`) differs between arms.
- Sequential testing is off and the analysis is a single fixed-horizon read, so the p-values are valid as reported.
- CUPED is off, as requested.

## Guardrails
All four are within their pre-registered margins. The margins read as relative changes, and the CI bounds below are approximate relative figures.

| Metric | Change | CI half-width | Margin |
|---|---|---|---|
| Latency p95 | +0.2% | ±0.5% | 2% |
| Abandonment Rate | +0.1% | ±0.6% | 1% |
| Zero Result Rate | 0.0% | ±1.4% | 3% |
| Revenue per User | −0.1% | ±0.7% | 1% |

## Secondary and segment metrics (exploratory)
I checked about 60 secondary and segment metrics. Five of them have p < 0.05, which is roughly what chance alone would give at that count. None was pre-registered and I applied no multiple-comparison correction, so I wouldn't act on any of them.
- Navigational Successful Search Rate: −0.0039, p = 0.039.
- Head-query Time to First Click: p = 0.031, in the worse direction.
- Mobile Clicks per User: −0.093, p = 0.011.
- Informational Clicks per User: +0.052, p = 0.033, in the opposite direction.
- The Desktop Successful Search Rate (−0.0043, p = 0.065) and overall Clicks per User (p = 0.056) are not significant. CTR and Long Click Rate are also flat.

These point the wrong way as often as the right way. They don't support a segment-level win, and they aren't strong enough on their own to count as harm.

## Recommendation
- Don't launch v7 on this evidence. It showed no measurable gain and costs an engineering rollout.
- Treat the result as a null: the test was adequately powered for a 0.5-point effect and found none.
- Before any follow-up, the team should settle whether the bar is absolute or relative and write that into the prereg.
- A follow-up would only be worth running if there is a design change that could plausibly produce a larger effect.