Decision: Don't ship

# Ranker v7 – launch readout

**Bottom line:** v7 meets the primary bar, but it breaks the pre-registered Abandonment Rate guardrail. The breach is statistically clear, so we shouldn't ship as is.

## Setup (checked against prereg)
- Two-arm A/B on userID, 50/50 inside a 20% allocation. The only parameter that differs is `ranker_model` (v6 vs v7), as intended.
- Ran the planned 14 days (Pulse ds 2026-09-25). There are 1.0M users per arm against 0.9M planned. The exposure balance check passed.
- The audit log is empty, so the config wasn't changed mid-flight.
- Pulse was pulled without CUPED, at 95% CI, no sequential testing, no Bonferroni, as the prereg assumed. All intervals below are unadjusted.

## Primary: Successful Search Rate (bar +0.005, ship needs point estimate ≥ bar)
- 0.4120 → 0.4171, **+0.0051 abs (+1.24% rel)**, 95% CI ≈ [+0.0035, +0.0067], p < 0.001.
- The point estimate clears the pre-registered bar of 0.005, but only just. The CI lower bound is below the bar, so the true lift could be about 0.0035–0.0067.

## Guardrails (margins read as relative, see caveat)
| Metric | Change (rel) | 95% CI | Margin | Verdict |
|---|---|---|---|---|
| **Abandonment Rate** (lower is better) | **+2.2%** (0.187 → 0.1911, +0.0041 abs) | ≈ [+1.5%, +2.9%] | 1% | **Breached.** The whole CI is past the margin, p < 0.001. |
| Latency p95 | +0.2% (+0.8 ms) | ≈ [-0.3%, +0.7%] | 2% | OK |
| Zero Result Rate | 0.0% | ≈ ±1.4% | 3% | OK |
| Revenue per User | -0.1% | ≈ [-0.8%, +0.6%] | 1% | OK, but the CI is wide and can't exclude a loss close to the margin. |

Success rate is up while abandonment is also up, which is unusual. Related Pulse metrics show more clicks (CTR +1.9%, Clicks/User +2.1%), but no gain in Long Click Rate (-0.09%, p = 0.76), Reformulation (+0.5% in the wrong direction, ns) or Time to First Click (ns). One reading is that v7 produces more shallow clicks and more sessions with no engagement. That is a hypothesis and the data here don't test it.

## Segments (exploratory only)
There are 42 segment rows and none of them are pre-registered or multiplicity-corrected. A few cross p < 0.05 (Abandonment up in Head Queries, CTR and Clicks down in Tail Queries). At that count, a handful of such hits is expected by chance, so I'm not acting on any of them. The segment Successful Search Rate rows are all individually non-significant.

## Caveats
- **Margin units are not stated in the prereg.** I read them as relative. Absolute margins would be nonsensical for the other guardrails (a 0.02 ms latency margin, or a 0.03 Zero Result margin when the rate itself is 0.031). If someone intended an absolute 0.01 for Abandonment, the +0.0041 would pass. Please confirm with the prereg authors before the meeting.
- The primary lift is barely above the bar, so the guardrail breach isn't offset by a comfortable win.

## Recommendation
Don't ship v7 as configured. If the team wants to proceed, the next step is to find out why abandonment rose (for example, inspect which queries end without a click or long click) and re-test a fix. The alternative is an explicit, documented exception by the decision owners, which would be a call to override the prereg and not something this data supports.
