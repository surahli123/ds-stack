Decision: Don't ship

# Ranker v7 readout (Pulse ds 2026-09-25, 95% CI, no CUPED)

## Bottom line
Ranker v7 improves Successful Search Rate (SSR) but does not meet the pre-registered ship criteria. The pre-registration requires **both** primaries to have a point estimate at or above their bar (rule "all", ship_requires "point_at_bar"). Long Click Rate misses by a wide margin, so under the criteria we committed to, this does not ship. This is a real but small win, not a failed experiment.

## Primaries (bar = +0.005 each)
| Metric | Control | Test | Abs. change (95% CI) | Rel. | p | Bar met? |
|---|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | +0.0033 (±0.0016) → [+0.0017, +0.0050] | +0.81% | 7e-05 | **No** (point 0.0033 < 0.005) |
| Long Click Rate | 0.2210 | 0.2213 | +0.0003 (±0.0013) → [-0.0011, +0.0016] | +0.12% | 0.70 | **No** (indistinguishable from zero) |

- SSR is clearly positive, so the effect is real. It is about two-thirds of the size we said we needed.
- Long Click Rate shows nothing. Read as an absolute change, its CI upper end (+0.0016) is well below the 0.005 bar.
- **Bar units are not stated in prereg.json.** If 0.005 means an absolute change, both primaries miss, and SSR's CI upper end (+0.00498) is just under the bar. If it means a 0.5% relative change, SSR passes (+0.81%), but Long Click (+0.12%, CI up to about +0.7%) still misses on its point estimate. The decision is the same under either reading. The review should confirm the unit so the record is clean.

## Guardrails (all within margin, none regressed)
| Metric | Change | CI half-width | Margin |
|---|---|---|---|
| Latency p95 | +0.8 ms (+0.2%) | ±0.5% | 2% |
| Abandonment Rate | +0.0002 (+0.1% rel.) | ±0.6% rel. | 1% |
| Zero Result Rate | 0.0 | ±1.4% rel. | 3% |
| Revenue per User | -$0.0009 (-0.1%) | ±0.7% | 1% |

Guardrails are not what blocks this decision. Revenue and abandonment margins are fairly tight against the CI widths, but both are inside them.

## Experiment health and validity
- Balanced 50/50 allocation, 1,000,000 units per arm (planned 900,000). The exposure health check passed.
- Ran 2026-09-12 for the planned 14 days. The config shows fixed-horizon analysis (no sequential testing), so a single look at the end is valid.
- The audit log is empty, so there were no mid-flight config changes.
- Minor mismatch: experiment.json lists only SSR as a primary metric, while the prereg has two. Long Click Rate was still evaluated as pre-registered.
- Config status is still "active". It has been running past the planned window, so stop it or ramp it down deliberately.

## Secondary and segment metrics (exploratory only)
Roughly 90 metrics and segment cuts were reported with no multiplicity correction, so a few p < 0.05 results are expected by chance. I would not act on any of them:
- Queries per User +1.07% (p=0.02)
- CTR on tail queries +1.5% (p=0.016)
- Long Click Rate on head queries -0.20pp (p=0.04)

SSR on head queries is -0.32pp (p=0.14) while navigational and informational are positive. That is not significant, but it is worth a look in a follow-up.

## Recommendation
1. Do not ship v7 as currently specified. It fails the pre-registered Long Click criterion.
2. If the team thinks SSR alone is the right success metric, that is a change to the pre-registered criteria. The review should decide it explicitly, not by reading the result after the fact. The guardrails are clean, so the product risk is low.
3. If the team wants to pursue v7, the options are a v7.1 aimed at long-click quality, or a longer or larger test. A test designed around the observed SSR effect (+0.0033) would need a bar that matches it.
4. Confirm the unit of the 0.005 bar and fix the primary-metric list in the experiment config.
