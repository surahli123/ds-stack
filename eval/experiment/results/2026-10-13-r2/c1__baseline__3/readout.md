Decision: Can't tell

# Ranker v7 readout

**Short version:** On the pre-registered analysis, v7 meets the ship rule. But the experiment config shows a traffic split that doesn't match the Pulse unit counts, and that split is far too uneven to be chance. Until someone explains the mismatch, I can't vouch for the result. If the split turns out to be benign, the call is **Ship**.

## Problem: possible sample ratio mismatch (SRM)
- experiment.json lists exposures of Control 1,010,000 and Test 990,000. The design is 50/50. That is a 50.5/49.5 split with n≈2M, which gives chi-square ≈ 200 (z ≈ 14) and p well below 1e-30. Chance can't produce that.
- The same file reports the `has_balanced_exposures` health check as PASSED. That contradicts the numbers next to it.
- Pulse (ds 2026-09-25) analyzed exactly 1,000,000 units per arm. The totals match, but the split differs from the config's exposures.
- I can't tell from these files which count is right. The Pulse units may come from a different cut or definition than the config exposures. If the config's split is real, the arms are not comparable and the lift below could be an artifact.
- **Ask:** have the owner check the raw assignment and exposure counts by arm, and confirm the health-check status in the console. This is a quick check.

## Primary metric (Successful Search Rate, pre-registered)
| | Control | Test | Abs. change | Relative change | 95% CI (relative) | p |
|---|---|---|---|---|---|---|
| Successful Search Rate | 41.20% | 41.53% | +0.334 pp | +0.81% | +0.41% to +1.21% | 7.2e-05 |

- Bar from the prereg: 0.005, with ship requiring the **point estimate** to be at or above the bar. I read the bar as a relative 0.5%, because the guardrail margins in the same file only make sense as relative values. The point estimate of +0.81% clears it.
- The CI's lower end (+0.41%) is below the bar. The prereg does not require the CI to clear it, so this doesn't block shipping. It does mean the true lift could be smaller than the bar.
- If the bar was meant as an absolute 0.5 pp, the point estimate (+0.33 pp) misses it and the answer becomes Don't ship. Please have the team confirm the intended unit.
- Pulse was requested with CUPED off at 95% confidence, matching the prereg's 95% CI. I re-derived the CI and p-value from the reported standard errors, and they agree.

## Guardrails (prereg margins read as relative)
Each guardrail is checked on its CI bound against its margin.

| Metric | Change | Worst CI bound | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.2% (412.0 → 412.8 ms) | about +0.7% | 2% | OK |
| Abandonment Rate | +0.1% | about +0.7% | 1% | OK |
| Zero Result Rate | 0.0% | +1.4% | 3% | OK |
| Revenue per User | -0.1% | about -0.8% | -1% | OK |

None of the four guardrails is breached.

## Other things I looked at
- The audit log is empty, so there were no mid-flight config changes. Control and Test differ only in `ranker_model`, as intended. `snippet_length` is the same in both arms.
- Pulse has 56 secondary metrics, with no multiplicity correction. Two are nominally significant: Clicks per User -1.0% (p=0.014) and Abandonment Rate on tail queries +1.7% relative (p=0.034). Expect a couple of such hits by chance among 56 metrics. Neither is a prereg metric or guardrail. Clicks per User falling while search success rises is worth a glance but is not a blocker.
- The segment views (mobile, desktop, head, tail, navigational, informational) show no consistent pattern of harm.
- The config says status "active" and the planned 14 days have passed. Pulse is as of 2026-09-25, so the data is about two and a half weeks old.

## Recommendation for review
1. Resolve the exposure and SRM discrepancy first.
2. Confirm the bar is relative.
3. If the exposures are balanced and the bar is relative, ship v7. The prereg criteria are met and no guardrail is breached.
