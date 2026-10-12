Decision: Ship

# Ranker v7 – launch readout

**Design:** 50/50 A/B on userID, 20% layer allocation, 2026-09-12 start, 14 days, Pulse ds 2026-09-25 (no CUPED, 95% CI, no sequential testing, no multiplicity correction). Exposure health check passed; 1.0M units per arm (plan: 900k). Audit log is empty, so the config did not change mid-run. The only parameter that differs between arms is `ranker_model` (v6 → v7), as intended.

## Primary (pre-registered): Successful Search Rate
| | Control | Test | Abs. change | Rel. change | 95% CI (rel.) | p |
|---|---|---|---|---|---|---|
| SSR | 0.4120 | 0.4153 | +0.00334 | +0.81% | +0.41% to +1.21% | 7e-5 |

The lift is real, and the point estimate (+0.81%) clears the pre-registered bar of 0.005 (ship rule: point estimate at the bar, not the CI lower bound). Even the CI's lower end (+0.41%) is a positive lift.

## Guardrails (worst end of the 95% CI vs. pre-registered margin, relative)
| Metric | Observed | Worst CI bound | Margin | Pass |
|---|---|---|---|---|
| Latency p95 | +0.2% | +0.7% | 2% | yes |
| Abandonment rate | +0.1% | +0.7% | 1% | yes |
| Zero result rate | 0.0% | +1.4% | 3% | yes |
| Revenue / user | −0.1% | −0.8% | 1% | yes |

## Caveats
1. **The bar's unit is not stated in prereg.json.** I read 0.005 as a relative lift (0.5%) because the guardrail margins in the same file only make sense as relative fractions (e.g. 0.02 on a 412 ms latency). On that reading it is met. If the team meant 0.5 percentage points absolute, the result is +0.33 pp, with a CI upper end of +0.50 pp, and the bar is **not** met. The review should confirm the intended unit; the decision depends on it.
2. **Ad Click Rate fell 2.8% (p=0.022).** It is not a pre-registered guardrail. It is one of 56 secondary metrics tested without correction, so about 3 nominal hits at 5% are expected by chance (7 are below 0.05, in both directions). Revenue per user is flat, so there is no sign of monetization harm, but I'd keep Ad Click Rate on watch after launch.
3. Secondary metrics (CTR, long clicks, reformulation, queries per user) show no significant movement. Segment cuts (device, query type) are all directionally consistent or null, and I'd treat them as exploratory.
4. Effect size at the bar is thin: the CI includes lifts below 0.5%. The launch gives a small gain with no detected harm.

**Recommendation:** Ship, conditional on the review confirming the bar is relative (caveat 1). If it was absolute, the answer becomes Don't ship (or iterate).
