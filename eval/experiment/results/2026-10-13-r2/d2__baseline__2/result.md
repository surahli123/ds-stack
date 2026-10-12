Decision: Don't ship

I wrote the readout to `readout.md` in the working directory.

- **Primary metric:** Successful Search Rate fell from 41.20% to 40.94%, a change of −0.255 pp. The 95% CI is [−0.42, −0.09] pp (p = 0.0024). The pre-registered ship bar was +0.5 pp, so it is missed, and the whole CI sits below zero.
- **Guardrails:** None breached. Latency, abandonment, zero-result rate and revenue per user all have CIs well inside their margins. Revenue per User is the closest, with a worst case of −0.8% against a 1% margin.
- **Secondary and segment metrics:** Only 2 of 56 are significant, which is about what chance produces with no multiple-comparison correction. The Successful Search Rate segment cuts are non-significant and mixed in direction, so they don't support a segment-targeted launch.
- **Setup:** The audit log is empty, so the config didn't change during the run. Only `ranker_model` differs between arms. Exposures are balanced, with 1.0M users per arm against 900k planned.
- **Caveats:** The Pulse results are dated 2026-09-25, one day before the planned end, and the experiment still shows as `active`. I didn't re-pull results, and one more day wouldn't change the conclusion.

The readout recommends keeping v6 and closing the experiment. Any follow-up on why Successful Search Rate dropped would be a new pre-registered experiment.