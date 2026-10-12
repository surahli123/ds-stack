Decision: Don't ship

**Ranker v7 raised Successful Search Rate, but by less than the pre-registered ship bar.**

**Primary metric (Successful Search Rate, 95% CI, no CUPED)**
- Control is 41.20% and Test is 41.53%. The lift is +0.334 pp absolute (+0.81% relative), with a 95% CI of +0.17 to +0.50 pp (p = 7e-5).
- The pre-registration says ship requires the point estimate to reach +0.5 pp. The point estimate is 0.334 pp, which is about two-thirds of the bar.
- The lift is real and positive. The upper end of the CI only just touches the bar, so a +0.5 pp effect is possible but not what we observed. This is a miss on the pre-registered criterion, not a null result.

**Guardrails (relative change, margins from the pre-registration)**

| Guardrail | Change (95% CI half-width) | Margin | Result |
|---|---|---|---|
| Latency p95 | +0.2% (±0.5%) | 2% | Within |
| Abandonment Rate | +0.1% (±0.6%) | 1% | Within |
| Zero Result Rate | 0.0% (±1.4%) | 3% | Within |
| Revenue per User | −0.1% (±0.7%) | 1% | Within |

The pre-registration doesn't say whether the margins are relative or absolute. I read them as relative. All four guardrails pass, and none of them blocks a ship. The ship bar is the only thing that does.

**Things the review should know**
- **Exposure imbalance.** `experiment.json` lists 1.01M control exposures and 0.99M test exposures. At a 50/50 split that is a sample-ratio mismatch (chi-square about 200, p far below 0.001). The "Exposures balanced: PASSED" health check contradicts it. Pulse reports 1.0M units per arm, which is also above the planned 900k, so the two files don't agree. The exposure counts may be from a later snapshot than the Pulse data (ds 2026-09-25). Someone should confirm this. If the mismatch is real, the primary result is not trustworthy, whichever way it points.
- **Clicks per User.** It fell by 1.0% (±0.8%, p = 0.014). It isn't a pre-registered guardrail, and it is one of about 14 secondary metrics (about 60 including segments) with no multiplicity correction, so it could be chance. It is the one result that conflicts with a "better ranking" story, though, so check it before any re-run.
- **Segment results.** I'd treat them as exploratory. Tail-query Abandonment (+1.7%, p = 0.034) is one of about 48 segment cuts, which is consistent with chance. No segment shows a clear win.
- **Config and timing.** The audit log is empty, so no config changes were recorded during the run. The run covers 14 days (Sep 12 to Sep 25) with a single look and no sequential testing. Both are consistent with the plan.

**Recommendation**
- Don't ship v7 on this readout.
- If the team still wants it, treat it as a new decision. Either re-run with a larger or longer test, or have the owners explicitly revise the ship bar. Don't reinterpret the result after seeing it.
- Resolve the exposure-count discrepancy first.