Decision: Ship

# Ranker v7 – launch readout

**Recommendation:** Ship. The pre-registered primary clears its bar and all four pre-registered guardrails stay inside their margins. Two things need the room's attention: a latency regression and a CTR drop (below).

## Setup (matches prereg)
- A/B, unit = userID, 50/50 split inside 20% allocation, layer `search_ranking`. Only `ranker_model` differs (v6 vs v7); `snippet_length` is identical (160), so there are no confounding parameter changes.
- Run Sep 12 – Sep 25, 2026 (14 days, as planned). 1.0M units per arm (plan: 900k). Exposure balance check passed. Audit log has no mid-test changes.
- Fixed-horizon analysis, 95% CIs, no CUPED. The one primary was pre-registered, so no multiplicity adjustment is needed.

## Primary: Successful Search Rate (bar: +0.5%, point estimate must reach the bar)
| | Control | Test | Abs. change | Rel. change (95% CI) | p |
|---|---|---|---|---|---|
| Successful Search Rate | 41.20% | 41.53% | +0.33 pp | **+0.81% (±0.40 → +0.41% to +1.21%)** | 7e-5 |

The point estimate (+0.81%) is above the +0.5% bar. The CI lower bound (+0.41%) is below the bar, but the prereg rule is `point_at_bar`, so this passes. The lift is real (CI excludes 0), though its true size could be below the bar.

**Assumption to confirm:** the prereg doesn't state units for the bar or the margins. I read them as relative changes. The latency margin of 0.02 only makes sense as 2%, and I applied the same reading to the bar. If the bar were meant as an absolute +0.5 pp, the result (+0.33 pp, CI upper bound +0.50 pp) would fail it and the decision would flip to Don't ship. Please confirm this reading in the review.

## Guardrails (worst end of the 95% CI vs. prereg margin, relative)
| Guardrail | Change (95% CI) | Margin | Status |
|---|---|---|---|
| Latency p95 | +1.2% worse (+0.7% to +1.7%) | 2% | Within margin, but significantly worse (p=3e-6) |
| Abandonment Rate | +0.1% worse (±0.6) | 1% | Pass |
| Zero Result Rate | 0.0% (±1.4) | 3% | Pass |
| Revenue per User | −0.1% (±0.7; worst −0.8%) | 1% | Pass |

## Things to flag
- **Latency:** p95 is up about 5 ms (412 → 417 ms). The effect is statistically certain. It is inside the agreed tolerance, but the upper CI is 1.7% against a 2% margin, so there is little headroom. Suggest tracking it after launch.
- **CTR (secondary, not pre-registered):** −0.71% (p=0.005), while Successful Search Rate rose. This is consistent with fewer wasted clicks, and Long Click Rate (−0.27%, p=0.37) and Abandonment are flat. But it is a significant move in a metric people care about. Treat it as an explanation to monitor, not as evidence against shipping.
- The remaining secondaries (queries, sessions, reformulation, time to first click, ads, clicks) show no significant change. I did not mine the roughly 45 segment metrics for effects. With that many looks, a stray significant segment would be expected by chance.

## Caveats
- The lower end of the primary effect (+0.41%) is under the bar, so the realized lift may be smaller than the point estimate suggests.
- Two weeks covers weekly cycles, but novelty effects were not checked.
