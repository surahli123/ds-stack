Decision: Can't tell

# Ranker v7 launch readout

**Bottom line:** The unadjusted Pulse result clears the pre-registered bar, but the two arms already differed on the primary metric before launch by about the same amount. I can't separate the ranker's effect from that pre-existing gap. Don't ship on this readout. Re-run the analysis with pre-period adjustment first.

## Primary metric: Successful Search Rate (bar: +0.5% relative, point estimate)
| | Control | Test | Abs. diff | Rel. diff (95% CI) | p |
|---|---|---|---|---|---|
| Unadjusted (Pulse, CUPED off) | 0.4120 | 0.4153 | +0.00334 | **+0.81% (+0.41%, +1.21%)** | 7e-5 |

- Taken at face value this passes. The point estimate (+0.81%) is above the +0.5% bar, which is the prereg's ship rule (`point_at_bar`). The CI lower bound (+0.41%) is below the bar, though.
- **The pre-period gap is the problem.** prereg.json records a pre-period difference on this same metric of **+0.71% (CI +0.31%, +1.11%)**. That CI excludes zero (p about 0.0006). Randomized arms shouldn't differ that much before treatment.
- The Pulse figure is not adjusted for it, because it was pulled with `cuped: false`. Subtracting the pre-period gap leaves about **+0.10% ± 0.57%** (rough difference-in-differences, treating the two periods as independent). That is consistent with no effect and with an effect above the bar, so the data can't tell them apart.
- The exposure-balance health check passed, and the unit counts are equal (1,000,000 per arm). That check covers only the exposure counts, so it doesn't rule out a gap in the metric itself. I can't tell from these files why the arms differ at baseline. It could be a bucketing or salt problem, or the pre-period window could be a poor comparison. It needs checking either way.

## Guardrails (all within prereg margins, treated as relative)
Each upper or lower bound is the worst case from the Pulse 95% CI.

| Metric | Change (95% CI half-width) | Worst case vs. margin |
|---|---|---|
| Latency p95 | +0.2% (±0.5%) | +0.7% vs. 2% margin: pass |
| Abandonment Rate | +0.1% (±0.6%) | +0.7% vs. 1% margin: pass |
| Zero Result Rate | 0.0% (±1.4%) | +1.4% vs. 3% margin: pass |
| Revenue per User | −0.1% (±0.7%) | −0.8% vs. 1% margin: pass |

These are differences between arms, so the baseline gap affects them as well. The margins leave room, so they are less likely to flip the call.

## Supporting evidence
- Secondary metrics don't corroborate a gain. CTR (+0.16%), Long Click Rate (+0.23%), Reformulation Rate (−0.18%) and Clicks per User (+0.11%) are all small and not significant.
- Of the roughly 45 segment cuts, a few are nominally significant: Time to First Click for Desktop and Tail queries, and Clicks per User for Tail queries. Nothing is corrected for multiple comparisons, so I read these as noise, not findings.
- Mobile Successful Search Rate is −0.82% (p=0.11), against +0.51% on Desktop. That is not significant, but it is worth a look if the ranker goes forward.

## Setup checks
- The change log is empty, so nothing was altered mid-test. Control and Test differ only in `ranker_model`; `snippet_length` is 160 in both.
- Pulse data is dated 2026-09-25, which is day 14 of 14 (start 2026-09-12). Sequential testing is off, so one look at the planned end is valid.
- Sample is 1.0M per arm against 0.9M planned. The experiment is still marked `active` today (2026-10-12), well past the planned end. Any newer Pulse pull would be a later look than the prereg planned.

## Next steps before or at the review
1. Re-pull Pulse with CUPED on, using pre-period data. Alternatively, use the prereg's pre-period for a covariate-adjusted estimate.
2. Investigate why the arms differ at baseline: check assignment, the salt, and any overlap with other layer experiments.
3. Decide the call from the adjusted estimate against the +0.5% bar:
   - Ship if the adjusted point estimate is at or above +0.5% and the guardrails hold.
   - Don't ship or No effect if the adjusted estimate stays near +0.1%.
   - If the baseline gap can't be explained, rerun with fresh assignment.
