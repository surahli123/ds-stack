"""ds-interrogate runs a reviewer from another model family and keeps only the findings a rerun proves.

A fake reviewer (a Python script standing in for codex exec or claude -p) runs real queries through ds-mode's
runner and writes findings.json, so every check here runs without a model."""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time

import pytest
from conftest import ROOT

sys.path.insert(0, os.path.join(ROOT, "skills", "ds-interrogate", "tools"))
import interrogate  # noqa: E402

RUN = os.path.join(ROOT, "eval", "results", "2026-10-14-claude-en", "f1__full__2")
DB = os.path.join(ROOT, "eval", "fixtures", "f1", "warehouse.db")
SCRIPT = os.path.join(ROOT, "skills", "ds-interrogate", "tools", "interrogate.py")
QUOTE = next(line.split("[")[0].strip() for line in open(os.path.join(RUN, "result.md"), encoding="utf-8")
             if line.startswith("- Observed:"))

# Runs one query through the logged runner (the brief's command), then writes findings.json from a template.
# The template's {id} becomes the printed query id and {n} the first number in the first row.
FAKE = r'''
import json, re, subprocess, sys
print("model: gpt-served-1", file=sys.stderr)  # the header Codex prints
brief = open(sys.argv[2]).read()
spec = json.loads(open("SPEC").read()) if __import__("os").path.exists("SPEC") else None
cmd = re.search(r'^    (python3 .+?) "SELECT \.\.\."$', brief, re.M).group(1)
if spec is None:
    print("I looked and wrote nothing.")
    sys.exit(0)
out = json.loads(subprocess.run(cmd + " " + json.dumps(spec["sql"]), shell=True, capture_output=True, text=True).stdout)
if spec.get("write"):
    subprocess.run(cmd + " " + json.dumps("drop table search_daily"), shell=True)
n = next(v for row in out["rows"] for v in row if isinstance(v, (int, float)))
findings = json.loads(json.dumps(spec["findings"]).replace("{id}", out["id"]).replace("{n}", str(n)))
open("findings.json", "w").write(json.dumps(findings))
print(len(findings))
'''


@pytest.fixture
def setup(tmp_path, monkeypatch):
    fake = tmp_path / "fake.py"
    fake.write_text(FAKE)
    overlay = tmp_path / "overlay"
    overlay.mkdir()
    monkeypatch.setenv("DS_OVERLAY_DIR", str(overlay))

    def configure(families, spec):
        reviewers = [{"family": f, "model": f"{f}-m", "cmd": [sys.executable, str(fake), "{model}", "{prompt_file}"]}
                     for f in families]
        (overlay / "reviewers.json").write_text(json.dumps({"reviewers": reviewers}))
        # Each reviewer directory gets the spec through a file the fake reads from its working directory.
        monkeypatch.setattr(interrogate, "prepare", with_spec(interrogate.prepare, spec))
        return tmp_path
    return configure


def with_spec(prepare, spec):
    def wrapped(workdir, *args):
        prompt = prepare(workdir, *args)
        if spec is not None:
            open(os.path.join(workdir, "SPEC"), "w").write(json.dumps(spec))
        return prompt
    return wrapped


def finding(**overrides):
    base = {"title": "Observed change is wrong", "readout_quote": QUOTE, "query_id": "{id}",
            "shows": "the query gives {n}", "why_it_matters": "the headline would change"}
    return {**base, **overrides}


def run(tmp_path, *extra):
    report = tmp_path / "report.json"
    code = interrogate.main([os.path.join(RUN, "result.md"), "--request",
                             os.path.join(ROOT, "eval", "fixtures", "f1", "task.md"),
                             "--queries", os.path.join(RUN, "queries.log"), "--checks", os.path.join(RUN, "checks.log"),
                             "--db", DB, "--out", str(tmp_path / "out"), "--json", str(report), *extra])
    return code, json.loads(report.read_text())


SQL = "select platform, sum(searches) from search_daily group by platform"


def test_a_proven_finding_is_kept_with_its_query(setup, capsys):
    tmp = setup(["gpt"], {"sql": SQL, "findings": [finding()]})
    code, report = run(tmp, "--analyst-family", "claude")
    assert code == 1 and len(report["findings"]) == 1
    kept = report["findings"][0]
    assert kept["sql"] == SQL and kept["rows"] and kept["reviewers"] == ["gpt:gpt-m"]
    assert report["independence"].startswith("independent")
    assert "for you to judge" in capsys.readouterr().out


