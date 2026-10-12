Decision: Keep running

# Ranker v7 readout (Pulse snapshot ds 2026-09-25, no CUPED, 95% CI)

## Bottom line
Successful Search Rate is up, but the point estimate is below the pre-registered bar, so the prereg ship rule is not met. The test is also only about 13 of 90 planned days in. Keep running to the planned end and re-read then. Guardrails look fine so far.

## Primary metric (Successful Search Rate)
- Control 0.4120, test 0.4153. Absolute change +0.00334 (+0.81% relative), 95% CI [+0.00169, +0.00500], p = 7e-5.
- The effect is real (CI excludes 0), but the prereg requires the **point estimate** to be at or above +0.005. The estimate is 0.0033, about two-thirds of the bar. Not a ship under the prereg.
- The CI upper end (+0.00502) just touches the bar, so we can't call it a miss for good. "Don't ship" would also be premature.

## Guardrails (prereg margins, relative; 95% CI)
| Metric | Change | CI half-width | Margin | Result |
|---|---|---|---|---|
| Latency p95 | +0.2% (worse) | ±0.5% | 2% | OK |
| Abandonment Rate | +0.1% (worse) | ±0.6% | 1% | OK |
| Zero Result Rate | 0.0% | ±1.4% | 3% | OK |
| Revenue per User | -0.1% | ±0.7% | 1% | OK |

No guardrail breach. All intervals sit inside their margins.

## Caveats
1. **Timing.** The experiment started 2026-09-12 and is configured for 90 days. This snapshot is from 2026-09-25, about 13 days, and is now 17 days old. Sequential testing is off, so repeated looks inflate false positives. Re-pull Pulse and decide at the planned end, not off this snapshot.
2. **Design is a holdout, not an isolated v7 test.** The config is "Q3 search launches holdout" (id q3_search_launches_holdout, 5% holdout vs 95% test, 20% layer allocation). Its stated hypothesis is the *combined* effect of the quarter's ranking launches. The visible parameter difference is only ranker_model (v6 vs v7), but the holdout may also contain other launches. Attribute the lift to v7 only if the team confirms nothing else differs between arms.
3. **Unit counts don't match the config.** The config sets a 95/5 split, but Pulse shows 1,000,000 units in each arm. The prereg planned 50,000 per arm. The balanced-exposure health check says PASSED. Someone should check how Pulse is sampling the arms before trusting the intervals.
4. **Subgroup and secondary metrics are not evidence.** About 55 metrics were tested with no multiplicity correction (Bonferroni is off). A few nominal hits are expected by chance: Head-query SSR p = 0.04, Navigational CTR p = 0.02 (negative), Mobile time-to-first-click p = 0.04. None were pre-registered, so I'm not acting on them.
5. The audit log is empty, so there's no record of mid-flight config changes.

## Next steps
- Re-pull Pulse at day 90 (or the pre-agreed end) and apply the prereg rule: ship only if the SSR point estimate is at or above +0.005 and guardrails hold.
- Resolve items 2 and 3 before that review.
