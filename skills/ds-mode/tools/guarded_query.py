"""Reference guarded query runner: the safety envelope for live, unsupervised runs.

The overlay contract requires every agent query to go through a runner like
this one. It enforces these rules no matter what the agent was told:

1. Writes go only to objects whose name starts with the run's scratch prefix
   (an index must also sit on a scratch table).
2. One statement per call (no smuggled second statement).
3. Results are aggregates: more than `max_rows` rows, any text cell longer than
   `max_cell_chars`, or more than `max_result_chars` in total is refused.
4. A query that runs longer than `max_seconds` is aborted.
5. Every statement is logged, with an id (q1, q2, ...), its parameters, as-of
   period, row count, time taken and the capped result rows, whether it ran,
   was blocked or failed (`run_logged`). Results computed elsewhere enter the
   same log through `log_pasted`. A readout cites the id, so a reviewer can
   read the number's source instead of re-running it.

Row and character caps reduce raw-text exposure; they do not remove it. The
structural fix for untrusted free text (search queries, documents) is a
warehouse view without those columns, granted to the agent's role.

This reference implementation speaks DB-API with SQLite. A warehouse adapter in
the private overlay must keep the same contract, including the log, using
native controls where they exist, such as read-only roles or a cap on bytes
scanned.
"""

import json
import os
import re
import sqlite3
import time
from contextlib import contextmanager

try:
    import fcntl
except ImportError:  # Windows: ids stay sequential as long as queries run one at a time
    fcntl = None

LOG_NAME = ".ds-queries.log"

WRITE_KEYWORDS = {"insert", "update", "delete", "create", "drop", "alter", "replace", "merge", "truncate", "attach", "pragma", "vacuum"}
READ_KEYWORDS = {"select", "with", "explain"}
WRITE_WORDS = re.compile(r"\b(insert|update|delete|create|drop|alter|replace|merge|truncate|attach)\b", re.I)
NAME = r"[\"`\[]?([\w.]+)[\"`\]]?"
TARGET = re.compile(
    r"^\s*(?:insert\s+(?:or\s+\w+\s+)?into|update(?:\s+or\s+\w+)?|delete\s+from|replace\s+into|merge\s+into|truncate(?:\s+table)?"
    r"|create\s+(?:temp(?:orary)?\s+)?(?:table|view)(?:\s+if\s+not\s+exists)?"
    r"|drop\s+(?:table|view|index)(?:\s+if\s+exists)?|alter\s+table)\s+" + NAME,
    re.I,
)
INDEX = re.compile(r"^\s*create\s+(?:unique\s+)?index\s+(?:if\s+not\s+exists\s+)?" + NAME + r"\s+on\s+" + NAME, re.I)


class Blocked(Exception):
    """The query broke the safety envelope and was not run."""


def lex(sql):
    """One left-to-right pass: drop comments, blank out string literals, keep identifiers."""
    out, i, n = [], 0, len(sql)
    while i < n:
        if sql.startswith("--", i):
            end = sql.find("\n", i)
            i = n if end < 0 else end
            out.append(" ")
        elif sql.startswith("/*", i):
            end = sql.find("*/", i + 2)
            i = n if end < 0 else end + 2
            out.append(" ")
        elif sql[i] in "'\"`":
            quote, j = sql[i], i + 1
            while j < n:
                if sql[j] == quote:
                    if j + 1 < n and sql[j + 1] == quote:
                        j += 2
                        continue
                    break
                j += 1
            out.append("''" if quote == "'" else sql[i:j + 1])
            i = j + 1
        else:
            out.append(sql[i])
            i += 1
    return "".join(out)


def _scratch(name, prefix):
    return bool(prefix) and name.split(".")[-1].lower().startswith(prefix.lower())


def classify(sql, scratch_prefix):
    """Return 'read' or 'scratch_write', or raise Blocked."""
    body = lex(sql).strip().rstrip(";").strip()
    if not body:
        raise Blocked("empty statement")
    if ";" in body:
        raise Blocked("one statement per call")
    keyword = body.split(None, 1)[0].lower()
    if keyword in READ_KEYWORDS:
        if keyword in ("with", "explain") and WRITE_WORDS.search(body):
            raise Blocked(f"'{keyword}' wrapping a data-modifying statement is not allowed")
        if re.search(r"\binto\b", body, re.I):
            raise Blocked("SELECT ... INTO creates a table; write to scratch with CREATE TABLE instead")
        return "read"
    if keyword not in WRITE_KEYWORDS:
        raise Blocked(f"statement type '{keyword}' is not allowed")
    index = INDEX.match(body)
    if index:
        name, table = index.groups()
        if not (_scratch(name, scratch_prefix) and _scratch(table, scratch_prefix)):
            raise Blocked(f"index '{name}' on '{table}' is outside the scratch prefix '{scratch_prefix}'")
        return "scratch_write"
    match = TARGET.match(body)
    if not match:
        raise Blocked(f"'{keyword}' is not allowed")
    if not _scratch(match.group(1), scratch_prefix):
        raise Blocked(f"write to '{match.group(1)}' is outside the scratch prefix '{scratch_prefix}'")
    return "scratch_write"


