# Decision memo: Relevance labeling for the offline eval

**To:** Morgan, Eval Lead
**Decision needed by:** Oct 20, 2026
**Why that date:** The vendor renewal has to be cancelled before Oct 31.

## Decision requested

Approve or reject **Option C (hybrid)**. Under it, an LLM judge labels everything, and humans label a monthly calibration sample plus all EU queries. The budget is about **$18k per quarter**, down from about $60k.

We recommend approval.

## Background

The offline NDCG eval needs about 6,000 query-result labels per quarter. Human raters through the vendor do all of them today. That costs about $60k per quarter and takes 3 weeks to turn around, which blocks ranker iterations.

## Options

| | A: Humans only | B: LLM judge only | C: Hybrid (recommended) |
|---|---|---|---|
| Cost per quarter | ~$60k | ~$4k | ~$18k |
| Turnaround | 3 weeks | Same day | 2 days (non-EU) |
| Main weakness | Slow and expensive. Raters agree only ~0.71 on tail queries. | The judge drifts when the model version changes. Legal hasn't approved sending EU query logs to the provider. | Needs ongoing calibration work and a fallback process. |

**Option A, humans only.** This is the trusted baseline.

**Option B, LLM judge only.** In a 1,200-label pilot, the judge agreed with the human majority label 82% of the time (Cohen's kappa 0.74). Kappa fell to 0.61 after a provider model update. Legal has not approved EU data, so B cannot cover all markets.

**Option C, hybrid.** The judge labels everything. Humans label a 15% calibration sample to measure drift, and humans label all EU queries. That removes the EU blocker and gives us a drift check.

## Rationale

- **Cost:** C saves about $42k per quarter against A.
- **Speed:** C cuts turnaround from 3 weeks to 2 days for non-EU queries, so ranker iteration is no longer gated on labels.
- **Quality:** The meeting's view was that kappa 0.74 is good enough for comparing rankers. It is not good enough for reporting absolute quality to leadership. Absolute numbers should keep a human-labeled basis.
- **Risk:** Drift is a real risk, since the pilot showed it. C is the only low-cost option that measures it.

## Risk and mitigation

- **Drift:** If monthly kappa on the calibration sample falls below **0.65**, we fall back to human labels for that month.
- **EU:** Humans label all EU queries until legal approves sending that data to the provider.

## Out of scope

A fine-tuned in-house judge is deferred and out of scope this quarter.

## Open items to confirm

- **Calibration sample size:** The notes say the 15% sample is "monthly (~900 labels)". But 15% of 6,000 quarterly labels is about 900 per quarter, or about 300 per month. This should be reconciled before the $18k estimate is final.
- **EU volume:** The EU share of queries is not stated in the notes. It drives how much of the $18k is human labeling.
- **Pilot size:** The kappa figures come from a single 1,200-label pilot.

## Next steps if approved

1. Morgan signs off on the budget by Oct 20.
2. Cancel the vendor renewal before Oct 31. Keep enough vendor capacity for the calibration sample and EU labels.
3. Set up the monthly calibration sample and the kappa < 0.65 fallback check.
