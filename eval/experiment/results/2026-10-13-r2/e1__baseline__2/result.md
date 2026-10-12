Decision: Don't ship

# Ranker v7: launch readout

**Why:** Ranker v7 improves Successful Search Rate, but by less than the pre-registered bar of +0.005. The pre-registration requires the point estimate to reach the bar, and it doesn't.

## Primary metric

| | Control | Test | Absolute lift | 95% CI | Relative lift | p |
|---|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | **+0.0033** | [+0.0017, +0.0050] | +0.81% | 7e-5 |

- The lift is real and statistically significant.
- It is about two-thirds of the +0.005 bar.
- The CI upper end is +0.00498, so the data also exclude the effect being at or above the bar. That is only just, so call it "very unlikely to reach the bar" rather than "ruled out".

## Guardrails

Pulse reports relative changes. I assumed the pre-registered margins are relative too, which the prereg doesn't state.

| Guardrail | Change | 95% CI half-width | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.2% | ±0.5% | 2% | Clear |
| Zero Result Rate | 0.0% | ±1.4% | 3% | Clear |
| Revenue per User | −0.1% | ±0.7% | 1% | Clear |
| Abandonment Rate | +0.6% (worse) | ±1.0% | 1% | **Not cleared** |

- Abandonment is not significant (p=0.24), but the worst-case end of its CI is about +1.6%, which is past the 1% margin.
- Even with a larger lift, this guardrail could not be called safe from this data.

## Exploratory findings, not decision-relevant

- Pulse includes about 50 segment metrics (device, query head/tail, query intent) that were not pre-registered.
- Two of them cross p<0.05 in the bad direction: Informational Successful Search Rate (−0.0035, p=0.036) and Informational CTR (p=0.044).
- Desktop time-to-first-click is also worse (p=0.027).
- With this many looks, a few such results are expected by chance. Treat them as hypotheses to check, not as findings.
- The segment means don't reconcile with the overall metric. Mobile and Desktop control Successful Search Rate are 0.500 and 0.435, but the overall control is 0.412, which a weighted average of the two can't produce. Their lifts (−0.0036 and +0.0015) also both sit below the overall +0.0033. The segment definitions are probably different from the primary metric's, so I wouldn't read anything into the mobile/desktop split until that is explained.

## Experiment health and caveats

- Allocation is 50/50 within a 20% layer, with 1.0M users per arm (900k planned). The exposure-balance health check passed.
- The audit log is empty, so there were no mid-flight config changes.
- The only parameter that differs between arms is `ranker_model`, which matches the intent.
- The analysis was fixed-horizon (`sequentialTesting` is off), so the single look at the end is valid.
- The Pulse snapshot is dated 2026-09-25, day 14 of 14 (the experiment started 2026-09-12). The experiment still shows "active" today, 2026-10-12. If it kept running after the snapshot, the numbers are stale, and a fresh pull should be considered before the meeting. Exposure counts are exactly 1,000,000 per arm, which looks rounded, so I'd confirm them against the source.
- Pulse was requested with CUPED off, so these are unadjusted intervals.

## Recommendation

- Don't ship v7 on this evidence.
- If leadership wants to ship it anyway as a smaller-than-planned win, that is a business decision. It would need the pre-registered bar waived explicitly and the abandonment risk accepted.
- A better route is a follow-up that investigates the abandonment and Informational-query signals. It could also re-run with CUPED on to tighten the intervals.