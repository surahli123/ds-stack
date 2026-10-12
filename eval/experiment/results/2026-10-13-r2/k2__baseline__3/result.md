Decision: Keep running

I also saved this readout as `readout.md` in the working directory.

**Ranker v7 readout**

**Bottom line.** The pooled lift on Successful Search Rate (SSR) is real and no guardrail is hurt. But the daily effect is fading, and by days 10–12 it is below the pre-registered bar with a confidence interval (CI) that includes zero. The pooled number is an average over a shrinking effect, so we can't yet say what the lasting lift is.

**Primary metric (pulse dated 2026-09-25, no CUPED, 95% CI)**
- Control is 0.4120 and Test is 0.4153. The absolute change is +0.00334 (CI +0.0016 to +0.0050). The relative change is +0.81% (CI +0.41% to +1.21%), with p = 7e-5.
- The pre-registered bar is 0.005, and the rule is that the point estimate must reach it. The prereg doesn't say whether the bar is absolute or relative.
  - Read as relative, it passes (+0.81% vs 0.5%). That is probably what was meant, since the guardrail margins and the daily series are relative.
  - Read as absolute, it fails (+0.0033 vs 0.005).
  - The team should confirm which at the review.

**The effect decays**

| Day | Relative effect | 95% CI |
|---|---|---|
| 1 | +1.50% | +0.9% to +2.1% |
| 5 | +1.00% | +0.4% to +1.6% |
| 8 | +0.70% | +0.1% to +1.3% |
| 10 | +0.52% | −0.08% to +1.12% |
| 12 | +0.40% | −0.2% to +1.0% |

- The decline is steady, at roughly 0.1 percentage point per day.
- The pooled +0.81% is weighted toward the early days. This looks like a novelty effect, and shipping on the pooled number could overstate the lasting benefit by about 2x.
- The daily series has only 12 points, so it may not cover the full 14-day plan.

**Guardrails.** All four are inside their margins, reading the margins as relative.

| Metric | Change | CI half-width | Margin |
|---|---|---|---|
| Latency p95 | +0.2% | ±0.5% | 2% |
| Abandonment | +0.1% | ±0.6% | 1% |
| Zero Result Rate | 0.0% | ±1.4% | 3% |
| Revenue per User | −0.1% | ±0.7% | 1% |

**Secondary and segment results (exploratory)**
- No secondary metric is significant, so nothing else corroborates the SSR lift.
- A few segments look off: Desktop SSR is −0.79% (p = 0.07) and Tail-query clicks per user are −2.25% (p = 0.004). Head- and Tail-query CTR are up about 1.4% each.
- There are about 60 segment metrics with no multiple-comparison correction, so these are hypotheses, not findings. The tail-click drop is worth watching.

**Hygiene.**
- The exposure balance check passed, and the audit log is empty (no mid-flight changes).
- The pulse is stale. It is dated 2026-09-25, but the experiment started around 2026-09-12 and is still active on 2026-10-12, well past the planned 14 days.

**Next steps**
1. Confirm whether the 0.005 bar is absolute or relative.
2. Pull a fresh pulse and extend the daily series to see whether the decay flattens above 0.5% or goes to zero.
3. Agree now on the ship criterion: the plateau (or last-7-day) effect is at or above the bar, and the guardrails still hold.
4. If the effect plateaus around 0.4%, it falls below the bar. The call is then don't ship at this bar, or a documented decision to accept a smaller win.