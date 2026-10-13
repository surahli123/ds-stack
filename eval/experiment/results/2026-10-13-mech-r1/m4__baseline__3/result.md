**Short version:** Ranker v7 did not move the primary metric, so the prereg ship rule isn't met. Two secondary metrics moved a lot, CTR down and zero-result rate down. The data you have can't explain either one yet, and you should say so in the meeting. Everything below is from the files in this directory. I haven't run any new cuts.

## Is the setup trustworthy?
- **Design:** Config and prereg agree. Only `ranker_model` differs between arms (`snippet_length` is 160 in both), 50/50 split, and the exposure-balance health check passed.
- **Change history:** `audit_logs.json` is empty, so nothing was changed mid-flight.
- **Duration:** The experiment ran 2026-09-12 for 14 days, and the Pulse snapshot is dated 09-25, which is day 14.
- **Sample size:** Each arm has 1.0M units against 900k planned, so power is at least as good as planned.
- **Pulse settings:** The Pulse call was requested with CUPED off and 95% CIs. There is no sequential testing and no multiple-comparison correction.
- **Day-by-day:** The daily cuts by days-since-exposure are flat at about -0.1% every day, so there's no novelty or decay story.

## Scorecard and what to say
| Metric | Result | What to say |
|---|---|---|
| **Successful Search Rate (primary)** | -0.0004 absolute (-0.1%), 95% CI [-0.0016, +0.0008], p=0.51 | A flat result. The bar was +0.005 at the point estimate, and even the CI's upper end is about 6x below it. The test could have detected a gain this size, so it's not underpowered. The hypothesis isn't supported, and it's not a ship. |
| **Latency p95 (guardrail)** | +0.8 ms (+0.2%), CI ±2.06 ms | Passes. The worst case is about +0.7%, inside the 2% margin. |
| **Revenue per User (guardrail)** | -0.00087 (-0.1%), CI ±0.0061 | Passes, but only just: the lower bound is about -0.8% against a -1% margin. Say "inside margin", not "no impact". |
| **CTR** | -0.0055 (-1.8%), p<0.001 | A real, significant drop. I can't explain it with what's here (see below). |
| **Zero Result Rate** | -0.0037 (-12%), p<0.001 | A real, large improvement. It's unexplained because a re-ranker shouldn't change retrieval (see below). |
| Long Click Rate, Abandonment, Reformulation, Queries, Sessions, Time to First Click, Clicks per User, Ad Click Rate, Pagination, Autocomplete Acceptance | All within noise (p from 0.11 to 0.92) | Nothing to explain. Don't invent stories for these. |

## The two moves triage will push on
**1. CTR is down 1.8%, but the other metrics don't support it.**
- Clicks per User is -0.3% (not significant) and Queries per User is -0.3% (not significant). If CTR were clicks divided by queries, it would be about flat.
- Every segment CTR is at or above -0.0014, yet the overall CTR is -0.0055. Navigational is +0.0039 and informational is +0.0036. Head is +0.001 and tail is -0.001. Mobile and desktop are both about zero.
- A total can't fall outside the range of its segments unless the segment mix shifted, or the CTR denominator isn't what we think (impressions, result-page views or sessions, not queries).
- Don't say "the new ranker gets fewer clicks". The click counts don't show that. Say it's unexplained and that you're checking the CTR definition and the segment mix.

**2. Zero Result Rate is down 12% with no change in Successful Search Rate.**
- Zero-result queries come from retrieval, not ranking. Either v7 changed candidate generation or query relaxation as well, or something else in the `search_ranking` layer overlapped.
- The config can't rule that out, so ask what shipped in `lambdamart_v7`.
- If those queries now return results but nobody succeeds on them, that fits a flat Successful Search Rate and could also feed the CTR dilution. That is a hypothesis, not a finding.

## Segment results are noise
- The segment results are roughly 60 comparisons at 95%, so about 3 false positives are expected. There are 3 at p<0.05:
  - CTR for navigational queries is up (p=0.009).
  - Abandonment for head queries is up, which is the bad direction (p=0.036).
  - Clicks per User for informational queries is down (p=0.020).
- They point in unrelated directions and none survives correction. Don't present any of them as a finding.
- Navigational and informational Successful Search Rate are both about -0.001, yet the overall is -0.0004. That's a small, noisy version of the same mix-shift question.

## Deep-dive cuts, in order
1. **CTR definition and denominators.**
   - Pull numerator and denominator separately per arm: clicks, impressions, queries, sessions.
   - If the denominator, not clicks, moved, it's a measurement artifact. If clicks truly fell, Clicks per User should show it, and it doesn't.
2. **Query-segment mix per arm.**
   - Compare the share of navigational, informational, head, tail, mobile and desktop traffic.
   - If the mix shifted, that explains CTR falling while every segment is flat or up. A mix shift could also point to a logging or classification change.
3. **Zero-result queries.**
   - Split the queries that stopped returning zero results into what they are now (the 3.1% to 2.7% gap), and measure their click and success rates.
   - I expect low success on them, which would explain a flat Successful Search Rate.
4. **Retrieval and layer overlap.**
   - Diff `lambdamart_v6` against `lambdamart_v7` for candidate-set or query-rewrite changes.
   - Check what else ran in the `search_ranking` layer from 09-12 to 09-25.
5. **Successful Search Rate on the queries where the ranker actually reorders results.**
   - This is exploratory only, because the prereg primary is overall Successful Search Rate and it's flat.
   - It will probably show a small effect if the rest of the traffic dilutes it.
   - Any such finding is a hypothesis for a follow-up test, not grounds to ship.
6. **Revenue per User by segment.**
   - It has the thinnest margin (-0.8% against -1%), so confirm it's not concentrated in one segment.

## Readiness
The primary and guardrail answer is clean: don't ship. But the two largest secondary moves can't be explained, and the engineer will be asked about them first. They should present the "no effect" conclusion confidently and treat the CTR and zero-result items as open, with cuts 1 to 3 run before the meeting if possible.

Ready for triage: Ready, with open questions