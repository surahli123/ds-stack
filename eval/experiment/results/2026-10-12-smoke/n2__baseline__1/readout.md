Decision: No effect found

# Ranker v7 – launch review readout

**Bottom line:** Ranker v7 did not reach the pre-registered bar on its primary metric, and the data rule out an effect that large. Don't launch on this evidence. This is not a "keep running" case: the planned 14 days have run and the interval is already narrow.

## Primary metric (pre-registered: Successful Search Rate, ship only if the point estimate is at least +0.5pp)
| | Control | Test | Diff (abs) | 95% CI | p |
|---|---|---|---|---|---|
| Successful Search Rate | 41.20% | 41.22% | +0.025pp | [-0.099pp, +0.148pp] | 0.70 |

- The point estimate is +0.025pp, about a twentieth of the +0.5pp bar. The CI upper bound (+0.148pp) is also well below the bar, so a bar-sized win is excluded, not just unproven.
- Relative change is +0.06% (±0.3%).

## Guardrails (pre-registered margins, 95% CIs)
No guardrail is harmed. Each CI sits well inside its margin. Margins are read as relative, which is my assumption since prereg.json doesn't say. Abandonment passes under either reading.

| Metric | Change | 95% CI half-width | Margin |
|---|---|---|---|
| Latency p95 | +0.2% (+0.8 ms) | ±0.5% | 2% |
| Abandonment Rate | +0.1% | ±0.6% | 1% |
| Zero Result Rate | 0.0% | ±1.4% | 3% |
| Revenue per User | -0.1% | ±0.7% | 1% |

Because the primary misses, the guardrails don't change the decision.

## Experiment validity
- Run as planned: 14 days (2026-09-12 to 09-25), A/B on userID, 50/50, 1.0M users per arm (plan: 0.9M).
- The balanced-exposure health check passed.
- The audit log is empty, so there were no mid-test config changes.
- The only parameter that differs between arms is ranker_model, as intended (snippet_length is 160 in both).
- Pulse ran without CUPED at 95% confidence, and no sequential testing or multiplicity correction was applied. The primary is a single pre-registered test, so none is needed for it.

## Secondary and exploratory (not decision-relevant)
- Most of the 56 secondary and slice metrics show nothing. CTR is +0.15pp (p=0.052) and is not corroborated by Long Click Rate (p=0.93) or by the primary.
- **Tail queries:** Successful Search Rate is +1.46pp (p<0.001). I'd treat this as a lead, not a result. It is one slice among about 56, it was not pre-registered, and it sits oddly against the flat overall result and the flat head, navigational and informational slices. Any follow-up should be pre-registered as its own test, for example a tail-targeted ranker.
- Navigational CTR (-0.55pp, p=0.03) and Mobile Long Click Rate (p=0.06) are borderline. With this many slices, a couple of p<0.05 hits are expected by chance.

## Recommendation
1. Don't ship v7 as a general search-quality win.
2. Don't extend the run. At this sample size the CI half-width is about 0.12pp, so more days would not change the conclusion against a 0.5pp bar.
3. Optionally, pre-register a follow-up on tail queries if the team cares about that segment.
