Decision: Ship

**Ranker v7 readout (Pulse snapshot 2026-09-25, day 14 of 14, 1.0M users per arm)**

**Primary metric: Successful Search Rate**
- It rose from 41.20% to 41.53%. That is +0.33 pp, or +0.81% relative (95% CI +0.41% to +1.21%, p = 7e-5).
- The pre-registered bar is +0.005. The daily files and Pulse's `percentChange` are in relative units, so I read the bar as +0.5% relative. The point estimate of +0.81% clears it, and the prereg says ship requires `point_at_bar`.
- If the bar was meant as +0.5 pp absolute, it would fail (+0.33 pp). The prereg doesn't state the unit, so the team should confirm the reading. I think relative is right.
- The CI lower bound (+0.41%) is below the bar. The prereg doesn't require the lower bound to clear it, but the true effect could be somewhat under 0.5%.

**Guardrails**
I read each margin as relative, the same unit as the bar. All four pass: the worst plausible end of each CI stays inside its margin.

| Guardrail | Change (95% CI) | Margin |
|---|---|---|
| Latency p95 | +0.2% (±0.5%) | 2% |
| Abandonment Rate | +0.1% (±0.6%) | 1% |
| Zero Result Rate | 0.0% (±1.4%) | 3% |
| Revenue per User | −0.1% (±0.7%) | 1% |

Revenue has the least headroom. Its CI reaches about −0.8% against a −1% margin.

**Validity**
- Exposures are balanced: 1M users per arm, and the health check passed.
- The run covered the full planned 14 days.
- The audit log is empty, so there were no mid-test config changes.
- The only parameter that differs between arms is `ranker_model`, as intended. `snippet_length` is the same in both.
- The unadjusted analysis and the 95% interval match the prereg.
- Allocation was 1M per arm against the 900k planned.

**Durability**
- By calendar day, the lift fades from +1.25% on day 1 to +0.50% on day 14. The last three days' CIs include 0.
- By days since exposure, the effect is flat at about +0.8% on days 1–12. Each user's lift doesn't decay, so this doesn't look like a novelty effect.
- I can't fully reconcile the two views. If the per-user effect is constant, the calendar-day effect should be too. The decline may come from a change in which cohorts contribute later in the test. Please watch the metric after launch.

**Other observations (secondary, not pre-registered, no multiplicity correction)**
- Of 56 secondary metrics, 3 have p < 0.05. That is about what chance alone would give (56 × 0.05 ≈ 3), so I'm not treating them as findings.
- Reformulation Rate got worse: +1.0% relative (CI ±0.8%), p = 0.013. This is the one to watch.
- Time to First Click improved, by 1.1%.
- Mobile and Desktop Successful Search Rate are both slightly negative (−0.8% and −0.7%, neither significant). That is hard to square with an overall +0.81% if the two segments cover all users. I suspect the segments overlap or use different denominators, but I haven't confirmed it. Someone should check the segment definitions before launch.

**Recommendation:** Ship. The pre-registered primary clears its bar on the point estimate and every guardrail holds. After launch, monitor Reformulation Rate, Revenue per User and the calendar-day trend, and keep a holdback if one is cheap.