Decision: Ship

# Ranker v7 – launch readout

**Bottom line.** The new ranker (lambdamart_v7 vs v6) raises Successful Search Rate (SSR) by +0.334 pp (0.4120 → 0.4134), +0.81% relative, 95% CI +0.17 to +0.50 pp (+0.41% to +1.21% relative), p = 7e-5. This meets the pre-registered bar at the point estimate, and no pre-registered guardrail is breached. One caveat on how the bar is read (below) could flip the call.

## Setup checks
- Design matches prereg: A/B, userID, 50/50 within a 20% allocation, 14 days (2026-09-12 to 09-25), 1.0M users/arm (plan 900k). Exposure-balance health check passed.
- Audit log is empty: no mid-test config changes. Only `ranker_model` differs between arms (`snippet_length` is 160 in both), as intended.
- Pulse used CUPED at 95%. No sequential testing, so a single end-of-test read is valid. One primary metric, so no multiplicity issue on the decision.

## Pre-registered decision rule (ship needs primary point estimate ≥ bar; guardrails within margin)
| Metric | Result (rel. change, 95% CI) | Prereg threshold | Pass |
|---|---|---|---|
| SSR (primary) | +0.81% (+0.41, +1.21) | ≥ +0.5% | yes (point) |
| Latency p95 | +0.2% (worst +0.7%) | ≤ 2% worse | yes |
| Abandonment | +0.1% (worst +0.7%) | ≤ 1% worse | yes |
| Zero Result Rate | 0.0% (worst +1.4%) | ≤ 3% worse | yes |
| Revenue/User | −0.1% (worst −0.8%) | ≤ 1% worse | yes |

Each guardrail's CI bound on the harmful side stays inside its margin, so this is non-inferiority, not just "not significant".

## Caveat: units of the bar
prereg says `bar: 0.005` without units. I read it as relative (0.5%), the same unit as the guardrail margins (a 0.02 latency margin can only be relative). On that reading the bar is met at the point estimate (0.81%), though the CI lower bound (0.41%) is below it. If the team meant 0.5 percentage points absolute, the result (+0.33 pp) misses the bar and the call becomes **Don't ship**. **The review should confirm the intended unit before approving.**

## Exploratory findings (not in prereg, ~60 uncut segment/secondary tests, no multiplicity correction; expect ~3 false positives at 5%)
- SSR on Head Queries: −0.38 pp (−0.95%), p = 0.011. Tail also −0.19 pp (n.s.). Mobile +0.30 pp (p = 0.08), Desktop −0.25 pp (n.s.). Head and tail both being negative while the total is +0.33 pp implies the unreported middle (torso) slice is strongly positive. I can't verify that from Pulse, so check the segment definitions.
- Reformulation Rate worse overall (+0.12 pp, p = 0.039) and for Navigational (+0.31 pp, p = 0.010); Time to First Click better (−0.07 s, p = 0.031). CTR, Long Click Rate, Clicks/User, and Ad Click Rate show no significant change, and their point estimates are slightly negative.
- None of these is a guardrail. They are worth a follow-up analysis of head/navigational queries after launch, not a reason to block. Watch head-query SSR and reformulation in post-launch monitoring.

## Recommendation
Ship, conditional on the review confirming that the 0.005 bar is relative. Keep a holdback or monitor head/navigational query SSR and Reformulation Rate after launch.
