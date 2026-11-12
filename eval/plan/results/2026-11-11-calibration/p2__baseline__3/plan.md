# Plan: Does the AI answer panel help 3P users?

Decision: turn the panel on by default for 3P users, yes or no.

## Design facts that drive the analysis
- Randomization was by user, 50/50, within every tenant (412 tenants, ~180k users, 2026-09-01 to 09-28). Tenant is a block, not an arm.
- Success is per session (click with 30s+ dwell, or answer copied).
- Logs start 2026-06-01, so there are about 3 months of pre-test behavior per user.

## Unit of estimation
- Estimate the effect at the user level, the unit of randomization. Sessions are repeated measures within a user, and heavy searchers would dominate a session-level comparison and understate the uncertainty.
- Outcome per user: share of their test-window sessions that succeeded. Secondary: successful sessions per user and sessions per user, to check whether the panel changes search volume (a session-level rate alone can hide that).
- Sanity checks first: arm split is about 50/50 overall and within tenant (sample ratio mismatch), arms balanced on pre-period activity, and users.arm matches search_sessions.arm.

## Defining a 3P user
- Do not use tenants.segment ('3P power'). It is a sales label of the tenant's installed connectors, so it says nothing about whether an individual uses 3P content. Most users in a '3P power' tenant may never search 3P content, and many users in 'standard' tenants may. It is a different question from the one the PM asked.
- Do not use used_3p_result during the test window to classify users. It is measured after assignment and the panel may change what people click, so classifying on it conditions on an outcome of treatment and biases the comparison.
- Classify each user from the pre-period only (2026-06-01 to 2026-08-31): the share of their sessions with used_3p_result = true, with a minimum session count for stability. 3P user = share at or above a threshold (pick before looking at results; examine the distribution, with a sensitivity check at other cutoffs, and also show the effect across the continuous share in bins).
- Users with no or too little pre-period history (e.g. signed up after 08-31, per users.signup_date) are left unclassified and reported separately, not forced into either group.
- Compare to the rest ("non-3P") in the same model to see whether the effect differs; report the 3P effect itself with its interval.

## Estimation
- Difference in mean user-level outcome between treatment and control within the 3P segment, with tenant fixed effects (the randomization was blocked on tenant) and optionally pre-period success rate as a covariate to reduce variance.
- Standard errors clustered by tenant (users within a tenant share content and admins' configuration).
- Interaction model (arm x 3P user) to test whether the effect is different for 3P users versus others.

## Tenants
- Tenants range from 5 to 9,000 seats, so a pooled user-level estimate is dominated by a few huge tenants. Handle this explicitly:
  - Main estimate: within-tenant comparisons (tenant fixed effects), pooled over users, clustered by tenant. This answers "per user, what does the panel do".
  - Robustness: tenant-weighted estimate (each tenant's effect counts equally, with tenants having too few 3P users per arm dropped or shrunk), and a version excluding the largest tenants.
  - Check effect heterogeneity by tenant size and by the sales segment ('3P power' vs 'standard') as a secondary cut, not as the definition of the segment.
- Report how many tenants contribute 3P users and how concentrated they are.

## Guardrails and reporting
- Guardrails: search volume, reformulation rate, zero-success sessions, latency if available.
- Novelty: effect by week of the test; the 4-week window may overstate or understate the steady state.
- Report effect size with a confidence interval in absolute and relative terms, for 3P users, non-3P users, and overall.
- Recommendation rule set in advance: ship by default for 3P users if the lower bound of the interval is above zero (or above a minimum meaningful lift the PM sets) and guardrails are not harmed.

Unit: User (the randomization unit); outcome is each user's share of test-window sessions that succeeded, with SEs clustered by tenant.
Segment: A 3P user is a user whose share of sessions with a 3P result (used_3p_result) in the pre-test period (2026-06-01 to 08-31) meets a threshold fixed in advance, with a minimum session count; users without enough history are left unclassified. Not tenants.segment and not in-test behavior.
Tenants: Tenants enter as blocks, with tenant fixed effects and tenant-clustered standard errors on the pooled user-level estimate; tenant-weighted and exclude-largest-tenants versions are robustness checks, and tenant size and the sales segment are heterogeneity cuts.
