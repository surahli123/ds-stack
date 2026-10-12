Decision: Ship

# Ranker v7 – launch review readout

**Bottom line:** Ranker v7 (lambdamart_v7 vs lambdamart_v6) raised Successful Search Rate by +0.81% relative (+0.33 pp; 95% CI +0.41% to +1.21% relative, p = 7e-5). The point estimate clears the pre-registered bar, and no guardrail breached its margin.

## Setup checks
- Pre-registered A/B on userID, 50/50 split, 14 days (start 2026-09-12, Pulse ds 2026-09-25 = day 14). Results are the full planned window, a single look. Sequential testing was off, so there was no peeking correction to apply.
- Exposure balance health check passed. Pulse shows 1.0M units per arm, above the 900k planned.
- The audit log is empty, so the config did not change during the run. The only parameter that differs between arms is ranker_model (snippet_length is identical), which is the intended parameter.
- Pulse used CUPED at 95% confidence, as requested.
- The experiment status is still "active". It should be concluded or rolled out as part of the launch.

## Primary (pre-registered, ship requires point estimate at the bar)
| Metric | Control | Test | Δ (abs) | Δ (rel) | 95% CI (rel) | Bar |
|---|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4134 | +0.0033 | +0.81% | +0.41% to +1.21% | +0.5% |

The point estimate (+0.81%) is above the 0.5% bar, and the CI excludes zero.

**Assumption to confirm:** prereg.json gives the bar as 0.005 with no unit. I read it as relative (0.5%), which matches how the guardrail margins must be read. A 0.03 margin on Zero Result Rate (baseline 0.031) or 0.02 on latency p95 (412 ms) is only sensible as a fraction of baseline. If the team meant 0.5 percentage points absolute, the observed +0.33 pp misses the bar. The upper CI end, +0.50 pp, would only just reach it. In that case the call becomes "Don't ship" under point_at_bar. Please confirm the unit in the review.

**The lower CI end is below the bar.** The true lift could be as low as about +0.4%. The pre-registered rule only requires the point estimate to reach the bar, so this doesn't block shipping. Expect a lift somewhere in the 0.4–1.2% range, not a certain 0.8%.

## Guardrails (worst-case end of the 95% CI vs. pre-registered margin, relative)
| Guardrail | Observed Δ | Worst CI end | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.2% (413 vs 412 ms) | +0.7% | 2% | OK |
| Abandonment Rate | +0.1% | +0.7% | 1% | OK |
| Zero Result Rate | 0.0% | +1.4% | 3% | OK |
| Revenue per User | −0.1% | −0.8% | 1% | OK |

The worst ends of the Abandonment and Revenue CIs are within about 0.2–0.3 pp of their margins. We can rule out large harms, but we can't rule out small ones near the margin.

## Secondary and exploratory (not part of the decision)
There are about 60 secondary and segment metrics, all unadjusted at 95%, so a few nominal hits are expected by chance.
- Nominal p < 0.05: Time to First Click −1.1% (better, p = 0.03). Reformulation Rate +0.84% (worse, p = 0.04). Reformulation – Navigational +2.4% (worse, p = 0.01).
- Successful Search Rate – Head Queries is −0.95% (p = 0.011), the opposite sign from the overall lift. Across the 6 Successful Search Rate segments, this one doesn't survive a Bonferroni correction (threshold 0.05/6 ≈ 0.008). It is still worth watching, because head queries are high-traffic.
- CTR (−0.02%), Long Click Rate (−0.2%) and Clicks per User (−0.5%) are flat to slightly negative. The primary lift does not show up in click volume. That is consistent with better-targeted results, but it is not proof, and it is worth a look at how "successful search" is defined.
- Desktop (−0.5%, p = 0.23) and Mobile (+0.7%, p = 0.08) go in different directions. Neither is significant and the CIs overlap heavily. We can't tell from this experiment whether v7 helps both platforms.

## Recommendation
Ship, since the pre-registered primary clears its bar and all guardrails hold. Before or alongside rollout:
1. Confirm the bar unit (relative vs absolute) as described above.
2. Monitor head-query Successful Search Rate and Reformulation Rate after launch, and keep a holdback if possible.
3. Close out the experiment's "active" status.
