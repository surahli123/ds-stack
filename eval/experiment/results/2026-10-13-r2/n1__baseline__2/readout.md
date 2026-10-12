Decision: No effect found

# Ranker v7 – launch readout

**Bottom line:** Ranker v7 did not move the pre-registered primary metric, and the data rule out an effect as large as the bar we set for shipping. Recommend not launching on the basis of this test.

## Primary metric (pre-registered: Successful Search Rate, ship bar +0.5 pp)
| | Control | Test | Δ (abs) | 95% CI | p |
|---|---|---|---|---|---|
| Successful Search Rate | 41.20% | 41.22% | +0.016 pp | −0.107 pp to +0.140 pp | 0.79 |

- The point estimate (+0.016 pp) is far below the +0.5 pp bar, and the CI upper end (+0.14 pp) is also well below it. Under the prereg's rule (ship requires the point estimate at the bar), this fails clearly. It is a precise null, not an underpowered one.
- Any true gain is at most about 0.14 pp (~0.3% relative), about a quarter of what the team said was worth shipping.

## Guardrails (prereg margins; all pass)
| Metric | Relative change | 95% CI half-width | Margin |
|---|---|---|---|
| Latency p95 | +0.2% (412.0 → 412.8 ms) | ±0.5% | 2% |
| Abandonment Rate | +0.1% | ±0.6% | 1% |
| Zero Result Rate | 0.0% | ±1.4% | 3% |
| Revenue per User | +3.1% | ±2.1% | (increase wanted) |

No guardrail regression. Revenue per User is up, see caveat below.

## Experiment health
- 1.0M units per arm (plan 900k), exposures balanced (health check passed), 50/50 split, 14-day duration matches plan. Pulse snapshot is 2026-09-25 (the last day of the planned window).
- Audit log is empty: no config changes during the run. Only `ranker_model` differs between arms (`snippet_length` is identical), so the comparison is clean.
- No CUPED, no sequential testing, no multiplicity correction were applied; one primary metric, so nothing to adjust there.

## Secondary metrics and the Revenue result
- 57 metrics reported (primary + secondary + segment cuts). 4 have p<0.05: Revenue per User (p=0.004), Time to First Click – Desktop (slower, +0.28 s, p=0.004), Clicks per User – Mobile (p=0.04) and Clicks per User – Tail Queries (p=0.013). With 57 uncorrected tests, ~3 false positives are expected by chance, so the last three are consistent with noise.
- **Revenue per User +3.1% (p=0.004)** is the one worth a look. It is not a pre-registered primary, and nothing supporting it moves: Ad Click Rate is flat (−0.03%, p=0.96), clicks and CTR are flat or slightly down. It does not survive a Bonferroni correction across 57 metrics (0.0038×57≈0.22). Treat it as a hypothesis, not a win. It does not justify shipping a ranker whose stated purpose (successful searches) shows no gain.
- All segment cuts of Successful Search Rate (mobile/desktop/head/tail/navigational/informational) are null.

## Recommendation / next steps
1. Do not ship Ranker v7 for the search-quality hypothesis. Keep control.
2. The experiment is still `active` in Statsig past its planned end; stop it so it doesn't keep consuming 20% of layer traffic.
3. If the team wants to pursue the revenue signal, it needs its own pre-registered test with a mechanism (why would ads revenue rise with no change in ad clicks?).
