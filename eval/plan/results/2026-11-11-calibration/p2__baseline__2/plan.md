# Plan: Does the AI answer panel help 3P users?

## Decision
Whether to turn the panel on by default for 3P users (people who search content from third-party connectors).

## Design facts that drive the analysis
- Randomization was at the user level, 50/50, inside every tenant (412 tenants, ~180k users, 2026-09-01 to 2026-09-28).
- Sessions are not independent: heavy users contribute many sessions, and users cluster in tenants.
- `tenants.segment` ('3P power', 61 tenants) is a sales label for the tenant, based on connectors installed. It is not the same as a user who searches 3P content.

## Unit and outcome
- Estimate the effect per user, the randomization unit. For each user, compute the success rate = successful sessions / sessions during the test, plus sessions per user as a guardrail. Panel could change how many searches people run, so a per-session comparison could be biased by selection.
- Primary estimand: difference in mean per-user success rate, treatment minus control. As a robustness check, also use successful sessions per user (does not condition on the session count).
- Do not pool sessions as if independent. Do not use session-level p-values.

## Defining 3P users
- Segment at the user level using pre-test behavior only: share of sessions with `used_3p_result` = true in the pre-period (2026-06-01 to 2026-08-31). Classify as 3P user if they have at least a minimum number of pre-period sessions (e.g. 5) and the 3P share is at or above a threshold (pick before looking at outcomes; check sensitivity at a couple of thresholds, and also show the share as a continuous dose-response).
- Do not define it using `used_3p_result` during the test. The panel may change what people click, so that is post-treatment and would break the randomized comparison.
- Do not use the tenant's '3P power' label as the user definition. Use it only as a secondary cut (tenant-level heterogeneity) and report how well it overlaps with the user-level definition.
- Users with too little pre-period history (new signups after 2026-06-01, per `users.signup_date`) go in an "unclassified" group. Report them separately and do not drop them silently.
- Pre-period classification is not affected by arm, so check balance: the share of 3P users should be about equal across arms (sample ratio and covariate balance checks).

## Tenants
- Tenants are the randomization block, not the unit. Because assignment was 50/50 within each tenant, compare within tenant: regression of user outcome on arm with tenant fixed effects (or a stratified estimator), with standard errors clustered by tenant.
- Tenant sizes run 5 to 9,000 seats, so a plain user-level pool is dominated by a few large tenants. Report two versions: user-weighted (each user counts equally; the pooled effect on users) and tenant-weighted (each tenant counts equally), and look at the spread of per-tenant effects (e.g. forest plot, large vs small) to see if a handful of tenants drive the result.
- Check that no tenant has a badly skewed arm split.

## Checks before reading results
1. Sample ratio: arm split overall, per tenant, and within the 3P segment.
2. Pre-period balance of success rate and activity across arms (also within 3P users).
3. Only count users active during the test; confirm the "active" definition does not depend on arm.
4. Data quality of `success` and `used_3p_result` (nulls, logging changes during the test), and a check of `arm` agreeing between `users` and `search_sessions`.

## Analysis steps
1. Overall effect (all users) as context.
2. Effect in 3P users (primary), with 95% CI, using the tenant-FE model above. Use CUPED / pre-period success rate as a covariate for precision.
3. Effect in non-3P users, and a formal interaction test (arm x 3P) so that "helps 3P more" is not a comparison of separate p-values.
4. Heterogeneity: by 3P share (dose-response), tenant size, tenant '3P power' label.
5. Guardrails: sessions per user, search abandonment/reformulations, clicks on 3P results, any latency or complaint metrics available. Check that the success metric (30s dwell or copy) is not inflated simply because the panel adds copyable text.
6. Novelty: weekly effect over the 4 weeks to see if it fades.

## Decision rule (set before querying)
Turn on by default for 3P users if the CI for the 3P-user effect excludes harm of more than a pre-agreed margin, the point estimate is positive, guardrails do not regress, and the result is not driven by a few tenants. Otherwise recommend a staged rollout or further testing.

## Open questions for the PM
- Minimum meaningful lift and acceptable harm margin.
- Whether the default decision is per user, or per tenant (this would change the weighting).

Unit: user (the randomization unit), with per-user success rate over the test period as the outcome
Segment: a user is a 3P user if their pre-test sessions (2026-06-01 to 2026-08-31) show a high share with used_3p_result (threshold set before looking at outcomes); not the sales tenant label, and not test-period 3P usage
Tenants: as randomization blocks (tenant fixed effects, standard errors clustered by tenant), reported both user-weighted and tenant-weighted, with per-tenant effects checked for domination by large tenants
