**Bottom line:** Ranker v7 did not move the primary metric, and nothing else moved either. There are no real movements to explain, so the engineer shouldn't invent causes.

**Primary: Successful Search Rate**
- Test is 0.41208 against control 0.4120, a change of +0.00008 (+0.02%). The 95% CI is ±0.00124, so roughly −0.0011 to +0.0013, with p=0.90.
- The pre-registered ship bar is +0.005. The upper end of the CI (+0.0013) is well below it, whether the bar is read as absolute or relative (a relative reading is about 0.002 absolute).
- This is a conclusive null, not an underpowered one. The test can rule out the effect size the team needed. The recommendation is not to ship on the primary.

**Guardrails.** All four pass against the pre-registered margins, using the worst end of each CI:

| Guardrail | Observed change | Worst end of CI vs margin |
|---|---|---|
| Latency p95 | +0.8 ms (+0.2%) | about +0.7% vs 2% |
| Abandonment | +0.0002 | about +0.7% relative vs 1% |
| Zero Result Rate | 0.0 | about 1.4% vs 3% |
| Revenue per User | −0.00087 | about −0.8% vs −1% |

Revenue per User has the least headroom. Expect the question "could revenue be down?" The honest answer is that it is flat, but the data can't exclude a loss of about 0.8%.

**Secondary metrics.** Nothing is significant. The nearest misses are Long Click Rate (−0.0012, p=0.08) and Clicks per User (+0.023, p=0.12). Their signs partly conflict with each other (CTR is slightly down while clicks per user are slightly up). That pattern fits noise. If asked why Long Click fell, say it didn't, within noise. Don't offer a story about ranking quality.

**Deep-dive cuts.** Run these only after the segment data are checked (see open questions).
1. **Segment partitions (mobile/desktop, head/tail, navigational/informational).** I expect flat results. Of the roughly 60 metrics and segment cuts, only one has p<0.05 (Time to First Click, tail queries, p=0.039). That is about what chance produces, so don't present it as a finding.
2. **Time to First Click by tail queries and desktop (p=0.039 and 0.057).** These point in opposite directions, so they look like noise. A pre-specified replication or a longer run would settle it.
3. **Days since exposure.** The daily file shows no novelty or decay trend (±0.06%, all CIs include zero). It stops at day 12 and repeats an exact three-day pattern (−0.0002, +0.0002, +0.0006). That is too regular to be real data, so check the pipeline before citing it.
4. **Revenue per User by segment, or a longer run.** This would tighten the guardrail with the thinnest margin.

**Open questions to resolve before the meeting**
- **Segment results contradict the overall result.** Mobile and desktop are both about −0.0015 on Successful Search Rate, yet the overall change is +0.0001. Head/tail and navigational/informational are all positive. If the segments partition users, the overall change must lie between them, and in these cases it doesn't. Every segment row also reports 1,000,000 units per arm, the same as the overall total. Either the segments aren't partitions, or the unit counts or segment definitions are wrong. Until that is explained, don't interpret the cuts.
- **The Pulse run completed.** The Pulse date is 2026-09-25 and the start time is 2026-09-12, which makes 14 days, as planned. The experiment status still reads "active", so confirm it was concluded.
- **Setup looks clean.** The audit log has no changes, only `ranker_model` differs between arms (`snippet_length` is identical), exposures are balanced, and the arms have 1M units against 900k planned. There is no sequential testing or multiple-comparison correction, which is acceptable for a fixed 14-day read on one primary.

Ready for triage: Ready, with open questions