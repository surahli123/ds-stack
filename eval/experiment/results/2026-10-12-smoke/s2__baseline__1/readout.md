Decision: Ship

# Ranker v7 – launch readout

**Design checks (clean).** A/B on userID, 50/50 (control lambdamart_v6 vs test lambdamart_v7), 1,000,000 units per arm (900k planned), 14 days (start 2026-09-12, Pulse ds 2026-09-25), fixed-horizon (no sequential testing, so one final read is valid). Exposure-balance health check PASSED. The only parameter that differs between arms is `ranker_model` (as intended; `snippet_length` is 160 in both). Audit log is empty, so there were no mid-flight config changes. Pulse was pulled with CUPED off, 95% CI, as pre-registered.

**Primary: Successful Search Rate (pre-reg: increase; ship if point estimate ≥ bar of 0.005).**
- Control 0.4120 → Test 0.4153: +0.0033 absolute (95% CI +0.0017 to +0.0050), +0.81% relative (CI about +0.40% to +1.21%), p = 7e-5.
- The effect is real. The point estimate is +0.81% relative, which clears the 0.5% bar (0.005).
- Units: Pulse reports percentChange in percent (0.81 = 0.81%), so the comparison is 0.0081 vs 0.005. I read the bar as relative because the pre-reg guardrail margins in the same file (2%, 1%, 3%, 1%) are relative. **If the bar was meant as an absolute 0.5 pp, the point estimate (0.33 pp) misses it.** Please confirm with the pre-reg author in the review. The decision depends on this.
- The pre-reg rule is point-at-bar, so the CI lower bound (+0.40% relative) being under the bar does not block shipping. The true lift could plausibly be anywhere from about +0.4% to +1.2%.

**Guardrails (all within margin; worst end of the 95% CI vs margin, relative).**

| Metric | Change | Worst CI end | Margin | Result |
|---|---|---|---|---|
| Latency p95 | +0.2% (worse) | +0.7% | 2% | pass |
| Abandonment Rate | +0.1% (worse) | +0.7% | 1% | pass, thin headroom |
| Zero Result Rate | 0.0% | +1.4% | 3% | pass |
| Revenue per User | -0.1% | -0.8% | -1% | pass, thin headroom |

Abandonment and Revenue are not proven neutral. Their CIs reach 70–80% of the margin, so a small harm cannot be excluded. Neither point estimate is significant (p = 0.74 and 0.78).

**Things to know (not pre-registered, not blocking).**
- Ad Click Rate fell 2.8% (0.0520 → 0.0505, p = 0.022). It is not a pre-registered guardrail, and with about 40 secondary and segment metrics reported, one p < 0.05 is expected by chance. It is the one result that could connect to revenue, so watch it after launch. Revenue per User itself is flat.
- Secondary engagement metrics (CTR, long clicks, queries/user, sessions, clicks) are all non-significant. Long Click Rate and Queries per User lean slightly negative (p = 0.21 and 0.076). No supporting engagement signal accompanies the Successful Search Rate gain.
- The segment cuts (mobile/desktop, head/tail, navigational/informational) are exploratory and all CIs include zero. The gain looks concentrated on desktop (+0.40 pp) rather than mobile (+0.03 pp), but this is not statistically distinguishable. No claims by segment.

**Recommendation.** Ship Ranker v7, subject to confirming that the 0.005 bar is relative. After launch, monitor Abandonment, Revenue per User and Ad Click Rate. If the bar turns out to be absolute, the decision changes to Don't ship under the pre-registered rule.
