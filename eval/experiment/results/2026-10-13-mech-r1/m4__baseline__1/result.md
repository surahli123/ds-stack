**Short version:** Ranker v7 did not move the primary metric. The 95% interval for Successful Search Rate (SSR) excludes the pre-registered +0.005 bar, so the answer is don't ship. The two real movements, CTR down and zero-result rate down, are not yet explained, and the slice tables don't reconcile with the headline numbers.

## Setup checks
- **Run length:** the run was Sep 12 to Sep 25 (14 days, as planned). It has about 1.0M users per arm against 900k planned, and the exposure-balance health check passed.
- **Config:** the audit log is empty, so nothing changed mid-flight. Only `ranker_model` differs between arms (`snippet_length` is 160 in both), which matches the prereg.
- **Statistics:** CUPED was off, sequential testing was off, and there is no multiple-comparison correction. The pulse has about 50 metrics.

## Why each metric moved

**Primary: SSR is flat.**
- The change is −0.0004 (−0.1%), with a CI of about [−0.0016, +0.0008] and p=0.51.
- The upper bound is far below the +0.005 bar, so this is a null that rules out the hoped-for lift.
- The engineer should not say "not significant, needs more time." The CI already excludes the bar.
- Mobile (−0.0018) and desktop (+0.0008) are both noise (p>0.26).

**Guardrails pass.**
- Latency p95 is +0.2% (worse direction), CI ±0.5%, inside the 2% margin.
- Revenue per user is −0.1%, CI ±0.7%, so the lower bound of about −0.8% stays inside the 1% margin.
- The CIs are wide enough that this means "no evidence of harm," not "proven safe."

**CTR is down 1.8% (−0.0055, about 3.6× its CI half-width, p≈0). This is the one real adverse movement, and it is unexplained.**
- Clicks per user (−0.3%), long-click rate (−0.4%) and queries per user (−0.3%) all lean negative but are not significant.
- SSR didn't move, so the lost clicks were probably low-value ones, such as accidental or exploratory clicks. That is a hypothesis, not a finding.

**Zero Result Rate is down 12% (3.1% → 2.7%, p≈0). This is real and is the only clear win.**
- It is probably a recall or query-handling effect of the new model.
- It did not translate into SSR, long clicks or revenue.
- It also can't simply explain the CTR drop. Queries that used to return nothing can't lower CTR on a per-search basis unless CTR is computed over searches with results and the newly served results are poor. Someone needs to check how CTR is defined.

**Everything else is noise.**
- Abandonment, reformulation, time to first click, sessions, ad clicks, pagination and autocomplete all have p>0.1.
- Three slice results look "significant": CTR for navigational queries (+0.0039, p=0.009), abandonment for head queries (p=0.036) and clicks per user for informational queries (p=0.02). With about 50 uncorrected tests you'd expect 2 to 3 hits at p<0.05, and they point in different directions. The engineer should not build a story around them.

**No novelty or ramp effect.**
- The daily by-days-since-exposure series is flat, around −0.1% with CIs that include zero.
- That series covers days 1 to 12 only, and its values repeat in a fixed 3-day cycle (−0.14%, −0.10%, −0.06%). The engineer should confirm the export is real before quoting it.
- Even taken at face value it only rules out novelty decay. It says nothing about the CTR drop.

## Problem with the slice tables
The slice metrics can't be reconciled with the headline metrics, so don't use them to explain CTR yet.
- **SSR control means:** mobile is 0.328 and desktop is 0.359, but overall is 0.412. A partition can't average above both of its parts. Head (0.471) and tail (0.415) also can't average to 0.412.
- **CTR control means:** head is 0.226 and tail is 0.268, but overall is 0.305.
- **CTR deltas:** the overall CTR delta (−0.0055) is outside the range of every slice delta (−0.0014 to +0.0039). That would need a large mix shift or different metric definitions.
- Either the slices use different definitions or populations (for example, only users with a classified query), or the slice metrics are mis-specified. This is the first thing triage is likely to catch.

## Deep-dive cuts, in priority order
1. **CTR definition and denominator.** Compute CTR over searches with results versus all searches.
   - *If* CTR is per search with results, expect the drop to concentrate in queries that newly return results. That would mean the ZRR win and the CTR loss are one effect.
   - *If* it is per all searches, the drop is a true quality regression in the ranking.
2. **Slice reconciliation.** Re-derive the slice metrics from raw events and check that the slices sum to the totals.
   - If the slices were all-user, CTR would be down in most of them. If a mix shift is behind the gap, it will show up as a large change in the share of searches in some segment.
3. **Zero-result queries, split into "previously zero-result" and "always had results."**
   - I expect the CTR loss to be concentrated in the first group and CTR roughly flat in the second.
   - Check the SSR for the first group too.
4. **Click quality.** Break clicks down by dwell time and rank position.
   - I expect fewer short-dwell or low-rank clicks with long clicks unchanged. That would fit SSR being flat while CTR falls.
5. **Position of first click and query type (head, tail, navigational, informational), only after cut 2 is fixed.** Treat any difference found as hypothesis-generating, not as a result.
6. **Power note.** The CI half-width on SSR is about 0.0012, so the study could detect a lift of about 0.0025 or more. The prereg bar of +0.005 is conservative, and a smaller true lift of 0.001 to 0.002 can't be excluded. If the team wants to chase that, it needs a new, larger experiment.

## Verdict
The decision is clear: the primary missed its bar, so don't ship v7 as is. The open questions are why CTR fell and why the slice tables don't reconcile. The engineer should have answers to both, or say plainly that they are unexplained, before the meeting.

Ready for triage: Ready, with open questions