Decision: Don't ship

**Ranker v7 readout (launch review)**

**Result.** The primary metric moved up, but by less than the pre-registered bar. The pre-registration says ship only if the point estimate reaches the bar.

| | Value |
|---|---|
| Successful Search Rate | 0.4120 control → 0.4153 test |
| Absolute lift | +0.00334 (95% CI +0.0017 to +0.0050), p = 7e-5 |
| Relative lift | +0.81% (CI +0.4% to +1.2%) |
| Pre-registered bar | +0.005 |

The lift is real: it is statistically significant and the interval excludes zero. But +0.0033 is below +0.005, and the interval's upper end only just reaches the bar. The data give no support for an effect as large as the bar.

**Assumption to confirm.** The pre-registration doesn't state the unit of the bar. I read 0.005 as an absolute change in the rate (0.5 percentage points), which is the metric's native unit in Pulse. If the team meant a 0.5% relative lift, the point estimate (+0.81%) clears it and the call becomes Ship, since all guardrails below also pass. Please confirm with the pre-registration author before the meeting. The decision turns on this one point.

**Guardrails.** All four are within their margins. I read the margins as relative changes. Under an absolute reading, the unit problem doesn't change the outcome for any of them.

| Metric | Change (95% CI) | Margin | Status |
|---|---|---|---|
| Latency p95 | +0.2% (±0.5%) | 2% | OK |
| Abandonment Rate | +0.1% (±0.6%) | 1% | OK |
| Zero Result Rate | 0.0% (±1.4%) | 3% | OK |
| Revenue per User | −0.1% (±0.7%) | 1% | OK |

**Experiment validity.**
- The exposure balance health check passed.
- It ran the planned 14 days (Sep 12–25), with about 1.0M users per arm against 0.9M planned.
- The split is 50/50, and the audit log shows no mid-flight changes.
- Only the intended parameter (`ranker_model`) differs between arms. `snippet_length` is 160 in both.
- Sequential testing is off, which is fine for a fixed-horizon readout.
- Pulse was pulled without CUPED, as requested.

**Secondary signals.** These were not pre-registered and I ran no multiplicity correction across about 30 metrics, so treat them as hypotheses.
- Reformulation Rate went up (worse), +0.0014 absolute, p = 0.018. That is the only nominal significance among the secondaries.
- Long Click Rate went down, −0.0012, p = 0.074.
- Success Rate on Head Queries is down, −0.0026, not significant (p = 0.16).
- CTR is flat and Queries per User is flat.
- Together, the reformulation and long-click movements hint that some of the extra "successes" may be shallow clicks. That would explain why the success lift is small.

**Recommendation.**
1. Don't ship v7 as is, because it misses the pre-registered bar.
2. Confirm the unit of the bar. If it was relative, revisit this decision.
3. If the team wants to pursue v7, look into the head-query and reformulation signals before a follow-up test. Extending this test to chase the bar isn't justified, because the 14-day horizon was planned and the interval is already fairly tight.