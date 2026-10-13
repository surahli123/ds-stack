**Ranker v7 did not move the primary metric, and I'd present it as a clean null, not a win.**

Nothing in the config or audit log undermines the headline. The audit log is empty, so nothing changed mid-flight. Only `ranker_model` differs between arms (`snippet_length` is 160 in both), and exposure balance passed. The pulse covers 2026-09-12 to 09-25, the full 14 days, with 1.0M units per arm against 0.9M planned.

## Why each metric moved

| Metric | Result | What to say |
|---|---|---|
| Successful Search Rate (primary) | 0.412 vs 0.412, Δ 0.000 ±0.0012, p=1.0 | There is no effect. The prereg bar is +0.005 and the CI upper end is +0.0012, so the bar is ruled out. The 14-day run was powered for this, so it isn't "underpowered." Ship requires the point estimate at the bar, so it fails. |
| CTR | +0.0073 (+2.4%), p≈0 | Real. |
| Clicks per User | +0.079 (+2.2%), p≈0 | Real. |
| Long Click Rate, Queries per User, Sessions per User | Flat | Searches didn't increase. The extra clicks come from more clicks per search, not more searching. |
| Reformulation Rate | −0.9%, p=0.027 | Directionally good, but it is one of 56 secondary metrics with no multiplicity correction. Treat it as a hint. |
| Guardrails | All pass | Latency +0.2% (margin 2%), Abandonment +0.1% ±0.6% (margin 1%), Zero Result 0.0% ±1.4% (margin 3%), Revenue −0.1% ±0.7% (margin 1%). |

The story for the CTR move is that v7 gets more clicks, but they are not more successful searches. Long-click rate and SSR are both flat. So the extra clicks look like shallow or unsatisfied clicks, such as users clicking a second result, pogo-sticking, or clicking more attractive but not better results. This is a hypothesis, not something the data shows yet. The engineer should say so.

Avoid these claims: "CTR proves relevance improved," and "the ranker works on mobile or head queries." No segment SSR effect exists.

## Deep-dive cuts to run, and what each would show

1. **Dwell-time split of the extra clicks (short <10s vs long).** If the hypothesis holds, the CTR lift sits entirely in short clicks and long clicks are flat.
2. **Clicks per clicked search and click rank position.** I expect more multi-click searches and more clicks at lower ranks.
3. **Searches with at least one click vs clicks per search.** This separates "more searches get a click" from "searches get more clicks." The flat Abandonment Rate suggests the latter.
4. **Exposure-day trend of CTR and Clicks per User.** The supplied daily series is flat around 0 with CIs of about ±0.6%, and it stops at day 12. I can't tell which metric it covers. Re-pull it for CTR to rule out novelty effects.
5. **Segment cuts (device, head/tail, nav/info).** These are only for hypothesis generation. The segment SSR deltas are all within noise, and a handful of nominal p<0.05 hits (CTR-Desktop, Reformulation-Nav, TTFC-Nav) are about what chance gives across 56 metrics.

## Open questions before the meeting

- **The segment metrics don't reconcile with the overall metrics.** Control CTR is 0.305 overall, but Mobile is 0.320 and Desktop is 0.334, so both are above the overall figure. SSR is 0.412 overall, but Mobile is 0.346 and Desktop is 0.401, so both are below it. Also, every CTR segment delta is negative while overall CTR is +0.0073 with p≈0. These can't all be true if the cuts partition the traffic. The segment definitions or denominators are probably different. Check this before anyone quotes a segment number.
- The primary delta and Zero Result delta are exactly 0.000000 with p=1.0. That is plausible but unusually tidy, so confirm the pipeline isn't returning a default value.
- CUPED was off and sequential testing was off. This is fine for a fixed-horizon read.

The decision is don't ship on the primary. Whether to iterate on the ranker or investigate click quality depends on cut 1.

Ready for triage: Ready, with open questions