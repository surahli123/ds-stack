---
name: ds-interrogate
description: >-
  Use for a second opinion on a ds-mode readout from a model of another
  family: "interrogate this readout", "have another model check it", "cross-model
  review", "let Codex check it", "让另一个模型审一遍", "交叉审核这个结论". A
  reviewer agent tries to break the readout with its own queries on a copy of the
  data; only findings that a rerun proves are kept. Run ds-verify first. Also
  runs on /ds-interrogate.
---

# ds-interrogate

ds-verify checks a readout against its own evidence. It can't see a wrong filter, a wrong comparison or an alternative nobody listed. This skill gives the readout to a reviewer from another model family, which tries to break it with its own queries. A script keeps a finding only when a rerun proves it. A person decides whether a kept finding changes the answer.

## Steps

1. Run ds-verify and fix its failures first. It costs nothing; a reviewer costs a model call and a few minutes.
2. Save the original request to `request.md`.
3. Run the script from the analysis directory, naming your own model family:

   ```bash
   python3 <skills>/ds-interrogate/tools/interrogate.py readout.md --request request.md --analyst-family <family>
   ```

   The family is `claude` in Claude Code, `gpt` in Codex, and the family of the model you run on in Cursor. With `--analyst-model <slug>` the script works out the family. `--reviewers 2` runs two reviewers, from two families when two are installed. Each reviewer's directory, log and queries stay under `ds-interrogate/`.
4. Read the report. The first line gives the number of verified findings, the reviewers that ran, and whether the review was independent. Each finding shows the readout's words, the reviewer's query and rows, what the rows show, and the reviewer's claim about why it matters.
5. Act on it:
   - Analyst: for each finding, fix the analysis or say in the readout why the finding doesn't change the answer. Then run ds-verify again.
   - Reviewer: judge each finding. The rows are proven; the claim about what they mean is not.
   - Dropped findings are listed with the reason. Don't act on them.
   - "No verified findings" means no reviewer proved the readout wrong. It doesn't prove it right.

## Choosing the reviewer

A reviewer is a command-line agent that the script runs as its own process. So the harness's own subagents don't limit the choice: in Claude Code the reviewer can be Codex, and in Codex it can be Claude Code. A `/codex` command that runs Codex from Claude Code can call this script.

The reviewers come from `reviewers.json` in `$DS_OVERLAY_DIR` (see `overlay.example/reviewers.json`). Without that file the defaults are Codex for `gpt` and Claude Code for `claude`. Each entry names a family, a model (`-` for the CLI's own default, so Codex keeps your daily model and effort) and a command. The wrappers in `tools/reviewers/` run `codex exec`, `claude -p` and `cursor-agent -p --model <slug>`. With Cursor, any model family it offers can review.

The script uses only installed reviewers, in file order, and takes them from a family other than the analyst's. When only the analyst's family is installed, it runs one anyway and says the review is not independent. When the analyst's family is unknown, it says the family check didn't run.

On the work laptop, list only the CLIs approved for company data. The reviewer reads the readout, the logs and a copy of the data.

## What counts as proof

A finding is kept only when all four hold:

1. Its quote is in the readout, word for word.
2. Its query ran through ds-mode's runner, in the reviewer's own log.
3. That query, replayed on a fresh copy of the data, gives the same rows.
4. Its "shows" text quotes those rows. At least one of its numbers is in them. Of the numbers that aren't already in the readout or the analyst's logs, at least half are in them too. The rest, such as differences the reviewer worked out, are listed as "not in the rows" for you to check.

The reviewer's private copy of the data has no scratch tables from the analysis. Its writes never reach the analysis database. The brief it gets is `references/brief.md`.

## First live run

On 2026-11-02 a Claude reviewer, standing in for a Codex analyst, reviewed one correct f1 readout and a copy with one planted fault. The planted fault changed "mobile share rose from 40.1% to 55.1%" to "45.1%" in an alternative line, which ds-verify passes.

- The reviewer found the planted fault with its own query. The first version of rule 4 dropped the finding, because the finding quoted the readout's wrong number and a difference the reviewer had worked out. Rule 4 now allows both, and the finding is kept.
- On the correct readout, 3 findings were kept. Each questions the reasoning, not a number: the mix shift happened on the rollout day, seasonality was ruled out on one week of data, and a logging change was ruled out on the release log alone. Whether they change the answer is a person's call.

The GPT reviewer through Codex hasn't run yet; it needs the work laptop. Record each finding and whether it held, so the next change to the rules rests on data.
