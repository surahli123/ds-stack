Decision: Ship

I wrote the readout to `readout.md` in the work directory.

- **Primary:** Successful Search Rate rose from 0.412 to 0.4153. That is +0.81% relative (95% CI +0.41% to +1.21%, p=7e-5). The pre-registered bar is +0.5% with a "point at bar" rule, so the point estimate clears it.
- **Guardrails:** Latency p95, Abandonment Rate, Zero Result Rate and Revenue per User all stay inside their margins, including at the worst end of the CI.
- **Health:** The exposure balance check passed. Each arm has 1.0M units against 0.9M planned. The audit log is empty and sequential testing is off. The only parameter that differs between arms is `ranker_model`.

Two things to raise in the review:
- **Bar units:** I read the 0.005 bar as relative, because the guardrail margins only make sense that way. If the team meant an absolute +0.005, the point estimate (+0.0033) misses it and the decision changes. Someone should confirm what the team intended.
- **Reformulation Rate:** It is up 0.96% (p=0.018), but it isn't pre-registered and sits among about 60 uncorrected secondary and segment metrics. I flagged it for post-launch monitoring instead of treating it as harm.

I recommend shipping with a small holdout.