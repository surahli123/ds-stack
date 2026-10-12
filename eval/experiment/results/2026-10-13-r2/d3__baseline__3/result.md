Decision: Don't ship

I wrote the readout to `readout.md`. Ranker v7 hits the primary bar but fails the Abandonment Rate guardrail.

- **Primary (Successful Search Rate):** the lift is +0.00511 (95% CI +0.0035 to +0.0068), against a pre-registered bar of +0.005. The point estimate clears the bar by 0.0001, which counts as a pass under the prereg's "point at bar" rule. The CI's lower end is below the bar.
- **Abandonment Rate:** it rose 2.2% relative (CI +1.5% to +2.9%), against a 1% margin. The whole interval is past the margin, so the guardrail is breached.
- **Other guardrails:** Latency p95, Zero Result Rate and Revenue per User are all inside their margins. Revenue's worst CI end is -0.8% against a 1% margin.
- **Setup:** the test ran the planned 14 days (2026-09-12 to 2026-09-25) with 1M users per arm. The exposure-balance check passed, only `ranker_model` differs between arms, and the audit log is empty.
- **Segment cuts:** I treated these as exploratory and drew no conclusions. About 60 were run, so a few nominal p<0.05 results are expected by chance.

The call depends on how I read the Abandonment margin. I treated it as relative, like the latency, revenue and zero-result margins. If the team meant 0.01 absolute, the upper CI bound of +0.0054 would sit inside it and the call would become Ship. The review should confirm which they meant.