Decision: Don't ship

# Ranker v7 – launch review readout

**Bottom line.** Ranker v7 produced a real but small lift in Successful Search Rate (SSR). That lift is well below the +0.005 bar the team pre-registered as the requirement to ship. No guardrail is harmed. By the pre-registered rule (`ship_requires: point_at_bar`), this does not ship.

## Primary metric: Successful Search Rate (95% CI, no CUPED, fixed-horizon)
| | Control | Test | Abs. change | 95% CI | Rel. change | p |
|---|---|---|---|---|---|---|
| SSR | 0.4120 | 0.4133 | **+0.00128** | [+0.00054, +0.00202] | +0.31% (CI ±0.18%) | 0.0007 |

- The effect is statistically distinguishable from zero.
- The point estimate (+0.0013) is about a quarter of the bar (+0.005). The bar reads the same way either as an absolute change or as a 0.5% relative change: the point is 0.31% relative, and the CI upper end is about 0.49% relative.
- The upper end of the CI (+0.0020) is also below the bar. The data rule out reaching the bar, not just the point estimate missing it.

## Guardrails (pre-registered margins)
I read each margin as relative to control. The conclusion is the same if a margin is meant as an absolute change. Each guardrail is judged on the CI's worse end.

| Metric | Change | 95% CI worse end vs. margin | OK? |
|---|---|---|---|
| Latency p95 | +0.82 ms (+0.2%) | +2.9 ms ≈ +0.7% vs 2% | Yes |
| Abandonment Rate | +0.00019 | +0.0013 ≈ +0.7% rel. vs 1% | Yes |
| Zero Result Rate | 0.0000 | +0.00043 ≈ +1.4% rel. vs 3% | Yes |
| Revenue per User | −$0.0009 (−0.1%) | −$0.0070 ≈ −0.8% vs −1% | Yes, but the lower end of the CI is close to the margin |

## Validity checks
- Design: a 50/50 A/B on userID, run fixed-horizon (no sequential testing), so the 95% CI is valid at the one look.
- Exposure: 1,000,000 units per arm, above the 900,000 planned. The balanced-exposure health check passed.
- Duration: the config start is 2026-09-12 and the pulse date is 2026-09-25, which is the planned 14 days. The audit log is empty, so the config was not changed mid-run.
- Parameters: the only difference between arms is `ranker_model` (v6 vs v7), as intended. `snippet_length` is identical.
- The pulse is dated 2026-09-25, and the experiment still shows "active" on 2026-10-12. Nothing here is based on later data. If the experiment has kept running, the extra data has not been analysed.

## Secondary and segment metrics (descriptive only)
- No secondary metric shows a meaningful move. CTR, Long Click Rate, Reformulation Rate, Queries per User and Time to First Click are all well within noise.
- SSR by segment (mobile, desktop, head, tail, navigational, informational) shows no significant difference. Mobile and head queries lean slightly negative, desktop slightly positive, and all of these CIs include zero.
- One segment-level result, CTR on navigational queries (−0.0048, p=0.023), is nominally significant. It is one of about 60 unplanned segment cuts, which is what chance alone would produce. I treat it as noise, not a finding. It could be worth a look if anyone revisits this.

## Recommendation
- **Don't ship v7 on this evidence.** It does not clear the pre-registered bar, and the CI says it will not clear it with more data at this effect size.
- If the team thinks a +0.1–0.2pp SSR gain is worth having at neutral guardrails, that is a new decision. It would mean explicitly changing the bar. That should be argued on its merits, not by reading this result as a pass. Moving the bar after seeing the data is exactly what the pre-registration is meant to prevent.
- The more useful next step is to find out why a model change moved SSR so little, and what a larger change would look like.
