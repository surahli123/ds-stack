Decision: Don't ship

# Ranker v7 readout

**Summary.** Ranker v7 hits the pre-registered primary bar, but it breaks a pre-registered guardrail. Abandonment Rate got worse by about 2.2% relative, and the whole 95% CI sits beyond the 1% margin. Under the prereg, that means no ship.

## Primary: Successful Search Rate (bar: +0.005 absolute, point estimate)
- Control 0.4120, Test 0.4171. Lift is +0.00511 absolute (+1.24% relative), 95% CI [+0.0035, +0.0068], p<0.001.
- The point estimate clears the 0.005 bar by only 0.0001. The CI lower bound is below the bar. The prereg asks for the point estimate (`point_at_bar`), so this passes, but narrowly.

## Guardrails (prereg margins, read as relative changes, 95% CI, unadjusted Pulse output)
| Metric | Change (relative) | 95% CI | Margin | Result |
|---|---|---|---|---|
| **Abandonment Rate** (lower is better) | **+2.2%** (0.187 → 0.191) | **[+1.5%, +2.9%]** | 1% | **BREACHED**. Significantly worse, and the CI lies entirely beyond the margin |
| Latency p95 | +0.2% (412 → 412.8 ms) | [-0.3%, +0.7%] | 2% | OK |
| Zero Result Rate | 0.0% | [-1.4%, +1.4%] | 3% | OK |
| Revenue per User | -0.1% | [-0.8%, +0.6%] | 1% | OK, but the CI's lower end is close to the margin |

The margins are not labeled absolute or relative in the prereg. I read them as relative because a 0.02 margin on a latency in milliseconds makes no sense in absolute terms. If Abandonment's 0.01 were meant as absolute, the upper CI end (+0.0054) would be inside it. I would confirm the intent with the prereg authors, but the other three margins only work as relative.

## Supporting signals
- CTR is up 1.9% and Clicks per User is up 2.1%, both significant. Long Click Rate is flat (-0.09%, p=0.76), so the extra clicks do not look like better outcomes.
- Abandonment is the opposite of what the primary win suggests. More searches end in a successful click, and more end in abandonment too. This is worth understanding before any relaunch.
- Segments are exploratory, with about 45 slices and no correction, so treat them as hypotheses only. Abandonment is worse in Head Queries (p=0.04). CTR and Clicks per User are lower in Tail Queries (p=0.014 and p=0.027). These would not survive multiple-comparison correction. The segment table does not explain the overall abandonment increase.

## Validity checks
- The design is a clean A/B test: userID unit, 50/50 split, 1.0M users per arm. The prereg planned 900k, so the test has more users than planned. The exposure balance health check passed.
- There were no config changes during the run (the audit log is empty). The only parameter difference between arms is `ranker_model`, as intended. `snippet_length` is identical in both arms.
- Pulse was requested without CUPED and at 95% confidence. There is no sequential testing correction, and none is needed for a single fixed-horizon read.
- The Pulse snapshot is dated 2026-09-25. The test started 2026-09-12 and has a 14-day duration, so the snapshot may be a day short of the full window. I did not re-pull the data.

## Recommendation
Don't ship v7 as is. The primary lift is real and about at the bar, but the abandonment regression is statistically clear and larger than the allowed margin. Next steps:
1. Investigate the cause of the abandonment increase. Check the Head Query ranking and whether the clicks are shallow.
2. Iterate on the ranker and retest.
3. If the team would accept an abandonment trade-off for the SSR gain, that is a change to the prereg and needs explicit sign-off at launch review, not a default.
