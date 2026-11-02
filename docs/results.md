# Results and reviews

What the evals, the real-case review and the research found, with numbers. The README keeps a summary.

## Acceptance: Claude Code and Codex (2026-10-14, 2026-11-02)

Claude ran its matrix in a cloud session on 2026-10-14 (Sonnet). dots ran the Codex matrix on the owner's machine on 2026-11-02: Codex 0.166.0, the owner's daily model at medium effort, commit b197e90. All 144 Codex runs executed on the first attempt, and the isolation probe passed.

| Level | Claude, en | Claude, zh | Codex, en | Codex, zh |
|---|---|---|---|---|
| Plumbing | PASS, 24 of 24 | PASS, 24 of 24 | PASS, 24 of 24 | PASS, 24 of 24 |
| Correctness | PASS, 8 of 8 | PASS, 8 of 8 | FAIL, 7 of 8 (f1) | FAIL, 6 of 8 (f1, f3) |
| Value | PASS, plain missed 67% | PASS, plain missed 89% | FAIL, plain missed 22% | FAIL, plain missed 11% |

Why Codex failed:

- **f1 in English.** All 3 full runs had the right number (Adjusted −0.002 pp), but each called the ranker "ruled in as an unresolved possibility". The grader reads "ruled in" as shown, so it counted a false cause. ds-mode offered only two verdicts, and Codex wrote "ruled in" for an open alternative in at least 31 of its 48 full-arm readouts.
- **f1 and f3 in Chinese, and f3 run 1 in English.** These 7 readouts headlined `can't tell` although Adjusted was computed: Codex abstained because the cause wasn't identified. ds-mode already said that is no reason to abstain.
- **Value.** Plain Codex already gets f7 and f8 right, and only f6, the team's metric definition, separates the arms. The bar counts plain prompting's misses, so these fixtures can't show Codex's gain; changing them would restart the count.

0.7.0 adds the verdict `not ruled out` and a ds-verify rule for the abstentions. A new Codex run will measure them.

### ds-verify's held-out test

The rule was pre-registered on 2026-11-01 (`eval/README.md`). ds-verify as of b197e90 ran on the 48 Codex full-arm runs:

- It failed 9 of the 10 wrong runs. The bar was 2 of 3.
- It failed 22 of the 38 right runs, all on `alternatives`. Read by hand, each is a "ruled in" that means "not excluded", which is a real fault in the readout under the rule. 7 right runs were unverified and 9 passed.
- 7 of the 10 wrong runs were abstentions, and ds-verify had no rule for them: it failed 6 only for their wording. With 0.7.0's rule, 4 of the 7 also fail on `estimand`. That number is in-sample. The rule adds no failure to the Claude acceptance runs.

### ds-verify as ds-mode's last step (0.8.0, smoke test)

Claude (Sonnet) ran 5 full-arm runs with ds-verify wired in: f1, f3 and f6 in English, and f1 and f3 in Chinese. These are the cases Codex missed. All 5 were graded right with clean isolation, at about $0.75 in total. In every run the agent ran ds-verify, ended at `ds-verify: pass` and put that line in Provenance. Two runs first failed on an untagged "100%" and fixed it. Every open alternative read `not ruled out`. This is a smoke test, not acceptance: the Codex rerun is the test that counts. Results: `eval/results/2026-11-02-wiring-smoke-{en,zh}/`.

### ds-interrogate smoke test

A Codex reviewer checked a Claude f1 readout twice, once with a planted error:

- The planted error, a post-rollout mobile share of 45.1% where the data gives 55.1%, was found and proved by a replayed query.
- Both runs also found two faults in the unchanged readout that the grader and ds-verify had passed. It says the change is −0.00 pp in all four cells; they range from −0.08 to +0.05 pp. It also uses the ±0.15 pp interval as a bound on v2's effect to reject a rollback, although ranker and week are fully confounded.
- The report labelled the reviewer `gpt:-`, and the findings on the English readout came back in Chinese, from the owner's Codex settings. ds-interrogate now records the model the CLI ran, and the brief asks for the readout's language.

dots' first push failed, because that shell had no git credentials ("could not read Username"; `gh` returned 401). The branches were pushed later, so the "NOT PUSHED" lines in the reports are out of date.

Results: `eval/results/2026-11-02-0911-codex-{en,zh,report}/`, `eval/results/2026-11-02-interrogate-codex/`.

## Estimand and localization fixes (2026-10-14)

A local Codex smoke run failed (report on branch `docs/local-f1-smoke-20261014`): its Chinese readout headlined the observed −2.10 pp total, and the grader read the "95" of "95% CI" as the estimate. Two root causes:

- **Ambiguous skill text.** "Headline the measured change" let Claude headline the within-segment change and Codex the total.
- **An English-only grader.** It didn't handle 个百分点, full-width brackets or 至, took a number in the wrong unit, and silently dropped translated alternatives.

What changed:

- The readout now separates `Observed`, `Adjusted` (descriptive, saying what it holds fixed) and `Causal effect` (a number only from an identifying design).
- Gold names the estimand it scores.
- The parser normalizes Chinese and full-width input, ignores confidence levels, never takes a number in another unit, and fails loudly on translated fixed words or a headline with two estimates.

| Metric | Plain prompting | Checks only | Full ds-mode |
|---|---|---|---|
| Cases right (majority of 3) | 4 of 5 | 3 of 5 | 5 of 5 |
| Runs right | 12 of 15 | 9 of 15 | 15 of 15 |
| Readouts passing `verify_readout.py` | n/a | n/a | 15 of 15 |
| Cost | $1.02 | $1.18 | $2.24 |

