# Prompt: acceptance run, dots's part (Codex on the owner's machine)

You run the Codex column of the ds-stack acceptance matrix on the machine of the person you work for. Claude owns the acceptance doc, the fixtures and every fix (`docs/prompts/acceptance-claude.md`). Your job is to run, grade and report. Don't fix anything.

## Rules

- Synthetic data only. Don't open, query or copy company data, and don't run SMA.
- Don't edit `docs/acceptance.md`, any skill, the grader or the fixtures. If something looks wrong, report it.
- Gold stays hidden while agents run, as step 2 describes.
- Never overwrite a results or report directory. Each run gets a new one; `run_arms.py` refuses an existing run.
- `eval/never_grade.txt` names the contaminated Codex directories, made before commit `1093ca9`; `grade.py` and `acceptance.py` refuse them. Keep them and list them in the report.
- A run that didn't execute (rate-limited, at capacity, not isolated, crashed) is not a result. `acceptance.py` then prints INVALID instead of levels, as for `2026-10-13-2343-codex-*`. Never report `--diagnostic` output as an acceptance result.
- The small validation passed on 2026-10-14 (`results/2026-10-14-1326-codex-validate`), and the owner approved this matrix. Those validation runs used Codex's default effort, so they don't count here.
- Codex runs with the owner's daily model and reasoning effort, from `~/.codex/config.toml` (step 2).
- Push only your results, to a new branch named `results/<date>-<harness>`. Don't merge anything, and don't open a PR unless the owner asks.

## Steps

### 1. Check that it is time to start

```bash
if [ -d ~/ds-stack/.git ]; then git -C ~/ds-stack checkout main && git -C ~/ds-stack pull --ff-only; else git clone https://github.com/surahli123/ds-stack ~/ds-stack; fi
cd ~/ds-stack && test -f docs/acceptance.md && git log -1 --format=%H
```

Stop and tell the owner if `docs/acceptance.md` doesn't exist yet. Record the commit hash. Also check that `codex --version` works and that `codex login status` shows a sign-in.

Each code block below is meant to run as one shell command. Blocks don't share variables, so later blocks read the run id from `~/ds-run-id` and the daily model and effort from `~/ds-codex-pin`.

### 2. Pin the daily model, fix the run id, then hide gold and Codex's global instructions

```bash
for p in ~/ds-run-id ~/ds-codex-pin ~/ds-gold-hidden ~/ds-codex-hidden; do [ -e "$p" ] && { echo "leftover $p from an unfinished run: stop and report"; exit 1; }; done
python3 ~/ds-stack/eval/agents/codex-daily.py > ~/ds-codex-pin || { rm -f ~/ds-codex-pin; echo "no daily model and effort found: stop and ask the owner"; exit 1; }
cat ~/ds-codex-pin
date +%Y-%m-%d-%H%M > ~/ds-run-id && cat ~/ds-run-id
mv ~/ds-stack/eval/gold ~/ds-gold-hidden
mkdir ~/ds-codex-hidden
for f in AGENTS.md AGENTS.override.md skills prompts; do [ -e ~/.codex/$f ] && mv ~/.codex/$f ~/ds-codex-hidden/; done
ls ~/ds-codex-hidden
```

If the first line reports a leftover, stop: an earlier run didn't finish cleanly, and the owner decides what to restore.

`codex-daily.py` prints the `model` and `model_reasoning_effort` from `~/.codex/config.toml`, or from the profile its `profile` line names. If it finds none, ask the owner for the two values and write them to `~/ds-codex-pin` as one line, `<model> <effort>`.

`--ignore-user-config` skips only `config.toml`. Global instructions in `~/.codex` would reach every arm, plain prompting included. Leave `auth.json` and `plugins/` where they are. `eval/agents/codex.sh` also gives Codex an empty `HOME`, so skills in `~/.agents/skills` stay out, and switches off plugins, remote plugins, apps and memories for each run. Codex rebuilds `~/.codex/skills/.system` on its first start; `codex.sh` allows only that folder, and refuses to start Codex (exit 4) if anything else is back.

