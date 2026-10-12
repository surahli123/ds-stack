Decision: Ship

# Ranker v7 – launch readout

**Design:** A/B, unit = userID, 50/50 (lambdamart_v6 vs lambdamart_v7), 14 days (2026-09-12 → 09-25), ~1.0M users/arm (plan: 900k). Pulse read at the planned end, no CUPED, 95% CI, no peeking/sequential rules. Exposure-balance health check passed.

## Primary (pre-registered: Successful Search Rate, ship if point estimate ≥ bar 0.005)
| | Control | Test | Δ abs | Δ rel | 95% CI (rel) | p |
|---|---|---|---|---|---|---|
| Successful Search Rate | 41.20% | 41.53% | +0.334 pp | +0.81% | ±0.40% → [+0.41%, +1.21%] | 7e-5 |

The point estimate (+0.81% relative) clears the 0.5% bar; the effect is clearly nonzero. The prereg rule is point-at-bar, so the CI lower bound (+0.41%) falling below the bar does not block shipping, but the true lift could be smaller than the bar.

## Guardrails (prereg margins, read as relative; 95% CI worst-case end vs margin)
| Metric | Δ rel | CI | Margin | OK |
|---|---|---|---|---|
| Latency p95 | +0.2% | ±0.5% (worst +0.7%) | 2% | yes |
| Abandonment Rate | +0.1% | ±0.6% (worst +0.7%) | 1% | yes |
| Zero Result Rate | 0.0% | ±1.4% | 3% | yes |
| Revenue per User | −0.1% | ±0.7% (worst −0.8%) | −1% | yes |

All four guardrails are inside their margins even at the CI's bad end. Secondary metrics (CTR, long clicks, reformulation, etc.) show nothing significant; ~60 segment cuts were examined and none is credible evidence of harm or heterogeneity (a few p≈0.05–0.07 among dozens of tests is what chance gives; unadjusted, so don't read them). CTR is slightly down and not significant (−0.29%, p=0.26); worth monitoring, not a blocker.

## Caveats the review should know
1. **Bar/margin units are not stated in prereg.** I read 0.005 as relative (0.5%), the only reading consistent with the guardrail margins (a 0.02 absolute margin on a 412 ms latency or 0.03 on a 3.1% zero-result rate is meaningless). If the team meant 0.5 percentage points absolute, the lift (+0.33 pp) misses the bar and the decision becomes Don't ship. Please confirm with the prereg authors before the meeting.
2. **Allocation changed mid-test.** The audit log shows allocation 20% → 10% on 2026-09-16 (day 5), yet experiment.json currently shows 20. Either it was reverted without a log entry or the log/config disagree; this needs an explanation. Both arms were scaled equally and the exposure-balance check passed, so the randomized comparison should hold, but the pooled result mixes two traffic regimes and Statsig advises against changing allocation mid-run. I did not have per-day data to check for a time trend or novelty effect.
3. Single primary metric, so no multiplicity correction needed for the headline; secondary/segment p-values are unadjusted.

## Recommendation
Ship, conditional on (1) confirming the bar is relative and (2) a satisfactory explanation of the allocation edit. If either fails, change to Don't ship / Escalate respectively.
