# Private overlay: the contract

The generic core (this repo) holds no company facts. Anything specific to a workplace lives in a **private overlay**: a directory outside every git repo, on the machine where the work happens.

```
~/ds-stack-private/overlay/      # never inside a repo
├── denylist.txt                 # terms that must never be committed (used by hooks/)
├── metrics.json                 # metric definitions the agent reads
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

**metrics.json.** Each metric needs a name, numerator, denominator, filters and an owner. The agent reads this file so that "CTR" means the dashboard's CTR and not one it invented. Keep it as definitions only, with no data.

**runner.json.** Settings for the guarded query runner. A warehouse adapter must keep the same contract as `safety/guarded_query.py`:
- writes only to tables that start with `scratch_prefix`, plus a per-run suffix
- one statement per call
- results of at most `max_rows` rows, `max_cell_chars` per text cell and `max_result_chars` in total, so only aggregates reach the conversation (search logs are untrusted text and can carry prompt injection). The caps reduce raw-text exposure but don't remove it. The structural fix is a warehouse view without free-text columns, granted to the agent's role
- a time cap, plus a bytes-scanned cap where the warehouse supports one
- read-only credentials outside scratch, enforced by the warehouse, not only by the runner

Before any unsupervised session, run the adapter's copy of `safety/selftest.py`. It must exit 0.
