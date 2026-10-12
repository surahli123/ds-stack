Decision: Ship

**Ranker v7 readout (Pulse snapshot ds 2026-09-25, no CUPED, 95% CIs)**

**Result**
- Ranker v7 raised Successful Search Rate, the only pre-registered primary metric. Control was 41.20% and Test 41.53%, a lift of +0.334 points (+0.81% relative).
- The 95% CI on the lift is +0.17 to +0.50 points (+0.4% relative half-width), with p = 7e-05.
- The pre-registered bar is 0.005 and "point at bar", so the point estimate must reach it. I read the bar as relative (0.5%), and +0.81% clears it.
- **Assumption to confirm:** prereg.json gives no unit for the bar. If it meant 0.005 absolute (0.5 points), the point estimate of +0.33 points would miss it, and the call would change to Don't ship or Escalate. I read it as relative because the guardrail margins only make sense as relative: a 0.03 absolute margin on a Zero Result Rate of 0.031 would be meaningless. Please confirm this at the review.

**Guardrails**
Each guardrail passes if the worst end of its CI stays inside the margin.

| Metric | Change | Worst end of CI | Margin | Result |
|---|---|---|---|---|
| Latency p95 | +0.2% (412.8 ms vs 412.0 ms) | +0.7% | 2% | Pass |
| Abandonment Rate | +0.1% | +0.7% | 1% | Pass |
| Zero Result Rate | 0.0% | +1.4% | 3% | Pass |
| Revenue per User | −0.1% | −0.8% | −1% | Pass (narrow) |

Revenue per User has the least headroom. The CI is wide enough that a loss of up to 0.8% is not ruled out, against a 1% tolerance.

**Experiment validity**
- It is a clean two-arm A/B test, and the exposure balance health check passed.
- Test and control each had 1.0M users, against 0.9M planned.
- The snapshot covers the full 14-day window (09-12 to 09-26). The audit log is empty, so no config changes were made mid-test.
- Sequential testing was off. The result is a single fixed-horizon read at the planned end, so there is no peeking problem.
- The Test and Control groups differ only in `ranker_model`. `snippet_length` is the same in both, so the lift is not confounded by a second change.

**Caveats (not blockers)**
- **Ad Click Rate:** it fell 2.8% relative (p = 0.022). It is not pre-registered and is one of about 60 metrics shown, so it could be chance. Revenue per User, the metric it would feed into, is flat. Worth watching after launch.
- **Subgroup cuts:** several of these look nominally significant, for example Desktop Time to First Click, Informational CTR and Clicks per User. They are exploratory and uncorrected for multiple comparisons (Bonferroni was off), so I would not act on them.
- **Secondary metrics:** none moved in a direction that contradicts the primary result. Queries per User is −0.8% (p = 0.08), not significant.
- **Subgroup lifts:** Desktop (+0.40 points) and Mobile (+0.03 points) differ, but the CIs overlap heavily, so there is no evidence of a segment-specific effect.

**Recommendation:** Ship, provided the review confirms the bar is relative. Monitor Revenue per User and Ad Click Rate after rollout.