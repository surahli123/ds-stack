# ds-stack

A pstack-style plugin for data-science work. It makes an agent's number trustworthy and its document readable. Scripts check the mechanics of an analysis. The agent rules alternative explanations in or out with evidence. Every analysis ends in a fixed readout, and every document goes through a structure, format and reader test.

> If you want to go fast, go deep first. (poteto, [pstack](https://github.com/cursor/plugins/tree/main/pstack))

This repo holds only the generic core. Company facts live in a private overlay outside any repo (see [`overlay.example/`](overlay.example/README.md)).

## Skills

| Skill | Fixes | Enforced by |
|---|---|---|
| `ds-mode` | Analyses: checks the data, decomposes a movement, rules alternatives in or out, writes the readout | Four check scripts that log every run |
| `ds-doc` | Doc structure and narrative: doc type, the spine (reader, decision, one-sentence answer, takeaways), answer-first drafting, DS claim rules | A step checklist; skipped steps stay visible |
| `doc-tighten` | Format and concision: answer placement, bold, log drift, tables, clutter, length budget | `doc_lint.py`, 14 rules |
| `cold-read` | Whether the doc works: a fresh reader must recover the answer and decision from a skim, and every takeaway from a full read | `skim_view.py` and fixed reader prompts |

Each lint rule is tied to a count from 119 agent-written docs, or to the DS editing guide in ai-writing-suite (`tools/rules.json`). On that corpus, 76 docs open with method or status before any answer, 64 lean on bold, 27 restate points in new words, and 13 turn into logs. The lint's answer-first rule flags 77 of the 119.

Word-level polish is not duplicated here. If ai-writing-suite is installed, `ds-doc` hands off to its `comms-polish` skill.

## Install

Install the whole plugin:

```bash
claude plugin marketplace add surahli123/ds-stack && claude plugin install ds-stack@ds-stack
codex plugin marketplace add surahli123/ds-stack && codex plugin add ds-stack
```

For Cursor, the `.cursor-plugin/plugin.json` manifest points at `skills/`. To install a single skill instead, copy its folder from `skills/` into your tool's skills directory. The skills are plain SKILL.md files with standard-library Python tools.

Status by tool: in Claude Code the plugin validates, installs, and exposes all four skills (`ds-stack:ds-mode`, `ds-doc`, `doc-tighten`, `cold-read`), and both evals ran there. Codex and Cursor have not been smoke-tested yet.

## Results so far

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
- Agents skipped the in-loop cold read even when told to, but said so in their reply.

What the evals show: short tasks written from clean notes are too easy, both for analysis and for writing. The corpus failures came from long, multi-session docs written mid-work. The next eval should rewrite real bloated docs and measure a fresh reader before and after, using cases built from real incidents.

## Develop

```bash
make test                               # unit tests
make lint-doc DOC=doc.md TYPE=readout   # lint one document
make selftest                           # safety envelope
make hooks                              # denylist hook (needs DS_OVERLAY_DIR or DS_DENYLIST)
make eval && make grade RUN=eval/results/<dir>                       # analysis eval
make writing-eval && make writing-grade RUN=eval/writing/results/<dir>   # writing eval
```

Transcripts stay local because they are bulky. A regrade without them fails closed as unverifiable.

## Other caveats

- Three of the four analysis checks are provisional until real incidents back them.
- The method in `ds-mode` is a draft, to be replaced with the analyst's own first five moves.
- The lint thresholds come from one person's corpus. Expect to tune them after a few weeks of use.
