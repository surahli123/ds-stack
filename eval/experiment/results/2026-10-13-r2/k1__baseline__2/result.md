Decision: Can't tell

**Why: this Pulse is an early peek, not the pre-registered readout.**
- The Pulse snapshot is dated 2026-09-15. The experiment started 2026-09-12 and was planned for 14 days, so this is about day 3–4.
- It has about 260k units per arm against 900k planned, roughly 29% of the sample.
- The experiment config shows `sequentialTesting: false`. The p-values and CIs are fixed-horizon, and they aren't valid for a ship decision taken from an interim look.
- The config still shows the experiment as `active` today (2026-10-12), which is well past the planned end of 2026-09-26. The Pulse in hand is stale. I don't have a Pulse for the full run.

**Primary metric: Successful Search Rate (pre-registered bar +0.005 absolute, ship if the point estimate reaches it)**

| | Control | Test | Absolute lift | 95% CI | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4179 | +0.00585 (+1.42% relative) | [+0.0013, +0.0104] | 0.011 |

- The point estimate clears the bar, but the CI lower bound is far below it. The data are consistent with a lift anywhere from +0.1pp to +1.0pp.
- At this sample size, the point estimate is not trustworthy relative to the bar. Early estimates are noisy and tend to overstate effects.

**Guardrails (pre-registered margins, treated as relative; the margin units aren't specified in the prereg)**

| Guardrail | Change | CI half-width | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.2% | ±0.5% | 2% | Inside margin |
| Abandonment Rate | +0.1% | ±0.6% | 1% | Inside margin |
| Zero Result Rate | 0.0% | ±1.4% | 3% | Inside margin |
| Revenue per User | −0.1% | ±0.7% | 1% | Inside margin |

- All four have the worst end of their CI inside the margin. That is encouraging but also only interim, and Revenue has the least headroom.

**Health and integrity**
- Exposure balance check passed. Units are 261k test and 260k control, so there is no sign of a sample-ratio problem.
- The audit log is empty, so there were no mid-flight config changes.
- The test and control arms differ only in `ranker_model`, which matches the prereg's `intended_params`. `snippet_length` is identical in both arms.

**Secondary and segment metrics (exploratory only)**
- Of about 60 metrics and segment cuts, only two have p < 0.05: CTR (p = 0.003, up) and Desktop Time to First Click (p = 0.04996, worse). With that many looks and no multiplicity correction, a couple of crossings are expected by chance.
- Desktop (−0.27pp), Tail queries (−0.18pp) and Navigational queries (−0.30pp) all lean negative on Successful Search Rate. None is significant, and the Pulse gives no interaction test.
- I would not read the segment differences as real. They are worth checking in the full-data run.

**Next step before the review**
1. Re-pull Pulse with the same settings (`cuped: false`, 95% confidence) once the full planned window is in, and confirm unit counts are close to 900k per arm.
2. Apply the pre-registered rule to that result. Ship if the Successful Search Rate point estimate is at least +0.005 and no guardrail breaches its margin.
3. If the experiment was meant to stop on 2026-09-26, ask why it is still active and whether a final Pulse exists.

I'd advise against shipping or killing on the Sep 15 numbers. The early signal is positive and nothing is alarming.