Decision: Not an A/B test

# Ranker v7 readout

## Bottom line
The Pulse numbers can't be read as "v7 vs v6", so they can't support a ship call. The experiment was pre-registered as a **team-draft interleaving** test. It was configured and analysed as a between-group comparison. That comparison does not measure the thing we set out to test.

## What the config shows
- Control (`g_control`, 50%) serves `ranker_model=lambdamart_v6` with no `serving_mode`. Users see pure v6 rankings.
- Test (`g_test`, 50%) serves `ranker_model=lambdamart_v7` with `serving_mode=team_draft_interleaving`. Users see a blend of v6 and v7 results on each page.
- The pre-reg lists both `serving_mode` and `ranker_model` as intended parameters. Only the test arm has `serving_mode`, so the two arms differ in two things at once.
- So Pulse compares **pure v6 against an interleaved v6/v7 blend**. It does not compare v6 against v7.
- A proper interleaving test has every user see both rankers in the same result list. The readout is the within-user preference: which ranker's results got the credited clicks. Pulse's arm-vs-arm delta doesn't compute that. We have no per-ranker click credit or win-rate in these files.
- The audit log is empty, so nothing records or explains the setup. The "Exposures balanced" health check passes, but it only tells us the 50/50 split is intact.

## What Pulse reports (descriptive only, 2026-09-25, no CUPED, 95% CI)
| Metric | Δ abs (test − control) | 95% CI half-width | p |
|---|---|---|---|
| Successful Search Rate (primary) | +0.00334 (+0.81% rel; 0.4120 → 0.4153) | ±0.00165 | 7e-05 |

- The pre-registered bar is +0.005 at the point estimate, and the observed +0.0033 is below it.
- The point estimate would miss the bar even if the arms were comparable.
- The blend contains only part v7, so the effect of a full v7 launch could be larger. It could also be different in other ways. We can't scale this number up to a v7 effect.
- Guardrails show no flagged movement. Each interval is well inside its margin, but the margins are looser than the intervals, so this is weak evidence of safety rather than proof:
  - Latency p95: +0.2% (±0.5%)
  - Abandonment: +0.1% (±0.6%)
  - Zero Result Rate: 0.0%
  - Revenue per User: −0.1% (±0.7%)
- I did not look into the roughly 45 segment metrics (device, head/tail, navigational/informational). Slicing 60 metrics without correction would produce false positives.
- Units are 1.0M per arm against 0.9M planned, and the config runs 14 days from 2026-09-12. These are minor deviations.

## Recommendation for review
1. Don't treat this as a launch-gating result either way, and don't cite the +0.81% as the v7 effect.
2. Re-analyse from the interleaving logs, at the user level, for the per-ranker preference (v7 win rate against 50%, with a CI). Alternatively, rerun it as a real A/B test with v6-only against v7-only and `serving_mode` identical in both arms.
3. Decide the ship criterion before looking at the new result. The pre-reg bar (+0.005 on Successful Search Rate) was defined for an A/B delta. If the readout becomes an interleaving preference, the bar needs translating into preference terms.
