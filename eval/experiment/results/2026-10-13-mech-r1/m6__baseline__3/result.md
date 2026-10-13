**Ready for triage: Ready, with open questions**

The scorecard is clean, but the headline win doesn't hold up as a ranking-quality win yet. The engineer should present it as "SSR is up, and we're still working out why."

## What the data shows

- **Experiment health:** The run was 14 days (Sep 12–25) with 1.0M units per arm. Exposures are balanced and the audit log is empty, so there were no mid-test changes. The only changed parameter is `ranker_model`; `snippet_length` is 160 in both arms.
- **Primary (Successful Search Rate, SSR):**
  - SSR is 41.20% → 41.53%, a change of +0.33 pt absolute or +0.81% relative (p=7e-5, CI ±0.165 pt).
  - The effect is flat across days (about +0.8% every day), so it isn't a novelty effect.
  - **The bar's unit is ambiguous.** The prereg says `0.005` with no unit, and the ship rule is that the point estimate must reach the bar.
    - Read as relative (0.5%), SSR passes: 0.81% is above the bar.
    - Read as absolute (0.5 pt), it fails: +0.33 pt is below the bar.
    - The guardrail margins (0.02, 0.01, 0.03) look relative, so relative is probably what was meant. Confirm that before the meeting.
- **Guardrails:** All four pass non-inferiority, with each CI inside its margin.

  | Guardrail | Change | CI half-width | Margin |
  |---|---|---|---|
  | Latency p95 | +0.2% | ±0.5% | 2% |
  | Abandonment | +0.1% | ±0.6% | 1% |
  | Zero Result Rate | 0.0% | ±1.4% | 3% |
  | Revenue per User | −0.1% | ±0.7% | −1% |

  Abandonment and Zero Result Rate have unusually wide intervals relative to their margins, so "passes" is a weaker statement for them.

## Why the metrics moved

The ratio metrics look like they moved because the denominator shrank, not because users got more successes.

1. **Queries per User fell 1.9%** (11.80 → 11.58, p≈0). It is the biggest move on the scorecard and it goes the wrong way. Sessions (−0.08%, p=0.76) and Clicks per User (+0.1%, p=0.81) are flat.
2. **CTR's +2.1% is arithmetic.** Clicks are flat and queries are down, so clicks ÷ queries rises: 3.6036 / 11.5758 = 0.3114, which matches the reported CTR. Long Click Rate is flat (−0.03%, p=0.92), so there is no sign of better clicks. The engineer shouldn't say CTR shows relevance improved.
3. **SSR is partly the same effect.** Successes per user are roughly 4.86 in control and 4.81 in test, which is flat to slightly down. Fewer searches with the same successes pushes the ratio up.
4. **The segment SSRs disagree with the overall number.** Mobile −0.04 pt, Desktop −0.12, Head −0.05, Tail −0.15, Informational −0.38, Navigational +0.16, while the overall is +0.33. Mobile and desktop together make up all users, so a pooled gain can't come from two negative (or zero) segment deltas unless the mix of queries changed. This points to a mix shift: the queries that disappeared were disproportionately low-success ones. The segment CIs are wide (±0.25–0.43 pt), so the negatives aren't individually significant. The conflict with the overall result is still the thing to explain.
5. **The nominally significant segment cells are probably noise.** CTR Tail is up and Long Click Rate Desktop is down. Long Click Rate Tail is up at p=0.048, which is borderline. There are about 40 segment cells and no multiple-comparison correction, so you'd expect about 2 hits by chance. Don't build a story on them.

## Deep-dive cuts to run, in priority order

1. **Queries per User, split by query type and by day.** I expect the drop to be concentrated in one query class, probably informational or reformulation-style queries. Check whether those lost queries had below-average success.
2. **Fixed-denominator SSR: successful searches per user and per session, and SSR on a fixed query mix.** If successes per user are flat and the mix-adjusted SSR is about 0 or negative, the "win" is mix shift or lost queries.
3. **Query-volume breakdown by cause.** Split users who search less into:
   - **Fewer reformulations.** Reformulation Rate and abandonment are flat, which argues against this.
   - **Users giving up.**
   - **A logging or instrumentation difference** in how queries are counted under the new ranker.
   
   Also check whether autocomplete or the query-suggestion path changed. Autocomplete acceptance is flat (+0.12%, p=0.68).
4. **Desktop and Informational segments.** These have the most negative point estimates (Desktop Long Click Rate −1.7%, Informational SSR −0.9%). Check them for a real regression with more power, such as the full 14 days pooled or a CUPED run.
5. **A CUPED rerun and heterogeneity by user tenure.** The pulse was run without CUPED, so there is variance reduction available. Tenure would also show whether heavy searchers drive the query drop.

## Answers for the likely questions

- **"Is it a novelty effect?"** No. The effect is stable from day 1 to day 12.
- **"Did latency or revenue regress?"** No. Both are within their margins.
- **"Why did CTR go up?"** Fewer queries with the same clicks. It isn't evidence of better relevance.
- **"Should we ship?"** Not on this evidence. The SSR lift may be a denominator and mix artifact, and the bar's unit is unresolved. The recommendation should be to hold until cuts 1–3 are back.