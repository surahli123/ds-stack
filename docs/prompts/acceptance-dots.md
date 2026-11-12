# Prompt: acceptance run, dots's part (Codex on the owner's machine)

You run the Codex column of the ds-stack acceptance matrix on the machine of the person you work for. Claude owns the acceptance doc, the fixtures and every fix (`docs/prompts/acceptance-claude.md`). Your job is to run, grade and report. Don't fix anything.

## Rules

- Synthetic data only. Don't open, query or copy company data, and don't run SMA.
- Don't edit `docs/acceptance.md`, any skill, the grader or the fixtures. If something looks wrong, report it.
- Run from `~/ds-accept`, a worktree of its own at `origin/main`. Never run from a checkout with uncommitted changes, and never switch branches in another checkout.
- Gold stays hidden while agents run, every copy on the machine, as step 2 describes.
- Never overwrite a results or report directory. Each run gets a new one; `run_arms.py` refuses an existing run.
- `eval/never_grade.txt` names the contaminated Codex directories, made before commit `1093ca9`; `grade.py` and `acceptance.py` refuse them. Keep them and list them in the report.
- A run that didn't execute (rate-limited, at capacity, not isolated, crashed) is not a result. `acceptance.py` then prints INVALID instead of levels, as for `2026-10-13-2343-codex-*`. Never report `--diagnostic` output as an acceptance result.
- The small validation passed on 2026-10-14 (`results/2026-10-14-1326-codex-validate`), and the owner approved this matrix. Those validation runs used Codex's default effort, so they don't count here.
- Codex runs with the owner's daily model and reasoning effort, from `~/.codex/config.toml` (step 2).
- Push only your results, to a new branch named `results/<date>-<harness>`. Don't merge anything, and don't open a PR unless the owner asks.

## Steps

### 1. Check that it is time to start

```bash
if [ -e ~/ds-accept ]; then
  [ -z "$(git -C ~/ds-accept status --porcelain)" ] || { echo "~/ds-accept has uncommitted changes: stop and report"; exit 1; }
  git -C ~/ds-accept fetch origin && git -C ~/ds-accept checkout --detach origin/main
elif [ -d ~/ds-stack/.git ]; then
  git -C ~/ds-stack fetch origin && git -C ~/ds-stack worktree add --detach ~/ds-accept origin/main
else
  git clone https://github.com/surahli123/ds-stack ~/ds-accept
fi
cd ~/ds-accept && test -f docs/acceptance.md && git log -1 --format=%H
```

The worktree leaves `~/ds-stack` and its branches as they are. Stop and tell the owner if `docs/acceptance.md` doesn't exist yet. Record the commit hash. Also check that `codex --version` works and that `codex login status` shows a sign-in.

Then check that step 6 will be able to push. On 2026-11-02 the push failed at the end ("could not read Username"; `gh` returned 401):

```bash
gh auth status && git -C ~/ds-accept push --dry-run origin HEAD:refs/heads/results/push-check 2>&1 | tail -1
```

If either fails, stop before any paid call. Ask the owner to run `gh auth login` and then `gh auth setup-git`, and check again.

Each code block below is meant to run as one shell command. Blocks don't share variables, so later blocks read the run id from `~/ds-run-id` and the daily model and effort from `~/ds-codex-pin`.

### 2. Pin the daily model, fix the run id, then hide gold and Codex's global instructions

First list every copy of the answers on the machine, without moving anything, and report the list:

```bash
find ~ -path "$HOME/Library" -prune -o -type d -path '*/eval/gold' -print 2>/dev/null
```

If a listed copy is in a checkout that another session is using right now, stop and ask the owner. Otherwise:

