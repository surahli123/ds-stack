---
name: ds-ready
description: >-
  Use before ds-stack runs on a new work project, and again whenever readouts
  fall back to [guess] definitions: "is this project ready for ds-stack", "set
  up ds-stack here", "audit the overlay", "what's missing for ds-mode",
  "检查这个项目能不能用 ds-stack", "帮我准备 ds-stack 的配置". Audits the
  private overlay, the data sources, the project's AGENTS.md and the tables and
  metrics past analyses used; lists the gaps; and writes questions for each
  metric owner. It never writes a metric definition. Also runs on /ds-ready.
---

# ds-ready

ds-mode can only be as right as the definitions it reads. This skill checks that a work project gives it what it needs: the team's metric definitions, notes on the tables, the runner and reviewer settings, and an AGENTS.md that loads ds-mode. It lists what is missing and writes the questions that get it filled in. People write the answers; this skill never drafts a definition.

## Steps

1. Run the audit from the project folder, with the overlay in `$DS_OVERLAY_DIR`:

   ```bash
   python3 <skills>/ds-ready/tools/audit.py --db <warehouse.db>
   ```

   `--db` (else `$DS_WAREHOUSE`) checks each metric's source table and columns through the SQLite reference adapter. A warehouse port replaces `table_columns()` in `tools/audit.py`; without either, the source check is skipped. `--project <folder>` audits another folder. The questions go to `<project>/ds-ready/`, or to an empty `--out`; the audit refuses a folder that holds anything else. `--json` writes the report wherever you point it, outside that folder's `.gitignore`.
2. Read the first line: `ready` or `not ready`, with the count of blocking and recommended gaps and the number of past query logs and readouts it read.
3. Fix the blocking gaps first:
   - a missing or invalid overlay or metrics.json;
   - a metric without numerator, denominator, filters, grain, source or owner;
   - a source table or column the database doesn't have;
   - an AGENTS.md that doesn't load ds-mode;
   - a metric the readouts kept defining for themselves.
4. Send each `ds-ready/questions-<owner>.md` to that owner. A person on the team writes the answers into the overlay's `metrics.json` and `tables.json`. Don't let an agent draft them: a wrong definition becomes every later answer.
5. Run the audit again until it says `ready`, then run test 1 of `docs/porting.md`.

## What it checks

| Area | Blocking when | Recommended when |
|---|---|---|
| Overlay | `DS_OVERLAY_DIR` is unset, the folder is missing, or metrics.json is missing or invalid | runner.json, reviewers.json or denylist.txt is missing, or the denylist is empty |
| Metrics | An entry lacks a field, has an empty or wrongly typed one, or sets `available` to anything but true or false | It lacks `verified`, `pitfalls` or `aliases`, or its numerator reads like prose |
| Data (`--db`) | The database can't be read, a source doesn't exist, or a numerator or denominator names a missing column | A filter names something that isn't a column (quote it if it is a value) |
| Playbook | AGENTS.md is missing, or doesn't point to an existing ds-mode SKILL.md | Its ds-verify path is missing or stale, or readouts wrote their own version of a metric the overlay defines |
| Tables | tables.json is invalid | A table in past query logs has no grain, keys, `complete_when`, owner or pitfalls in tables.json |
| Past readouts | Two or more readouts defined the same metric themselves ([guess]), and metrics.json lacks it | One readout did |
| Scan | It stopped at `--max-files` (default 5000) readouts and logs, so some were missed | |

Paths in AGENTS.md may use `~`, `$HOME` or a path relative to the project; one inside an HTML comment doesn't count. Readouts that define one metric in different words are grouped by the columns they use.

The questions name internal metrics and tables, so a folder the audit creates gets a `.gitignore`. Exit code: 0 ready, 1 not ready, 3 a usage or internal error.
