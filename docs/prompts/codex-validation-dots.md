# Prompt: small Codex validation, dots's part, before the next matrix

The ask: check the harness fix with 5 paid Codex calls, once, on the commit the owner names, before any new matrix. Don't run the full matrix. The rules of `docs/prompts/acceptance-dots.md` apply: synthetic data only, no SMA, no edits, gold hidden while agents run, never overwrite a directory.

Why: the Codex attempt 2026-10-13-2343 measured nothing. 137 of its 144 runs died on HTTP 429 or "model at capacity" within seconds. Every run also carried a false "not isolated" warning, because the wrapper flagged the system skills Codex rebuilds in `~/.codex/skills/.system`. Now the wrapper allows only that folder and refuses to start Codex on any other leftover. The runner records whether each run executed, retries rate-limited runs after a pause, stops after repeated failures, and exits 2 when a job didn't execute. The acceptance script prints INVALID instead of levels for such a directory.

## Steps

### V1. Tests and replay (free)

```bash
cd ~/ds-stack && git fetch origin && git checkout <commit the owner names> && python3 -m pytest tests -q | tail -1
cd ~/ds-stack && rm -rf /tmp/ds-replay && mkdir /tmp/ds-replay && git archive origin/results/2026-10-13-2343-codex eval/results | tar -x -C /tmp/ds-replay && python3 eval/acceptance.py /tmp/ds-replay/eval/results/2026-10-13-2343-codex-en /tmp/ds-replay/eval/results/2026-10-13-2343-codex-zh --allow-no-transcript; echo "acceptance exit $?"
```

The second command replays the published attempt from its branch, since checking out the commit removes it from the working tree. Expected: every test passes. Both directories print `INVALID`, the English one with `not_isolated+rate_limited 69, not_isolated 2, not_isolated+capacity 1`, and the exit code is 2.

### V2. What Codex rebuilt last time (free)

```bash
ls -A ~/ds-codex-recreated-2026-10-13-2343/skills ~/ds-codex-recreated-2026-10-13-2343/skills/.system
```

Expected: `skills` holds only `.system`. `.system` holds `.codex-system-skills.marker` and Codex 0.153.4's six system skills: imagegen, openai-docs, plugin-creator, review-agent, skill-creator, skill-installer. Anything else: stop and report it.

### V3. Hide, then probe (1 paid call)

Run step 2 of `acceptance-dots.md` exactly: the leftover guard, `~/ds-run-id`, hiding gold and `~/.codex/{AGENTS.md,AGENTS.override.md,skills,prompts}`, then the probe. Expected: `PASS`. On `FAIL`, restore with step 5's first block and report.

### V4. A real leftover blocks the run (free)

```bash
cd ~/ds-stack && D=$(cat ~/ds-run-id) && mkdir ~/.codex/skills/ds-canary && echo canary > ~/.codex/skills/ds-canary/SKILL.md && python3 eval/run_arms.py --fixtures f5 --arms baseline --runs 1 --agent-cmd "sh $PWD/eval/agents/codex.sh {prompt_file}" --out eval/results/$D-validate-canary; echo "run_arms exit $?"; rm ~/.codex/skills/ds-canary/SKILL.md; rmdir ~/.codex/skills/ds-canary; cat eval/results/$D-validate-canary/f5__baseline__1/agent.log
```

Expected: `run_arms exit 2`, `failed: not_isolated 1`, and an `agent.log` line naming `ds-canary` and saying Codex was not started. The run takes under 2 seconds.

### V5. Four real runs (4 paid calls)

```bash
cd ~/ds-stack && D=$(cat ~/ds-run-id) && python3 eval/run_arms.py --fixtures f1,f6 --arms baseline,full --runs 1 --parallel 2 --agent-cmd "sh $PWD/eval/agents/codex.sh {prompt_file}" --out eval/results/$D-validate-codex; echo "run_arms exit $?"
```

Expected: `run_arms exit 0` and `executed 4 of 4`. No `agent.log` says `not isolated`. Each `meta.json` has `"execution": "ok"`, `agent_model` and `reasoning_effort`.

If runs end `rate_limited` or `capacity` after their retries, the exit is 2: that is a finding, not a failure of the fix. Report the times in `meta.json` and `attempt*.log`.

### V6. Restore, grade, push

Run step 5 of `acceptance-dots.md` (restore, then grade), naming `eval/results/$D-validate-canary` and `eval/results/$D-validate-codex` in place of the two Codex directories. The canary directory grades INVALID, as it should. Levels on these directories are not acceptance results: only execution and Plumbing matter here. Push with step 6, using the branch `results/$D-codex-validate` and `git add eval/results/$D-validate-*`.

## Report back

```
Codex validation, <date>, commit <hash>; Codex <version>; model and effort: <from meta.json>
V1: <tests line>; replay: <the two INVALID lines>; exit <code>
V2: <ls output>
V3: probe <PASS or FAIL, reply shortened>
V4: run_arms exit <code>; <run-status failed>; agent.log: <the line>
V5: run_arms exit <code>; <run-status line>; per run: <fixture arm: execution, seconds, attempts>
Pushed: <branch>
Problems: <none, or the step, the command and its error>
```
