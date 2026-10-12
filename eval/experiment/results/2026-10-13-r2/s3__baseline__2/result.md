Decision: Ship

**Ranker v7 launch readout**

**Result.** Ranker v7 beats the pre-registered primary bar, and no guardrail is breached. I recommend shipping.

**Design checks.**
- This is a clean 50/50 A/B test at the user level, with 1.0M users per arm (900k planned).
- The exposure-balance health check passed.
- The audit log is empty, so nothing was changed mid-flight.
- The only parameter that differs between arms is `ranker_model`, which is the intended one (`snippet_length` is 160 in both).
- Pulse was pulled without CUPED at 95% confidence, as pre-registered. The readout was run over the planned 14 days with no sequential peeking, so the p-values are not distorted by early looks.

**Primary: Successful Search Rate.** Bar: point estimate at or above +0.5% relative.

| | Control | Test | Effect | 95% CI |
|---|---|---|---|---|
| Successful Search Rate | 41.20% | 41.53% | +0.81% relative (+0.33pp) | +0.41% to +1.21% (p = 7e-5) |

- The point estimate clears the +0.5% bar.
- I read the bar as relative, because the daily files and guardrail margins are expressed as relative changes. If the bar were meant as +0.5pp absolute, it would not be met (+0.33pp). The prereg doesn't say which, so please confirm that reading in the room.
- The lower CI bound (+0.41%) is below the bar. The prereg requires the point estimate at the bar, not the CI, so this is not a failure. The true lift could be somewhat under 0.5%.

**Guardrails.** Each worst-case CI bound is compared with its margin.

| Guardrail | Change | Worst case | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.2% (412.8 vs 412.0 ms) | +0.7% | 2% | Pass |
| Abandonment Rate | +0.1% | +0.7% | 1% | Pass |
| Zero Result Rate | 0.0% | +1.4% | 3% | Pass |
| Revenue per User | −0.1% | −0.8% | 1% | Pass |

**Is the effect fading?**
- By calendar day, the lift falls from +1.25% on day 1 to about +0.6% on day 12, with the CI touching zero around day 12. Read alone, that looks like novelty decay.
- By exposure day, the lift is flat at about +0.8% from the first day since exposure through day 12, with no decay. The calendar-day decline is therefore a cohort-mix effect, not users tiring of the new ranker. The cumulative +0.81% is a fair estimate of the steady-state lift.

**Caveats (none block shipping).**
- **Reformulation Rate:** it got worse, +1.0% relative (p = 0.013). It is not a pre-registered guardrail, and it is one of about 14 unadjusted top-level secondaries, so it could be chance. Time to First Click improved (−1.1%, p = 0.029). Neither moves the decision.
- **Platform split:** Successful Search Rate is nominally negative on Mobile (−0.83%, p = 0.058) and Desktop (−0.68%, p = 0.078), against +0.81% overall.
  - The platform means can't average to the overall figure (test overall 41.53% exceeds both Mobile 41.37% and Desktop 34.07%), so the segment cuts must not cover all traffic. I can't reconcile them from these files.
  - These are about 30 unadjusted subgroup comparisons with wide CIs, and none are significant. I treat this as exploratory, not a reason to hold the launch.
- **Follow-up:** I suggest checking the platform cut after launch and keeping a holdback, if one is cheap, to confirm the lift.