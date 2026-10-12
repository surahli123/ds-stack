Decision: Ship

I wrote the full readout to `readout.md`. The ship call depends on two things I couldn't confirm from the files, listed at the end.

**Primary metric: Successful Search Rate.**
- It rose from 41.20% to 41.53%, which is +0.334 pp or +0.81% relative.
- The 95% CI is +0.41% to +1.21% relative, with p = 7e-5.
- The pre-registration says to ship if the point estimate reaches the 0.005 bar, and +0.81% clears 0.5%. The CI's lower end (+0.41%) is below the bar, so the true lift could be smaller than the bar.

**Guardrails** all stay inside their pre-registered margins, even at the bad end of the CI (margins read as relative):

| Guardrail | Change | Worst case in CI | Margin |
|---|---|---|---|
| Latency p95 | +0.2% | +0.7% | 2% |
| Abandonment Rate | +0.1% | +0.7% | 1% |
| Zero Result Rate | 0.0% | +1.4% | 3% |
| Revenue per User | −0.1% | −0.8% | −1% |

**Secondary metrics and segment cuts.**
- Nothing is significant after allowing for the number of tests.
- CTR is slightly down (−0.29%, p = 0.26). It is worth monitoring but doesn't block shipping.

**Two things to settle before the meeting:**
1. **Bar units:** The pre-registration doesn't say whether 0.005 is relative or absolute. I read it as relative, because a 0.02 absolute margin on 412 ms latency would make no sense. If the team meant 0.5 pp absolute, the +0.33 pp lift misses the bar and the decision becomes Don't ship.
2. **Allocation change:** The audit log shows allocation cut from 20% to 10% on 2026-09-16, but `experiment.json` currently shows 20%. Both arms were scaled equally and the exposure-balance check passed, so the comparison should hold. I had no per-day data to check for a time trend, and the config and log still need to be reconciled.