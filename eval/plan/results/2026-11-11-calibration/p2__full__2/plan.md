# Plan: does the AI answer panel help 3P users?

Decision: PM decides whether to turn the panel on by default for 3P users. Options: on by default for 3P users, stay opt-in/test-only, or on for everyone. Smallest change that matters: [guess] a +1 pp lift in per-user success rate, or any harm for 3P users. Needs confirming with the PM.

## Unit
Users were randomized 50/50 inside every tenant, so estimate at the user level. A tenant-level rollup would leave 412 units instead of about 180k and would add no power. Success is logged per session, so collapse it to one number per user: success sessions / sessions, plus sessions per user as a guardrail. Both come from the test window, 2026-09-01 to 09-28. Users with zero sessions need handling. Include them in the sessions-per-user guardrail and drop them from the rate.

## Who counts as a 3P user
Use the user's own behavior before the test, not the tenant label. `tenants.segment = '3P power'` is set by sales from connector count at the tenant level. Most users in those 61 tenants may never open a 3P result, and standard tenants contain heavy 3P users. Both would blur the segment.
- Definition: share of a user's sessions with `used_3p_result = 1` over the pre-period, 2026-06-01 to 08-31. Segment is "3P user" if that share is at or above a threshold, with a minimum session count.
- Fix the threshold before looking at results, and report a sensitivity check with two other cutoffs and a continuous version.
- Use only pre-period data, so the segment cannot be affected by the panel. Users with too few pre-period sessions, including new signups from `users.signup_date`, go into a separate "unclassified" bucket. Report how many there are.
- Report the overlap with the sales label: how many "3P power"-tenant users are 3P users by behavior, and how many 3P users sit in standard tenants.

## Tenants
Tenants are strata, not the unit. Randomization was within tenant, so the main estimate is the treatment-vs-control difference, adjusted for tenant (tenant fixed effects or tenant-stratified differences). That removes the tenant-size effect, since tenants range from 5 to 9,000 seats, and is more precise. Cluster standard errors by tenant only if treatment was assigned to whole tenants, and it was not. As a robustness check, report the estimate with tenant-clustered errors and with large tenants down-weighted, to show a few 9,000-seat tenants do not drive the result. The `segment` label is used only as a secondary comparison, never as the definition of a 3P user.

## First test
Verify the randomization: arm balance (about 50/50) within tenant, in the segment, and on pre-period activity (A/A check on June to August). Then estimate the treatment effect on per-user success rate for behavior-defined 3P users, adjusted for tenant, with a confidence interval. Fails if: arms are imbalanced, with a sample ratio mismatch or different pre-period behavior, in which case fix assignment or data before any effect is read. The panel is "not shown to help" if the lower CI bound for 3P users is below zero or below the PM's minimum useful lift.

## Analysis steps
1. Check inputs: confirm `search_sessions` covers 06-01 to 09-28, `arm` is populated on every row, and `arm` in sessions matches `arm` in `users`. Drop sessions from users not assigned in the test.
2. Build the pre-period 3P share per user, assign segments.
3. Estimate the effect: all users, 3P users, non-3P users, and the difference between them (interaction), all adjusted for tenant.
4. Guardrails: sessions per user (the panel could cut searches by answering directly), and success rate by pre-period activity level.
5. Metric validity: see below.
6. Heterogeneity within the 3P segment by tenant size and by new vs returning users, and weekly effects to check for novelty.

## Questions
1. Is the success metric (click with 30 s dwell, or answer copied) a fair measure for the panel? An answer shown on the panel can remove the need to click, which lowers dwell-based success even when the user is better served. Check the click and copy components separately.
2. Which minimum lift does the PM need, and is "3P user" for the PM a behavior (uses 3P results) or a customer type (tenant with connectors)?
3. Were there other changes to the product or connectors during 09-01 to 09-28 that hit one arm differently? Randomization covers this in principle; confirm assignment was sticky per user.

## Open
- The PM's and sales' meaning of "3P power" is unresolved. If the PM means the tenant label, I report that cut too, as a secondary view, and flag it as a coarser proxy.
- Power for the 3P segment is unknown until I count users in it. If too few, the answer will be "inconclusive for 3P", not "no effect".
- `used_3p_result` is session-level and may be affected by the panel itself, which is why the segment uses only pre-period sessions.

## Premises
- Randomization was by user, within tenant, 50/50: given (notes).
- 412 tenants, about 180k active users, 61 "3P power" tenants: given.
- Session logs from 2026-06-01 exist: given, not yet queried [guess] that they have `used_3p_result` populated for the whole pre-period.
- Pre-period behavior predicts in-test 3P use: [guess], check on control users.
- Success metric reflects user value: [guess].
- Minimum lift of interest: [guess].

Unit: user (the randomized unit); per-user success rate over the test window, adjusted for tenant
Segment: a 3P user is a user whose own pre-test share of sessions with a 3P result (used_3p_result, 2026-06-01 to 08-31, minimum session count) is at or above a pre-set threshold; the tenants.segment sales label is not used to define it
Tenants: strata only; tenant fixed effects or stratified differences in the user-level analysis, tenant-clustered errors and size-weighting as robustness checks, and the sales segment label as a secondary comparison
