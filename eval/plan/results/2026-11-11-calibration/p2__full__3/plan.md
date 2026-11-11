# Plan: does the AI answer panel help 3P users?

Decision: PM decides whether to turn the panel on by default for 3P users. Options: on by default for 3P users, stay opt-in/off, or roll out wider/narrower. Ship if the 3P effect is positive and clear of a harm threshold. [guess] The threshold is a relative lift of about 1% or more in session success, and a drop of 1% or more blocks the rollout. Confirm this with the PM.

Unit: the user. Randomization was per user, 50/50, inside every tenant, so I estimate at the user level (or at the session level with standard errors clustered by user). Rolling up to tenants would leave 412 units instead of ~180k and add no power. The question is about users ("3P users"), so this matches.

## Segment definition
- The `tenants.segment = '3P power'` label is not the segment. It is set by sales from how many connectors a tenant has installed, and it is a property of the tenant. Many users in those 61 tenants never search 3P content, and many users in "standard" tenants do.
- A 3P user is defined by their own behavior before the test: share of the user's sessions with `used_3p_result = true` in the pre-period (2026-06-01 to 2026-08-31). Proposed cut: at least N sessions in the pre-period and a 3P share above a threshold (e.g. 20%). Pick the threshold from the distribution before looking at any treatment effect. Report 2-3 cutoffs as sensitivity checks.
- Do not use `used_3p_result` from the test period to define the segment. The panel can change what people click, so it is post-treatment and conditioning on it breaks the randomization.
- Users with no pre-period sessions (new signups, see `users.signup_date`) cannot be classified. Report them as a separate "unclassified" group and say how many there are.
- As a side check, say how many 3P-behavior users sit in "standard" tenants and how many users in "3P power" tenants are not 3P users. This shows how far apart sales' label and the behavioral definition are, since the PM and sales both say "3P power".

## Tenants
Tenants are a stratification factor, not the unit. Tenants were not treated whole, so there is no tenant clustering. Estimate within tenant (tenant fixed effects, or a stratified difference in means) and average across tenants weighted by users. Tenants range from 5 to 9,000 seats, so large tenants would dominate a pooled average. Report the user-weighted result and check it against an equal-weight-per-tenant result. Use the `segment` label only as a secondary cut.

## Checks before the effect
1. Randomization: arm balance (50/50) overall, by tenant, and within the 3P segment. Check sample ratio mismatch. Compare the pre-period 3P share and session volume across arms. Check that `users.arm` matches `search_sessions.arm`.
2. Data: query the one input everything rests on first, which is `used_3p_result` and `success` for 2026-06-01 through 2026-09-28. Confirm both are populated for the pre-period and that the logging did not change on 2026-09-01.
3. Metric validity: "success" includes "answer copied". Copying an answer can only happen with the panel, so the treatment arm has an extra way to succeed. Check whether copy events exist in control. Report the click-and-dwell-30s component alone as well as the combined metric. The panel may cut clicks because the answer is enough, which would lower the dwell part even when users are better served. If the click-dwell part falls and copies rise, the combined metric alone cannot show whether users are better off. Add a guardrail such as reformulated queries or sessions per task, if it is logged.

## First test
Among classified 3P users, compute per-user success rate (successful sessions / sessions during 2026-09-01 to 2026-09-28), treatment minus control, stratified by tenant, with a CI. Do it on the whole segment, and again with pre-period success rate as a covariate (CUPED) to tighten the interval. It fails (the panel does not help) if the CI includes the harm threshold, or the lift is within noise of zero. It also fails if the click-dwell component falls and copies are the only thing driving the gain. Present the non-3P-user effect next to it, with an interaction test, so the PM sees whether 3P users really differ.

## Other points
- Novelty: check the effect by week of the test (4 weeks).
- Pooling: heavy and light searchers, and tenant size bands, may differ. Report them separately and not only pooled.
- Power: count 3P users per arm once defined, then check the minimum detectable effect against the smallest change that matters.
- Reproducibility: panel answers depend on user permissions and index state, so session-level results are not replayable. Only the logs are.

## Questions for the PM
1. What lift or harm in success would change the decision?
2. Is "3P user" meant as a user who searches 3P content, or a customer with many connectors? The plan assumes the former.
3. Is the copied-answer event logged in control, or only for the panel?

## Open
- Segment threshold (share and minimum sessions) is not set. If it stays open, report the effect at several cutoffs and decide only if they agree.
- Whether control can produce "copied" events is unknown. If it stays open, base the decision on the click-dwell component alone.
- The harm threshold is a [guess].

## Premises
- Users randomized 50/50 within every tenant: given (notes).
- 412 tenants, ~180k active users, 61 tenants labeled '3P power': given.
- Logs reach back to 2026-06-01, so a pre-period exists: given, not yet queried.
- `used_3p_result` is reliably logged in the pre-period: [guess].
- "Answer copied" is only possible with the panel: [guess].

Unit: user (randomized unit), estimated within tenant strata with a user-weighted average
Segment: a 3P user is a user whose own sessions in 2026-06-01 to 2026-08-31 (before the test) have a high share with used_3p_result, not a user in a '3P power' tenant; threshold set from the pre-period distribution before looking at effects
Tenants: as strata (tenant fixed effects or stratified difference in means, user-weighted, checked against equal-weight), not as the unit and not clustered, since users were randomized within tenants