@pytest.mark.parametrize("change, reason", [
    ({"shows": "the query gives 123456789"}, "none of its specific numbers is in the output"),
    ({"shows": "the query gives {n}, then 111111, 222222 and 333333"}, "most of its numbers aren't in the output"),
    ({"readout_quote": "a sentence the readout never said"}, "quote isn't in the readout"),
    ({"query_id": "q99"}, "isn't a query that ran"),
    ({"why_it_matters": ""}, "missing why_it_matters"),
])
def test_unproven_findings_are_dropped_with_the_reason(setup, change, reason):
    tmp = setup(["gpt"], {"sql": SQL, "findings": [finding(**change)]})
    code, report = run(tmp, "--analyst-family", "claude")
    assert code == 0 and report["findings"] == []
    assert reason in report["results"][0]["dropped"][0]["reason"]


def test_no_findings_file_means_the_reviewer_did_not_run(setup):
    tmp = setup(["gpt"], None)
    code, report = run(tmp, "--analyst-family", "claude")
    assert code == 2 and not report["results"][0]["ran"]


def test_an_empty_list_is_a_valid_review(setup, capsys):
    tmp = setup(["gpt"], {"sql": SQL, "findings": []})
    code, report = run(tmp, "--analyst-family", "claude")
    assert code == 0 and report["results"][0]["ran"]
    assert "doesn't prove the readout right" in capsys.readouterr().out


@pytest.mark.parametrize("families, analyst, chosen, note", [
    (["claude", "gpt"], "claude", "gpt", "independent"),
    (["claude", "gpt"], "gpt", "claude", "independent"),
    (["claude"], "claude", "claude", "not independent"),
    (["gpt", "claude"], None, "gpt", "family check didn't run"),
])
def test_the_reviewer_comes_from_another_family(setup, families, analyst, chosen, note):
    tmp = setup(families, {"sql": SQL, "findings": []})
    extra = ["--analyst-family", analyst] if analyst else []
    _, report = run(tmp, *extra)
    assert report["results"][0]["reviewer"].startswith(chosen)
    assert note in report["independence"]


def test_a_model_slug_gives_the_family():
    assert interrogate.family_of("claude-opus-5-5") == "claude"
    assert interrogate.family_of("gpt-6-astra") == "gpt"
    assert interrogate.family_of("grok-4.7-xhigh-fast") == "grok"
    assert interrogate.family_of("mystery-1") is None


def test_the_reviewer_never_touches_the_analysis_database(setup):
    before = hashlib.sha256(open(DB, "rb").read()).hexdigest()
    tmp = setup(["gpt"], {"sql": SQL, "findings": [finding()], "write": True})
    run(tmp, "--analyst-family", "claude")
    assert hashlib.sha256(open(DB, "rb").read()).hexdigest() == before


def test_uninstalled_reviewers_are_skipped(tmp_path, monkeypatch):
    overlay = tmp_path / "overlay"
    overlay.mkdir()
    (overlay / "reviewers.json").write_text(json.dumps({"reviewers": [
        {"family": "gpt", "cmd": ["no-such-agent-cli", "{prompt_file}"]}]}))
    monkeypatch.setenv("DS_OVERLAY_DIR", str(overlay))
    chosen, note = interrogate.choose(interrogate.load_reviewers(), "claude", 1)
    assert chosen == [] and "no reviewer" in note


def test_the_default_wrappers_name_the_cli_they_need(monkeypatch):
    monkeypatch.delenv("DS_OVERLAY_DIR", raising=False)
    reviewers = interrogate.load_reviewers()
    assert [r["family"] for r in reviewers] == ["gpt", "claude"]
    monkeypatch.setattr(interrogate.shutil, "which", lambda name: "/bin/" + name if name == "claude" else None)
    assert [interrogate.installed(r) for r in reviewers] == [False, True]


def test_cli_usage_errors():
    assert subprocess.run([sys.executable, SCRIPT], capture_output=True).returncode == 2  # argparse: --request missing
    proc = subprocess.run([sys.executable, SCRIPT, os.path.join(RUN, "result.md"), "--request", "/nope"],
                          capture_output=True, text=True)
    assert proc.returncode == 3


