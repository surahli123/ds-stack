Decision: Don't ship

**Ranker v7 (`lambdamart_v7` vs `lambdamart_v6`): readout for launch review**

**Result.** The primary metric moved the wrong way, and the 95% CI excludes zero.

| Successful Search Rate | Control | Test | Abs. change | 95% CI | p |
|---|---|---|---|---|---|
| Pulse as of 2026-09-25, 1.0M users per arm | 41.20% | 40.94% | −0.26 pp (−0.62% rel.) | [−0.43, −0.09] pp | 0.002 |

The pre-registered bar to ship was +0.5 pp, with the point estimate at or above the bar. The estimate is about 0.76 pp below that bar. The upper CI limit is below zero, so this is more than a miss: the data point to a small regression.

**Guardrails.** None were breached, but none give a reason to ship.
- Latency p95: +0.8 ms (+0.2%), CI ±2.1 ms. This is inside the 2% margin.
- Abandonment Rate: +0.02 pp, not significant.
- Zero Result Rate: unchanged (0.0 change).
- Revenue per User: −0.1%, not significant.

**Secondary metrics.**
- CTR is −0.11 pp (p=0.16). Long Click Rate is +0.09 pp (p=0.19). Neither is significant.
- Autocomplete Acceptance is −0.19 pp (p=0.067). This is borderline, and I wouldn't read anything into it.
- No secondary metric shows a gain that offsets the primary loss.

**Segments.** The Successful Search Rate cuts (mobile, desktop, head, tail, navigational, informational) are all non-significant, with mixed signs.
- Most segment point estimates are positive, even though the overall result is negative. The segment CIs are wide (about ±0.4 pp), so this is noise.
- I'm not claiming any "winning" segment. These were not pre-registered and there is no multiplicity correction.

**Validity checks.**
- The exposure balance health check passed. Both arms have 1.0M units, versus the 900k planned.
- The experiment ran Sep 12 to about Sep 26 (14 days, as planned). Pulse is dated 09-25, so it is essentially the full window.
- The audit log is empty, so there were no mid-test config changes.
- The only parameter that differs between arms is `ranker_model`, as intended. `snippet_length` is the same in both.
- It is a clean A/B on userID, with no sequential testing and no CUPED. The CIs are plain 95% intervals, and the only primary metric is the pre-registered one.

**Caveats.**
- The effect is small, at less than 1% relative. It is statistically clear but may not matter much in practice.
- The prereg doesn't say whether the 0.005 bar is absolute or relative. I read it as absolute (0.5 pp). If it were relative (0.5%), the result still fails, because the estimate is negative.
- I only had one Pulse snapshot, so I can't check for novelty or learning effects over time.

**Recommendation.** Don't ship v7 as tested. There is no evidence of benefit and some evidence of harm to the primary metric. If the team still believes in the model, the next step is to diagnose why it lowers success. One place to look is query types where CTR and Autocomplete Acceptance dip. Any revised ranker needs a new pre-registered test.