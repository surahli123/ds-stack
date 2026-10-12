Decision: Escalate

# Ranker v7 launch readout

**Bottom line.** The Test arm clears the pre-registered primary bar and no guardrail is hurt. But Test differs from Control in two parameters, and the pre-registration only covers one. The measured lift belongs to the bundle (new ranker + longer snippets), not to the ranker alone. Whether to ship the bundle as tested is a call for the owners, not for the data.

## Primary: Successful Search Rate
| | Control | Test | Abs. change | Relative | 95% CI (relative) | p |
|---|---|---|---|---|---|---|
| SSR | 0.4120 | 0.4153 | +0.334 pp | +0.81% | +0.41% to +1.21% | 7e-5 |

- Pre-registered bar: 0.005, rule "point estimate at or above the bar". I read the bar as relative (+0.5%), the same convention as the guardrail margins. For example, the Zero Result margin of 0.03 only makes sense relative to a base rate of 0.031. On that reading, +0.81% passes.
- **The reading matters.** If 0.005 means 0.5 pp absolute, the point estimate (+0.33 pp, CI +0.17 to +0.50 pp) misses the bar and this would be "Don't ship". The pre-registration doesn't state the unit, so the owners need to confirm it.
- The CI lower bound (+0.41%) is below the bar even on the relative reading. The pre-registered rule only needs the point estimate, but the true lift could be smaller than the bar.

## Guardrails (all within pre-registered margin, relative change, 95% CI)
| Metric | Change | CI half-width | Margin | OK? |
|---|---|---|---|---|
| Latency p95 | +0.2% | ±0.5% | 2% | yes |
| Abandonment Rate | +0.1% | ±0.6% | 1% | yes |
| Zero Result Rate | 0.0% | ±1.4% | 3% | yes |
| Revenue per User | -0.1% | ±0.7% | 1% | yes |

The Zero Result CI (±1.4%) is wide relative to its 3% margin but still inside it. No guardrail shows harm.

## Issue: unplanned second change in the Test arm
`experiment.json` shows Test = `ranker_model: lambdamart_v7` **and `snippet_length: 220`** (Control: `lambdamart_v6`, 160). The pre-registration lists only `ranker_model` as an intended parameter. The audit log is empty, so there is no record of who changed snippet length, when, or why. Longer snippets could plausibly affect click and success behaviour on their own. This experiment can't separate the two effects.

## Other checks
- Design: 50/50 A/B on userID, exposure balance check passed, 1.0M units per arm (plan was 0.9M).
- Duration: started 2026-09-12, 14 days planned, pulse date 2026-09-25. The planned window is complete.
- Pulse was requested with CUPED off and 95% CI, matching the pre-registration. Sequential testing and Bonferroni are off, which is fine for a single primary.
- Secondary metrics: no significant movement in either direction after reading ~20 top-level metrics. Time to First Click is slightly worse (+0.9%, p=0.08), not significant and not a guardrail.
- Segments (exploratory, not pre-registered, no multiplicity correction): Tail Queries SSR +0.93% (p=0.015) and Mobile CTR (p=0.013) are nominally significant. Desktop SSR is -0.66% (p=0.11, n.s.). With ~40 segment cuts a couple of p<0.05 results are expected by chance, so I would not act on any of these. The Desktop sign is worth a look, but it is not evidence of harm.

## What I need from the review
1. Confirm that the bar of 0.005 is relative. If it is absolute, the answer flips to Don't ship.
2. Find out who set `snippet_length` to 220 and whether it was intended.
3. Choose one of:
   - **Ship the bundle exactly as tested** (v7 + 220), accepting that the lift can't be credited to the ranker. This is supported by the data if item 1 is relative.
   - **Rerun with snippet_length held at 160**, if the ranker must be shipped or evaluated on its own. This is the cleaner option if there is time.
