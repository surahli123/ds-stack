Decision: No effect found

# Ranker v7: launch review readout

**Bottom line.** Ranker v7 did not move the pre-registered primary metric, and the data rules out the lift the team set as the ship bar. I don't recommend shipping it on this evidence. A possible gain on tail queries is worth a follow-up test, but it can't support a launch decision today.

## Test validity
- **Design:** this is a 50/50 A/B test on userID. Control runs `lambdamart_v6` and test runs `lambdamart_v7`. `snippet_length` is the same in both arms (160).
- **Duration:** the test started 2026-09-12 and the Pulse snapshot is dated 2026-09-25, so it covers the full planned 14 days.
- **Sample size:** each arm has 1.0M units, against 900k planned. That is enough, and the Pulse data covers the full run.
- **Health:** the exposure-balance check passed, and both arms have identical unit counts.
- **Config changes:** the audit log is empty, so nothing was changed mid-test.
- **Settings:** the analysis is unadjusted (no CUPED) at 95% confidence, with no sequential testing and no multiplicity correction. That matches the single primary metric in the pre-registration.

## Primary metric: Successful Search Rate
| | Value |
|---|---|
| Control | 41.20% |
| Test | 41.22% |
| Difference | +0.025 pp (95% CI −0.099 to +0.148 pp), p = 0.70 |
| Pre-registered ship bar | +0.5 pp, with the point estimate required to be at the bar |

The point estimate is about one-twentieth of the bar. The upper end of the CI (+0.15 pp) is also well below +0.5 pp. So this result isn't an underpowered "maybe". The test shows that v7 does not deliver a lift of the size we required, and the ship criterion fails.

## Guardrails
No guardrail is breached, but none of them is a reason to ship. All margins are read as relative changes against control.

| Metric | Change vs control | Worst case in CI | Pre-registered margin |
|---|---|---|---|
| Latency p95 | +0.8 ms (+0.2%) | about +0.5% | 2% |
| Abandonment Rate | +0.02 pp | about +0.7% relative | 1% |
| Zero Result Rate | 0.000 | ±1.4% relative | 3% |
| Revenue per User | −$0.0009 (−0.1%) | about −0.8% | 1% |

Revenue per User and Abandonment Rate are the closest to their margins. Their CIs stay inside the margins, but not by much.

## Secondary and segment metrics (exploratory)
- Nothing in the top-level secondary metrics is significant at 95%. The closest are CTR (+0.15 pp, p = 0.052) and Pagination Rate (p = 0.11).
- The data contains about 60 segment-level metrics, none of them pre-registered, and about 15 of them have p < 0.15. With that many comparisons, scattered small p-values are expected by chance. Navigational CTR (−0.55 pp, p = 0.027) and Mobile Long Click Rate (p = 0.06) are examples, and I would not read anything into them.
- **One segment stands out:** Successful Search Rate on tail queries is +1.46 pp (CI ±0.47 pp, p ≈ 0). That is strong enough to survive a multiplicity correction across all the segments. However:
  - It was not pre-registered.
  - Head, navigational and informational queries show essentially zero change.
  - The overall effect is only +0.025 pp, so tail queries must be a small share of traffic, or there are offsetting losses elsewhere. The data doesn't show the traffic mix, so I can't say which.
  - The segment-level rows for tail queries don't tell a consistent story. Tail CTR (+0.17 pp) and tail long-click rate are small and not significant.

  I'd treat this as a hypothesis, not a result.

## Recommendation
1. **Don't ship v7 on the pre-registered criterion.** The primary metric missed the bar, and the CI excludes the bar.
2. **Optional follow-up on tail queries.** If the team wants to pursue the tail-query signal, run a new pre-registered test aimed at tail queries. It should include a tail-query traffic share and a defined bar, so that a confirmatory result is possible.
3. **Not a regression.** v7 shows no sign of harm: all guardrails are within their margins. If the team has non-metric reasons to prefer v7 (for example, maintenance or infrastructure), the data doesn't argue against it. That would be a separate decision with different criteria.

## Caveats
- Segment shares and the metric definitions are not in the files I was given, so I couldn't reconcile the tail-query lift with the flat overall result.
- Guardrail margins are read as relative changes. If the team meant absolute margins, abandonment (+0.02 pp against a 1 pp margin) still passes, and the conclusion doesn't change.