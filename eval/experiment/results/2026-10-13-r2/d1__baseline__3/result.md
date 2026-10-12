Decision: Don't ship

I wrote the readout to `readout.md` in the working directory. Ranker v7 improves Successful Search Rate, but it breaks the latency guardrail from the pre-registration.

- **Latency:** p95 latency is up 3.1% (412 → 424.8 ms). The 95% CI is +2.5% to +3.7%, and the whole interval is past the pre-registered 2% tolerance. This alone blocks the launch.
- **Primary metric:** Successful Search Rate is up +0.00334 absolute (+0.81% relative, 95% CI +0.0017 to +0.0050, p = 7e-5). Whether that meets the 0.005 bar depends on units the pre-registration doesn't state. If the bar is relative (0.5%), the point estimate clears it. If it's absolute, the point estimate misses. The decision is the same either way, but someone should confirm the intended units.
- **Other guardrails:** Abandonment Rate, Zero Result Rate and Revenue per User are all within their margins.
- **Setup:** The test ran 14 days (2026-09-12 to 09-26) on a 50/50 split with about 1M users per arm, and the exposure-balance check passed. The audit log is empty, so there were no mid-test config changes.
- **Segment cuts:** I treated these as exploratory. They are many unadjusted tests, so a few nominal hits are expected by chance.

My recommendation is to fix the roughly 13 ms latency regression and re-test. The alternative is a documented waiver from the owners, who would be weighing about +0.3 points of search success against +3% latency. I couldn't tell from the aggregate data whether the latency regression comes from the model itself or from infrastructure noise.