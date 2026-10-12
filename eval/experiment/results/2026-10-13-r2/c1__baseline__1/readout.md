Decision: Don't ship

# Ranker v7: launch readout

**Bottom line.** Ranker v7 raises Successful Search Rate (SSR) by less than the bar we set before launch. The pre-registered rule is "ship requires the point estimate at or above +0.5 pp", so the rule says don't ship. The effect is real but small.

## Primary metric (pre-registered, one metric)
| | Control | Test | Abs. change | 95% CI | Bar |
|---|---|---|---|---|---|
| Successful Search Rate | 41.20% | 41.53% | **+0.334 pp** (+0.81% rel.) | [+0.169, +0.499] pp | +0.5 pp |

- p = 7e-5, so it is clearly positive.
- The point estimate is about two-thirds of the bar. Even the CI's upper end (+0.499 pp) is just under it.
- Calling this a win means lowering the bar after seeing the data. I recommend against that.
- If the team wants v7 anyway, the honest options are a new pre-registered decision with a justified lower bar, or a follow-up test with an improved ranker. That is a launch-review call, not something this analysis can settle.

## Guardrails (pre-registered margins, 95% CI, CUPED off)
All four are inside their margins. That is "no evidence of harm", not proof of no harm, because the CIs are fairly wide.
| Guardrail | Change (rel.) | CI half-width (rel.) | Margin |
|---|---|---|---|
| Latency p95 | +0.2% (+0.8 ms) | ±0.5% | 2% |
| Abandonment Rate | +0.1% (worse) | ±0.6% | 1% |
| Zero Result Rate | 0.0% | ±1.4% | 3% |
| Revenue per User | −0.1% | ±0.7% | 1% |

## Things I noticed, none of which change the decision
1. **Possible sample-ratio mismatch (SRM).** experiment.json shows exposures of 1,010,000 control vs 990,000 test, against a 50/50 split. That gap is far too big to be chance (z ≈ 14). Yet the platform's balance health check says PASSED, and Pulse reports exactly 1,000,000 units per arm. These sources disagree.
   - The exposure counts may be cumulative through today, and the experiment is still `active` past the planned 14 days. The Pulse snapshot is from 2026-09-25.
   - The figures also look rounded.
   - Someone should check raw assignment counts before anyone relies on this result. If the imbalance is real, the SSR estimate is suspect in either direction.
   - A real SRM would not rescue a ship decision, because the estimate is already below the bar.
2. **Clicks per User fell 1.0% (p = 0.014).** It is not a pre-registered primary or guardrail, and it is one of ~70 unplanned metrics and slices, so it is likely noise. It is also directionally odd next to a higher SSR, so it is worth a look. Segment slices showed no robust pattern. Tail-query abandonment was the only slice below p = 0.05 (p = 0.034, +0.39 pp worse), which is expected by chance across this many slices. I treat all of these as exploratory.
3. **Experiment is still running** beyond its planned 14 days. The Pulse data is from day 14 (09-25, start 09-12), which matches the plan. Extra time won't change the verdict unless the bar changes, and sequential testing is off, so repeatedly peeking and extending would inflate false positives.
4. **Sample size.** About 1.0M per arm was analysed against 900k planned, so the test was adequately powered.
5. **Config.** The only intended change is `ranker_model`; `snippet_length` is identical across arms. The audit log is empty, so there is no sign of mid-test changes.

## Recommendation
Don't ship v7 as is. Resolve the exposure-count discrepancy, and decide explicitly whether a +0.33 pp gain is worth shipping. If it is, that needs a documented change to the bar, not a quiet reinterpretation.
