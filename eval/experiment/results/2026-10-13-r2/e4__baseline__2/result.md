Decision: Don't ship

I wrote the readout to `readout.md` in the working directory.

- **Primary metric:** Successful Search Rate is up 1.9% on triggered searches (+0.0078 absolute, p<0.001). The pre-registered bar is defined overall, and triggered searches carry only 20.5% of control successes. Rescaled, the lift is about +0.39% relative, with a 95% CI of roughly +0.27% to +0.51%. That is below the 0.5% bar, and the pre-registration requires the point estimate to be at the bar.
- **Units of the bar:** I read the bar as relative, which fits the pre-registration's `mass_share` framing. If it is 0.005 absolute overall, the gap is much larger and the decision is unchanged. The pre-registration authors should confirm the units.
- **Guardrails:** All four are within their margins: latency p95, abandonment, zero-result rate and revenue per user.
- **Validity:** The exposure-balance check passed, the run covered the planned 14 days, the audit log is empty, and only `ranker_model` differs between arms.
- **Secondary metrics:** Queries per User is down 1.04% (p=0.024). It is one of about 60 uncorrected metrics and cuts, so I treated it as a hypothesis, not a finding.

Extending the run won't move the point estimate. Shipping would need an explicit, documented change to the bar.