def test_a_relative_out_directory_still_reaches_the_reviewer(setup, monkeypatch):
    tmp = setup(["gpt"], {"sql": SQL, "findings": [finding()]})
    monkeypatch.chdir(tmp)
    code = interrogate.main([os.path.join(RUN, "result.md"), "--request", os.path.join(ROOT, "eval", "fixtures", "f1", "task.md"),
                             "--queries", os.path.join(RUN, "queries.log"), "--checks", os.path.join(RUN, "checks.log"),
                             "--db", DB, "--analyst-family", "claude", "--out", "relative-out"])
    assert code == 1


def test_derived_numbers_and_the_readouts_own_numbers_do_not_drop_a_proven_finding(setup, capsys):
    # As in the first live run: the reviewer quoted the readout's wrong number and a difference it worked out.
    shows = "the query gives {n}; the readout's own figures say otherwise, and the gap is 98765.4"
    tmp = setup(["gpt"], {"sql": SQL, "findings": [finding(shows=shows)]})
    code, report = run(tmp, "--analyst-family", "claude")
    assert code == 1 and report["findings"][0]["unmatched"] == ["98765.4"]
    assert "not in the rows (derived or unproven): 98765.4" in capsys.readouterr().out



# --- regressions from the adversarial review ----------------------------------------------------------------

@pytest.mark.parametrize("sql", ["select 12345.6 as fake", "select 'search_daily' as t, 12345.6 as fake"])
def test_a_query_that_reads_no_table_proves_nothing(setup, sql):
    tmp = setup(["gpt"], {"sql": sql, "findings": [finding(shows="the data gives 12345.6")]})
    code, report = run(tmp, "--analyst-family", "claude")
    assert code == 0 and "reads no data table" in report["results"][0]["dropped"][0]["reason"]


@pytest.mark.parametrize("change, reason", [
    ({"readout_quote": "pp"}, "too short"),
    ({"shows": "The data does not support this at all."}, "quotes no number"),
    ({"shows": "0 days support this; see the 9 and 21 figures for 2026"}, "none of its specific numbers"),
    ({"shows": "{n} {n} {n} {n} and 777.7 888.8 999.9"}, "most of its numbers aren't in the output"),
])
def test_weak_or_padded_findings_are_dropped(setup, change, reason):
    tmp = setup(["gpt"], {"sql": SQL, "findings": [finding(**change)]})
    code, report = run(tmp, "--analyst-family", "claude")
    assert code == 0 and reason in report["results"][0]["dropped"][0]["reason"]


def test_a_number_matches_times_100_only_when_written_as_a_percent():
    assert interrogate.in_values("55.07", True, [0.5507])
    assert not interrogate.in_values("55.07", False, [0.5507])
    assert interrogate.cell_values([["2026-09-21", "mobile 40.1"]]) == [40.1]


def test_two_findings_on_one_line_are_both_kept(setup):
    tmp = setup(["gpt"], {"sql": SQL, "findings": [finding(), finding(title="A second, different fault")]})
    code, report = run(tmp, "--analyst-family", "claude")
    assert code == 1 and len(report["findings"]) == 2 and report["findings"][0]["reviewers"] == ["gpt:gpt-m"]


def test_the_default_model_is_recorded_as_the_one_that_ran(setup):
    tmp = setup(["gpt"], {"sql": SQL, "findings": [finding()]})
    reviewers = tmp / "overlay" / "reviewers.json"
    config = json.loads(reviewers.read_text())
    config["reviewers"][0]["model"] = "-"
    reviewers.write_text(json.dumps(config))
    code, report = run(tmp, "--analyst-family", "claude")
    assert code == 1 and report["findings"][0]["reviewers"] == ["gpt:gpt-served-1"]


def test_the_brief_asks_for_findings_in_the_readouts_language():
    with open(os.path.join(ROOT, "skills", "ds-interrogate", "references", "brief.md"), encoding="utf-8") as handle:
        assert "in the language of the readout's prose" in handle.read()


PROBE = """
import json, os, sys
print("CWD=" + os.getcwd())
print("KEYS=" + ",".join(sorted(os.environ)))
sys.stdout.flush()
sys.stdout.buffer.write(b"\\xff\\xfe not utf-8\\n")
open("review.queries.log", "w").write(json.dumps({"id": 7, "status": "ok"}) + "\\n")
open("findings.json", "w").write("[]")
"""


