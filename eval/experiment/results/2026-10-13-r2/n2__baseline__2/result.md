Decision: No effect found

The readout is saved at `readout.md` in the working directory.

**Primary metric:** Successful Search Rate moved from 0.4120 to 0.41225. That is +0.00025, with a 95% CI of [-0.0010, +0.0015] and p = 0.70. The pre-registered ship bar was +0.005, and even the CI's upper end is far below it. The test was well powered (about 1M users per arm against 900k planned), so this is a precise null and not a lack of power.

**Guardrails:** All four stay inside their pre-registered margins, even at the worst end of the CI. That covers p95 latency, abandonment, zero-result rate and revenue per user. I assumed the margins are relative, since the pre-registration doesn't say. v7 does no harm, but it also shows no benefit.

**Health:**
- Exposures are balanced.
- Only `ranker_model` differs between arms.
- The audit log is empty, so there were no mid-test changes.
- The experiment still shows `status: active`, although its 14-day window ended around 2026-09-26. It should be stopped.

**Tail queries (exploratory):** Successful Search Rate for tail queries is up 1.46 pp (p < 0.001), which would survive a Bonferroni correction across the roughly 35 slices. It was not pre-registered, so I treated it as a lead for a follow-up test and not a reason to ship. The one other nominal hit, navigational CTR at p = 0.027, looks like noise given about 55 comparisons.

**Recommendation:** Don't ship v7 as a general launch. If the team wants the tail gain, pre-register a tail-targeted test. Confirm the tail definition and its share of traffic first.