Decision: Ship

I wrote the readout to `readout.md`. It meets the pre-registered ship rule, provided the primary bar is relative, which I'm inferring and the review should confirm.

- **Primary:** Successful Search Rate rose from 0.4120 to 0.4153, a +0.81% relative lift (95% CI about +0.41% to +1.21%, p=7e-5). The prereg rule asks only for the point estimate to clear the bar, and +0.81% clears 0.5%. The CI's lower bound is below 0.5%, so the true lift could be smaller.
- **The bar's unit:** I read the bar of 0.005 as relative because the guardrail margins can only be relative. If it was meant as absolute, the +0.0033 change misses it and the call becomes Don't ship.
- **Guardrails:** all four are inside their margins. Latency p95 is the tight one. It is up 1.2% (CI up to +1.7%, margin 2%), and that regression is statistically significant.
- **Validity:** the test ran its full 14 days, with 1M users per arm against 900k planned. The balance health check passed and the audit log shows no mid-flight changes.
- **CTR:** it fell 0.71% (p=0.005). It wasn't a pre-registered guardrail, but I flagged it for a follow-up look.
- **Segment cuts:** I wouldn't act on the segment cuts. There are dozens of uncorrected comparisons, and none shows a significant change in the primary metric.