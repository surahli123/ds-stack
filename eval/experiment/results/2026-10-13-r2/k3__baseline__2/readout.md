Decision: No effect found

# Ranker v7: launch review readout

**Recommendation:** Don't launch v7 on this evidence. The ranker does not move Successful Search Rate by anywhere near the pre-registered bar. No guardrail is harmed, so there is no safety reason to roll it back beyond the lack of benefit.

## Primary metric (pre-registered: Successful Search Rate, ship only if the point estimate is at least +0.005 absolute)
| | Control | Test | Diff (abs) | 95% CI | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4125 | +0.00049 (+0.12% rel) | [-0.0015, +0.0025] | 0.62 |

- The point estimate is about a tenth of the bar. The CI upper end (+0.0025) is also below the bar, so the data rule out an effect of the size the team needed.
- The CI includes zero. v7 could be mildly positive or mildly negative, at most about ±0.2 points.

## Guardrails (margins from prereg, read as relative changes)
All four are within margin. The CI is the Pulse 95% interval, and each is checked against the margin in the harmful direction.
| Metric | Change (rel) | 95% CI half-width | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.2% | ±0.5% | 2% | OK |
| Abandonment Rate | +0.1% | ±0.6% | 1% | OK |
| Zero Result Rate | 0.0% | ±1.4% | 3% | OK |
| Revenue per User | -0.1% | ±0.7% | 1% | OK |

These show no harm. They also don't prove the metrics are unchanged, only that harm beyond the margin is unlikely.

## Experiment validity
- Design is a plain A/B test on userID. Control and test are 50/50 in a 20% layer allocation. Only `ranker_model` differs between arms (`snippet_length` is identical), as intended.
- Exposure balance check passed. Both arms have 1,000,000 units against 900,000 planned, and the run is 14 days as planned (started 2026-09-12; Pulse ds 2026-09-25).
- The audit log has no changes, so there was no mid-test reconfiguration.
- Pulse used no CUPED, 95% confidence, no sequential testing and no Bonferroni correction. The result is a single fixed-horizon read.

## Secondary and segment metrics (exploratory, not a basis for a decision)
Pulse reports about 70 secondary and segment metrics with no multiplicity correction. The few nominal hits are consistent with chance at that count, and they point in different directions:
- Worse: Clicks per User on mobile (-0.093, p=0.011), SSR on Navigational queries (-0.0039, p=0.039), Time to First Click on Head queries (+0.14s, slower, p=0.031).
- Better: Clicks per User on Informational queries (+0.052, p=0.033).
- Near threshold: SSR on Desktop (-0.0043, p=0.065) and overall Clicks per User (-0.028, p=0.056).

None of these were pre-registered, and none survive correction. Overall, clicks and CTR lean slightly down rather than up. That is the opposite of the hypothesis and doesn't suggest a hidden win. A follow-up could look at Navigational and Desktop queries, but treat that as hypothesis-generating only.

## Next steps
- Don't ship v7 as is. The experiment answered its question: no lift at the +0.5 point level.
- If v7 has other reasons to ship (cost, maintainability), the guardrails say it is safe at the margins above. That would be a separate decision from this A/B result.
- Any further iteration should aim for a larger effect, or pre-register a smaller bar with matching sample size. Detecting about ±0.2 points needs roughly the current sample.
