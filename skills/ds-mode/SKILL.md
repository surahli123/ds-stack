---
name: ds-mode
description: >-
  Use for data analysis that produces a number someone will act on: a metric
  moved, an experiment readout, a "did X cause Y" question, or a sizing.
  Pins the metric definition first, runs mechanical checks on aggregates
  before any number is reported, rules alternative explanations in or out
  with evidence, and ends with a fixed human-readable readout. Also runs on
  /ds-mode.
---

# ds-mode

You own the number and the inference. A number that passes every check but answers the wrong question, or tells the wrong story, is still wrong. A wrong number stated with confidence is worse than "can't tell".

## Method

This is a draft, to be replaced with the analyst's own first moves.

1. Restate the question in one sentence and name the decision it feeds. Treat the requester's guess about the cause as one alternative, not the premise.
2. Pin the metric before you query: numerator, denominator, filters, grain and source table. Take it from the overlay's `metrics.json` when the metric is there, and say so. When it isn't, write your definition into the readout and label it `[guess]`. Never invent a definition silently; a plausible number on the wrong definition is the most common wrong answer, and no check below catches it.
3. Decide whether the question can be answered.
   - If two readings of it give materially different numbers and nothing settles which one is meant, ask before computing. When no one can answer, pick the reading the decision most likely needs, state it in the Answer, and put the other in the caveats.
   - If the data can't answer it (the metric isn't logged, the period hasn't landed), say so up front instead of computing a substitute.
4. Check the data before the question. Make sure every period you use is complete (`completeness`). After any join, compare row counts before and after (`fanout`).
5. Size, then decompose.
   - When a rate moved, run `mix_shift` on the segments whose mix could have shifted (platform, country, traffic source). Use the finest grain that keeps about 100 units per cell on both sides, then rerun at one coarser grain. If the two disagree, report both.
   - For an experiment, run `srm` on the assignment counts before you read any lift.
6. Rule each alternative in or out with evidence. Always consider mix-shift, seasonality and day of week, data completeness, logging or definition changes, and the requester's cause. The evidence names a check or a query result from this session. Label each conclusion measured, inferred or guess.
7. Write the readout below as your final reply.

## Checks

Run each check as `python3 <dir of this SKILL.md>/checks/run.py <check> --json '<spec>'`. `--list` shows when to use each check and an example spec. Checks take aggregates you computed, never raw rows. Each one prints a JSON line and logs it to `.ds-checks.log`.

| Check | Run it when |
|---|---|
| `completeness` | before reporting any period |
| `fanout` | after any join |
| `mix_shift` | a rate moved and segment mix could have changed |
| `srm` | before reading any experiment lift |

Statuses mean different things:

- `pass`: nothing found.
- `flag` is a finding, not a defect. From `mix_shift`, it means segment mix explains a real part of the move, so the Answer must say how much of the change is mix and how much is within-segment change.
- `fail` is a data or query defect. It must change the answer, or the readout must show with evidence why it doesn't. If you can't resolve it, the headline is `can't tell`; say what is missing and what would settle it.
- `could not run` because of how you called it (wrong spec, wrong grain): fix the call and rerun.
- `could not run` because the data can't support the check at all (for example, `completeness` with no earlier periods): answer anyway, report the check as could not run, and put the gap in the caveats. Abstain only if that gap could plausibly change the answer.

Report every check that applies, with its status. If you skip one, say why. Copy check output exactly; never edit it.

On a live warehouse, send every query through the overlay's guarded runner, and keep raw rows out of the conversation.

## Readout

Your final reply is exactly this format, written for the person who acts on it:

```
## Answer
Headline: <signed number> <unit> (<95% interval>)   or   Headline: can't tell
<one plain sentence: what happened and how big>

## What it means for <the decision>
<one or two sentences that compare the interval with the smallest change that would alter the decision>

## Why we believe it
- Alternatives considered:
  - <alternative>: ruled <in|out> by <evidence> [measured|inferred|guess]
- Checks run:
  - <check>: <pass|flag|fail|could not run|skipped> <one-line result or reason>

## Caveats, and what would change the answer
- <short list>

## Provenance
- Metric: <definition>, from <metrics.json | stated here [guess]>
- Data: <tables or views>, through <last complete period>
- Queries and checks: <where they are logged>
```

- The interval is required. `mix_shift` reports one for the overall change (`delta_ci95_pp`). For an experiment lift, use a two-proportion interval. When no interval can be computed, write `(no interval: <reason>)`.
- Use causal words ("caused", "drove", "because of") only for a randomized test or a design that identifies the cause. Otherwise say "coincided with" or "is associated with", and name what would confirm it.
- measured means computed from data in this session.
- inferred means it follows from measured facts by reasoning.
- guess means neither.

When this readout grows into a document for other people (a readout, memo, plan or handover), write it with the `ds-doc` skill.
