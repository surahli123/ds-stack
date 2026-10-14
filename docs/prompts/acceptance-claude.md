# Prompt: acceptance run, Claude's part

Goal: show that the ds-mode plugin works in Claude Code, Codex and Cursor, with the bar fixed in writing before any run. One green smoke run is not enough. You own the acceptance doc, the new fixtures and the Claude column. dots runs the Codex and Cursor columns on the owner's machine from `docs/prompts/acceptance-dots.md`.

## Phase A: before any acceptance run

1. Write `docs/acceptance.md` and get it merged to main before anyone runs the matrix. It defines "works" per harness (`claude -p`; `codex exec` and `cursor-agent -p` via `eval/agents/*.sh`). Every number in it is fixed from then on, and changing one restarts the count.

| Level | Passes when |
|---|---|
| Plumbing | In every full-arm run, at least one query is logged, every completed check names its source query, and `verify_readout.py` passes |
| Correctness | The full arm is right by majority of 3 runs on every fixture, scored by `eval/grade.py` (details below the table) |
| Language | The same correctness with `--prompt-suffix "请用中文写结论。"`. Prose may be Chinese; the fixed words stay English |
| Value | On the new fixtures, plain prompting misses at least 30% of runs, and the full arm is right on more of them |
| Review | A data scientist who didn't build ds-stack checks one full-arm readout in under 10 minutes, using only the readout, its two logs and `skills/ds-mode/references/review-checklist.md` |

"Right" under Correctness covers four things:
- the estimand gold names is within tolerance;
- no false alarm on the clean control;
- no number on an abstain case;
- no number on `Causal effect:` where gold says the cause can't be identified.

2. Add three build fixtures to `eval/make_fixtures.py`, each with a gold file that never reaches an agent:
   - f6, a metric-definition trap: the obvious definition gives a different number from the one in `metrics.json`. Set `DS_OVERLAY_DIR` for that fixture so the definition is available.
   - f7, an unanswerable question: the right answer is `can't tell`, with a stated reason.
   - f8, a many-to-many join that inflates a rate.
   Calibrate difficulty on plain prompting only. Stop changing the fixtures once the acceptance run starts.
3. Run `make test` and open a PR. Once it merges, tell the owner that dots can start.

## Phase B: the Claude column

4. Run `eval/run_arms.py --runs 3` with all three arms, once in English and once with the Chinese suffix. Each run gets a new results directory under `eval/results/`.
5. Grade with `eval/grade.py`. Diagnose every failing run from raw evidence: its `transcript.jsonl`, `queries.log`, `checks.log`, and the SKILL.md copy the agent saw. Don't diagnose from one-line summaries.
6. For each failure, find the first point where the agent left the skill. Classify it as harness or plumbing, skill-text ambiguity, grader parsing, fixture flaw, or model error. Fix only that layer, and add a regression test built from the failing artifact. A fix to the skill, grader or fixtures restarts the matrix in new directories, so tell the owner that dots must rerun too.
7. Prove the eval has teeth. On a scratch branch, remove the three-estimate-lines rule from SKILL.md and run the full arm on f1, f3 and f6. Confirm that grading catches it, then delete the branch. Record the result.
8. When dots pushes its `results/<date>-<harness>` branches, merge them and fill in the acceptance table.

## Constraints

- Synthetic data only. No company data, and no running SMA.
- Never overwrite a results or report directory. That includes `docs/reports/2026-10-14-local-f1-smoke` on branch `docs/local-f1-smoke-20261014`.
- Gold stays out of every analysis agent's reach. Only `grade.py` and `smoke_check.py` load it, after the agent has finished.
- Never write 0 for an unidentified causal effect to pass a fixture, and never change a gold value after seeing results.

## Report

- The acceptance table filled in for each harness and language.
- Failure counts by category.
- What was fixed in each layer, with commits.
- The teeth-test result.
- What still fails, and what remains unverified.
