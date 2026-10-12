Decision: Don't ship

**Ranker v7 raises Successful Search Rate as pre-registered, but it breaks the Latency p95 guardrail.**

**Primary metric: met**
- Successful Search Rate rose from 41.20% to 41.53%, which is +0.33 pp absolute and +0.81% relative (95% CI +0.41% to +1.21%, p = 7e-5).
- The pre-registered bar is 0.005. The guardrail margins are relative fractions, so I read the bar as relative too (+0.5%).
- The point estimate (+0.81%) clears that bar. The CI's lower end (+0.41%) does not, but the pre-registration requires only `point_at_bar`.
- If the bar were meant as an absolute 0.5 pp, the point estimate (+0.33 pp) would miss it. Please confirm the intended unit.

**Guardrails**

| Metric | Change (95% CI) | Margin | Result |
|---|---|---|---|
| Latency p95 | +3.1% (+2.5% to +3.7%), 412 → 425 ms | 2% | **Breached.** The whole CI is above the margin. |
| Abandonment Rate | +0.1% (±0.6%) | 1% | Within margin |
| Zero Result Rate | 0.0% (±1.4%) | 3% | Within margin |
| Revenue per User | −0.1% (±0.7%) | 1% | Within margin |

A guardrail failure is a pre-registered reason not to ship as is. The worsening is real and significant, not noise. Whether +0.8% search success justifies about 13 ms of added p95 latency is a product call, but the pre-registration does not allow shipping through it by default.

**Validity checks**
- The exposure balance check passed. Each arm has 1.0M users, against 0.9M planned.
- The run covers 14 days, from Sep 12 to the Sep 25 results date, as planned.
- The audit log is empty, so the config was not changed mid-run.
- The only parameter that differs between arms is `ranker_model`, as intended (`snippet_length` is 160 in both).
- Pulse was requested without CUPED at 95% confidence, matching the pre-registration.
- Sequential testing and Bonferroni correction are off. That is fine for a single primary metric read at the planned end.

**Other observations**
- The secondary and segment metrics are mostly flat. CTR, long clicks, reformulation, queries, sessions and revenue show no clear change.
- A few segment metrics cross p<0.05 (Tail CTR −1.1%, Informational clicks per user −1.5%, Mobile abandonment −1.8%, Autocomplete acceptance +0.6%). There are about 70 secondary metrics and none were pre-registered, so I would expect a few of these by chance. I would not act on them.
- The segment Successful Search Rate metrics don't reconcile with the overall figure:
  - Mobile and Desktop are both negative (−0.10 pp and −0.26 pp), while the overall metric is +0.33 pp.
  - Control Head (0.414) and Tail (0.494) bracket the overall 0.412 incorrectly.
  - These segment metrics are probably defined differently from the primary, so they are not true partitions. That should be checked before anyone cites them.

**Recommendation**
- Don't ship v7 as configured.
- Have the ranker team investigate the latency regression, for example model size or feature fetch cost.
- If a version at or under +2% latency keeps the quality gain, re-test it.
- If the owners want to accept the latency cost, that is an explicit decision to override the pre-registered guardrail. It should be recorded as such, not treated as a pass.