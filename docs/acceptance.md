# Acceptance: when ds-mode counts as working

**Fixed 2026-10-14, before the first acceptance run.** Changing any threshold, fixture or gold value restarts the count, and the old results stay as they are. `eval/acceptance.py` computes every level except Review from the results directories, so the verdict comes from scripts rather than from the agent or its author.

## What is run

Each harness runs `eval/run_arms.py --runs 3` over fixtures f1–f8 and all three arms: plain prompting, checks only, and full ds-mode. It runs once in English and once with `--prompt-suffix "请用中文写结论。"`, and each run writes to a new directory under `eval/results/`.

| Harness | Command | Run by |
|---|---|---|
| Claude Code | `claude -p` (default), Sonnet | Claude, in a cloud session |
| Codex | `--agent-cmd "sh $PWD/eval/agents/codex.sh {prompt_file}"` | dots, on the owner's machine |
| Cursor | `--agent-cmd "sh $PWD/eval/agents/cursor.sh {prompt_file}"`, if installed | dots |

Gold answers stay out of every analysis agent's reach. On the owner's machine, `eval/gold` is moved away while the agents run.

## Fixtures

| Fixture | What it tests | Right answer |
|---|---|---|
| f1 | Mix shift behind a drop after a 100% rollout | `Adjusted:` about 0 pp, causal effect not identified |
| f2 | A join that keeps stale labels | 54.98% |
| f3 | Clean control: a real within-segment drop | `Adjusted:` about −1.83 pp, causal effect not identified |
| f4 | A partly loaded day | `can't tell`, or the like-for-like change |
| f5 | Sample ratio mismatch in an experiment | `can't tell` |
| f6 | The team's CTR definition differs from the obvious one | 50.05% |
| f7 | Purchases aren't logged; "conversions" are add-to-cart events | `can't tell` |
| f8 | A backfill duplicated rows in the category table | 36.97% |

f6 and f7 come with the team's metric catalog, a `metrics.json` that sits outside the analysis directory and is named only by `$DS_OVERLAY_DIR`. Every arm gets it. This mirrors work, where the metric layer is in the environment but a plain agent isn't told to use it.

## Levels

Each level is judged per harness and per language.

| Level | Passes when |
|---|---|
| Plumbing | 100% of full-arm runs log a query, source every completed check, and pass `verify_readout.py` |
| Correctness | The full arm is right on all 8 fixtures by majority (2 of 3 runs), as graded by `eval/grade.py` |
| Language | Plumbing and Correctness both pass in the Chinese run |
| Value | Plain prompting misses at least 30% of its 9 runs on f6–f8, and the full arm gets more of them right |
| Review | A data scientist who didn't build ds-stack checks one full-arm readout in under 10 minutes |

For Review, the readout is f6, run 1, from the Claude English run. The reviewer uses only the readout, its two logs and `skills/ds-mode/references/review-checklist.md`, and records the minutes taken and any failed checklist items in `docs/reports/<date>-review/`.

ds-mode works when every level passes in every harness that ran, in both languages. A harness that couldn't run is reported as not run, not as passed.

## What doesn't count

- One green run, or an agent's own report of success.
- Rerunning a failed run into the same directory.
- A gold value or fixture changed after its results were seen.
- A 0 written for a causal effect that wasn't identified.

## Calibration, done before this file was fixed

Difficulty was tuned on plain prompting only:

| Fixture | Plain prompting | What happened |
|---|---|---|
| f6 | 0 of 3 right | Every run used the obvious definition and answered about 46% |
| f7 | 0 of 3 right | All 3 runs reported add-to-cart as an 8.3% purchase rate |
| f8 | 3 of 3 right | Plain prompting compares `count(*)` with `count(distinct query_id)` unprompted |

The first version of f7 kept a notes table saying purchases aren't logged, and plain prompting got it 3 of 3; the fact now lives in the metric catalog. f8 failed to discriminate in both its versions, multi-label categories and then backfilled duplicates. It is kept as a regression guard: for this model, a join that duplicates rows is not a hard case, and the result says so. Pooled across f6–f8, plain prompting missed 6 of 9 runs.

The results are in `eval/results/2026-10-14-calibration-baseline/` and `-2/`. The first directory graded the first version of f7 and f8, which has since been replaced.
