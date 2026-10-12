Decision: Ship

# Ranker v7 – launch readout

**Bottom line:** Ranker v7 raised Successful Search Rate (SSR) by +0.81% relative (95% CI +0.41% to +1.21%, p=7e-5). That clears the pre-registered 0.5% bar on the point estimate, which is the rule the team set (`ship_requires: point_at_bar`). No pre-registered guardrail breached its margin. Recommend shipping, with the caveats below.

## Test validity
- Clean two-arm A/B on userID. Control `lambdamart_v6` vs test `lambdamart_v7`. The only parameter that differs is `ranker_model`, the intended one. `snippet_length` is 160 in both arms.
- 50/50 split, 1,000,000 users per arm (plan was 900k). The exposure-balance health check passed.
- Fixed-horizon test, no sequential testing. The Pulse snapshot is ds 2026-09-25, the 14th day from the 2026-09-12 start, so the planned duration is complete. The CIs are valid for a single look.
- The audit log is empty, so there were no mid-test config changes.
- Pulse was pulled with CUPED off, 95% CI. These are unadjusted numbers.
- The experiment still shows `status: active` in Statsig, and the snapshot is about 2.5 weeks old. Someone should confirm nothing changed after 9/25 and conclude the experiment.

## Primary metric (pre-registered)
| Metric | Control | Test | Abs Δ | Rel Δ (95% CI) | Bar | Result |
|---|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | +0.0033 | +0.81% (+0.41%, +1.21%) | +0.5% | Point estimate above bar |

The CI lower bound (+0.41%) is below the 0.5% bar. The prereg requires the point estimate to be at the bar, not the lower bound, so the rule is met. The true lift could plausibly be a bit under 0.5%. It is very unlikely to be zero or negative.

**Assumption to confirm:** the prereg gives `bar: 0.005` with no unit. I read it as relative (0.5%), the same convention as the guardrail margins. For example, the latency margin of 0.02 can only mean 2%. If the team meant an absolute +0.005 (about 1.2% relative), the point estimate (+0.0033) and even the CI upper bound (+0.0050) fall short, and the decision would flip to Don't ship. Please confirm the unit in the review.

## Guardrails (pre-registered, relative margins)
The table compares the worst end of each 95% CI with its margin.

| Guardrail | Rel Δ (95% CI) | Worst case vs margin | Status |
|---|---|---|---|
| Latency p95 | +0.2% ±0.5% | +0.7% vs 2% | OK |
| Abandonment Rate | +0.1% ±0.6% | +0.7% vs 1% | OK |
| Zero Result Rate | 0.0% ±1.4% | +1.4% vs 3% | OK |
| Revenue per User | −0.1% ±0.7% | −0.8% vs 1% | OK |

Abandonment and revenue have the thinnest headroom. Both stay within margin even at the CI extremes, and neither is statistically significant.

## Things to know (not blocking, not pre-registered)
- **Ad Click Rate fell 2.8%** (0.0520 → 0.0505, p=0.022). It is not a prereg guardrail, and Revenue per User is flat (−0.1%, p=0.78). If ad CTR is a leading indicator for revenue, watch it post-launch.
- **Engagement metrics do not corroborate the SSR lift.** CTR (+0.2%), Clicks per User (+0.6%) and Long Click Rate (−0.4%) are all non-significant. Queries per User is −0.8% (p=0.076). SSR is the pre-registered primary, but the review should know the lift is not visible in the other click metrics.
- **Segment cuts are exploratory.** About 60 secondary and segment metrics were checked with no multiplicity correction, so a few nominal hits are expected by chance. The notable ones are Desktop Clicks per User (−2.0%, p=0.026), Desktop Time to First Click (+1.9% slower, p=0.044), Tail-query Time to First Click (−2.5%, faster, p=0.033) and Informational Clicks per User (+2.1%, p=0.037). Desktop SSR is +0.84% against Mobile +0.07%, but neither segment is significant and the difference between them was not tested. I would not act on any of these without a follow-up.

## Recommendation
Ship Ranker v7, conditional on the review confirming the bar is relative (0.5%). Monitor Ad Click Rate and Revenue per User after launch. Consider a holdback to check that the SSR lift holds.
