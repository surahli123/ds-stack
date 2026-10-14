# Eval

Two evals ask whether ds-stack changes what an agent produces, compared with plain prompting. Scripts do the grading, so no model judges a number. Both run on synthetic tasks and report `INSUFFICIENT_N` until the pre-registered task counts are met. Results so far are in the top-level README.

## Analysis eval

| File | Role |
|---|---|
| `make_fixtures.py` | Builds the synthetic warehouses in `fixtures/` and the answers in `gold/`, deterministically |
| `run_arms.py` | Runs each fixture through three arms (baseline, checks, full) in a clean profile, 3 runs each. Gold is never copied in |
| `readout.py` | Parses a readout into fields a script can grade |
| `grade.py` | Grades a results directory against gold, applies `pass_rule.json`, writes `summary.md` and `summary.json` |

Fixtures come in three kinds: error (a planted problem), clean (nothing wrong, so any alarm is a false alarm) and abstain (the right answer is "can't tell").

`grade.py` checks the estimand the gold names against its value and tolerance: the headline by default, or the readout's `Adjusted:` line when gold sets `"estimand": "adjusted"`. With `"causal_identified": false`, a number on the `Causal effect:` line fails. It also checks whether the run abstained, and which alternatives it ruled in. Whether checks ran comes from each run's `.ds-checks.log`, not from the readout. Each fixture is scored by majority vote over its runs, never per run. A run that touched the eval tree is marked contaminated.

The pass rule: at least 15 holdout fixtures, 3 runs each. The full arm beats baseline by at least 4 fixtures, adds no false alarms over baseline, and answers no abstain case with a number. With fewer fixtures the verdict is `INSUFFICIENT_N`.

## Writing eval

`writing/` compares baseline with the ds-doc skills on documents written from raw notes (a readout, a memo, a handover). `run_writing.py` produces the docs. `grade_writing.py` has a fresh reader answer questions from a skim view and from the whole doc, graded by script against gold facts. Lint fails and word counts are reported but secondary. `writing/pass_rule.json` needs at least 10 tasks, 3 runs each, a skim margin of 0.2, a full-read margin of 0.0 and no lint fails in the full arm.

## Running it

```bash
make eval                                    # three arms x all fixtures x 3 runs
make grade RUN=eval/results/<dir>
make writing-eval
make writing-grade RUN=eval/writing/results/<dir>
```

`run_arms.py` and `cold_read.py` call an agent CLI. The agent command is configurable; see `--help`. The writing-eval scripts also call an agent CLI.

## Lessons carried from earlier eval work

An earlier project scored prose documents with model judges. That is a different setting from scripted grading, so read its numbers as the size of the noise, not as targets. The lessons apply to anything model-graded here, such as the cold-read reader, and to any score compared across runs.

| Lesson | Why |
|---|---|
| Average at least 3 runs per scored comparison | Single runs swung about 1 point on a 10-point scale; three-run averages had stdev 0.16 to 0.36 |
| Compare against an averaged baseline | One low baseline made a +1.67 gain look real. The true gain was about +0.25; the rest was regression to the mean |
| Judge with a different model family than the one that wrote | A model scoring its own output is unreliable |
| Pin one judge model across runs, and never compare scores across judge models | One judge scored systematically higher than another on the same text |
| Use binary checkpoints only for objectively verifiable items | "Are intervals reported?" had stdev 0.0. Subjective yes/no questions, such as "do the conclusions follow from the evidence?", had stdev above 1.0 |
| At a plateau, stop and hand back to a person | A loop can't add substance that isn't there. It halted after three straight non-improvements |

The earlier loop also counted a change only if it beat noise by 0.3 points, and treated a stdev above 0.5 as too noisy to use.

Here the default reader model is from the same family as the default agent. Treat reader scores as a screen, and point the agent command at another family for an independent read.

## Rules specific to ds-stack

- Pre-register the pass rule before a run (`pass_rule.json`). Change it only before a new run, never after seeing results.
- Tune on a build split. Touch the holdout once.
- Keep clean controls and abstain cases. The pass rule allows no more false alarms than baseline and no abstain case answered with a number.
- Calibrate the baseline miss rate to 30-40% on the build split. Plain prompting got all 5 current cases right, so those cases cannot show a gain. Make cases harder until baseline misses about a third of them.
