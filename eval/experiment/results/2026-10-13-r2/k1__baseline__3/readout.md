Decision: Can't tell

# Ranker v7 readout

**Bottom line:** The Pulse I was given is a 3-day interim snapshot, not the final 14-day result. It looks promising but can't support a ship decision. Pull a fresh Pulse (same settings) and decide against the pre-registered bar.

## Why the data is not decision-grade
- **Snapshot date:** Pulse `ds` is 2026-09-15. The experiment started 2026-09-12 (3 days in), planned 14 days, and today is 2026-10-12. This Pulse is a month stale and covers only the first days.
- **Sample:** 261k test / 260k control units. The pre-reg plans 900k per arm, so we have about 29%.
- **Peeking:** The experiment has no sequential testing (`sequentialTesting: false`), so a p-value from a mid-run look isn't valid for a go/no-go. Early days also tend to over-represent heavy and returning users and novelty effects.
- **Status:** The config still says `active` well past the planned end. Someone should confirm whether it was meant to stop and whether anything changed. `audit_logs.json` is empty, so the config shows no mid-flight edits. The arms are 50/50, the exposure-balance check passed, and the parameters differ only in `ranker_model` as intended. `snippet_length` is identical in both arms.

## Primary metric: Successful Search Rate (bar: +0.005 absolute, point estimate must reach it)
| | Control | Test | Abs. change | 95% CI | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4179 | +0.00585 (+1.42%) | about [+0.0013, +0.0104] | 0.011 |

- The point estimate (+0.00585) is above the +0.005 bar, so on this snapshot the pre-reg's `point_at_bar` rule is met.
- The CI is wide (half-width 0.0045, nearly the size of the bar). The lower end is +0.0013, so the true lift could be well under the bar. The result is not yet precise enough to tell "clears the bar" from "positive but small".
- I'm reading "+0.005" as an absolute change in rate. That is how the Pulse reports it, but the pre-reg doesn't say. If it meant relative, the bar would be about +0.002 absolute, which the data would clear.

## Guardrails (pre-registered margins, 95% CI)
All four pass on this snapshot. I read the margins as relative, matching Pulse's `percentChange`.
| Guardrail | Change | CI half-width | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.2% (+0.8 ms) | 0.5% | 2% | OK |
| Abandonment Rate | +0.1% | 0.6% | 1% | OK |
| Zero Result Rate | 0.0% | 1.4% | 3% | OK |
| Revenue per User | -0.1% | 0.7% | 1% | OK |

## Secondary and segment metrics
- CTR is up (+0.0023, p=0.003) and agrees in direction with the primary. Other secondaries (long clicks, reformulation, queries per user, and so on) are flat or not significant.
- I scanned about 60 segment metrics (mobile/desktop, head/tail, navigational/informational). A few have p near 0.05 (Desktop time-to-first-click, p=0.050; Navigational clicks per user, p=0.053), but with that many looks and no correction these are expected noise. I'm not reading anything into them. The segment point estimates for Successful Search Rate go in both directions (for example, desktop -0.003 and head queries +0.003, none significant), so there is no sign of a segment-specific problem or win.

## Recommendation
1. Re-pull Pulse (`cuped: false`, `confidence: 95`) now that the planned window is over. Verify that it shows about 900k per arm and a `ds` at or after about 2026-09-26.
2. If the final point estimate for Successful Search Rate is at or above +0.005 and all guardrails stay inside their margins, the pre-reg says Ship. If the point estimate falls below +0.005, the pre-reg says Don't ship or No effect found, depending on the CI.
3. Confirm why the experiment is still active past its planned end date.

Today's data does not change the call for either outcome: tomorrow's review should treat this as "promising, awaiting final numbers", not as a launch approval.
