**Short version:** v7 did nothing detectable to Successful Search Rate (SSR), and the data rules out the effect size the team pre-registered. The honest story at triage is "no effect, not shipping on this evidence". One segment result needs a check before the meeting.

## Why the metrics moved

**Primary: SSR.**
- It moved +0.033pp absolute (+0.08% relative), with a 95% CI of ±0.124pp (±0.3% relative) and p=0.60.
- The pre-registered bar is 0.005, and the CI upper bound (+0.157pp, or +0.38% relative) is below it whether the bar is read as absolute or relative.
- So this is not an underpowered "maybe". The test had 1.0M units per arm against 0.9M planned, and it can exclude the effect we hoped for.
- Prereg requires the point estimate to reach the bar to ship. It doesn't, so the ship criterion fails.

**Overall secondary metrics.**
- All 14 non-segment metrics are inside noise: CTR, long click rate, reformulation, queries, sessions, clicks, time to first click, ads, pagination and autocomplete.
- Queries, sessions and clicks per user are all slightly negative (p between 0.15 and 0.34). That is consistent with zero. Don't narrate it as "users are searching less".
- The honest answer to "why did X move?" is that it didn't, and the CI says so.

**Guardrails.** All four pass against their prereg margins, assuming the margins are relative. They would also pass as absolute margins.

| Guardrail | Observed change (95% CI) | Margin |
|---|---|---|
| Latency p95 | +0.2% (±0.5%) | 2% |
| Abandonment | +0.1% (±0.6%) | 1% |
| Zero results | 0% (±1.4%) | 3% |
| Revenue per user | −0.1% (±0.7%) | 1% |

**Health checks.**
- Exposure balance passed.
- The audit log is empty, so the config didn't change mid-flight.
- Both arms differ only in `ranker_model`, with `snippet_length` held at 160.
- Daily deltas by days since exposure sit at +0.04% to +0.12% with CIs that include zero. I see no novelty or decay pattern.
- That file covers only 12 days, while the pulse covers about 14 (start 2026-09-12, ds 2026-09-25). Confirm that's just a lag.

## Deep-dive cuts

I count 48 segment rows (6 segments × 8 metrics). At 95% with no correction (`bonferroniCorrection` is false), expect about 2–3 false positives. Treat them accordingly.

1. **Tail queries, SSR (the one to run first).**
   - The row shows +1.13pp, CI ±0.30pp, p≈0. That survives a Bonferroni threshold of about 0.001 across the 48 rows.
   - It is the only segment effect that does, and "query class" was the pre-registered segment. It is a hypothesis to confirm, not a win.
   - Head queries (−0.25pp, not significant) and navigational queries (−0.45pp, p=0.02) lean negative. A real story would be "helps the long tail, flat or slightly worse on navigational."
   - Next steps: get the tail share of users and check whether tail SSR holds in a holdout or later days. Also check whether the navigational dip is a regression.
   - If it is real, the follow-up is a targeted rollout or a re-test aimed at tail queries. It is not a ship of the current experiment.
2. **Mobile CTR.**
   - It is −0.44pp, p=0.007, but it was not pre-registered and SSR on mobile is not significant (−0.24pp, p=0.14).
   - Expect it to be noise. Split mobile by days since exposure and by query class. If it persists, it is a possible UI or snippet interaction.
3. **Navigational reformulation and SSR.**
   - Reformulation is +0.23pp and SSR is −0.45pp, both p≈0.02. They are consistent with each other, which makes a small real regression slightly more plausible.
   - Cut by navigational sub-intent or brand queries. If real, v7 may reorder the exact-match result.

## Open question to resolve before the meeting

The segment rows don't reconcile with the overall result.
- Using control means to back out segment shares, the segment effects imply different overall SSR changes depending on the cut:
  - Head and tail imply about +0.34pp.
  - Navigational and informational imply about −0.38pp.
  - Mobile and desktop imply about −0.13pp.
- The overall result is +0.03pp.
- Every segment row also reports 1,000,000 units, the same as the total.
- That suggests segments are defined per user with overlap, or are built on a different denominator.
- If someone asks "head −0.25 and tail +1.13 but overall flat?", the engineer needs to know the segment definitions and the denominator. Otherwise the tail result can't be trusted.

## Verdict

The primary, guardrails and health checks are clean and tell one clear story. The only open item is the segment denominator question, which affects the tail-queries lead and not the headline.

Ready for triage: Ready, with open questions