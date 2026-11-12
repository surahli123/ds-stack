# Private overlay: the contract

The generic core (this repo) holds no company facts. Anything specific to a workplace lives in a **private overlay**: a directory outside every git repo, on the machine where the work happens.

```
~/ds-stack-private/overlay/      # never inside a repo
├── denylist.txt                 # terms that must never be committed (used by hooks/)
├── metrics.json                 # metric definitions the agent reads
├── tables.json                  # notes on the tables the work reads (grain, keys, completeness)
├── reviewers.json               # reviewer CLIs ds-interrogate may run
└── runner.json                  # safety-envelope settings for the guarded query runner
```

Set it up:

```bash
mkdir -p ~/ds-stack-private && cp -r overlay.example ~/ds-stack-private/overlay
export DS_OVERLAY_DIR=~/ds-stack-private/overlay   # add to your shell profile
git config core.hooksPath .githooks                 # in this repo: enables the denylist hook
```

## What each file must provide

**denylist.txt.** One term per line; `#` starts a comment. Use it for project codenames, internal metric and table names, and team names. Matching is case-insensitive substring. The pre-commit and pre-push hooks block any added line that contains a term. With no denylist configured the hooks block everything (fail-closed). A machine that never holds work material can opt out explicitly with `DS_DENYLIST=none`.

**metrics.json.** Each metric needs a name, numerator, denominator, filters, grain, source and an owner. Add `verified` (when and how the definition was reconciled with the dashboard), `pitfalls` (traps a newcomer falls into) and `aliases` (other names people use, such as "点击率", so ds-verify can match a request to the entry). Write the numerator, denominator and filters as the column names and expressions the agent will write, because ds-verify looks for them in the readout's Metric line. The agent reads this file so that "CTR" means the dashboard's CTR and not one it invented. Write each entry yourself and verify it against data. Don't let an agent draft it, because a wrong definition here becomes every later answer. Keep it as definitions only, with no data.

**tables.json.** Notes on the tables the work reads, one entry per table: `grain`, `keys`, `complete_when` (when a day's data is complete), `owner` and `pitfalls` (backfills, duplicates, late data). ds-ready lists the tables past analyses used that have no entry. Write each entry yourself, like metrics.json.

**reviewers.json.** The reviewer agents ds-interrogate may run, in order of preference. Each entry gives a model family (`gpt`, `claude`, `grok`, ...), a model (`-` for the CLI's own default) and a command; `{tools}` is the skill's `tools/` folder. List only CLIs approved for company data. For Cursor, add an entry with the family of the model and `["sh", "{tools}/reviewers/cursor.sh", "<model slug>", "{prompt_file}"]`, using a slug from Cursor's model list.

**runner.json.** Settings for the guarded query runner. A warehouse adapter must keep the same contract as `safety/guarded_query.py`:
- writes only to tables that start with `scratch_prefix`, plus a per-run suffix
- one statement per call
- results of at most `max_rows` rows, `max_cell_chars` per text cell and `max_result_chars` in total, so only aggregates reach the conversation (search logs are untrusted text and can carry prompt injection). The caps reduce raw-text exposure but don't remove it. The structural fix is a warehouse view without free-text columns, granted to the agent's role
- a time cap, plus a bytes-scanned cap where the warehouse supports one
- read-only credentials outside scratch, enforced by the warehouse, not only by the runner, and held only by the runner process
- a log line for every statement, whether it ran, was blocked or failed: an id (`q1`, `q2`, ...), the SQL, parameters, as-of period, row count, time taken and the capped result rows, written to `.ds-queries.log` or `$DS_QUERIES_LOG`. Results computed outside the runner enter the same log through the pasted path. Readouts cite these ids and `verify_readout.py` resolves them, so an adapter without the log breaks review. The log holds SQL with table names, so keep it out of every repo

The reference adapter is `skills/ds-mode/tools/query.py` over `skills/ds-mode/tools/guarded_query.py` (SQLite). A warehouse adapter replaces its `connect()` and keeps the rest. Before any unsupervised session, run the adapter's copy of `safety/selftest.py`, including its log assertions. It must exit 0.
