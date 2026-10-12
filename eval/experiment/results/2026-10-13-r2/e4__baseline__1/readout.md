Decision: Don't ship

# Ranker v7 – launch readout

**Bottom line:** Ranker v7 produces a real but small improvement. It is about a third of the pre-registered bar, so it fails the ship criterion. Guardrails are clean.

## Primary metric: Successful Search Rate (pre-registered bar: +0.5 pt overall, point estimate must reach it)
- The Pulse scorecard covers **triggered searches only**. Triggered searches are 10% of searches and 20.5% of control successes. The bar is defined **overall**, so the scorecard number can't be compared to it directly.
- Triggered: 41.20% → 41.98%, **+0.783 pt** (95% CI +0.536 to +1.030 pt, p<0.001).
- Converted to overall (× 0.205): **≈ +0.16 pt** (95% CI ≈ +0.11 to +0.21 pt).
- The point estimate is below +0.5 pt, and even the top of the CI (+0.21 pt) is below it. Reading the raw +0.78 pt against the +0.5 bar would wrongly look like a pass.
- To clear the bar overall, the triggered lift would need to be about +2.4 pt, roughly 3× what was observed.

## Guardrails (all within pre-registered margins; none shows harm)
| Metric | Change (95% CI half-width) | Margin |
|---|---|---|
| Latency p95 | +0.2% (±0.5%) | 2% |
| Abandonment Rate | +0.1% worse (±0.6%) | 1% |
| Zero Result Rate | 0.0% (±1.4%) | 3% |
| Revenue per User | −0.1% (±0.7%) | 1% |

## Other observations
- **Queries per User −1.04%** (p=0.024). This is the only secondary result of note, and it is not pre-registered. About 60 secondary and segment metrics were scanned, so a few nominal p<0.05 results are expected by chance. Treat it as a flag to watch, not a finding. The same applies to the Desktop time-to-first-click and Informational reformulation segments (p≈0.04–0.05).
- No segment (mobile/desktop, head/tail, navigational/informational) shows a meaningful lift or harm. Secondary metrics (CTR, long clicks) are flat, so the support for the primary is limited.

## Experiment validity
- Design is a 50/50 A/B on userID. The exposure-balance health check passed. There are 1.0M units per arm against 0.9M planned.
- The run covers the full planned 14 days (09-12 to 09-25). Statsig sequential testing was off, so this is a single look and the p-values and CIs are valid.
- The audit log has no changes during the run. Only the intended parameter (`ranker_model`) differs between arms, and `snippet_length` is identical.
- Pulse was pulled with CUPED off, matching the pre-registered analysis.

## Recommendation
Don't ship on the pre-registered criterion. If the team still wants v7 for other reasons, that is a deliberate change to the bar and should be argued explicitly at the review, not inferred from the triggered +0.78 pt. A follow-up should look at why the triggered lift is small, or at broadening the trigger population.
