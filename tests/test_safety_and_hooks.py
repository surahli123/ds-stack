"""The guarded runner enforces the envelope; the denylist hook blocks leaks, fail-closed."""

import os
import sqlite3
import subprocess

import guarded_query as gq
import pytest
import selftest
from conftest import ROOT

HOOKS = os.path.join(ROOT, ".githooks")


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE events (id INTEGER, v INTEGER)")
    c.executemany("INSERT INTO events VALUES (?, ?)", [(i, i % 7) for i in range(500)])
    return c


@pytest.mark.parametrize("sql", [
    "DROP TABLE events",
    "INSERT INTO events VALUES (1, 1)",
    "UPDATE events SET v = 0",
    "DELETE FROM events",
    "CREATE TABLE prod_copy AS SELECT * FROM events",
    "SELECT 1; DROP TABLE events",
    "SELECT * INTO backup FROM events",
    "ATTACH DATABASE 'x.db' AS other",
    "PRAGMA writable_schema = 1",
    "WITH x AS (DELETE FROM events RETURNING *) SELECT * FROM x",
    "/* sneaky */ DELETE FROM events -- comment",
    "SELECT 1 -- /*\n; DROP TABLE events -- */",
    "EXPLAIN DELETE FROM events",
    "CREATE INDEX scratch_t_idx ON events(id)",
])
def test_guard_blocks_writes_outside_scratch(conn, sql):
    with pytest.raises(gq.Blocked):
        gq.run(conn, sql, scratch_prefix="scratch_t_")
    assert conn.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 500


def test_guard_allows_aggregates_and_scratch_writes(conn):
    assert gq.run(conn, "SELECT v, COUNT(*) FROM events GROUP BY v", scratch_prefix="scratch_t_") == [
        (v, 72 if v < 3 else 71) for v in range(7)]
    gq.run(conn, "CREATE TABLE scratch_t_summary AS SELECT v, COUNT(*) AS n FROM events GROUP BY v", scratch_prefix="scratch_t_")
    assert conn.execute("SELECT COUNT(*) FROM scratch_t_summary").fetchone()[0] == 7


def test_guard_allows_semicolons_inside_string_literals(conn):
    assert gq.run(conn, "SELECT ';' AS sep, COUNT(*) FROM events", scratch_prefix="scratch_t_") == [(";", 500)]


def test_guard_refuses_raw_text_packed_into_one_cell(conn):
    conn.execute("CREATE TABLE logs (txt TEXT)")
    conn.executemany("INSERT INTO logs VALUES (?)", [(f"user query number {i}",) for i in range(100)])
    with pytest.raises(gq.Blocked):
        gq.run(conn, "SELECT group_concat(txt, char(10)) FROM logs", scratch_prefix="scratch_t_")


def test_guard_refuses_raw_row_dumps(conn):
    with pytest.raises(gq.Blocked):
        gq.run(conn, "SELECT * FROM events", scratch_prefix="scratch_t_", max_rows=200)


def test_guard_aborts_slow_queries(conn):
    slow = "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n) SELECT COUNT(*) FROM n"
    with pytest.raises(gq.Blocked):
        gq.run(conn, slow, scratch_prefix="scratch_t_", max_seconds=0.2)


def test_selftest_passes_on_the_reference_runner():
    assert all(ok for _, ok in selftest.selftest(sqlite3.connect(":memory:"), "scratch_st_"))


def test_selftest_catches_a_leaky_runner():
    def leaky(conn, sql, **_):
        return conn.execute(sql).fetchall()
    results = dict(selftest.selftest(sqlite3.connect(":memory:"), "scratch_st_", run=leaky))
    assert not results["write outside scratch is blocked"]


def git(repo, *args, env=None, check=True):
    return subprocess.run(["git", *args], cwd=repo, env=env, capture_output=True, text=True, check=check)


@pytest.fixture
def repo(tmp_path):
    path = tmp_path / "repo"
    path.mkdir()
    git(path, "init", "-q", "-b", "work")
    git(path, "config", "user.email", "t@example.com")
    git(path, "config", "user.name", "t")
    os.symlink(os.path.join(ROOT, "hooks"), path / "hooks")
    git(path, "config", "core.hooksPath", HOOKS)
    return path


