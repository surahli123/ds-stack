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


ZH_SPINE = {"type": "readout", "reader": "能源业务的产品经理",
            "answer": "德国提高得更多：48.5 个百分点，法国 14.2 个。",
            "decision": "优先看德国的做法。",
            "misread": "可再生能源不含核电，所以法国的比例偏低。",
            "takeaways": ["德国 2014 年首次达到 25%。", "法国到 2023 年才达到 25%。", "两国每年都有数据。"]}


def test_chinese_keys_need_shared_words_now():
    assert cold_read.overlap("两国每年都有数据。", "我不知道") < 0.5
    assert cold_read.overlap("两国每年都有数据。", "两国每年都有数据，没有缺失") >= 0.5
    assert cold_read.overlap("德国提高 48.5 个百分点", "德国提高了 48.5 个百分点") >= 0.5


def test_unclear_words_and_clashes_fail_a_full_read():
    clear = {**GOOD, "full": GOOD["full"] + "\n7. Words: none\n8. Clash: none"}
    assert cold_read.grade(SPINE, clear)["pass"]
    jargon = {**GOOD, "full": GOOD["full"] + "\n7. Words: renewables_share_elec, change_pp\n8. Clash: none"}
    result = cold_read.grade(SPINE, jargon)
    assert not result["pass"] and result["unclear_words"].startswith("renewables_share_elec")
    clash = {**GOOD, "full": GOOD["full"] + "\n7. Words: 无\n8. Clash: '不知道是否有缺值' vs '没有缺失'"}
    assert not cold_read.grade(SPINE, clash)["pass"]


def test_the_misread_definition_is_graded_and_vocabulary_fills_the_prompt():
    replies = {"skim": "1. Answer: 德国提高得更多，48.5 个百分点，法国 14.2 个\n2. Decision: 优先看德国的做法\n3. Number: 48.5 个百分点",
               "full": "1. Answer: 德国提高得更多，48.5 个百分点，法国 14.2 个\n2. Decision: 优先看德国的做法\n"
                       "3. Number: 德国 2014 年首次达到 25%，法国到 2023 年才达到 25%，两国每年都有数据\n"
                       "4. Caveat: 可再生能源不含核电，所以法国的比例偏低\n5. Lost: nowhere\n6. Question: 核电算低碳吗？\n"
                       "7. Words: 无\n8. Clash: 无"}
    result = cold_read.grade(ZH_SPINE, replies)
    assert result["pass"] and result["full"] == "4/4"
    no_caveat = {**replies, "full": replies["full"].replace("可再生能源不含核电，所以法国的比例偏低", "unclear")}
    assert cold_read.grade(ZH_SPINE, no_caveat)["full"] == "3/4"
    text = cold_read.prompts("# 文档", ZH_SPINE)["full"]
    assert "You know your business and its products, but not data-science" in text and "{vocabulary}" not in text


def test_a_long_chinese_answer_is_refused(tmp_path):
    path = tmp_path / "spine.json"
    path.write_text(json.dumps({**ZH_SPINE, "answer": "德国提高得更多" * 9}), encoding="utf-8")
    with pytest.raises(ValueError):
        cold_read.load_spine(str(path))


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
