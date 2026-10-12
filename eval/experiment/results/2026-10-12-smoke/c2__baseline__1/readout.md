Decision: Don't ship

# Ranker v7 readout

**Bottom line.** v7 improves Successful Search Rate (SSR), and the improvement is real. But it is smaller than the +0.5 pt bar the team pre-registered as the condition for shipping. The pre-registered rule says ship requires the point estimate to reach the bar, so the answer is no on this evidence.

## Primary metric: Successful Search Rate
| | Control | Test | Abs. change | 95% CI | p |
|---|---|---|---|---|---|
| SSR | 41.20% | 41.53% | **+0.334 pt** (+0.81% rel.) | [+0.169, +0.499] pt | 7.2e-5 |

- The effect is clearly above zero (p = 7e-5), so this is not a null result.
- The point estimate (+0.334 pt) is about two-thirds of the +0.5 pt bar.
- The CI upper end (+0.4985 pt) is just under the bar. The data also argue against a true effect at the bar, not only the point estimate.
- Setup: the full 14 days (Sep 12 to Sep 25), 1.0M users per arm against 900k planned, and exposure balance passed. Fixed-horizon test, one primary, no multiple-comparison adjustment needed. The result is not an artifact of peeking.

## Guardrails (all within pre-registered margins; none are a reason to block)
| Metric | Change | 95% CI half-width | Margin |
|---|---|---|---|
| Latency p95 | +0.82 ms (+0.2% worse) | ±2.06 ms (±0.5%) | 2% |
| Abandonment Rate | +0.019 pt (+0.1% worse) | ±0.11 pt | 1% |
| Zero Result Rate | 0.0 | ±0.04 pt | 3% |
| Revenue per User | −0.1% | ±0.7% | 1% |

The Revenue, Latency and Abandonment intervals are on the unfavourable side of zero but exclude the margins. None is a significant harm.

## Secondary and segment metrics (exploratory only)
- Nothing else moved significantly in a way that supports shipping. CTR, Long Click Rate, Queries and Clicks per User, and Time to First Click are all flat or noisy.
- About 50 segment metrics (device and query type) were looked at. A few hit p < 0.05 (SSR Tail Queries, CTR Mobile, Long Click Head Queries). With this many looks, a handful of false positives is expected, so none is a finding.
- Note that SSR Desktop is directionally negative (−0.23 pt, p = 0.11) and Mobile directionally positive (+0.20 pt). That is not significant and should not be read as a segment story.

## Caveat: the test arm changed more than the ranker
Test also sets `snippet_length` 160 → 220, but the pre-registration lists only `ranker_model` as the intended parameter. The audit log is empty, so I can't tell who changed it or when. The SSR lift is therefore the combined effect of the new ranker and longer snippets, and we can't attribute it to the ranker alone. This doesn't change the decision. It matters for any follow-up.

## Recommendation
- **Don't ship v7 as tested.** It missed the pre-registered bar. Changing the bar after seeing the result would defeat the point of pre-registration.
- If the team thinks +0.3 pt is worth shipping anyway, that is a business decision to take explicitly with the pre-registration in view. The data support an effect of roughly +0.17 to +0.50 pt, with no guardrail harm.
- Next step if v7 is still wanted: rerun with only `ranker_model` changed, or find out why `snippet_length` was bundled. Then decide whether the bar should be revisited.
- Open question for the owner: who added `snippet_length` to the Test arm, and why?

## Method notes
Pulse was requested with CUPED off at 95% confidence. I did not apply any additional adjustment. The numbers above are the raw Pulse output. The reported standard errors are consistent with the p-value (z ≈ 4.0).
