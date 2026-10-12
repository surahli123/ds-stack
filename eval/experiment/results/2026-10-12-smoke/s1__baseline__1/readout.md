Decision: Ship

# Ranker v7 – launch readout

**Recommendation:** Ship lambdamart_v7. The pre-registered primary clears its bar at the point estimate, and every pre-registered guardrail is within its margin.

## Primary (pre-registered, 95% CI, no CUPED)
| Metric | Control | Test | Abs. change | Rel. change | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | +0.0033 (CI ±0.0016: +0.0017 to +0.0050) | **+0.81%** (CI ±0.4pp: +0.41% to +1.21%) | 7e-5 |

- The pre-reg bar is +0.5% and the rule is `point_at_bar`, so the point estimate must reach the bar. +0.81% does.
- I read the bar as relative. The guardrail margins (2% on a 412 ms latency, for example) only make sense as relative, and the same convention fits the bar. If the bar was meant as an absolute +0.005, the point (+0.0033) would miss it. Please confirm the intent in the review.
- The lower CI bound (+0.41%) is under the bar. The pre-reg only requires the point at the bar, not the CI, so this isn't a failure. The true lift may be somewhat below 0.5%.

## Guardrails (relative change vs. pre-registered margin; all pass)
| Guardrail | Change (95% CI) | Margin | Status |
|---|---|---|---|
| Latency p95 | +0.2% (±0.5) | 2% | pass |
| Abandonment Rate | +0.1% (±0.6) | 1% | pass |
| Zero Result Rate | 0.0% (±1.4) | 3% | pass |
| Revenue per User | −0.1% (±0.7) | 1% | pass |

The worst-case CI bound is inside the margin for each guardrail, so none of them is merely inconclusive.

## Experiment health
- Design is a 50/50 A/B on userID, with 20% allocation. The only parameter that differs between arms is `ranker_model`, which is the intended one (`snippet_length` is 160 in both).
- Exposure balance check PASSED. Each arm has 1.0M units against 0.9M planned.
- The audit log is empty, so there were no mid-test config changes.
- Sequential testing is off, and the test ran to its planned 14-day duration (start 2026-09-12; the Pulse snapshot is dated 2026-09-25). There was no early peeking.

## Things to know (not blockers)
- **Reformulation Rate** (secondary, lower is better) is up 0.96% (p=0.018). Long Click Rate is down 0.55% (p=0.074). Both point the opposite way from a clean win. Pulse reports roughly 60 secondary and segment metrics with no multiplicity correction, so a few nominal p<0.05 results are expected by chance. Neither metric is pre-registered. They are worth watching after launch, but I don't treat them as evidence of harm.
- **Segments:** none of the Mobile/Desktop/Head/Tail/Navigational/Informational Successful Search Rate cuts is significant. Head queries are nominally negative (−0.64%, p=0.16). These are exploratory and underpowered, so I'm making no segment claims. If Head queries matter, check them in the post-launch holdout.
- The headline lift is real but modest. Plan on about +0.4% to +1.2% relative, not a fixed +0.8%.

## Suggested follow-up
Ship with a small long-term holdout. Monitor Reformulation Rate and Head-query Successful Search Rate.
