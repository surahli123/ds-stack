Decision: Ship

# Ranker v7 – launch readout

**Design:** A/B on userID, Control (lambdamart_v6) vs Test (lambdamart_v7), 50/50, 1,000,000 users per arm. Only the intended parameter (`ranker_model`) differs; `snippet_length` is identical. Run 2026-09-12 to 09-25 (14 days, as planned). Pulse is non-CUPED, 95% CI, no sequential testing, so this is a single fixed-horizon read with no peeking correction needed. Exposure balance health check passed.

## Primary (pre-registered): Successful Search Rate
| | Control | Test | Abs. change | Rel. change (95% CI) | p |
|---|---|---|---|---|---|
| SSR | 41.20% | 41.53% | +0.334 pp | **+0.81% (±0.40%)** → [+0.41%, +1.21%] | 7e-5 |

Prereg rule: ship requires the **point estimate** to be at or above the bar of 0.005. Point estimate +0.81% relative is above 0.5%. Met.

**Unit assumption (please confirm in review):** prereg doesn't state units for `bar`. I read it as relative (0.5%), the same convention as the guardrail margins (e.g. latency 0.02 = 2%; an absolute 0.02 ms would be meaningless). If it was meant as an absolute 0.5 pp, the result (+0.33 pp) would miss the bar and the decision would change to Don't ship. Note also that the CI lower bound (+0.41%) is below 0.5%; the prereg rule only requires the point estimate, but the true lift could be a bit under the bar.

## Guardrails (non-inferiority, relative margins from prereg, using the CI's bad-side bound)
| Metric | Change (95% CI) | Worst-case bound | Margin | OK? |
|---|---|---|---|---|
| Latency p95 | +0.2% ± 0.5% | +0.7% | 2% | Yes |
| Abandonment Rate | +0.1% ± 0.6% | +0.7% | 1% | Yes |
| Zero Result Rate | 0.0% ± 1.4% | +1.4% | 3% | Yes |
| Revenue per User | −0.1% ± 0.7% | −0.8% | 1% | Yes |

All four guardrails are inside their margins, but Abandonment and Revenue have little headroom (0.3 and 0.2 pts).

## Caveats
- **Allocation was cut from 20% to 10% on 2026-09-16** (day 5; audit log). The arms stayed equal (1.0M each, balance check passed), so I see no bias, but users exposed before and after the change are mixed in one result. Worth a quick look at the daily lift before and after 09-16.
- **Pulse snapshot is dated 09-25** and the experiment still shows "active" today (10-12). Results are the 14-day read; nothing after that is included. Consider ending the experiment.
- Secondaries (CTR, long clicks, queries/sessions per user, etc.) show no significant movement either way; CTR is slightly negative (−0.29%, p=0.26), not significant. Segment cuts (mobile/desktop, head/tail, nav/info) are exploratory, about 50 metrics with no multiplicity correction, and none is significant at 5%. Desktop SSR is flat (−0.02%) and Navigational SSR is −0.27% (p=0.58); these are noise-level but worth monitoring post-launch.

## Recommendation
Ship Ranker v7, conditional on the bar being relative as assumed. Monitor Revenue per User and Abandonment after launch, since they have the thinnest margins.
