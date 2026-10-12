Decision: Ship

# Ranker v7: launch readout

**Recommendation:** Ship lambdamart_v7. The single pre-registered primary metric clears its pre-registered bar, and no pre-registered guardrail is breached.

## Setup (matches prereg)
- A/B test on userID. 50/50 split, about 1.0M users per arm (plan was 900k). Ran 2026-09-12 to 09-26 (14 days planned). The Pulse snapshot is dated 09-25.
- Exposure balance health check passed. The audit log is empty, so no mid-flight config changes.
- The only parameter that differs between arms is ranker_model (snippet_length is 160 in both). This is the intended change.
- Pulse was run without CUPED at 95% confidence, one pre-registered primary, so no multiplicity adjustment is needed.

## Primary: Successful Search Rate
| | Control | Test | Rel. change | 95% CI (rel.) | p |
|---|---|---|---|---|---|
| SSR | 41.20% | 41.53% | **+0.81%** (+0.33 pp) | +0.41% to +1.21% | 7e-5 |

- The prereg rule is "ship requires point estimate at or above the bar", with a bar of +0.5% relative. +0.81% meets it.
- The lower CI bound (+0.41%) is slightly under the bar. The prereg did not require the CI to clear it, so the rule is met. The true lift could be a bit under 0.5%, but it is very unlikely to be zero.
- The result is consistent with the pre-period estimate (+0.71%, CI +0.31% to +1.11%).
- I read the bar as relative, because the prereg margins and pre-period numbers are relative. If the bar were meant as 0.5 pp absolute, the test (+0.33 pp) would fail. Please confirm this reading in the room.

## Guardrails (worst end of the 95% CI vs the prereg margin)
| Metric | Change | Worst-case bound | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.2% (412.0 to 412.8 ms) | +0.7% | 2% | OK |
| Abandonment Rate | +0.1% | +0.7% | 1% | OK |
| Zero Result Rate | 0.0% | +1.4% | 3% | OK |
| Revenue per User | -0.1% | -0.8% | -1% | OK, but thin |

Revenue's lower bound is only 0.2 pp inside the margin. The revenue CI is wide, so a small revenue loss cannot be ruled out. I'd watch it after launch.

## Secondary and segment results (exploratory, not decision-driving)
- Secondary metrics (CTR, long click, reformulation, queries, sessions, ads) are all flat and non-significant.
- **Mobile SSR points the wrong way:** -0.82% (CI about -1.8% to +0.2%, p=0.11), against Desktop +0.51% (not significant). Neither segment is significant on its own. They are many unplanned cuts, so this is most likely noise. But it is the one pattern worth watching, so check mobile SSR after ramp.
- A few segment time-to-first-click and tail-click results have p<0.05 in the favorable direction (Desktop and Tail TTFC, Tail clicks per user). With about 70 segment metrics and no correction, I treat these as hints only.

## Caveats
- Short, single-window test, so novelty effects are not ruled out. Roll out with a holdback or monitor SSR for the first weeks.
- The experiment is still "active" in Statsig past its 14-day duration. Close it out when launching.
