Decision: Don't ship

I also saved this readout as `readout.md` in the working directory.

**Primary metric.** Successful Search Rate rose by +0.0033 (+0.33 pp, +0.81% relative). The 95% CI is [+0.0017, +0.0050], p = 7e-5. The lift is real, but the pre-registered ship rule requires the point estimate to reach +0.005. It doesn't, and even the CI's upper bound (+0.00499) falls just under the bar. The sample is 1M users per arm over the full 14 days, with a single look.

**Guardrails.** None is breached. The worst-case bounds are latency +0.7% against a 2% margin, abandonment about +0.7% against 1%, and zero-result rate about +1.4% against 3%. Revenue per User is the tight one: its worst case is −0.8% against a 1% margin. I read the margins as relative, because a 0.02 margin on a latency in milliseconds only makes sense that way.

**Secondary and segment metrics.** None is significant, so they offer no corroboration and no case for a segment-specific launch.

**Caveats for the review:**
- **Bar units.** The pre-registration doesn't say whether 0.005 is absolute or relative. I read it as absolute, which fails the bar. If the team meant a 0.5% relative lift, the observed +0.81% passes and the decision becomes Ship. Please confirm with the pre-registration authors before the meeting.
- **Allocation change.** The audit log shows allocation cut from 20% to 10% on 2026-09-16, but `experiment.json` still says 20, so the current state needs checking. The arms stayed 50/50 and the exposure-balance check passed, so the comparison is probably still valid. It does pool different traffic mixes over time, though.
- **Status.** The experiment is still marked active past its planned 14 days.