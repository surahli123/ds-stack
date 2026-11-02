# Changelog

Each version is the one in the plugin manifests (`.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`). Change the version in all of them, and add its section here, in the same pull request; `tests/test_packaging.py` checks both.

## 0.6.0 (2026-11-02)

- New skill `ds-ready`. It audits a work project before ds-stack runs on it. It checks the overlay's metric definitions (required fields, aliases, prose numerators), the sources against the database, the project's AGENTS.md, and the tables and metrics that past query logs and readouts used. It lists the gaps as blocking or recommended and writes questions for each metric owner. It never drafts a definition.
- New skill `ds-retro`, a first version. It reads finished analyses or eval runs and counts the ds-verify failures and grader misses that repeat in two or more runs. For each pattern it proposes where the fix belongs (the ds-mode skill, the overlay or the project setup), with a fixture sketch for the eval gate. It notes when ds-mode already has the rule, so a gate is better than more text. It changes nothing. It doesn't yet read conversations.
- The overlay gains `tables.json`, notes on the tables the work reads.
- dots' acceptance run uses its own worktree, `~/ds-accept`, and hides every copy of the gold answers on the machine.

## 0.5.0 (2026-11-02)

- New skill `ds-interrogate`. It runs a reviewer agent from another model family (Codex for a Claude analyst, Claude Code for a Codex analyst, any family through Cursor) as its own process. The reviewer tries to break a readout with its own logged queries on a private copy of the data. A finding is kept only when four rules hold: its quote is a real claim in the readout, its query reads a data table, the query reruns to the same rows, and its numbers are anchored in those rows. Reviewers work in a temporary folder outside the project, with a small environment and the CLI's sandbox. They come from `reviewers.json` in the overlay.

## 0.4.0 (2026-11-01)

- New skill `ds-verify`. It checks a finished ds-mode readout against its query log, check log, database and metric overlay. It replays every logged query on a private copy of the data, traces every number, and checks the estimand, the "ruled in" evidence, the flagged checks and the team's metric definition. The first line is `pass`, `fail` or `unverified`. A "Needs a human" list gives the reviewer what to read, in order.
- `eval/verify_eval.py` measures ds-verify on graded runs without gold.
- The eval harness records whether each run executed. It retries rate-limited runs and never grades a run that didn't execute (`eval/execution.py`).
- Codex runs check `~/.codex` for leftovers by name. They can pin the owner's daily model and effort (`DS_CODEX_MODEL`, `DS_CODEX_EFFORT`).
- `tests/test_packaging.py` checks that the manifests agree and that each skill is named after its folder.

## 0.3.0 (2026-10-13)

- The seed: ds-mode with a logged query runner, four logged checks and traceable readouts (`verify_readout.py`); ds-doc, doc-tighten and cold-read for documents.
- Folded in and retired ds-brainstorm-agent, ds-review and ds-trace.
