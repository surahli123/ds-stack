Decision: Don't ship

I wrote the readout to `readout.md` in the working directory. Ranker v7 gives a real but small lift in Successful Search Rate, well short of the pre-registered ship bar.

- **Primary metric:** Successful Search Rate went from 0.4120 to 0.4133. That is +0.00128 absolute (+0.31% relative), with a 95% CI of [+0.00054, +0.00202] and p=0.0007. The pre-registered bar is +0.005, so the point estimate is about a quarter of it.
- **Bar excluded:** The upper end of the CI is also below the bar. Extending the run would not change the conclusion. If the bar was meant as relative (0.5%), the result still falls short.
- **Guardrails:** All four pass. Revenue per User is closest to its margin: the worst case in the CI is about −0.8% against a 1% margin.
- **Validity:** The 50/50 split is balanced and the health check passed. The run has 1.0M users per arm against 900k planned, covers the full 14 days, and the audit log is empty.
- **Exploratory segments:** Of the roughly 50 secondary and segment metrics, only CTR on navigational queries is nominally significant (p=0.023). With that many uncorrected tests, a couple of chance hits are expected, so I treated it as a hypothesis to check, not a finding.

The readout says v7 is safe and slightly positive. Shipping it anyway would be a deliberate exception to the pre-registered bar. This test does not support it.