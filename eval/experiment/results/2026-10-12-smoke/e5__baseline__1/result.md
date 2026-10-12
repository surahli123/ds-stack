Decision: Don't ship

I wrote the readout to `readout.md`. The pre-registration says to ship only if both primary metrics reach +0.5 points on the point estimate. Neither does.

- **Successful Search Rate:** up 0.0033 (95% CI +0.0017 to +0.0050, p=7e-5). The lift is real but about two-thirds of the +0.005 bar.
- **Long Click Rate:** up 0.0003 (CI −0.0011 to +0.0016, p=0.70). This is flat, and the CI rules out the bar, so the miss on this metric alone blocks shipping.
- **Guardrails:** all four pass (latency p95, abandonment, zero-result rate, revenue per user), assuming the margins are relative. Revenue is the closest, with a worst case of −0.8% against a 1% margin.
- **Test health:** the test ran its full 14 days, with 1M users per arm against 900k planned. The exposure-balance check passed and the audit log is empty.
- **Secondary and segment metrics:** about 70 were reported with no multiplicity correction. The few that reach p<0.05 look like chance, and I did not use them in the decision.
- **Config mismatch:** the Statsig config lists only Successful Search Rate as a primary, while the pre-registration also requires Long Click Rate. I judged against the pre-registration.

The result is not "no effect", because Successful Search Rate improved modestly with no guardrail harm. If the team still wants v7, it should iterate on the model or make a new pre-registered decision, not relax the bar after seeing these results. Running longer is unlikely to change the answer.