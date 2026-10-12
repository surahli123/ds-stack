Decision: Keep running

# Ranker v7 readout

**Bottom line.** The cumulative lift on Successful Search Rate (SSR) is real, and no guardrail is hurt. But the daily effect is decaying steadily, and by day 10–12 it is below the pre-registered bar with a CI that includes zero. The pooled number that passes (or fails) the bar is an average over a fading effect. We can't tell yet whether the steady-state lift is worth shipping. Keep the experiment running until the daily effect flattens.

## Primary: Successful Search Rate (pulse ds 2026-09-25, no CUPED, 95% CI)
- Control 0.4120, Test 0.4153. Absolute +0.00334 (CI +0.0016 to +0.0050), relative +0.81% (CI +0.41% to +1.21%), p = 7e-5. 1.0M units per arm (plan was 0.9M).
- The pre-registered bar is 0.005 and the rule is "point estimate at the bar". The prereg doesn't say whether the bar is absolute or relative:
  - Relative (+0.81% vs 0.5%): passes. This matches the relative guardrail margins and the relative daily series, so it is probably what was intended.
  - Absolute (+0.0033 vs 0.005): fails.
  - The team should confirm the unit at the review. I'd treat the relative reading as likely but not certain.

## Why the pooled number isn't enough: the effect decays
Daily relative effect by days since exposure:

| Day | Relative effect | 95% CI |
|---|---|---|
| 1 | +1.50% | +0.9% to +2.1% |
| 5 | +1.00% | +0.4% to +1.6% |
| 8 | +0.70% | +0.1% to +1.3% |
| 10 | +0.52% | −0.08% to +1.12% |
| 12 | +0.40% | −0.2% to +1.0% |

- The decline is monotonic, about 0.1 percentage point per day.
- From day 10 on, the CI includes zero and the point estimate is at or below the 0.5% bar.
- This pattern looks like a novelty effect, or a cohort mix effect. The pooled +0.81% is dominated by early days, and a long-run effect near or below 0.4% is plausible.
- Shipping on the pooled number risks overstating the lasting benefit by about 2x.
- Caveat: the daily series has 12 points and the pulse covers the whole window. It isn't clear that the 14-day plan was fully observed.

## Guardrails (all inside prereg margins)
The margins are read as relative.

| Metric | Change | CI half-width | Margin |
|---|---|---|---|
| Latency p95 | +0.2% (412.8 vs 412 ms) | ±0.5% | 2% |
| Abandonment | +0.1% | ±0.6% | 1% |
| Zero Result Rate | 0.0% | ±1.4% | 3% |
| Revenue per User | −0.1% | ±0.7% | 1% |

The worst-case CI bound is within margin for all four. Zero Result Rate is a null result, but its interval is wide relative to the margin, so it is not a concern.

## Secondary and segment results (exploratory)
- Secondary metrics (CTR, long clicks, reformulation, queries and sessions per user) are all non-significant, so there is no corroboration of the SSR lift beyond SSR itself. This is worth noting because the SSR lift rests on a single metric.
- Desktop SSR −0.79% (p = 0.07) and Tail-query clicks per user −2.25% (p = 0.004) look negative, while Head-query CTR +1.4% and Tail-query CTR +1.4% (p = 0.009 and 0.02) look positive.
- There are roughly 60 segment metrics, with no Bonferroni correction and no segment prereg. A few p < 0.05 results are expected by chance. Treat these as hypotheses, not findings. The tail-click drop is worth watching in the longer run.

## Experiment hygiene
- Exposure balance health check passed. Audit log is empty, so there were no mid-flight config changes. Allocation is 20% with a 50/50 split, and the only parameter that differs is `ranker_model`, as intended.
- The pulse snapshot is dated 2026-09-25, but the experiment is still "active" on 2026-10-12, which is past the planned 14 days (started ~2026-09-12). The results are stale. Refresh the pulse first.

## Recommendation / next steps
1. Confirm whether the 0.005 bar is absolute or relative.
2. Pull a fresh pulse. Re-cut the daily series with more days, and check whether the decay flattens above 0.5% (a ship case) or reaches zero (a novelty effect).
3. Ship criterion, to agree on before looking: the plateau (or last-7-day) effect has a point estimate at or above the bar, and the guardrails still hold.
4. If the effect plateaus at about 0.4%, below the bar, the answer is "don't ship at this bar" (or a conscious, documented decision to accept a smaller win).
