# Agent runbook: smoke-test ds-stack with the local Codex

You are an agent running this test on the machine of the person you work for. Follow the steps in order, run each command as written, and stop at the first step that fails. The test uses synthetic data only.

To start it, the person tells Codex: "Clone or update github.com/surahli123/ds-stack into ~/ds-stack, then read and follow ~/ds-stack/docs/agent-runbook.md."

## Rules

- Synthetic data only. Don't open, query or copy company data, and don't point Codex at any work project.
- Work only in `~/ds-stack`, `~/ds-skills` and the test directories created below.
- Don't commit, push or post anything anywhere.
- Don't read `~/ds-stack/eval/gold/`, and don't let the test runs read it. It holds the answers; only `smoke_check.py` reads it.
- Retry a failed step at most once. If it fails again, stop and report.
- `git clone`, `git pull` and the inner `codex exec` need the network. If your sandbox blocks them, ask the person to approve those commands; approve nothing else outside the sandbox.

## Steps

### 1. Check the tools

`python3 --version` must show 3.9 or later. `git --version`, `codex --version` and `codex login status` must all work. Stop if Codex isn't installed or isn't signed in.

### 2. Get the code

```bash
if [ -d ~/ds-stack/.git ]; then git -C ~/ds-stack pull --ff-only; else git clone https://github.com/surahli123/ds-stack ~/ds-stack; fi
git -C ~/ds-stack log -1 --format=%h
```

Cloning needs the person's GitHub access. Record the commit. If the pull fails because `~/ds-stack` has local changes, stop and report; don't discard them.

### 3. Install the skills side by side and run the self-test

```bash
mkdir -p ~/ds-skills && for s in ds-mode ds-verify ds-interrogate ds-ready; do
  [ -e ~/ds-skills/$s ] && mv ~/ds-skills/$s ~/ds-skills/$s.bak-$(date +%Y%m%d-%H%M%S)
  cp -R ~/ds-stack/skills/$s ~/ds-skills/
done
python3 ~/ds-stack/safety/selftest.py
```

Every line of the self-test must start with `ok`. An existing skill folder is moved aside, never deleted. The skills must sit side by side: ds-mode's last step runs ds-verify from `../ds-verify`, and ds-verify, ds-interrogate and ds-ready use ds-mode's tools.

### 4. Run f1 in a fresh Codex run

f1 is a mix-shift trap: CTR fell after a ranker launch, but the drop comes from more mobile traffic.

```bash
T=~/ds-test-f1-$(date +%Y%m%d-%H%M%S) && mkdir -p "$T" && cp ~/ds-stack/eval/fixtures/f1/task.md ~/ds-stack/eval/fixtures/f1/warehouse.db "$T"/ && cd "$T"
echo "For any data analysis request, read and follow $HOME/ds-skills/ds-mode/SKILL.md" > AGENTS.md
git init -q
codex exec --sandbox workspace-write -c 'approval_policy="never"' --skip-git-repo-check "$(cat task.md)"; echo "codex exit $?"
echo "$T"
```

These are the Codex 0.166 flags. If Codex rejects one, run `codex exec --help` and use its equivalent: the run must execute commands and write files in `$T` without asking. Codex needs a writable home directory, so it can't start on a read-only machine image. The run usually takes a few minutes.

### 5. Check f1

Use the directory step 4 printed:

```bash
T=<the f1 directory>
python3 ~/ds-stack/eval/smoke_check.py "$T" --fixture f1
grep -E "^Headline|^- (Observed|Adjusted|Causal effect)|Verified" "$T/readout.md"
```

It passes when `smoke_check.py` ends with `PASS` and the `Verified` line ends with `ds-verify: pass`. The right answer is an Adjusted change of about 0 pp, with `Causal effect: not identified`.

### 6. Run and check f6, with the team's metric definition

f6's team defines CTR differently from the obvious formula, in a `metrics.json` overlay that only `$DS_OVERLAY_DIR` names.

```bash
T6=~/ds-test-f6-$(date +%Y%m%d-%H%M%S) && mkdir -p "$T6" && cp ~/ds-stack/eval/fixtures/f6/task.md ~/ds-stack/eval/fixtures/f6/warehouse.db "$T6"/ && cd "$T6"
echo "For any data analysis request, read and follow $HOME/ds-skills/ds-mode/SKILL.md" > AGENTS.md
git init -q
DS_OVERLAY_DIR=$HOME/ds-stack/eval/fixtures/f6/overlay codex exec --sandbox workspace-write -c 'approval_policy="never"' --skip-git-repo-check "$(cat task.md)"; echo "codex exit $?"
python3 ~/ds-stack/eval/smoke_check.py "$T6" --fixture f6
grep -E "^Headline|^- (Observed|Adjusted|Causal effect)|Verified" "$T6/readout.md"
```

It passes on the same terms. The right answer is about 50.05%; 46.05% means the run used the obvious formula instead of the team's.

### 7. Optional: Cursor

If the `cursor-agent` command exists, repeat steps 4 and 5 in a new directory with `cursor-agent -p --force "$(cat task.md)"` in place of the Codex line. Check `cursor-agent --help` for the flags if needed.

## If it fails

| Failing line | Likely cause | Try once |
|---|---|---|
| `readout.md is missing` | Codex didn't follow the skill to the end | Check that `AGENTS.md` holds an absolute path, then rerun the step in a new directory |
| `no logged queries` | Codex queried the database directly | Rerun the step, adding "Use the skill's tools/query.py for every query." to the end of the prompt |
| No `ds-verify:` on the `Verified` line | ds-verify isn't next to ds-mode, so the last step skipped it | Check that `~/ds-skills/ds-verify/tools/ds_verify.py` exists, then rerun |
| `verify_readout: fail` | A number without a tag, or a tag that doesn't resolve | Report it. It is a finding about the skill, not about this machine |
| `answer vs gold` | The analysis reached the wrong answer | Report it, with the Headline and estimate lines from `readout.md` |
| f6 answer near 46.05% | The run didn't read the overlay | Check that the command set `DS_OVERLAY_DIR` and that `$DS_OVERLAY_DIR/metrics.json` exists, then rerun |
| `none of the ... alternative lines says 'ruled in' or 'ruled out'` | The readout translated the fixed English words | Report it. The skill asks for those words in English |

## Report back

Send the person you work for exactly this, with nothing from outside the test directories:

```
ds-stack smoke test, <date>, commit <hash>
Codex: <codex --version>   Python: <python3 --version>
Self-test: <ok | the failing line>
f1: <the full output of smoke_check.py>
    <the grep lines>
f6: <the full output of smoke_check.py>
    <the grep lines>
Cursor: <the same block, or "not run">
Problems: <none, or the step, the command and its error>
```

Test 2, a real question with data from SMA, is for the person to run themselves, not an agent. It is described in `docs/porting.md`.