```bash
for p in ~/ds-run-id ~/ds-codex-pin ~/ds-gold-hidden ~/ds-gold-hidden-extra ~/ds-codex-hidden; do [ -e "$p" ] && { echo "leftover $p from an unfinished run: stop and report"; exit 1; }; done
python3 ~/ds-accept/eval/agents/codex-daily.py > ~/ds-codex-pin || { rm -f ~/ds-codex-pin; echo "no daily model and effort found: stop and ask the owner"; exit 1; }
cat ~/ds-codex-pin
date +%Y-%m-%d-%H%M > ~/ds-run-id && cat ~/ds-run-id
mv ~/ds-accept/eval/gold ~/ds-gold-hidden
mkdir ~/ds-gold-hidden-extra && n=0
find ~ -path "$HOME/Library" -prune -o -path "$HOME/ds-gold-hidden*" -prune -o -type d -path '*/eval/gold' -print 2>/dev/null | while IFS= read -r g; do
  n=$((n + 1)); mv "$g" ~/ds-gold-hidden-extra/$n && echo "$g -> $HOME/ds-gold-hidden-extra/$n" >> ~/ds-gold-hidden-extra/moves.txt
done
cat ~/ds-gold-hidden-extra/moves.txt 2>/dev/null
mkdir ~/ds-codex-hidden
for f in AGENTS.md AGENTS.override.md skills prompts; do [ -e ~/.codex/$f ] && mv ~/.codex/$f ~/ds-codex-hidden/; done
ls ~/ds-codex-hidden
```

If the first line reports a leftover, stop: an earlier run didn't finish cleanly, and the owner decides what to restore.

`codex-daily.py` prints the `model` and `model_reasoning_effort` from `~/.codex/config.toml`, or from the profile its `profile` line names. If it finds none, ask the owner for the two values and write them to `~/ds-codex-pin` as one line, `<model> <effort>`.

`--ignore-user-config` skips only `config.toml`. Global instructions in `~/.codex` would reach every arm, plain prompting included. Leave `auth.json` and `plugins/` where they are. `eval/agents/codex.sh` also gives Codex an empty `HOME`, so skills in `~/.agents/skills` stay out, and switches off plugins, remote plugins, apps and memories for each run. Codex rebuilds `~/.codex/skills/.system` on its first start; `codex.sh` allows only that folder, and refuses to start Codex (exit 4) if anything else is back.

Then confirm the isolation with one paid call:

```bash
cd ~/ds-accept && read M E < ~/ds-codex-pin && DS_CODEX_MODEL=$M DS_CODEX_EFFORT=$E sh eval/agents/codex-isolation-probe.sh
```

The script prints Codex's two-line reply and the model and effort from Codex's log, then `PASS` or `FAIL`. It fails if Codex didn't run the pinned model and effort. It passes only when every listed skill is one of Codex's six system skills (imagegen, openai-docs, plugin-creator, review-agent, skill-creator, skill-installer) and no instruction file is listed. The model may list fewer; `codex.sh` checks the folder itself on every run. On `FAIL`, run step 5's first block to put everything back, then stop and report the reply.

### 3. Run a quick check of f1 and f3, then the Codex column

The fixes in 0.7.0 and 0.8.0 target the two fixtures Codex missed on 2026-11-02. Check them first: 12 runs of the full arm, f1 and f3, 3 runs each, in both languages.

```bash
cd ~/ds-accept && D=$(cat ~/ds-run-id) && read M E < ~/ds-codex-pin && for L in en zh; do S=""; [ $L = zh ] && S="请用中文写结论。"; DS_CODEX_MODEL=$M DS_CODEX_EFFORT=$E python3 eval/run_arms.py --fixtures f1,f3 --arms full --runs 3 --parallel 2 --timeout 1800 --agent-cmd "sh $PWD/eval/agents/codex.sh {prompt_file}" --prompt-suffix "$S" --out eval/results/$D-codex-quick-$L; c=$?; echo "run_arms $L exit $c"; [ $c = 0 ] || break; done
```

This is round 1. Go straight to step 5 (restore and grade) and step 6 (push), which also clears the run id. Go on only if, on both f1 and f3 and in both languages, the full arm is right in at least 2 of 3 runs. Then start round 2 at step 1, which puts `~/ds-accept` back on `origin/main`, with a new run id and a new probe. In round 2, run the two blocks below instead of this one. Otherwise stop and report. The quick check isn't an acceptance result; only round 2 is.

```bash
cd ~/ds-accept && D=$(cat ~/ds-run-id) && read M E < ~/ds-codex-pin && DS_CODEX_MODEL=$M DS_CODEX_EFFORT=$E python3 eval/run_arms.py --runs 3 --parallel 2 --timeout 1800 --agent-cmd "sh $PWD/eval/agents/codex.sh {prompt_file}" --out eval/results/$D-codex-en; echo "run_arms exit $?"
```

