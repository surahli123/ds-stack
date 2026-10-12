Decision: No effect found

# Ranker v7 readout

**Bottom line:** Ranker v7 did not move Successful Search Rate (SSR), and the data rule out an improvement as large as the pre-registered +0.5pp bar. Don't launch on the strength of this test. Guardrails are fine, but nothing here justifies shipping.

## Primary metric (pre-registered: SSR, ship only if the point estimate reaches +0.005 absolute)
- Control 0.4120, Test 0.41216. Difference **+0.016pp** (+0.04% relative), p = 0.79.
- 95% CI: **[-0.107pp, +0.140pp]**. Even the upper end is about 1/4 of the bar, so a +0.5pp effect is ruled out. The point estimate is 30x below the bar.
- The ship rule (point estimate at or above the bar) is not met.

## Guardrails (95% CIs, relative change vs. pre-registered margin)
| Metric | Change (95% CI half-width) | Margin | Result |
|---|---|---|---|
| Latency p95 | +0.2% (±0.5%) | 2% | OK |
| Abandonment | +0.1% (±0.6%) | 1% | OK |
| Zero Result Rate | 0.0% (±1.4%) | 3% | OK |
| Revenue per User | +3.1% (±2.1%) | -1% (must not drop) | OK, no harm |

No guardrail is harmed. Note that the abandonment and latency changes are small and not significant.

## Revenue per User (+3.1%, p = 0.004): treat as a lead, not a result
It is not a pre-registered primary. It is one of ~15 overall secondary metrics (and ~70 counting segment cuts), with no multiplicity correction in the experiment config. A Bonferroni correction over the 15 overall secondaries gives p ≈ 0.06. It is also hard to explain mechanically: clicks, CTR and ad click rate are all flat to slightly down. It is not a basis for launch. If the team cares, pre-register it and rerun.

## Other secondaries / segments
Nothing consistent. A few segment cuts are nominally significant (Mobile clicks/user +2.1%, Tail clicks/user +2.3%, Desktop time-to-first-click +3.6% worse), but that is roughly what chance gives across ~60 uncorrected segment tests, and segment SSR is flat everywhere. Not actionable.

## Test validity
- Two arms, 50/50, 1,000,000 users each (planned 900k/arm); exposure balance health check passed.
- Only `ranker_model` differs between arms (`snippet_length` is 160 in both), matching the pre-registered intended parameter.
- Audit log is empty: no mid-test config changes.
- Start 2026-09-12, 14-day plan; Pulse is dated 2026-09-25 and the experiment still shows "active". It looks like the planned duration was reached, so the result is a fixed-horizon read and no peeking was involved. Sequential testing was off, which is consistent with a single final read. CUPED was off; enabling it could tighten the CI but cannot rescue a point estimate this far from the bar.

## Recommendation
Don't launch v7 as a search-quality win. The experiment was well powered for the bar and the answer is "no effect of that size". If v7 has other merit (e.g. the revenue signal), it needs a new pre-registered test. Close this experiment.

**Caveat:** "No effect found" means no effect at the size we cared about; a true effect within ±0.14pp can't be excluded.
