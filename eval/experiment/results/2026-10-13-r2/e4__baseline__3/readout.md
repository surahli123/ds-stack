Decision: Don't ship

# Ranker v7 readout

**Bottom line:** v7 improves Successful Search Rate (SSR) on the searches it touches. The pre-registered bar is on overall SSR, and v7 is well short of it. The shortfall is a matter of scale, not noise, so more runtime won't fix it.

## Primary metric against the pre-registered bar
- Pulse reports SSR on **triggered searches only**: control 0.4120, test 0.4198, **+0.00783 absolute** (+1.9% relative), 95% CI ±0.00247, p<0.001.
- The pre-reg bar is **+0.005 overall**, and ship requires the *point estimate* to reach it. The raw Pulse number (0.0078 > 0.005) compares a triggered-population effect to an overall bar, so it isn't a valid comparison.
- Per the prereg note, triggered searches are 10% of searches and 20.5% of control successes. Diluting to all searches:
  - Absolute: 0.00783 × 10% ≈ **+0.0008** (95% CI ≈ +0.0005 to +0.0011).
  - Relative: 1.9% × 20.5% ≈ **+0.39%** (CI ≈ +0.27% to +0.51%).
- On either reading the point estimate is below the bar, and the upper CI bound is too. The absolute reading is about 6× short. Under the relative reading the upper bound only just touches 0.5%.
- I assumed the bar is an absolute overall difference. If the team meant relative, the result is still below the bar, though closer.

## Guardrails (all within margin, 95% CIs, relative)
| Metric | Change | Margin | Status |
|---|---|---|---|
| Latency p95 | +0.2% ±0.5% | 2% | OK |
| Abandonment | +0.1% ±0.6% | 1% | OK |
| Zero Result | 0.0% ±1.4% | 3% | OK |
| Revenue/User | −0.1% ±0.7% | 1% | OK |

Guardrails would not block a ship, but the primary does.

## Validity
- Design is a clean A/B on userID, 50/50, with the exposure balance check passed. There are 1.0M users per arm against 900k planned.
- The run covers 2026-09-12 to 09-25, the planned 14 days.
- The audit log is empty, so there were no mid-run config changes.
- There was no sequential testing or peeking issue, because this is a single fixed-horizon read.

## Things not to over-read
- **Queries per User −1.0% (p=0.024)** is a secondary, non-guardrail metric. Roughly 70 metrics and segments were read with no multiplicity correction, so about 3–4 nominal p<0.05 hits are expected by chance. It is worth watching but is not evidence of harm.
- The segment cuts (mobile/desktop, head/tail, navigational/informational) show no consistent pattern. The few nominal hits (Desktop time to first click, Informational reformulation) are consistent with chance. Don't build a narrative on them.
- CTR, long-click rate and clicks per user are flat. The SSR lift is not corroborated by other engagement metrics, which is plausible given their wide CIs, but I can't claim a broader benefit.

## Recommendation
Don't ship v7 on this evidence, because it misses the pre-registered bar. If the team wants to ship anyway, say that the bar is being waived. Don't present the triggered +0.0078 as clearing it. Options for the review:
1. Treat the bar as unmet and stop.
2. If the bar was meant to apply to the triggered population (contradicting the prereg note), decide that explicitly and record it as a deviation. Under that reading the lift passes and guardrails hold.
3. Widen the trigger so more searches are affected, then rerun. Dilution is the limiter.
