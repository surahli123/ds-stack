Decision: Don't ship

# Ranker v7 – launch review readout

## Bottom line
v7 improves Successful Search Rate (SSR), and the improvement is real. But it is smaller than the bar the team pre-registered. The pre-registered rule is `ship_requires: point_at_bar`, and the bar is +0.005 on SSR. The measured lift is +0.0033, so v7 does not meet the ship criterion.

## Primary metric (pre-registered, CUPED, 95% CI)
| | Control | Test | Abs. diff | 95% CI | Rel. | p |
|---|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4134 | **+0.00334** | [+0.00169, +0.00499] | +0.81% | 7e-5 |

- The effect is clearly positive. The CI excludes 0.
- The point estimate is 0.00334, below the 0.005 bar. The CI upper end (0.00499) is also below the bar, so even an optimistic read doesn't reach it.
- I read the bar as an absolute change (0.5 percentage points). **Assumption:** prereg.json doesn't state the unit. If the team meant a relative 0.5%, the +0.81% relative lift would clear it and this decision would flip. Please confirm with the prereg authors at the review. I think the absolute reading is the more natural one for a rate metric.

## Guardrails (all pass)
The worst end of each 95% CI stays inside its margin. I assumed the margins are relative.
| Guardrail | Change (worst CI end) | Margin |
|---|---|---|
| Latency p95 | +0.2% (+0.7%) | 2% |
| Abandonment Rate | +0.1% abs (+0.13% abs) | 1% |
| Zero Result Rate | 0.0% (+1.4% rel.) | 3% |
| Revenue per User | -0.1% (-0.8%) | -1% |

Revenue's worst end sits close to its margin, so I'd watch it after any launch.

## Things I checked
- **Design and health:** it is a 50/50 A/B test on userID with a balanced-exposures check passed. Pulse shows 1.0M units per arm against 0.9M planned. The data is at ds 2026-09-25, which is the 14-day planned duration. No peeking issue: sequential testing is off and this is the single planned readout.
- **Pulse internal consistency:** the primary's CI, p-value and relative change agree with the reported means and standard errors.
- **Audit log:** empty, so there were no mid-test config changes.
- **Secondary and segment metrics (exploratory, not pre-registered, no multiplicity correction):**
  - About 60 metrics and segments were reported. A handful of nominal p<0.05 results is expected by chance, so none should drive the decision.
  - SSR on head queries is -0.0038 (p=0.011), a possible regression. It is one of 6 SSR segments among ~60 exploratory tests and doesn't survive correction. Mobile (+0.0030) and desktop (-0.0025) also point in opposite directions. It is worth a follow-up but isn't evidence of harm.
  - Reformulation rate is up (p=0.039, a worse direction) and time to first click is down (p=0.031, a better direction). They roughly offset and neither survives correction.
  - CTR, long clicks, clicks and queries per user, sessions and ad clicks show no detectable change.

## Recommendation
Don't ship v7 as a launch on the current pre-registered criterion. A real but sub-bar +0.33pp SSR gain with clean guardrails is a reasonable candidate to iterate on, for example by examining head-query behavior. Overriding the bar is a product decision for the review, not something the data supports on its own. First, settle the unit of the bar.
