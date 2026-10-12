Decision: Don't ship

I wrote the readout to `readout.md`. Ranker v7 lowered Successful Search Rate, the pre-registered primary metric, instead of raising it.

- **Primary metric:** it went from 41.20% to 40.94%, a change of -0.255 pp (95% CI -0.42 to -0.09, p=0.0024). The pre-registered bar to ship was +0.5 pp. The CI sits entirely below zero, so this is a measured regression, not just a miss.
- **Guardrails:** none was breached. At the worst end of its CI, each metric stayed inside its pre-registered margin. This doesn't change the decision, because the primary metric failed.
- **Secondary metrics:** none is significant, and nothing offsets the primary drop.
- **Validity:**
  - Exposures were balanced.
  - The run covers the full 14 days (Sep 12 to Sep 25), with 1.0M units per arm against 0.9M planned.
  - The only parameter that differs between arms is `ranker_model`, as intended, and the audit log shows no changes.
- **Limits:** I only had the aggregate Pulse output, so I didn't check novelty effects or segment differences.