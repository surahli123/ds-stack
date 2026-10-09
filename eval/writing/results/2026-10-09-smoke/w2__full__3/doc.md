# Decision memo: labeling approach for the offline relevance eval

## The ask

Morgan, please approve option C (LLM judge plus human calibration) at about $18k/quarter, by Oct 20. The vendor renewal must be cancelled before Oct 31, and cancelling depends on this approval.

## Recommendation

Approve option C. It cuts cost from about $60k to about $18k per quarter and turnaround from 3 weeks to 2 days for non-EU queries. It also keeps humans in the loop to catch the judge's main weakness, drift. The eval team and search infra agreed on this in the Oct 7 meeting.

## Options

We need about 6,000 query-result labels per quarter for the offline nDCG eval. Today the vendor's human raters label all of them.

| Option | Cost/quarter | Turnaround | Main risk |
|---|---|---|---|
| A. Human raters only (today) | ~$60k | 3 weeks | Slow, which blocks ranker iterations |
| B. LLM judge only | ~$4k | Same day | Drift; legal has not cleared EU query logs |
| C. LLM judge, 15% human calibration, humans for EU | ~$18k | 2 days (non-EU) | Needs monthly drift check |

**A is trusted but slow.** Raters also disagree on tail queries (agreement about 0.71, per Jamie).

**B is cheap and fast but not safe alone.** In last month's pilot on 1,200 labels, the judge agreed with the human majority label 82% of the time (Cohen's kappa 0.74). After a provider model update during the pilot, kappa fell to 0.61. Separately, legal has not approved sending query logs to the provider in all markets, and EU is the blocker.

**C addresses both B risks.** The judge labels everything outside the EU. Humans label every EU query, so EU data never goes to the provider. Humans also label a 15% calibration sample each month (about 900 labels). That sample measures drift directly.

## Is kappa 0.74 good enough?

The meeting's view was yes for comparing rankers, no for reporting absolute quality to leadership. This is a judgment from discussion, not a tested result. Under option C, ranker comparisons can use judge labels. Absolute quality numbers for leadership should not come from the judge alone.

## Risks and what we'd watch

- **Drift.** Each month we compute kappa between the judge and humans on the calibration sample. If it falls below 0.65, we use human labels for that month. The pilot's 0.61 would have triggered this. The 0.65 threshold was set in the meeting; it is not derived from data.
- **EU cost.** The $18k estimate comes from the meeting. The notes do not give the EU share of queries or how it enters the estimate, and human labels cost more than judge labels. A larger EU share raises cost and slows EU turnaround. Please ask for this breakdown before approving if the number matters to your decision.
- **Pilot size.** The 0.74 kappa comes from one pilot of 1,200 labels. The monthly calibration sample is the check on whether it holds.

## Out of scope

A fine-tuned in-house judge. The meeting deferred it past this quarter.
