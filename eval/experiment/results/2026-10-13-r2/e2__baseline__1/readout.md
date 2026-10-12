Decision: Ship

# Ranker v7 – launch readout

**Bottom line:** Ranker v7 meets the pre-registered ship rule. The primary metric rose by more than the bar, and every pre-registered guardrail stays inside its margin. There are two things the review should know about: a small but real latency regression, and a CTR drop.

## Design and validity
- Design is a plain A/B test (lambdamart_v6 vs v7, with snippet_length held at 160 in both arms). It is randomized by userID at 50/50 inside 20% allocation.
- Pulse data is dated 2026-09-25. The test started 2026-09-12 and was planned for 14 days, so the window is complete. Fixed-horizon analysis, no sequential testing, 95% CI, no CUPED. That matches the request.
- 1,000,000 units per arm, against 900,000 planned. The exposure balance health check passed. The audit log shows no mid-flight changes.

## Primary (pre-registered: Successful Search Rate, ship if point estimate ≥ bar of 0.005)
| | Control | Test | Abs. change | Rel. change (95% CI) | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | +0.0033 | +0.81% (≈ +0.41% to +1.21%) | 7e-5 |

- **Reading of the bar:** I read the bar of 0.005 as a relative lift of 0.5%. The prereg guardrail margins can only be relative (a 0.02 margin on a latency of about 412 ms is meaningless in absolute terms). The point estimate of +0.81% clears 0.5%.
- **If the bar was meant as absolute (+0.005 points):** the point estimate of +0.0033 would miss it, and the call would flip to Don't ship. Please confirm the unit with the prereg authors in the room.
- The CI lower bound (+0.41%) is below the bar. The prereg rule only asks the point estimate to reach the bar, so this doesn't block shipping. The true lift could be somewhat under 0.5%.

## Guardrails (relative change, 95% CI; the harmful side of the CI must stay inside the margin)
| Guardrail | Change (CI) | Margin | Status |
|---|---|---|---|
| Latency p95 | +1.2% (+0.7% to +1.7%) | 2% | Within margin, but a significant regression (412 → 417 ms, p=3e-6) |
| Abandonment Rate | +0.1% (−0.5% to +0.7%) | 1% | Within margin |
| Zero Result Rate | 0.0% (±1.4%) | 3% | Within margin |
| Revenue per User | −0.1% (−0.8% to +0.6%) | 1% | Within margin |

The latency upper bound of +1.7% leaves little room under the 2% margin. Watch it after launch.

## Things to flag
- **CTR fell 0.71%** (p=0.005), while successful searches rose. CTR was not pre-registered as a guardrail. A plausible reading is fewer wasted clicks per successful search, but that is a guess. Long Click Rate (−0.27%, n.s.) does not show quality loss. Worth a follow-up look.
- **Segment cuts** (device, head/tail/nav/info queries) are exploratory, with dozens of metrics and no multiplicity correction. A few nominal hits (for example Head-query Long Click Rate up, Tail-query Time to First Click down, Head-query abandonment down) are about what chance produces across that many tests. No segment shows a significant primary-metric change in either direction. I would not act on these.
- Other secondary metrics are flat (Queries per User, Sessions per User, Ad Click Rate, and others).

## Recommendation
Ship, with a post-launch watch on p95 latency and CTR, and with confirmation that the bar of 0.005 is a relative threshold.
