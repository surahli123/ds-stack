Decision: No effect found

# Ranker v7: launch review readout

## Bottom line
Ranker v7 did not move the pre-registered primary metric, and the data rule out an effect as large as the one we needed. Do not ship on this evidence. The one encouraging signal, Tail Queries, was not pre-registered. It is a lead for a follow-up test and not grounds to ship.

## Primary metric (pre-registered)
Successful Search Rate (SSR), 95% CI, no CUPED, about 1.0M users per arm:
- Control 0.4120, Test 0.41225. The absolute change is **+0.00025** (+0.06% relative), with a CI of **[-0.0010, +0.0015]** and p = 0.70.
- The pre-registered ship bar is +0.005 (0.5 pp) at the point estimate. The point estimate is 20 times too small. The CI's upper end (+0.0015) is also well below the bar, so this is a precise null. It does not just reflect low power.
- The test was adequately sized: 1.0M users per arm against 900k planned.

## Guardrails (pre-registered margins)
The worst-case end of each 95% CI stays inside its margin. I read the margins as relative.

| Guardrail | Change | Worst-case CI bound | Margin | OK |
|---|---|---|---|---|
| Latency p95 | +0.82 ms (+0.2%) | about +0.7% | 2% | yes |
| Abandonment Rate | +0.1% | about +0.7% | 1% | yes |
| Zero Result Rate | 0.0% | about +1.4% | 3% | yes |
| Revenue per User | -0.1% | about -0.8% | -1% | yes |

No guardrail was harmed. Nothing here argues against v7. It just doesn't show a benefit.

## Experiment health
- Exposures are balanced (health check passed). The unit is userID and the split is 50/50 within a 20% allocation.
- Only `ranker_model` differs between arms (`snippet_length` is 160 in both), which matches the intended params.
- The audit log is empty, so there were no mid-test config changes.
- Pulse data is dated 2026-09-25. The test started 2026-09-12 with a 14-day plan, so it covers the planned window.
- The experiment still shows `status: active` today (2026-10-12). It should be stopped or decided.
- Sequential testing and multiple-comparison correction are off. That is fine for one primary metric, but it matters for the slices below.

## Secondary and slice metrics (exploratory)
- Of about 55 secondary and slice metrics, most are flat, as expected from a null primary.
- **SSR - Tail Queries: +1.46 pp (0.4705 to 0.4851), p < 0.001.** It is the only slice that would survive a Bonferroni correction across roughly 35 slices. All other SSR slices are within noise: Head +0.05 pp, Navigational +0.04 pp, Informational -0.07 pp, Mobile +0.12 pp, Desktop +0.32 pp, none significant.
- This was not pre-registered and was found by slicing after the fact. Tail traffic is evidently a small share of searches, which is why overall SSR doesn't move. Related tail metrics are directionally positive but not significant (CTR - Tail +0.17 pp, Clicks per User - Tail p = 0.09).
- CTR - Navigational is -0.55 pp (p = 0.027). With about 55 comparisons, one or two p < 0.05 results are expected by chance. I treat it as noise, but it is worth watching in any follow-up.
- Overall CTR is +0.15 pp (p = 0.052, not significant) and does not offset the null SSR result.

## Recommendation
1. Don't ship Ranker v7 as a general launch. It misses the pre-registered bar and the data exclude the effect size we needed.
2. Stop the experiment, since it is past its planned window.
3. If the team wants to pursue the tail-query gain, pre-register it. Options are a tail-targeted rollout or a new test with tail SSR as the primary, sized for a roughly 1.5 pp effect on that population. Confirm the tail definition and its share of traffic first.

## Caveats
- The guardrail margins are assumed to be relative; the pre-registration doesn't say.
- Results come from a single Pulse snapshot without CUPED. CUPED would tighten the CIs but is unlikely to change the conclusion given the gap to the bar.
