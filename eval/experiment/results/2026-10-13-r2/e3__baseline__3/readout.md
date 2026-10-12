Decision: Don't ship

# Ranker v7 – launch review readout

**Bottom line:** Ranker v7 improves Successful Search Rate (SSR), but by about a quarter of the lift the pre-registration required. Even the optimistic end of the CI is well short of the bar. Guardrails are clean, so v7 isn't harmful. It just doesn't clear the ship criterion we set before launch.

## Primary metric (pre-registered: SSR, ship requires point estimate ≥ +0.005 at 95% CI)
| | Control | Test | Abs. diff | 95% CI | Rel. | p |
|---|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4133 | **+0.00128** | [+0.00054, +0.00202] | +0.31% | 0.0007 |

- The lift is real: the CI excludes zero.
- It is far below the bar. The point estimate is 0.0013 against 0.005 required. The CI upper bound (0.0020) is also below 0.005, so this isn't an underpowered near-miss. The data rule out a lift of the required size.
- The conclusion doesn't depend on whether the bar is read as absolute (0.005) or relative (0.5%). The observed +0.31% relative also misses a 0.5% relative bar.

## Guardrails (pre-registered margins; 95% CIs, no CUPED)
| Metric | Change (rel.) | 95% CI half-width | Margin | Verdict |
|---|---|---|---|---|
| Latency p95 | +0.2% (worse) | ±0.5% | 2% | OK (worst case +0.7%) |
| Abandonment Rate | +0.1% (worse) | ±0.6% | 1% | OK (worst case +0.7%) |
| Zero Result Rate | 0.0% | ±1.4% | 3% | OK |
| Revenue per User | −0.1% | ±0.7% | 1% | OK (worst case −0.8%) |

All four guardrails are inside their margins. Abandonment and revenue have the thinnest room (worst case 0.7% and 0.8% against a 1% margin).

## Secondary metrics
None of the ~30 secondary and segment metrics (CTR, long clicks, reformulation, queries, clicks, time to first click, device and query-type cuts) show a significant movement. I didn't treat these as evidence either way. There are many of them, and none are pre-registered as decision metrics.

## Experiment validity
- Design is a standard 50/50 A/B test on userID. The exposure-balance health check passed.
- Pulse covers 1.0M units per arm against 0.9M planned. The test ran the planned 14 days (2026-09-12 to 09-25 complete days).
- The audit log is empty, so there were no mid-test config changes. Only the pre-registered parameter (`ranker_model`) differs between arms. `snippet_length` is identical (160).
- Sequential testing and multiplicity corrections are off. That's fine for a single pre-registered primary read once at the planned end.
- Results are un-CUPED, as requested. CUPED would tighten the CIs but can't plausibly move the point estimate from 0.0013 to 0.005.

## Recommendation
Don't ship v7 as specified. If the team believes a ~0.1-pp SSR gain is worth shipping on cost or maintenance grounds, that is a change to the pre-registered bar. It should be argued as an explicit, documented decision by the review, not read as a pass. Whether to iterate on the ranker toward a larger lift is a product call.

## Caveats
- The bar's units (absolute vs relative) aren't stated in the pre-reg. The conclusion holds under both readings.
- A single 14-day window may not capture novelty or long-run learning effects.
