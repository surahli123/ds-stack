Decision: Don't ship

# Ranker v7 – launch readout

**Bottom line:** v7 improves Successful Search Rate (SSR) on triggered searches, but converted to the overall population the pre-registered bar is 0.005. The lift comes to roughly 0.0008 absolute, or 0.39% relative, depending on how the bar is read. Either way it misses the bar. The pre-reg says ship requires the *point estimate* to be at the bar, so this is a Don't ship under the agreed rule.

## Primary metric (pre-registered: SSR, bar 0.005, overall)
- Pulse scorecard, triggered searches: control 0.4120, test 0.4198. Δ = +0.00783 (95% CI ±0.00247), +1.9% relative, p<0.001. The effect is real.
- The scorecard is **not** on the bar's population. The prereg notes triggered searches are 10% of searches and 20.5% of control successes, and the bar is overall.
- Translating to overall:
  - Absolute: 0.00783 × 10% of searches = **≈ +0.00078** (CI ≈ +0.00053 to +0.00103). This is about 16% of a 0.005 absolute bar, and the CI excludes the bar.
  - Relative: 1.9% × 20.5% of successes = **≈ +0.39%** (CI ≈ +0.27% to +0.51%). If the bar is read as 0.5% relative, the point estimate is still short. The CI upper end only just reaches 0.5%.
- Reading the triggered +0.0078 (or +1.9%) directly against the bar would wrongly look like a pass. That is the trap here.
- The prereg doesn't say whether 0.005 is absolute or relative. I'd confirm that with the team, but the decision is the same under both readings.
- The overall figures are my derivation from the prereg's mass shares, not Pulse output. Pulse has no overall-population SSR. If someone wants a firm number, have it computed on all searches.

## Guardrails (all within margin, none is a blocker)
| Metric | Δ (rel.) | CI half-width | Margin |
|---|---|---|---|
| Latency p95 | +0.2% (412.0→412.8 ms) | ±0.5% | 2% |
| Abandonment | +0.1% | ±0.6% | 1% |
| Zero Result | 0.0% | ±1.4% | 3% |
| Revenue/User | −0.1% | ±0.7% | 1% |

## Validity
- The design is a clean A/B test. Only `ranker_model` differs between arms (`snippet_length` is the same at 160), which matches the intended params.
- The audit log is empty, so there were no mid-test changes.
- The exposure balance check passed. Both arms have 1.0M units, above the 900k planned. The run covered the planned 14 days (data as of 2026-09-25).
- CUPED is off, there is no sequential testing, and no multiplicity correction is configured. A single primary makes that fine for the decision.

## Secondary metrics (exploratory, not decision-driving)
- There are about 60 secondary and segment metrics, and no correction was applied. At 95% about 3 would be expected to be "significant" by chance.
- Three have p<0.05:
  - Queries per User: −1.0% (p=0.024)
  - Desktop time to first click: +0.13 s (p=0.043)
  - Informational reformulation rate: +1.8% (p=0.050)
- All three go in the unfavorable direction, so they merit a follow-up look, but none is a pre-registered metric. I wouldn't treat them as established harms.
- CTR, long clicks, clicks per user and the head/tail and mobile/desktop SSR splits show no detectable movement.

## Recommendation
- Don't ship v7 as-is against this bar.
- If the team thinks a ~0.4% relative (≈0.0008 absolute) overall gain is still worth shipping, that is a different decision. It means revising the bar, and it should be made explicitly, not by reading the triggered number against the bar after the fact.
- Possible follow-ups:
  - Increase the triggered population.
  - Look into the queries-per-user drop.
