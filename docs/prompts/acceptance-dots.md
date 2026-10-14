# Prompt: acceptance run, dots's part (Codex on the owner's machine)

You run the Codex column of the ds-stack acceptance matrix on the machine of the person you work for. Claude owns the acceptance doc, the fixtures and every fix (`docs/prompts/acceptance-claude.md`). Your job is to run, grade and report. Don't fix anything.

## Rules

- Synthetic data only. Don't open, query or copy company data, and don't run SMA.
- Don't edit `docs/acceptance.md`, any skill, the grader or the fixtures. If something looks wrong, report it.
- Gold stays hidden while agents run, as step 2 describes.
- Never overwrite a results or report directory. Each run gets a new one; `run_arms.py` refuses an existing run.
- Codex results made before commit `1093ca9` (a `codex.sh` without an empty `HOME`) are contaminated by the owner's global instructions and skills. Keep them, list them as contaminated in the report, and never grade them into the acceptance table.
- Push only your results, to a new branch named `results/<date>-<harness>`. Don't merge anything, and don't open a PR unless the owner asks.

## Steps

### 1. Check that it is time to start

```bash
if [ -d ~/ds-stack/.git ]; then git -C ~/ds-stack pull --ff-only; else git clone https://github.com/surahli123/ds-stack ~/ds-stack; fi
cd ~/ds-stack && test -f docs/acceptance.md && git log -1 --format=%H
```

Stop and tell the owner if `docs/acceptance.md` doesn't exist yet. Record the commit hash. Also check that `codex --version` works and that `codex login status` shows a sign-in.

Each code block below is meant to run as one shell command. Blocks don't share variables, so every block from step 3 on reads the run id from `~/ds-run-id`.

### 2. Fix the run id, then hide gold and Codex's global instructions

```bash
for p in ~/ds-run-id ~/ds-gold-hidden ~/ds-codex-hidden; do [ -e "$p" ] && { echo "leftover $p from an unfinished run: stop and report"; exit 1; }; done
date +%Y-%m-%d-%H%M > ~/ds-run-id && cat ~/ds-run-id
mv ~/ds-stack/eval/gold ~/ds-gold-hidden
mkdir ~/ds-codex-hidden
for f in AGENTS.md skills prompts; do [ -e ~/.codex/$f ] && mv ~/.codex/$f ~/ds-codex-hidden/; done
ls ~/ds-codex-hidden
```

If the first line reports a leftover, stop: an earlier run didn't finish cleanly, and the owner decides what to restore.

`--ignore-user-config` skips only `config.toml`. Global instructions in `~/.codex` would reach every arm, plain prompting included. Leave `auth.json` and `plugins/` where they are. `eval/agents/codex.sh` also gives Codex an empty `HOME`, so skills in `~/.agents/skills` stay out, and switches off plugins, remote plugins, apps and memories for each run.

Then confirm the isolation with one paid call:

```bash
cd ~/ds-stack && sh eval/agents/codex-isolation-probe.sh
```

The script prints Codex's two-line reply, then `PASS` or `FAIL`. It passes only when every listed skill is one of Codex's five rebuilt system skills (imagegen, openai-docs, plugin-creator, skill-creator, skill-installer) and no instruction file is listed. On `FAIL`, run step 5's first block to put everything back, then stop and report the reply.

### 3. Run the Codex column, in English and in Chinese

```bash
cd ~/ds-stack && D=$(cat ~/ds-run-id) && python3 eval/run_arms.py --runs 3 --agent-cmd "sh $PWD/eval/agents/codex.sh {prompt_file}" --out eval/results/$D-codex-en
```

```bash
cd ~/ds-stack && D=$(cat ~/ds-run-id) && python3 eval/run_arms.py --runs 3 --agent-cmd "sh $PWD/eval/agents/codex.sh {prompt_file}" --prompt-suffix "请用中文写结论。" --out eval/results/$D-codex-zh
```

Each command runs every fixture through three arms (plain prompting, checks only, full ds-mode), 3 times each. Each run's directory keeps `result.md`, `agent.log` (Codex's own log), `queries.log`, `checks.log` and `meta.json`.

### 4. Don't run Cursor

The Cursor column isn't run this round.

### 5. Restore everything, then grade

Restore first, also when you stop early. Codex rebuilds `~/.codex/skills` (its system skills) on every run, so the rebuilt copy moves to `~/ds-codex-recreated-<run id>`, kept, before the original goes back:

```bash
D=$(cat ~/ds-run-id 2>/dev/null || date +%Y-%m-%d-%H%M)
[ -e ~/ds-stack/eval/gold ] || mv ~/ds-gold-hidden ~/ds-stack/eval/gold
for f in ~/ds-codex-hidden/* ~/ds-codex-hidden/.[!.]*; do
  [ -e "$f" ] || continue; n=$(basename "$f")
  if [ -e ~/.codex/"$n" ]; then mkdir -p ~/ds-codex-recreated-$D && mv ~/.codex/"$n" ~/ds-codex-recreated-$D/; fi
  mv "$f" ~/.codex/
done; rmdir ~/ds-codex-hidden
ls ~/ds-stack/eval/gold ~/.codex ~/ds-codex-recreated-$D 2>/dev/null
```

Then grade:

```bash
cd ~/ds-stack && D=$(cat ~/ds-run-id) && grep -l "is not isolated" eval/results/$D-codex-*/*/agent.log; for R in eval/results/$D-codex-*; do python3 eval/grade.py "$R" --allow-no-transcript; done; python3 eval/acceptance.py eval/results/$D-codex-* --allow-no-transcript
```

### 6. Push the results

```bash
cd ~/ds-stack && D=$(cat ~/ds-run-id) && git checkout -b results/$D-codex && git add eval/results/$D-codex-* && git commit -m "Acceptance results from Codex, $D" && git push -u origin results/$D-codex && rm ~/ds-run-id
```

## Report back

Send the person you work for this, and nothing else:

```
ds-stack acceptance, <date>, commit <hash>
Codex: <version>
<the full output of eval/acceptance.py>
<for each results directory: its Fixtures-by-majority table from summary.md>
Failing runs: <directory/run: the Reason column from summary.md>
Pushed: <branch name>
Contaminated earlier directories: <list, or "none">
Hidden from ~/.codex: <what step 2 moved, or "nothing">; isolation probe: <its reply, shortened>; runs flagged "not isolated": <count>
Problems: <none, or the step, the command and its error>
```
