Decision: Ship

I wrote the readout to `readout.md` in the working directory. It starts with the exact decision line.

- **Primary result:** Successful Search Rate went from 41.20% to 41.53%, which is +0.33 pp or +0.81% relative (95% CI +0.41% to +1.21%, p = 7e-5). There were 1.0M users per arm over the full 14 days, and the exposure-balance health check passed.
- **Pre-registered rule:** Ship needs the point estimate at or above the 0.5% bar, and +0.81% clears it. The lower CI bound is below the bar, but the rule only asks about the point estimate.
- **Bar units:** I read the 0.5% bar as relative, because the guardrail margins and daily files are relative. If the team meant 0.5 pp absolute, the result misses it (0.33 pp). This needs confirming at the review.
- **Guardrails:** Latency p95, Abandonment Rate, Zero Result Rate and Revenue per User all sit within their margins.
- **Durability:**
  - By calendar day the lift fades from +1.25% to +0.50%, and the day-14 CI includes 0.
  - By days-since-exposure it is flat at about +0.8% for all 12 days, which argues against a novelty effect.
  - The two views disagree on day 1, where they should match (+1.25% vs +0.82%). I couldn't resolve that from the files, so it's flagged for a data check.
- **Secondary and segment metrics:**
  - Reformulation Rate is worse (+1.0%, p = 0.013). It doesn't survive correction across the 56 secondary metrics and wasn't a pre-registered guardrail, so I'd only watch it.
  - Successful Search Rate is negative in both Mobile and Desktop while the overall result is positive. That can't happen if the two segments cover all users, so the segment definitions need checking. Neither segment result is significant.
- **Config:** The only parameter that differs between arms is `ranker_model`, and the audit log is empty, so there were no mid-test changes.

The recommendation is to ship, conditional on confirming the bar's units, checking the day-1 discrepancy, and checking the segment definitions.