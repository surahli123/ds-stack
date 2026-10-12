Decision: Don't ship

I wrote the readout to `readout.md`. It rests on one assumption about the bar's unit, which the pre-registration doesn't state.

- **Primary metric:** Successful Search Rate rose by +0.00334 (95% CI +0.0017 to +0.0050, p=7e-5). That is real, but it falls short of the pre-registered bar of 0.005. The pre-registration requires the point estimate to reach the bar to ship.
- **Guardrails:** All four (latency, abandonment, zero-result rate, revenue per user) have confidence intervals inside their margins.
- **Validity:** The test is a randomized 50/50 A/B. Exposures are balanced, only `ranker_model` differs between arms, the audit log is empty, and the run lasted the planned 14 days. The pre-registration calls the design a "holdout", but I treated it as a standard A/B.
- **Secondary and segment metrics:** A few of the roughly 70 cross p<0.05, with mixed signs and no multiplicity correction. I treated them as exploratory.
- **The unit of the bar:** I read 0.005 as an absolute difference, the same scale as the metric. If it was meant as a relative 0.5%, the observed +0.81% clears it and the decision becomes Ship. The readout asks the pre-registration authors to confirm this before the meeting.