def test_the_reviewer_runs_outside_the_project_with_a_small_environment(tmp_path, monkeypatch):
    probe = tmp_path / "probe.py"
    probe.write_text(PROBE)
    overlay = tmp_path / "overlay"
    overlay.mkdir()
    (overlay / "reviewers.json").write_text(json.dumps({"reviewers": [
        {"family": "gpt", "cmd": [sys.executable, str(probe), "{prompt_file}"]}]}))
    monkeypatch.setenv("DS_OVERLAY_DIR", str(overlay))
    monkeypatch.setenv("SOME_COMPANY_SECRET", "x")
    code, report = run(tmp_path, "--analyst-family", "claude")
    assert code == 0 and report["results"][0]["ran"]
    log = open(os.path.join(report["results"][0]["dir"], "reviewer.log"), encoding="utf-8").read()
    cwd = log.split("CWD=")[1].split("\n")[0]
    assert cwd.startswith(tempfile.gettempdir()) and not cwd.startswith(str(tmp_path))
    assert not os.path.exists(cwd)  # cleaned up; only the record came back
    keys = log.split("KEYS=")[1].split("\n")[0].split(",")
    assert "SOME_COMPANY_SECRET" not in keys and "DS_QUERIES_LOG" in keys
    assert not os.path.exists(os.path.join(report["results"][0]["dir"], "warehouse.db"))


def test_two_runs_in_the_same_second_do_not_collide(setup):
    tmp = setup(["gpt"], {"sql": SQL, "findings": []})
    assert run(tmp, "--analyst-family", "claude")[0] == 0
    assert run(tmp, "--analyst-family", "claude")[0] == 0
    assert (tmp / "out" / ".gitignore").read_text().endswith("*\n")


def test_an_internal_error_is_exit_4_not_a_finding(setup, monkeypatch, capsys):
    tmp = setup(["gpt"], {"sql": SQL, "findings": []})
    monkeypatch.setattr(interrogate, "choose", lambda *a: 1 / 0)
    assert interrogate.main([os.path.join(RUN, "result.md"), "--request", os.path.join(ROOT, "eval", "fixtures", "f1", "task.md"),
                             "--db", DB, "--out", str(tmp / "out")]) == 4
    assert "ZeroDivisionError" in capsys.readouterr().err


def test_a_timeout_kills_everything_the_reviewer_started(tmp_path, monkeypatch):
    hang = tmp_path / "hang.py"
    hang.write_text("import subprocess, time\nsubprocess.Popen(['sleep', '313'])\ntime.sleep(60)\n")
    overlay = tmp_path / "overlay"
    overlay.mkdir()
    (overlay / "reviewers.json").write_text(json.dumps({"reviewers": [
        {"family": "gpt", "cmd": [sys.executable, str(hang), "{prompt_file}"]}]}))
    monkeypatch.setenv("DS_OVERLAY_DIR", str(overlay))
    code, report = run(tmp_path, "--analyst-family", "claude", "--timeout", "2")
    assert code == 2 and report["results"][0]["exit"] == "timeout"
    time.sleep(0.5)
    alive = subprocess.run(["pgrep", "-f", "sleep 313"], capture_output=True, text=True).stdout.strip()
    assert alive == ""


def test_family_names_are_compared_without_case_and_unknown_families_are_flagged(tmp_path, monkeypatch):
    overlay = tmp_path / "overlay"
    overlay.mkdir()
    monkeypatch.setenv("DS_OVERLAY_DIR", str(overlay))
    entry = {"cmd": [sys.executable, "-c", "pass"]}
    (overlay / "reviewers.json").write_text(json.dumps({"reviewers": [{**entry, "family": "GPT"}]}))
    assert interrogate.choose(interrogate.load_reviewers(), "gpt", 1)[1].startswith("not independent")
    (overlay / "reviewers.json").write_text(json.dumps({"reviewers": [{**entry, "model": "mystery-9"}]}))
    assert "family is unknown" in interrogate.choose(interrogate.load_reviewers(), "claude", 1)[1]
    assert interrogate.family_of("sonnet-4.5") == interrogate.family_of("opus-4[1m]") == "claude"
    (overlay / "reviewers.json").write_text(json.dumps({"reviewers": [{"family": "gpt"}, {**entry, "family": "claude"}]}))
    assert [r["family"] for r in interrogate.load_reviewers()] == ["claude"]
