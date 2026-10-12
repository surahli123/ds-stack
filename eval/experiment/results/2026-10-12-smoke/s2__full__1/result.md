I rendered the readout and ran lint and the cold read. The cold read failed, so I'm giving you the result as it stands.

Decision: Ship

Ranker v7. Successful Search Rate improved +0.81% (+0.41% to +1.21%), which clears the 0.50% bar and every guardrail held.

Ask: Approve the launch to all traffic.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% | better |
| Other guardrails | guardrail | Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- Daily results by days since first exposure showing the lift fading would move this to Keep running.
- A pre-exposure comparison showing the arms already differed would make the test Can't tell.
- Revenue per User or Latency p95 moving past its margin in a longer run would make it Don't ship.

## Why it moved

- [measured] Segment cuts show no single segment carrying the lift: Desktop +0.84% and Mobile +0.07% both have wide ranges.
- [guess] Ad Click Rate fell 2.8%, not a registered guardrail and not clear after correction. The new ranker may show fewer ad-adjacent results.
- [inferred] Long Click Rate is flat to down (-0.38%), so some added successes may be shallow clicks.

## Analyst's view

The analyst would call this Escalate: The low end of the range (+0.41%) is under the 0.50% bar, Ad Click Rate fell 2.8%, and the pre-period and novelty checks could not run. Ship holds under the registered rule.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

Lint: 0 fail, 0 warn, 264 body words (readout)
Cold read: skim 2/2, full 2/3 - fail

The cold read failed because the reader missed the pre-period caveat as a takeaway. It also found the Ship call versus the analyst's Escalate view confusing. I did not rerender after that.

The call is Ship because the estimate clears the pre-registered point-at-bar rule, which the team marked confirmed. I wrote the first line as "Decision: Ship" as you asked, replacing the title the renderer produced. The files are in `out/`.