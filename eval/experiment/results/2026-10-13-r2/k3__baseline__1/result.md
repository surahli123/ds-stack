Decision: No effect found

**Ranker v7 readout: Successful Search Rate (SSR) did not move, and the +0.5 pt bar is ruled out**

**Result**
- SSR was 41.20% in control and 41.25% in test, a change of +0.049 pt (+0.12% relative). The 95% CI is −0.15 to +0.25 pt, and p = 0.62.
- The pre-registered ship rule required the point estimate to reach +0.5 pt. It came in at roughly a tenth of that.
- The CI's upper end (+0.25 pt) is also below the bar. So v7 is unlikely to deliver the lift the team planned for, and the data don't support a larger effect.
- The CI also includes zero, so we can't say v7 is better or worse than v6. Any real effect is within about ±0.25 pt.

**Guardrails.** None showed a problem. Each CI sits inside its pre-registered margin, so the guardrails are "not shown to be harmed", not "shown to be equal".

| Metric | Change (95% CI half-width) | Margin |
|---|---|---|
| Latency p95 | +0.2% (±0.5%) | 2% |
| Abandonment | +0.1% (±0.6%) | 1% |
| Zero Result Rate | 0.0% (±1.4%) | 3% |
| Revenue per User | −0.1% (±0.7%) | 1% |

**Experiment validity**
- The run lasted the planned 14 days (2026-09-12 to 09-25), with about 1.0M users per arm against 0.9M planned.
- The exposure balance check passed. The audit log is empty, so no config changes were made mid-flight.
- The only parameter that differs between arms is `ranker_model`, as intended. This is a clean 50/50 A/B test on userID.

**Secondary and segment metrics (exploratory)**
- Pulse reports about 55 secondary metrics and segment cuts with no multiplicity correction, and Bonferroni is off. A few nominal p < 0.05 results are expected by chance alone.
- The notable ones all lean slightly negative:
  - Navigational SSR: −0.39 pt, p = 0.039.
  - Mobile clicks per user: p = 0.011.
  - Head-query time to first click: p = 0.031.
  - Desktop SSR: −0.43 pt, p = 0.065.
  - Overall clicks per user: −0.028, p = 0.056.
- None of these were pre-registered, and none would survive correction. I'd treat them as hypotheses to look at if v7 is iterated on, not as findings.

**Recommendation**
- Don't launch v7 on the grounds of SSR improvement, because the bar wasn't met and can't plausibly be met with this data.
- Extending the run won't help. The CI is already tight enough (±0.2 pt) to exclude the bar.
- If the team wants v7 for other reasons, such as cost or maintainability, the guardrails show no harm. That would be a separate decision from this pre-registered one.
- A possible follow-up is to check whether v7's lower clicks per user and navigational SSR are real, before any v8 iteration.

**Caveats**
- Pulse was requested with CUPED off, so the intervals are unadjusted. CUPED would only narrow them.
- I used the single ds = 2026-09-25 snapshot and did not look at daily trends or novelty effects.
- Abandonment's pre-registered margin is a relative or absolute 1%. Either reading is cleared by a wide gap.