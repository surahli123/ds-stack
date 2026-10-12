Decision: Ship

# Ranker v7 – launch readout

**Design check.** A/B on userID, Control (lambdamart_v6) vs Test (lambdamart_v7), 50/50 within a 20% allocation. Ran 2026-09-12 to 09-26 (14 days, as planned). Pulse is for ds 2026-09-25, the last full day. Each arm has 1,000,000 units, above the planned 900k. The exposure-balance health check passed. The audit log is empty, so nothing changed mid-flight. The only parameter that differs between arms is `ranker_model`, the intended one (`snippet_length` is 160 in both). Pulse was pulled with CUPED off, 95% CIs, no sequential testing and no Bonferroni correction, so the numbers below are plain fixed-horizon results.

**Primary (pre-registered): Successful Search Rate, bar +0.005, ship rule "point estimate at or above the bar".**
| | Control | Test | Abs. diff | Relative | 95% CI (relative) | p |
|---|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | +0.0033 | **+0.81%** | +0.41% to +1.21% | 7e-5 |

The lift is clearly real. The point estimate (+0.81%) is above the +0.5% bar.

**Guardrails (pre-registered margins, read as relative, harm side of the 95% CI):**
| Metric | Change | Worst end of CI | Margin | OK? |
|---|---|---|---|---|
| Latency p95 | +0.2% (+0.8 ms) | +0.7% | 2% | yes |
| Abandonment Rate | +0.1% | +0.7% | 1% | yes |
| Zero Result Rate | 0.0% | +1.4% | 3% | yes |
| Revenue per User | -0.1% | -0.8% | 1% | yes |

All four guardrails stay inside their margins, even at the unfavorable edge of the CI.

**Caveats**
- **Bar units are my interpretation.** prereg.json gives `bar: 0.005` without units. I read it as relative (+0.5%), because the guardrail margins in the same file (e.g. 0.02 on latency p95 in ms) only make sense as relative. If the team meant +0.005 absolute (about +1.2% relative), the point estimate (+0.0033) misses the bar and the call would be Don't ship. Please confirm this at the review.
- **The lower CI bound (+0.41%) is below the bar.** The preregistered rule uses the point estimate, so it passes. The true lift could still be somewhat under 0.5%.
- **Reformulation Rate is worse** (+0.96% relative, p=0.018; lower is better). It isn't a pre-registered primary or guardrail. Of the 60+ secondary and segment metrics with no multiplicity correction, a few p<0.05 hits are expected by chance. Even so, it is the one signal that points the wrong way and it is worth watching after launch. Long Click Rate is also slightly down (-0.55%, p=0.074, not significant).
- **Segment results are exploratory.** Mobile, desktop, head/tail and navigational/informational cuts for Successful Search Rate are all non-significant and point mostly positive, except Head Queries (-0.64%, p=0.16, not significant). The only individually significant segment result, Long Click Rate on Desktop (+1.75%, p=0.006), is not something to act on given how many cuts there are.
- **CTR, Clicks per User and Sessions per User** are flat. Sessions per User is +0.5% (p=0.058, not significant).

**Recommendation:** Ship, after confirming the bar units. Monitor Reformulation Rate and Long Click Rate post-launch, ideally with a holdback.
