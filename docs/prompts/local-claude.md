# Prompt: local Claude Code session (research, plus the Cursor column)

You are a Claude Code session on the owner's own machine, opened in `~/ds-stack`. You have two jobs that the cloud session can't do:

- **Research with open network access.** The cloud session could reach only microsoft.com and github.com.
- **The Cursor column of the acceptance run,** if `cursor-agent` is installed.

Three workers share this repo:
- dots runs the Codex column (`docs/prompts/acceptance-dots.md`).
- The cloud Claude session diagnoses, fixes, builds fixtures and merges.
- You research and run Cursor.

Each worker pushes its own branch, and only the cloud session merges.

## Rules

- Synthetic data only. Don't open, query or copy company data, and don't run SMA.
- Don't edit any skill, the grader, the fixtures, `eval/gold` or `docs/acceptance.md`.
- In `docs/`, change only what job A below says.
- Never overwrite a results or report directory.
- Push only to the branches named below. Don't merge, and don't open a PR unless the owner asks.
- Cite only sources you opened. Mark every miss-risk estimate as a judgment unless you measured it.

## Job A: research (branch `research/<date>`)

Read `docs/eval-candidates.md` first: it holds the first search and the five cases already marked to build first. Then search what that search couldn't reach:
- Fabijan et al., KDD 2019, on diagnosing sample ratio mismatch;
- Kohavi et al., KDD 2012, "Trustworthy Online Controlled Experiments: Five Puzzling Outcomes Explained";
- Crook et al., "Seven Pitfalls to Avoid when Running Controlled Experiments on the Web";
- Deng et al. on the delta method, the full paper;
- Li and Tokuda on good abandonment;
- engineering-blog posts from Booking.com, Airbnb, Netflix, LinkedIn and Spotify about real metric bugs or misreads;
- the failure analyses in DABStep, BIRD (its evidence field), Spider 2.0 and DA-Code.

For each new case, write the same fields the existing table uses:
- the mechanism;
- the source (title, authors or organization, year, URL);
- how to build it as a small synthetic SQLite fixture, with a task prompt that doesn't reveal the trap;
- the gold answer and how it is computed;
- the ds-mode component it tests;
- why a strong model without the skill would plausibly miss it.

Mark duplicates of f1–f8 or of existing candidates. A small simulation that measures a miss rate is welcome; keep its code outside the repo and report the number.

Append your cases to `docs/eval-candidates.md` under a heading "Second search (<date>)". Keep the file under its length budget: `python3 skills/doc-tighten/tools/doc_lint.py docs/eval-candidates.md --type reference` must report 0 fail. Commit the file and push the branch.

## Job B: the Cursor column (branch `results/<date>-cursor`)

Skip this job, and say so, if `command -v cursor-agent` finds nothing.

1. Run `git pull --ff-only` and record the commit hash. `docs/acceptance.md` must exist.
2. Hide gold: `mv eval/gold ~/ds-gold-hidden`. Put it back before you report, even if a step fails.
3. Run both languages, each into a new directory:
   ```bash
   D=$(date +%Y-%m-%d)
   python3 eval/run_arms.py --runs 3 --agent-cmd "sh $PWD/eval/agents/cursor.sh {prompt_file}" --out eval/results/$D-cursor-en
   python3 eval/run_arms.py --runs 3 --agent-cmd "sh $PWD/eval/agents/cursor.sh {prompt_file}" --prompt-suffix "请用中文写结论。" --out eval/results/$D-cursor-zh
   ```
   If `cursor-agent` rejects a flag in `eval/agents/cursor.sh`, report it and stop. Don't edit the script.
4. Restore gold, then grade and fill in the table:
   ```bash
   mv ~/ds-gold-hidden eval/gold
   for R in eval/results/$D-cursor-*; do python3 eval/grade.py "$R" --allow-no-transcript; done
   python3 eval/acceptance.py eval/results/$D-cursor-* --allow-no-transcript
   ```
5. Commit only `eval/results/$D-cursor-*` to `results/$D-cursor`, and push.

## Report back

```
Local session, <date>, commit <hash>
Research: <number of new cases>, pushed to <branch>; the three you'd build first and why
Cursor: <the eval/acceptance.py output, or "skipped: cursor-agent not installed">
Problems: <none, or the step, the command and its error>
```
