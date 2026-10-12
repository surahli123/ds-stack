Decision: No effect found

**Ranker v7 did not raise Successful Search Rate, and the data rule out the improvement the team pre-registered as the bar. I recommend not launching on this result.**

**Primary metric: Successful Search Rate (95% CI, no CUPED)**
- Control is 0.4120 and test is 0.4118, a difference of −0.021 pp (−0.0002).
- The 95% CI is about −0.14 pp to +0.10 pp, and p = 0.74.
- The pre-registered ship bar is +0.005. That is +0.5 pp if read as absolute, or about +0.2 pp if read as 0.5% relative.
- The CI's upper end (+0.10 pp) is below the bar under either reading, so the bar is ruled out.
- The prereg requires the point estimate to reach the bar, and it doesn't (the estimate is about zero).

**Guardrails: none breached**
Each CI stays inside its pre-registered margin, so v7 is neutral on these. The checks were one-sided: a guardrail passes if its CI doesn't reach past the margin in the harmful direction.

| Guardrail | Change | CI half-width | Margin |
|---|---|---|---|
| Latency p95 | +0.2% (worse) | ±0.5% | 2% |
| Abandonment Rate | +0.1% (worse) | ±0.6% | 1% |
| Zero Result Rate | 0.0% | ±1.4% | 3% |
| Revenue per User | −0.1% | ±0.7% | 1% |

**Design and health**
- The sample is 1.0M users per arm, above the 900k planned. The split is 50/50 and the exposure-balance check passed.
- The audit log is empty, so the config wasn't changed mid-run.
- Pulse is dated 2026-09-25, which matches the 14-day plan if the run started on 2026-09-12. I worked that start date out from `startTime`, so please confirm it.
- The experiment still shows `status: active` today (2026-10-12). It should be closed out, and I did not check whether it kept running after the 09-25 snapshot.
- Sequential testing and Bonferroni correction are both off, which is fine for a single fixed-horizon read at the planned end.

**Secondary and subgroup metrics: not evidence of an effect**
- Pulse shows 56 secondary and segment metrics. Two are nominally significant at 95%, and that is roughly what chance alone would produce across this many tests.
- Queries per User is +1.9% (p = 0.028). It is not a pre-registered metric, and it is not backed by Sessions, Clicks, or CTR, which are flat.
- Ad Click Rate is −1.5% relative (p = 0.013). It isn't a guardrail, but it is a revenue-adjacent signal. I'd keep an eye on it, though Revenue per User is flat.
- No segment moved the primary metric (mobile, desktop, head, tail, navigational, informational all have p > 0.09). I did not treat any of these as findings.

**For the review**
- v7 isn't harmful, but it shows no benefit on its stated goal. The experiment was adequately powered to detect a bar-sized gain and found none.
- If the team still wants v7 for other reasons, that needs a new decision with a new hypothesis. This test can't support shipping it as a search-quality win.
- Checking whether the Ad Click Rate dip and the Queries per User rise are real would take a follow-up test with those metrics pre-registered.