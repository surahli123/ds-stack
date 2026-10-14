# Setting up the seed on the work laptop

You need one folder and one line of config. Data comes through the tools you already have, such as the Search Metric Analyzer (SMA), so no warehouse adapter is needed for testing.

## Set up (about 10 minutes)

1. Copy `skills/ds-mode/` to a place outside every repo, for example `~/ds-skills/ds-mode/`. It runs on Python's standard library, so there is nothing to install. For test 1, also copy the two files in `eval/fixtures/f1/`.
2. In the root of the project you work in (the SMA project, for example), create `AGENTS.md` with one line. Codex and Cursor both read it. Use the absolute path:
   ```
   For any data analysis request, read and follow /Users/<you>/ds-skills/ds-mode/SKILL.md
   ```
   To keep the file out of that project's git, add `AGENTS.md` to `.git/info/exclude`.
3. Optional: write the definitions of 2-3 metrics you use often into `~/ds-overlay/metrics.json`, giving numerator, denominator, filters, grain and source for each, then `export DS_OVERLAY_DIR=~/ds-overlay`. Without it, ds-mode still runs and labels the definition `[guess]`.

## Test 1: synthetic data (about 5 minutes, no company data)

To have an agent run this test and report back, give it [`agent-runbook.md`](agent-runbook.md).

```bash
mkdir /tmp/ds-test && cp <ds-stack>/eval/fixtures/f1/* /tmp/ds-test/ && cd /tmp/ds-test
echo "For any data analysis request, read and follow /Users/<you>/ds-skills/ds-mode/SKILL.md" > AGENTS.md
```

Open Codex or Cursor in that directory and paste in the text of `task.md`. It passes when:

- the answer is about 0 pp, with mix shift (mobile's share rising) as the cause;
- `.ds-queries.log`, `.ds-checks.log` and `readout.md` appear in the directory;
- `python3 ~/ds-skills/ds-mode/tools/verify_readout.py readout.md`, run by you, prints `pass`.

When it fails, the usual cause is a script path the agent can't resolve. Check that `AGENTS.md` uses an absolute path.

## Test 2: a real question, with data from SMA

In the SMA project, ask a question you answered last month. Pick one where the obvious metric definition gives a different number from the dashboard's. Add this line to the prompt:

> Get the data through SMA as usual, and log each result with ds-mode's `query.py --pasted`.

Each SMA result then gets an id (q1, q2, ...), and the checks and `verify_readout.py` work as usual. It passes when:

- `verify_readout.py` prints `pass`;
- you can check the readout in under 10 minutes;
- the number matches your answer from last month, or the readout explains the difference.

To gather evidence for the SMA rethink, run the same question with SMA alone and then with SMA plus ds-mode. Compare the review time, and whether either run caught something you missed.

## Later, before any unattended run on company data

Only then add the structural pieces:

- a warehouse adapter (a copy of `tools/query.py` whose `connect()` opens the warehouse), passing its copy of `safety/selftest.py`;
- a warehouse credential held only by that runner, with writes limited to scratch;
- a view without free-text columns;
- web and MCP tools off;
- the denylist hook (`make hooks`) in any repo that holds the work copy.
