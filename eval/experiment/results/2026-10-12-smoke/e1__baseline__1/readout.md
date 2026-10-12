Decision: Escalate

# Ranker v7: launch readout

**Summary.** v7 clears the pre-registered primary bar, but the Abandonment Rate guardrail is not cleared. Its point estimate is worse (higher) than control, and the CI reaches past the pre-registered margin. I can't call this a clean ship or a clean no-ship. The launch owners need to decide whether to accept that risk.

## Setup (checked)
- Clean 50/50 A/B on userID, layer `search_ranking`. The only differing parameter is `ranker_model` (lambdamart_v6 vs v7), which is the intended one. `snippet_length` is the same in both arms.
- Pulse snapshot is 2026-09-25, 14 days after the 2026-09-12 start, which matches the planned 14 days. There are 1.0M units per arm against 900k planned. The exposure balance health check passed. The audit log is empty, so no mid-test config changes.
- Pulse was requested without CUPED at 95% CI. There's no sequential testing and no multiplicity correction. There is one pre-registered primary, so no correction is needed for it.
- Assumption: prereg `bar` and `margin` are relative changes. The guardrail margins only make sense that way (for example, 0.02 on latency in ms, 0.03 on a 3.1% zero-result rate). If the bar were absolute (+0.5pp), v7 would miss it: the +0.33pp point estimate is below it. Please confirm the unit with the prereg author.

## Primary: Successful Search Rate
| | Control | Test | Abs. change | Rel. change (95% CI) | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | +0.33pp (±0.16pp) | **+0.81% (±0.40%)**, so about +0.41% to +1.21% | 7e-5 |

- The result is statistically clear. The prereg rule is `point_at_bar`, and the point estimate of +0.81% is above the +0.5% bar, so the primary criterion is met.
- The CI's lower end (+0.41%) is below the bar. The true lift could be a bit under the bar, but the prereg did not require the CI to clear it.

## Guardrails (relative change vs prereg margin, harm direction)
| Metric | Rel. change (95% CI) | Margin | Status |
|---|---|---|---|
| Latency p95 | +0.2% (±0.5%), worst case +0.7% | 2% | OK |
| Zero Result Rate | 0.0% (±1.4%) | 3% | OK |
| Revenue per User | -0.1% (±0.7%), worst case -0.8% | 1% | OK |
| **Abandonment Rate** | **+0.6% (±1.0%), worst case +1.6%** | 1% | **Not cleared** |

- Abandonment is 0.187 in control and 0.188 in test. The increase is not significant (p=0.24), but the CI cannot rule out a relative increase above the 1% margin.
- Treat it as unresolved, not as harm and not as safe. It also sits oddly beside the primary win, since better success would normally go with lower abandonment.
- Related metrics don't show a coherent harm signal. Reformulation Rate rose slightly (+0.65%, p=0.11, wrong direction) and Long Click Rate was flat (p=0.84). Neither is significant.

## Other metrics and segments
- All other secondary metrics (CTR, Queries, Sessions, Clicks, Time to First Click, Ad Click Rate, Pagination, Autocomplete) are not significant.
- The segment cuts (mobile/desktop, head/tail, navigational/informational) are exploratory and unadjusted for multiplicity. The primary has no clear segment story: Mobile -0.7% and Informational -0.9% have CIs spanning zero, with widths about ±1%. I would not act on them, but they are worth a look if the ranker rolls out.

## Recommendation for the review
1. Decide whether a possible abandonment increase of up to about 1.6% (relative) is acceptable for a +0.8% gain in successful searches. If the owners would not accept it, this becomes "Don't ship" or a v7 revision.
2. The planned 14 days are complete, so extending would only be a tool to narrow the abandonment CI. It would need an explicit decision, and the prereg did not plan for it.
3. If shipping, use a staged rollout with abandonment monitored against the 1% margin, and confirm the bar's unit first.
