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
