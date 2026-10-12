Decision: Can't tell

**Ranker v7 readout for launch review**

**Why I can't call it**
- **The Pulse snapshot is an interim look.** It is dated 2026-09-15 and the experiment started 2026-09-12, so it covers about 3 days of the planned 14. It has 261k test and 260k control users, against 900k per arm planned, which is about 29%.
- **The experiment hasn't been closed out.** Today is 2026-10-12 and the planned 14 days ended around 2026-09-26. The config still shows the experiment as `active`, and the audit log is empty, so nobody has changed or stopped it. I don't have a final Pulse pull.
- **Peeking isn't corrected for.** The pre-registered design is a fixed horizon, and the config has sequential testing off. A p-value from an early look doesn't carry its nominal meaning.
- **This data can't carry a ship decision.** I'd rather not decide on a stale 3-day cut when the full-duration data should already exist.

**Primary metric: Successful Search Rate**

| | Value |
|---|---|
| Control | 0.4120 |
| Test | 0.4179 |
| Absolute lift | +0.00585 (+1.42% relative) |
| 95% CI | about +0.0013 to +0.0104 |
| p-value | 0.011 |
| Pre-registered bar | +0.005 |

- The point estimate (+0.00585) is above the pre-registered bar of +0.005, and the direction is favorable.
- The CI is wide, and the bar sits well inside it. The data are consistent with a lift anywhere from a negligible +0.13 points to a large +1.04 points, so they don't establish that the true lift reaches the bar.
- The pre-registration requires the point estimate to be at the bar. That holds in this cut, but I wouldn't trust a point estimate from 29% of the sample and 3 days to stay there. Early lifts often shrink as more data comes in. Day-of-week and novelty effects are also not yet averaged out.

**Guardrails (margin from the pre-registration)**

All four are within their margins at this interim look. The intervals are wide enough that none of this is established.

| Metric | Change | Margin | Result |
|---|---|---|---|
| Latency p95 | +0.8 ms (+0.2%, worse) | 2% | CI ±0.5%, within margin |
| Abandonment Rate | +0.0002 absolute (worse), +0.1% relative | 1% | Within margin (CI upper ≈ +0.0013 absolute, vs. 1% of 0.187 ≈ 0.0019) |
| Zero Result Rate | 0.0% | 3% | CI ±1.4%, within margin |
| Revenue per User | −0.1% | 1% | CI ±0.7%, lower bound about −0.8%, which is close to the −1% margin |

Revenue per User is the one to watch. Its lower bound is near the margin, and a modest drop with more data could cross it.

**Secondary metrics**
- CTR is up and nominally significant (+0.75%, p=0.003), consistent with the primary.
- The other secondary metrics are flat or inconclusive. Examples are Long Click Rate, Queries per User, Sessions per User, and Ad Click Rate. I didn't adjust for multiplicity, so I wouldn't highlight any single one.

**Health and setup**
- The exposure balance check passed. Arm sizes are 261k vs 260k and the split is 50/50.
- The test and control arms differ only in `ranker_model`, which is the intended parameter. `snippet_length` is the same in both arms.
- Allocation is 20% and the pre-registration is confirmed.

**Next steps**
1. Re-pull Pulse for the full window with the same settings (`cuped: "false"`, 95% confidence). Check that it reaches about 900k per arm.
2. Apply the pre-registered rule to that pull:
   - **Ship** if the lift point estimate is at or above +0.005 and every guardrail stays within its margin. Check Revenue per User first.
   - **Don't ship** if the lift point estimate falls below +0.005. A 95% CI that excludes zero would still mean an effect exists, just not one that meets the bar.
3. Have someone confirm why the experiment is still `active` past its planned end. It may be intentionally extended, or someone may have forgotten to close it.
4. If the final data can't be pulled before the meeting, the review should treat this as "no decision yet" and not as a positive signal.