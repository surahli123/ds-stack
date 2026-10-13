#!/usr/bin/env python3
"""Run one SQL statement through the guarded runner and log it.

    python3 tools/query.py "SELECT ..." [--as-of 2026-10-04] [--params '[...]']
    python3 tools/query.py --pasted --sql "<the SQL that was run>" \
        --columns '["week", "ctr"]' --rows '[["2026-09-21", 0.304]]' [--as-of ...]

Prints one JSON line with the query id (q1, q2, ...), columns and rows, and
appends the statement and its result to .ds-queries.log (or $DS_QUERIES_LOG).
Cite the id in the readout as [q<n>], and pass it to a check as "from": "q<n>".
Use --pasted for a result computed outside this tool, such as SQL a person ran
and pasted back: it gets an id and the same size caps.

This file is the reference adapter. It opens SQLite: --db, else $DS_WAREHOUSE,
else ./warehouse.db. A warehouse adapter replaces connect() and keeps the rest,
log included. Limits and the scratch prefix come from runner.json in
$DS_OVERLAY_DIR when it is set; $DS_RUN_ID names the per-run scratch suffix.

Exit code: 0 ran, 1 blocked or failed (the attempt is still logged), 3 usage error.
"""

import argparse
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import guarded_query as gq  # noqa: E402

DEFAULTS = {"scratch_prefix": "scratch_dsmode_", "per_run_suffix": True, "max_rows": 200,
            "max_cell_chars": 200, "max_result_chars": 20_000, "max_seconds": 120}


def load_config():
    config = dict(DEFAULTS)
    overlay = os.environ.get("DS_OVERLAY_DIR")
    if overlay and os.path.exists(os.path.join(overlay, "runner.json")):
        with open(os.path.join(overlay, "runner.json")) as handle:
            config.update(json.load(handle))
    if config.get("per_run_suffix"):
        config["scratch_prefix"] += os.environ.get("DS_RUN_ID", "run") + "_"
    return config


def connect(args):
    path = args.db or os.environ.get("DS_WAREHOUSE") or "warehouse.db"
    if not os.path.exists(path):
        raise FileNotFoundError(f"no database at {path}; pass --db or set DS_WAREHOUSE")
    return sqlite3.connect(path)


def limits(config, *names):
    return {name: config[name] for name in names}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("statement", nargs="?", help="the SQL statement to run")
    parser.add_argument("--sql", help="the SQL, as an alternative to the positional argument")
    parser.add_argument("--params", default="[]", help="JSON list of query parameters")
    parser.add_argument("--as-of", help="last complete period the result covers, for example 2026-10-04")
    parser.add_argument("--db", help="SQLite file (reference adapter only)")
    parser.add_argument("--pasted", action="store_true", help="log a result computed outside this tool")
    parser.add_argument("--columns", help="with --pasted: JSON list of column names")
    parser.add_argument("--rows", help="with --pasted: JSON list of rows")
    args = parser.parse_args(argv)

    sql = args.sql or args.statement
    if not sql:
        parser.print_usage(sys.stderr)
        return 3
    config = load_config()
    try:
        if args.pasted:
            if args.columns is None or args.rows is None:
                print("--pasted needs --columns and --rows", file=sys.stderr)
                return 3
            entry = gq.log_pasted(sql, json.loads(args.columns), json.loads(args.rows), as_of=args.as_of,
                                  **limits(config, "max_rows", "max_cell_chars", "max_result_chars"))
        else:
            conn = connect(args)
            entry = gq.run_logged(conn, sql, json.loads(args.params), as_of=args.as_of,
                                  scratch_prefix=config["scratch_prefix"],
                                  **limits(config, "max_rows", "max_cell_chars", "max_result_chars", "max_seconds"))
    except ValueError as err:
        print(f"unreadable JSON argument: {err}", file=sys.stderr)
        return 3
    except FileNotFoundError as err:
        print(str(err), file=sys.stderr)
        return 3
    except Exception as err:  # blocked or failed; run_logged already logged it
        last = gq.read_log()[-1:] or [{}]
        print(json.dumps({"id": last[0].get("id"), "status": "blocked" if isinstance(err, gq.Blocked) else "error",
                          "error": str(err)}))
        return 1
    print(json.dumps({key: entry.get(key) for key in ("id", "status", "row_count", "columns", "rows")}, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
