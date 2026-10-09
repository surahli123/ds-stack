# Approve the hybrid labeling approach (about $18k/quarter) by Oct 20

## The ask

Morgan, please approve or reject option C, an LLM judge with human calibration, at about $18k/quarter, by Oct 20. The vendor renewal has to be cancelled before Oct 31, and cancelling is only safe once the approach is approved.

## Recommendation

Approve option C. It cuts label cost from about $60k to about $18k per quarter (about 70% lower) and turnaround from 3 weeks to 2 days for non-EU queries. It keeps humans where the LLM judge is least safe: EU queries and a monthly drift check. The eval team (4), search infra (2) and I agreed on this in the Oct 7 meeting.

## Options

We need about 6,000 query-result labels per quarter for the offline NDCG eval. Costs and turnaround for B and C are estimates; the pilot measured agreement only.

| Option | Cost per quarter | Turnaround | Main risk |
|---|---|---|---|
| A. Human raters only (today) | about $60k | 3 weeks | Slow, and raters agree only 0.71 on tail queries |
| B. LLM judge only | about $4k | same day | Drift, and no legal approval for EU |
| C. Hybrid (recommended) | about $18k | 2 days (non-EU) | Drift, caught monthly |

**A is trusted but blocks ranker iterations.** The 3-week turnaround is the bottleneck. Human labels are also noisy on tail queries: agreement is about 0.71 (Jamie's figure from the meeting).

**B is cheap and fast but not available as stated.** A pilot last month on 1,200 labels gave 0.82 agreement with the human majority label (Cohen's kappa 0.74). Legal has not approved sending query logs to the provider for all markets, and EU is the blocker. Kappa also fell to 0.61 after a provider model update during the pilot (Priya's observation), and nothing in B would have detected that.

**C keeps B's speed and adds a way to see drift.** The LLM judge labels everything outside the EU. Humans label all EU queries, so no EU logs go to the provider. Humans also label a 15% calibration sample each month (about 900 labels), and we compare judge and human labels on it.

## What kappa 0.74 supports

The team's view after long discussion: 0.74 is good enough to compare rankers, and not good enough for absolute quality numbers reported to leadership. This is a judgment from the meeting, not a tested threshold. Under option C, leadership-facing absolute quality should still come from human labels.

## Risks and what we'd watch

- **Judge drift.** If monthly kappa on the calibration sample falls below 0.65, we use human labels for that month. The pilot's post-update kappa of 0.61 would have tripped this rule. The cost of a fallback month is not estimated.
- **Calibration sample size.** About 900 labels a month is the agreed design. We have not computed how precisely it estimates kappa.
- **Legal.** Option C depends on EU queries staying human-labeled. Non-EU markets are assumed cleared because only EU was named as a blocker; this needs confirming with legal.
- **Vendor.** The $18k estimate includes human labeling for EU and the calibration sample. Before cancelling the renewal, we need to confirm where that human capacity comes from, and that it can scale up for a fallback month.

## Out of scope

A fine-tuned in-house judge was discussed and deferred past this quarter.

## What we need from you

1. Approve or reject option C and its budget of about $18k/quarter by Oct 20.
2. If approved, we cancel the vendor renewal (or renegotiate it to the reduced scope) before Oct 31.
