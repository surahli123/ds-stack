Decision: Escalate

I wrote the readout to `readout.md` in the working directory. It starts with the exact decision line.

- **Primary (Successful Search Rate):** Up 0.81% relative (95% CI about +0.41% to +1.21%, p=7e-5). That is above the pre-registered +0.5% bar, and the rule is point estimate at the bar, so the primary criterion is met.
- **Abandonment guardrail:** Not cleared. It rose 0.6% relative (±1.0%, p=0.24), so the CI reaches +1.6% against a 1% margin. The data can't rule out harm or confirm safety.
- **Other guardrails:** Latency p95, Zero Result Rate and Revenue per User are all within their margins.
- **Setup:** I found no problems. It's a clean 50/50 test on userID, the exposure balance health check passed, and the audit log is empty. The snapshot is day 14 of 14, with 1.0M users per arm against 900k planned.
- **Assumption to confirm:** I read the prereg `bar` and `margin` as relative changes, because the guardrail margins only make sense that way. If the bar is actually an absolute +0.5pp, v7 misses it (+0.33pp). The prereg author should confirm the unit.

The readout recommends that the launch owners decide whether a possible abandonment increase of up to about 1.6% is acceptable for the gain. If they ship, it suggests a staged rollout with abandonment monitored against the 1% margin.