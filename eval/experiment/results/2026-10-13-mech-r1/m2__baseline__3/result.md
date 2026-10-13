**Verdict: Ranker v7 should not ship, and the evidence for that is solid.** The primary metric moved the wrong way by a statistically clear margin. Some of the "why" is still a hypothesis, and the segment tables don't add up to the topline (details below).

## Scorecard and what to say

| Metric | Result | What to say |
|---|---|---|
| **Successful Search Rate** (primary, bar +0.5pp) | −0.30pp (−0.72%), 95% CI ±0.16pp, p=0.0004 | It missed the bar and is significantly negative. The whole CI is below zero, so the best case is about −0.13pp. The pre-reg says ship requires the point estimate at the bar, so this is a clear no-ship. |
| **Reformulation Rate** | +0.69pp (+4.8%), p≈0 | This is the most likely mechanism. Users are more often rephrasing after the first results. It matches the SSR drop in size and direction. |
| **Queries per User** | +2.3%, p=1e-6 | Not an engagement win, even though it is tagged "increase". Sessions per user are flat (−0.06%, p=0.82), so the extra queries are retries within a session. This follows from the reformulation increase. |
| CTR, Long Click Rate, Clicks per User | Within about ±0.2%, all p>0.4 | No detectable change. SSR dropped without a matching click drop, so the lost successes appear to be reformulations, not abandonment. |
| **Abandonment, Zero Result, Latency p95, Revenue per User** (guardrails) | Abandonment +0.1%, Zero Result 0.0%, Latency +0.2%, Revenue −0.1% | All guardrails pass. The worst-case CI bounds stay inside the pre-registered margins (Revenue's lower bound is about −0.8% against a −1% margin). Latency is not the cause. |
| Ad Click Rate | +1.4%, p=0.02 | Treat as noise unless it replicates. Revenue is flat, and this is one of about 57 metrics tested. |

Two points to make unprompted:
- **The effect is stable, not a novelty effect.** The daily series by days since exposure sits at −0.68% to −0.76% from day 1 through day 12, and every daily CI excludes zero. There is no ramp or decay to wait out. Only 12 of the 14 days are in that series, which is a minor gap.
- **The experiment itself looks sound.** The exposure health check passed, the 50/50 split gives 1.0M units per arm (planned 900k), the config changed nothing mid-flight (the audit log is empty), and the only parameter that differs between arms is `ranker_model`.

## Things triage may push on

- **Multiple comparisons.** Sequential testing and Bonferroni are both off. Of 57 metrics, 8 have p<0.05, and 3 of those are the real story (SSR, Reformulation, Queries per User). The other five are Ad Click Rate, Desktop Abandonment, Tail Reformulation, Informational Long Click, and Tail Clicks per User. Roughly 2–3 false positives are expected by chance, so don't build narratives on them. Desktop Abandonment, for example, moved in the good direction, which contradicts the overall story.
- **The segment cuts don't reconcile with the topline.** Mobile (+0.17pp) and Desktop (+0.18pp) SSR are both positive, yet overall SSR is −0.30pp. Head (−0.01pp) and Tail (−0.08pp) are also both far smaller than the overall drop. Control means don't reconcile either: Mobile 0.429 and Desktop 0.471 are both above the overall control mean of 0.412. Either there is a third platform or segment not shown, or the segment metrics use a different definition or denominator. I can't tell which from these files, and the engineer shouldn't explain the topline using these cuts until it's resolved.
- **Stale pulse.** The experiment started 2026-09-12, and the pulse is from 2026-09-25 (day 14). The experiment is still `active` today, 2026-10-13. Confirm whether it is still running, and refresh the pulse if so.

## Deep-dive cuts to run next

1. **Reformulation breakdown, as a bridge to SSR.** Split searches into those with a click, those reformulated, and those abandoned, then check whether the lost successes show up as reformulations. This is the direct test of the mechanism. Expect abandonment to stay flat and reformulated-then-eventually-successful sessions to rise.
2. **Query type (head/tail, navigational/informational).** Expect the damage to concentrate in tail and informational queries. The weak hints so far are Tail Reformulation +2.1% and Tail Clicks −2.1%, but the SSR differences between segments are not significant. This cut should be framed as exploratory, and the segment definitions need reconciling first.
3. **Platform, including any missing third segment.** This resolves the inconsistency above. Expect the segments to sum to the topline once every platform is included.
4. **Position of the first click and rank displacement.** Check whether v7 pushes previously successful results down or reorders the top 3. Expect a lower first-click rank and more "result moved" cases among queries that were successful under v6.
5. **Per-query regression analysis.** Find the query clusters where v7 loses the most, for example ones where it replaced a navigational result. This is what the model owners need for a v7.1.
6. **Query-level SSR within user** (users who ran both a reformulated and a first-try query). Optional check that the 2.3% rise in queries per user is the same effect as the reformulations.

I would not spend time on a time-trend cut, a latency cut, or the ad and revenue metrics. The first two are flat or passing, and the last is noise.

## Recommendation for the meeting

The engineer should present this as a clean negative result. The new ranker lowers search success by about 0.7% relative. The likely cause is more reformulations, not slower or emptier results. No guardrail is breached, and the effect is stable from day 1. The decision is no-ship, with the reformulation and query-type cuts as follow-ups for the next iteration. The engineer should say plainly that the segment tables don't reconcile and that the mechanism is still a hypothesis.

Ready for triage: Ready, with open questions