- The gap is mostly the new readout format, not better analysis. The three estimate lines, shown to every setup, lead the setups without ds-mode's rule to answer "can't tell" on the two full-rollout cases (f1, f3). ds-mode's rule that an unidentified cause is no reason to abstain prevents that. Read it as the rule being necessary under this format, not as a measured gain.
- A Claude run of f1 asked to write in Chinese passed `smoke_check.py`. Its prose was Chinese, its fixed words English, and its three estimate lines were kept apart.
- Regrading all 180 committed readouts flags two copies of one old baseline headline that gave two estimates. Results from Codex and Cursor are still to come from the owner's machine.

Results: `eval/results/2026-10-14-estimand/`.

## Seed eval (2026-10-13, `v0.3` seed)

Before the estimate lines existed, runs right were 15 of 15 with plain prompting, 13 of 15 with checks only and 15 of 15 with full ds-mode; all 15 full readouts passed `verify_readout.py` (`eval/results/2026-10-13-seed/`). Its first run found three problems, fixed before that result: a clean control with byte-identical weeks (the generator now adds noise), agents searching the filesystem for `metrics.json` (ds-mode now reads only `$DS_OVERLAY_DIR`), and the full arm abstaining on f3.

## Evals

Both evals use synthetic tasks, 3 runs per setup, Sonnet as the agent, and clean profiles. Both report `INSUFFICIENT_N`, because the pre-registered rules need more tasks before they give a verdict.

**Analysis eval** (5 cases; `eval/results/`). Plain prompting got all 5 cases right, and so did the checks-only and full setups after a fix. Round 1 found a real bug: the skill told the agent to abstain whenever a check couldn't run, so it withheld a correct answer on a case with only one week of data. The rule now separates a failed check, a check called wrongly, and data that can't support a check.

**Writing eval** (3 tasks: a readout, a memo, a handover; `eval/writing/results/`).

| Metric | Plain prompting | ds-doc |
|---|---|---|
| Fresh reader, skim (answer, decision, number) | 0.96 | 0.89 |
| Fresh reader, full read (all takeaways) | 0.89 | 0.94 |
| Docs with no lint fail | 2 of 9 | 9 of 9 |
| Mean words | 423 | 356 |
| Cost per run | $0.055 | $0.080 |

- The skills fix format and length. Plain prompting failed the lint on 7 of 9 docs, mostly on bold and bold-label bullets. The ds-doc docs are 16% shorter.
- No comprehension gain is shown. Readers already understood the plain docs. The one skim gap is a grading artifact: the reader prompt asked a handover for its conclusion rather than its current state. That prompt is now fixed.

What the evals show: short tasks written from clean notes are too easy, both for analysis and for writing. The corpus failures came from long, multi-session docs written mid-work.

## Real-case review (2026-10-10)

An independent reviewer ran the skills on 10 real notes docs and on two public Simpson's-paradox datasets (Berkeley admissions, kidney stones), disguised so the agent couldn't recall the answer.

| Finding | Change made |
|---|---|
| ds-mode got 6 of 6 answers right but reported an interval in 0 of 3 runs; plain prompting did in 2 of 3 | The readout requires an interval, or `(no interval: <reason>)`; `mix_shift` reports a 95% CI for the overall and within-segment change |
| `mix_shift` fired on 12-27% of cases with no real change | A noise floor of 2 standard errors; 0 of the null cases fire now |
| `mix_shift` called a real Simpson's paradox a `fail`, so agents had to explain it wasn't a data defect | New status `flag`: a finding the answer must report |
| Per-segment mix effects were uninterpretable (+47 and -37 pp on a +4.6 pp total) | Deviation form: each segment's mix term now reads on its own |
| `completeness` failed a normal Saturday and passed an 85% load | Same-weekday baseline; default threshold 90% |
| `fanout` missed duplicate keys cancelled by dropped rows | Optional `matched_left_rows` catches it |
| ds-doc rewrites: 36% shorter, lint-clean on 7 of 10 (plain prompting 0 of 10); spine written and cold read run in 0 of 5 | `spine.json` comes before the draft; `cold_read.py` grades the reader by script |
| Lint precision on 24 hand-checked findings was 0.67 | Nine false-positive patterns and five misses fixed; about 0.88 on the same set, which is optimistic because the fixes were tuned on it |

A re-run of the three ds-mode cases after the fixes: all 3 correct, all 3 with a 95% interval and `mix_shift` as `flag`, and each ended with provenance labelling the metric `[guess]`, as no `metrics.json` was given.

Fresh readers understood originals and rewrites alike: ds-doc made docs shorter and cleaner without losing the answer, with no comprehension gain. Rewrites did drop facts the next reader needs: a status line saying the plan was already executed, and a handover's list of attacks already tried. The doc types now keep both.

## What the research changed

A review of data-agent benchmarks, vendor guidance and practitioner write-ups (October 2026) found three levers, in order of measured effect:

1. Curated, data-verified metric definitions (+26 to +36 points on hard DABStep tasks).
2. Execute-and-verify loops with independent review (+2 to +6 points on SQL benchmarks).
3. An explicit right to abstain, which no mainstream benchmark scores.

The skills now act on all three:

- ds-mode pins the metric from the overlay's `metrics.json` before querying, and labels any definition it had to state itself `[guess]`. It asks when a question has two readings that give different numbers.
- The readout carries a provenance section, and allows "caused" only for a randomized test or another design that identifies the cause.
- `metrics.json` entries now carry `grain`, `source`, `verified` and `pitfalls`, and are written by a person, never drafted by an agent.

Still open:

- an independent reviewer before the readout is sent (a human checklist now exists; no automated reviewer)
- answerability cases in the eval, scored +1 right, 0 abstain, minus a penalty wrong
- an eval with real past errors that crosses definitions in context with checks on and off
