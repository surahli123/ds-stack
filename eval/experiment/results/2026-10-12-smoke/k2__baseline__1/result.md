Decision: Don't ship

**Ranker v7 raises Successful Search Rate, but not by enough to meet the pre-registered bar, and the effect is shrinking.**

**Primary metric** (Successful Search Rate, 14 days, 1.0M users per arm, no CUPED, 95% CI)
- Control is 41.20% and test is 41.53%, a lift of +0.33pp (+0.81% relative).
- The CI is +0.17pp to +0.50pp (p = 7e-5), so the lift is real.
- The pre-registration requires the point estimate to reach the 0.005 bar. The prereg doesn't say whether 0.005 is absolute or relative.
  - Read as absolute (0.5pp), the point estimate of 0.33pp misses the bar. The CI upper end just touches it.
  - Read as relative (0.5%), the pooled +0.81% clears it. As explained below, I don't think the pooled number is the right one to judge.

**The effect fades over time** (`daily_by_exposure_day.json`)
- The daily relative lift falls steadily from +1.5% on day 1 to +0.4% on day 12.
- The day-12 CI is −0.2% to +1.0%, so it includes zero. Days 13–14 aren't in the file.
- This looks like a novelty effect. The pooled +0.81% is an average over a decaying effect and overstates where it is heading.
- The recent daily lift is below even the relative reading of the bar, so the conclusion is the same under either reading.

**Guardrails** (all pass; every CI sits well inside the margin)

| Metric | Change | Margin |
|---|---|---|
| Latency p95 | +0.2% ± 0.5% | 2% |
| Abandonment Rate | +0.1% ± 0.6% | 1% |
| Zero Result Rate | 0.0% ± 1.4% | 3% |
| Revenue per User | −0.1% ± 0.7% | 1% |

I read each margin as a relative change. I'm not certain the prereg meant that.

**Health and setup**
- Exposure balance passed. The test ran its planned 14 days (Sep 12–25). There is no sequential testing, and the audit log shows no mid-flight changes.
- The only parameter changed was `ranker_model`, as intended.

**Secondary and segment metrics**
- None of these were pre-registered, and Bonferroni correction is off, so I don't draw conclusions from them.
- About 60 segment cuts were tested, so a few "significant" results are expected by chance. Examples are CTR for head and tail queries and Clicks per User for tail queries (p = 0.004).
- Mobile and desktop point in opposite directions (+0.26pp and −0.24pp), but neither is significant.

**Recommendation**
- Don't ship on this evidence. The pre-registered ship rule isn't met, and the lift appears to be decaying toward a value that is small or zero.
- If the team still wants v7, run a longer holdout or re-run, and judge it on the steady-state effect from later exposure days. Going forward, the prereg should state whether the bar is absolute or relative.