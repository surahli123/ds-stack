Decision: Don't ship

**Ranker v7 raises Successful Search Rate, but not by as much as the pre-registered ship bar requires.**

**Primary metric (Successful Search Rate)**
- Control is 41.20% and Test is 41.53%. The lift is +0.334 pp absolute, or +0.81% relative.
- The 95% CI is +0.169 to +0.502 pp, and p = 7e-5. The effect is real.
- The prereg says to ship only if the point estimate reaches the bar of 0.005 (0.5 pp). The point estimate is 0.33 pp, so the bar is not met.
- The CI's upper end just touches 0.5 pp. The data do not rule out a lift that large, but they do not show one either.
- I read the 0.005 bar as absolute, in the same units as the metric. If the team meant a 0.5% relative lift, the bar would be met (0.81%). Please confirm which was meant. If it was relative, the verdict flips to Ship, since all the guardrails pass.

**Guardrails (all within margin, so none block a ship)**

I read the prereg margins as relative, and I checked that none of the guardrails breach their margin under an absolute reading either.

| Metric | Change | CI half-width | Margin | Result |
|---|---|---|---|---|
| Latency p95 | +0.2% (worse) | ±0.5% | 2% | Pass |
| Abandonment Rate | +0.1% (worse) | ±0.6% | 1% | Pass |
| Zero Result Rate | 0.0% | ±1.4% | 3% | Pass |
| Revenue per User | −0.1% | ±0.7% | 1% | Pass |

**Test validity**
- The run lasted the full 14 days (Sep 12 to Sep 25). Both arms have about 1.0M units, above the planned 900k per arm.
- The audit log is empty, so the config did not change during the test.
- Only `ranker_model` differs between arms (`snippet_length` is the same), which matches the intended parameters.
- Sequential testing is off and there was a single pre-registered primary, so there is no peeking or primary-metric multiplicity problem.
- **Open item:** `experiment.json` lists exposures of 1,010,000 Control and 990,000 Test. If that split is real, it is a severe sample-ratio mismatch (about 14σ). Pulse shows 1.0M units in each arm, and Statsig's balance check says PASSED. The config figure is probably a later or different snapshot, but someone should confirm it before the review. A real mismatch would invalidate this readout. It would not change the decision, because we still would not ship.

**Exploratory findings (not decision-relevant, not corrected for multiple comparisons)**
- Clicks per User is down 1.0% (p = 0.014). It is the only notable secondary movement, and the other click metrics are flat.
- Tail-query abandonment is up (p = 0.034), and navigational and informational long-click rates are down (p ≈ 0.054). These are among about 60 secondary and segment metrics, so a few nominal hits are expected by chance.
- Neither Clicks per User nor tail abandonment is a pre-registered guardrail, so they do not drive the decision. They are worth a look if v7 is iterated on.

**Recommendation**
- Don't ship v7 as is.
- If the team believes the true lift is at or above 0.5 pp, the choice is to extend the run or iterate on the model. At the current CI width (±0.165 pp), the lower bound will not reach the bar.
- The alternative is to amend the bar. That should be done openly, because changing it after seeing results undermines the prereg.