# Plan: Does the AI answer panel help 3P users?

## Decision
Should the panel be on by default for 3P users (people who search third-party connector content)? We need the effect of the panel on the success metric within that group, with uncertainty, and whether it differs from other users.

## Design facts that drive the analysis
- Randomization was by user, 50/50, within every tenant (412 tenants, ~180k users, 2026-09-01 to 09-28). So tenant is a block, not a treated unit.
- Success = session with a click dwelling >= 30s, or an answer copied. Note: the panel could change this metric mechanically (answer copy is only possible with the panel; the panel may reduce clicks). Flag this as a metric-validity risk and look at the components separately.
- Logs go back to 2026-06-01, giving a pre-period (06-01 to 08-31) that is untouched by treatment.

## Unit of analysis
- Randomization unit is the user, so estimate the effect per user: collapse each user's test-period sessions to one row (e.g. success rate = successful sessions / sessions, and sessions per user), then compare arms.
- Do not treat sessions as independent. Heavy searchers would dominate and SEs would be too small. If session-level modelling is used, cluster SEs by user.
- Primary: per-user mean success rate (and a secondary per-user successful sessions count, which also captures whether the panel changes search volume). Check the ratio-vs-user-mean choice for sensitivity.

## Defining the 3P segment
- `tenants.segment = '3P power'` is a sales label about the tenant's installed connectors. It says nothing about whether an individual user searches 3P content (a 3P-power tenant has many users who never touch connectors, and standard tenants have some who do). Not used as the definition.
- `search_sessions.used_3p_result` in the test period is post-treatment: the panel can change what people click and see, so segmenting on it would compare unlike people across arms and bias the effect. Not used for assignment to the segment.
- Definition: a user-level, pre-treatment flag from the pre-period logs (06-01 to 08-31), e.g. the share of a user's sessions with used_3p_result = true, with a threshold (e.g. >= some share or >= N sessions with a 3P result). Choose the threshold and minimum activity before looking at outcomes; report a continuous dose-response by pre-period 3P share as a check.
- Users with no pre-period history (signed up after 06-01 or low activity; use users.signup_date) cannot be classified. Report how many, keep them as a separate "unclassified" group, and do not drop silently.
- Validate: balance of the flag across arms (should be equal in expectation because it is pre-treatment); size of the segment; overlap with tenant segment as a descriptive crosstab.
- Sensitivity: alternative thresholds; tenant-level '3P power' as the segment (this answers the sales-framing question, shown separately).

## Tenants
- Tenants enter as blocks, because randomization was within tenant: estimate with tenant fixed effects (or stratified estimate by tenant, combined with weights). Within-tenant comparison removes tenant size and connector mix as confounders.
- Tenant sizes run from 5 to 9,000 seats, so a handful of big tenants could dominate a user-weighted pooled estimate. Primary is user-weighted (the decision is a default applied to users). Also report tenant-weighted / tenant-level effects and a leave-large-tenants-out check, and look at effect heterogeneity across tenants (a forest plot or random-effects spread).
- Cluster SEs at user level (the randomization unit); report tenant-clustered SEs as a robustness check since users in a tenant may be correlated.
- Tiny tenants contribute little within-tenant contrast; keep them in the fixed-effects model but do not interpret them individually.

## Checks before the effect estimate
1. Sample ratio mismatch: arm split 50/50 overall and within tenants and within the 3P segment.
2. Pre-period balance: pre-period success rate and activity by arm, overall and for 3P users.
3. Exposure: confirm treated users actually saw the panel; confirm no control user did (compliance). Analyze as assigned (intent-to-treat).
4. Novelty: effect by test week.
5. Data quality: duplicate sessions, bots/test accounts, users who changed tenant.

## Estimation
- Primary: for 3P users, regression of per-user success rate on arm with tenant fixed effects; pre-period success rate as a covariate for variance reduction (CUPED). Report difference, 95% CI, relative lift.
- Compare with non-3P users via an arm x segment interaction, so "helps 3P users" is judged against what we see elsewhere and not by significance in one subgroup alone.
- Secondary: metric components (dwell-click vs copy), sessions per user, and a guardrail such as searches reformulated per session or abandonment if available.
- Account for the few segment cuts tried (one pre-registered segment definition; others labelled exploratory).

## Recommendation rule (set in advance)
Turn on by default for 3P users if the CI for the 3P user effect excludes harm beyond an agreed margin and the point estimate is meaningfully positive, with no guardrail regressions and no sign that the result is driven by a few tenants. Otherwise recommend keeping opt-in or a staged rollout.

Unit: User (the randomization unit): one row per user with their test-period success rate, SEs clustered by user; sessions are not treated as independent.
Segment: A user is 3P if their pre-test behaviour (sessions 2026-06-01 to 2026-08-31, using used_3p_result) shows sustained 3P searching above a threshold fixed before looking at outcomes; users with no pre-period history are reported as unclassified; neither the sales tenant label nor test-period used_3p_result is used.
Tenants: As randomization blocks: tenant fixed effects within the user-level estimate (user-weighted primary), with tenant-weighted, leave-large-tenants-out and heterogeneity-across-tenants checks, and the sales '3P power' label only as a sensitivity segment.
