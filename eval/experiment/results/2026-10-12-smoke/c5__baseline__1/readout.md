Decision: Don't ship

# Ranker v7 – launch review readout

**Bottom line:** v7 improves Successful Search Rate (SSR), but by less than the pre-registered ship bar. Under the pre-reg rule (`ship_requires: point_at_bar`), the point estimate must reach +0.5 pp. It is +0.33 pp, so we don't ship as specified.

## Primary metric (pre-registered, single primary)
| | Control | Test | Abs. diff | 95% CI | Rel. | p |
|---|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | **+0.334 pp** | [+0.169, +0.499] pp | +0.81% | 7e-5 |

- The effect is real: the CI excludes 0 and p is far below 0.05. No multiplicity issue, since there is one primary.
- The bar is +0.500 pp. The point estimate misses it by about a third, and even the CI upper bound (+0.499 pp) sits just under the bar. This is not a "needs more data" case. More data would narrow the CI around about +0.33 pp, not move it to +0.5.

## Guardrails (pre-registered margins)
All four are inside their margins, and each CI's worse bound stays within the margin (margins read as relative).

| Guardrail | Change (95% CI half-width) | Margin | Verdict |
|---|---|---|---|
| Latency p95 | +0.2% (±0.5%) | 2% | OK |
| Abandonment Rate | +0.1% (±0.6%) | 1% | OK |
| Zero Result Rate | 0.0% (±1.4%) | 3% | OK |
| Revenue per User | −0.1% (±0.7%) | 1% | OK |

Guardrails are not what blocks this. The primary shortfall is.

## Secondary and segment metrics
No secondary metric (CTR, long clicks, reformulation, time to first click, etc.) is significant at 95%. I also looked at about 40 device and query-type cuts. There are no significant movers. The nearest to the line are Long Click Rate – Tail (p=0.069, negative), Reformulation – Desktop (p=0.070, favorable), and Time to First Click – Desktop (p=0.053, favorable). At this many cuts that is what noise looks like. Treat them as exploratory only; they don't change the decision. SSR segment effects are directionally mixed: Mobile and Tail are positive, Navigational, Informational and Desktop are about 0 or negative. None is distinguishable from the overall effect.

## Validity checks and caveats
- Design is a clean A/B on userID: 50/50 split, 1.0M units per arm (plan was 900k). The exposure-balance health check passed. Pulse is dated 2026-09-25, day 14 of 14, so the planned duration is complete.
- **Allocation was cut from 20% to 10% on 2026-09-16 (4 days in).** This is not in the pre-reg. Because both arms keep a 50/50 split and exposures are balanced, it should not bias the comparison. I can't verify from these files how users were handled when the allocation shrank (dropped or retained), or whether the effect varies by day. The review should be told this happened. If someone wants to argue for shipping anyway, this needs a by-day check first.
- Pulse was run without CUPED (as requested). A CUPED run would likely tighten the CI but would not change the point estimate, which is what the pre-reg bar uses.
- Sequential testing and Bonferroni are off, which is fine for a single fixed-horizon primary.

## Recommendation
- Don't ship v7 as specified. It misses the pre-registered bar.
- If the team thinks +0.33 pp is worth shipping anyway (guardrails are clean and the lift is statistically solid), that is a decision to change the bar, and it should be made explicitly by the owners. I'm not making that call in this readout, and a post-hoc lowering of the bar after seeing results should be flagged as such.
- Otherwise, iterate on the ranker. The lift appears to be about 2/3 of what the team hoped for.
