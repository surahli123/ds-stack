#!/usr/bin/env python3
"""Startup self-test for a guarded runner. Run it before any unsupervised session.

Exits 0 only if the runner blocks a write outside scratch, a second smuggled
statement, and an oversized result, and still allows an aggregate read and a
scratch write. The default target is the reference SQLite runner. A warehouse
adapter in the private overlay should ship its own copy of these assertions.
"""

import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import guarded_query as gq  # noqa: E402


def selftest(conn, scratch_prefix, run=gq.run):
    results = []

    # Judge outcomes, not exception types: a statement the database itself
    # rejects did not run, which is what the envelope needs.
    def expect_blocked(label, sql):
        try:
            run(conn, sql, scratch_prefix=scratch_prefix, max_rows=10)
        except Exception:
            results.append((label, True))
        else:
            results.append((label, False))

    def expect_allowed(label, sql):
        try:
            run(conn, sql, scratch_prefix=scratch_prefix, max_rows=10)
            results.append((label, True))
        except Exception:
            results.append((label, False))

    expect_blocked("write outside scratch is blocked", "CREATE TABLE prod_copy AS SELECT 1 AS x")
    expect_blocked("second statement is blocked", "SELECT 1; DROP TABLE events")
    expect_blocked("raw-row dump is blocked", "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 50) SELECT i FROM n")
    expect_allowed("aggregate read is allowed", "SELECT COUNT(*) FROM sqlite_master")
    expect_allowed("scratch write is allowed", f"CREATE TABLE IF NOT EXISTS {scratch_prefix}selftest AS SELECT 1 AS x")
    return results


def main():
    conn = sqlite3.connect(":memory:")
    results = selftest(conn, scratch_prefix="scratch_selftest_")
    for label, ok in results:
        print(f"{'ok  ' if ok else 'FAIL'} {label}")
    return 0 if all(ok for _, ok in results) else 1


if __name__ == "__main__":
    sys.exit(main())
