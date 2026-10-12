Decision: Don't ship

I wrote the readout to `readout.md` in the working directory. In short, Ranker v7 does improve the primary metric, but by far less than the pre-registered bar.

- **Primary metric:** Successful Search Rate rose by +0.00128 (95% CI +0.00054 to +0.00202, p=0.0007). The bar was +0.005. Even the top of the CI is below it, so this isn't an underpowered near-miss. It misses whether the bar is read as absolute or as 0.5% relative, since the observed lift is +0.31% relative.
- **Guardrails:** Latency p95, Abandonment Rate, Zero Result Rate and Revenue per User all stay inside their margins. Abandonment and Revenue have the thinnest room: the worst case is 0.7% and 0.8% against a 1% margin.
- **Validity:** The test is a standard 50/50 A/B test and ran the planned 14 days. The exposure-balance check passed, and the audit log is empty, so nothing changed mid-test. The 30-odd secondary metrics show nothing significant, and I didn't treat them as evidence either way.
- **Recommendation:** If the team still wants to ship a gain of about 0.1 percentage points, the review should explicitly change the bar and record that. It shouldn't be read as a pass.

The pre-registration doesn't say whether the bar is absolute or relative. The conclusion holds either way.