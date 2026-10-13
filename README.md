# ds-stack

A pstack-style plugin for data-science work. It makes an agent's number trustworthy and its document readable. Scripts check the mechanics of an analysis. The agent rules alternative explanations in or out with evidence. Every analysis ends in a fixed readout, and every document goes through a structure, format and reader test.

> If you want to go fast, go deep first. (poteto, [pstack](https://github.com/cursor/plugins/tree/main/pstack))

This repo holds only the generic core. Company facts live in a private overlay outside any repo (see [`overlay.example/`](overlay.example/README.md)).

**This is the prototype seed (`v0.3-seed`).** The work side imports it and builds on its internal metric layer. Changes flow one way, from here to work, so fixes made at work do not come back to this repo. Treat it as a snapshot.

The trust bar is review, not autonomy: a data scientist who didn't run the analysis can check a readout in under 10 minutes. Every number in a readout carries a tag (`[q3]`, `[check:mix_shift#1]`, `[given]`) that `verify_readout.py` resolves against the query and check logs.

## Skills

| Skill | Fixes | Enforced by |
|---|---|---|
| `ds-mode` | Analyses: pins the metric, checks the data, decomposes a movement, rules alternatives in or out, writes a traceable readout | A logged query runner, four logged check scripts, and `verify_readout.py`, which fails any untraced number |
| `ds-doc` | Doc structure and narrative: doc type, the spine (reader, decision, one-sentence answer, takeaways), answer-first drafting, DS claim rules | A step checklist; skipped steps stay visible |
| `doc-tighten` | Format and concision: answer placement, bold, log drift, tables, clutter, length budget | `doc_lint.py`, 14 rules |
| `cold-read` | Whether the doc works: a fresh reader must recover the answer and decision from a skim, and every takeaway from a full read | `cold_read.py`: a fresh reader (`claude -p` by default, any agent CLI through `DS_AGENT_CMD`), graded by script against `spine.json` |

Each lint rule is tied to a count from 119 agent-written docs, or to the DS editing guide in ai-writing-suite (`tools/rules.json`). On that corpus, 76 docs open with method or status before any answer, 64 lean on bold, 27 restate points in new words, and 13 turn into logs. The lint's answer-first rule flags 77 of the 119.

Word-level polish is not duplicated here. If ai-writing-suite is installed, `ds-doc` hands off to its `comms-polish` skill.

## Reviewing a readout

1. Run `python3 skills/ds-mode/tools/verify_readout.py readout.md` in the analysis directory. It resolves every tag against `.ds-queries.log` and `.ds-checks.log` and lists the `[given]` numbers to confirm against the request.
2. Read each cited query's SQL and stored result in `.ds-queries.log`, which holds the as-of period and the capped result rows, so nothing needs re-running.
3. Work through `skills/ds-mode/references/review-checklist.md`. A failed item goes back to the analyst with its number.

## What came from the retired tools

Three earlier tools (ds-brainstorm-agent, and ds-review and ds-trace in ds-productivity-agents) were folded in and retired. Only what serves review or fills a gap was kept:

| Kept | From | Now |
|---|---|---|
| The analysis reviewer's questions, without scores | ds-review | `skills/ds-mode/references/review-checklist.md` |
| Recording what the agent did | ds-trace | the query log and readout tags, written by script rather than by the agent |
| Verifying one result against a second source | ds-trace | the readout's `Reconciled:` line |
| Mistake classes with detection rules | ds-brainstorm anti-patterns | `skills/ds-mode/references/mistake-classes.md`, to seed the wrong-number archive |
| Methodology, decision and feasibility lenses | ds-brainstorm personas | `skills/ds-mode/references/plan-critique.md`, optional and not wired into the method |
| Lessons on judge noise and regression to the mean | autoresearch | `eval/README.md` |

Dropped: scoring frameworks (uncalibrated), domain digests (stale, with invented entries tagged authoritative), the writer-judge loop (no gain beyond noise), report generation and stakeholder profiles.

## Install

Install the whole plugin:

```bash
claude plugin marketplace add surahli123/ds-stack && claude plugin install ds-stack@ds-stack
codex plugin marketplace add surahli123/ds-stack && codex plugin add ds-stack
```

For Cursor, the `.cursor-plugin/plugin.json` manifest points at `skills/`. To install a single skill instead, copy its folder from `skills/` into your tool's skills directory. The skills are plain SKILL.md files with standard-library Python tools.

Status by tool: in Claude Code the plugin validates, installs, and exposes all four skills (`ds-stack:ds-mode`, `ds-doc`, `doc-tighten`, `cold-read`), and both evals ran there. Codex and Cursor have not been smoke-tested yet. The eval runner and `cold_read.py` take any agent CLI through `--agent-cmd` or `DS_AGENT_CMD`; runs without a transcript are graded with `grade.py --allow-no-transcript` and reported as unverified isolation. In the eval's full arm, the skill is pointed to from a `CLAUDE.md` note, which another agent may not read; check that first when porting.

## Results so far

Both evals use synthetic tasks and report `INSUFFICIENT_N`: plain prompting already gets the current cases right, so they can't show a gain yet. A review on real notes docs and public Simpson's-paradox data fixed several check and lint bugs. The research found curated metric definitions to be the largest lever, then execute-and-verify loops, then an explicit right to abstain. Details, numbers and what is still open: [`docs/results.md`](docs/results.md).

## Develop

```bash
make test                               # unit tests
make lint-doc DOC=doc.md TYPE=readout   # lint one document
make selftest                           # safety envelope, including the query log
make verify READOUT=readout.md          # every number traces to a logged query or check
make hooks                              # denylist hook (needs DS_OVERLAY_DIR or DS_DENYLIST)
make eval && make grade RUN=eval/results/<dir>                       # analysis eval
make writing-eval && make writing-grade RUN=eval/writing/results/<dir>   # writing eval
```

Transcripts stay local because they are bulky. A regrade without them fails closed as unverifiable, unless the runs came from a custom agent and `--allow-no-transcript` is passed.

## Other caveats

- Three of the four analysis checks are provisional until real incidents back them.
- The method in `ds-mode` is a draft, to be replaced with the analyst's own first five moves.
- `mix_shift` intervals assume independent units. Sessions clustered within users make them too narrow.
- A model reader in `cold-read` is a screen, not a certificate.
- The lint thresholds come from one person's corpus. Expect to tune them after a few weeks of use.
