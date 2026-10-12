Decision: Escalate

# Ranker v7 launch readout

**Summary.** The primary metric clears the pre-registered bar at the point estimate. One guardrail, Abandonment Rate, is not cleared. Its confidence interval still allows harm larger than the pre-registered margin, and the point estimate leans the wrong way. The pre-registration doesn't say what to do in that case, so the review needs to decide whether to accept the risk.

## Setup
- The test is a clean 50/50 A/B on userID, with Control `lambdamart_v6` and Test `lambdamart_v7`. Only `ranker_model` differs. `snippet_length` is 160 in both arms.
- Exposure is 1,000,000 users per arm, against 900,000 planned. The balanced-exposure health check passed.
- The audit log is empty, so nothing was changed mid-test.
- Pulse is dated 2026-09-25 and is not CUPED-adjusted. The 95% CIs are plain and unadjusted. Sequential testing and Bonferroni correction are both off.
- I assumed the pre-registered `bar` and `margin` values are relative changes. That is the only reading that works for Latency p95 and Zero Result Rate. A 0.02 ms latency margin or a 3-point Zero Result margin would be absurd. Please confirm the team means relative.

## Primary: Successful Search Rate
| | Control | Test | Abs. change | Relative change | 95% CI (relative) | p |
|---|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | +0.00334 | **+0.81%** | +0.41% to +1.21% | 7e-5 |

- The pre-registered bar is +0.5% relative, with `ship_requires: point_at_bar`. The point estimate of +0.81% clears it.
- The interval excludes zero, but its lower end (+0.41%) is below the bar. The true lift could be smaller than the bar. The pre-registered rule only asks for the point estimate, so it passes.
- If the bar was meant as an absolute +0.5 percentage points, the result (+0.33 pp) misses it. This is the second reason to confirm the units.

## Guardrails
Harm is measured against the pre-registered margin. A guardrail is cleared only if the worst end of the CI stays inside the margin.

| Guardrail | Change in the harmful direction | Worst end of CI | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.2% (412.8 vs 412 ms) | +0.7% | 2% | Cleared |
| Zero Result Rate | 0.0% | +1.4% | 3% | Cleared |
| Revenue per User | −0.1% | −0.8% | 1% | Cleared |
| **Abandonment Rate** | **+0.6%** (0.1881 vs 0.1870), p=0.24 | **+1.6%** | 1% | **Not cleared** |

- Abandonment is not significantly worse. But the point estimate is in the harmful direction, and the data can't rule out an increase of about 1.6%, which is above the 1% margin.
- Roughly 6× more data would be needed to resolve it. That is not realistic for a test that has already run its planned 14 days.

## Other observations (exploratory, not part of the decision)
- **Secondary metrics.** None moved significantly. CTR, Long Click Rate, Clicks per User and Queries per User are flat, so the lift in Successful Search Rate isn't backed by a clear change in engagement.
- **Segments.** Of about 60 segment cuts, two are nominally significant, both in the Informational segment:
  - Successful Search Rate: −0.87%, p=0.036.
  - CTR: −1.19%, p=0.044.
  - Desktop Time to First Click also improved, with p=0.027.
  - With this many uncorrected cuts, a few p<0.05 results are expected by chance. Mobile Successful Search Rate is also negative (−0.72%, not significant). I'd treat these as hypotheses to check, not findings.

## Recommendation
Don't ship automatically. Take it to the review as an explicit risk call:
1. **Accept the risk and ship.** The primary win is real. The cost is a possible abandonment increase of up to about 1.6%, which would breach the pre-registered 1% margin.
2. **Hold.** Run a longer or larger confirmation focused on Abandonment Rate, with a staged rollout and an abandonment monitor.
3. **Settle the unit question first.** Confirm whether `bar` and `margin` are relative. If the bar was absolute, this is a Don't ship.