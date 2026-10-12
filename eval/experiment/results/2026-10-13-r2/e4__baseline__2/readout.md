Decision: Don't ship

# Ranker v7 readout

**Bottom line.** v7 improves Successful Search Rate (SSR) on the searches it touches. Once that gain is translated to the overall scale the pre-registration uses, it is about 0.39% relative, below the pre-registered 0.5% bar. The pre-registration says ship requires the point estimate to be at the bar, so the answer is Don't ship. The bar is missed narrowly, not by a lot (see the caveat on the bar's units).

## Primary metric
| | Triggered scorecard (Pulse) | Overall (rescaled) |
|---|---|---|
| Control SSR | 0.4120 | ~0.201 |
| Abs. change | +0.00783 (95% CI ±0.00247) | +0.00078 (±0.00025) |
| Rel. change | +1.9% (CI roughly +1.3% to +2.5%) | **+0.39%** (CI roughly +0.27% to +0.51%) |

- Pulse reports the triggered population only. Triggered searches are 10% of all searches and 20.5% of control successes (prereg `mass_share`), and the bar is defined overall.
- Rescaling: 1.9% × 0.205 ≈ 0.39%. Cross-check: 0.1 × 0.00783 / (0.0412 / 0.205) ≈ 0.39%.
- Reading the 1.9% triggered lift against the 0.5% bar would wrongly clear it.
- The point estimate (0.39%) is below the bar (0.5%). The overall CI only reaches the bar at its upper edge (~0.51%). The lift is real (p<0.001) but too small for the pre-registered criterion.
- Caveat on the bar's units: I read it as relative, which matches the mass_share framing. If it were 0.005 absolute overall, the gap would be far larger (0.0008 vs 0.005), so the decision is the same either way. Please confirm the intended units with the pre-reg authors.

## Guardrails (all within margin, no concern)
- Latency p95: +0.2% (CI ±0.5%), margin 2%.
- Abandonment: +0.1% (CI ±0.6%), margin 1%.
- Zero Result Rate: 0.0% (CI ±1.4%), margin 3%.
- Revenue per User: −0.1% (CI ±0.7%), margin 1%.

## Validity
- Exposure balance health check passed. The arms have 1.0M units each (the plan was 0.9M) and a 50/50 split.
- The run covers 14 days, as planned. The audit log is empty, so there were no mid-test config changes.
- Only `ranker_model` differs between arms. `snippet_length` is identical (160), so there is no confound.
- Analysis was fixed-horizon (no sequential testing), CUPED off, 95% CI. One primary metric, so no multiplicity adjustment is needed for it.

## Secondary / exploratory (not decision-bearing)
- Queries per User is −1.04% (p=0.024). It is directional (higher is better) and would be worth a look. It is one of ~60 metrics and segment cuts with no correction, and Sessions and Clicks per User are flat. Treat it as a hypothesis, not a finding.
- Segment cuts are consistent with a small positive effect and no clear heterogeneity. The few nominal p<0.05 hits (Desktop Time to First Click, Informational Reformulation) are within what chance produces across this many cuts.
- CTR and Long Click Rate are flat, so the SSR gain is not corroborated by engagement metrics.

## Recommendation
Do not launch v7 as is. Options for the review:
1. Accept the miss and iterate on the ranker.
2. If the team thinks the 0.5% bar was set too high relative to a 0.39% gain with clean guardrails, change it through an explicit, documented decision. That is a new decision, and it should not be presented as this test meeting its criterion.
3. Extending the run would narrow the CI but would not move the point estimate. Do not extend the run to chase the bar.
