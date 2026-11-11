# Plan: does the AI answer panel help 3P users?

Decision: PM decides whether to turn the panel on by default for 3P users. Options: on by default for 3P users, stay opt-in/off, or roll out by sub-segment. The smallest change that matters is a [guess] of about 1 point of session success rate. The PM should confirm that figure.

Unit: the user. Users were randomized 50/50 inside every tenant, so the effect is estimated per user (about 180k users). Per-user success rate is the mean over the user's sessions; also report the session-weighted version. Rolling up to 412 tenants would leave fewer units and no extra power.

## Segment: who is a 3P user
- Do not use `tenants.segment` ('3P power'). Sales set it from installed connectors, which is a tenant trait. Most users in those 61 tenants may never search 3P content, and users in 'standard' tenants may. It is also the label sales uses, which may differ from the PM's meaning.
- Use each user's own behavior before the test. A user is 3P if they had at least one session with `used_3p_result` = true in the pre-period 2026-06-01 to 2026-08-31 (logs reach back to June 1). Run the cutoff (at least 1 session, or a share of sessions) as a sensitivity check.
- Do not define the segment from `used_3p_result` during the test. The panel can change what users click, so in-test labels are post-treatment and would unbalance the arms.
- Users with no pre-period sessions (new signups, `users.signup_date` after 2026-06-01) can't be classified. Report them as a separate "unclassified" group and say how many there are.
- Check that arm is balanced within the segment (counts, pre-period activity, share of 3P users).

## First test
Among pre-period 3P users, compare treatment and control on per-user success rate over 2026-09-01 to 2026-09-28. Regress on arm with tenant fixed effects (stratify by tenant), using robust standard errors. Do not cluster by tenant, because tenants were not treated whole. It fails if the 95% interval on the effect excludes the minimum worth acting on, or is negative, or the effect is clearly smaller than in non-3P users. Contrast with non-3P users to show whether 3P is where the panel helps.

## Tenants
- Use them as strata (fixed effects) in the user-level analysis.
- Tenant size runs from 5 to 9,000 seats, so a pooled user-level estimate is dominated by large tenants. Report per-user pooled results and check for heterogeneity by tenant size band. Leave-one-out on the largest tenants shows whether a few tenants drive the result.
- Report the sales '3P power' label only as a secondary cut, with the share of its users who are 3P by behavior.

## Metric caveats
- Success = click with at least 30s dwell, or answer copied. Copying an answer is likely possible only where the panel shows an answer, so it may count for treatment only. Compute success both with and without the copy component. Without it, the metric is comparable across arms.
- A panel that answers directly can cut clicks and dwell (deflection). That would look like a loss on the click metric even when users are satisfied. Also look at sessions per user, reformulations and abandonment as guardrails.
- Success is a proxy for satisfaction, not a direct measure of it.

## Questions
1. What size of success-rate change would make the PM turn the panel on by default?
2. Does the PM mean the behavioral 3P user or the sales '3P power' tenant? The two groups differ.
3. Can the copy action occur in the control arm?

## Open
- Whether `used_3p_result` is logged the same way in both arms. If the panel changes how it is set, the pre-period definition is still safe, but in-test comparisons are not. Check the pre-period field by arm.
- Sample-ratio mismatch and the balance of arms in the 3P group are unchecked. Run them before the effect estimate.
- Minimum detectable effect for the 3P group has not been computed. Do it with the 3P user count and the per-user variance once the data are queried.

## Premises
- Users randomized 50/50 within every tenant: given (notes).
- 412 tenants, about 180k active users, 61 tenants labelled '3P power': given.
- Session logs reach back to 2026-06-01: given, not yet queried.
- `used_3p_result` populated in the pre-period for both arms: [guess].
- Minimum effect of about 1 point: [guess].

Unit: user (the randomized unit), with per-user success rate over the test window
Segment: a 3P user is a user with at least one session with used_3p_result true in the pre-test period 2026-06-01 to 2026-08-31, taken from that user's own session logs; the tenant 'segment' label is not used
Tenants: strata (fixed effects) in the user-level analysis, with no tenant-level clustering since users were randomized within tenants; the sales '3P power' label and tenant size are secondary heterogeneity cuts only
