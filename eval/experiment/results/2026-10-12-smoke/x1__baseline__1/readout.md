Decision: Don't ship

# Ranker v7 – launch review readout

## Bottom line
Ranker v7 produces a real but small lift in Successful Search Rate (SSR). The lift is below the +0.5 pt bar the team pre-registered as the ship criterion, so by our own rule it does not ship. No guardrail is harmed, so this is a "didn't clear the bar", not a "does harm".

## Primary metric (pre-registered: SSR, ship only if point estimate ≥ +0.005 absolute)
| | Control | Test | Abs. change | 95% CI | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | **+0.0033** (+0.81% rel.) | [+0.0017, +0.0050] | 7e-5 |

- The effect is statistically distinguishable from zero.
- The point estimate (+0.0033) is about two-thirds of the bar. The CI upper end (+0.00498) is just under the bar, so the data do not support a lift of the size we required.
- Pre-reg rule is `point_at_bar`; this fails it.

## Guardrails (pre-registered margins; judged on the CI's worst end)
| Guardrail | Change (95% CI worst end) | Margin | Status |
|---|---|---|---|
| Latency p95 | +0.2% (worst ≈ +0.7%) | 2% | OK |
| Abandonment Rate | +0.1% rel. (worst ≈ +0.7%) | 1% | OK |
| Zero Result Rate | 0.0% (worst ≈ +1.4%) | 3% | OK |
| Revenue per User | −0.1% (worst ≈ −0.8%) | 1% | OK |

Abandonment and Zero Result margins are read as relative; they also pass if read as absolute.

## Secondary and segment metrics (exploratory only)
- About 70 secondary/segment metrics were reported with no multiplicity correction (Bonferroni off). A few nominally significant results (Pagination Rate worse, p=0.03; Navigational Long Click Rate better, p=0.049) are what chance would produce at this count. They are not evidence either way.
- SSR segments (mobile, desktop, head, tail, navigational, informational) all have CIs spanning zero. Tail queries lean positive (+0.0023) and mobile/head lean negative, but none is conclusive and none was pre-registered.

## Validity checks
- Exposure balance health check: passed. 1,000,000 users per arm (pre-reg planned 900k).
- Audit log is empty: no config changes during the run. Run is 14 days (2026-09-12 to 09-25), as planned.
- CUPED off, 95% CI, no sequential testing, so the fixed-horizon CI is valid at the planned end.
- **Design deviation to note:** the pre-reg says "interleaving", but the Statsig config is a standard user-level A/B (two 50/50 groups, 20% allocation). The Pulse numbers are valid for that A/B. If the bar was calibrated for an interleaving metric, it may not translate to this absolute-SSR scale. The team should confirm that the +0.005 bar is meant for this scale.

## Recommendation
- Don't ship v7 as is under the pre-registered criterion.
- If the team believes a +0.33 pt SSR gain is worth shipping with no guardrail cost, that is a decision to re-open the bar explicitly. It should not be made by quietly relaxing it after seeing the result.
- Possible follow-ups: investigate the tail-query gains, since a targeted rollout is a new hypothesis needing its own pre-registration. Also resolve the interleaving vs. A/B mismatch.
