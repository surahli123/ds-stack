Decision: Don't ship

# Ranker v7: launch readout

**Recommendation:** Don't ship v7 as it stands. It meets the primary-metric bar, but it fails the pre-registered Abandonment Rate guardrail.

## Setup (checked)
- Design: A/B test, lambdamart_v6 vs lambdamart_v7, 50/50 split on userID. Only `ranker_model` differs between arms (`snippet_length` is 160 in both).
- Window: 2026-09-12 to 2026-09-25, the planned 14 days. The Pulse `ds` is 2026-09-25, so it covers the full window.
- Sample: 1,000,000 users per arm, above the 900k planned. The exposure balance health check passed.
- The audit log is empty, so the config was not changed mid-flight.
- Pulse was requested with CUPED off at 95% CIs. No sequential testing and no multiplicity correction are configured, which matches the prereg (a single primary metric).

## Primary: Successful Search Rate (bar: +0.005 absolute, point estimate)
- Control 0.4120, test 0.4171. The change is **+0.00511** (95% CI +0.0035 to +0.0068), or +1.24% relative.
- The point estimate clears the pre-registered bar of 0.005, but only just: it is 0.0001 above it.
- The CI lower bound is below the bar, so the true lift could be as small as about +0.0035. The prereg rule is `point_at_bar`, so this counts as a pass.

## Guardrails (margins treated as relative, consistent with the latency, revenue and zero-result margins)
| Metric | Change (rel., 95% CI) | Margin | Verdict |
|---|---|---|---|
| **Abandonment Rate** (lower is better) | **+2.2%** (+1.5% to +2.9%); 0.187 to 0.191 | 1% | **Breached.** The whole CI is worse than the margin. |
| Latency p95 | +0.2% (±0.5%), +0.8 ms | 2% | OK |
| Zero Result Rate | 0.0% (±1.4%) | 3% | OK |
| Revenue per User | -0.1% (±0.7%) | 1% | OK (the CI's worst end is -0.8%, which is close to the margin) |

If the Abandonment margin were meant as 0.01 absolute, the upper CI bound of +0.0054 would sit inside it. The other three margins only make sense as relative, so I read this one the same way. The team should confirm that reading, because the decision depends on it.

## Context
- CTR (+1.9%) and Clicks per User (+2.1%) rose with the primary metric. Long Click Rate (-0.1%, p=0.76) was flat. If the extra clicks are not turning into satisfied clicks, that would fit abandonment rising too, but this is a hypothesis, not something the data shows.
- Segment cuts (device, head/tail, navigational/informational) are exploratory and unadjusted. About 60 cuts were run, so a few nominal p<0.05 results are expected by chance. Examples are Head-query abandonment (+1.6%, p=0.04) and Tail-query CTR (-1.1%, p=0.014). I'm not drawing conclusions from any of them. None of the segment lifts in Successful Search Rate is individually significant.

## What would change the call
- If the team confirms Abandonment Rate was meant to carry an absolute 0.01 margin, v7 passes every pre-registered criterion and the decision becomes Ship.
- Otherwise, find out why abandonment rose: look at the query types or sessions where searches end without a click, and whether the extra clicks are low quality. Then fix it and re-test, or have the review explicitly accept a roughly 2% abandonment cost in exchange for a +1.2% success-rate lift. That would be a deliberate waiver of the prereg, not a ship under it.
