Decision: Don't ship

# Ranker v7 – launch review readout

**Bottom line:** Ranker v7 lowered the pre-registered primary metric, Successful Search Rate (SSR), and the drop is statistically significant. It missed the ship bar by a wide margin. Don't ship. Stop the experiment, which is still marked "active" in Statsig.

## Primary metric (pre-registered; ship requires the point estimate to reach +0.005)
| | Control (lambdamart_v6) | Test (lambdamart_v7) | Diff | 95% CI | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4094 | **-0.26 pp** (-0.62% rel.) | [-0.42 pp, -0.09 pp] | 0.0024 |

- The bar is +0.005, read as +0.5 pp absolute. The point estimate is -0.0026. Even the top of the CI (-0.09 pp) is below zero, so the data do not fit a small gain. The result is also well short of the bar if it was meant as +0.5% relative.
- The effect is a harm, not just a null.

## Guardrails (95% CI against the pre-registered margins)
All four guardrails are within margin. That does not change the decision, because the primary fails.
- Latency p95: +0.2% (CI about ±0.5%). Margin 2%. OK.
- Abandonment Rate: +0.1% (CI about ±0.6%). Margin 1%. OK.
- Zero Result Rate: 0.0% (CI about ±1.4%). Margin 3%. OK.
- Revenue per User: -0.1% (CI about ±0.7%). The worst case is about -0.8%, inside the -1% margin. OK, but it is not strongly ruled out.

## Validity
- Design is a clean A/B on userID. The 50/50 split has 1.0M users per arm, above the 0.9M planned. The exposure-balance health check passed.
- The test ran the planned 14 days (2026-09-12 to 09-25). Sequential testing is off and the analysis is fixed-horizon, so there is no peeking problem.
- The audit log is empty, so there were no mid-test config changes.
- The only parameter that differs between arms is `ranker_model`, as intended. `snippet_length` is 160 in both arms.
- The pulse is unadjusted: CUPED is off and there is no multiplicity correction. That is fine for a single pre-registered primary.

## Secondary and segment results (exploratory only)
- CTR, Long Click Rate, Autocomplete Acceptance and the other secondaries all lean slightly negative or are flat. None is significant on its own.
- I scanned about 50 segment metrics (device, head/tail, navigational/informational) with no correction. Two are nominally significant, both CTR decreases: Head queries -1.5% (p=0.003) and Informational -1.3% (p=0.038). With that many looks, expect a few by chance. Don't treat them as findings, but they agree in direction with the primary.
- SSR by segment is not significant anywhere. Mobile, Head and Navigational point positive, and Desktop points negative. All the intervals are wide and include zero. This is not enough to justify shipping to a subset, and no subset was pre-registered.

## Recommendation
1. Don't ship v7 as is.
2. End the experiment in Statsig. It is still "active" more than two weeks after the last pulse date (2026-09-25).
3. If the team still wants the v7 model, diagnose why SSR fell, starting with head and informational queries where CTR is weakest, before a new pre-registered test.
