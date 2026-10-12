Decision: Don't ship

# Ranker v7 readout

**Bottom line:** Ranker v7 produces a real but small lift in Successful Search Rate (SSR). The lift is well below the pre-registered ship bar, and the 95% CI rules out reaching the bar. Guardrails are clean, so v7 is not harmful. It just doesn't deliver enough to ship under the pre-registered rule.

## Primary metric (pre-registered): Successful Search Rate
| | Value |
|---|---|
| Control / Test | 0.4120 / 0.4133 |
| Absolute change | **+0.00128** (+0.13 pp), 95% CI [+0.00054, +0.00202] |
| Relative change | +0.31% (CI about ±0.18%) |
| p-value | 0.0007 |
| Pre-registered bar | +0.005 (point estimate must reach the bar) |

- The effect is statistically significant, but the point estimate is about a quarter of the bar.
- The upper CI end (+0.0020) is also below +0.005, so the bar is excluded, not just missed. If the bar was meant as relative, +0.31% is still below 0.5%, and the upper CI end of about 0.49% is also below it.
- The pre-reg rule is "ship_requires: point_at_bar", so this fails.

## Guardrails (pre-registered margins, 95% CI)
All pass. None has a CI reaching its margin.
- Latency p95: +0.8 ms (+0.2%), CI ±2.1 ms. The worst case is about +0.7% against a 2% margin.
- Abandonment Rate: +0.0002 absolute, CI ±0.0011. This is inside the 1% margin.
- Zero Result Rate: 0.0000, CI ±0.0004. This is inside the 3% margin.
- Revenue per User: −0.0009 (−0.1%), CI ±0.0061. The worst case is about −0.8% against a 1% margin, which is close to the margin but inside it. Revenue is not shown to be harmed, but the data can't rule out a loss of nearly 1%.

## Validity checks
- The design is a 50/50 A/B test on userID. The exposure-balance health check passed.
- There are 1.0M units per arm against 900k planned, and the run covers the full 14 days (2026-09-12 to 2026-09-25 data). The sample is adequate, and the experiment config matches the pre-reg's `ranker_model` parameter. `snippet_length` is identical across arms (160).
- The audit log is empty, so there were no mid-test config changes.
- The analysis is not CUPED-adjusted (as requested), with no sequential testing and no multiplicity correction. Only one primary metric was pre-registered, so none is needed for it.

## Secondary and segment metrics (exploratory, not decision-driving)
- About 50 secondary and segment metrics were tested without correction. Nearly all are null.
- The only nominal hit is CTR on Navigational queries: −0.0048, p=0.023. At this many tests, about 2 or 3 false positives are expected by chance. It is not a pre-registered guardrail, and SSR on navigational queries is flat (p=0.97). Treat it as a hypothesis to check, not a finding.
- SSR by segment is directionally mixed (Desktop +0.0018, Mobile −0.0012, Head −0.0036), all with p>0.17. There is no evidence of heterogeneity.

## Recommendation
Don't ship v7 as is under the pre-registered criterion. v7 is safe and slightly positive, so the team can reasonably decide whether a +0.13 pp SSR gain is worth shipping on other grounds. That would be a deliberate exception to the pre-registered bar, not a result of this test. Extending the run would not change the conclusion, since the CI already excludes the bar.
