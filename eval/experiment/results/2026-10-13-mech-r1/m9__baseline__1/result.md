**Bottom line:** Ranker v7 did nothing measurable. It is a clean null, and the engineer's story at triage should be "no detectable effect, and we can rule out the effect we were looking for." It should not be "here is why each metric moved."

## Primary metric and ship decision
- **Successful Search Rate:** 0.4120 vs 0.4120, a change of +0.00008 absolute (+0.02% relative). The 95% CI is ±0.0012 (±0.3% relative) and p = 0.90.
- **Prereg bar:** the bar is +0.005 and ship requires the point estimate to reach it. The point estimate is about 60 times too small. Even the CI upper bound (+0.0013) is below the bar. This holds whether the bar is read as absolute (0.005) or relative (0.5%, about 0.0021 absolute).
- **Decision:** this is a no-ship, and it is a well-powered null, not an inconclusive one.
- **Sample and exposure:** there are 1.0M units per arm against 900k planned, and the exposure-balance health check passed. The experiment ran from Sep 12 for 14 days, and the Pulse snapshot is dated Sep 25.
- **Other checks:** the audit log is empty, so no mid-test changes were recorded. The only parameter that differs between arms is `ranker_model`, as intended. `snippet_length` is 160 in both arms.
- **Over time:** the daily results by days since exposure have CIs of about ±0.6% on every day and sit near zero throughout. I see no novelty or decay pattern. The 12 days of data fit the Sep 25 snapshot, since the 13th day is most likely still maturing.

## Guardrails
All four guardrails stay within their prereg margins, judging by the CI bounds. I'm reading the margins as relative, and they also pass if they are absolute.

| Guardrail | Change | CI upper bound (worse side) | Margin |
|---|---|---|---|
| Latency p95 | +0.8 ms (+0.2%) | +2.9 ms | 2% (about 8 ms) |
| Abandonment | +0.0002 | +0.0013 | 1% |
| Zero Result Rate | exactly 0 | +0.0004 | 3% |
| Revenue per User | −0.1% | about −0.8% | 1% |

Revenue per User is the tightest guardrail. Its CI lower bound is about −0.8% against a −1% margin, so it passes but with little room.

## Why the metrics "moved"
They didn't. Every one of the 15 top-level metrics has p > 0.05. The nearest to the line is **Long Click Rate** at −0.54% with p = 0.08.

- **Long Click Rate:** the engineer shouldn't build a story on this one. CTR is flat, Clicks per User is slightly up (+0.6%, p = 0.12), and Successful Search Rate is flat. Those don't fit together as a "quality got worse" story.
- **Pagination Rate:** it is nominally +0.8% (p = 0.23) but also noise.
- **Direction labels:** for metrics where lower is better, such as Abandonment, Latency and Time to First Click, a positive change is the bad direction. Several "up" numbers on the scorecard are nominally adverse but nowhere near significant.

## Deep-dive cuts, and what each should show
The pre-built segment metrics are Mobile/Desktop, Head/Tail and Navigational/Informational. There are about 48 segment-level rows in Pulse. At 95% confidence, roughly 2–3 should look "significant" by chance alone, and three do:

- Tail Queries Time to First Click is +2.4% with p = 0.039.
- Desktop Time to First Click is −2.2% with p = 0.057.
- Tail Queries Abandonment is +1.2% with p = 0.071.

The engineer should say these are consistent with chance. These cuts were not preregistered, and none survives multiple-comparison correction. Bonferroni was off in the config, and it would need p < about 0.001.

1. **Primary by segment (Mobile/Desktop, Head/Tail, Navigational/Informational):** expect all CIs to include zero and to span the overall estimate. The point estimates range from −0.5% to +0.6% relative with no consistent pattern, which is what noise looks like. Mobile and Desktop are both slightly negative, and Head, Tail and Navigational are slightly positive. A heterogeneous effect is possible, but the data doesn't support it.
2. **Tail-query timing and abandonment:** this is the one pairing worth a quick look, since slower first clicks and more abandonment on tail queries would be a coherent story. Check it only to confirm it isn't consistent across days or in a holdout slice. I expect it to vanish.
3. **Time-based cut:** a daily or weekly trend of the primary. I expect a flat line around zero, which rules out novelty effects or late drift as hiding a real effect.
4. **Funnel decomposition (CTR → Long Click → Successful Search):** this would show where the ranker changed behavior, if anywhere. I expect no step to move beyond noise. The answer to "did it reorder results at all?" would come from a ranking-diff analysis (how often the top-k results differ between arms), not from Pulse. If top-k overlap is very high, that explains the null directly.
5. **MDE statement for the Q&A:** with a CI of ±0.3% relative, any true effect above about 0.3% is excluded. That is much tighter than the 0.5% bar, so "the test was underpowered" is not a valid objection.

## Verdict
The experiment is clean and the decision is clear. The only preparation needed is framing: say "null result, bar ruled out, guardrails fine," and don't narrate noise as effects.

Ready for triage: Ready