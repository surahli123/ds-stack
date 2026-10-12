Decision: Escalate

# Ranker v7 readout

**Bottom line.** The primary metric moved up and met the pre-registered bar, and no guardrail was breached. But the Test arm changed two things, not one: `ranker_model` (lambdamart_v6 → v7, as pre-registered) and `snippet_length` (160 → 220). The pre-registration lists only `ranker_model` as an intended parameter, and the audit log is empty, so there is no record of who added the snippet change or why. This experiment cannot say how much of the lift is the ranker. Someone who owns the ship decision needs to choose between shipping the bundle and re-testing the ranker alone.

## Primary (pre-registered): Successful Search Rate
- Control 0.4120, Test 0.4153. Absolute +0.00334 (95% CI +0.0017 to +0.0050). Relative +0.81% (CI +0.41% to +1.21%). p = 7e-5.
- Bar is 0.005 with rule "point estimate at the bar". I read the bar as relative (+0.5%), because the guardrail margins (2%, 1%, 3%, 1%) are clearly relative. On that reading the point estimate (+0.81%) clears it. If the bar was meant as an absolute +0.005 (+1.2pp), it is **not** met (+0.0033). The team should confirm which was intended.
- The CI's lower end (+0.41%) is below the bar. The prereg only requires the point estimate to reach it, so this is not disqualifying. The true lift could still be smaller than the bar.

## Guardrails (95% CI worst end vs. pre-registered margin, relative)
| Metric | Change | Worst end of CI | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.2% | +0.7% | 2% | OK |
| Abandonment Rate | +0.1% (worse) | +0.7% | 1% | OK |
| Zero Result Rate | 0.0% | +1.4% | 3% | OK |
| Revenue per User | -0.1% | -0.8% | -1% | OK, but only just |

Revenue's lower bound is close to its margin. The abandonment bound is also within 0.3 points of its margin.

## Validity checks
- Design is a 2-arm A/B on userID with a 50/50 split inside a 20% allocation. The exposure-balance health check passed. There are 1.0M units per arm against 900k planned.
- The run covers the planned 14 days (started 2026-09-12, Pulse ds 2026-09-25). Sequential testing is off, so the fixed-horizon CI and p-value apply. Pulse was requested without CUPED at 95% confidence, which matches the prereg.
- **Confound:** `snippet_length` 160 → 220 changed alongside the ranker. Longer snippets plausibly affect click and success behavior on their own.
- Secondary metrics don't corroborate the lift. CTR, Long Click Rate, Clicks per User and Queries per User are all flat and not significant. Time to First Click is +0.9% (worse, p=0.08). It is unclear why "successful search" rose while clicks did not.

## Exploratory only (not pre-registered, no multiplicity correction)
There are dozens of segment cuts. Tail Queries success (+0.93%, p=0.015), Mobile CTR (p=0.013) and Head-query Long Click (p=0.04) look significant. Desktop success is negative (-0.66%, p=0.11). With this many cuts, a few p<0.05 results are expected by chance. None of this should drive the decision. The desktop vs. mobile gap is worth a follow-up.

## What I'd ask the review to decide
1. Who added `snippet_length=220`, and is it meant to ship? If the bundle is the intended launch, the evidence supports it: the primary meets the bar (relative reading) and the guardrails pass.
2. If the claim is "the new ranker works", re-run with `snippet_length` held at 160 in both arms. The current data cannot support that claim.
3. Confirm whether the 0.005 bar is relative or absolute.
