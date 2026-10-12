Decision: Can't tell

**Ranker v7 readout (Statsig Pulse, 2026-09-12 to 09-25, 14 days, 1.0M users per arm)**

**Why "Can't tell"**
- The headline result clears the pre-registered bar. But the pre-registration shows the two arms already differed by about the same amount before launch.
- That pre-launch gap explains most of the lift, so the data can't separate the ranker's effect from a baseline gap between arms.

**Primary metric: Successful Search Rate**

| | Value |
|---|---|
| Control | 41.20% |
| Test | 41.53% |
| Raw lift | +0.81% relative (+0.33 pp), 95% CI about [+0.41%, +1.21%], p = 7e-5 |
| Pre-registered bar | +0.5% relative |

- **Raw result:** The point estimate is above the bar, which is what the pre-registration required to ship. The CI lower bound (+0.41%) is below the bar.
- **Unit of the bar:** I read the bar as relative, because the pre-period and guardrail margins are relative. If it is absolute (0.5 pp), the result fails it.
- **Pre-launch gap:** The pre-period for the same metric shows test already ahead of control by +0.71% relative, CI [+0.31%, +1.11%]. That gap is statistically significant, so the arms were not equivalent before the ranker was live.
- **Adjusted for the gap:** Subtracting the pre-period difference leaves about +0.10%, CI roughly [−0.47%, +0.67%]. This is my own rough calculation. It assumes the pre-period gap would have persisted unchanged, and it treats the pre-period CI as the same width as the post-period one.
- **What that interval means:** It includes zero, and it also includes the +0.5% bar, so it supports neither a real effect nor a null result.
- **Pulse settings:** The pulse was pulled with CUPED off, so it does not correct for this gap.

**Guardrails**

All four are inside the pre-registered margins, even at the worst end of their CIs.

| Metric | Change (relative) | 95% CI half-width | Margin |
|---|---|---|---|
| Latency p95 | +0.2% (worse) | ±0.5% | 2% |
| Abandonment Rate | +0.1% (worse) | ±0.6% | 1% |
| Zero Result Rate | 0.0% | ±1.4% | 3% |
| Revenue per User | −0.1% (worse) | ±0.7% | 1% |

- **Revenue per User:** Its worst-case bound is −0.8%, close to the 1% margin but inside it.
- **Latency p95:** Its worst-case bound is +0.7%, inside the 2% margin.
- **Guardrails don't resolve the gap:** They say v7 probably does no harm. They don't say it helps.

**Other checks**
- **Exposure balance:** The health check passed, so the pre-period gap is not a sample-ratio problem.
- **Config:** The audit log is empty, so nothing changed mid-test. The experiment ran 14 days as planned. Only the intended parameter (`ranker_model`) differs between arms, and sample size was above the 900k plan.
- **Secondary metrics:** None moved meaningfully, and no secondary metric (including segment slices) was significant after correcting for the number tested.
  - Of the ~60 secondary metrics and slices, the 3 nominal hits (Desktop and Tail time-to-first-click, Tail clicks per user) are what chance alone would produce.
  - Mobile Successful Search Rate is −0.82% (p = 0.11), a negative direction worth watching but not significant.

**Recommendation for the review**
1. Don't ship on the raw number. Don't kill it either, since the guardrails are clean and the adjusted estimate is still compatible with the bar.
2. Re-pull the pulse with CUPED on, using the pre-period covariate. This is a quick check and may settle the question tomorrow.
3. Find out why test led before launch. Likely causes are a bucketing or salt issue, or a layer overlap with `search_ranking`. If the arms are not equivalent, the randomization needs fixing before any rerun.
4. If CUPED shows the adjusted lift is about +0.1%, treat v7 as not meeting the bar and rerun with clean randomization.
5. If the adjusted lower bound clears the bar, it's a ship.