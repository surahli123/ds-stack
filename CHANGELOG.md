# Changelog

Each version is the one in the plugin manifests (`.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`). Change the version in all of them, and add its section here, in the same pull request; `tests/test_packaging.py` checks both.

## 0.4.0 (2026-11-01)

- New skill `ds-verify`. It checks a finished ds-mode readout against its query log, check log, database and metric overlay. It replays every logged query on a private copy of the data, traces every number, and checks the estimand, the "ruled in" evidence, the flagged checks and the team's metric definition. The first line is `pass`, `fail` or `unverified`. A "Needs a human" list gives the reviewer what to read, in order.
- `eval/verify_eval.py` measures ds-verify on graded runs without gold.
- The eval harness records whether each run executed. It retries rate-limited runs and never grades a run that didn't execute (`eval/execution.py`).
- Codex runs check `~/.codex` for leftovers by name. They can pin the owner's daily model and effort (`DS_CODEX_MODEL`, `DS_CODEX_EFFORT`).
- `tests/test_packaging.py` checks that the manifests agree and that each skill is named after its folder.

## 0.3.0 (2026-10-13)

- The seed: ds-mode with a logged query runner, four logged checks and traceable readouts (`verify_readout.py`); ds-doc, doc-tighten and cold-read for documents.
- Folded in and retired ds-brainstorm-agent, ds-review and ds-trace.
