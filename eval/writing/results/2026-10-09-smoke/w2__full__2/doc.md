# Decision: approve the hybrid labeling approach (option C) at about $18k/quarter

## The ask

Morgan, please approve option C and its budget of about $18k/quarter by Oct 20. The vendor renewal must be cancelled before Oct 31, and the cancellation depends on your sign-off. Option C replaces the current human-only process, which costs about $60k/quarter, so it saves about $42k/quarter.

## Recommendation

Approve option C. An LLM judge labels every query, and humans label a monthly calibration sample plus all EU queries. It is the only option that cuts cost and turnaround while keeping a measured check on judge quality.

The judge tracks human labels well enough for comparing rankers: in last month's pilot on 1,200 labels, agreement with the human majority label was 0.82 (Cohen's kappa 0.74). The team's view in the Oct 7 meeting was that this is good enough for ranking comparisons but not for reporting absolute quality to leadership. Under option C, absolute-quality numbers for leadership should still be anchored on the human-labeled sample.

## Options

We need about 6,000 query-result labels per quarter for the offline NDCG eval. Costs for B and C are estimates, not quotes.

**A. Keep human raters.** About $60k/quarter, 3-week turnaround, which blocks ranker iterations. Humans are trusted, but they disagree on tail queries (agreement about 0.71), so the baseline is noisier than it looks.

**B. LLM judge only.** About $4k/quarter, same-day turnaround. Two problems rule it out:
- The judge drifts when the provider changes model versions. In the pilot, kappa fell from 0.74 to 0.61 after a provider update.
- Legal has not approved sending query logs to the provider for all markets. EU is the blocker.

**C. Hybrid.** About $18k/quarter, 2-day turnaround for non-EU queries.
- The LLM judge labels everything it is allowed to.
- Humans label a 15% calibration sample each month (about 900 labels) to measure drift.
- Humans label all EU queries, which sidesteps the legal blocker.

Building our own fine-tuned judge is out of scope this quarter.

## Risks and what we'd watch

- **Judge drift.** Each month we compute kappa on the calibration sample. If it drops below 0.65, we fall back to human labels for that month. The pilot's post-update kappa of 0.61 would have triggered this rule, so the guardrail is calibrated to a drift we have already seen.
- **EU turnaround.** EU queries stay on human raters, so they keep the slower turnaround until legal approves. The notes give the 2-day figure for non-EU only.
- **Fallback cost.** A fallback month costs more than the $18k/quarter estimate because humans label that month's queries. We have not costed this.

## Open question

The notes give "15% calibration sample" and "about 900 labels" per month. But 15% of 6,000 labels is 900 per quarter, not per month. If the sample is 900 a month, it is closer to 45% of volume, and the $18k estimate needs rechecking. I will confirm the sample size and cost with the eval team before Oct 20.

## Source

Meeting notes from Oct 7 (eval team, search infra). The pilot figures come from a single 1,200-label pilot run last month.
