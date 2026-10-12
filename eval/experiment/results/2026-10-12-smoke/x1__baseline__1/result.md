Decision: Don't ship

I saved the full readout as `readout.md`.

**Primary metric:** Successful Search Rate rose from 0.4120 to 0.4153. That is +0.0033 absolute, with a 95% CI of [+0.0017, +0.0050] and p = 7e-5. The lift is real, but the pre-registered rule requires a point estimate of at least +0.005. The result reaches about two-thirds of that, and the top of the CI sits just under the bar.

**Guardrails:** All four pass, judged on the worst end of each CI.

| Guardrail | Observed change | Worst end of CI | Pre-registered margin |
|---|---|---|---|
| Latency p95 | +0.2% | +0.7% | 2% |
| Abandonment Rate | +0.1% | +0.7% | 1% |
| Zero Result Rate | 0.0% | +1.4% | 3% |
| Revenue per User | −0.1% | −0.8% | 1% |

I read the Abandonment and Zero Result margins as relative. They also pass if read as absolute.

**Secondary and segment metrics:** Pagination Rate is worse (p = 0.03) and Navigational Long Click Rate is better (p = 0.049). With about 70 uncorrected metrics, I treat both as noise, not evidence.

**Validity:**
- The exposure-balance health check passed.
- There are 1M users per arm, against 900k planned.
- The audit log is empty, so nothing changed during the run.

**Design mismatch:** The pre-registration says "interleaving", but the Statsig config is a standard user-level A/B test. The Pulse numbers are valid for an A/B test. The team should confirm that the +0.005 bar was meant for this absolute scale.

If the review wants to ship a +0.33 pt gain anyway, they should reopen the bar explicitly.