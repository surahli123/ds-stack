**Short version:** Ranker v7 didn't move the primary metric. The one clear signal is a gain on tail queries that is cancelled out elsewhere. The engineer can present this, but several questions need answers first.

## What the scorecard says

**Primary, Successful Search Rate (SSR):** 41.20% → 41.23%. That is +0.033pp absolute, or +0.08% relative, with p=0.60 and a 95% CI of ±0.124pp.
- The pre-registered bar is 0.005 and ship requires the point estimate to reach it. The point estimate is about 15× short of the bar if the bar is 0.5pp. If it's 0.5% relative, the point estimate is about 6× short (+0.08% against 0.5%).
- The CI upper bound is +0.157pp absolute (+0.38% relative). That is below the bar under either reading, so the result is a flat null, not an underpowered "maybe".
- The answer to "why did SSR move?" is that it didn't. The engineer shouldn't build a story around +0.08%.

**Guardrails** (all inside their margins):

| Metric | Change | Margin |
|---|---|---|
| Latency p95 | +0.2% (+0.8ms) | 2% |
| Abandonment | +0.1% relative | 1% |
| Zero Result Rate | 0.0% | 3% |
| Revenue per User | −0.1%, CI ±0.7% | 1% |

Revenue's CI is the one to be careful with. It is inside the margin, but only just: the lower bound (−0.8%) is close to −1%.

**Secondary metrics:** nothing moved overall. CTR, long clicks, reformulation, time to first click, clicks per user and queries per user are all non-significant. The queries-per-user and clicks-per-user point estimates are slightly negative, so the engineer should expect a question about them.

## The one real signal: heterogeneity by query class

Query class is the only segmentation pre-registered. The mobile/desktop cuts are not, so treat those as exploratory.

| Cut | SSR change | p |
|---|---|---|
| Tail queries | **+1.13pp** (control 33.3%) | <0.001 |
| Head queries | −0.25pp | 0.31 |
| Navigational | **−0.45pp** | 0.02 |
| Informational | +0.06pp | 0.69 |

- **Tail:** the tail gain survives any multiplicity correction. This is the likely mechanism: v7 helps long-tail queries, which fits a new LambdaMART model with better recall or relevance on rare queries. That is a hypothesis, not something the data shows.
- **Navigational:** the drop is plausible. Nav queries have one right answer, and a ranker that reshuffles the top slots can hurt them. It is p=0.02 among dozens of cuts, so it is suggestive only. Nav reformulation rate rises (+0.23pp, p=0.02) and nav clicks per user fall (p=0.06), which hangs together with the SSR drop.
- **Mobile CTR:** −0.44pp, p=0.007. This is an exploratory cut, so treat it as unconfirmed.
- **Why the overall number is flat:** a tail gain offset by head and navigational losses would net to roughly zero.
- **Multiplicity:** there are 56 metrics and cuts in the pull and about 4 nominal hits at p<0.05. That is a little under 3 hits expected by chance at α=0.05 (56 × 0.05 = 2.8). Only tail SSR is clearly beyond chance.

## Deep-dive cuts to run next, and what each should show

1. **Tail × navigational/informational cross.** The head/tail and nav/info splits overlap. This cut shows whether the nav loss sits in head-nav queries (where the "one right answer" story would predict it) and whether the tail gain is concentrated in informational queries.
2. **Query-frequency deciles (finer than head/tail).** If the effect is monotone, with gains growing as queries get rarer, that supports the tail mechanism.
3. **Mobile vs desktop × query class.** This checks whether the mobile CTR drop is just the navigational effect showing up on mobile, or a separate layout effect. Mobile SSR is −0.24pp (p=0.14) with a negative sign, consistent with a real but small effect.
4. **Per-segment weights.** Compute each segment's traffic share multiplied by its effect. This should reconcile to the overall +0.033pp, and it tells the engineer how much tail gain a fix for navigational queries would unlock.
5. **Revenue and ad clicks by segment.** Ad click rate is −0.36% relative. Check whether the losses sit on commercial or navigational queries.
6. **Decision-level question:** would a hybrid (v7 on tail, v6 on head and navigational) clear the bar? That would be a new hypothesis, so it needs a new pre-registered test and can't be claimed from this one.

## Open questions before triage

- **The pull is stale.** The Pulse snapshot is dated 2026-09-25, which is 13 days after the 09-12 start, and the experiment is still marked `active` today (10-13). The daily file stops at day 12. Re-pull final 14-day results so the scorecard matches what was planned.
- **Unit counts.** Pulse shows 1.0M units per arm against 900k planned. Confirm that is just later accrual and not an allocation change. The audit log is empty, so no change was recorded, and exposure balance passed.
- **No time trend.** The daily series is flat (about +0.04–0.12%) across exposure days, so there is no novelty or decay effect to explain.
- **Sequential testing and Bonferroni are both off.** The tail result holds anyway. Say that the segment hits are exploratory, apart from tail.
- **Unconfirmed bar units.** Confirm whether the 0.005 bar is absolute or relative. The conclusion is the same either way, but the engineer should be able to say which.

## Recommendation

Don't ship v7 on this evidence. Present it as a null on the primary, with guardrails clean and a segment story (tail up, navigational down) as the follow-up hypothesis.

Ready for triage: Ready, with open questions