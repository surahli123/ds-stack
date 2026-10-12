Decision: Don't ship

The readout is saved at `readout.md` in the working directory. Ranker v7 meets the primary bar but breaks the Abandonment Rate guardrail from the pre-registration.

- **Primary:** Successful Search Rate rose 0.4120 → 0.4171, a gain of +0.0051 (95% CI about +0.0035 to +0.0067). The point estimate clears the 0.005 bar the pre-registration requires, but the lower end of the CI is below it.
- **Abandonment guardrail:** it rose 2.2% relative (+0.0041 absolute), with a CI of about +1.5% to +2.9%. That interval sits entirely above the 1% margin. Latency, Zero Result Rate and Revenue per User are within their margins. The Revenue CI is wide, so a loss near the margin can't be ruled out.
- **Setup:** the experiment ran the planned 14 days with 1.0M users per arm, the exposure balance check passed, and the audit log is empty.
- **Segments:** the 42 segment rows are exploratory and uncorrected for multiple comparisons. I didn't act on any of them.
- **Open question:** the pre-registration doesn't say whether the guardrail margins are relative or absolute. I read them as relative, because absolute margins make no sense for latency (0.02 ms) or Zero Result Rate (0.03 against a 0.031 rate). If the Abandonment margin was meant as an absolute 0.01, the breach disappears. Please confirm that with the pre-registration authors before the review.