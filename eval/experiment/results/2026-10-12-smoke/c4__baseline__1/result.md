Decision: Ship

I saved the readout to `readout.md`. Ranker v7 meets the pre-registered ship rule.

- **Primary metric:** Successful Search Rate is up 0.81% relative (+0.33 pp), against a pre-registered bar of +0.5% on the point estimate. The 95% CI is +0.41% to +1.21% and p is 7e-5. The CI's lower end is below the bar, but the pre-reg only requires the point estimate to reach it.
- **Guardrails:** All four are inside their pre-registered margins at the worst end of the CI: latency p95, abandonment, zero-result rate and revenue per user.
- **Validity:** The exposure-balance health check passed, with 1,000,000 users per arm. The audit log is empty, so nothing changed mid-flight. Only `ranker_model` differs between arms.
- **Assumption to confirm in the review:** I read the bar and the margins as relative changes, because absolute margins would be meaningless (for example 0.02 ms on latency). If the bar was meant as an absolute 0.5 pp, the +0.33 pp result misses it.
- **Clicks per User:** It is down 1.2% (p = 0.003). It isn't a pre-registered guardrail, but CTR and Long Click Rate don't back up the primary win, so I'd monitor it after launch.
- **Desktop Successful Search Rate:** It is down 1.3% (p = 0.003). Among about 60 segment metrics it wouldn't survive a multiple-comparison correction, and the segment baselines don't reconcile with the overall one. I'd still watch it.
- **Stale snapshot:** The Pulse snapshot is from 2026-09-25, and the experiment still shows as active. I'd refresh Pulse before the review.