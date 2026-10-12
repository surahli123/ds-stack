Decision: Keep running

# Ranker v7 – launch review readout

**Bottom line.** The pooled lift on Successful Search Rate (SSR) is real, but it is shrinking every day since exposure. The latest day is below the pre-registered bar and no longer distinguishable from zero. I can't tell from this data whether a durable effect of at least the bar exists, so I recommend extending the test rather than shipping tomorrow.

## Primary metric (pre-registered: SSR, ship if point estimate ≥ 0.005)
- Pooled (Pulse, no CUPED, 95% CI, 1.0M units/arm): 41.20% → 41.53%, **+0.334 pp absolute (+0.81% relative)**, 95% CI +0.17 to +0.50 pp (p = 7e-5).
- **The bar's unit isn't stated in the prereg.** Read as relative (0.5%, same convention as the guardrail margins), the pooled point estimate passes (0.81%). Read as absolute (0.5 pp), it fails (0.33 pp, and even the CI upper bound only just reaches 0.50). The review should confirm which was meant. I assumed relative below.
- **Effect decays with days since exposure** (relative lift, daily file):

| Exposure day | 1 | 4 | 7 | 9 | 10 | 12 |
|---|---|---|---|---|---|---|
| Lift | +1.50% | +1.15% | +0.82% | +0.61% | +0.52% | +0.40% |
| 95% CI | 0.9–2.1 | 0.55–1.75 | 0.22–1.42 | 0.01–1.21 | −0.08–1.12 | −0.20–1.00 |

  The lift falls about 0.1 pp/day, and the CI includes zero from day 10. The pooled 0.81% is mostly a weighted average of the early, larger days. The day-12 estimate (0.40%) is below the 0.5% bar. This pattern fits a novelty/learning effect, which would mean the steady-state effect is smaller than the pooled number. A straight-line extrapolation reaches zero around day 19, but the daily CIs are wide (about ±0.6 pp), so a plateau at a small positive value is equally consistent with the data. The daily file stops at day 12, although the test ran 14 days (Sep 12 – Sep 25). Later exposure days are thin because few users have been exposed that long.

## Guardrails (95% CI vs. pre-registered margin, relative)
All are within margin, with no sign of harm, but the CIs are not tight enough to rule out small losses.
- Latency p95: +0.2% (CI ±0.5%), margin 2%.
- Abandonment rate: +0.1% (CI ±0.6%), margin 1%.
- Zero result rate: 0.0% (CI ±1.4%), margin 3%.
- Revenue per user: −0.1% (CI ±0.7%), margin 1%.

## Validity checks
- Design is a 50/50 A/B on userID, one parameter changed (`ranker_model`; `snippet_length` is identical in both arms). Exposure balance health check passed. Audit log is empty, so there were no mid-test config changes.
- Sequential testing is off. The test was read at its planned 14-day end, so there is no peeking problem. Bonferroni is off and there is one primary metric, so no multiplicity adjustment is needed for the primary.
- Secondary metrics (CTR, long clicks, reformulation, etc.) show no significant movement overall, so they neither corroborate nor contradict the SSR lift.

## Segment cuts (exploratory, not pre-registered)
About 60 segment × metric results were reported with no multiplicity correction, so a few nominal hits are expected by chance. Worth noting but not decision-driving:
- Tail queries: clicks per user −2.25% (p = 0.004), while tail CTR is up and tail SSR is −0.6% (n.s.). Desktop SSR −0.79% (p = 0.07) vs. mobile +0.63% (n.s.). Head-query CTR +1.4% (p = 0.009).
- None survives correction, but tail queries and desktop are worth a pre-specified look in the extension.

## Recommendation and decision rule
Don't ship on the pooled number. Keep the test running (target at least 2 more weeks) and decide on a pre-agreed rule, for example:
1. Ship if the lift for the most recent exposure days (e.g. days ≥ 12) has a point estimate ≥ the bar (confirmed unit) and the guardrails stay within margin.
2. Call it "no durable effect" if the late-day lift CI sits below the bar or around zero.
3. Pre-specify the tail-query and desktop checks as guardrail-style reads.

The cost of waiting is small, since there is no evidence of harm. The risk of shipping now is launching on a transient lift of about 0.4% or less.

Open items for the review: confirm the bar's unit (relative vs. absolute); obtain daily results beyond day 12.
