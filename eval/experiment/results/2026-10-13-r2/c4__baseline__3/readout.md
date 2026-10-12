Decision: Ship

# Ranker v7 launch readout

**Design check.** Two-arm A/B on userID, 50/50 split inside a 20% allocation. There are 1,000,000 users per arm (900k planned). The window is 2026-09-12 to 09-25, which is the planned 14 days. The balanced-exposure health check passed. The audit log is empty, so nothing changed mid-flight. Sequential testing is off and there was a single fixed-horizon look, so the 95% CIs are valid as reported (no CUPED). The only intended change is `ranker_model` (v6 to v7). `snippet_length` is 160 in both arms.

**Primary (pre-registered): Successful Search Rate.** Control is 41.20% and test is 41.53%.
- Absolute change: +0.33 pt (CI +0.17 to +0.50), p = 7e-5.
- Relative change: +0.81% (CI +0.41% to +1.21%).
- The pre-registered bar is 0.005, with ship rule "point estimate at the bar". I read the bar as relative (+0.5%), the same units as the guardrail margins, e.g. 2% on a 412 ms latency. The point estimate of +0.81% clears it. The CI lower bound (+0.41%) does not, but the prereg rule does not require that.
- **If the bar was meant as absolute (+0.5 pt), the result misses it** (+0.33 pt) and the call becomes Don't ship. Please confirm the units with the prereg authors at the review.

**Guardrails (relative change, worst CI end against margin).** All are inside their margins.

| Metric | Change | Worst CI end | Margin |
|---|---|---|---|
| Latency p95 | +0.2% | +0.7% | 2% |
| Abandonment | +0.1% | +0.7% | 1% |
| Zero Result Rate | 0.0% | +1.4% | 3% |
| Revenue per User | -0.1% | -0.8% | -1% |

Abandonment, zero-result rate and revenue are closest to their margins. The CIs for zero-result rate and revenue are wide enough that a small harm is not ruled out.

**Things the review should know (not pre-registered, so exploratory).**
- Clicks per User is down 1.2% (-0.043, p = 0.003). CTR and Long Click Rate are flat. This is consistent with fewer clicks per successful search, but we should watch it.
- Successful Search Rate on Desktop is -0.69 pt (p = 0.003). Mobile is +0.03 pt.
- Pulse reports about 60 secondary and segment metrics. Roughly 3 to 4 have p < 0.05, which is about what chance gives. None of them survive a multiple-comparison correction (about 0.0008). I treat them as hypotheses, not findings.
- **Data oddity.** The overall Successful Search Rate lift (+0.33 pt) is larger than the lift in every segment of each split (mobile/desktop, head/tail, navigational/informational). A weighted average of segments cannot exceed all of its parts. Possible causes are segment metrics defined with different denominators, or a Pulse segmentation artifact. The primary metric itself is internally consistent (the CI matches the p-value). Someone should check the segment definitions before the Desktop number is quoted either way.

**Recommendation.** Ship, because the pre-registered primary meets its bar and no guardrail is breached. Two conditions go with that:
1. Confirm the relative-bar interpretation.
2. After launch, monitor Desktop Successful Search Rate and Clicks per User, and check the segment definitions.
