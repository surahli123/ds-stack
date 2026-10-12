Decision: No effect found

# Ranker v7 – launch review readout

**Bottom line:** Ranker v7 did not move the pre-registered primary metric, and the test was big enough to rule out the lift the team said it needed. I recommend not shipping on this evidence. This is a negative result, not an inconclusive one.

## Primary (pre-registered): Successful Search Rate
| | Control | Test | Abs. diff | 95% CI | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.41225 | +0.00025 (+0.06% rel.) | [−0.00099, +0.00148] | 0.70 |

- Ship rule was: point estimate at or above +0.005. The estimate is +0.00025, about 5% of the bar.
- The CI upper bound (+0.0015) is also well below the bar, so a lift of +0.005 is ruled out. If the bar is read as relative (+0.5%), the result is the same: the upper bound is +0.36% rel.
- The data can't show the new ranker is worse. They do show any true effect is small (at most about +0.15pp), far short of what was needed to ship.

## Guardrails (pre-registered margins)
No guardrail was breached. No metric moved detectably, and every CI sits well inside its margin.
- Latency p95: +0.8 ms (+0.2%, CI ±0.5%) vs 2% margin.
- Abandonment: +0.0002 abs, CI ±0.0011, vs 0.01 margin.
- Zero Result Rate: no change (0.031 in both arms), CI ±1.4% rel. vs 3% margin.
- Revenue per User: −0.1% (CI ±0.7%) vs 1% margin.

## Validity checks
- Exposures are balanced (1,000,000 vs 1,000,000 units, health check PASSED). The planned size was 900k per arm.
- The data are from ds 2026-09-25. The experiment started 2026-09-12, so this covers the full 14 planned days.
- Fixed-horizon analysis: no sequential testing, so there is no peeking issue. CUPED was off, so the CIs are unadjusted and conservative.
- The two arms differ only in `ranker_model` (`snippet_length` is 160 in both), matching the intended parameters.
- The audit log is empty, so there were no mid-test config changes.
- Caveat: I could not check for novelty or primacy effects, because Pulse gives only a single pooled readout.

## Secondary and segment metrics (exploratory, not a basis for a decision)
- Pulse reports about 60 secondary and segment metrics, none of them pre-registered. At 95% some will look "significant" by chance. For example, Navigational CTR is −0.55pp at p=0.027, and it is unsupported by the other navigational metrics.
- Tail queries stand out: Successful Search Rate is +1.46pp (CI ±0.47pp, p<0.001), which survives a correction for this many comparisons. Head, Navigational and Informational queries show nothing.
- This is a post-hoc segment finding that was not in the pre-registration. It also sits oddly with the flat overall result, so I would not treat it as an effect of the whole launch. It is a hypothesis worth a **new, pre-registered test** targeted at tail queries. It does not justify shipping this experiment.

## Recommendation
1. Don't ship Ranker v7 on the primary metric. It missed the pre-registered bar and the bar is excluded by the CI.
2. Optionally propose a follow-up experiment on tail queries with its own pre-registered metric and bar.
