Decision: Ship

I wrote the readout to `readout.md` in the working directory. It starts with the exact decision line.

- **Primary metric:** Successful Search Rate rose from 41.20% to 41.53%. That is +0.81% relative, with a 95% CI of about +0.41% to +1.21% (p = 7e-5). The prereg rule is "ship requires point at bar", and the point estimate clears the 0.005 bar. The lower CI edge is below the bar, but the prereg doesn't require it to clear.
- **Bar units:** The prereg doesn't say whether 0.005 is relative or absolute. I read it as relative, like the guardrail margins. If it were absolute (0.5pp), the +0.33pp result would miss it and the call would flip to Don't ship. Someone should confirm this in the review.
- **Guardrails:** All four are within margin. Abandonment and revenue are the tightest, with CI edges at +0.7% against a 1% margin and −0.8% against a 1% margin.
- **Validity:** The exposure health check passed, the audit log is empty, and the test ran the planned 14 days. Only `ranker_model` differs between arms.
- **Trend:** On a calendar-day basis the lift fades from +1.25% to +0.50%, which looks like novelty decay. On an exposure-day basis it is flat at about +0.8%, so I read the fade as cohort mix. I recommend a small post-launch holdout, because I can't fully rule out an external time effect.
- **Reformulation Rate:** It got worse (+1.0% relative, p = 0.013). It isn't a prereg guardrail, and it wouldn't survive a multiple-comparison correction across about 15 secondaries. It's worth watching after launch.
- **Segment tables:** Mobile and Desktop are both negative while the overall effect is positive, which can't happen if they partition the users. Either there are other platforms or the segment tables don't reconcile with the headline. None of the segments is significant. I'd check the segment pipeline before anyone reads them.