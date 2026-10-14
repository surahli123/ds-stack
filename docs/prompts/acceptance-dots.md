# Prompt: acceptance run, dots's part (Codex and Cursor on the owner's machine)

You run the Codex column, and the Cursor column if `cursor-agent` is installed, of the ds-stack acceptance matrix on the machine of the person you work for. Claude owns the acceptance doc, the fixtures and every fix (`docs/prompts/acceptance-claude.md`). Your job is to run, grade and report. Don't fix anything.

## Rules

- Synthetic data only. Don't open, query or copy company data, and don't run SMA.
- Don't edit `docs/acceptance.md`, any skill, the grader or the fixtures. If something looks wrong, report it.
- Gold stays hidden while agents run, as step 2 describes.
- Never overwrite a results or report directory. Each run gets a new one.
- Push only your results, to a new branch named `results/<date>-<harness>`. Don't merge anything, and don't open a PR unless the owner asks.

## Steps

### 1. Check that it is time to start

```bash
if [ -d ~/ds-stack/.git ]; then git -C ~/ds-stack pull --ff-only; else git clone https://github.com/surahli123/ds-stack ~/ds-stack; fi
cd ~/ds-stack && test -f docs/acceptance.md && git log -1 --format=%H
```

Stop and tell the owner if `docs/acceptance.md` doesn't exist yet. Record the commit hash. Also check that `codex --version` works and that `codex login status` shows a sign-in.

### 2. Hide gold while the agents run

```bash
mv ~/ds-stack/eval/gold ~/ds-gold-hidden
```

Move it back only in step 5, after every agent has finished. If anything stops you early, move it back before you report.

### 3. Run the Codex column, in English and in Chinese

```bash
cd ~/ds-stack && D=$(date +%Y-%m-%d)
python3 eval/run_arms.py --runs 3 --agent-cmd "sh $PWD/eval/agents/codex.sh {prompt_file}" --out eval/results/$D-codex-en
python3 eval/run_arms.py --runs 3 --agent-cmd "sh $PWD/eval/agents/codex.sh {prompt_file}" --prompt-suffix "请用中文写结论。" --out eval/results/$D-codex-zh
```

Each command runs every fixture through three arms (plain prompting, checks only, full ds-mode), 3 times each. Each run's directory keeps `result.md`, `agent.log` (Codex's own log), `queries.log`, `checks.log` and `meta.json`.

### 4. Run the Cursor column, if `cursor-agent` exists

Repeat step 3 with `eval/agents/cursor.sh`, writing to `$D-cursor-en` and `$D-cursor-zh`.

### 5. Restore gold and grade

```bash
mv ~/ds-gold-hidden ~/ds-stack/eval/gold
for R in eval/results/$D-codex-* eval/results/$D-cursor-*; do [ -d "$R" ] && python3 eval/grade.py "$R" --allow-no-transcript; done
```

### 6. Push the results

```bash
git checkout -b results/$D-codex && git add eval/results/$D-* && git commit -m "Acceptance results from Codex/Cursor, $D" && git push -u origin results/$D-codex
```

## Report back

Send the person you work for this, and nothing else:

```
ds-stack acceptance, <date>, commit <hash>
Codex: <version>   Cursor: <version or "not run">
<for each results directory: its Fixtures-by-majority table and the per-arm runs_correct line from summary.md>
Failing runs: <directory/run: the Reason column from summary.md>
Pushed: <branch name>
Problems: <none, or the step, the command and its error>
```
