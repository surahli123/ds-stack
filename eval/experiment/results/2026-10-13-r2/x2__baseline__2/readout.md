Decision: Don't ship

# Ranker v7 – launch review readout

**Bottom line.** The pre-registered ship rule is not met. Successful Search Rate (SSR) is up +0.33 pp (0.4120 → 0.4153, +0.81% relative, 95% CI +0.16 to +0.50 pp, p = 7e-5). The effect is real, but the point estimate is below the pre-registered bar of +0.50 pp (`ship_requires: point_at_bar`). The CI upper bound only just touches the bar. Passing a significance test is not the criterion the team set.

## Primary (pre-registered)
| Metric | Control | Test | Δ abs | 95% CI | Bar | Met? |
|---|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | +0.0033 | [+0.0017, +0.0050] | +0.0050 | **No** |

## Guardrails (all within margin; none are the blocker)
| Metric | Δ (relative) | Margin | Note |
|---|---|---|---|
| Latency p95 | +0.2% (+0.8 ms ± 2.1) | 2% | fine |
| Abandonment Rate | +0.10% rel (+0.0002 abs ± 0.0011) | 1% | fine |
| Zero Result Rate | 0.0% | 3% | fine |
| Revenue per User | −0.1% (CI about −0.8% to +0.6%) | 1% | within margin, but the CI is not tight against it |

Secondary metrics (CTR, long clicks, reformulation, etc.) show nothing significant. I did not slice-hunt. Of about 40 segment metrics, a few have p < 0.05 (SSR head queries, CTR navigational, TTFC mobile). That is about what chance gives across ~40 uncorrected looks, so I don't treat them as findings.

## Caveats the review should know
1. **Config is not the pre-registered design as written.** `experiment.json` is "Q3 search launches holdout" (id `q3_search_launches_holdout`), a 5% holdout meant to measure the *combined* effect of the quarter's ranking launches. The prereg id is `ranker_v7`. Only `ranker_model` differs between arms (v6 vs v7), so the contrast is plausibly v7, but I can't rule out other launches bundled into the holdout (`holdoutIDs: q3_search_holdout`). Attribution to v7 alone should be confirmed by the owner. The audit log is empty, so there is no change history to check.
2. **Arm sizes look inconsistent.** The config has a 5/95 split with 20% allocation, but Pulse reports exactly 1,000,000 units in each arm. The health check says "balanced exposures: PASSED". Either the Pulse arms are not what the config describes, or the config was changed after launch. This needs a quick check before anyone relies on the numbers. Unit counts are also 20x the pre-registered 50,000 per arm.
3. **Early look.** Pulse is dated 2026-09-25, about 13 days into a planned 90. Sequential testing is off and there is no multiplicity correction, so the CI is a fixed-horizon interval read early. The estimate is tight and would have to move by about 50% to reach the bar. Novelty or learning effects could still shift it either way.
4. CUPED is off, so the intervals are unadjusted and conservative.

## Recommendation
Don't ship v7 on this evidence as the pre-registration defines success. If the team still wants v7, the route is a documented decision to lower the bar (not a post-hoc reinterpretation of this result) or a better-than-0.5 pp variant. Before the meeting, the owner should resolve items 1 and 2. If they show the data is not a clean v6-vs-v7 contrast, the decision becomes "Can't tell".