def commit(repo, text, env):
    (repo / "note.md").write_text(text)
    git(repo, "add", "note.md", env=env)
    return git(repo, "commit", "-q", "-m", "c", env=env, check=False)


def hook_env(**extra):
    env = {k: v for k, v in os.environ.items() if not k.startswith("DS_")}
    env.update(extra)
    return env


def test_hook_blocks_a_denylisted_term(repo, tmp_path):
    denylist = tmp_path / "denylist.txt"
    denylist.write_text("# codenames\nProjectFalcon\n")
    result = commit(repo, "Q3 readout for projectfalcon ranking\n", hook_env(DS_DENYLIST=str(denylist)))
    assert result.returncode != 0 and "blocked" in result.stderr


def test_hook_allows_clean_content(repo, tmp_path):
    denylist = tmp_path / "denylist.txt"
    denylist.write_text("ProjectFalcon\n")
    assert commit(repo, "generic mix-shift check\n", hook_env(DS_DENYLIST=str(denylist))).returncode == 0


def test_hook_reads_the_overlay_dir(repo, tmp_path):
    overlay = tmp_path / "overlay"
    overlay.mkdir()
    (overlay / "denylist.txt").write_text("secret_table\n")
    assert commit(repo, "select * from SECRET_TABLE\n", hook_env(DS_OVERLAY_DIR=str(overlay))).returncode != 0


def test_hook_fails_closed_without_a_denylist(repo):
    result = commit(repo, "anything\n", hook_env())
    assert result.returncode != 0 and "no readable denylist" in result.stderr


def test_hook_opt_out_is_explicit(repo):
    assert commit(repo, "anything\n", hook_env(DS_DENYLIST="none")).returncode == 0


def push(repo, stdin, env):
    return subprocess.run([os.path.join(ROOT, "hooks", "denylist-check.sh"), "push"], cwd=repo, env=env,
                          input=stdin, capture_output=True, text=True)


def sha(repo, ref="HEAD"):
    return git(repo, "rev-parse", ref).stdout.strip()


def test_push_scans_every_commit_not_the_net_diff(repo, tmp_path):
    denylist = tmp_path / "denylist.txt"
    denylist.write_text("ProjectFalcon\n")
    env = hook_env(DS_DENYLIST=str(denylist))
    commit(repo, "base\n", env)
    base = sha(repo)
    commit(repo, "projectfalcon numbers\n", hook_env(DS_DENYLIST="none"))
    commit(repo, "clean again\n", hook_env(DS_DENYLIST="none"))
    head = sha(repo)
    result = push(repo, f"refs/heads/work {head} refs/heads/work {base}\n", env)
    assert result.returncode != 0 and "blocked" in result.stderr
    new_branch = push(repo, f"refs/heads/work {head} refs/heads/work {'0' * 40}\n", env)
    assert new_branch.returncode != 0


def test_push_fails_closed_on_an_unknown_remote_sha(repo, tmp_path):
    denylist = tmp_path / "denylist.txt"
    denylist.write_text("ProjectFalcon\n")
    env = hook_env(DS_DENYLIST=str(denylist))
    commit(repo, "base\n", env)
    result = push(repo, f"refs/heads/work {sha(repo)} refs/heads/work {'1' * 40}\n", env)
    assert result.returncode != 0


def test_hook_scans_binary_files_and_paths(repo, tmp_path):
    denylist = tmp_path / "denylist.txt"
    denylist.write_text("secret_table\nProjectFalcon\n")
    env = hook_env(DS_DENYLIST=str(denylist))
    db = repo / "data.db"
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE secret_table (x INTEGER)")
    c.commit()
    c.close()
    git(repo, "add", "data.db", env=env)
    assert git(repo, "commit", "-q", "-m", "db", env=env, check=False).returncode != 0
    git(repo, "rm", "-q", "--cached", "data.db", env=env)
    (repo / "ProjectFalcon-notes.md").write_text("clean content\n")
    git(repo, "add", "ProjectFalcon-notes.md", env=env)
    assert git(repo, "commit", "-q", "-m", "path", env=env, check=False).returncode != 0
