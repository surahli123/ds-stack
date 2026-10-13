**Ranker v7 triage prep**

**Scorecard (Pulse, ds 2026-09-25, day 14 of 14, 1M users per arm, CUPED off, 95% CI)**

| Metric | Change | Read |
|---|---|---|
| Successful Search Rate (primary) | +0.28 pt, +0.68% relative (CI ±0.4%), p=0.0009 | Significant lift |
| CTR | −1.1% (±0.4), p<0.001 | Down |
| Clicks per User | −1.2% (±0.7), p=0.0008 | Down |
| Abandonment Rate (guardrail) | +2.1% (±0.6) | Significantly worse, but inside the 4% margin |
| Latency p95 (guardrail) | +0.2% (±0.5) | Flat, margin is 2% |
| Autocomplete Acceptance | −0.69%, p=0.025 | Weakly down |
| Long Click, Reformulation, Time to First Click, Queries, Sessions, Zero Result, Revenue, Ad Click, Pagination | all flat, p>0.2 | No effect |

**Ship criteria**
- The pre-registration says ship requires the point estimate to be at the bar, with a bar of 0.005.
- Read as relative, like the guardrail margins of 0.02 and 0.04, the bar is met: +0.68% against 0.5%. The CI lower bound (+0.28%) is below the bar, but the rule only asks for the point estimate.
- Read as an absolute 0.5 pt, it fails: +0.28 pt. The margins only make sense as relative, so I read the bar the same way. Confirm that with whoever wrote the pre-registration before the meeting.
- Both guardrails pass.
- There are no config problems. Exposures are balanced and the audit log is empty, so nothing changed mid-run. Duration is complete (started Sep 12, ds Sep 25). Both arms have identical parameters except `ranker_model`.
- The lift is stable by days since exposure, at about +0.64% to +0.72% every day. That argues against a novelty effect.

**Why the metrics moved**

The data doesn't give a mechanism. These are hypotheses to test.
- **Successful Search Rate up, CTR and Clicks per User down.** The most natural story is that the new ranker puts the right result higher, so users need fewer clicks, and fewer clicks are bounces. This predicts a fall in short or low-value clicks and a stable or rising share of searches with a successful click.
- **The data only partly supports that story.** Long Click Rate is flat (+0.18%, p=0.55), Time to First Click is flat, and Reformulation is flat. So the success gain isn't visibly backed by long clicks. Don't claim "better satisfaction" yet.
- **Abandonment up 2.1% is the awkward number.** It's significant and moves the opposite way to the primary. It could be:
  - good abandonment, where users get their answer from the page without clicking, which would also explain the CTR drop; or
  - real harm, where some users find nothing and leave.

  The data can't tell these apart. This will be the first question at triage.
- **The CTR drop is concentrated on desktop.** Desktop CTR is −1.28% (p=0.011), while mobile is +0.29% (not significant). Mobile Reformulation is +2.0% (p=0.043).
- **Treat the segment p-values as exploratory.** There are about 55 segment tests with no multiplicity correction, so 2 to 3 false positives at p<0.05 are expected. Report them as leads, not findings.

**One thing to fix before the meeting: the segment cuts don't add up to the headline**
- Overall Successful Search Rate is +0.28 pt. Every cut is at or below that:

| Cut | Change |
|---|---|
| Mobile | −0.10 pt |
| Desktop | −0.11 pt |
| Head queries | +0.02 pt |
| Tail queries | −0.18 pt |
| Navigational | −0.11 pt |
| Informational | +0.01 pt |

- Mobile and desktop partition traffic, so a +0.28 pt overall can't come from two negative parts. The same goes for head/tail and nav/info. Randomization rules out a mix shift between arms.
- The segment rows also each show 1,000,000 units, the same as the total, which a subset shouldn't.
- Likely causes are that the cuts use a different definition or denominator, or that they aren't exhaustive. Check how the segment metrics are defined in Statsig.
- If the cuts are right, the headline is suspect. If the headline is right, the cuts are mislabeled. Either way the engineer shouldn't present the segment table as is.

**Deep-dive cuts to run next, and what each would show**
1. **Reconcile segments to the total.** Recompute the primary by platform and by query type from raw events. Expected: the parts average to about +0.28 pt. If they don't, find the definition mismatch first.
2. **Abandonment split into good and bad.** Cut abandonment by whether the page had a direct answer or a rich result, and by dwell time and next-query behavior. If good abandonment is driving it, the rise is benign and tracks the CTR drop. If it sits on tail queries or zero-result-adjacent queries, it's real harm (tail is +1.07%, p=0.16, which is suggestive but weak).
3. **Click composition.** Break clicks into short and long (dwell above the long-click threshold), and into clicks by rank position. The story predicts fewer short and low-rank clicks, with long clicks unchanged.
4. **Desktop vs mobile.** Check desktop CTR with a pre-specified, single-test CI, plus mobile reformulation. This tells whether the two exploratory leads are real.
5. **Check the primary's definition.** Confirm whether the denominator is searches or sessions, and whether it includes searches with no click. A change in the denominator could produce a ratio lift with fewer clicks.
6. **Query-type cut (head, tail, nav, info) of CTR and success after step 1 is fixed.** Don't interpret it until then.
7. **Optional: CUPED re-run.** It tightens the CIs and should leave the point estimate about the same. It wasn't used here, and it shouldn't change the conclusion.

**Verdict**

The pre-registered primary is met under the relative reading, guardrails pass, and the lift is stable over time. What's open is the reconciliation of the segment cuts to the headline, the bar's units, and the unexplained abandonment increase.

Ready for triage: Ready, with open questions