**Ranker v7 did not move the primary metric, and it made latency, abandonment and CTR worse. It should not ship as it stands.**

## Why each metric moved

| Metric | Result (test vs control) | What to say |
|---|---|---|
| **Successful Search Rate (primary)** | 0.412 vs 0.412, change 0.0%, CI ±0.3% relative (±0.0012 absolute), p=1.0 | This is a precise null. The CI's upper end is about +0.12pp, well under the 0.005 bar, whether the bar is absolute or relative. The pre-reg requires the point estimate to reach the bar, so it fails. The hypothesis is not supported. |
| **Latency p95** | 412 → 437 ms, +6.0% (CI ±0.8%), p<0.001 | This is real. The v7 model costs about 25 ms. It is inside the pre-registered 0.1 margin, but only if the margin is relative, which is my assumption. |
| **Abandonment Rate** | 18.7% → 19.0%, +1.6% (CI ±0.4%), p<0.001 | This is real and in the wrong direction. It is inside the 0.03 margin, again assuming the margin is relative. The CI's worst case is about +2.0%, so there is little headroom. |
| **CTR** | 30.5% → 30.0%, −1.5% (CI ±0.4%), p<0.001 | This is real, and it is the one the engineer will be asked about most. |
| Everything else | Long clicks, reformulations, queries, sessions, clicks per user, revenue, ads, zero-result rate, pagination, autocomplete and time to first click are all non-significant with CIs spanning zero | Nothing else moved. |

**Explaining the CTR drop.** The honest account is that the data doesn't show why. The engineer should offer hypotheses and label them as hypotheses.
- **Latency:** slower pages could cause both more abandonment and fewer clicks. Latency, abandonment and CTR all moved the same way, which fits.
- **Fewer low-value clicks:** the new ranker might remove accidental or bounce clicks. SSR and long-click rate being flat fits this, but the data doesn't distinguish the two stories.
- **No change in what users search for:** queries per user and zero-result rate are flat, so this is not a query-mix or retrieval-coverage effect.

**Not a novelty effect.** The effect by days since exposure is flat at about 0 on every day from 1 to 12, with CIs of about ±0.6%. There is no early lift decaying and no ramp.

## Deep-dive cuts to run, and what each would show

1. **Latency-bucket cut** (fast vs slow responses, within each arm) for abandonment, CTR and SSR. If the latency story holds, the damage concentrates in slow responses (above about 500 ms). Fast responses should look neutral or slightly positive on SSR.
2. **Latency-matched comparison** of test against control. If the CTR and abandonment gaps shrink toward zero, latency explains them. If they persist, the ranking itself is changing click behavior.
3. **Click-quality breakdown:** the CTR drop split into long clicks (dwell above a threshold) and short clicks. If the lost clicks are mostly short, the "fewer bounce clicks" story holds. Long-click rate is flat overall, which points that way.
4. **Rank-position click distribution** (clicks by result position 1, 2, 3 and so on). This shows whether v7 reshuffles which results get clicked even though success rate is the same.
5. **Device and query-type cuts, but only after the reconciliation issue below is fixed.** At face value, Mobile SSR is −0.8% (p=0.053) and Head and Tail clicks per user are about −1.7% (p≈0.07). Treat these as hypotheses, not findings.

## Problems with the data to raise first

- **The segment metrics don't reconcile with the totals.**
  - Abandonment is 18.7% overall in control, but both its Head (23.6%) and Tail (21.2%) segments are above that, and so are both query-type groups.
  - Mobile (44.6%) and Desktop (50.0%) SSR are both above the 41.2% overall.
  - A partition's rates must bracket the overall rate, so these segments use different denominators or definitions from the headline metrics.
  - Don't explain headline movement using the segment rows until someone confirms how they are defined.
- **There are about 50 segment tests with no multiplicity correction.** The experiment has `bonferroniCorrection: false`, and none of the segment cuts is pre-registered. The few nominal hits are consistent with chance. Long Click Rate on Desktop (p=0.033) and Mobile SSR (p=0.053) are examples. Don't present them as findings.
- **Sample size is above plan.** 1.0M units per arm were observed against 900k planned. This is minor, but the engineer should know it.
- **The pre-reg doesn't say whether the bar and margins are relative or absolute.** The conclusions above hold either way for the primary. The guardrail verdicts depend on it.
- **The audit log is empty and the health check passed** (exposures balanced). No config changes occurred mid-run, so there is no contamination concern.

## Verdict

The primary result is a clean null, and the guardrail costs are clear, so the call is straightforward: don't ship, and either optimize v7's latency or rework it. What is unresolved is why CTR and abandonment moved, plus the segment reconciliation issue. The engineer can present the conclusion confidently but needs those open questions listed.

Ready for triage: Ready, with open questions