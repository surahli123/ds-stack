Decision: No effect found

I wrote the readout to `readout.md` in the working directory. Ranker v7 didn't move the pre-registered primary metric, and the test was large enough to rule out the lift the team needed.

- **Primary (Successful Search Rate):** The lift was +0.00025 (+0.06% relative), with a 95% CI of [−0.00099, +0.00148] and p=0.70. The ship bar was +0.005, so even the CI's upper end falls well short of it.
- **Guardrails:** None were breached. Latency p95, Abandonment, Zero Result Rate and Revenue per User all sit well inside their pre-registered margins.
- **Validity:** Exposures are balanced at 1M per arm, and the data cover the full 14 planned days. The arms differ only in `ranker_model`, and the audit log is empty. I couldn't check for novelty or primacy effects, because Pulse gives only a single pooled readout.
- **Tail queries:** Tail-query Successful Search Rate is +1.46pp (p<0.001). That's a post-hoc segment among about 60 non-pre-registered metrics, and it sits oddly with the flat overall result. It isn't a basis for shipping, but it's worth a new pre-registered test targeted at tail queries.

My recommendation is not to ship on the primary metric.