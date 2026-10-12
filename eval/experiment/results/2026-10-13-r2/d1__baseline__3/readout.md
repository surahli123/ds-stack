Decision: Don't ship

# Ranker v7 – launch review readout

**Bottom line:** Ranker v7 improves Successful Search Rate (SSR), but it breaks the pre-registered latency guardrail. Latency p95 is about 3% worse, and the 95% CI excludes the 2% tolerance. Per prereg, that blocks launch as configured. The way forward is a latency fix and re-test, or an explicit, documented waiver by the owners.

## Setup checks
- Two-arm A/B on userID, 50/50 split, 1.0M units per arm (planned 900k). The exposure-balance health check passed.
- The run covers 2026-09-12 to 09-26. Pulse is the ds=2026-09-25 snapshot, which matches the planned 14 days.
- No sequential testing or multiple-comparison correction is configured. The audit log is empty, so there were no mid-test config changes.
- Pulse is not CUPED-adjusted, at 95% confidence.
- The only intended parameter change is ranker_model. snippet_length is identical in both arms.

## Primary: Successful Search Rate (prereg: point estimate must reach +0.005)
| | Control | Test | Abs. change | Rel. change | 95% CI (abs.) | p |
|---|---|---|---|---|---|---|
| SSR | 0.4120 | 0.4153 | +0.00334 | +0.81% | [+0.0017, +0.0050] | 7e-5 |

- The lift is real: the CI excludes 0.
- Whether it reaches the bar depends on the bar's units, and prereg doesn't say. The guardrail margins are clearly relative, so the bar may be too.
  - Relative (0.5%): the point estimate (+0.81%) clears it, though the CI lower edge (+0.41%) does not.
  - Absolute (0.5 pt): the point estimate (+0.33 pt) misses, and even the CI upper edge (+0.50 pt) only just touches it.
- The decision doesn't depend on this ambiguity, because the guardrail fails either way. Please confirm the intended units.

## Guardrails (margin = tolerated relative degradation)
| Metric | Rel. change (95% CI) | Margin | Status |
|---|---|---|---|
| **Latency p95** | **+3.1% [+2.5%, +3.7%]** (412 → 424.8 ms) | 2% | **BREACHED** (whole CI beyond the margin) |
| Abandonment Rate | +0.1% [-0.5%, +0.7%] | 1% | OK (CI inside the margin) |
| Zero Result Rate | 0.0% [-1.4%, +1.4%] | 3% | OK (CI inside the margin) |
| Revenue per User | -0.1% [-0.8%, +0.6%] | -1% | OK (CI inside the margin) |

## Other metrics (exploratory, not decision-driving)
- Secondary metrics (CTR, Long Click Rate, Queries, Sessions, Clicks and others) show no significant movement.
- The segment cuts (device, head/tail, navigational/informational) are a large set of unadjusted tests, so a few nominal p<0.05 hits are expected by chance. Examples are Tail CTR (-1.1%), Mobile Abandonment (-1.8%) and Autocomplete Acceptance (+0.6%). I don't treat any of them as a finding.
- SSR by segment is directionally mixed. Desktop (-0.58%) and Mobile (-0.25%) are both negative and not significant, which is odd next to a positive overall result. Segment CIs are wide, so this is not evidence of harm, but it's worth a look.

## Recommendation
1. Don't ship v7 as configured. The latency guardrail is breached.
2. Investigate and reduce the roughly 13 ms p95 regression (for example model cost or the serving path), then re-test.
3. If the owners want to ship anyway, they need a documented waiver of the latency guardrail, weighing a +0.3 pt SSR gain against +3% p95 latency.
4. Clarify the unit of the SSR bar in prereg.

Not checked: whether the latency regression comes from the model itself or from infrastructure noise. Only aggregate Pulse data was available, with no time series.
