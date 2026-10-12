Decision: Ship

# Ranker v7: launch readout

**Recommendation: ship.** The pre-registered primary metric cleared its bar and no pre-registered guardrail was breached. There are two non-pre-registered signals (below) that the review should see before it agrees.

## Setup (checks)
- Ran 2026-09-12 to 2026-09-26 (14 days, as planned). Pulse is dated 2026-09-25. Allocation is 20%, split 50/50.
- 1,000,000 users per arm, above the 900,000 planned. The exposure-balance health check passed.
- Control and test differ only in `ranker_model` (v6 vs v7), which is the intended parameter. `snippet_length` is the same in both arms.
- The audit log is empty, so there were no mid-run config changes.
- Pulse was requested with CUPED off at 95% CI, matching the pre-registration. No sequential testing or Bonferroni correction was applied, which is fine for a single fixed-horizon primary.

## Primary: Successful Search Rate (pre-reg bar: +0.5%, point estimate must reach it)
| | Control | Test | Abs. change | Relative change | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | +0.0033 (±0.0016) | **+0.81%** (95% CI about +0.41% to +1.21%) | 7e-5 |

- The point estimate (+0.81%) is above the +0.5% bar, and the result is statistically significant.
- **Assumption:** I read the bar as a relative lift. The guardrail margins in the same file, such as 2% on p95 latency in ms, can only be relative, and Pulse reports `percentChange` as a fraction.
- If the bar was meant as an absolute +0.005, the result (+0.0033) misses it and the call becomes Don't ship. Please confirm which was meant.
- The lower end of the CI (+0.41%) is below the bar. The pre-registered rule is point-at-bar, so this does not block shipping. The true lift could be a bit under 0.5%.

## Pre-registered guardrails (95% CI worst end vs. margin)
| Guardrail | Change (relative) | Worst end of CI | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.2% (±0.5%) | +0.7% | 2% | Pass |
| Abandonment Rate | +0.1% (±0.6%) | +0.7% | 1% | Pass |
| Zero Result Rate | 0.0% (±1.4%) | +1.4% | 3% | Pass |
| Revenue per User | -0.1% (±0.7%) | -0.8% | 1% | Pass |

All four pass under either a relative or an absolute reading of the margins. Revenue is the tightest, with its lower bound at -0.8% against a 1% margin.

## Things the review should know (not pre-registered, so not decision rules)
1. **Clicks per User is down 1.2%** (3.60 to 3.56, p=0.003).
   - The same direction shows up in Queries per User (-0.5%) and Sessions per User (-0.4%), but neither is significant.
   - CTR and Long Click Rate are flat.
   - This was 1 of 56 secondary and segment metrics. Roughly 3 would reach p<0.05 by chance, and p=0.003 would not survive a Bonferroni correction across 56 (about 0.19).
   - It could be benign (users find answers with fewer clicks) or an engagement loss. I can't tell from this data. Watch it in a post-launch holdout.
2. **The segment cuts do not reproduce the headline lift.**
   - Successful Search Rate by segment: Mobile +0.0003, Desktop -0.0069 (p=0.003), Head +0.0002, Tail -0.0011, Navigational -0.0029, Informational +0.0014. None of these is above +0.0014, yet the overall change is +0.0033.
   - The segment control means also don't average to the overall 0.412. Navigational and Informational, for example, are both well below it.
   - So either the segment metrics are defined on different denominators than the headline, or the arms differ in segment mix. I haven't resolved which.
   - Desktop -1.3% (p=0.003) is the one segment worth a follow-up. Across about 48 segment tests, one at p=0.003 is not strong evidence on its own.
   - I'd ask the metrics owner to confirm the segment definitions before launch. If the headline is a mix artifact, the primary result would need to be re-checked.
3. Other secondary metrics (Reformulation, Time to First Click, Ad Click Rate, Pagination, Autocomplete) show nothing notable.

## Recommendation and follow-up
- Ship v7 to 100% per the pre-registered rule.
- Keep a small holdout or monitor post-launch for Clicks per User, Desktop Successful Search Rate and Revenue per User.
- Resolve the bar's units and the segment-definition question at the review. Either one could change the decision.
