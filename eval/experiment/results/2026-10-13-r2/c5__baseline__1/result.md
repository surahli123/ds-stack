Decision: Ship

I've also saved the full readout as `readout.md`. The decision depends on one assumption about the pre-registration (below).

**Primary metric (Successful Search Rate):**
- It rose from 41.20% to 41.53%, which is +0.33 percentage points or +0.81% relative (95% CI +0.41% to +1.21%, p=7e-5).
- The pre-registration requires the point estimate to reach the bar of 0.005, and +0.81% is above 0.5%.

**Assumption to confirm:** the pre-registration doesn't give units for the bar. I read it as relative (0.5%), the same way as the guardrail margins. If it meant an absolute 0.5 percentage points, the +0.33 point lift misses the bar and the decision becomes Don't ship. The CI's lower bound (+0.41%) is also below 0.5%, but the pre-registered rule only requires the point estimate to clear the bar.

**Guardrails:** all four are within their margins, using the worse end of each 95% CI.

| Metric | Worst case | Margin |
|---|---|---|
| Latency p95 | +0.7% | 2% |
| Abandonment Rate | +0.7% | 1% |
| Zero Result Rate | +1.4% | 3% |
| Revenue per User | −0.8% | 1% |

Abandonment and Revenue per User have the least headroom, so watch them after launch.

**Other things the review should know:**
- Allocation was cut from 20% to 10% on 2026-09-16, partway through the run. The arms stayed equal at 1M users each and the exposure balance check passed, so I see no bias. A look at the daily lift before and after that date would confirm it.
- The Pulse results are dated 2026-09-25, the end of the planned 14 days, but the experiment still shows as active today.
- About 50 secondary and segment metrics were not corrected for multiple comparisons, and none is significant at 5%.