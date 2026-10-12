Decision: Can't tell

# Ranker v7 – launch readout

## Bottom line
The Pulse numbers do not answer the question the pre-registration asked, so I can't recommend shipping or killing v7 from them. Read at face value they also miss the pre-registered bar. The right next step is an interleaving analysis from the raw logs, not another Pulse run.

## Why Pulse can't be read as "v7 vs v6"
- Prereg design is **team-draft interleaving**, where each user sees v6 and v7 results merged in one list. The estimand is a within-user preference (win rate) for v7 over v6.
- The experiment as configured is a **between-user split**. Control gets `ranker_model=lambdamart_v6` with no `serving_mode`. Test gets `lambdamart_v7` with `serving_mode=team_draft_interleaving`. So Pulse compares pure v6 against an interleaved mix, not v7 against v6.
- If the test arm is roughly half v6 and half v7, the measured lift is a diluted version of the v7 effect. By how much depends on how interleaving credit and click attribution work, and Pulse can't tell us. Pulse also has no interleaving preference metric.
- `serving_mode` was an intended parameter in the prereg but is set on only one arm, and the control arm doesn't get the same serving path. Any serving-path difference is confounded with the ranker.
- The audit log is empty, so there is no change history to explain this. I can't tell whether the config was always this way.

## What Pulse shows (day 14, ds 2026-09-25, no CUPED, 95% CI)
Primary, Successful Search Rate: control 0.4120, test 0.4153. Change **+0.0033 abs (+0.81%), CI ±0.0016** (about +0.0017 to +0.0050), p = 7e-5.
- The effect is real, and the arms differ.
- The prereg ship rule is a point estimate at or above +0.005. +0.0033 **does not meet it**, and the CI upper bound only just reaches it.
- Because of the dilution above, I would not treat +0.0033 as v7's true lift or use it as the final comparison to the bar.

Guardrails (margins read as relative, from prereg). None is breached, though the intervals are loose and none is proven safe in any strong sense:
| Metric | Change | 95% CI half-width | Margin |
|---|---|---|---|
| Latency p95 | +0.2% | 0.5% | 2% |
| Abandonment Rate | +0.1% | 0.6% | 1% |
| Zero Result Rate | 0.0% | 1.4% | 3% |
| Revenue per User | -0.1% | 0.7% | 1% |

Secondary metrics are mostly flat. The one nominal hit is Pagination Rate, +1.4% (p = 0.03), in the unfavourable direction. With roughly 70 secondary and segment metrics and no multiplicity correction, one p < 0.05 is expected by chance, so I treat it as noise to watch, not a finding. Segment cuts (mobile/desktop, head/tail, and so on) show no reliable differences.

## Other notes
- Exposure is balanced (health check passed), with 1.0M units per arm against 0.9M planned. Duration is 14 days as planned.
- The primary metric is a ratio, and I used the Pulse CIs as given.

## Recommended next steps
1. Compute the interleaving preference metric (v7 wins / (v7 + v6 wins), per user or per query, bootstrapped by user) from raw logs, and check it against the prereg bar.
2. Ask the owner why control has no `serving_mode` and whether the test arm's blend is 50/50. Then decide whether to re-run with the proper interleaving setup (or a clean v6 vs v7 A/B).
3. Until then, no ship decision. Nothing seen points to harm, and the guardrails look fine.
