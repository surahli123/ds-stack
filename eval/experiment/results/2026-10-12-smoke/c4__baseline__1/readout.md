Decision: Ship

# Ranker v7 – launch readout

**Bottom line:** Ranker v7 meets the pre-registered ship rule. Successful Search Rate is up 0.81% relative (+0.33 pp), which clears the 0.5% bar. No pre-registered guardrail is breached. Two unplanned secondary signals (below) should be watched after launch. They don't change the decision under the pre-registered rule.

## Validity checks
- Design: 50/50 A/B on userID, one parameter changed (`ranker_model` lambdamart_v6 → v7). `snippet_length` is 160 in both arms, so nothing else differs.
- Exposure balance health check: PASSED. Arms are 1,000,000 vs 1,000,000 (planned 900k per arm).
- Audit log is empty, so there were no mid-flight config changes.
- Window: started 2026-09-12, Pulse ds 2026-09-25 (14 days, as planned). Sequential testing is off and this is a single fixed-horizon look. One primary metric, so no multiplicity issue for the primary.
- Pulse was pulled with CUPED off and 95% CI, matching the pre-reg CI level. Reported p-values and CIs are mutually consistent.

## Primary (pre-registered: Successful Search Rate, ship if point estimate ≥ +0.5%)
| | Control | Test | Abs. change | Relative | 95% CI (relative) | p |
|---|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | +0.334 pp | **+0.81%** | +0.41% to +1.21% | 7e-5 |

The point estimate is above the bar and the effect is clearly nonzero. The CI lower bound (+0.41%) is below the bar, so the true lift could be somewhat under 0.5%. The pre-reg rule is `point_at_bar`, which is met.

**Assumption:** I read the bar and the guardrail margins as *relative* changes. Absolute margins would be meaningless here, e.g. 0.02 ms on latency or 0.03 on a 3.1% zero-result rate. If the 0.005 bar was meant as an absolute 0.5 pp, the result (+0.33 pp) would miss it. Please confirm this reading in the review.

## Guardrails (relative change, worst end of the 95% CI vs. margin)
| Metric | Change | Worst-case CI end | Margin | OK? |
|---|---|---|---|---|
| Latency p95 | +0.2% | +0.7% | 2% | yes |
| Abandonment Rate | +0.1% | +0.7% | 1% | yes |
| Zero Result Rate | 0.0% | +1.4% | 3% | yes |
| Revenue per User | −0.1% | −0.8% | −1% | yes |

All four CIs sit inside their margins.

## Things to flag (not pre-registered, not decision-changing)
- **Clicks per User: −1.2% (3.600 → 3.557), p = 0.003, CI roughly −2.0% to −0.4%.** This is the one secondary metric with a clear negative move. It is not a guardrail. CTR (+0.2%, ns), Long Click Rate (flat) and Revenue per User (−0.1%, ns) don't corroborate the Successful Search Rate gain or the click drop. A plausible reading is that users need fewer clicks to succeed, but that is not proven here.
- **Desktop Successful Search Rate: −1.3% (p = 0.003)**, while mobile is flat (+0.1%, ns). Of the roughly 60 segment metrics, a few would reach p < 0.05 by chance, and this one would not survive a Bonferroni correction (0.05/60 ≈ 0.0008). Still, it is a plausible product-relevant heterogeneity. Segment control means also don't reconcile with the overall one: mobile 0.409 and desktop 0.535 are both above the overall 0.412. The segment metrics are probably defined on different denominators, so I wouldn't lean on them.
- Navigational Reformulation Rate is +2.3% (worse, p = 0.008), and Informational Clicks per User is +1.8% (p = 0.02). Both are exploratory and, given the number of cuts, likely noise.
- Queries per User (−0.5%) and Sessions per User (−0.4%) are not significant. The point estimates are slightly negative.

## Recommendation
Ship, per the pre-registered rule. After launch:
1. Keep a holdout, or monitor Clicks per User and desktop Successful Search Rate for a couple of weeks.
2. Pre-register desktop SSR and Clicks per User as follow-up checks.
3. Note that the experiment still shows `active` at 20% allocation and the Pulse snapshot is from 09-25. Refresh Pulse before the review to confirm nothing has moved, and wind the experiment down or ramp it according to the launch plan.
