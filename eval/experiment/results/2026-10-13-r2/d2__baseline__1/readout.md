Decision: Don't ship

# Ranker v7: launch review readout

**Bottom line:** Ranker v7 lowered Successful Search Rate, the pre-registered primary metric. The pre-registration required a lift of at least +0.5 percentage points. We measured -0.26 pp, and the whole 95% CI is below zero. Don't ship.

## Primary metric (pre-registered, 95% CI, no CUPED)
| Metric | Control | Test | Abs. change (95% CI) | Rel. change | p |
|---|---|---|---|---|---|
| Successful Search Rate | 41.20% | 40.94% | **-0.255 pp** (-0.420, -0.090) | -0.62% | 0.0024 |

- Ship rule: the point estimate must reach +0.5 pp. It is 0.76 pp short of that bar.
- The CI excludes zero, so this is a measured regression, not just a miss.
- The CI also excludes the bar. Even the best case in the interval (-0.09 pp) is far from +0.5 pp.

## Guardrails (pre-registered margins, relative change vs. margin, worst end of CI)
| Guardrail | Change | Worst end of 95% CI | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.2% (412.8 vs 412.0 ms) | +0.7% | 2% | Within margin |
| Abandonment Rate | +0.1% | +0.7% | 1% | Within margin |
| Zero Result Rate | 0.0% | +1.4% | 3% | Within margin |
| Revenue per User | -0.1% | -0.8% | 1% | Within margin |

No guardrail was breached. That does not change the decision, because the primary metric failed.

## Secondary metrics (descriptive only, not part of the ship rule)
None of the secondary metrics is significant. CTR is -0.11 pp (p=0.16) and Long Click Rate is +0.09 pp (p=0.19). Clicks, queries and sessions per user, and the query-segment cuts, are all flat within noise. Nothing offsets the primary regression. Informational-query clicks are slightly negative (-1.1%, p=0.27), which is not significant and is worth watching only if the team iterates.

## Validity checks
- Design: A/B, unit userID, 50/50 split, 20% layer allocation. Exposures balanced (health check passed).
- Duration: started 2026-09-12, planned 14 days, Pulse ds 2026-09-25. The full planned window is covered, so there is no peeking issue.
- Sample: 1.0M units per arm, above the 0.9M planned.
- Config: the only parameter that differs between arms is `ranker_model` (v6 vs v7), the intended one. `snippet_length` is the same in both arms. The audit log has no changes after launch.
- Single pre-registered primary, so no multiplicity adjustment is needed.
- Caveats: Pulse was requested without CUPED, as pre-registered. I only had the aggregate Pulse output, so I did not check novelty effects or segment heterogeneity.

## Recommendation
Do not launch v7 as configured. If the team wants to iterate, look at why the regression appears (informational queries are one lead) and re-test with a new pre-registration.
