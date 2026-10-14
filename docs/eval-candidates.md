# Eval candidates for the next round

These cases are for the round after the current acceptance run. The current bar (`docs/acceptance.md`) is frozen on f1–f8, so none of them changes it. Each case would become a synthetic SQLite fixture: the mechanism comes from the source, the data doesn't. Each would be calibrated on plain prompting only, and the ones that discriminate become holdout candidates, run once.

The cases came from a web search on 2026-10-14. The session's network allowed only microsoft.com and github.com, so arXiv, the ACM library, company engineering blogs and the DABStep, BIRD and Spider 2.0 pages weren't read. The main source is Dmitriev et al., ["A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls in Online Controlled Experiments"](https://www.microsoft.com/en-us/research/uploads/prod/2020/08/2017-08-KDDMetricInterpretationPitfalls.pdf) (KDD 2017; "DD" below), read in full. The miss risks are judgments, not measurements, except where a simulation is cited.

## Build first

| Case | Mechanism | Source | What it tests | Miss risk |
|---|---|---|---|---|
| Client vs. server clicks | Opening results in a new tab raises beacon delivery (97% vs. 88%), not clicks | DD 5.3; Microsoft, "Tracking Users' Clicks and Submits" (2010) | The `Reconciled:` line against a second log; Observed vs. Causal | High |
| Query-level test on a user-randomized test | Within-user correlation makes a pooled query-level interval too narrow | DD 5.2; Deng et al., delta method (KDD 2018) | Cluster-aware intervals, which ds-mode lacks today | Medium to high |
| Pre-period imbalance | The arms differ before launch, so the in-period gap isn't the effect | Microsoft ExP, "Patterns of Trustworthy Experimentation" | Observed vs. Adjusted vs. Causal | Medium to high |
| Metric-level sample ratio mismatch | Fast back-button page loads vanish in treatment, so mean latency rises | DD 5.1 | `srm` applied to a metric's denominator, not just to users | Medium to high |
| Bot filter keyed on engagement | Treatment pushes real heavy users into the "bot" bucket | DD 5.9 | `srm` after filtering; the estimand changes | Medium |

The query-level case has one measurement: an A/A simulation with 1,000 runs. A query-level z-test gave 45% false positives, against 3.9% with user-clustered intervals.

## Later, or only as variants

| Case | Mechanism | Note |
|---|---|---|
| Worse ranker, higher engagement | Reformulations inflate queries and clicks per session | Needs a session-success definition in the metric catalog |
| Feature CTR with a moved denominator | Impressions +200%, clicks +74%, CTR −40% | Partly duplicates the mix-shift fixture |
| Post-treatment segments | Treatment moves segment membership | Per-segment `srm` |
| Novelty effect | The lift decays within a week | Needs a new time-trend check |
| Zero-result rate by unit | Query-level and user-level rates disagree in sign | Partly duplicates the CTR definition trap |
| Regression to the mean | The worst queries are selected, then "fixed" | Tests abstention without a matched control |
| Slice fishing | 2 of 40 slices at p ≈ 0.03, and a failed replication | Tests abstention |
| Good abandonment | An answer card cuts CTR, not satisfaction | Easy if the card flag is labeled; Li and Tokuda (SIGIR 2009) read only as a snippet |
| Underpowered null, Simpson's paradox datasets | — | Likely easy for a strong model |

## What two of them would add to the skill

The client/server and query-level cases each need something ds-mode doesn't have:
- a reconciliation check that compares two logs of the same event;
- an interval that respects the randomization unit.

Build the fixtures first. Write the checks only if plain prompting misses the fixtures and the archive rule holds, meaning the mistake has happened twice in real work.

No harder variants of join fan-out, partly loaded days or backfill duplicates turned up in the sources that could be read.

## Second search (2026-10-13)

Every source below was opened and the cited passages checked. Gold values are design targets; miss risks are judgments.

### New cases

| Case | Mechanism | Source | What it tests | Miss risk |
|---|---|---|---|---|
| Triggered-population SRM | Control's slow page loses the batched "saw it" event for users who quit; assignment stays 50/50 | Fabijan et al., [Diagnosing SRM](https://exp-platform.com/Documents/2019_KDDFabijanGupchupFuptaOmhoverVermeerDmitriev.pdf) (KDD 2019) 5.4 | `srm` on the analysed population; intent-to-treat | High: joining impressions as "exposed users" is natural |
| Repairable SRM | A misconfigured campaign URL forces users into one arm; excluding them restores 50/50 | Fabijan 5.5 | Abstaining only when an SRM stays unexplained | Medium: f5 rewards blanket abstention |
| NULL means "all" | A rules table uses NULL as a wildcard; an equality join drops those rows silently | Egg et al., [DABStep](https://arxiv.org/abs/2506.23719) (Adyen, 2025) and its manual | Match rules; `fanout` sees only the drop | Medium to high: the count looks plausible |
| Early peek | p reached 0.05 on day 7 at +4%, then the test ended neutral; early bookers dominate at first | Overgoor, [Experiments at Airbnb](https://medium.com/airbnb-engineering/experiments-at-airbnb-e2db3abf39e7) (2014) | Answerability: planned runtime against data so far | Medium to high: p < 0.05 invites "ship" |
| Seven-hour contamination | One headline differed between arms for seven hours; the lift vanished without that window | Crook et al., [Seven Pitfalls](https://exp-platform.com/Documents/2009-ExPpitfalls.pdf) (KDD 2009) 9 | Ruling out a non-treatment difference by hour | Medium to high: needs an hourly split |
| Sentinel label | Label −1 means "page dead: drop and renumber"; clamping it to 0 shifts NDCG | Adapted from BIRD's value evidence, Li et al. ([NeurIPS 2023](https://arxiv.org/abs/2305.03111)) | Pinning a metric from a label guide | Medium: the model picks its own rule |

### How to build them

| Case | Fixture | Prompt | Gold |
|---|---|---|---|
| Triggered SRM | 20,000 users per arm, success 40% vs 41.5%; control's impression log keeps 96% of successes, 70% of failures | "What was the module's effect on the share of users with a successful search?" | Intent-to-treat +1.5 pp; triggered −6.3 pp is invalid |
| Repairable SRM | 20,000 organic users per arm, plus 1,600 campaign users in control at 5% success | "Estimate the new ranker's effect on successful-search rate." | +1.5 pp on organic users; naive +4.1 pp |
| NULL rule join | 40 boost rules, 14 with NULL locale, 9 with NULL platform; a notes row defines NULL | "How many logged queries had a boost rule applied?" | Match on NULL or equal: about 6,300; naive 3,900 |
| Early peek | Config plans 28 days; 7 loaded; median booking lag 5 days; true effect 0 | "Is treatment better on booking rate? Should we launch?" | Abstain: bookings immature; +4% is provisional |
| Seven-hour window | Hourly arm counts for 48 hours; CTR 4.0%, treatment 5.2% in hours 20–26 | "Did the treatment ranker lift CTR over the 48-hour test?" | Pooled +0.175 pp (z-test p ≈ 0.002), zero outside the window |
| Sentinel label | 2,000 judgments, 6% labelled −1, more near the top; a label-guide row | "What is mean NDCG@10 for the production ranker?" | Drop and renumber: about 0.93; clamped 0.89 |

Simulation, triggered case: 2,000 A/A runs of 40,000 users; control loses the event for 5% of its failures. `srm` on assignment counts flagged 0.1% of runs; the triggered comparison reached p < 0.05 in 48%; `srm` on triggered counts caught 58%.

### Duplicates and variants

- Duplicates: client vs. server clicks (Kohavi et al., [Five Puzzling Outcomes](https://exp-platform.com/Documents/puzzlingOutcomesInControlledExperiments.pdf), KDD 2012), query-level test (Deng et al., [delta method](https://arxiv.org/abs/1803.06336): naive SE 0.0052, true 0.0090), good abandonment (Li et al., SIGIR 2009), bot filter, worse ranker.
- Variants: ramp-up Simpson (f1), bucket carryover (pre-period imbalance), one robot in one arm (bot filter), click-conditioned metric (metric-level SRM), a flat interval over time (underpowered null), merged-document join key (f8), two cancellation pipelines (client vs. server).

Build first: triggered SRM, NULL rule join, repairable SRM. The first two pass the checks as written; the third catches a skill that over-learned f5.
