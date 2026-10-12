Decision: Don't ship

# Ranker v7: launch readout

**Bottom line.** The pre-registered ship rule needs *both* primaries to reach their bar (+0.5 pt) on the point estimate. Neither does. Successful Search Rate (SSR) is up, but by less than the bar. Long Click Rate (LCR) shows no lift, and its CI rules out the bar. Under the rule, v7 does not ship as built.

## Design and data check
- A/B, 50/50 control (lambdamart_v6) vs test (lambdamart_v7), unit = userID, 20% allocation, 95% CI, no CUPED, no sequential testing.
- Window: start 2026-09-12, 14 days, matches the plan. The Pulse snapshot is ds 2026-09-25, the last planned day.
- 1,000,000 users per arm (plan was 900k). Exposure balance check PASSED. Audit log is empty, so there were no mid-test config changes.
- The config only lists SSR as a primary metric. The prereg also requires LCR. I judged against the prereg.

## Primary metrics (prereg: rule = all, ship requires point estimate ≥ bar)
| Metric | Control | Test | Abs. change (95% CI) | p | Bar | Met? |
|---|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | +0.0033 (+0.0017, +0.0050), +0.81% rel | 7e-5 | +0.005 | No |
| Long Click Rate | 0.2210 | 0.2213 | +0.0003 (−0.0011, +0.0016), +0.12% rel | 0.70 | +0.005 | No |

- SSR: the lift is real (CI excludes 0), but the point estimate is about two-thirds of the bar. The CI upper end only just touches the bar, so the effect is probably below it.
- LCR: flat. The CI upper bound (+0.0016) is well under the bar, so the bar is ruled out.
- Because the rule is "all", the LCR miss alone blocks shipping.

## Guardrails (prereg margins, read as relative changes)
All pass: the worst-case end of each CI stays inside its margin.
- Latency p95: +0.2% (±0.5%), margin 2%.
- Abandonment Rate: +0.1% (±0.6%), margin 1%.
- Zero Result Rate: 0.0% (±1.4%), margin 3%.
- Revenue per User: −0.1% (±0.7%), margin 1%. The lower bound is −0.8%, which is close to the margin but inside it.

I'm assuming the margins are relative. If they are absolute, the conclusion is the same.

## Secondary and segment metrics: not evidence
About 70 secondary and segment metrics were reported, with no multiplicity correction (Bonferroni is off). A handful are nominally significant at p<0.05, as expected from chance alone. These are Queries per User (+1.07%, p=0.02), CTR on tail queries (+0.0033, p=0.016) and LCR on head queries (−0.0020, p=0.04). None was pre-registered, and they point in mixed directions. I'm not using any of them for the decision. Head-query SSR (−0.0032, p=0.14) is not significant, but it is the segment to look at if v7 is iterated.

## Recommendation
- Don't ship v7 as is. It misses the pre-registered bar on both primaries.
- The result is not "no effect": SSR improved modestly with no guardrail harm. If the team still wants v7, it should go through a new pre-registered decision or an iteration on the model. The bar should not be relaxed after seeing these results.
- Keeping the test running is unlikely to change the answer. The SSR CI is already narrow (±0.0016) and LCR is clearly flat.
- Follow-up: fix the experiment config so both prereg primaries are registered.
