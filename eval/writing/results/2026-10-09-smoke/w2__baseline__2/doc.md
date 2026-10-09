# Decision memo: relevance labeling for the offline eval

**To:** Morgan (Eval Lead)
**Decision needed by:** Oct 20, 2026
**Why that date:** The vendor renewal must be cancelled before Oct 31.

## Decision requested

Approve **option C (hybrid)**, with a budget of about **$18k per quarter**. The eval team and search infra agreed on this at the Oct 7 meeting. Option C replaces the current ~$60k per quarter vendor spend, a saving of about $42k per quarter. If you approve, we cancel the vendor renewal. If you reject, we renew the vendor and keep today's process.

## Background

The offline NDCG eval needs about 6,000 query-result labels per quarter. Human raters at the vendor produce all of them today. That costs about $60k per quarter and takes 3 weeks, which blocks ranker iterations.

## Options considered

| | A: Human raters (status quo) | B: LLM judge only | C: Hybrid (recommended) |
|---|---|---|---|
| Cost per quarter | ~$60k | ~$4k | ~$18k |
| Turnaround | 3 weeks | Same day | 2 days (non-EU) |
| Quality evidence | Rater agreement ~0.71 on tail queries | Pilot (1,200 labels): 0.82 agreement with human majority, kappa 0.74 | Same judge as B, plus monthly human check |
| Main problem | Slow and expensive | Drift, and EU legal block | More moving parts than B |

- **Option A:** Trusted, but slow and expensive. Raters also disagree often on tail queries.
- **Option B:** Cheapest and fastest. In the pilot, kappa fell from 0.74 to 0.61 after a provider model update. Legal has not approved sending query logs to the provider for all markets, and EU is the blocker. These two problems rule it out.
- **Option C:** The LLM judge labels everything except EU queries. Humans label all EU queries. Humans also label a 15% calibration sample (~900 labels) to measure drift.

Building our own fine-tuned judge was discussed and put out of scope for this quarter.

## Why option C

- It cuts turnaround from 3 weeks to 2 days for non-EU queries, so ranker iteration is no longer blocked.
- The human calibration sample detects drift, the failure seen in the pilot.
- Human labeling of EU queries avoids the legal blocker.
- It costs less than a third of the current spend.

## Limits of the judge

The team's view is that kappa 0.74 is good enough for **comparing rankers**. It is **not** good enough for reporting **absolute quality** to leadership. Under option C, absolute-quality numbers shouldn't go to leadership without further validation.

## Risk and mitigation

**Risk:** Judge drift, for example after a provider model update.

**Mitigation:** Compute kappa on the human calibration sample every month. If it falls below **0.65**, that month's labels fall back to humans.

## Open items

- **Budget arithmetic:** The notes say the 15% sample is ~900 labels per month. 15% of 6,000 labels per quarter is ~900 per quarter, or ~300 per month. We should confirm which figure the $18k estimate assumes before you sign off.
- **Fallback cost:** A fallback month means paying for human labels on top of the judge. The $18k estimate may not cover this.
- **EU volume:** The EU share of queries drives the human-label cost, and the notes don't state it.
- **Vendor timing:** Cancelling the renewal removes the vendor as an immediate fallback. We should confirm that the vendor can be re-engaged on short notice, or that a fallback month can be covered another way.

## Next steps if approved

1. Cancel the vendor renewal before Oct 31.
2. Set up monthly calibration sampling and the kappa check.
3. Continue working with legal on approval for EU markets. Until then, humans label all EU queries.
