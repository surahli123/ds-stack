Decision: Keep running

# Ranker v7 readout

**Bottom line:** The data we have can't support ship or no-ship. The Pulse snapshot is an early, partial one, and under the pre-registered sequential analysis the primary metric is not yet distinguishable from zero, let alone from the ship bar. Pull a fresh Pulse covering the full run before deciding.

## Primary: Successful Search Rate (bar: +0.5%, point estimate must reach it)
- Control 0.4120, Test 0.4143. Lift is +0.0023 absolute, or +0.55% relative.
- The fixed-horizon 95% CI is ±0.40%, p = 0.007. That is the "naive" view, and it is not valid here because this is an interim look.
- The pre-registered sequential 95% CI is ±0.76%, so the relative lift is **+0.55% [-0.21%, +1.31%]**. It includes zero.
- The point estimate sits just above the 0.5% bar only if the bar is relative. I read it as relative because the guardrail margins are relative, but prereg.json doesn't say. If the bar is absolute (+0.005), the point estimate (+0.0023) is well short of it.
- Either way, the interval spans both "no effect" and "clearly above bar", so the ship criterion is not met with any confidence.

## Why this isn't a final result
- **Stale and partial data:** the Pulse is dated 2026-09-18, which is day 7 of 14 (start 2026-09-12). It has about 481k units per arm against 900k planned (53%). The planned end was 2026-09-26, and the experiment is still "active" in config. Today is 2026-10-12, so the snapshot is about 3.5 weeks old.
- **Config vs. prereg mismatch:** experiment.json shows `sequentialTesting: false`, while prereg and the Pulse request use sequential. I used the sequential intervals, as pre-registered. The audit log is empty, so nobody changed this after launch. It is simply set up inconsistently, and the setting should be fixed.
- **Health:** exposures are balanced (481k vs 480k, health check passed), so there's no sample-ratio concern.

## Guardrails (sequential 95% CIs, relative; margin in brackets)
| Metric | Change | CI half-width | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.20% | ±0.95% | 2% | Within margin |
| Zero Result Rate | 0.0% | ±2.66% | 3% | Within margin |
| Abandonment Rate | +0.10% (worse) | ±1.14% | 1% | Not cleared: worst case about +1.24% |
| Revenue per User | -0.10% | ±1.33% | 1% | Not cleared: worst case about -1.43% |

Neither Abandonment nor Revenue shows harm. The intervals are just too wide to rule it out yet.

## Secondary and segments
All secondary metrics (CTR, long clicks, reformulation, queries, sessions and the rest) are flat. None is significant on the sequential intervals.
Segment cuts were not pre-registered. Head queries show +0.96% (p = 0.043 fixed-horizon), and mobile is -0.59%. With roughly 60 unadjusted segment metrics, one nominal p < 0.05 is expected by chance, so I would not act on either. Mobile is worth a look in the final data.

## Recommendation
1. Pull the final Pulse (full 14 days, sequential on, same settings) and re-run this readout.
2. Ship only if the sequential CI supports the pre-registered bar and Abandonment and Revenue are cleared within their margins.
3. If the full-sample interval still straddles zero, call it "No effect found" rather than extending further.