Then confirm the isolation with one paid call:

```bash
cd ~/ds-stack && read M E < ~/ds-codex-pin && DS_CODEX_MODEL=$M DS_CODEX_EFFORT=$E sh eval/agents/codex-isolation-probe.sh
```

The script prints Codex's two-line reply and the model and effort from Codex's log, then `PASS` or `FAIL`. It fails if Codex didn't run the pinned model and effort. It passes only when every listed skill is one of Codex's six system skills (imagegen, openai-docs, plugin-creator, review-agent, skill-creator, skill-installer) and no instruction file is listed. The model may list fewer; `codex.sh` checks the folder itself on every run. On `FAIL`, run step 5's first block to put everything back, then stop and report the reply.

### 3. Run the Codex column, in English and in Chinese

```bash
cd ~/ds-stack && D=$(cat ~/ds-run-id) && read M E < ~/ds-codex-pin && DS_CODEX_MODEL=$M DS_CODEX_EFFORT=$E python3 eval/run_arms.py --runs 3 --parallel 2 --timeout 1800 --agent-cmd "sh $PWD/eval/agents/codex.sh {prompt_file}" --out eval/results/$D-codex-en; echo "run_arms exit $?"
```

```bash
cd ~/ds-stack && D=$(cat ~/ds-run-id) && read M E < ~/ds-codex-pin && DS_CODEX_MODEL=$M DS_CODEX_EFFORT=$E python3 eval/run_arms.py --runs 3 --parallel 2 --timeout 1800 --agent-cmd "sh $PWD/eval/agents/codex.sh {prompt_file}" --prompt-suffix "请用中文写结论。" --out eval/results/$D-codex-zh; echo "run_arms exit $?"
```

Each command runs every fixture through three arms (plain prompting, checks only, full ds-mode), 3 times each, two at a time. Each run's directory keeps `result.md`, `agent.log` (Codex's own log), `queries.log`, `checks.log` and `meta.json`. A rate-limited or at-capacity run is retried after a pause, and its earlier attempts' logs stay in the run directory. `run-status.json` counts what executed. A higher effort makes runs slower, so the time cap is 30 minutes; a run that hits it still counts, as a miss.

`run_arms exit 0` means every job executed. On `run_arms exit 2`, don't start the Chinese block: go to step 5, and report `run-status.json`.

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
cd ~/ds-stack && D=$(cat ~/ds-run-id) && cat eval/results/$D-codex-en/run-status.json eval/results/$D-codex-zh/run-status.json; for R in eval/results/$D-codex-en eval/results/$D-codex-zh; do python3 eval/grade.py "$R" --allow-no-transcript; done; python3 eval/acceptance.py eval/results/$D-codex-en eval/results/$D-codex-zh --allow-no-transcript; echo "acceptance exit $?"
```

### 6. Push the results

```bash
cd ~/ds-stack && D=$(cat ~/ds-run-id) && git checkout -b results/$D-codex && git add eval/results/$D-codex-* && git commit -m "Acceptance results from Codex, $D" && git push -u origin results/$D-codex && rm ~/ds-run-id ~/ds-codex-pin
```

## Report back

Send the person you work for this, and nothing else:

```
ds-stack acceptance, <date>, commit <hash>
Codex: <version>; pinned: <~/ds-codex-pin>; model and reasoning effort in meta.json: <agent_model and reasoning_effort, and whether every run matches the pin>
run-status.json, per directory: <executed of jobs; failed by kind; not started; stopped>
<the full output of eval/acceptance.py, and its exit code>
<for each results directory: its Fixtures-by-majority table from summary.md>
Failing runs: <directory/run: the Reason column from summary.md>
Pushed: <branch name>
Contaminated earlier directories: <list, or "none">
Hidden from ~/.codex: <what step 2 moved, or "nothing">; isolation probe: <its reply, shortened>
Problems: <none, or the step, the command and its error>
```
