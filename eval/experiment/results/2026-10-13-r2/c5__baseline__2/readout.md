Decision: Don't ship

# Ranker v7 – launch review readout

**Bottom line:** Ranker v7 improves Successful Search Rate (SSR), but by less than the pre-registered ship bar. Under the pre-registered rule (point estimate must reach the bar) it does not qualify for launch.

## Primary metric (pre-registered, one primary, 95% CI, no CUPED)
| | Control | Test | Abs. diff | 95% CI (abs.) | Rel. | p |
|---|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | **+0.0033** (+0.33 pp) | [+0.0017, +0.0050] | +0.81% | 7e-5 |

- The lift is real: the CI excludes zero.
- The bar was +0.005 (0.5 pp, absolute). The point estimate (+0.0033) is below it, and even the CI upper bound (+0.00499) is just under it. So this is not a case of "too noisy to tell"; the true effect is very likely smaller than the bar.
- Data: 1.0M users per arm (plan: 900k), ds 2026-09-25, start 2026-09-12 and 14-day duration, so the planned window is complete. Single look, so sequential testing is not an issue. The exposure-balance health check passed.

## Guardrails (pre-registered margins; I read them as relative, see caveat)
Worst-case = the CI bound on the harmful side.
| Metric | Observed change | Worst-case bound | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.8 ms (+0.2%) | +2.9 ms (+0.7%) | 2% | OK |
| Abandonment Rate | +0.0002 (+0.1%) | +0.0013 (about +0.7%) | 1% | OK |
| Zero Result Rate | 0.0000 | +0.0004 (about +1.4%) | 3% | OK |
| Revenue per User | -$0.0009 (-0.1%) | -$0.0070 (-0.8%) | 1% | OK, but tight |

No guardrail is breached. Revenue's worst case uses most of its margin, so it is the one to watch.

## Secondary and segment metrics
Not pre-registered and not multiplicity-adjusted, so treat them as descriptive. None is significant at 95%. CTR, Long Click Rate, queries per user and clicks per user are all flat, so there's no corroborating evidence beyond SSR. The mobile/desktop and head/tail/navigational/informational SSR splits are all within noise. I would not use any of them to justify a segment-specific launch.

## Caveats to raise in the room
1. **Bar units.** The bar is 0.005 and the prereg doesn't state units. I read it as absolute (0.5 pp), consistent with how Pulse reports `absoluteChange`. If the team meant a 0.5% *relative* lift, the observed +0.81% would clear it and the decision would flip to Ship. Please confirm the intent with the prereg authors before the meeting. I believe the absolute reading is the natural one for a rate metric.
2. **Mid-test allocation change.** The audit log shows allocation cut from 20% to 10% on 2026-09-16 (day 5 of 14). `experiment.json` still shows 20, which disagrees with the log, so someone should confirm the current state. The arms stayed 50/50 and exposures are balanced, so the comparison is probably still valid. But it pools different traffic mixes over time, and a time-varying effect or novelty effect could bias the estimate in a way Pulse can't show. This is a reason for caution, not a reason to override the result.
3. The experiment is still marked `active` past its planned 14 days. It should be stopped or ramped down deliberately.

## Recommendation
Do not ship on the current evidence. If the team still wants v7, the options are (a) decide whether a +0.3 pp lift is worth shipping and amend the bar through the normal review process, not after seeing results, or (b) iterate on the ranker. Either way, resolve the bar-units question first.
