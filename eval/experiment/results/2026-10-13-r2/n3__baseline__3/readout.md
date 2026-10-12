Decision: No effect found

# Ranker v7: launch review readout

**Bottom line.** The experiment was run as planned and is complete. Ranker v7 did not move the primary metric, and the data rule out the improvement we pre-registered as the bar for shipping. It doesn't meet the ship criterion. I recommend not launching it on this evidence. Nothing here shows v7 is harmful.

## Primary metric (pre-registered): Successful Search Rate
| | Control | Test | Abs. diff (test − control) | 95% CI | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4118 | −0.0002 (−0.05% rel.) | [−0.0014, +0.0010] | 0.74 |

- The pre-registered ship rule needs the point estimate at or above +0.005 absolute. I read the bar as absolute, since the prereg doesn't say. If it were relative (+0.5% ≈ +0.002), the conclusion would be the same.
- The point estimate is −0.0002. The CI's upper end is +0.0010, a fifth of the bar. A lift of the size we wanted is ruled out, so this is a well-powered null and not an inconclusive result.
- The result is not statistically distinguishable from zero. Any true effect lies between about −0.14 and +0.10 percentage points.

## Design and validity
- A/B test on userID, 50/50 split (Control `lambdamart_v6`, Test `lambdamart_v7`). The only parameter that differs is `ranker_model`, as intended. `snippet_length` is 160 in both arms.
- 1.0M units per arm against 900k planned. The data end 2026-09-25, the 14th day after the 2026-09-12 start, so the planned duration is complete.
- The exposure-balance health check passed. The audit log has no changes after launch.
- Sequential testing and multiplicity correction were off, and Pulse was pulled without CUPED. The 95% CIs are plain fixed-horizon intervals, which suits a single look at the planned end.

## Guardrails (pre-registered margins)
| Metric | Change (rel.) | 95% CI | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.2% | ±0.5% | 2% | OK |
| Abandonment Rate | +0.1% | ±0.6% | 1% | OK |
| Zero Result Rate | 0.0% | ±1.4% | 3% | OK |
| Revenue per User | −0.1% | ±0.7% | 1% | Within margin, but the lower bound (−0.8%) is close |

Each guardrail's CI stays inside its margin. Revenue is the only one with little room.

## Secondary and exploratory metrics (not decision-driving)
- 56 secondary metrics were tracked with no multiplicity correction, so about 3 would be expected to land at p<0.05 by chance.
- Two did, and neither was pre-registered:
  - Queries per User +1.9% (p=0.028).
  - Ad Click Rate −1.5% (p=0.013). It points the "wrong" way for revenue, but Revenue per User shows nothing.
- Treat both as hypotheses, not findings. The segment cuts show no consistent pattern: Informational +0.24pp (p=0.09) and Navigational −0.24pp (p=0.12) are opposite and not significant. Mobile, desktop, head and tail are all null.

## Recommendation and caveats
- The ship bar was not met, and further running won't change that: the precision is already tight relative to the bar.
- Revisit only with a different ranker change, or if the team decides a much smaller lift is worth shipping. That would be a new decision, not a reading of this result.
- If the team wants to follow up on Ad Click Rate or Queries per User, run a new pre-registered test.
