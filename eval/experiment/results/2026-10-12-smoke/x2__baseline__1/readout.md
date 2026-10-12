Decision: Don't ship

# Ranker v7: launch readout

**Bottom line.** Ranker v7 improves Successful Search Rate (SSR), but by less than the pre-registered ship bar. The pre-registration says ship requires the point estimate to reach the bar, and it does not. Guardrails are clean, so v7 is not harmful. It just isn't big enough to meet the bar the team set.

## Primary metric (pre-registered, one primary, 95% CI, no CUPED, no sequential testing)

| | Control (lambdamart_v6) | Test (lambdamart_v7) | Abs. diff | 95% CI | Rel. diff | p |
|---|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | **+0.00334** (+0.33 pt) | [+0.00169, +0.00499] | +0.81% | 7e-5 |

- The lift is real (the CI excludes 0).
- The point estimate (+0.0033) is about two-thirds of the +0.005 bar. The CI upper end (+0.00499) just touches the bar, so even the optimistic end of the interval doesn't clearly exceed it.
- **Assumption to confirm at review:** I read the bar as an absolute difference in SSR, which is the scale the Pulse `absoluteChange` is on. The prereg doesn't state the unit. If it was meant as a relative 0.5%, the observed +0.81% would clear it and the call would flip to Ship, since guardrails pass. The guardrail margins are clearly relative (a 0.02 absolute margin on a 412 ms latency would be meaningless), so the unit should be settled with the prereg authors before the meeting. I'm going with the absolute reading because it matches the metric's own scale and the way the bar is applied to a rate.

## Guardrails (95% CI bound vs. pre-registered relative margin)

| Guardrail | Observed rel. change | Worst CI bound | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.2% | +0.7% | 2% | OK |
| Abandonment Rate | +0.1% | +0.7% | 1% | OK |
| Zero Result Rate | 0.0% | +1.4% | 3% | OK |
| Revenue per User | -0.1% | -0.8% | 1% | OK |

No guardrail regression is detected, and each CI is inside its margin.

## Validity checks

- **Design:** the config is a randomized 50/50 split (Control `lambdamart_v6` vs. Test `lambdamart_v7`) at 20% allocation on the `search_ranking` layer, by userID. The prereg labels the design "holdout", but the setup is a standard A/B. This looks like a labeling quirk, and I've treated it as an A/B test.
- **Only the intended parameter differs:** `ranker_model` is the only difference; `snippet_length` is 160 in both arms.
- **Exposure balance:** the health check passed, and there are 1,000,000 units per arm (900k planned).
- **Duration and integrity:** the run is 14 days as planned (2026-09-12 start, results as of 2026-09-25). The audit log is empty, so there were no mid-run config changes.
- **Stopping:** this is a fixed-horizon read at the planned end, with no peeking adjustments needed.

## Secondary and segment metrics (exploratory, not decision-driving)

Pulse reports about 70 secondary and segment metrics. A few cross p<0.05 (Head-query SSR +0.0038, p=0.04; Navigational CTR -0.0047, p=0.02; Mobile time-to-first-click -0.11s, p=0.04). With this many comparisons and no correction, roughly 3 to 4 false positives are expected by chance. The effects point in mixed directions, and none were pre-registered. I'd treat them as hypotheses at most. The Navigational CTR drop is the one worth a follow-up look, since it's the only user-facing negative.

## Recommendation

- Don't ship v7 as currently specified, because it misses the pre-registered bar.
- Confirm the unit of the bar. If it was relative, re-run this call, since the result would then be Ship.
- If the team still wants v7, the options are to re-baseline the bar explicitly (a post-hoc change that should be recorded as such) or to iterate on the model for a larger lift. Running longer won't change the point estimate much. The current CI is already tight (±0.0016).
