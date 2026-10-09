---
name: doc-tighten
description: >-
  Use after drafting any document, or when asked to tighten, shorten, clean
  up or reformat a doc. Fixes format and concision: runs a lint calibrated on
  119 agent-written docs (answer placement, bold, log drift, tables,
  clutter, length budget), then cuts in a fixed order. Does not change
  meaning. Also runs on /doc-tighten.
---

# doc-tighten

## 1. Run the lint

```
python3 <dir of this SKILL.md>/tools/doc_lint.py <doc.md> --type readout|memo|plan|handover|reference|other
```

- Every fail must be fixed.
- Judge each warn: fix it, or leave it because the doc needs it there.

Rerun until no fails remain. `tools/rules.json` holds each rule's threshold and the evidence behind it.

## 2. Cut in this order

Each pass removes one kind of weight. Stop when the doc fits its budget and nothing else can go without losing a fact the reader needs.

1. Restatements. Say each point once, where it belongs. A second summary, a "restated" section and a closing recap are the usual places.
2. Process. Take out what you did: which tools ran, which agents checked, what you tried first. Keep a method only if the reader must rerun or audit it, and then put it in the appendix.
3. Meta-commentary. Take out "verified" badges, status banners, thinking out loud and self-praise.
4. Detail. Move anything the decision doesn't turn on into the appendix.
5. Sentences. Delete words that do no work, and split sentences that carry two ideas.

## 3. Use the right format for each piece

| Piece | Use it for |
|---|---|
| Prose | Reasoning: anything with "because", "so" or "but" in it |
| Numbered list | Steps in order |
| Bullets | Parallel items, at most seven, without bold labels |
| Table | Three or more items compared on two or more attributes; every cell a short fact |
| Heading | The section's claim, in sentence case; two levels are enough under 1,000 words |
| Bold | Only what a skimmer must not miss; at most two spans per 100 words, never a whole sentence |
| Code font | Names the reader will type or search for |

All-caps is never emphasis. Prose in a table cell means the table is wrong.

## Out of scope

This skill does not change claims, numbers or conclusions. A finding that must change goes back to the author. It also doesn't police word choice; for that, use ai-writing-suite's `comms-polish` if it is installed.
