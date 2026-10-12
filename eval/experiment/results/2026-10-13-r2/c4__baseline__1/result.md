Decision: Ship

**Ranker v7 readout (Pulse snapshot 2026-09-25, 95% CI, no CUPED)**

**Result:** Ship. The primary metric clears its pre-registered bar, and no guardrail breaches its margin. Two caveats below need an owner at the review.

**Setup**
- The test is a clean 50/50 A/B on userID, run 2026-09-12 to 09-26. Pulse's last day is 09-25, so it covers the full 14 days.
- Each arm has 1,000,000 units, against 900,000 planned.
- The exposure-balance health check passed, and the audit log shows no mid-flight changes.
- Sequential testing and Bonferroni correction are off. That fits a single pre-registered primary read once at the planned end.

**Primary: Successful Search Rate**

| | Value |
|---|---|
| Control | 41.20% |
| Test | 41.53% |
| Absolute change | +0.334 pp (95% CI +0.169 to +0.498 pp) |
| Relative change | +0.81% (95% CI +0.41% to +1.21%) |
| p-value | 7e-5 |

- The pre-registration says ship requires the point estimate to be at the bar of 0.005. I read that bar as relative (+0.5%), and the point estimate of +0.81% clears it.
- The relative reading is an inference. The pre-registration doesn't state the unit.
- The guardrail margins can only be relative. For example, the Zero Result Rate margin is 0.03 against a baseline of 0.031. I applied the same convention to the bar.
- The CI lower bound (+0.41%) is below the bar, but the pre-registered rule only needs the point estimate to reach it.
- **If the bar were absolute (+0.5 pp), the point estimate of +0.33 pp would miss it and the call would flip to Don't ship.** The team should confirm the unit at the review.

**Guardrails.** I checked the worse-direction bound of each CI against its margin. All pass.

| Metric | Change (95% CI) | Margin | Result |
|---|---|---|---|
| Latency p95 | +0.2% (±0.5%), worst +0.7% | 2% | Pass |
| Abandonment Rate | +0.1% (±0.6%), worst +0.7% | 1% | Pass |
| Zero Result Rate | 0.0% (±1.4%) | 3% | Pass |
| Revenue per User | −0.1% (±0.7%), worst −0.8% | 1% | Pass |

Revenue is the tightest guardrail. Its worst-case bound sits close to its margin.

**Caveats (not pre-registered, so exploratory)**
1. **Clicks per User fell 1.2%** (p=0.003), and **Desktop Successful Search Rate fell 1.3%** (−0.69 pp, p=0.003).
   - Pulse reports about 66 secondary and segment metrics. At 5%, roughly three false positives are expected by chance.
   - Neither p-value survives a Bonferroni correction (threshold about 0.0008).
   - Fewer clicks alongside a higher success rate is also plausible if users need fewer clicks to succeed.
   - I'd treat both as things to watch, not as grounds to block.
   - Desktop deserves a follow-up check after launch.
2. **The segment results don't reconcile with the primary.**
   - Overall Successful Search Rate is +0.33 pp. Every pair of segments has both members below that: Mobile +0.03 and Desktop −0.69 pp, Head +0.02 and Tail −0.11, Navigational −0.29 and Informational +0.14.
   - If each pair partitions users or searches, the overall effect can't exceed both segment effects.
   - I couldn't tell from the files whether this comes from how the segment metrics are defined (different denominators or filters) or from a data problem.
   - Someone who knows the Statsig metric definitions should check this before the review. If the segments turn out to be valid partitions, the primary result needs another look.

**Recommendation:** Ship Ranker v7, conditional on two confirmations at the review: the bar is relative, and the segment inconsistency has an explanation. After launch, monitor Desktop Successful Search Rate and Clicks per User.