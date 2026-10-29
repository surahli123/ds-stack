#!/usr/bin/env python3
"""Print the model and reasoning effort the owner uses day to day in Codex, read from $CODEX_HOME/config.toml.

    python3 eval/agents/codex-daily.py    # prints "<model> <effort>", or exits 1 saying what is missing

Reads the top-level `model` and `model_reasoning_effort`. When a top-level `profile` names a
`[profiles.<name>]` table, that table's values win. codex.sh runs Codex with --ignore-user-config, so the eval
uses Codex's defaults unless DS_CODEX_MODEL and DS_CODEX_EFFORT carry these two values. Reads nothing else from
the file. Needs no TOML library, because the system Python on macOS has none.
"""

import os
import re
import sys

KEY = re.compile(r"""^\s*([A-Za-z0-9_-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')\s*(?:#.*)?$""")
TABLE = re.compile(r"^\s*\[([^\[\]]+)\]\s*(?:#.*)?$")


def tables(text):
    """String values per table: {"": top level, "profiles.daily": {...}, ...}."""
    found, current = {"": {}}, ""
    for line in text.splitlines():
        if line.lstrip().startswith("[["):
            current = None  # an array of tables holds nothing we read
            continue
        table = TABLE.match(line)
        if table:
            current = table.group(1).strip().replace('"', "").replace("'", "")
            found.setdefault(current, {})
            continue
        key = KEY.match(line)
        if key and current is not None:
            found[current][key.group(1)] = key.group(2) if key.group(2) is not None else key.group(3)
    return found


def daily(text):
    """(model, effort) from config.toml's text; either may be None."""
    found = tables(text)
    values = dict(found[""])
    if values.get("profile"):
        values.update(found.get(f"profiles.{values['profile']}", {}))
    return values.get("model"), values.get("model_reasoning_effort")


def main():
    home = os.environ.get("CODEX_HOME") or os.path.join(os.path.expanduser("~"), ".codex")
    path = os.path.join(home, "config.toml")
    if not os.path.exists(path):
        print(f"codex-daily: {path} doesn't exist, so ask the owner for the model and the effort", file=sys.stderr)
        return 1
    with open(path, encoding="utf-8") as handle:
        model, effort = daily(handle.read())
    missing = [name for name, value in (("model", model), ("model_reasoning_effort", effort)) if not value]
    if missing:
        print(f"codex-daily: {path} sets no {' and no '.join(missing)}, so ask the owner", file=sys.stderr)
        return 1
    print(model, effort)
    return 0


if __name__ == "__main__":
    sys.exit(main())
