**Bottom line:** Ranker v7 did not move the primary metric, so it fails the ship criterion. The test is clean and conclusive. The engineer can present it, but two things need an explanation first.

## Is the setup sound?
- **Config:** the config matches the prereg. The only change is `ranker_model`, `snippet_length` is the same in both arms (160), and the audit log is empty, so nothing changed mid-flight.
- **Allocation:** each arm has 1.0M users against 900k planned, and the exposure health check passed.
- **Timing:** the experiment ran 14 days (Sep 12–26) and Pulse is dated Sep 25. Statsig's sequential testing and Bonferroni correction are both off, so p-values are nominal.
- **Guardrails:** all four guardrails pass at 95% CI.

| Guardrail | Change (95% CI) | Margin |
|---|---|---|
| Latency p95 | +0.2% ± 0.5% | 2% |
| Abandonment | +0.1% ± 0.6% | 1% |
| Zero Result Rate | 0 ± 1.4% | 3% |
| Revenue per User | −0.1% ± 0.7% | 1% |

## Why the metrics moved
- **Primary, Successful Search Rate:** it moved by exactly 0.000 (41.2% in both arms, p=1.0). The CI is ±0.12pp, so the +0.5pp bar is ruled out, not just missed.
  - The exposure-day trend is flat at about ±0.04% every day for 12 days. There is no novelty effect or late drift hiding in the average.
  - The engineer should say "no effect, and we can exclude the effect we needed". They should not say "inconclusive".
- **CTR (+2.4%) and Clicks per User (+2.2%):** these are the only large, significant moves, and they are the headline question for triage.
  - The extra clicks did not become successes. Long Click Rate is −0.1% (not significant), Abandonment is flat, and Successful Search Rate is flat.
  - A plausible reading is that v7 surfaces more clickable results, or better snippets or titles, but the clicks are short or low-value. That is a hypothesis, not something the data shows.
- **Reformulation Rate (−0.9%, p=0.027):** this is directionally good but weak. It is one of about 15 secondary metrics, so it is consistent with chance. Don't present it as a win.
- **Everything else:** queries, sessions, time to first click, ad clicks, pagination, autocomplete and zero results are all flat.

## Two things that don't reconcile
1. **CTR contradicts its own segments.** Overall CTR is +0.0073, but every CTR segment is negative: mobile −0.0016, desktop −0.0050, head −0.0012, tail −0.0009, navigational −0.0015, informational −0.0009. The overall change should sit between the segment changes unless the segments have different denominators or there is a mix shift.
2. **Clicks per User segments don't add up either.** Head is −0.052 and tail is about 0, yet overall is +0.079. Mobile plus desktop is +0.079, which does reconcile.

Before the meeting, find out whether this is a segment-definition problem (overlap, unassigned users, a different denominator) or a real mix shift. Until then, the engineer shouldn't lean on the CTR lift as real.

## Deep-dive cuts to run
1. **Reconcile CTR and Clicks per User.** Compute them from raw logs by segment with consistent denominators. I expect the overall lift to either shrink or trace to a specific segment or an unsegmented population.
2. **Click quality.** Split clicks into short and long, with dwell-time buckets and pogo-sticking. I expect the extra clicks to be short ones, with no gain in long clicks.
3. **Click position and result type.** Look at click-position distribution and a snippet or title click breakdown. I expect more clicks at lower ranks or on a new result type, which would explain more clicks with the same success rate.
4. **Searches and queries per user.** Check whether CTR is clicks per search or per user, and whether query volume shifted. I expect it to be flat, so this should rule out a denominator artifact.
5. **Reformulation by segment.** The nominal hits are mobile (−0.0020, p=0.058) and navigational (+0.0025, p=0.043, the wrong direction). I expect noise. If I'm wrong, the mobile result would be worth a follow-up test.

Several segment cells have p<0.05 (desktop CTR, navigational reformulation, navigational time to first click). With about 48 segment metrics, two or three such hits are expected by chance, so the engineer shouldn't build a story on them.

## Recommendation
Don't ship. The prereg requires the point estimate to reach the bar, and it is 0.0 against 0.005. The follow-up is to decide whether the extra clicks justify a v7 iteration aimed at success, not clicks.

Ready for triage: Ready, with open questions