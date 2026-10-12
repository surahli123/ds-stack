Decision: Keep running

# Ranker v7 readout

**Bottom line:** The pooled result clears the pre-registered bar, but the effect is shrinking steadily with time since exposure. The latest days sit below the bar and their CI includes zero. We can't tell whether the steady-state lift is worth shipping, so I recommend extending the test rather than shipping on the pooled number.

## Primary: Successful Search Rate (pre-reg: increase, ship if the point estimate ≥ 0.005 bar)
- Control 41.20% → Test 41.53%. Abs +0.33 pp (95% CI +0.17 to +0.50 pp), relative **+0.81%** (CI ±0.40%), p = 7e-5. 1.0M users per arm, no CUPED, fixed horizon (pulse ds 2026-09-25, day 14).
- Reading the bar as relative (+0.5%, the same units as the guardrail margins), the pooled point estimate passes: 0.81% vs 0.5%. The pre-reg doesn't state the unit. If it meant an absolute +0.5 pp, this fails (0.33 pp, and the CI tops out right at 0.50). Someone should confirm the intended unit.

## Why not ship: the effect decays
Daily effect by days since exposure (relative lift, 95% CI):

| Day | 1 | 4 | 7 | 9 | 10 | 12 |
|---|---|---|---|---|---|---|
| Lift | +1.50% | +1.15% | +0.82% | +0.61% | +0.52% | **+0.40%** |
| CI | 0.9–2.1 | 0.55–1.75 | 0.22–1.42 | 0.01–1.21 | −0.08–1.12 | **−0.20–1.00** |

- The decline is monotonic, about 0.06–0.1 pp per day, with no sign of flattening by day 12.
- The pooled +0.81% is an average over early, inflated days. This is the pattern of a novelty or learning effect. The long-run effect is plausibly below the 0.5% bar, and possibly near zero.
- Day 10 onward, the daily CI includes 0. Day 12 is below the bar.
- The series has 12 points although the plan was 14 days, so I haven't seen days 13–14.

## Guardrails (margins from pre-reg, treated as relative)
All pass, with no evidence of harm. Intervals are wide enough that small harms aren't excluded.

| Metric | Change (rel.) | 95% CI half-width | Margin |
|---|---|---|---|
| Latency p95 | +0.2% (412.0 → 412.8 ms) | ±0.5% | 2% |
| Abandonment Rate | +0.1% | ±0.6% | 1% |
| Zero Result Rate | 0.0% | ±1.4% | 3% |
| Revenue per User | −0.1% | ±0.7% | 1% |

## Health and integrity
- Exposures balanced (health check PASSED), 50/50 split, 1.0M per arm (plan was 0.9M).
- The audit log is empty, so there were no mid-test config changes.
- Only `ranker_model` differs between arms. `snippet_length` is identical, so there is no confound.

## Secondary and segment results: don't over-read
There are about 70 secondary and segment metrics, with no multiplicity correction. The few nominal hits are consistent with chance:
- CTR Head (+0.52 pp, p = 0.009) and CTR Tail (p = 0.02).
- Clicks per User Tail (−0.094, p = 0.004), which points the opposite way.
- No segment of the primary shows a significant effect: Desktop is −0.24 pp (p = 0.07) and Head is +0.42 pp (p = 0.09).

None of these should drive the decision. Overall CTR and Long Click Rate are flat, so the primary's gain isn't corroborated by the engagement metrics.

## Recommendation and next steps
1. Keep the experiment running. It is still `active` in config.
2. Re-pull Pulse. The current results are from 2026-09-25, and the test started 2026-09-12.
3. Look at the latest exposure-day effect and the days-since-exposure curve. Ship if the latest ≥ ~0.5% relative, with a CI excluding harm, and the curve has flattened. Don't ship if the curve keeps falling toward zero.
4. Confirm whether the 0.005 bar is relative or absolute.
5. Consider a holdout of the ranker v6 control after launch to measure the long-run effect.
