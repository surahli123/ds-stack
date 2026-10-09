---
name: cold-read
description: >-
  Use before sending or handing off any document, to prove it works for its
  reader: a fresh reader with no context gets the doc and must recover the
  answer, the decision and the key takeaways, first from a skim and then from
  a full read. The doc is fixed until they do. Also runs on /cold-read.
---

# cold-read

A doc passes when its reader gets the point, not when its author likes it. This is the failing test for writing.

## 1. Write the answer key first

You need the spine from `ds-doc`:
- the reader's role
- the answer in one sentence
- the decision
- the three takeaways

If you have no spine, write the key now from what you meant to say. Do not derive it from the doc, or the test can't fail.

## 2. Build the skim view

```
python3 <dir of this SKILL.md>/tools/skim_view.py <doc.md>
```

This prints the first 120 words, then every heading with the first sentence of its section. That is roughly what a busy reader sees.

## 3. Ask a fresh reader

Use a reader that hasn't seen your work: a new subagent, or another model run in a clean context. A different model family is better, because it doesn't share your blind spots. Give it the reader's role and the text, and nothing else: not the spine, not the source notes, not this skill.

Use the prompts in `references/reader-prompts.md`:

1. **Skim pass.** The skim view only. Ask for the answer, the decision, and the number that matters most.
2. **Full pass.** The whole doc. Ask the same questions, then where they had to reread or got lost, and what they would ask the author.

## 4. Grade against the key

Mark each item got, partly or missed.

| Pass | Passes when |
|---|---|
| Skim | The reader states the answer and the decision |
| Full | The reader gets all three takeaways, and every "got lost" spot is fixed or answered in the doc |

When a reader misses something, fix the doc, not the reader. Usually the fix is moving the answer up, renaming a heading to state its claim, or cutting the section that buried the point. Rerun after each fix. After three failed rounds, stop and report what the reader keeps missing; the spine itself may be wrong.

Report the result in one line: "cold-read: skim 2/2, full 3/3".
