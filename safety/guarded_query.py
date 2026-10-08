"""Reference guarded query runner: the safety envelope for live, unsupervised runs.

The overlay contract requires every agent query to go through a runner like
this one. It enforces these rules no matter what the agent was told:

1. Writes go only to objects whose name starts with the run's scratch prefix
   (an index must also sit on a scratch table).
2. One statement per call (no smuggled second statement).
3. Results are aggregates: more than `max_rows` rows, any text cell longer than
   `max_cell_chars`, or more than `max_result_chars` in total is refused.
4. A query that runs longer than `max_seconds` is aborted.

Row and character caps reduce raw-text exposure; they do not remove it. The
structural fix for untrusted free text (search queries, documents) is a
warehouse view without those columns, granted to the agent's role.

This reference implementation speaks DB-API with SQLite. A warehouse adapter in
the private overlay must keep the same contract, using native controls where
they exist, such as read-only roles or a cap on bytes scanned.
"""

import re
import sqlite3
import time

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
    _check_size(rows, max_rows, max_cell_chars, max_result_chars)
    return rows
