Decision: Ship

# Ranker v7 readout

**Recommendation:** Ship `lambdamart_v7`. The single pre-registered primary clears its bar at the point estimate, and all four pre-registered guardrails are within margin. One exploratory segment result (head queries) is worth monitoring after launch. It doesn't change the decision.

## Primary (pre-registered, the only one)
| Metric | Control | Test | Abs. change | Relative change (95% CI) | p | Bar |
|---|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4134 | +0.00334 (±0.00165) | **+0.81%** (+0.41% to +1.21%) | 7e-5 | +0.5% relative, point estimate |

- The prereg rule is `ship_requires: point_at_bar`. The point estimate (+0.81%) is above the 0.5% bar, so the rule is met.
- The CI excludes zero. Its lower end (+0.41%) is below the bar, so the true lift could be somewhat under 0.5%. The prereg didn't require the CI to clear the bar.
- Reading of the bar: I took 0.005 as a relative lift. The guardrail margins use the same convention (a 3% margin on a 3.1% zero-result rate only makes sense as relative). If the bar were meant as an absolute 0.5pp, the result (+0.33pp) would fail. Please confirm this reading in the room, because the decision depends on it.

## Guardrails (pre-registered margins, relative; pass = worst end of the 95% CI is inside the margin)
| Guardrail | Change (95% CI) | Worst end vs. margin | Result |
|---|---|---|---|
| Latency p95 (lower is better) | +0.2% (±0.5%) | +0.7% vs 2% | Pass |
| Abandonment Rate (lower is better) | +0.1% (±0.6%) | +0.7% vs 1% | Pass |
| Zero Result Rate (lower is better) | 0.0% (±1.4%) | +1.4% vs 3% | Pass |
| Revenue per User (higher is better) | −0.1% (±0.7%) | −0.8% vs −1% | Pass (tightest) |

Revenue per User and Abandonment have the least room. Their CIs don't rule out harm of up to 0.8% and 0.7%, but both stay inside the agreed margins.

## Validity
- Design: user-level A/B, 50/50, 20% allocation. The `has_balanced_exposures` check passed.
- Duration: Sep 12 to Sep 25, which is the planned 14 days. Sequential testing was off, so a fixed-horizon read at the planned end is appropriate.
- Sample: 1.0M users per arm, above the 900k planned.
- Config: the audit log is empty, so there were no mid-test changes. The only parameter that differs between arms is `ranker_model` (`snippet_length` is 160 in both), which matches the intended params.
- Pulse was run with CUPED at 95% confidence, as requested.

## Exploratory findings (not pre-registered, ~90 metrics and segments, no multiplicity correction)
Treat these as hypotheses. At this volume, a handful of p<0.05 results is expected by chance.
- **SSR on head queries: −0.95% (−0.38pp, p=0.011).** This is the one to watch. It is directionally negative, and tail queries (−0.5%) and desktop (−0.5%) are also negative, while mobile is +0.7%. It sits oddly with the positive overall lift. Head and tail both being negative while the total is positive means the segments don't partition the population (e.g. torso queries are missing) or there is a mix shift. I haven't been able to reconcile this from the Pulse output. Suggested follow-up: a head-query SSR dashboard after ramp, plus a check of how the segments are defined.
- Reformulation Rate is worse overall (+0.84%, p=0.039, lower is better) and for navigational queries (+2.4%, p=0.010). Time to First Click is better (−1.1%, p=0.031). Neither was pre-registered.
- CTR, Long Click Rate, Clicks per User, and Queries and Sessions per User show no detectable change. CTR and Clicks per User are slightly negative in point estimate but nowhere near significant.

## Risks and caveats
- The lift is modest. The lower CI bound (+0.41%) is under the bar, so the realized gain may be a bit under the target.
- Head-query and reformulation results are unadjusted and exploratory. They could be noise, or a real trade-off in which the new ranker helps some queries and hurts others.
- Two weeks of data can't speak to novelty or long-term effects.

## Suggested next steps
1. Confirm in the review that the bar is a 0.5% relative lift.
2. Ship to 100%, ideally with a holdback or a short post-launch monitor on head-query SSR, Reformulation Rate, and Revenue per User.
3. Investigate the segment definitions and the head-query result as a follow-up.
