Decision: No effect found

I wrote the readout to `readout.md`. Ranker v7 did not improve Successful Search Rate, and the data rule out the lift the pre-registration required, so it doesn't meet the ship bar.

- **Primary metric:** Successful Search Rate went from 0.4120 to 0.4118, a difference of −0.0002 with a 95% CI of [−0.0014, +0.0010] (p=0.74). The bar was +0.005. I read the bar as absolute because the prereg doesn't say, and a relative reading gives the same conclusion.
- **Validity:** The test ran its full 14 days (2026-09-12 to 2026-09-25) with 1.0M users per arm against 900k planned. The exposure balance check passed, the audit log shows no changes, and `ranker_model` was the only parameter that differed.
- **Guardrails:** Latency p95, Abandonment Rate, Zero Result Rate and Revenue per User all stay within their pre-registered margins. Revenue has the least room: its CI lower bound is −0.8% against a 1% margin.
- **Secondary metrics:** Two of 56 were significant at p<0.05, which is about what chance would give with no multiplicity correction. They were Queries per User (+1.9%) and Ad Click Rate (−1.5%), and neither was pre-registered. The readout treats both as hypotheses to follow up in a new test.

I chose "No effect found" over "Don't ship" because the result is a well-powered null and not evidence of harm. The recommendation in the readout is still not to launch on this evidence.