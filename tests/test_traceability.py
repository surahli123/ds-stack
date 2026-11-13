"""Every number in a readout traces to a logged query or check, and a script proves it."""

import json
import sqlite3

import guarded_query as gq
import pytest
import query
import run as checks_run
import verify_readout as vr
from readout import parse


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("DS_QUERIES_LOG", raising=False)
    monkeypatch.delenv("DS_CHECKS_LOG", raising=False)
    monkeypatch.delenv("DS_OVERLAY_DIR", raising=False)
    conn = sqlite3.connect(tmp_path / "warehouse.db")
    conn.execute("CREATE TABLE events (platform TEXT, clicks INTEGER, searches INTEGER)")
    conn.executemany("INSERT INTO events VALUES (?, ?, ?)", [("web", 30, 100), ("app", 20, 100)])
    conn.commit()
    conn.close()
    return tmp_path


def read_jsonl(path):
    return [json.loads(line) for line in open(path)]


def test_runner_logs_every_statement_with_a_unique_id(workdir):
    conn = sqlite3.connect("warehouse.db")
    entry = gq.run_logged(conn, "SELECT platform, SUM(clicks) AS k FROM events GROUP BY platform ORDER BY platform",
                          as_of="2026-10-04", scratch_prefix="scratch_t_")
    assert entry["id"] == "q1" and entry["status"] == "ok" and entry["as_of"] == "2026-10-04"
    assert entry["columns"] == ["platform", "k"] and entry["rows"] == [["app", 20], ["web", 30]]
    with pytest.raises(gq.Blocked):
        gq.run_logged(conn, "DROP TABLE events", scratch_prefix="scratch_t_")
    with pytest.raises(sqlite3.OperationalError):
        gq.run_logged(conn, "SELECT nope FROM events", scratch_prefix="scratch_t_")
    log = gq.read_log()
    assert [(e["id"], e["status"]) for e in log] == [("q1", "ok"), ("q2", "blocked"), ("q3", "error")]
    # run() keeps its old return type for existing callers
    assert gq.run(conn, "SELECT COUNT(*) FROM events", scratch_prefix="scratch_t_") == [(2,)]


def test_pasted_results_get_an_id_and_the_same_size_caps(workdir):
    entry = gq.log_pasted("SELECT ...", ["n"], [[5]], as_of="2026-10-04")
    assert entry["source"] == "pasted" and entry["id"] == "q1"
    with pytest.raises(gq.Blocked):
        gq.log_pasted("SELECT ...", ["n"], [[i] for i in range(500)])
    assert [e["status"] for e in gq.read_log()] == ["ok", "blocked"]


