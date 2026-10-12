Decision: Don't ship

I also saved the readout as `readout.md` in the working directory.

**Why:** The pre-registration says to ship only if both primary metrics reach their +0.5 pt bar. Neither does.

| Primary metric | Change (95% CI) | Bar | Result |
|---|---|---|---|
| Successful Search Rate | +0.33 pt (+0.17 to +0.50), p=7e-5 | +0.50 pt | Real lift, but below the bar. The top of the CI sits just under it. |
| Long Click Rate | +0.03 pt (−0.11 to +0.16), p=0.70 | +0.50 pt | Flat. The CI rules out the bar. |

**Setup:** This is a clean 50/50 randomized test on userID, with about 1M units per arm. The exposure-balance check passed and the audit log is empty, so nothing changed mid-test. Only `ranker_model` differs between arms. Pulse was read once at the planned end, so the plain 95% CIs are valid for the two primaries.

**Guardrails:** All four are within their pre-registered margins.
- Latency p95 is +0.2% (margin 2%).
- Abandonment rate is +0.1% relative (margin 1%).
- Zero result rate is unchanged (margin 3%).
- Revenue per user is −0.1%, with a CI of roughly −0.8% to +0.6% (margin 1%).

**Secondary metrics:** I read about 60 secondary and segment metrics with no multiplicity correction. A few cleared p<0.05, which is about what chance alone would give, so I didn't act on them:
- Queries per User is up.
- Tail-query CTR is up.
- Head-query Long Click Rate is down. This one is worth a follow-up look.

**Config mismatch:** The Statsig config lists only Successful Search Rate as primary, but the pre-registration has two. I used the pre-registration.

**Override option:** If the review wants to ship below the bar, that overrides the pre-registration. It should be made as an explicit escalation. The review would need to weigh a +0.17 to +0.50 pt Successful Search Rate gain against a flat Long Click Rate.