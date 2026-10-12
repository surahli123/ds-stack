Decision: No effect found

# Ranker v7 readout

**Bottom line:** Ranker v7 did not move the pre-registered primary metric, and the test was precise enough to rule out the lift we needed. Don't launch it on the strength of this test. The "No effect found" decision is about the primary only. v7 shows no harm on the pre-registered guardrails, but it also has no demonstrated benefit.

## Test validity
- Plain A/B test, 50/50 split on userID, 20% layer allocation. The exposure-balance health check passed.
- The run is complete. It started 2026-09-12 and was planned for 14 days. The Pulse data is dated 2026-09-25, the last full day.
- There are 1.0M units per arm, against 0.9M planned. The test was fixed-horizon, so there is no peeking problem.
- Results are not CUPED-adjusted, with 95% CIs, as pre-registered.
- The audit log is empty, so the config did not change mid-test.
- The test group changes only `ranker_model`, as intended. `snippet_length` is the same in both arms.

## Primary metric: Successful Search Rate (pre-registered bar: +0.005, point estimate must reach it)
| | Control | Test | Diff | 95% CI | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4118 | -0.0002 (-0.05%) | [-0.0014, +0.0010] | 0.74 |

- The point estimate is slightly negative, so the ship rule (point estimate at or above the bar) fails.
- The upper end of the CI is +0.0010, which is about 5x below the +0.005 bar. The data rule out a lift of the size we pre-registered.
- The relative reading, if the bar was meant as +0.5%, gives the same answer: the CI is [-0.34%, +0.24%].
- This is a well-powered null, not an underpowered "can't tell". Running longer is unlikely to change the call.

## Guardrails (pre-registered margins)
The CI stays inside each margin, so no guardrail was breached.

| Metric | Change | 95% CI half-width | Margin |
|---|---|---|---|
| Latency p95 | +0.2% (+0.8 ms) | ±0.5% | 2% |
| Abandonment Rate | +0.1% | ±0.6% | 1% |
| Zero Result Rate | 0.0% | ±1.4% | 3% |
| Revenue per User | -0.1% | ±0.7% | 1% |

- Revenue per User is the tightest of the four. Its CI lower bound is about -0.8%, against a -1% margin.
- I read each margin as relative. If a margin was meant as absolute, the abandonment and zero-result CIs (±0.001 and ±0.0004) are still well inside it.

## Secondary metrics (56 total, no multiplicity correction; treat as exploratory)
- **Ad Click Rate:** -1.5% relative (p = 0.013). This is the only secondary that looks like a real move, and it is not a pre-registered guardrail. It is worth a look, because it could connect to revenue, but Revenue per User is flat. With about 56 metrics at 95%, 2–3 nominal "hits" are expected by chance, and this one would not survive a correction.
- **Queries per User:** +1.9% (p = 0.028). It is also uncorrected and would not survive correction. It is not consistent with any gain in success rate, clicks or sessions.
- The other secondaries (CTR, long clicks, reformulation, time to first click, clicks and sessions per user) are all flat.
- The segment cuts (mobile/desktop, head/tail, navigational/informational) show no significant movement. The closest are Successful Search Rate for informational queries (+0.0024, p = 0.09) and mobile abandonment (-0.0024, p = 0.09). I wouldn't act on subgroup trends found after the fact.

## Recommendation for the review
1. Don't ship v7 as a ranking win. The pre-registered success criterion was not met.
2. Shipping for other reasons (for example, retiring v6) is a separate call. The data show no latency, abandonment or revenue harm, but none of that is a benefit.
3. Optionally, follow up on the Ad Click Rate dip. Don't base a decision on the subgroup trends.
4. If the team believes a smaller lift (up to about +0.1pp) is valuable, that needs a new pre-registered bar and a new test. It can't be claimed from this one.
