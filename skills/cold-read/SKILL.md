---
name: cold-read
description: >-
  Use before sending or handing off any document, to prove it works for its
  reader: a fresh reader with no context gets the doc and must recover the
  answer, the decision and the key takeaways, first from a skim and then from
  a full read, graded by a script against the spine. The doc is fixed until
  they do. Also runs on /cold-read.
---

# cold-read

A doc passes when its reader gets the point, not when its author likes it. This is the failing test for writing.

## 1. Write the answer key first

The key is `spine.json` from `ds-doc`: the reader's role, the answer in one sentence, the decision and three takeaways. If you have none, write it now from what you meant to say. Do not derive it from the doc, or the test can't fail.

## 2. Run it

```
python3 <dir of this SKILL.md>/tools/cold_read.py doc.md --spine spine.json
```

The script builds the skim view (the first 120 words, then each heading with its section's first sentence). It sends the skim and the full doc to a fresh reader, using `claude -p` with no tools and none of your context, with the prompts in `references/reader-prompts.md`. Then it grades the answers against the spine. The script does the grading, not you. Items that share too few words with the key go to a separate grader call. It prints one line per item and a verdict, for example "cold-read: skim 2/2, full 3/3 - pass", and writes `cold_read.json` next to the doc.

| Pass | Passes when |
|---|---|
| Skim | The reader states the answer and the decision |
| Full | The reader recovers all three takeaways |

Without the `claude` CLI (for example in Cursor or Codex), run with `--prompts-only`. Send each prompt to a fresh subagent with nothing else, save the replies as `{"skim": "...", "full": "..."}`, and grade with `--replies replies.json`. A reader from a different model family than the author is better, because it doesn't share the author's blind spots.

## 3. Fix the doc, not the reader

When the reader misses something, the fix is usually one of these: move the answer up, rename a heading so it states its claim, or cut the section that buried the point. Rerun after each fix. Read the reader's "got lost" line even on a pass; it finds problems the grading can't, like two baselines with no word on which one counts. After three failed rounds, stop and report what the reader keeps missing. The spine itself may be wrong.

A fresh model reader is a screen, not a certificate. For a high-stakes doc, also ask one real reader to state the decision after reading only the first screen.