def test_query_cli_prints_the_id_and_logs_blocked_attempts(workdir, capsys):
    assert query.main(["SELECT SUM(clicks) FROM events", "--as-of", "2026-10-04"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["id"] == "q1" and out["rows"] == [[50]]
    assert query.main(["DELETE FROM events"]) == 1
    assert json.loads(capsys.readouterr().out) == {"id": "q2", "status": "blocked",
                                                   "error": "write to 'events' is outside the scratch prefix 'scratch_dsmode_run_'"}
    assert query.main(["--pasted", "--sql", "SELECT 1", "--columns", '["x"]', "--rows", "[[1]]"]) == 0
    assert json.loads(capsys.readouterr().out)["id"] == "q3"
    assert query.main(["--pasted", "--sql", "SELECT 1"]) == 3
    assert query.main(["SELECT 1", "--db", "missing.db"]) == 3


def test_queries_record_the_metric_and_slice_they_compute(workdir, capsys):
    assert query.main(["SELECT SUM(clicks) * 1.0 / SUM(searches) FROM events", "--metric", "ctr"]) == 0
    assert query.main(["--pasted", "--sql", "x", "--columns", '["ctr"]', "--rows", "[[0.2]]", "--metric", "ctr", "--slice", "app"]) == 0
    assert query.main(["SELECT 1"]) == 0
    log = read_jsonl(workdir / ".ds-queries.log")
    assert [(e.get("metric"), e.get("slice")) for e in log] == [("ctr", "all"), ("ctr", "app"), (None, None)]


def test_one_metric_reported_with_two_values_is_listed(capsys):
    base = {"status": "ok", "metric": "ctr", "slice": "all", "as_of": "2026-10-04"}
    queries = [{**base, "id": "q1", "sql": "SELECT SUM(clicks) * 1.0 / SUM(searches) FROM s", "rows": [[0.304]]},
               {**base, "id": "q2", "sql": "SELECT ... WHERE is_bot = 0", "rows": [[0.291]]},
               {**base, "id": "q3", "sql": "SELECT week, ...", "rows": [["2026-09-28", 0.2912], ["2026-10-04", 0.304]]},
               {**base, "id": "q4", "slice": "mobile", "rows": [[0.22]]}]
    text = ("## Answer\nHeadline: CTR 30.4% [q1]\n- Without bots: 29.1% [q2]\n- Weekly: 29.1% then 30.4% [q3]\n"
            "- Mobile: 22.0% [q4]\n\n## Provenance\n- Reconciled: not done (none)\n")
    problems, stats, _ = vr.verify(text, queries, [])
    assert problems == [] and [(c[3]["id"], c[4]["id"]) for c in stats["conflicts"]] == [("q1", "q2")]
    assert vr.verify(text.replace("- Without bots: 29.1% [q2]\n", ""), queries, [])[1]["conflicts"] == []


def test_checks_record_their_id_and_source_queries(workdir, capsys):
    spec = {"observed": [5000, 5000], "expected_ratio": [0.5, 0.5], "from": "q1"}
    checks_run.main(["srm", "--json", json.dumps(spec)])
    checks_run.main(["srm", "--json", json.dumps({**spec, "from": ["q1", "q2"]})])
    assert checks_run.main(["srm", "--json", json.dumps({**spec, "from": "select 1"})]) == 2
    log = read_jsonl(workdir / ".ds-checks.log")
    assert [(e["id"], e["from"], e["status"]) for e in log] == [
        ("srm#1", ["q1"], "pass"), ("srm#2", ["q1", "q2"], "pass"), ("srm#3", [], "could_not_run")]


READOUT = """## Answer
Headline: -2.1 pp (95% interval -2.3 to -1.9) [check:mix_shift#1]
Overall CTR fell from 30.4% to 28.3% between 2026-09-21 and 2026-10-04 [q1, check:mix_shift#1]; ranker v2 shows no within-segment change.

## What it means for the rollback decision
The interval excludes the 0.5 pp harm that would trigger a rollback [check:mix_shift#1] [given].

## Why we believe it
- Alternatives considered:
  - Mix-shift: ruled in by mobile share rising from 40% to 55% [q1] [measured]
- Checks run:
  - mix_shift: flag mix share 1.00 [check:mix_shift#1]

## Caveats, and what would change the answer
- One week on each side; 3 more weeks would settle seasonality.

## Provenance
- Metric: CTR = clicks / searches, stated here [guess]
- Reconciled: not done (no dashboard)
"""
QUERIES = [{"id": "q1", "status": "ok"}, {"id": "q2", "status": "blocked"}]
CHECKS = [{"id": "mix_shift#1", "check": "mix_shift", "from": ["q1"]}, {"id": "srm#1", "check": "srm", "from": []}]


def test_verify_passes_a_fully_traced_readout_and_lists_given_numbers():
    problems, stats, given = vr.verify(READOUT, QUERIES, CHECKS)
    assert problems == []
    assert stats["queries"] == {"q1"} and stats["checks"] == {"mix_shift#1"}
    assert len(given) == 1 and "0.5 pp" in given[0]


@pytest.mark.parametrize("change, expected", [
    (("ruled in by mobile share rising from 40% to 55% [q1]", "ruled in by mobile share rising from 40% to 55%"), "untagged number"),
    (("[q1, check:mix_shift#1]", "[q9]"), "[q9] doesn't resolve: it is not in the query log"),
    (("[q1, check:mix_shift#1]", "[q2]"), "[q2] doesn't resolve: it was blocked"),
    (("flag mix share 1.00 [check:mix_shift#1]", "pass [check:srm#1]"), "[check:srm#1] has no source query"),
    (("flag mix share 1.00 [check:mix_shift#1]", "pass [check:srm#4]"), "[check:srm#4] doesn't resolve"),
    (("- Reconciled: not done (no dashboard)\n", ""), "no 'Reconciled:' line"),
])
def test_verify_fails_untraced_or_unresolved_numbers(change, expected):
    problems, _, _ = vr.verify(READOUT.replace(*change), QUERIES, CHECKS)
    assert any(expected in p for p in problems), problems


def test_dates_interval_levels_and_names_are_not_numbers():
    assert vr.numbers_in("ranker v2 from 2026-09-21 (95% interval) [q3]") == []
    assert vr.numbers_in("1. CTR fell 2.1 pp") == ["2.1"]
    assert vr.tags_in("x [q3, q4] [check:srm#2] [measured]") == ["q3", "q4", "check:srm#2"]


def test_numbers_are_looked_up_in_what_their_tags_hold(capsys):
    queries = [{"id": "q1", "status": "ok", "rows": [["2026-09-21", 0.304], ["2026-09-28", 0.283]], "row_count": 14}]
    checks = [{"id": "mix_shift#1", "check": "mix_shift", "from": ["q1"], "details": {"delta_pp": -2.0968}}]
    text = ("## Answer\nHeadline: -2.10 pp [check:mix_shift#1]\n"
            "- Observed: CTR fell from 30.4% to 28.3% over 14 days [q1]\n"
            "- Gap: 2.1 pp, interval 1.9 to 2.3 pp [q1]\n"
            "- Threshold: 0.5 pp [given]\n")
    problems, stats, _ = vr.verify(text, queries, checks)
    assert problems == []
    assert stats["unsourced"] == [(["2.1", "1.9", "2.3"], "- Gap: 2.1 pp, interval 1.9 to 2.3 pp [q1]")]
    assert not vr.in_source("30.9", vr.values_in(queries[0]["rows"]))


def test_unsourced_numbers_are_listed_but_do_not_fail(tmp_path, capsys):
    (tmp_path / "q.log").write_text(json.dumps({"id": "q1", "status": "ok", "rows": [[0.304]]}))
    (tmp_path / "r.md").write_text("## Answer\nHeadline: 30.4% [q1]\nIt rose 1.7 pp [q1]\n\n## Provenance\n- Reconciled: not done (none)\n")
    assert vr.main([str(tmp_path / "r.md"), "--queries", str(tmp_path / "q.log"), "--checks", str(tmp_path / "none")]) == 0
    out = capsys.readouterr().out
    assert "1 not found in their source" in out and "not in its source (confirm, or log how it was computed): 1.7 in:" in out


@pytest.mark.parametrize("subheading", ["Caveats by segment", "Provenance by segment"])
def test_reserved_subheadings_stay_in_the_checked_section_and_sibling_sections_split(subheading):
    queries = [{"id": "q1", "status": "ok", "rows": [[0.304]]}]
    text = (f"## Answer\nHeadline: 30.4% [q1]\n\n### {subheading}\n| stale results | 96 of 169 |\n\n"
            "## Caveats, and what would change the answer\n- 292 tickets did not join.\n\n"
            "## Provenance\n- Reconciled: not done (none)\n\n## Appendix\nRaw counts: 1,062 tickets.\n")
    problems, stats, _ = vr.verify(text, queries, [])
    assert problems == ["untagged number in 'Answer': | stale results | 96 of 169 |"]
    assert stats["numbers"] == 3
    found = vr.readout_sections(text)
    assert [name for name, _ in found] == [
        "Answer", "Caveats, and what would change the answer", "Provenance", "Appendix"
    ]
    bodies = dict(found)
    assert "292 tickets did not join" in bodies["Caveats, and what would change the answer"]
    assert "Reconciled: not done" in bodies["Provenance"]
    assert "Raw counts: 1,062 tickets" in bodies["Appendix"]


@pytest.mark.parametrize("heading", ["## Provenance", "## **Provenance**"])
def test_stamp_skips_provenance_named_subheadings_inside_answer(heading):
    text = ("## Answer\nHeadline: 30.4% [q1]\n\n### Provenance by segment\nNo extra figures.\n\n"
            f"## Caveats\nNone.\n\n{heading}\n- Reconciled: not done (none)\n\n## Appendix\nRaw notes.\n")
    stamped = vr.stamp(text, "verify_readout: pass")
    bodies = dict(vr.readout_sections(stamped))
    assert "Verified:" not in bodies["Answer"]
    assert bodies["Provenance"].strip().splitlines()[-1] == "- Verified: verify_readout: pass"
    assert vr.stamp(stamped, "verify_readout: pass") == stamped
    assert stamped.endswith("## Appendix\nRaw notes.\n")


def test_stamp_writes_one_verified_line_at_the_end_of_provenance(tmp_path, capsys):
    (tmp_path / "q.log").write_text("\n".join(json.dumps(e) for e in QUERIES))
    (tmp_path / "c.log").write_text("\n".join(json.dumps(e) for e in CHECKS))
    args = ["--queries", str(tmp_path / "q.log"), "--checks", str(tmp_path / "c.log"), "--stamp"]
    readout = tmp_path / "r.md"
    readout.write_text(READOUT + "\n## Notes\nnone\n")
    assert vr.main([str(readout), *args]) == 0
    assert vr.main([str(readout), *args]) == 0
    text = readout.read_text()
    provenance = text.split("## Provenance")[1].split("## Notes")[0].strip().splitlines()
    assert provenance[-1].startswith("- Verified: verify_readout: pass (")
    assert text.count("Verified:") == 1 and text.endswith("## Notes\nnone\n")
    readout.write_text(READOUT.replace(" [q1] [measured]", " [measured]"))
    assert vr.main([str(readout), *args]) == 1
    assert "Verified:" not in readout.read_text()
    assert vr.main(["-", "--stamp"]) == 3


def test_verify_cli_exit_codes(tmp_path, capsys):
    (tmp_path / "r.md").write_text(READOUT)
    (tmp_path / "q.log").write_text("\n".join(json.dumps(e) for e in QUERIES))
    (tmp_path / "c.log").write_text("\n".join(json.dumps(e) for e in CHECKS))
    args = ["--queries", str(tmp_path / "q.log"), "--checks", str(tmp_path / "c.log")]
    assert vr.main([str(tmp_path / "r.md"), *args]) == 0
    assert capsys.readouterr().out.startswith("verify_readout: pass")
    (tmp_path / "r.md").write_text(READOUT.replace(" [q1] [measured]", " [measured]"))
    assert vr.main([str(tmp_path / "r.md"), *args]) == 1
    assert vr.main([str(tmp_path / "missing.md")]) == 3


def test_eval_parser_ignores_trace_tags():
    readout = parse(READOUT)
    assert readout.ok and readout.value == -2.1 and readout.interval == (-2.3, -1.9)
