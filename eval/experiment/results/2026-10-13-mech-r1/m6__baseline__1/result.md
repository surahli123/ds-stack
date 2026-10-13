**Bottom line:** Ranker v7 raised Successful Search Rate (SSR) by less than the bar the team pre-registered. The aggregate lift also doesn't show up in any device or query-type cut. The engineer can't yet explain why the metrics moved, so I'd hold the readout.

## What the scorecard says

| Metric | Result | Verdict |
|---|---|---|
| **SSR (primary)** | +0.33pp (+0.81%), 95% CI [+0.17, +0.50]pp, p=7e-5 | Significant, but the point estimate is below the 0.5pp bar. Prereg says `ship_requires: point_at_bar`, so it fails. The CI's upper end only just touches the bar. |
| Guardrails (latency, abandonment, zero-result, revenue) | Latency +0.2%, abandonment +0.1%, zero-result 0.0%, revenue −0.1% | All CI bounds are inside the prereg margins. Revenue's worst case is about −0.8% against a 1% margin, so it's close. |
| CTR | +2.1%, p≈0 | Probably a denominator effect (see below) |
| Queries per user | −1.9% (−0.22), p≈0 | The one unexplained significant move |
| Long click, clicks/user, sessions, ad clicks, reformulation, time to first click | All flat | Nothing moved |

Exposure is balanced (1M per arm against 900k planned). The audit log is empty, so there were no mid-test changes. The two arms differ only in `ranker_model`. The daily lift by days since exposure is flat at about 0.8% (0.77–0.85%), so there's no novelty decay.

## Why the metrics moved

- **CTR +2.1% is mostly a smaller denominator, not more clicking.** Queries fell 1.9% while clicks per user (+0.1%) and long clicks (flat) didn't move. The same click count over about 2% fewer queries gives about 2% higher CTR. The engineer shouldn't say "users click more."
- **SSR +0.81% is likely partly the same effect.** If successes stayed constant and queries fell 1.9%, the rate would rise about 1.9%. The observed +0.81% is smaller, but I can't separate real quality from denominator shrinkage with this data. This is the core open question.
- **The cause of the query drop is unknown.** Reformulation rate is flat, so reformulations fell in proportion. Abandonment, sessions and clicks are flat, so users aren't giving up. Candidate causes are:
  - v7 resolves intents in fewer queries, which would be good.
  - Fewer low-value or repeat queries.
  - A change in how queries are logged or counted. This is not ruled out.
- **Flat long-click rate, ad clicks and revenue** say the extra CTR isn't producing more satisfying clicks or more money.

## A red flag: the segments don't reconcile with the headline

The overall SSR is +0.33pp, but every split with a negative or mixed sign sits below it:

- Mobile −0.04pp and desktop −0.12pp.
- Head −0.05pp and tail −0.15pp.
- Navigational +0.16pp and informational −0.38pp.

An overall rate should be a weighted average of a partition, so it should fall between the segment values. Here the overall is above both device cuts. The same thing happens with CTR: overall +0.64pp, mobile −0.05pp, desktop −0.34pp. A query-mix shift could explain part of it, since the query denominator moved. I doubt it explains all of it. It could also be a pipeline or segment-definition problem. The segment metrics are not pre-registered, and none are individually significant.

Three segment cells have p<0.05: CTR on tail queries, and long-click rate on desktop and on tail queries. There are about 54 segment metrics with no multiple-comparison correction, so about 3 hits is what chance gives. Don't build stories on them.

## Deep-dive cuts, in priority order

1. **Decompose SSR into numerator and denominator** (successful searches and total searches per user, by arm). I expect the denominator to be down about 2% and the numerator to be flat or slightly up. That would mean the lift is largely a rate artifact.
2. **Query-count drop by query type.** Split by repeat or reformulated queries, autocomplete-triggered queries, and head versus tail. If the missing queries are repeats or re-fires, v7 is genuinely resolving intent faster. If they're evenly spread, suspect logging.
3. **Reconcile segments to the total.** Check that mobile + desktop sums to the overall figure for users, queries and successes, and look at the query-share mix by arm. This resolves the weighted-average contradiction.
4. **SSR on a per-user basis**, such as users with at least one success. This sidesteps the changing query denominator.
5. **Logging check on query counting.** Compare client and server query events by arm.

## Open items

- Pulse is dated 2026-09-25 (day 14), but today is 2026-10-13 and the experiment still shows "active". Confirm the engineer is presenting the final pull.
- The daily series stops at day 12 of exposure, and its 3-day repeating pattern is suspiciously regular. Verify it isn't a template or interpolated.
- Queries-per-user direction is set to "increase" in the config, but nothing pre-registered says whether fewer queries is good or bad. Decide that before triage.

## How to present it

"SSR is up 0.33pp, statistically significant but under our 0.5pp ship bar. Guardrails are clean. The CTR and SSR gains coincide with a 2% drop in queries, so we're checking how much is real quality versus a denominator effect. We're not recommending ship on this data."

Ready for triage: Not ready