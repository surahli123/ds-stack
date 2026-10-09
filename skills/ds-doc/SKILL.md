---
name: ds-doc
description: >-
  Use when writing or rewriting a document someone will read and act on: an
  analysis or experiment readout, a decision memo, a plan, or a handover.
  Fixes document structure and narrative: picks the doc type, writes the spine
  (reader, decision, one-sentence answer, takeaways) before any prose, drafts
  answer-first, then runs doc-tighten and cold-read. Also runs on /ds-doc.
---

# ds-doc

Agent-written docs rarely fail on wording. They fail on order and emphasis. The answer arrives after the method. Bold carries the emphasis instead of the sentence. The doc turns into a log. The same point comes back in new words. This skill fixes the shape. `doc-tighten` fixes format and length, and `cold-read` proves a reader gets the point.

## Steps

Copy these steps into your todo list before you start. A step you skip stays in the list as "skip: <reason>".

1. Pick the doc type.
2. Write the spine.
3. Draft in skeleton order.
4. Check DS claims against their evidence.
5. Run the lint until it reports 0 fail.
6. Run the cold read until it passes.
7. Reply with one line per check, for example "lint: 0 fail, 2 warn; cold-read: skim 2/2, full 3/3".

## 1. Pick the doc type

Read `references/doc-types.md` and pick one type: readout, memo, plan or handover. A doc that has two jobs becomes two docs. If no type fits, use the closest one and say which section you changed.

## 2. Write the spine before any prose

Write these in your working notes, not in the doc:

- Reader: one role, such as "the PM who owns the launch". Address that reader one way all through the doc.
- Decision: what the reader will decide or do after reading.
- Answer: one sentence of at most 30 words that includes the number that matters.
- Takeaways: the three facts the reader must leave with. `cold-read` tests these, so make each one checkable.
- Headings: one per section, each stating that section's claim ("Mix explains the whole drop"), not its topic ("Analysis").

Then run the skim test on the spine. The headings plus the first sentence of each section, read alone, must tell the whole story. If they don't, fix the spine before writing.

## 3. Draft in skeleton order

- The first screen carries the answer, what it means for the decision, and any ask. Method, sources and provenance go last or into an appendix.
- Each section opens with its claim, and the evidence follows. A section that only "provides context" gets merged or cut.
- Link sections with the reason they follow each other ("so", "but", "because"), not with "Next, …".
- Write the current state. History lives in git: no dated DONE lines, no strikethrough, no change log.
- Call things by name. If a code like `B3` must stay, define it the first time it appears.

## 4. Hold DS claims to their evidence

Follow `references/ds-claims.md`. Every number and causal claim points at its evidence. Hedges match the strength of the evidence, and the answer carries none. "Significant", "causal" and "drives" need a named test or design. The "so what" comes from what the analysis measured, and its label (measured, inferred or guess) says how far it goes.

## 5. Tighten, then test with a reader

1. Lint the draft, fix every fail, and rerun until it reports 0 fail. The `doc-tighten` skill sits next to this one and covers the cutting order and format rules:
   ```
   python3 <dir of this SKILL.md>/../doc-tighten/tools/doc_lint.py doc.md --type <type>
   ```
2. Cold-read the draft with the spine's answer, decision and takeaways. The `cold-read` skill sits next to this one. Build the skim view, then give it and the full doc to a fresh subagent with the reader prompts:
   ```
   python3 <dir of this SKILL.md>/../cold-read/tools/skim_view.py doc.md
   ```
   Fix the doc until the reader gets the answer and decision from the skim, and every takeaway from the full read.
3. Optional word-level polish: if the ai-writing-suite plugin is installed, run its `comms-polish` skill. Wording is not this skill's job.

## When not to use it

Skip it for chat replies, one-line commit messages and code comments. For a ds-mode readout, the fixed readout format already is the skeleton. Use this skill when that readout grows into a document for other people.