def _check_size(rows, max_rows, max_cell_chars, max_result_chars):
    if len(rows) > max_rows:
        raise Blocked(f"result has more than {max_rows} rows; aggregate before returning rows")
    total = 0
    for row in rows:
        for cell in row:
            if isinstance(cell, (str, bytes)):
                if len(cell) > max_cell_chars:
                    raise Blocked(f"a text cell is longer than {max_cell_chars} characters; return aggregates, not raw text")
                total += len(cell)
            else:
                total += len(str(cell))
    if total > max_result_chars:
        raise Blocked(f"result is larger than {max_result_chars} characters")


def run(conn, sql, params=(), *, scratch_prefix, max_rows=200, max_cell_chars=200, max_result_chars=20_000, max_seconds=60.0):
    return _execute(conn, sql, params, scratch_prefix, max_rows, max_cell_chars, max_result_chars, max_seconds)[1]


def _execute(conn, sql, params, scratch_prefix, max_rows, max_cell_chars, max_result_chars, max_seconds):
    """Run one statement inside the envelope; return (columns, rows)."""
    kind = classify(sql, scratch_prefix)
    deadline = time.monotonic() + max_seconds
    if isinstance(conn, sqlite3.Connection):
        conn.set_progress_handler(lambda: 1 if time.monotonic() > deadline else 0, 10_000)
    try:
        cursor = conn.execute(sql, params)
        if kind == "scratch_write":
            conn.commit()
            return [], []
        columns = [col[0] for col in cursor.description or ()]
        rows = cursor.fetchmany(max_rows + 1)
    except sqlite3.OperationalError as err:
        if "interrupted" in str(err):
            raise Blocked(f"query exceeded {max_seconds}s") from err
        raise
    finally:
        if isinstance(conn, sqlite3.Connection):
            conn.set_progress_handler(None, 0)
    _check_size(rows, max_rows, max_cell_chars, max_result_chars)
    return columns, rows


def log_path(path=None):
    return path or os.environ.get("DS_QUERIES_LOG") or os.path.join(os.getcwd(), LOG_NAME)


def read_log(path=None):
    """Every entry in the query log, oldest first. Unreadable lines are skipped."""
    entries = []
    try:
        with open(log_path(path)) as handle:
            for line in handle:
                try:
                    entries.append(json.loads(line))
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return entries


@contextmanager
def _locked(path):
    with open(path, "a+") as handle:
        if fcntl:
            fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield handle
        finally:
            if fcntl:
                fcntl.flock(handle, fcntl.LOCK_UN)


def _append(path, make_entry):
    """Give the entry the next id and append it, under a lock so ids stay unique."""
    with _locked(path) as handle:
        handle.seek(0)
        count = sum(1 for line in handle if line.strip())
        entry = {"id": f"q{count + 1}", "ts": round(time.time(), 3), **make_entry()}
        handle.seek(0, os.SEEK_END)
        handle.write(json.dumps(entry, default=str) + "\n")
    return entry


def run_logged(conn, sql, params=(), *, as_of=None, log=None, scratch_prefix, max_rows=200, max_cell_chars=200,
               max_result_chars=20_000, max_seconds=60.0):
    """Run one statement through the envelope and log it, whatever the outcome.

    Returns the log entry. Raises Blocked or the database error after logging it.
    """
    started = time.monotonic()
    base = {"source": "runner", "sql": sql, "params": list(params), "as_of": as_of}
    try:
        columns, rows = _execute(conn, sql, params, scratch_prefix, max_rows, max_cell_chars, max_result_chars, max_seconds)
    except Exception as err:
        status = "blocked" if isinstance(err, Blocked) else "error"
        _append(log_path(log), lambda: {**base, "status": status, "error": str(err),
                                        "seconds": round(time.monotonic() - started, 3)})
        raise
    return _append(log_path(log), lambda: {**base, "status": "ok", "seconds": round(time.monotonic() - started, 3),
                                           "row_count": len(rows), "columns": columns, "rows": [list(r) for r in rows]})


def log_pasted(sql, columns, rows, *, as_of=None, log=None, max_rows=200, max_cell_chars=200, max_result_chars=20_000):
    """Log a result computed outside the runner (for example, run by a person).

    The same size caps apply, so only aggregates enter the log. Returns the entry.
    """
    base = {"source": "pasted", "sql": sql, "params": [], "as_of": as_of}
    rows = [list(row) for row in rows]
    try:
        _check_size(rows, max_rows, max_cell_chars, max_result_chars)
    except Blocked as err:
        _append(log_path(log), lambda: {**base, "status": "blocked", "error": str(err)})
        raise
    return _append(log_path(log), lambda: {**base, "status": "ok", "row_count": len(rows),
                                           "columns": list(columns), "rows": rows})
