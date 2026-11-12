## Answer
Headline: can't tell [inferred]
Recorded CTR rose from 30.00% to 31.20%, a +1.20 percentage-point difference [measured], but a causal improvement is not established [inferred].
- Observed: +1.200 percentage points (nominal 95% interval: +1.125 to +1.275) [measured; interval inferred]
- Adjusted: +1.200 percentage points (nominal 95% interval: +1.125 to +1.275), holding the pooled date distribution fixed [measured; interval inferred]
- Causal effect: not identified (validated random assignment, assignment-level outcomes, and resolution of the allocation imbalance would identify it) [inferred]

## What it means for the launch decision
The smallest decision-changing improvement was not supplied [measured]; if it is zero [guess], the nominal interval lies entirely above it [measured]. Launch based on causal CTR improvement is not supported until the allocation imbalance is explained [inferred].

## Why we believe it
- Alternatives considered:
  - Calendar composition explains the lift: ruled out as a material explanation by the unchanged date-adjusted estimate [measured].
  - Allocation or reporting bias: ruled in as unresolved because treatment has fewer recorded users every day [inferred].
- Checks run:
  - Coverage: pass—all 14 dates have both arms, with no duplicate date/experiment/arm rows [measured].
  - Count validity: pass—counts are present, positive denominators, and clicks never exceed searches [measured].
  - 50/50 allocation: flag—first-day treatment share is 48.773%; assuming unique randomized users, χ²=41.96, p=9.32×10⁻¹¹ [measured; interpretation inferred].
  - User clustering and assignment integrity: could not run—only daily aggregates are available [measured].

## Caveats, and what would change the answer
- Intervals assume independent Bernoulli searches; repeated searches/users could change uncertainty [inferred].
- Daily `users` may represent activity rather than assignments; the imbalance’s cause cannot be determined here [inferred].
- Assignment logs, user-level outcomes, a confirmed CTR definition, and the launch threshold would enable a stronger decision [inferred].

## Provenance
- Metric: total clicks / total searches, from stated here [guess]; no metrics.json found [measured].
- Data: `experiment_daily`, through 2026-09-30; date coverage is complete, ingestion completeness unverified [measured].
- Reconciled: not done (no dashboard or independent source supplied) [measured].
- Queries and checks: [analysis.py](/private/tmp/ds-runs/e8cd9f34b1/analysis/analysis.py), with outputs in [analysis_results.json](/private/tmp/ds-runs/e8cd9f34b1/analysis/analysis_results.json) [measured].
