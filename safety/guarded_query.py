"""Reference guarded query runner: the safety envelope for live, unsupervised runs.

The overlay contract requires every agent query to go through a runner like
this one. It enforces four rules no matter what the agent was told:

1. Writes go only to tables whose name starts with the run's scratch prefix.
2. One statement per call (no smuggled second statement).
3. Results are aggregates: more than `max_rows` rows is refused.
4. A query that runs longer than `max_seconds` is aborted.

This reference implementation speaks DB-API with SQLite. A warehouse adapter in
the private overlay must keep the same contract, using native controls where
they exist, such as read-only roles or a cap on bytes scanned.
"""

import re
import sqlite3
import time

WRITE_KEYWORDS = {"insert", "update", "delete", "create", "drop", "alter", "replace", "merge", "truncate", "attach", "pragma", "vacuum"}
READ_KEYWORDS = {"select", "with", "explain"}
TARGET = re.compile(
    r"^\s*(?:insert\s+(?:or\s+\w+\s+)?into|update(?:\s+or\s+\w+)?|delete\s+from|replace\s+into|merge\s+into|truncate(?:\s+table)?"
    r"|create\s+(?:temp(?:orary)?\s+)?(?:table|view|index)(?:\s+if\s+not\s+exists)?"
    r"|drop\s+(?:table|view|index)(?:\s+if\s+exists)?|alter\s+table)\s+[\"`\[]?([\w.]+)",
    re.I,
)


class Blocked(Exception):
    """The query broke the safety envelope and was not run."""


def _strip_comments(sql):
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    return re.sub(r"--[^\n]*", " ", sql)


def classify(sql, scratch_prefix):
    """Return 'read' or 'scratch_write', or raise Blocked."""
    body = _strip_comments(sql).strip().rstrip(";").strip()
    if not body:
        raise Blocked("empty statement")
    if ";" in body:
        raise Blocked("one statement per call")
    keyword = body.split(None, 1)[0].lower()
    if keyword in READ_KEYWORDS:
        if keyword == "with" and re.search(r"\b(insert|update|delete|create|drop|alter|replace|merge|truncate|attach)\b", body, re.I):
            raise Blocked("data-modifying CTEs are not allowed")
        if re.search(r"\binto\b", body, re.I):
            raise Blocked("SELECT ... INTO creates a table; write to scratch with CREATE TABLE instead")
        return "read"
    if keyword not in WRITE_KEYWORDS:
        raise Blocked(f"statement type '{keyword}' is not allowed")
    match = TARGET.match(body)
    if not match:
        raise Blocked(f"'{keyword}' is not allowed")
    table = match.group(1).split(".")[-1]
    if not scratch_prefix or not table.lower().startswith(scratch_prefix.lower()):
        raise Blocked(f"write to '{table}' is outside the scratch prefix '{scratch_prefix}'")
    return "scratch_write"


def run(conn, sql, params=(), *, scratch_prefix, max_rows=200, max_seconds=60.0):
    kind = classify(sql, scratch_prefix)
    deadline = time.monotonic() + max_seconds
    if isinstance(conn, sqlite3.Connection):
        conn.set_progress_handler(lambda: 1 if time.monotonic() > deadline else 0, 10_000)
    try:
        cursor = conn.execute(sql, params)
        if kind == "scratch_write":
            conn.commit()
            return []
        rows = cursor.fetchmany(max_rows + 1)
    except sqlite3.OperationalError as err:
        if "interrupted" in str(err):
            raise Blocked(f"query exceeded {max_seconds}s") from err
        raise
    finally:
        if isinstance(conn, sqlite3.Connection):
            conn.set_progress_handler(None, 0)
    if len(rows) > max_rows:
        raise Blocked(f"result has more than {max_rows} rows; aggregate before returning rows")
    return rows
