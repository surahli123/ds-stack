Decision: Don't ship

**Ranker v7 raises Successful Search Rate, but by less than the pre-registered bar.**

**Primary metric** (Successful Search Rate, bar +0.005 absolute, increase, 95% CI, no CUPED)

| | Control | Test | Absolute change | 95% CI | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | +0.00334 (+0.81% relative) | [+0.0017, +0.0050] | 7e-5 |

- The lift is real: the CI excludes zero.
- The prereg requires the point estimate to reach the bar (`ship_requires: point_at_bar`). It doesn't: 0.0033 against 0.005.
- The CI upper end is 0.00498, so even the optimistic end of the interval doesn't reach the bar. More data won't fix this: the effect would have to be larger than what's been measured.

**Guardrails** (margins read as relative, from the percent CIs)

| Guardrail | Change | Relative CI | Margin | Result |
|---|---|---|---|---|
| Latency p95 | +4.9 ms (+1.2%) | [+0.7%, +1.7%] | 2% | Within margin, but a statistically significant regression (p=3e-6) |
| Abandonment Rate | +0.1% | [−0.5%, +0.7%] | 1% | Within margin |
| Zero Result Rate | 0.0% | ±1.4% | 3% | Within margin |
| Revenue per User | −0.1% | [−0.8%, +0.6%] | 1% | Within margin |

No guardrail is breached. Latency is the one to watch, because its worst-case 1.7% is close to the 2% limit.

**Validity**
- Exposures are balanced (health check passed), at 1.0M units per arm against 900k planned.
- Pulse data runs to 2026-09-25. The experiment started 2026-09-12 and was planned for 14 days, so the window is covered.
- The audit log is empty, so there were no mid-test config changes.
- The only parameter that differs between arms is `ranker_model`, as intended. `snippet_length` is 160 in both.
- The experiment still shows "active" past its planned end.

**Secondary and segment metrics (exploratory)**
- CTR is down 0.22 points (−0.71% relative, p=0.005). That runs against the hypothesis and is worth a look, but it wasn't pre-registered.
- About 50 segment metrics were scanned with no multiplicity correction. The few nominal hits are consistent with chance, so I'm not acting on any of them:
  - Head-query long-click rate is up (p=0.007).
  - Tail-query time to first click is down (p=0.013).
  - Head-query abandonment is down (p=0.027).
  - Informational clicks per user are up (p=0.047).
- The Successful Search Rate segments are all non-significant.

**Recommendation**
- Don't ship v7 as tested, per the prereg rule.
- If the team wants to ship a smaller gain, that would be a deliberate departure from the prereg. The review would have to agree to it explicitly, weighing a roughly +0.3 point lift (CI +0.17 to +0.50) against a small latency cost and the CTR dip.
- The more useful next step is probably a v7.1 that cuts latency and recovers more lift. I'd also look into why CTR fell while the success rate rose.