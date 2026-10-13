**Ready for triage: Not ready**

The prereg "win" is probably failure behavior, and the metric the hypothesis is about moved the wrong way. Triage will ask about both.

## Why the metrics moved

**1. Queries per User is +2.6% (CI ±0.9%, p<0.001).** This is the prereg primary, and it clears the 1% bar even at the lower bound. It is probably not an engagement gain, for three reasons:
- Reformulation Rate is +5.5% (0.143 → 0.151, p≈0). That is the largest and cleanest move in the table.
- Clicks per User (+0.46%, p=0.26) and Sessions per User (+0.42%, p=0.10) are flat. Users are searching more within a session without clicking more.
- Successful Search Rate (SSR) and CTR are both slightly down.

The likely story is that v7 returns worse first-page results for some queries. Users retype the query, which inflates query count and reformulations. The data is consistent with that story but doesn't prove it. A "queries up" win is only a win if the extra queries are productive.

**2. SSR is −0.45% (−0.185pp, CI about −0.85% to −0.05%, p=0.027).** This is the metric the hypothesis names ("raises the share of searches that end in a successful click"), and it is significantly down. Two problems follow:
- The prereg primary (Queries per User) and the metric configured in Statsig and named in the hypothesis (SSR) disagree. Someone needs to explain that before the meeting.
- The result is p=0.027 with no multiplicity correction. Pulse has bonferroni and sequential testing off, and there are about 55 metrics on the scorecard. I would call it a likely small regression, not a proven one.

**3. Latency p95 is +0.2% (CI ±0.5%).** The guardrail passes against the 2% margin. Ranker cost doesn't explain the other moves.

**4. Autocomplete Acceptance is +0.97% (p=0.001).** I can't explain this from the data. It could be a downstream effect of more query activity, or it could mean v7 changed something upstream of the results page. The engineer should be ready for the question.

**5. Everything else is noise.** CTR, Long Click Rate, Abandonment, Zero Result, Ad Click Rate, Revenue per User, Pagination and Time to First Click all have CIs spanning zero. Don't let anyone tell a story about those.

**6. The segment p-values are not findings.** The scorecard has dozens of segment rows. Informational SSR (p=0.047), Informational CTR (p=0.017) and Mobile Reformulation (p=0.047) are roughly what chance produces across about 55 tests. Desktop SSR (+1.5%, p=0.001) is the only one that stands out. Treat these as hypotheses for the deep dives, not explanations.

## Deep-dive cuts to run

1. **Reformulation chain analysis.** Split queries by whether the next query is a reformulation, and compare the success rate of the final query in a chain. This is the cut that tests the main story. If it holds, the extra queries are reformulation chains that end in no more clicks than control, and Queries per User should be reported as a failure signal.
2. **Queries per User decomposed into reformulation and non-reformulation queries.** The expectation is that nearly all of the +0.31 queries/user comes from the reformulation component.
3. **Informational vs navigational queries.** Informational SSR (−0.41pp) and CTR (−0.26pp) lean down and navigational leans up. The cut should show v7 hurting open-ended queries and being neutral or slightly positive on navigational ones. Treat this as a hypothesis, since it isn't significant after correction.
4. **Device (mobile vs desktop).** Desktop SSR is +0.73pp and mobile is −0.07pp. Mobile reformulation is up (+1.8%), so I'd expect the reformulation problem to concentrate on mobile and desktop to look healthy.
5. **Autocomplete Acceptance by path.** Check whether the lift comes from users who reformulate. If so, it is a symptom of query churn and not an independent benefit.

## Data issues to settle first

- **Mobile and desktop don't add up.** Overall SSR is −0.185pp, but mobile is −0.068pp and desktop is +0.73pp. An overall average can't fall below both segments. Either there is a third segment (tablet or other), the arms have a mix shift in device, or the segment definitions differ from the overall metric. The segment rows also all report 1,000,000 units, so they look like full-population placeholders and not real segment denominators. Confirm the cut definitions before showing any device story.
- **The pulse is stale.** It is dated 2026-09-25. The experiment started 2026-09-12 and the plan ended 2026-09-26, but the config still shows "active" on 2026-10-13. Re-pull the results and confirm whether the experiment was stopped.
- **Unit counts are off.** Each arm shows 1.0M users against the 900k planned. That isn't a problem by itself, but it should be explained, for example by the 20% allocation in the layer or a longer ramp. The balanced-exposure health check passed.
- **Time-trend data stops at day 12.** The days-since-exposure series for SSR runs only to day 12 of 14. It is flat at about −0.4% to −0.5% with every daily CI spanning zero, so novelty or primacy effects don't explain the result. The daily values repeat in an exact three-day pattern, which looks synthetic, so confirm the source before citing it.
- **The audit log is empty.** It shows no history, not even creation. Confirm the config wasn't edited after launch.

## What to tell the engineer

Don't present "Queries per User +2.6%, passes the bar" as a win. The engineer should say that the prereg primary technically clears the bar but is most likely driven by reformulations, that SSR is modestly negative, and that these cuts are in progress. Recommend no ship until the reformulation analysis is back. Ready with open questions would only apply after the pulse is refreshed and the device inconsistency is resolved.