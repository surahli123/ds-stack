---
name: ds-mode
description: >-
  Use for data analysis that produces a number someone will act on: a metric
  moved, an experiment readout, a "did X cause Y" question, or a sizing.
  Runs mechanical checks on aggregates before any number is reported, rules
  alternative explanations in or out with evidence, and ends with a fixed
  human-readable readout. Also runs on /ds-mode.
---

# ds-mode

You own the number and the inference. A number that passes every check but answers the wrong question, or tells the wrong story, is still wrong. A wrong number stated with confidence is worse than "can't tell".

## Method

This is a draft, to be replaced with the analyst's own first moves.

1. Restate the question in one sentence and name the decision it feeds. Treat the requester's guess about the cause as one alternative, not the premise.
2. Check the data before the question. Make sure every period you use is complete (`completeness`). After any join, compare row counts before and after (`fanout`).
3. Size, then decompose.
   - When a rate moved, split the change by the segments whose mix could have shifted (platform, country, traffic source) and run `mix_shift`.
   - For an experiment, run `srm` on the assignment counts before you read any lift.
4. Rule each alternative in or out with evidence. Always consider mix-shift, seasonality and day of week, data completeness, logging or definition changes, and the requester's cause. Label each conclusion measured, inferred or guess.
5. Write the readout below as your final reply.

## Checks

Run each check as `python3 <dir of this SKILL.md>/checks/run.py <check> --json '<spec>'`. `--list` shows when to use each check and an example spec. Checks take aggregates you computed, never raw rows. Each one prints a JSON line and logs it to `.ds-checks.log`.

| Check | Run it when |
|---|---|
| `completeness` | before reporting any period |
| `fanout` | after any join |
| `mix_shift` | a rate moved and segment mix could have changed |
| `srm` | before reading any experiment lift |

- Report every check that applies, with its status. If you skip one, say why.
- A failed check must change the answer, or the readout must show with evidence why it doesn't. If you can't resolve it, the headline is `can't tell`. Say what is missing and what would settle it.
- A check that could not run because of how you called it (wrong spec, wrong grain) gets fixed and rerun.
- A check that could not run because the data can't support it at all (for example, `completeness` with no earlier periods to compare against) does not by itself mean `can't tell`. Answer, report the check as could not run, and put the gap in the caveats. Abstain only if that gap could plausibly change the answer.
- Copy check output exactly; never edit it.

On a live warehouse, send every query through the overlay's guarded runner, and keep raw rows out of the conversation.

## Readout

Your final reply is exactly this format, written for the person who acts on it:

```
## Answer
Headline: <signed number> <unit> [(<interval>)]   or   Headline: can't tell
<one plain sentence: what happened and how big>

## What it means for <the decision>
<one or two sentences>

## Why we believe it
- Alternatives considered:
  - <alternative>: ruled <in|out> by <evidence> [measured|inferred|guess]
- Checks run:
  - <check>: <pass|fail|could not run|skipped> <one-line result or reason>

## Caveats, and what would change the answer
- <short list>
```

- measured means computed from data in this session.
- inferred means it follows from measured facts by reasoning.
- guess means neither.

When this readout grows into a document for other people (a readout, memo, plan or handover), write it with the `ds-doc` skill.
