**Bottom line:** v7 did not move the primary metric, and it made CTR, abandonment and latency worse. The pre-registered ship criterion is not met. The data is readable enough to present, but the segment rows have problems the engineer should know about before someone asks.

## Scorecard (Pulse, no CUPED, 95% CI, 1.0M units per arm)

| Metric | Change | Reading |
|---|---|---|
| **Successful Search Rate (primary)** | 0.000, 95% CI ±0.0012 (0.412 base) | Flat. The CI upper bound (+0.12pp) is far below the pre-registered bar of +0.5pp, so this is a real null, not an underpowered one. |
| CTR | −0.46pp (−1.5%), p<0.001 | Significantly worse. |
| Abandonment Rate (guardrail) | +0.30pp (+1.6% ±0.4), p<0.001 | Significantly worse, but within the 3% margin, so the guardrail passes. |
| Latency p95 (guardrail) | +24.7ms (+6.0% ±0.8), p<0.001 | Significantly worse, but within the 10% margin, so the guardrail passes. |
| Long Click, Reformulation, Queries, Sessions, TTFC, Clicks, Revenue, Ads | All CIs include 0 | No evidence of movement. |
| Zero Result Rate | Exactly 0.0, p=1.0 | Expected, since a re-ranker shouldn't change retrieval. |

The prereg's primary metric fails ("ship requires point at bar"). The two guardrails pass only because they are inside their margins, and both are significantly in the wrong direction.

## Why the metrics moved

Only three metrics moved: CTR down, abandonment up, latency up. A plausible story is that v7 is a heavier model, so p95 latency rises by about 25ms. Slower results lead to more no-click exits and fewer clicks. The ranking quality itself is unchanged, which would explain why successful searches and long clicks are flat.

**This story is a hypothesis, not a finding.** The data shows the three metrics moving together, not that one caused the others. The engineer should say that.

Two weaker alternatives are worth naming:
- v7 reorders results so fewer clicks are needed (for example, better answers at the top), which would lower CTR without hurting success. That doesn't fit the abandonment increase.
- The abandonment rise could be partly "good abandonment" (the user got the answer from the snippet). The data can't separate this from bad abandonment.

## Things to flag before triage

1. **The segment rows are internally inconsistent. Don't present them as findings.**
   - Every Successful Search Rate segment delta is negative (−0.02pp to −0.35pp), yet the overall delta is exactly 0.000. Segments that partition the users can't all be negative while the total is zero.
   - Mobile (0.446) and Desktop (0.500) baselines are both above the overall 0.412, which is also impossible for a partition.
   - Every segment reports 1,000,000 units, the same as the overall count, so the segment definitions or denominators look wrong.
   - Check the segment metric definitions before anyone reads them.
2. **Multiple comparisons.** There are about 60 metric and segment rows at 95% with no Bonferroni correction. About three false positives are expected. Mobile SSR (p=0.053) and Desktop Long Click (p=0.033) are in that range, so don't build stories on them. CTR, abandonment and latency are strong enough (p<0.001) to survive correction.
3. **The daily view is thin.** The daily series covers only 12 of the 14 planned days, and it is flat with every day's CI spanning 0. There is no sign of a novelty effect or a ramping effect. It also can't rule one out for days 13–14.
4. **Sample size.** Each arm has 1.0M units against 900k planned. That's fine, and the exposure health check passed. The experiment status is still "active" and the audit log is empty, so no config changes explain anything.
5. **SSR is exactly 0.0.** The change is exactly 0.0 with p=1.0. That's plausible but unusual, so confirm the pipeline isn't returning a default.

## Deep-dive cuts to run, and what each should show

1. **Latency bucket × abandonment and CTR.** If the latency story is right, the damage concentrates in the slow tail and disappears among users whose latency didn't change. If abandonment is flat across latency buckets, the story is wrong.
2. **Device (mobile vs desktop) latency delta.** This should show whether mobile bears the p95 hit. The mobile SSR hint (−0.35pp) would only be worth a second look if the mobile latency penalty is much larger.
3. **Abandonment split: no-click exit vs no-click-then-reformulate.** If the extra abandonment is mostly quick exits, that points to latency or a worse top result. If it is dwell-then-exit, it points to good abandonment.
4. **CTR by click position.** A shift of clicks away from position 1 means worse top-result ranking. A uniform drop means a load or latency effect.
5. **Query type (head vs tail, navigational vs informational), once the segment definitions are fixed.** This would show whether v7 helps tail or informational queries and hurts head queries. At present this cut can't be trusted.
6. **Days 13–14 and a time-trend check.** This confirms the null holds through the full window.

## Recommendation

Do not ship v7 as is. The primary missed its bar with a tight CI, and the secondary metrics got worse. The most useful follow-up is a latency-optimized v7 and rerunning the latency cut.

Ready for triage: Ready, with open questions

The open questions are the unreliable segment metrics, the unconfirmed latency mechanism, and the missing last two days of the daily view.