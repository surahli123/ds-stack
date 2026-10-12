Decision: Keep running

# Ranker v7 readout

**Bottom line:** The early numbers look good, but this Pulse is a 3-day interim snapshot of a 14-day fixed-horizon test. It is not the pre-registered analysis, so I can't call ship or don't-ship from it. We need the full-window Pulse.

## What the data says (Pulse ds 2026-09-15, no CUPED, 95% CI)
Primary: Successful Search Rate (SSR)
- Control 41.20%, Test 41.79%. The lift is +0.585 pp absolute (+1.42% relative), 95% CI about [+0.13 pp, +1.04 pp], p = 0.011.
- The pre-registered ship rule is that the point estimate reaches the +0.5 pp bar. The point estimate (0.585 pp) is above it, but only just. The CI lower bound (0.13 pp) is well below the bar, so the true effect could be much smaller than the bar.

Guardrails (worst-case end of the CI vs. prereg margin, read as relative change). All are inside their margins so far.
| Guardrail | Observed | Worst case in CI | Margin |
|---|---|---|---|
| Latency p95 | +0.2% (412.8 vs 412.0 ms) | +0.7% | 2% |
| Abandonment | +0.1% | +0.7% | 1% |
| Zero Result Rate | 0.0% | +1.4% | 3% |
| Revenue per User | -0.1% | -0.8% | 1% |

Revenue and Zero Result have the least headroom, and the intervals are wide at this sample size.

Health: the exposure balance check passed. Arm sizes are 261,000 vs 260,000, with no sample-ratio concern.

## Why this can't support a ship decision yet
1. **Interim data.** The test started 2026-09-12, so the Pulse covers about 3 of the 14 planned days (about 260k units per arm vs. 900k planned, roughly 29%). It also misses a full weekly cycle, and early lifts often fade from novelty or day-of-week mix.
2. **Peeking.** The experiment is configured with `sequentialTesting: false`, so the 95% CI and p = 0.011 are valid only at the planned end. Stopping on an interim look inflates false-positive risk, and the estimate is likely biased upward.
3. **Stale snapshot.** Today is 2026-10-12. The planned end was around 2026-09-26, yet the config still shows status "active" and the only Pulse is from 09-15. I don't know why the experiment is still active, or whether a later Pulse exists. The audit log is empty, so I can't see any config changes. Nothing indicates a mid-test change, but the log gives no evidence either way.
4. **Segment cuts are not evidence.** Desktop, Tail and Navigational SSR are slightly negative and Mobile and Head are slightly positive, but none is significant. The one "significant" segment result (Desktop Time to First Click, p = 0.0499) is one hit among about 60 unadjusted segment metrics. This is expected noise. I'm not acting on any of it, but the final readout should check that no segment is clearly harmed.

## What we need before the decision
- Pull a fresh Pulse covering the full 14-day window (or whatever the run actually reached), with the same settings (no CUPED, 95%). Confirm why the experiment is still active, and stop it at the planned horizon.
- Apply the pre-registered rule to that result: SSR point estimate ≥ +0.5 pp, and all four guardrails inside their margins.
- If the final point estimate lands near the bar, say so plainly. The CI will still be wide, so call it "ship on the prereg rule, with uncertain magnitude" rather than a firm +0.5 pp.

## Recommendation for tomorrow's review
Don't ship on this snapshot. The signal is promising and nothing is harmful so far, so keep the test on its pre-registered schedule and decide on the full-window data.
