Decision: Can't tell

# Ranker v7 readout

**Bottom line:** The raw Pulse result clears the pre-registered bar, but the two arms already differed by about the same amount *before* launch. We can't tell how much of the +0.81% is the ranker. We recommend neither shipping nor killing on this data until the pre-period gap is explained.

## Raw result (Pulse, no CUPED, 95% CI)
Successful Search Rate (primary; bar = +0.5% relative, "point estimate at bar"):
- Control 0.4120, Test 0.4153: +0.00334 absolute, **+0.81% relative, CI [+0.41%, +1.21%]**, p = 7e-5.
- Taken at face value this passes: the point estimate is above the 0.5% bar, and the lower CI bound is below it, which the prereg's point-estimate rule allows.
- The test ran the planned 14 days (2026-09-12 to 09-25). It has 1.0M units per arm against 900k planned. The exposure health check passed, with a 50/50 split.

## Why I don't trust it: pre-period imbalance
prereg.json records a pre-launch difference between the arms on the same metric: **+0.71% relative, CI [+0.31%, +1.11%]**. That interval excludes zero, so the arms were not comparable before the ranker was applied.
- The post-launch lift (+0.81%) is almost entirely the same size as that pre-existing gap.
- Subtracting the gap gives a rough change-in-difference estimate of about **+0.10%**. Its approximate CI is [-0.5%, +0.7%] (my arithmetic, treating the two intervals as independent). That includes zero and includes the 0.5% bar.
- So the data are consistent with "no effect" and with "an effect at or above the bar". They can't separate the two.
- Pulse was requested with CUPED off. A pre-period-adjusted analysis (CUPED, or a diff-in-diff on the same users) is the obvious next step. It might settle this, but I haven't seen its output.

## Guardrails (relative change, 95% CI vs prereg margin)
These all pass on the raw numbers. They are not the issue.
| Metric | Change | CI half-width | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.2% (412.0 to 412.8 ms) | ±0.5% | 2% | OK |
| Abandonment | +0.1% | ±0.6% | 1% | OK |
| Zero Result Rate | 0.0% | ±1.4% | 3% | OK |
| Revenue per User | -0.1% | ±0.7% | 1% | OK |

## Secondary and segment metrics
- No other metric moves convincingly. CTR, Long Click, Reformulation, Queries, Sessions and Ad Click are all flat (p > 0.4).
- The 54 segment cuts were not pre-registered. Three have nominal p < 0.05: Time to First Click for Desktop and Tail Queries (both improved), and Clicks per User for Tail Queries (up).
- With this many looks, a few such hits are expected by chance. I treat them as noise, not evidence.
- The Successful Search Rate segments (mobile, desktop, head, tail, navigational, informational) are all non-significant. Mobile is -0.8% (p = 0.11) and desktop +0.5% (p = 0.31).

## Config and audit
- Only `ranker_model` differs between the arms. `snippet_length` is 160 in both.
- The audit log is empty, so there were no mid-test config changes.
- The experiment is still marked "active".

## Recommended next steps
1. Find out why the arms differed pre-launch. Check the assignment and salt, the layer `search_ranking` overlap with other experiments, and whether the pre-period was measured on the same exposed users.
2. Rerun Pulse with CUPED, or compute a pre/post difference-in-differences. If the adjusted lift is at or above +0.5% with a CI clear of zero, the call becomes Ship. If it is near +0.1%, the call becomes No effect found.
3. If the imbalance can't be explained, rerun with a fresh randomization. Under the current rule the decision is Can't tell.
