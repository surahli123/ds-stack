"""cold_read.py validates the spine, grades replies against it, and works without the CLI."""

import json
import os
import subprocess
import sys

import cold_read
import pytest
from conftest import ROOT

TOOL = os.path.join(ROOT, "skills", "cold-read", "tools", "cold_read.py")
SPINE = {"type": "readout", "reader": "Dana, the PM",
         "answer": "Keep ranker v2: the 2.1 pp CTR drop is a mobile traffic mix shift.",
         "decision": "Do not roll back v2; ask growth to explain the mobile jump.",
         "takeaways": ["CTR fell 2.1 pp but did not move within desktop or mobile.",
                       "Mobile share of searches rose from 40% to 55%.",
                       "There is no holdout, so a small v2 effect would not show."]}
GOOD = {"skim": "1. Answer: keep ranker v2; the 2.1 pp CTR drop is a mobile traffic mix shift\n"
                "2. Decision: do not roll back v2 and ask growth about the mobile jump\n3. Number: -2.1 pp",
        "full": "1. Answer: keep v2, the 2.1 pp drop is mobile mix\n2. Decision: do not roll back; ask growth\n"
                "3. Number: mobile share rose from 40% to 55%; CTR did not move within desktop or mobile\n"
                "4. Caveat: no holdout, so a small v2 effect would not show\n5. Lost: nowhere\n6. Question: why did mobile grow?"}
BURIED = {"skim": "1. Answer: unclear\n2. Decision: unclear\n3. Number: unclear",
          "full": "1. Answer: the team pulled two weeks of logs\n2. Decision: unclear\n3. Number: 14 days\n"
                  "4. Caveat: unclear\n5. Lost: the whole first page\n6. Question: what should I do?"}


def test_good_replies_pass_and_buried_ones_fail():
    assert cold_read.grade(SPINE, GOOD)["pass"]
    result = cold_read.grade(SPINE, BURIED)
    assert not result["pass"] and result["skim"] == "0/2"


def test_a_wrong_number_is_never_a_match():
    assert cold_read.overlap("Mobile share rose from 40% to 55%.", "mobile share rose from 40% to 65%") == 0.0


@pytest.mark.parametrize("bad", [
    {k: v for k, v in SPINE.items() if k != "decision"},
    {**SPINE, "takeaways": SPINE["takeaways"][:2]},
    {**SPINE, "answer": " ".join(["word"] * 31)},
])
def test_spine_is_validated(tmp_path, bad):
    path = tmp_path / "spine.json"
    path.write_text(json.dumps(bad))
    with pytest.raises(ValueError):
        cold_read.load_spine(str(path))


def test_cli_without_claude_uses_prompts_then_replies(tmp_path):
    doc, spine, replies = tmp_path / "doc.md", tmp_path / "spine.json", tmp_path / "replies.json"
    doc.write_text("# Readout\n\n## Answer\nKeep ranker v2.\n")
    spine.write_text(json.dumps(SPINE))
    replies.write_text(json.dumps(GOOD))
    env = {**os.environ, "PATH": "/nonexistent"}
    shown = subprocess.run([sys.executable, TOOL, str(doc), "--spine", str(spine), "--prompts-only"],
                           capture_output=True, text=True, env=env)
    assert shown.returncode == 0 and "Dana, the PM" in shown.stdout and "Keep ranker v2." in shown.stdout
    graded = subprocess.run([sys.executable, TOOL, str(doc), "--spine", str(spine), "--replies", str(replies)],
                            capture_output=True, text=True, env=env)
    assert graded.returncode == 0 and "cold-read: skim 2/2, full 3/3 - pass" in graded.stdout
    assert json.loads((tmp_path / "cold_read.json").read_text())["pass"]
