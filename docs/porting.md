# Porting the seed to the work laptop

Run part 1 on synthetic data before anything touches company data. Only after it passes do you build part 2. Nothing in this file needs company data to come home: changes flow from this repo to work, never back.

## 1. Smoke test in Codex and Cursor (synthetic data)

Import the `v0.3-seed` tree wherever company code lives, with no remote pointing back to this repo.

1. Safety and unit tests, from the repo root:
   ```bash
   python3 safety/selftest.py        # every line "ok", including the three log assertions
   python3 -m pytest -q              # needs pytest
   ```
2. Load the skill.
   - Cursor reads `.cursor-plugin/plugin.json`, or you can copy `skills/ds-mode/` into its skills directory.
   - Codex can install the plugin, or read `skills/ds-mode/SKILL.md` through an `AGENTS.md` line such as: "For any data analysis request, read and follow skills/ds-mode/SKILL.md".
3. Make a scratch directory, copy `eval/fixtures/f1/warehouse.db` into it, open the agent there, and paste the task in `eval/fixtures/f1/task.md`.
4. Confirm each of these in the agent's run:

| Check | What passing looks like |
|---|---|
| The skill loads | The agent follows the ds-mode method without being told the steps |
| Script paths resolve | It runs `<skill dir>/tools/query.py`; a wrong path shows up as "No such file" |
| Queries are logged | `.ds-queries.log` has one line per statement, with ids q1, q2, … |
| Checks name their source | `.ds-checks.log` lines carry `"from": ["q<n>"]` |
| The readout traces | `python3 <skill dir>/tools/verify_readout.py readout.md` prints `pass` when you run it yourself |
| The answer is right | about 0 pp attributable to the ranker, with mix shift ruled in |
| No filesystem search | The agent doesn't look for `metrics.json` outside `$DS_OVERLAY_DIR` |

5. Optional: run the eval through the agent's headless mode. Check its `--help` for the exact flags.
   ```bash
   DS_AGENT_CMD='codex exec {prompt_file}' python3 eval/run_arms.py --runs 1 --arms full
   python3 eval/grade.py eval/results/<dir> --allow-no-transcript
   ```
   The arm's pointer to the skill goes in both `CLAUDE.md` and `AGENTS.md`. With a custom agent, isolation is reported as unverified, because there is no transcript.

If a check fails because the agent can't call the scripts, strip the skill down to its scripts plus one prompt file and retry once (iteration plan, Step 1).

## 2. Before the first run on company data

Each item is structure, not an instruction to the agent.

| Item | In place when |
|---|---|
| Warehouse adapter | a copy of `skills/ds-mode/tools/query.py` whose `connect()` opens the warehouse. Keep the rest of the runner, the log included. |
| Self-test | the adapter passes its copy of `safety/selftest.py`, log assertions included. |
| Credentials | only the runner process holds the warehouse credential, and it can read and write only to scratch. |
| Data | the agent's role sees a view without free-text columns. Without one, run each query yourself and paste back aggregates with `query.py --pasted`. |
| Tools | web and MCP tools are off in the agent session. |
| No route home | run `make hooks` with a denylist seeded from internal metric and table names, and confirm that a planted term is blocked. |
| Metric adapter | ds-mode's pin-the-metric step reads definitions from the internal metric layer, or from an overlay `metrics.json` generated from it, through `$DS_OVERLAY_DIR`. |

The first real question should be one you answered last month, where the obvious definition gives a different number from the dashboard's. A good result is a readout whose metric comes from the internal layer, with `verify_readout.py` passing and a `Reconciled:` line. Review time is the measure, with a target of under 10 minutes.
