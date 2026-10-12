Decision: Can't tell

# Ranker v7 – launch review readout

**Bottom line:** This Pulse cannot tell us whether Ranker v7 meets its ship bar. The data comes from a different experiment than the one we pre-registered. Even taken at face value, the primary metric is below the bar. Don't treat this as a ship signal.

## 1. The experiment is not the one we pre-registered
- Pre-reg is `ranker_v7` (unit userID, 90 days, 50,000 units/arm). The config and Pulse are `q3_search_launches_holdout`. Its stated hypothesis is "the combined effect of the quarter's ranking launches", and it carries `holdoutIDs: q3_search_holdout`.
- Control is the 5% holdout on `lambdamart_v6`. Test is everyone else on `lambdamart_v7`, in layer `search_ranking`. Any other launches that shipped this quarter are bundled into Test. So even a clean lift is not attributable to v7 alone.
- Pulse shows 1,000,000 units in each arm, but the config says a 5% / 95% split. Equal arms don't match that, and neither matches the 50,000/arm plan. The only health check on the config is "exposures balanced: PASSED", which I can't reconcile with the numbers. Someone needs to confirm what population this Pulse actually covers.
- `audit_logs.json` is empty, so there is no change history to explain any of this.

## 2. Timing
- Started 2026-09-12 and planned for 90 days (ends 2026-12-11). The Pulse is dated 2026-09-25, about 2 weeks in. It was run without CUPED, at 95% CI, with no sequential testing correction. Today (2026-10-12) it is about 30 days in, so this Pulse is already stale.

## 3. Primary metric (Successful Search Rate, bar +0.005 absolute, ship needs the point estimate at the bar)
| | Value |
|---|---|
| Control → Test | 0.4120 → 0.4153 |
| Absolute change | **+0.0033** (+0.81% relative) |
| 95% CI | +0.0017 to +0.0050 |
| p | 7e-5 |

The lift is statistically real in this data. But the point estimate (+0.0033) is below the +0.005 bar, and the CI only just reaches it at the top. By the pre-reg's own rule this does not qualify to ship.

## 4. Guardrails (all within pre-registered margins, no harm detected)
- Latency p95: +0.2% (CI ±0.5%) vs 2% margin.
- Abandonment: +0.0002 abs (CI ±0.0011) vs 0.01 margin.
- Zero Result Rate: 0.0 change (CI ±1.4% rel) vs 3% margin.
- Revenue per User: −0.1% (CI ±0.7%) vs 1% margin.

## 5. Secondary and segment metrics (exploratory only)
- 56 secondaries were checked and none were pre-registered, so no multiplicity correction was applied. A handful have nominal p<0.05 (SSR head queries +0.0038; CTR navigational −0.0047; TTFC mobile −0.11s). With this many tests, about 3 hits are expected by chance, so I don't read any of them as findings.
- Overall secondaries (CTR, long clicks, reformulation, clicks/user, sessions) are flat. None shows a clear effect either way.

## 6. What I'd need to decide
1. Confirmation of whether a clean v7-only comparison exists (a `ranker_v7` experiment, or the holdout restricted to v7 exposure). If not, the pre-reg question is unanswerable from this setup.
2. Explanation of the unit counts and the 5/95 split.
3. A fresh Pulse, ideally at or near the planned duration. The current lead is about 0.0017 short of the bar, which more data could narrow, but it won't move the estimate.

**Recommendation for the review:** do not ship on this evidence. If a v7-only analysis shows an effect of at least +0.005 with guardrails intact, revisit.
