Decision: Don't ship

# Ranker v7 – launch review readout

## Summary
Ranker v7 (lambdamart_v7 vs lambdamart_v6) did not improve the pre-registered primary metric. Successful Search Rate (SSR) went **down**, and the drop is statistically significant. The pre-registered ship criterion was a point estimate of at least +0.5 pp. The observed change is −0.26 pp.

## Primary metric (pre-registered, 95% CI, no CUPED)
| Metric | Control | Test | Abs. change | 95% CI | p |
|---|---|---|---|---|---|
| Successful Search Rate | 41.20% | 40.94% | **−0.255 pp** (−0.62% rel.) | [−0.42 pp, −0.09 pp] | 0.0024 |

- Ship bar: +0.5 pp (point estimate). Not met. The whole CI is below zero, so this is a likely small regression, not just a missed bar.
- 1.0M users per arm, above the 900k planned. Exposures are balanced (health check passed). The allocation is a 50/50 split of a 20% layer allocation.
- Even the CI's best case (−0.09 pp) is about 0.6 pp short of the bar. More data would not plausibly change the decision.

## Guardrails (pre-registered margins)
No guardrail was breached. None is significant, and all CIs are well inside their margins. The guardrails don't offset the primary miss.

| Guardrail | Change | 95% CI half-width | Margin |
|---|---|---|---|
| Latency p95 | +0.82 ms (+0.2%) | ±0.5% | 2% |
| Abandonment Rate | +0.02 pp (+0.1%) | ±0.6% | 1% |
| Zero Result Rate | 0.0 | ±1.4% | 3% |
| Revenue per User | −0.1% | ±0.7% | 1% |

Revenue per User is the closest call. Its CI reaches −0.8%, which is within the 1% margin.

## Secondary and segment metrics (exploratory)
- Only 2 of 56 secondary metrics have p < 0.05. That is about what chance alone produces (roughly 3 expected), and no multiple-comparison correction was applied. I treat them as noise and don't base the decision on them.
- The SSR segment cuts (mobile, desktop, head, tail, navigational, informational) are all non-significant and point in mixed directions. They are not pre-registered, so they don't support a segment-targeted launch.
- CTR, long clicks and time to first click don't show a clear gain either. Nothing supports an argument that v7 helps on a metric other than SSR.

## Caveats
- The audit log is empty, so the config was not changed during the run. Only `ranker_model` differs between arms (`snippet_length` is 160 in both), which matches the pre-registered intended parameter.
- Pulse is dated 2026-09-25, one day before the planned 14-day end (started 2026-09-12). The experiment still shows `active` in the config. I did not re-pull results, and one extra day would not change the conclusion.
- No sequential-testing correction was configured, and the plan was a fixed-horizon read. The result is read once at the planned horizon, so this does not affect the inference.

## Recommendation
Don't ship v7 as is. Keep v6 in production and close or stop the experiment. If the team wants to continue, the next step is to investigate why SSR dropped, for example by looking at which query classes lose clicks. That would be a new, pre-registered experiment.
