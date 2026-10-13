**Ready for triage: Not ready**

The prereg primary (Queries per User) looks like a win, but the metrics around it say the new ranker is probably worse. The engineer needs a defensible story first.

## Setup checks

- **Allocation:** 1,000,000 units per arm against 900,000 planned, with a 50/50 split and the exposure-balance check passed. There's no sample-ratio problem.
- **Config changes:** The audit log is empty, so nothing changed mid-run. The arms differ only in `ranker_model`, as intended. `snippet_length` is 160 in both.
- **Timing:** The experiment ran 2026-09-12 to 09-26 (14 days). Pulse is dated 09-25 and the by-exposure-day file stops at day 12. Today is 10-13 and the experiment is still marked "active". Pull a final Pulse at the full 14 days.
- **Stats settings:** Pulse was run without CUPED, with no sequential testing and no Bonferroni correction. About 70 metrics and cuts are on the page, so roughly 3 to 4 false positives at p<0.05 are expected.

## The pre-registration doesn't match the experiment

- **Primary metric:** The prereg names Queries per User (QPU). The Statsig config and the hypothesis use Successful Search Rate (SSR). The engineer must say which one was the real primary before anyone asks.
- **Ship rule:** The prereg requires the point estimate to clear a +1% bar.
- **QPU result:** QPU is +2.6%, with a CI of about +1.7% to +3.5%. On paper that clears the bar and the primary passes.
- **Hypothesis:** The hypothesis is about successful searches, and SSR is down. If the engineer presents QPU as the headline, expect pushback.

## Why the metrics moved

| Metric | Result | Reading |
|---|---|---|
| SSR | −0.45% (CI −0.85% to −0.05%, p=0.027) | Significantly worse. This is the metric the hypothesis is about. |
| Reformulation Rate | +5.5% (p<0.001) | Worse (lower is better), and the most robust movement on the page. |
| QPU | +2.6% (p<0.001) | Probably not engagement. See below. |
| CTR, Clicks/User, Long Click Rate, Sessions/User, Abandonment | All flat (p>0.09) | No extra clicks or sessions came with the extra queries. |
| Latency p95 | +0.2% (CI about −0.3% to +0.7%) | Guardrail passes, since the upper bound is well inside the 2% margin. |
| Revenue, Ad Clicks, Zero Result Rate, Time to First Click | Flat | No harm visible. |

- **QPU:** The most likely explanation is that users re-query because the first results are worse. Reformulations rise by about 0.8 percentage points, SSR falls, and clicks and sessions don't move. More queries with no more clicks or sessions reads as extra searching, not more engagement.
- **Not proven:** This is a story consistent with the data, not a demonstrated mechanism. A query-level cut is needed to confirm it.
- **Autocomplete Acceptance:** It is up about 1% relative (p=0.0015). A ranker change shouldn't touch autocomplete unless the two share a model or index. This is either an unintended side effect or a real shared-component effect, and the engineer should find out which.
- **Novelty effect:** The by-exposure-day SSR delta is flat at roughly −0.4% to −0.5% on days 1–12, with every daily CI including zero. There is no novelty or learning pattern, so this doesn't look like a transient effect. The file doesn't label the metric (it matches SSR), and the daily CIs are wide.

## Deep-dive cuts to run, and what each should show

1. **Query-level sequences (reformulation chains).** Split QPU into first queries and follow-up queries per session.
   - If the story holds, the QPU gain comes entirely from reformulated follow-ups, and first-query SSR is down.
   - If extra queries show up as new sessions or topics instead, the "worse results" story is weaker.
2. **Informational vs. navigational queries.** Informational SSR is −0.85% (p=0.047) and informational CTR is −1.2% (p=0.017). Navigational is flat to slightly positive.
   - Expect the damage to concentrate in informational queries. That fits a ranker tuned toward navigational intent.
   - These cuts are nominal and uncorrected, so present them as leads, not findings.
3. **Platform: desktop vs. mobile (and any other platform).**
   - Desktop SSR is +1.5% (p=0.001) and mobile is −0.2%. Mobile reformulation is +1.8% (p=0.047, nominal).
   - The cuts should confirm that desktop gains while mobile or another platform loses.
   - They also don't add up. Overall SSR is −0.185 percentage points, but mobile is −0.07 and desktop is +0.73. The overall figure can't sit below both unless there is a third platform or the cut definitions differ.
   - Reformulation has the same problem. Overall is +0.79 percentage points, but every cut shown (mobile, desktop, head, tail, navigational, informational) is ≤0.3. That is impossible if the cuts partition the traffic.
   - Before the engineer shows any segment table, find the missing platform or segment (tablet, app, logged-out) and check how the ratios are defined. Right now the segment tables can't be trusted to explain the overall result.
4. **Autocomplete-driven queries vs. typed queries.** If acceptance is up, some of the extra queries may be autocomplete-assisted. This tests whether the QPU lift and the autocomplete lift are the same thing.
5. **Heavy vs. light users.** QPU is a mean, so a small group of heavy users could be driving it. Check the distribution, and run a winsorized or per-user-capped QPU.

## What to tell the engineer

- Don't lead with "QPU passed the prereg bar." Lead with "QPU rose, but SSR fell and reformulations rose, so the extra queries are likely failed searches."
- Be ready to say which metric was the primary and why the prereg and config disagree.
- Treat the segment results as exploratory until they reconcile with the totals and are corrected for multiple comparisons.
- The experiment currently supports a "do not ship" recommendation. The engineer needs to resolve the primary-metric mismatch, run the cuts above, and refresh Pulse to the full 14 days before the meeting.