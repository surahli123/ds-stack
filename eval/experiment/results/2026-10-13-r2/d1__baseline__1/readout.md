Decision: Don't ship

# Ranker v7 – launch review readout

**Bottom line:** Ranker v7 improves Successful Search Rate (SSR), but the gain is below the pre-registered bar, and it breaks the latency guardrail. Both failures are independent reasons not to ship as is.

Source: Statsig Pulse (ds 2026-09-25, no CUPED, 95% CIs), 1,000,000 users per arm (plan: 900k). The test started 2026-09-12 and was planned for 14 days. The exposure balance check passed. The audit log is empty, so the config did not change mid-test. The only parameter that differs between arms is `ranker_model`, which is the intended change.

## Primary metric (pre-registered: SSR, ship requires the point estimate ≥ +0.005)
| | Control | Test | Abs. change | 95% CI | Rel. change |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | **+0.0033** | [+0.0017, +0.0050] | +0.81% (±0.4) |

- The effect is real (p = 7e-5).
- The point estimate (+0.0033) is below the +0.005 bar. The upper end of the CI (+0.00498) is also just under the bar.
- I read the bar as absolute, in the same units as the metric. The prereg does not say. If the bar were meant as +0.5% relative, the primary would pass (+0.81%). Even then, the guardrail below still blocks shipping. The team should confirm the unit.

## Guardrails (pre-registered margins)
| Guardrail | Change | 95% CI | Margin | Result |
|---|---|---|---|---|
| **Latency p95** | **+12.8 ms (+3.1%)** | +2.5% to +3.7% | ≤ 2% worse | **FAIL.** The whole CI is beyond the margin. |
| Abandonment Rate | +0.0002 (+0.1%) | ±0.0011 | 1% | Pass (inconclusive, but within margin) |
| Zero Result Rate | 0.0 | ±0.0004 | 3% | Pass |
| Revenue per User | −0.1% | ±0.7% | 1% | Pass (inconclusive, but within margin) |

Latency p95 is clearly worse, by roughly 2.5–3.7%, against an allowed 2%. Slower search also tends to erode engagement over a longer window.

## Secondary and exploratory metrics
- No secondary metric moved significantly in a good direction. CTR, Long Click Rate, Clicks per User and Queries per User are flat, with CIs spanning zero.
- The only nominal signal is Clicks per User – Informational, at −1.5% (p = 0.037). It sits among many segment cuts, none of them pre-registered, and I did not correct for multiple comparisons. Treat it as a hypothesis to check, not a finding. It is a mild caution because it points the opposite way from the SSR gain.
- Ignore any other single p < 0.05 among the many secondary metrics unless it is replicated.

## Recommendation
1. Don't ship v7 as configured.
2. Profile and fix the p95 latency regression, for example by trimming model cost or caching. Then re-test.
3. Re-test at a size that can resolve the SSR effect against the bar. The current CI straddles the bar only at its upper edge, so a true effect of 0.005 or more is unlikely but not excluded. If the real effect is about +0.003, ask whether that is worth shipping at all, and reset the bar if so.
4. Confirm the unit of the bar (absolute or relative) in the prereg.

Caveats: this is a single 14-day readout, and novelty or seasonality effects were not examined. No CUPED variance reduction was applied.
