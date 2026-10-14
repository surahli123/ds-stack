# Agent runbook: smoke-test ds-mode with the local Codex

You are an agent running this test on the machine of the person you work for. Follow the steps in order, run each command as written, and stop at the first step that fails. The test uses synthetic data only.

## Rules

- Work only in `~/ds-stack`, `~/ds-skills` and the test directory created in step 4.
- Don't open, query or copy company data, and don't point Codex at any work project.
- Don't push, commit or post anything anywhere.
- Don't read `~/ds-stack/eval/gold/`, and don't let Codex read it. It holds the answers.
- Retry a failed step at most once. If it fails again, stop and report.

## Steps

### 1. Check the tools

`python3 --version` must show 3.9 or later. `git --version` and `codex --version` must both work. Stop if Codex isn't installed or isn't signed in.

### 2. Get the code

```bash
if [ -d ~/ds-stack/.git ]; then git -C ~/ds-stack pull --ff-only; else git clone https://github.com/surahli123/ds-stack ~/ds-stack; fi
```
The repo is private, so cloning needs their GitHub access.

### 3. Install the skill and run the self-test

```bash
mkdir -p ~/ds-skills && rm -rf ~/ds-skills/ds-mode && cp -R ~/ds-stack/skills/ds-mode ~/ds-skills/
python3 ~/ds-stack/safety/selftest.py
```
Every line of the self-test must start with `ok`.

### 4. Run the analysis in Codex

```bash
T=~/ds-test-$(date +%Y%m%d-%H%M%S) && mkdir -p "$T" && cp ~/ds-stack/eval/fixtures/f1/* "$T"/ && cd "$T"
echo "For any data analysis request, read and follow $HOME/ds-skills/ds-mode/SKILL.md" > AGENTS.md
git init -q
codex exec --full-auto --skip-git-repo-check "$(cat task.md)"
```
If Codex rejects a flag, run `codex exec --help` and use its equivalent: the run must let Codex execute commands and write files in `$T`. This step usually takes 1–3 minutes.

### 5. Check the result

```bash
python3 ~/ds-stack/eval/smoke_check.py "$T" --fixture f1
```
The last line is `PASS` or `FAIL`.

### 6. Optional: Cursor

If the `cursor-agent` command exists, repeat steps 4 and 5 in a new directory with `cursor-agent -p --force "$(cat task.md)"` in place of the Codex line. Check `cursor-agent --help` for the flags if needed.

## If it fails

| Failing line | Likely cause | Try once |
|---|---|---|
| `readout.md is missing` | Codex didn't follow the skill to the end | Check that `AGENTS.md` holds an absolute path, then rerun step 4 in a new directory |
| `no logged queries` | Codex queried the database directly | Rerun step 4, adding "Use the skill's tools/query.py for every query." to the end of the prompt |
| `verify_readout: fail` | A number without a tag, or a tag that doesn't resolve | Report it. It is a finding about the skill, not about this machine |
| `answer vs gold` | The analysis reached the wrong answer | Report it, with the Headline line from `readout.md` |

## Report back

Send the person you work for exactly this, with nothing from outside the test directory:

```
ds-stack smoke test, <date>
Codex: <codex --version>   Python: <python3 --version>
Self-test: <ok | the failing line>
<the full output of smoke_check.py>
Cursor: <the same block, or "not run">
Problems: <none, or the step, the command and its error>
```

Test 2, a real question with data from SMA, is for the person to run themselves, not an agent. It is described in `docs/porting.md`.
