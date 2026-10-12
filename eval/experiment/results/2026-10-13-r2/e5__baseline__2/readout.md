Decision: Don't ship

# Ranker v7 – launch readout

**Bottom line:** v7 does not meet the pre-registered ship criteria. The pre-reg requires *both* primaries (Successful Search Rate, Long Click Rate) to have a point estimate at or above the 0.005 bar. Long Click Rate misses it by a wide margin, and its 95% CI excludes the bar. SSR is a real but small win, and it also falls short of the bar if the bar is read as absolute.

## Validity
- A/B, userID, 50/50 split in a 20% allocation. Exposures balanced (1,000,000 vs 1,000,000; Statsig check PASSED).
- 14 days (2026-09-12 to 2026-09-25), as planned. Units per arm are 1.0M against 0.9M planned. The audit log is empty, so there were no mid-test config changes. The only parameter that differs is `ranker_model`, which is the intended one (`snippet_length` is identical).
- Pulse was pulled without CUPED at 95% CI. There is no sequential testing, and I did not adjust for multiplicity. Only two primaries were pre-registered. I used the decision rule exactly as written.
- Config gap: the Statsig config lists only SSR as a primary, while the pre-reg has two. Long Click is still the pre-registered primary, so I judged it as one.

## Primary metrics (bar = 0.005)
| Metric | Control | Test | Abs. change (95% CI) | Rel. change | p | Meets bar? |
|---|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | +0.0033 (±0.0016) → [+0.0017, +0.0050] | +0.81% | 7e-5 | Not as an absolute bar (0.0033 < 0.005). Reading 0.005 as relative, 0.81% > 0.5%. |
| Long Click Rate | 0.2210 | 0.2213 | +0.0003 (±0.0013) → [-0.0011, +0.0016] | +0.12% | 0.70 | **No.** The upper CI bound (+0.0016) is below the bar, on either reading. Relative +0.12% ± 0.6% also stays under 0.5%. |

The pre-reg doesn't state whether the bar is absolute or relative. SSR passes only under the relative reading. The decision doesn't depend on this, because Long Click fails under both and the rule is "all". The review should still settle the unit, because it affects how SSR is described.

## Guardrails (pre-reg margins)
All four are within margin. Each is judged by whether the worse end of the CI stays inside the margin.
- Latency p95: +0.2% (±0.5%) against a 2% margin. OK.
- Abandonment Rate: +0.1% (±0.6%), where an increase is worse, against a 1% margin. OK.
- Zero Result Rate: 0.0% (±1.4%) against a 3% margin. OK.
- Revenue per User: -0.1% (±0.7%) against a 1% margin. OK.

The guardrails are not the reason for this decision.

## Secondary and segment results (exploratory only)
- About 55 secondary and segment metrics were tested without correction. At 5% we'd expect around 3 to be nominally significant by chance. Four are:
  - Queries per User +1.07% (p=0.02)
  - CTR on tail queries +1.5% (p=0.016)
  - Long Click on head queries -1.2% (p=0.04)
  - the SSR primary itself
- None of the three secondary hits is a pre-registered claim, and they point in different directions. I would not use them to support or oppose a ship.
- SSR on head queries is -0.3pp (n.s., p=0.14), and Long Click on head and informational queries is negative. That is worth a look as a hypothesis for v8, not as a finding.

## What I'd tell the review
1. Don't ship v7 as specified. The pre-reg's "all primaries at the bar" rule is not met, because Long Click shows no lift of the required size.
2. SSR improved by about +0.33pp (+0.8% relative), with no guardrail harm. If the team wants to ship on SSR alone, that is a change to the pre-registered decision rule and needs an explicit sign-off from the owners, not a data reading.
3. More run time would not change the call. Long Click's CI already excludes the bar at 1M per arm.

## Caveats
- One experiment, no CUPED, and no novelty or time-trend view in the Pulse snapshot (a single ds).
- No pre-registered analysis of segments exists, so none can drive the decision.
