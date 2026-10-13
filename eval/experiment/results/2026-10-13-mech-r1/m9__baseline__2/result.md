**Short version: nothing moved, so there's nothing to explain. The honest line for triage is "Ranker v7 had no detectable effect, and the primary is conclusively below the bar."**

## What the scorecard says

**Primary, Successful Search Rate**
- Control is 0.4120 and test is 0.41208, a change of +0.00008 (+0.02% relative), p=0.90.
- The 95% CI is ±0.00124 absolute (about ±0.3% relative), so the upper bound is about +0.0013.
- The prereg bar is 0.005 and ship requires the point estimate to reach it. The point estimate is about 60× short, and even the CI upper bound is well under it. It misses whether the bar is read as absolute or relative.
- This is a precise null, not an underpowered result. The experiment can rule out an effect of the size the team hoped for.
- Don't say "directionally positive". +0.00008 is noise.

**Guardrails**
- None are breached, but all of them are flat and the CIs are wide relative to the margins.
- Latency p95 is +0.2% (+0.8 ms, p=0.43). Abandonment is +0.0002 (p=0.74). Zero Result Rate is exactly 0 change. Revenue per User is -0.0009 (p=0.78).
- "No evidence of harm" is accurate. "Proven safe" is not.
- Only Latency p95 has a CI I could compare to its margin (±0.5%, margin 2%), and it fits well inside. The prereg margins for the other three are ambiguous (relative or absolute), so I haven't claimed they're inside their margins.

**Secondary metrics**
- All 14 have p>0.07. The smallest is Long Click Rate at -0.0012 (p=0.079), alongside CTR -0.0005 (p=0.49) and Clicks per User +0.023 (p=0.12).
- Those three point in different directions, so there is no coherent "engagement down" or "engagement up" story.

**Segment cuts**
- There are about 48 segment metrics in the pulse. Two have p<0.05 or close to it: Time to First Click for tail queries (+0.12 s, p=0.039) and for desktop (-0.12 s, p=0.057). Abandonment on tail queries is p=0.07.
- With about 60 metrics in total and no multiplicity correction (`bonferroniCorrection: false`), about 3 hits at p<0.05 are expected by chance. That is what we see.
- If asked, say these are noise. Don't build a narrative like "tail queries are slower to click".

## What the engineer should not claim
- **Don't offer causes for any movement.** Nothing is distinguishable from zero, and an explanation for noise would be fabricated.
- **Don't say "launch and iterate" or "directionally positive".** The prereg ship rule is not met.
- **Don't cite the two near-significant timing cuts as findings.**

## Deep-dive cuts to run next, and what each should show
1. **Device split reconciliation.**
   - Mobile and desktop Successful Search Rate are both about -0.0015, yet the overall change is +0.00008. Head and tail are both positive, and so are navigational and informational.
   - A pooled effect can't sit outside both subgroup effects unless the two arms have different mix across segments (Simpson's paradox) or the segments aren't a true partition.
   - Check the device, query-type and navigational/informational share of users per arm, plus SRM by segment.
   - I expect equal shares and a definitional explanation, such as users in several segments or ratio denominators. If the shares differ, the overall number is unreliable.
2. **Days-since-exposure trend.**
   - The `daily_by_exposure_day.json` file shows the daily delta cycling between -0.02%, +0.02% and +0.06% with CIs about ±0.6%. It is flat, with no novelty decay or learning curve.
   - It covers only days 1–12, though. Pull days 13–14, because the experiment is planned for 14 days.
   - I expect the same flat line, which would rule out a diluted early effect.
3. **Heterogeneity on pre-specified cuts only, run once.**
   - Cut on head vs tail and on mobile vs desktop for Successful Search Rate. A true effect concentrated in one slice could be hidden in a flat average.
   - Judge it with a corrected threshold (Bonferroni across the cuts). I expect nothing to survive.
4. **Power and MDE statement.**
   - Compute the minimum detectable effect at this n. With CI ±0.0012, it is about 0.0012–0.0015, so the 0.005 bar was very conservative.
   - This lets the team say "the true effect is below about +0.0013" rather than "inconclusive".

## Data-quality and setup flags
- **Pulse is stale.** The snapshot is `ds` 2026-09-25 and today is 2026-10-13, 18 days later. The experiment started 2026-09-12, so the snapshot covers about 13–14 days. Status is still `active` in the config, and nobody has concluded it or shut it down. Re-pull the final pulse.
- **Exposure doesn't match the plan.** Prereg says 900k units per arm and the pulse shows exactly 1,000,000 per arm. That is likely fine (more power), but ask why.
- **Layer overlap.** The experiment sits in layer `search_ranking`. Check for other experiments touching the same surface, since only one health check (exposure balance) is configured.
- **Clean config.**
  - Audit log is empty, so no mid-flight changes.
  - Only `ranker_model` differs between arms, matching `intended_params`. `snippet_length` is 160 in both.
  - Exposure balance passed. The unit counts are suspiciously exact (1,000,000 each) and may be rounded.
- **Pulse settings.** The pulse was pulled with CUPED off, and CIs are 95%, unadjusted for multiplicity. That's fine for the primary, which is a single pre-registered test.

## Readiness
The result itself is clear (null on the primary, no guardrail breach), and there's enough to present: "no effect, don't ship". Three things are unresolved, though. These are the segment arithmetic that doesn't add up, the stale or unconcluded pulse (days 13–14), and the unexplained 1.0M vs 0.9M units. None of them is likely to change the conclusion, but the first could undermine confidence if someone at triage spots it.

Ready for triage: Ready, with open questions