```bash
cd ~/ds-accept && D=$(cat ~/ds-run-id) && read M E < ~/ds-codex-pin && DS_CODEX_MODEL=$M DS_CODEX_EFFORT=$E python3 eval/run_arms.py --runs 3 --parallel 2 --timeout 1800 --agent-cmd "sh $PWD/eval/agents/codex.sh {prompt_file}" --prompt-suffix "请用中文写结论。" --out eval/results/$D-codex-zh; echo "run_arms exit $?"
```

Each command runs every fixture through three arms (plain prompting, checks only, full ds-mode), 3 times each, two at a time. Each run's directory keeps `result.md`, `agent.log` (Codex's own log), `queries.log`, `checks.log` and `meta.json`. A rate-limited or at-capacity run is retried after a pause, and its earlier attempts' logs stay in the run directory. `run-status.json` counts what executed. A higher effort makes runs slower, so the time cap is 30 minutes; a run that hits it still counts, as a miss.

`run_arms exit 0` means every job executed. On `run_arms exit 2`, don't start the Chinese block: go to step 5, and report `run-status.json`.

### 4. Don't run Cursor

The Cursor column isn't run this round.

### 5. Restore everything, then grade

Restore first, also when you stop early. Codex rebuilds `~/.codex/skills` (its system skills) on every run, so the rebuilt copy moves to `~/ds-codex-recreated-<run id>`, kept, before the original goes back:

```bash
D=$(cat ~/ds-run-id 2>/dev/null || date +%Y-%m-%d-%H%M)
[ -e ~/ds-accept/eval/gold ] || mv ~/ds-gold-hidden ~/ds-accept/eval/gold
if [ -f ~/ds-gold-hidden-extra/moves.txt ]; then
  while IFS= read -r line; do src=${line%% -> *}; dst=${line##* -> }; [ -e "$src" ] || mv "$dst" "$src"; done < ~/ds-gold-hidden-extra/moves.txt
fi
if ls ~/ds-gold-hidden-extra 2>/dev/null | grep -qv '^moves.txt$'; then echo "gold copies are still in ~/ds-gold-hidden-extra: report"; else rm -f ~/ds-gold-hidden-extra/moves.txt; rmdir ~/ds-gold-hidden-extra 2>/dev/null; fi
for f in ~/ds-codex-hidden/* ~/ds-codex-hidden/.[!.]*; do
  [ -e "$f" ] || continue; n=$(basename "$f")
  if [ -e ~/.codex/"$n" ]; then mkdir -p ~/ds-codex-recreated-$D && mv ~/.codex/"$n" ~/ds-codex-recreated-$D/; fi
  mv "$f" ~/.codex/
done; rmdir ~/ds-codex-hidden
ls ~/ds-accept/eval/gold ~/.codex ~/ds-codex-recreated-$D 2>/dev/null
```

Then grade:

```bash
cd ~/ds-accept && D=$(cat ~/ds-run-id) && for R in eval/results/$D-codex-*; do cat "$R/run-status.json"; python3 eval/grade.py "$R" --allow-no-transcript; done; if [ -d eval/results/$D-codex-en ]; then python3 eval/acceptance.py eval/results/$D-codex-en eval/results/$D-codex-zh --allow-no-transcript; echo "acceptance exit $?"; fi
```

### 6. Push the results

```bash
cd ~/ds-accept && D=$(cat ~/ds-run-id) && git checkout -b results/$D-codex && git add eval/results/$D-codex-* && git commit -m "Acceptance results from Codex, $D" && git push -u origin results/$D-codex && rm ~/ds-run-id ~/ds-codex-pin
```

## Report back

Send the person you work for this, and nothing else:

```
ds-stack acceptance, <date>, commit <hash>
Quick check (f1, f3, full arm): <for each quick directory: its Fixtures-by-majority table>; matrix run: <yes, or no and why>
Codex: <version>; pinned: <~/ds-codex-pin>; model and reasoning effort in meta.json: <agent_model and reasoning_effort, and whether every run matches the pin>
run-status.json, per directory: <executed of jobs; failed by kind; not started; stopped>
<the full output of eval/acceptance.py, and its exit code>
<for each results directory: its Fixtures-by-majority table from summary.md>
Failing runs: <directory/run: the Reason column from summary.md>
Pushed: <branch name>
Contaminated earlier directories: <list, or "none">
Gold copies hidden: <the moves.txt lines, or "only ~/ds-accept">; hidden from ~/.codex: <what step 2 moved, or "nothing">; isolation probe: <its reply, shortened>
Problems: <none, or the step, the command and its error>
```
