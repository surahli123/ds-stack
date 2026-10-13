**Ready for triage: Ready, with open questions**

The experiment ran cleanly, but the headline result is a clear loss, and some of the segment numbers don't add up. The engineer can present the result tomorrow. They should not claim the segment cuts explain it.

## Validity
- **Config:** The config matches the pre-registration. The change history in `audit_logs.json` is empty, so nothing was changed mid-run.
- **Run length:** It ran 14 days, from Sep 12 to Sep 26, and the Pulse snapshot is from Sep 25, the last full day. Exposure balance passed, with 1.0M units per arm against 0.9M planned.
- **Stats settings:** I recomputed the CI and p-value for the primary and for Queries per User, and both match the Pulse output. Sequential testing and Bonferroni correction are off. That fits a fixed-horizon test read once at the end.

## Why the metrics moved
- **Primary, Successful Search Rate (SSR):**
  - **Result:** It fell from 41.20% to 40.90%, a change of -0.30pp (-0.72% relative). The 95% CI is about [-0.46, -0.13]pp and p=0.0004.
  - **Against the bar:** The pre-registered bar was +0.5pp, and the point estimate has to reach it. The result is missed by about 0.8pp, and the whole CI sits below zero. This is not "flat" or "underpowered". It is a probable small regression.
  - **Stability:** The effect is stable across days since exposure, at about -0.7% every day. There is no novelty or learning curve, so waiting longer won't turn it around.
- **Reformulation Rate:** It rose by 0.69pp (+4.8%) with p≈0, the largest move on the scorecard. Queries per User rose 2.3% (p≈1e-6).
  - **Likely mechanism:** v7 returns results that make users retype or refine their query. Users search more but succeed less often.
  - **Caveat:** The data supports this link but doesn't prove it.
  - **Reading Queries per User:** The engineer should not present this metric as a win for engagement.
- **Unchanged metrics:**
  - CTR, Long Click Rate, Abandonment, Sessions per User, Time to First Click, Clicks per User, Pagination and Autocomplete are all flat.
  - The four guardrails are all within their margins: latency +0.2%, abandonment +0.1%, zero-result 0.0%, revenue -0.1%. The guardrails passing does not offset the primary miss.
- **Ad Click Rate:** It is +1.4% relative with p=0.02. This is one of about 60 metrics with no correction, so treat it as noise unless it replicates. It doesn't offset the SSR loss either way.

## Segment cuts that look significant
There are about 54 segment rows. At 5%, roughly 3 would show up significant by chance, and 4 do:
- Desktop abandonment, p=0.014, an improvement.
- Tail reformulation, p=0.012, worse.
- Informational long-click rate, p=0.04, worse.
- Tail clicks per user, p=0.027, worse.

These are not evidence of anything on their own. I would not give any of them a causal story.

## The segment numbers don't reconcile
- **SSR by device:** Mobile is +0.17pp and desktop is +0.18pp, yet the total is -0.30pp. If those two were the only segments, the total could not be negative.
- **SSR control means:** Mobile is 42.9% and desktop is 47.1%, but the overall control mean is 41.2%, below both.
- **Reformulation by device:** Mobile and desktop are both at or below zero, but the total is +0.69pp.
- **Likely explanations:**
  - There is a third device group, such as tablet or unknown, that isn't in the cuts.
  - The segment metrics use a different denominator, such as only users with a classified query.
  - Every segment row shows 1.0M units, so the segment rows may not be restricting users at all.

The engineer should check these definitions before quoting any segment number. If asked, they should say "the segment metrics don't sum to the top line and we're checking why."

## Deep-dive cuts to run next
1. **Reconcile the segments.** Pull the metric definitions and the exposure share by device and query type. Add the missing device group or confirm the denominators. Everything below depends on this.
2. **Reformulation by query type.** Tail queries are the only segment where reformulation clearly rises (+0.24pp). I expect the SSR loss to concentrate in tail and informational queries (-0.08pp and -0.20pp in the current cut). Navigational queries look neutral to positive (+0.28pp) and head queries are flat.
3. **Reformulation type.** Split query refinements, such as adding terms or narrowing, from complete rewrites. This tests the "users retype because ranking misses" story.
4. **Rank position of the first click.** Check whether v7 pushes the first successful result further down. I'd expect the click-rank distribution to shift lower, which would point to a ranking-quality problem rather than a UI one.
5. **Per-user SSR distribution.** Compare quantiles to see whether a subset of users is hurt or the loss is spread evenly. The flat daily trend suggests an even loss, but this is cheap to confirm.
6. **Session-level SSR with queries per session.** Check whether the SSR drop comes from extra failed reformulation queries inflating the denominator. If sessions eventually succeed, the real harm may be extra effort rather than failed tasks.

## Talking points for the engineer
- **Decision:** Do not ship v7. The primary regressed, with the CI entirely below zero and well short of the +0.5pp bar.
- **What worked:** The experiment was clean, and the guardrails held.
- **What's open:** The mechanism is probably reformulation, but the segment tables need reconciling before they can be used as evidence.
- **Next step:** If v7 is iterated, fix the tail and informational queries first.