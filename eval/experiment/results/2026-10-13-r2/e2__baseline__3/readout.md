Decision: Ship

# Ranker v7 – launch readout

**Design:** A/B, userID, 50/50 within a 20% allocation, 14 days (2026-09-12 to 09-25), fixed-horizon, 95% CI, no CUPED. Exposures-balanced check passed; 1,000,000 units per arm (prereg planned 900,000). Audit log is empty, so the config did not change mid-test. The only parameter that differs between arms is `ranker_model` (v6 → v7), as intended.

## Primary (prereg: Successful Search Rate, ship if point estimate ≥ bar of 0.005)
| | Control | Test | Abs. change | Rel. change | p |
|---|---|---|---|---|---|
| Successful Search Rate | 41.20% | 41.53% | +0.334 pp (CI ±0.165 pp) | **+0.81%** (CI ±0.4%) | 7e-5 |

The lift is statistically significant. The point estimate (+0.81% relative) clears the 0.5% bar. The prereg rule is point-at-bar, so the lower CI bound (about +0.41%) falling under 0.5% does not block shipping.

**Assumption to confirm in the review:** prereg.json gives the bar as 0.005 with no unit. I read it as relative (0.5%). The guardrail margins in the same file can only be relative (e.g. 0.03 on Zero Result Rate, whose baseline is 0.031). If the bar is absolute (0.5 pp), the observed +0.33 pp (CI 0.17 to 0.50 pp) misses it and the call becomes Don't ship. The team should confirm the intended unit.

## Guardrails (margins read as relative, worst end of the 95% CI)
| Metric | Change | Worst case | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +1.2% (412 → 416.9 ms), p=3e-6 | +1.7% | 2% | Within margin, but a real regression |
| Abandonment Rate | +0.1% ±0.6% | +0.7% | 1% | OK |
| Zero Result Rate | 0.0% ±1.4% | +1.4% | 3% | OK |
| Revenue per User | −0.1% ±0.7% | −0.8% | 1% | OK |

## Things to flag (not blocking)
- **Latency:** about +5 ms p95, significantly slower. It is inside the agreed tolerance, but the upper bound (+1.7%) is close to the 2% limit. Worth a look from the serving team.
- **CTR fell** (30.5% → 30.3%, −0.71%, p=0.005) while successful-search rate rose. This is a secondary, non-preregistered metric. It is consistent with fewer wasted clicks, but nobody has verified that. Long Click Rate is flat (p=0.37).
- **Segments:** the lift is not significant in any segment (mobile, desktop, head, tail, navigational, informational). Head queries and desktop point slightly negative (−0.21 pp and −0.07 pp, both far from significant). The segments are underpowered, so they neither confirm nor contradict the overall result. They are exploratory only.
- Many secondary metrics were examined with no multiplicity correction. Only the primary and the guardrails drive the decision.

## Recommendation
Ship Ranker v7, subject to confirming that the 0.005 bar is relative. Monitor p95 latency and CTR after launch.
