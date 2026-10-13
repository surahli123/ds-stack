# Results and reviews

What the evals, the real-case review and the research found, with numbers. The README keeps a summary.

## Seed eval (2026-10-13, `v0.3` seed)

The `v0.3` seed (traceable readouts) gets every analysis case right, and every full-arm readout passes `verify_readout.py`. The cases are still too easy to show a gain over plain prompting, so the verdict is `INSUFFICIENT_N`. Results: `eval/results/2026-10-13-seed/`. The setup is as before: Sonnet, 3 runs per setup, clean profiles.

| Metric | Plain prompting | Checks only | Full ds-mode |
|---|---|---|---|
| Cases right (majority of 3) | 5 of 5 | 4 of 5 | 5 of 5 |
| Runs right | 15 of 15 | 13 of 15 | 15 of 15 |
| Readouts passing `verify_readout.py` | n/a | n/a | 15 of 15 |
| Cost | $0.97 | $1.15 | $2.11 |

- Checks-only abstained on the clean control (f3) in 2 of 3 runs, reasoning that a 100% rollout leaves the ranker's effect unidentified. Checks without the method push toward abstaining.
- The first seed run found three problems, all fixed before the run above:
  - The f3 clean control had byte-identical rows in both weeks, which a careful agent reads as a stale copy. The fixture generator now adds seeded noise.
  - Full-arm agents searched the filesystem for `metrics.json` and read the repo's example overlay; the grader flagged 5 runs as contaminated. ds-mode now reads the overlay only from `$DS_OVERLAY_DIR`.
  - The full arm abstained on f3 for the same reason checks-only did. ds-mode now says an unidentified cause is a reason for "coincided with", not for "can't tell". This was tuned on these five cases, which are a build set, not a holdout.

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
