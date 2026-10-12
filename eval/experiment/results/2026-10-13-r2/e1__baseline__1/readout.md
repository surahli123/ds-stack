Decision: Escalate

# Ranker v7 – launch readout

**Bottom line:** The primary metric clears its pre-registered bar at the point estimate, but the Abandonment Rate guardrail is not cleared. Its point estimate is worse, and its 95% CI reaches past the pre-registered margin. The pre-registration doesn't say what to do in that case, so this needs a decision from the review. I'm not calling it Ship or Don't ship.

## Setup (checks pass)
- Clean A/B: userID, lambdamart_v6 vs lambdamart_v7 (snippet_length is the same in both arms). 50/50 split, 20% allocation, exposures balanced (PASSED).
- 1.0M users per arm, above the 900k planned. The Pulse snapshot is ds 2026-09-25, which covers the full 14 planned days (start 2026-09-12). The audit log is empty, so the config wasn't changed mid-test.
- Pulse was requested with CUPED off at 95% confidence, as the pre-registration states. There is no sequential testing or Bonferroni correction, and no interim peeking is involved since this is the single planned readout.
- Assumption: the pre-registration doesn't state units for `bar` and `margin`. I read them as relative changes. The 2% latency margin and the 0.5% bar only make sense that way, and Pulse reports percent change. If the bar is absolute (0.5 percentage points), the primary misses it (+0.33pp), and the answer moves toward Don't ship / Keep running. **Please confirm the units.**

## Primary: Successful Search Rate (bar +0.5%, ship requires point estimate at the bar)
| | Control | Test | Abs. change | Relative change (95% CI) | p |
|---|---|---|---|---|---|
| Successful Search Rate | 41.20% | 41.53% | +0.334pp | **+0.81%** (+0.41% to +1.21%) | 7e-5 |

The effect is clearly real, and the point estimate (+0.81%) is above the +0.5% bar. The CI lower bound (+0.41%) is below the bar. That is acceptable under `point_at_bar`, but the true lift could plausibly be somewhat under the bar.

## Guardrails (relative margins from prereg)
| Metric | Change (95% CI) | Margin | Status |
|---|---|---|---|
| Latency p95 | +0.2% (−0.3% to +0.7%) | 2% | OK |
| Zero Result Rate | 0.0% (−1.4% to +1.4%) | 3% | OK |
| Revenue per User | −0.1% (−0.8% to +0.6%) | −1% | OK |
| **Abandonment Rate** (lower is better) | **+0.6% worse** (−0.4% to +1.6%) | 1% | **Not cleared** (p = 0.24) |

For Abandonment Rate, a harm larger than the 1% margin is not ruled out. The data are also compatible with no harm or a small improvement. This is inconclusive, not evidence of harm.

## Secondary and segment metrics (not pre-registered as decision metrics)
- Nothing else is significant at 95%. CTR, Long Click Rate, clicks, sessions and queries per user are flat. Ad Click Rate is −0.66% (p = 0.28) and Time to First Click is slightly worse (+0.4%, p = 0.39), both within noise.
- About 40 segment cuts were examined (mobile/desktop, head/tail, navigational/informational). None has a CI that excludes zero, and there are no corrections for multiple looks. Mobile Successful Search Rate is −0.7% and Informational is −0.9%, both within noise. Treat them as hypotheses, not findings.
- Long Click Rate is flat (−0.06%), so the extra successful searches don't show up as higher click quality. That is worth a look but doesn't change the decision.

## Recommendation for the review
1. Confirm the units of the bar and margins.
2. Decide whether a possible abandonment increase of up to ~1.6% is acceptable given a ~+0.8% success lift. If the team treats the guardrail as a hard gate, don't ship on this data. Run an extension, or a larger or CUPED-adjusted analysis, to tighten the abandonment CI. CUPED would need to be a documented change from the pre-registration.
3. If the team accepts the risk, ship with abandonment monitored after launch, e.g. a holdback.
