Decision: Ship

I wrote the full readout to `readout.md`. It rests on one assumption about units that the review needs to confirm.

**Primary metric:** Successful Search Rate rose from 41.20% to 41.53%. That is +0.33 pp, or +0.81% relative, with a 95% CI of +0.41% to +1.21% (p=7e-5). The prereg rule is that the point estimate must reach the +0.5% bar, and it does. The lower end of the CI is below the bar, so the true lift could be smaller.

**Guardrails:** All four pre-registered guardrails are within their margins at the worst end of the 95% CI.
- Latency p95 is +1.2% worse (CI +0.7% to +1.7%) against a 2% margin.
- Abandonment Rate is +0.1% worse (±0.6) against a 1% margin.
- Zero Result Rate is unchanged (±1.4) against a 3% margin.
- Revenue per User is −0.1% (worst end −0.8%) against a 1% margin.

**Assumption to confirm:** The prereg doesn't say whether the bar and margins are relative or absolute. I read them as relative, because the latency margin of 0.02 only makes sense as 2%. If the bar is meant as an absolute +0.5 pp, the result (+0.33 pp, CI upper bound +0.50 pp) fails it, and the decision flips to Don't ship.

**Flags for the review:**
- **Latency:** p95 is up about 5 ms (412 → 417 ms), a statistically certain regression. It is inside the tolerance but has little headroom, so I suggest tracking it after launch.
- **CTR:** It fell 0.71% (p=0.005). CTR was not pre-registered. Long Click Rate and Abandonment are flat, so I read this as fewer wasted clicks, but it is worth monitoring.
- **Other secondary and segment metrics:** I did not mine them for effects. With about 45 segment metrics, a stray significant one would be expected by chance.

**Setup:** The test ran 14 days (Sep 12–25) with 1.0M users per arm against a plan of 900k. The exposure balance check passed, and only `ranker_model` differed between arms. The audit log shows no mid-test changes.