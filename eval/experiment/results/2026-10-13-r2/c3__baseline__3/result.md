Decision: Can't tell

I wrote the readout to `readout.md`. The unadjusted result looks like a ship, but the two arms already differed before launch by about the size of the observed lift. I can't separate the ranker's effect from that gap.

- **Primary metric:** Successful Search Rate is up 0.81% relative (95% CI +0.41% to +1.21%, p=7e-5). The point estimate clears the prereg bar of +0.5%, which is the stated ship rule. The CI's lower bound (+0.41%) is below the bar, though.
- **The problem:** prereg.json records a pre-launch gap of +0.71% on this same metric, with a CI that excludes zero. Pulse was pulled with CUPED off, so it isn't adjusted for that gap. Subtracting it leaves about +0.10% ± 0.57%, which fits both "no effect" and "above the bar". That difference is my rough calculation (treating the two periods as independent), not a Pulse output.
- **Guardrails:** latency, abandonment, zero-result rate and revenue per user are all within their prereg margins, even at the worst end of their CIs.
- **Corroboration:** the secondary metrics don't back up a gain. A few segment cuts are nominally significant, but nothing is corrected for multiple comparisons, so I treated them as noise.
- **Setup:** the change log is empty, the exposure-balance check passed, and sample sizes are equal (1.0M per arm). The experiment is still marked active, well past its planned 14 days. The Pulse data is from day 14, which is the planned end.

The readout recommends re-pulling Pulse with CUPED on and finding out why the arms differed at baseline. It lists which outcomes of the adjusted estimate lead to ship, don't ship or rerun.