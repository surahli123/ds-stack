Decision: Don't ship

**Ranker v7 raises Successful Search Rate by enough to meet the bar, but it breaches the pre-registered Abandonment Rate guardrail.**

**Primary metric (Successful Search Rate, bar +0.005 absolute)**
- The lift is +0.00511 (41.20% → 41.71%), or +1.24% relative. The 95% CI is ±0.00165, so it runs from about +0.0035 to +0.0068.
- The pre-registration's ship rule is "point_at_bar", so the point estimate only has to reach the bar, and it does (0.00511 vs 0.005). The CI lower bound is below the bar, so we are sure there is a lift, but not sure it is at least 0.005. The margin over the bar is thin.

**Guardrails (margins read as relative changes, 95% CI)**

| Metric | Change | Margin | Result |
|---|---|---|---|
| Abandonment Rate | +2.2% ±0.7 (worse), absolute +0.0041 ±0.0013, p≈0 | 1% | **Breached** |
| Latency p95 | +0.2% ±0.5 | 2% | Pass |
| Zero Result Rate | 0.0% ±1.4 | 3% | Pass |
| Revenue per User | −0.1% ±0.7 | 1% | Pass |

- Abandonment is the only breach. Even the favourable end of its CI (+1.5% worse) is beyond the 1% margin, so noise doesn't explain it.
- I read the margins as relative changes. The latency margin of 0.02 only makes sense that way.
- If the team meant the Abandonment margin as absolute (0.01), it would pass. That is worth confirming in the room, but the relative reading is the consistent one.
- The Abandonment increase looks real. CTR (+1.9%) and Clicks per User (+2.1%) also rose, and Long Click Rate was flat (−0.09%, p=0.76). More clicks without more long clicks, together with more abandonment, suggests the new ranker produces more shallow clicks without producing more satisfying results.
- Abandonment is worst on head queries (+1.55% ±1.49). Subgroups are secondary and exploratory, so treat that as a lead only.

**Experiment health**
- Exposures are balanced (health check passed), with 1,000,000 units per arm against 900,000 planned.
- The config is a clean 50/50 A/B test with a single changed parameter (`ranker_model`), as the pre-registration intended.
- The audit log is empty, so there were no mid-test changes.
- Pulse is dated 2026-09-25, the last day of the 14-day window. The test is still marked "active", so it hasn't been formally concluded.
- Sequential testing and multiple-comparison correction are both off. That is fine for one primary metric, but the guardrail CIs are uncorrected across four guardrails. The Abandonment breach is far enough out that this doesn't change the conclusion.
- Pulse ran without CUPED, as requested.

**Recommendation**
- Don't ship v7 as is.
- Investigate why abandonment rises, starting with head queries.
- If a revised ranker removes the abandonment regression and keeps the primary lift, re-test it.
- If leadership is willing to trade a roughly 2% abandonment increase for a roughly 0.5-point success-rate gain, that is a call to override the pre-registered guardrail explicitly. The data does not make that call for us.