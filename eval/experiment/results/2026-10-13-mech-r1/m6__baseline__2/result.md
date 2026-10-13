**Short version:** Ranker v7 has a small, statistically significant lift on the primary metric, but it misses the pre-registered bar if the bar is absolute. Most of the headline movement looks like a denominator effect, because queries per user fell 1.9%. The engineer can present, but not as a win.

## Scorecard facts

| Item | Result |
|---|---|
| Design checks | Complete 14-day run (Sep 12–25). Exposure-balance check passed. 1.0M units per arm, against 900k planned. Only `ranker_model` differs between arms (`snippet_length` is 160 in both). The audit log is empty, so there were no mid-flight changes. |
| Primary: Successful Search Rate | +0.0033 absolute (+0.81% relative), 95% CI [+0.0017, +0.0050], p=7e-5. |
| Bar | Prereg `bar: 0.005` and `ship_requires: point_at_bar`. The point estimate of 0.0033 is below an absolute 0.005, and the CI upper end (0.00499) only just stays under it. |
| Guardrails | All four pass, with the CI bounds inside the margins. Latency +0.2% (upper bound ≈ +0.7%, margin 2%). Abandonment +0.1%. Zero Result Rate 0.0%. Revenue per User −0.1% (lower bound ≈ −0.8%, margin 1%). |

## Why the metrics moved

- **CTR +2.1% (p≈0):** This is almost entirely the denominator. Clicks per user are flat (+0.1%) and queries per user are down 1.9%. The arithmetic matches: 1.001 / 0.981 ≈ +2.0%. Long-click rate, ad clicks, revenue and time to first click are all flat, so there is no sign that clicks got better.
- **Queries per user −1.9% (p≈0):** This is the real movement, and the scorecard will show it as a regression because its direction is "increase". Sessions per user are flat, so users are issuing fewer queries per session. The data doesn't say why. The reformulation *rate* is flat, which is odd if the cause were fewer failed-and-retried queries.
- **SSR +0.81%:** Part of this is probably the same denominator effect. If successful searches per user were flat, SSR would rise about 1.9%. It rose only 0.81%, which implies successful searches per user may be down about 1%, not up. That is my back-of-envelope inference, not a measured result. It needs the count metric to confirm.
- **Segments contradict the overall numbers:**
  - Mobile and desktop SSR deltas are both negative (−0.0004 and −0.0012), yet the overall delta is +0.0033.
  - Mobile and desktop CTR deltas are both negative, yet the overall delta is +0.0064.
  - Abandonment overall is +0.0002, below both of its segment deltas (+0.0018 and +0.0007).
  - An overall value can't sit outside its segments' range unless the segment mix shifted between arms. The −1.9% query drop is a plausible cause. If the queries that disappeared were disproportionately low-success ones, the overall rate rises without any segment improving (a Simpson's-paradox effect).
- **Segment significance is noise:** Three of the 48 segment cuts have p<0.05 (CTR tail +1.4%, long click tail +1.2%, long click desktop −1.7%). That is about what chance alone gives across 48 cuts, with no multiplicity correction. Don't build a story on them. "Helps tail queries" is a hypothesis to test, not a finding.
- **Over time:** The days-since-exposure file shows a steady ~+0.8% relative lift with no decay, so no novelty effect. It covers only days 1–12 of 14, and its provenance is unclear, so don't lean on it.

## Deep-dive cuts, in priority order

1. **Counts per user, not ratios:** Successful searches, clicks, long clicks and reformulations per user. I expect successful searches per user to be flat or slightly negative (about −1%), clicks flat, and long clicks flat. That would confirm the ratio lifts come from fewer queries rather than more success.
2. **Mix-shift decomposition of the SSR and CTR deltas:** Split into within-segment effect and mix effect, by device and by head/tail and navigational/informational. I expect the within-segment effects to be about zero or slightly negative, and the mix term to account for the positive overall delta. Also check that device and query-type segments partition the same population as the overall metric.
3. **Where the missing queries went:**
   - Queries per session by query position (first query vs follow-ups).
   - Sessions with one query vs several.
   - Queries per user by segment.
   
   I expect the drop to concentrate in follow-up queries or a specific segment. That would decide whether it means "resolved faster" or "less engaged".
4. **Tail-query hypothesis:** Check tail CTR and long click against a corrected significance threshold, and see whether the effect holds across the daily cohorts. I expect it to shrink toward zero. If it holds, it's the best positive story available.
5. **Time series through day 14, by calendar date:** Confirm there is no decay and no late drift.
6. **Metric definitions:** Confirm the denominators of SSR and long-click rate (per query or per click), and whether they are ratios of sums or per-user averages.

## Open questions to settle before the meeting

- **Is the 0.005 bar absolute or relative?** The prereg doesn't say. If it is absolute (0.5 percentage points), v7 misses it. If it is relative (0.5%), the +0.81% clears it. Check with whoever wrote the prereg, and don't argue it in the room.
- **Is the query drop a benefit or a loss?** Settle this before claiming a quality improvement.

## Recommendation

Frame it as "significant but small SSR lift, guardrails clean, and we are checking whether it reflects better results or just fewer queries". Don't recommend ship until cuts 1–3 are in.

Ready for triage: Ready, with open questions