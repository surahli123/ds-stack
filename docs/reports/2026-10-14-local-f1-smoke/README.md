# Local f1 smoke test: failed grading, preserved evidence

Run: 2026-10-14 UTC. Base: `b38292483163a55706fbefc5cfad6be06225e08c`, local branch `main`. Codex 0.153.4, Python 3.14.4. All eleven safety self-tests passed. Codex exited 0 and generated the readout; smoke_check exited 1 with four passing checks and `answer vs gold: headline 95 outside 0±0.3`. This is an evidence-only report; nothing in implementation or original artifacts was fixed.

## Evidence map

- [Original saved readout](readout.original.md): byte-identical artifact graded.
- [Queries](queries.jsonl), [checks](checks.jsonl): byte-identical complete retained logs, including failed check attempt.
- [Task](task.original.md), [run instructions](AGENTS.redacted.txt).
- [Public command trace](codex-public-trace.redacted.txt), [trace limits](TRACE-NOTES.md), [outer execution ledger](EXECUTION-LEDGER.md).
- [Original smoke output, transcribed](smoke-output.transcribed.txt), [self-test output, transcribed](selftest-output.transcribed.txt).
- [Read-only parser diagnostic](parser-diagnostic.json), [versions and hashes](provenance.json).
- [Reviewer handoff](HANDOFF.md).

## Verified diagnostic

At the base commit, `eval/readout.py`'s UNIT expression supports English pp/percentage points/points and percent, but not `个百分点`. `_candidates` splits only on ASCII `(`; the saved headline uses full-width `（` and `）`. It prioritizes unit-bearing candidates over unitless ones. Consequently the explicit `95%` confidence level comes before the actual −2.0968 estimate. `value_in('pp')` finds no pp candidate and falls back to the first candidate, 95. The diagnostic confirms candidates `(95, percent)`, `(−2.0968, null)`, `(−2.248, null)`, `(−1.946, null)`, a null interval, and no reported parse errors. This reproduces the parser behavior only; grading was not rerun.

Localization affects more than the headline: INTERVAL expects ASCII parentheses and English/punctuation separators, not `至`. VERDICT matches English `ruled in/out`; all five Chinese alternatives are dropped. The saved `mix_shift（粗粒度复核）` label is not independently parsed as another check. Actual check logs preserve both successful decompositions. English-only abstention words are another contract risk requiring tests, not an observed abstention in this run.

A parser fix alone does not resolve the failure. `eval/fixtures/f1/task.md` asks how much of the change is attributable to v2. `skills/ds-mode/SKILL.md:91` explicitly says a full rollout without holdout should headline the measured change and must not abstain solely because causation cannot be identified. Line 90 restricts causal language. The readout follows that guidance by headlining the measured total and saying attribution is unidentifiable. Original checker output exposes an accepted numeric target `0±0.3`; that target's intended estimand cannot be established from this output alone. No hidden gold was inspected. If only the parser were corrected to select −2.0968, that measured total would still be outside the displayed tolerance around zero. This is an inference from existing evidence, not a rerun result. Owners must align task, skill, answer fields and grader; do not silently relabel an adjusted descriptive residual as causal impact.

## What the retained analysis actually says

| Quantity | Fine platform × country decomposition | Interpretation |
|---|---:|---|
| Overall CTR before / after | 30.4212% / 28.3243% | Observed aggregate rates |
| Total change | −2.0968 pp; interval [−2.248, −1.946] | Observed before/after difference |
| Mix component | −2.0945 pp; share 0.9989 | Descriptive contribution of composition |
| Within-segment component | −0.0023 pp; interval [−0.153, +0.148] | Adjusted descriptive rate component |
| v2 causal effect | Not identified | Full rollout coincides with time; no simultaneous holdout |

The platform-only check agrees qualitatively: mix −2.0932 pp; within-segment −0.0036 pp, interval [−0.154, +0.147]. Intervals assume independent search units. Neither interval is a confidence interval for the causal effect of v2. The readout explicitly rejects treating the residual or zero as that effect and notes that the version could itself affect composition.

Two completeness checks passed, fine and corrected coarse mix_shift checks flagged a mix-dominant change, and a malformed coarse spec was retained as could_not_run before correction. Thus smoke reports four sourced checks out of five. fanout and srm were skipped with explanations (no joins, no randomized assignment). Five logged queries ran; verify_readout passed with 36 numbers on 8 lines, 4 referenced queries and 4 referenced checks. That verifies trace tags, not substantive correctness or parser/estimand agreement. The missing ds-doc reference is a separate installation contract gap.

## Delivery scope

This directory is intended for a local documentation-only commit. No implementation changes, gold inspection, grading/analysis reruns or external messages. After packaging, the user explicitly authorized pushing only this documentation/evidence commit to the existing ds-stack GitHub remote. The resulting commit hash and publication status are reported by the executor after committing; the commit cannot embed its own hash. The executor will verify the remote branch against the exact commit after the authorized push; final delivery links are provided outside this immutable commit.
