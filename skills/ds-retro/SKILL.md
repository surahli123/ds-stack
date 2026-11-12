---
name: ds-retro
description: >-
  Use to learn from finished analyses: "what mistakes keep repeating", "retro
  on the last readouts", "what should ds-mode learn", "复盘过去的分析",
  "总结反复出现的问题". Reads finished analyses or eval runs, finds the
  ds-verify failures and grader misses that repeat across runs, and proposes
  where each fix belongs (the ds-mode skill, the overlay, or the project setup)
  with a fixture for the eval gate. It proposes; a person decides. Also runs on
  /ds-retro.
---

# ds-retro

A mistake that happens once is noise. One that repeats is a missing rule, a missing check, or a rule that nobody follows. This skill finds the repeats and writes a proposal for each, with where the fix belongs and how to test it. It changes nothing. A person approves each proposal, and a change to ds-mode goes in only after it passes the eval gate.

## Steps

1. Run it on finished analyses, each a folder with the readout, its logs, and if possible `request.md` and the database:

   ```bash
   python3 <skills>/ds-retro/tools/retro.py --analyses <folder> <folder> ...
   ```

   For eval runs, use `--results eval/results/<dir> ...` instead; it adds the grader's reasons and reads the full arm unless `--arms` says otherwise. Don't include runs made with a deliberately broken skill, such as the teeth tests.
2. Read `ds-retro/proposals.md`. Each proposal gives:
   - the pattern and the number of runs it appeared in (2 or more by default; `--min-runs` changes that);
   - where the fix belongs;
   - the proposed rule, or a note that ds-mode already has the rule and the runs broke it;
   - a fixture sketch for the eval gate, and up to three examples.
3. Decide each proposal:
   - ds-mode skill: build the fixture, then run the eval gate. Plain prompting must miss it, ds-mode with the rule must get it right, and the fixture must fail again without the rule. When ds-mode already has the rule, prefer a gate (ds-verify before replying) over more text.
   - Overlay: the metric's owner writes the entry, as ds-ready asks.
   - Project setup: the owner fixes it.
   - "A person decides": read the examples; a real mistake with no check behind it becomes a candidate in `ds-mode/references/mistake-classes.md`.

## Where fixes belong

| Pattern | Fix |
|---|---|
| The readout ignored the overlay, or gave a number for an unavailable metric | ds-mode, gated by ds-verify; the overlay entry, if it was missing |
| Wrong unit, a causal number without a design, missing estimate lines, a Headline that is no estimate | ds-mode's readout rules |
| A hedged "ruled in", or alternatives without a verdict | ds-mode's verdict vocabulary |
| A failed check left out, a hand-computed Headline, a pasted result | ds-mode's readout rules, gated by ds-verify |
| No request or no check log next to the readout | Project setup |
| A wrong number that no check caught | A person decides; possibly a new check |

## Not yet

This version reads ds-verify findings and grader misses. It doesn't yet read your conversations with the agent: the places you corrected it or repeated an instruction. That needs a model to read free text, and it must run only on the work laptop, where those conversations live.
