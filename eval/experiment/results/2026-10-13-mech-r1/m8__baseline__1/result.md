**Ranker v7 triage prep**

**Bottom line:** The prereg primary, Queries per User (QPU), cleared its bar. But the mechanism looks like a regression, not a win. QPU rose because users are reformulating more, while the success metric fell. The engineer should not present the QPU result as a win.

**Scorecard (Pulse, no CUPED, 95% CI, 1.0M units per arm, 2026-09-12 start, data through 09-25)**

| Metric | Rel. change (95% CI half-width) | p-value | Read |
|---|---|---|---|
| Queries per User (prereg primary) | +2.6% (±0.9) | <0.001 | Bar is +1%. The CI of [+1.7%, +3.5%] clears the bar, so it passes the prereg's "point at bar" rule. |
| Successful Search Rate (config primary and hypothesis) | −0.45% (±0.40) | 0.027 | Moved the wrong way. |
| Reformulation Rate | +5.5% (±0.8) | <0.001 | Wrong way (lower is better) and the largest effect on the board. |
| CTR, Long Click, Abandonment, Clicks/User, Sessions/User, Time to First Click | all within noise | 0.10–0.96 | Flat. |
| Latency p95 (prereg guardrail) | +0.2% (±0.5) | 0.43 | Passes. The CI is well inside the 2% margin. |
| Revenue, Ad Click, Zero Result, Pagination | flat | >0.7 | No harm detected. |
| Autocomplete Acceptance | +0.97% (±0.6) | 0.001 | Real, and unexplained. |

**Why the metrics moved (the story to tell)**
1. **QPU is up, but clicks, sessions and long clicks are flat.** Users are issuing more queries per session without getting more clicks. That points to the first results being less satisfying, so users re-query.
2. **Reformulations (+5.5%) account for much of the extra queries.** Reformulation Rate is the share of queries that are reformulations. If they rise from 14.3% to 15.1% of queries, the extra queries are largely retries.
3. **Successful Search Rate is down slightly (−0.45%)**, which fits the same story. The drop is small and p=0.027 is not strong, since many metrics were tested with no correction. The direction is consistent with the reformulation increase, though.
4. **It isn't a novelty effect.** The SSR delta by days-since-exposure is flat at about −0.4% to −0.5% across days 1–12, with no decay. The per-day CIs include zero, so the daily file adds no new evidence beyond the pooled result.
5. **Latency isn't the cause.** It is flat.

**Problems to raise before the meeting**
- **The primary metric is inconsistent across documents.**
  - The prereg primary is QPU (increase, 1% bar).
  - The Statsig config primary is Successful Search Rate, which matches the hypothesis text ("share of searches ending in a successful click").
  - QPU passes only under the prereg metric and SSR fails under the config metric. Triage will see this immediately. The engineer needs to say which one the team committed to and why they differ.
  - QPU is also a weak proxy for the stated hypothesis, because more queries can mean worse search.
- **The platform segments don't add up.**
  - SSR is −0.07pp on Mobile and +0.73pp on Desktop (p=0.001), but the overall effect is −0.19pp.
  - A weighted average can't fall below both segments' values unless there is a third segment (tablet or other) or the platform mix differs between arms.
  - Check exposure by platform for a segment-level SRM (sample ratio mismatch) before trusting any platform cut.
- **Multiple comparisons.**
  - About 56 secondary and segment metrics were tested at 95% with no Bonferroni correction.
  - Expect around 3 false positives. Treat the p≈0.017–0.047 segment hits (Informational SSR, Informational CTR, Mobile Reformulation) as hypotheses, not findings.
  - The Desktop SSR (p=0.001) and Autocomplete (p=0.001) results are stronger but still exploratory.
- **The run looks stale or unfinished.** Pulse ds is 09-25, the planned duration is 14 days from 09-12 (ending around 09-26), and today is 10-13. The config still shows status "active". The audit log is empty, so there were no config changes, but confirm the experiment was stopped, and that the pulse covers the full 14 days. Exposure is 1.0M per arm against 900k planned, which is fine and balanced.
- **Segment definitions are unclear.** Statsig shows no explicit segment-level health checks, so confirm how Mobile/Desktop and Head/Tail are defined.

**Deep-dive cuts to run, and what each should show**
1. **Reformulation decomposition (by type: spelling, narrowing, broadening, same query) and Mobile vs. Desktop.** If the QPU lift is mostly reformulations concentrated on Mobile (+1.8%, p=0.047), v7 is a retry-driving regression there.
2. **Segment SRM by platform and the missing platform bucket.** This should show whether the Mobile/Desktop contradiction is caused by mix shift or an unlisted segment.
3. **Queries per session split into reformulation and non-reformulation queries, and QPU net of reformulations.** If the net lift disappears, the "bar" was cleared by retries alone.
4. **Informational vs. Navigational queries.** Informational shows SSR −0.85%, CTR −1.2% and Navigational +0.4%, which would mean v7 hurts open-ended queries and helps lookups.
5. **Desktop and Autocomplete.** Check whether the Desktop SSR gain is tied to autocomplete acceptance, which might mean the benefit comes from a suggestions interaction rather than ranking. This also bears on whether `snippet_length` or other parameters were truly held constant. Config shows both arms at 160 and only `ranker_model` differing, which matches the intent.
6. **Time-sliced check (week 1 vs. week 2)** with CUPED on. Expect the SSR and reformulation effects to hold and the CIs to tighten.

**Recommendation:** Do not argue for shipping. Present QPU as passing the prereg bar and explain, with the reformulation and SSR evidence, why that isn't a quality win. Acknowledge the prereg-versus-config primary mismatch up front. The mismatch, the platform inconsistency and the stale status are open items that should be fixed before the meeting.

Ready for triage: Not ready