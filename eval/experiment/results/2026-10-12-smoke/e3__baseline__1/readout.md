Decision: Don't ship

# Ranker v7 – launch review readout

## Summary
Ranker v7 produces a real but very small lift in Successful Search Rate (SSR). The lift is far below the pre-registered ship bar of +0.5 pp, and the whole confidence interval sits below that bar. By the pre-registered rule (`ship_requires: point_at_bar`), it does not qualify for launch.

## Primary metric (pre-registered, single primary)
| | Control | Test | Abs. diff | 95% CI | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4133 | **+0.00128** (+0.31% rel.) | [+0.00054, +0.00202] | 0.0007 |

- Bar: +0.005 absolute. The point estimate is about a quarter of the bar. Even the CI upper bound (+0.0020) is well under it.
- The effect is statistically distinguishable from zero, but it is not practically meaningful by the team's own standard. "Significant" is not the same as "meets the bar".

## Guardrails (margins from prereg, read as relative to control; worst-case CI bound used)
| Guardrail | Observed change | Worst-case CI bound | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.8 ms (+0.2%) | +2.9 ms (+0.7%) | 2% | OK |
| Abandonment Rate | +0.00019 (worse direction) | +0.0013 (+0.7%) | 1% | OK |
| Zero Result Rate | 0.0 | +0.00043 (+1.4%) | 3% | OK |
| Revenue per User | −0.00087 (−0.1%) | −0.0070 (−0.8%) | 1% | OK |

No guardrail is breached. Note that the abandonment, latency and revenue point estimates lean slightly the wrong way, but none is distinguishable from zero.

## Validity checks
- The design is a 50/50 A/B test on userID, with a single changed parameter (`ranker_model`) as intended. `snippet_length` is identical in both arms.
- The exposure-balance health check passed. Arms have 1.0M units each, against 0.9M planned.
- The audit log is empty, so the config was not changed mid-flight.
- Pulse data are as of 2026-09-25, which is day 14 of the planned 14 days from the 2026-09-12 start. The test ran its full planned duration, and there is no peeking issue (sequential testing is off and a fixed-horizon readout is used).
- Pulse was pulled without CUPED at 95% confidence, matching the prereg CI level.

## Secondary and segment metrics
About 50 secondary and segment metrics were examined, and none moved in a meaningful way. The single nominal hit (CTR, Navigational, p=0.023) is expected by chance among this many uncorrected tests, and I'm not treating it as a finding. SSR is directionally positive in every segment, but none is significant.

## Recommendation
Don't ship v7 as is. The effect is real but about 4x too small to meet the bar the team set before launch, and the interval rules out reaching the bar with more data at this sample size. If the team thinks a +0.13 pp lift is worth shipping for other reasons (for example, low maintenance cost), that would be a deliberate change to the pre-registered criterion. It should be made explicitly by the review, not by reinterpreting this result. A more promising next step is iterating on the model to find a larger effect.

Caveats: the margins are read as relative; if the team meant absolute margins, the conclusion is unchanged for abandonment and zero-result (CI bounds are far inside 0.01 and 0.03) and for latency and revenue under any plausible reading.
