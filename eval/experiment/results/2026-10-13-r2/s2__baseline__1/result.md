Decision: Ship

I wrote the readout to `readout.md`. The recommendation depends on one unit question for the review: the prereg's `bar: 0.005` has no unit. I read it as a 0.5% relative lift, the same way as the guardrail margins, and the decision flips if the team meant it as an absolute +0.005.

- **Primary metric:** Successful Search Rate rose 0.81% relative (95% CI +0.41% to +1.21%, p=7e-5). That clears the 0.5% bar on the point estimate, which is the prereg's rule (`point_at_bar`). The lower end of the CI is below the bar. The prereg doesn't require the lower end to clear it.
- **Guardrails:** All four are within their margins, even at the worst end of their CIs. Abandonment and revenue have the least headroom.
- **Test validity:**
  - The test is a clean 50/50 A/B with 1M users per arm.
  - Only `ranker_model` differs between the arms.
  - The exposure-balance check passed and the audit log is empty.
  - The 14-day test is complete, but Statsig still shows the experiment as active and the snapshot is from 9/25.
- **If the bar is absolute:** The lift is +0.0033 (CI up to +0.0050), so it falls short and the decision becomes Don't ship. Please confirm the unit in the review.
- **Flagged in the readout, not blocking:**
  - Ad Click Rate fell 2.8% (p=0.022), though revenue is flat.
  - The other click metrics don't show the Successful Search Rate lift.
  - The segment cuts are exploratory and uncorrected for multiple comparisons.