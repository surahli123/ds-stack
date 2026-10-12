Decision: Don't ship

# Ranker v7 – launch readout

**Bottom line:** Ranker v7 does not meet the pre-registered ship criteria. The rule required both primary metrics to reach their +0.5 pt bar. Neither does, and for Long Click Rate the data rule the bar out. Recommend not shipping as-is.

## Setup (checked)
- Randomized A/B on userID, 50/50 (control lambdamart_v6, test lambdamart_v7), 14 planned days, Pulse ds 2026-09-25. About 1.0M units per arm (plan 900k). Exposure balance health check PASSED. The audit log is empty, so there were no mid-test changes.
- The only parameter that differs between arms is ranker_model (snippet_length is 160 in both), as intended.
- Pulse was pulled without CUPED at 95% CI, no sequential testing, no multiplicity correction. This is a single look at the planned end, so the plain 95% CIs are valid for the two primaries.
- Config lists only Successful Search Rate as primary. The pre-reg has two (rule "all"). I used the pre-reg.

## Primary metrics (pre-reg: ship needs point estimate ≥ bar on both)
| Metric | Control | Test | Abs. change (95% CI) | Bar | Result |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | +0.33 pt (+0.17, +0.50), p=7e-5 | +0.50 pt | Real lift, but point estimate below bar; CI upper end (~+0.498) is just under it |
| Long Click Rate | 0.2210 | 0.2213 | +0.03 pt (−0.11, +0.16), p=0.70 | +0.50 pt | No detectable effect; bar excluded by CI |

Successful Search Rate improved (+0.81% relative), but by about two-thirds of the size the team said was needed. Long Click Rate, the second primary, is flat. The bar is not met.

## Guardrails (pre-reg margins) – all OK
- Latency p95: +0.8 ms (+0.2%), margin 2%. OK.
- Abandonment: +0.02 pt (+0.1% relative), CI ±0.6%, margin 1%. OK.
- Zero Result Rate: unchanged (0.0), margin 3%. OK.
- Revenue per User: −0.1% (CI roughly −0.8% to +0.6%), margin 1%. OK, though the CI is not far from the margin.

## Secondary / exploratory (not decision-bearing)
About 60 secondary and segment metrics were read, with no correction. At 95%, about 3 false positives are expected by chance. Nominal hits:
- Queries per User +0.13 (p=0.02), CTR Tail Queries +0.33 pt (p=0.016), Long Click Rate Head Queries −0.20 pt (p=0.041).
- None is pre-registered. I would not act on them, but the Head-query Long Click dip (alongside a non-significant Head SSR −0.32 pt) is worth a follow-up look.
- CTR, Sessions, Clicks per User, Reformulation and Time to First Click show no clear movement.

## Recommendation
- Don't ship v7 as tested. It is safe on guardrails and gives a small genuine SSR gain, but misses the pre-registered bar on both primaries.
- If the review wants to ship below the bar, that is a decision to override the pre-reg. It should be made explicitly, with the +0.17 to +0.50 pt SSR range and the flat Long Click Rate on the table. That is an escalation, not something this data supports on its own.
- Next step if v7 is iterated: investigate Head-query behavior, and re-test with a power calculation for a +0.5 pt effect on Long Click Rate.
