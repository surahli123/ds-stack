Decision: Ship

# Ranker v7 – launch readout

**Result.** Successful Search Rate (the single pre-registered primary): control 41.20% → test 41.53%, +0.33 pp absolute, **+0.81% relative** (95% CI +0.41% to +1.21%, p = 7e-5). n = 1.0M users/arm (plan 900k), full 14 days, fixed-horizon, no CUPED, balanced exposures (health check passed).

**Pre-registered rule.** Ship requires the point estimate to be at or above the 0.5% bar. +0.81% clears it. The lower CI bound (+0.41%) is below the bar. The rule asks for the point estimate, not the bound, so this is a pass. It does mean the true lift could be a bit under the bar. I read the bar as relative, since the guardrail margins and the daily files are relative. A relative bar is the only reading that makes sense for the Zero Result Rate margin. If the team meant 0.005 absolute (0.5 pp), the result would miss it (0.33 pp). Please confirm this at the review.

**Guardrails** (relative change, pre-registered margins; all within margin, so none fails):
| Metric | Change (95% CI) | Margin |
|---|---|---|
| Latency p95 | +0.2% (±0.5%) | 2% |
| Abandonment Rate | +0.1% (±0.6%) | 1% |
| Zero Result Rate | 0.0% (±1.4%) | 3% |
| Revenue per User | −0.1% (±0.7%) | 1% |

The Zero Result Rate CI (±1.4%) is within the 3% margin. Revenue's worst case, about −0.8%, is also inside the margin.

**Durability / novelty.** By calendar day the lift declines from +1.25% (day 1) to +0.50% (day 14), and the day-14 CI includes 0. By days-since-exposure the lift is flat at about +0.8% on every day (days 1–12, each CI above 0). A flat exposure-day curve argues against a novelty effect: users do not lose the benefit as they stay exposed. I weight it over the calendar view. The calendar decline is probably cohort mix or time effects.

Caveat: the two views disagree on day 1. On calendar day 1 every user is on their first exposure day, so both views should show the same number. They show +1.25% and +0.82%. I could not resolve this from the files, so the data pipeline should be checked. If the calendar trend is real, the steady-state lift could be near or just under the bar. Recommend a post-launch holdback or monitoring of the calendar-day trend.

**Secondary and segment metrics** (56 in Pulse, uncorrected, exploratory only):
- Reformulation Rate is worse: +1.0% relative, p = 0.013 (lower is better). Time to First Click is better: −1.1%, p = 0.029. Neither survives a multiple-comparison correction across 56 metrics. Reformulation is not a pre-registered guardrail. I'd keep an eye on it.
- Successful Search Rate is negative in both Mobile (−0.34 pp, p = 0.058) and Desktop (−0.23 pp, p = 0.078), while the overall result is +0.33 pp. If those two segments partition users, that is not arithmetically possible. The segments are probably defined differently (per-search vs per-user, or overlapping), or there is a mix shift. Neither is significant and neither was pre-registered. I did not treat them as evidence against shipping, but the segment definitions should be checked before anyone cites them.
- Config check: the only intended parameter difference is `ranker_model` (v6 → v7); `snippet_length` is identical in both arms. The audit log is empty, so there were no mid-test changes.

**Recommendation.** Ship, on the pre-registered criteria. Conditions: confirm the bar is relative, and check the day-1 calendar vs exposure-day discrepancy and the segment definitions.
