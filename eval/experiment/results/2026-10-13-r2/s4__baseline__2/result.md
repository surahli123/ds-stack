Decision: Ship

The readout is saved at `readout.md` in the working directory. It starts with the required decision line.

**Primary result.** Ranker v7 raises Successful Search Rate by +0.33 percentage points, from 0.4120 to 0.4134. That is +0.81% relative, with a 95% CI of +0.41% to +1.21% (p = 7e-5). The pre-registration says to ship if the point estimate is at or above the bar, and +0.81% clears a 0.5% bar.

**Guardrails.** All four pass, including the worst end of each confidence interval:

| Guardrail | Worst case in the CI | Pre-registered margin |
|---|---|---|
| Latency p95 | +0.7% | 2% |
| Abandonment Rate | +0.7% | 1% |
| Zero Result Rate | +1.4% | 3% |
| Revenue per User | −0.8% | 1% |

**Setup.** The exposure-balance health check passed, and the audit log is empty, so nothing changed mid-test. Only `ranker_model` differs between arms. The test ran the planned 14 days with 1.0M users per arm against the 900k planned.

**The call depends on one assumption.** The pre-registration gives the bar as `0.005` with no units. I read it as relative, because the guardrail margins can only be relative (a 0.02 latency margin makes no sense as milliseconds). If the team meant 0.5 percentage points, the +0.33 pp result misses the bar and the decision becomes Don't ship. The review should confirm which unit was meant before approving.

**Exploratory segment findings.** These weren't pre-registered and come from about 60 untested-for-multiplicity comparisons, so a few false positives are expected.
- Successful Search Rate on head queries is down 0.38 pp (p = 0.011).
- Reformulation Rate is worse overall (p = 0.039) and for navigational queries (p = 0.010).
- Head and tail queries are both negative while the total is positive. That would require the middle slice, which Pulse doesn't report, to be strongly positive, so the segment definitions are worth checking.

I treated these as monitoring items after launch, not as a reason to block.