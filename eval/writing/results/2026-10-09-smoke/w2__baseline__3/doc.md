# Decision memo: relevance labeling for the offline eval

**To:** Morgan (Eval Lead)
**Date:** 2026-10-09
**Decision needed by:** Oct 20, so we can cancel the vendor renewal before Oct 31

## Decision requested

Approve or reject **Option C (hybrid labeling) at about $18k/quarter**. The eval team and search infra agreed on Oct 7 to recommend it.

Approval means:
- We cancel the vendor renewal.
- We spend about $18k/quarter instead of about $60k, a saving of about $42k/quarter.

## Background

The offline NDCG eval needs about 6,000 query-result labels per quarter. Human raters at the vendor produce all of them today. That costs about $60k/quarter and takes 3 weeks, which blocks ranker iterations.

## Options

| | A: Humans only | B: LLM judge only | C: Hybrid (recommended) |
|---|---|---|---|
| Cost/quarter | ~$60k | ~$4k | ~$18k |
| Turnaround | 3 weeks | Same day | 2 days (non-EU) |
| Quality | Rater agreement ~0.71 on tail queries | Agreement with human majority 0.82, kappa 0.74 (1,200-label pilot) | Same judge, with monthly drift checks |
| Main problem | Slow and expensive | Drift, plus EU legal block | More moving parts |

**A: Keep human raters.** Trusted, but slow and expensive. Raters also disagree often on tail queries (agreement ~0.71).

**B: LLM judge only.** Cheapest and fastest, but we rejected it for two reasons:
- **Drift:** in the pilot, kappa fell from 0.74 to 0.61 after a provider model update. Nothing would catch that.
- **EU data:** Legal has not approved sending query logs to the provider for all markets. EU is the blocker.

**C: Hybrid.**
- The LLM judge labels everything outside the EU.
- Humans label a 15% calibration sample every month, about 900 labels, to measure drift.
- Humans label all EU queries.

## Why C

- It cuts cost by about 70% and turnaround from 3 weeks to 2 days.
- The monthly calibration sample catches the drift that sank Option B.
- Humans keep the EU queries, so we don't depend on a Legal approval that hasn't happened.

## Limits of the judge

Kappa of 0.74 is good enough for **comparing rankers**. It is **not** good enough for reporting absolute quality numbers to leadership. Those numbers should keep coming from human labels or be clearly caveated.

## Risks and mitigation

- **Drift:** if monthly kappa on the calibration sample drops below **0.65**, we fall back to human labels for that month. The pilot's 0.61 would have triggered this.
- **Cost estimate:** $18k is an estimate. It depends on the share of EU traffic, which the notes don't give.
- **Legal:** if EU approval comes later, the EU share could move to the judge and lower the cost. No timeline exists.

## Out of scope

A fine-tuned in-house judge was considered and deferred. It is not part of this quarter's plan.

## Open items to confirm

- The calibration sample is described as 15% and also as about 900 labels per month. 15% of 6,000 quarterly labels is 900 per quarter, or about 300 per month. The size needs confirming, and the $18k estimate depends on it.
- The pilot covered 1,200 labels. It is not known whether it included EU queries or tail queries.

## Recommendation

Approve Option C at about $18k/quarter, and approve cancelling the vendor renewal by Oct 20.
