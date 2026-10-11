#!/usr/bin/env python3
"""Run the cold read: a fresh reader answers fixed questions, graded against the spine.

    python3 cold_read.py doc.md --spine spine.json              # runs the reader with `claude -p`
    python3 cold_read.py doc.md --spine spine.json --prompts-only   # prints the prompts for a subagent
    python3 cold_read.py doc.md --spine spine.json --replies replies.json   # grades replies you collected

The spine is written before the draft (ds-doc step 2):

    {"type": "readout", "reader": "the PM who owns the launch",
     "answer": "...", "decision": "...", "takeaways": ["...", "...", "..."]}

Grading is done here, not by the author: each key item is matched against the
reader's answer lines by shared content words and numbers, and items that
don't match are checked by a separate grader call when `claude` is available.
Writes cold_read.json next to the doc. Exit 0 pass, 1 fail, 2 usage error.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import skim_view  # noqa: E402

PROMPTS = os.path.join(os.path.dirname(HERE), "references", "reader-prompts.md")
STOP = set("""a an the and or but if then of to in on at by for with from as is are was were be been this that these those it
its we you your our they their not no can could should would will may might must do does did have has had into than so
also just more most less about over under all any each some other which who what when where why how there here""".split())
KEYS = {1: "answer", 2: "decision", 3: "number", 4: "caveat", 5: "lost", 6: "question"}


def load_spine(path):
    with open(path, encoding="utf-8") as handle:
        spine = json.load(handle)
    missing = [k for k in ("reader", "answer", "decision", "takeaways") if not spine.get(k)]
    if missing:
        raise ValueError(f"spine is missing {', '.join(missing)}")
    if not isinstance(spine["takeaways"], list) or len(spine["takeaways"]) != 3:
        raise ValueError("spine needs exactly three takeaways")
    if len(spine["answer"].split()) > 30:
        raise ValueError("the spine's answer is over 30 words; tighten it before drafting")
    return spine


def prompts(doc, spine):
    with open(PROMPTS, encoding="utf-8") as handle:
        skim_prompt, full_prompt = re.findall(r"```\n(.*?)```", handle.read(), re.S)[:2]
    fill = lambda p, text: p.replace("{role}", spine["reader"]).replace("{text}", text)  # noqa: E731
    return {"skim": fill(skim_prompt, skim_view.skim(doc)), "full": fill(full_prompt, doc)}


def ask(prompt, model):
    work = tempfile.mkdtemp(prefix="cold-read-")
    try:
        proc = subprocess.run(["claude", "-p", prompt, "--model", model, "--disallowedTools",
                               "Bash,Read,Write,Edit,Glob,Grep,Task,Agent,WebFetch,WebSearch"],
                              cwd=work, capture_output=True, text=True, timeout=300)
        return proc.stdout
    finally:
        shutil.rmtree(work, ignore_errors=True)


def answer_lines(reply):
    lines = {}
    for line in reply.splitlines():
        match = re.match(r"^\s*\**\s*([1-6])[.)]\s*(.*)$", line)
        if match:
            lines[KEYS[int(match.group(1))]] = re.sub(r"^\**\s*\w+\s*:\**\s*", "", match.group(2)).strip()
    return lines


def tokens(text):
    words = re.findall(r"[a-z0-9][a-z0-9.%_-]*", text.lower().replace("−", "-"))
    return {w.rstrip(".") for w in words if w not in STOP and (len(w) > 2 or any(c.isdigit() for c in w))}


def overlap(key, text):
    want = tokens(key)
    if not want:
        return 1.0
    numbers = {w for w in want if any(c.isdigit() for c in w)}
    have = tokens(text)
    if numbers and not numbers <= have:
        return 0.0
    return len(want & have) / len(want)


def judge(pairs, model):
    """Ask a separate grader whether each reader answer conveys its key fact."""
    prompt = ("For each pair, say whether the reader's answer conveys the same fact as the key. "
              "Paraphrase is fine; a missing or different number is not. Reply with only a JSON list of true/false.\n\n"
              + json.dumps([{"key": k, "reader": r} for k, r in pairs], indent=1))
    reply = ask(prompt, model)
    match = re.search(r"\[[^\]]*\]", reply)
    try:
        verdicts = json.loads(match.group(0)) if match else []
    except ValueError:
        verdicts = []
    return verdicts if len(verdicts) == len(pairs) else [False] * len(pairs)


def grade(spine, replies, model=None):
    skim, full = answer_lines(replies["skim"]), answer_lines(replies["full"])
    items = [("skim", "answer", spine["answer"], skim.get("answer", "") + " " + skim.get("decision", "")),
             ("skim", "decision", spine["decision"], skim.get("decision", "") + " " + skim.get("answer", ""))]
    full_text = " ".join(full.get(k, "") for k in ("answer", "decision", "number", "caveat"))
    items += [("full", f"takeaway {n}", t, full_text) for n, t in enumerate(spine["takeaways"], 1)]
    results = []
    for mode, name, key, text in items:
        score = overlap(key, text)
        results.append({"pass": mode, "item": name, "key": key, "reader": text.strip(),
                        "got": score >= 0.5, "how": f"overlap {score:.0%}"})
    unsure = [r for r in results if not r["got"] and r["reader"]]
    if unsure and model and shutil.which("claude"):
        for r, ok in zip(unsure, judge([(r["key"], r["reader"]) for r in unsure], model)):
            if ok:
                r["got"], r["how"] = True, r["how"] + "; grader: same fact"
    skim_got = sum(r["got"] for r in results if r["pass"] == "skim")
    full_got = sum(r["got"] for r in results if r["pass"] == "full")
    passed = skim_got == 2 and full_got == 3
    return {"pass": passed, "skim": f"{skim_got}/2", "full": f"{full_got}/3", "items": results,
            "lost": full.get("lost", ""), "question": full.get("question", "")}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("doc")
    parser.add_argument("--spine", required=True)
    parser.add_argument("--replies", help="JSON {'skim': ..., 'full': ...} collected from a subagent")
    parser.add_argument("--prompts-only", action="store_true")
    parser.add_argument("--reader-model", default="haiku")
    args = parser.parse_args(argv)
    try:
        spine = load_spine(args.spine)
        with open(args.doc, encoding="utf-8") as handle:
            doc = handle.read()
    except (OSError, ValueError) as err:
        print(f"cold_read: {err}", file=sys.stderr)
        return 2

    texts = prompts(doc, spine)
    if args.prompts_only:
        for mode in ("skim", "full"):
            print(f"===== {mode} prompt: send to a fresh subagent with nothing else =====\n{texts[mode]}\n")
        print('Save the two replies as {"skim": "...", "full": "..."} and rerun with --replies.')
        return 0
    if args.replies:
        with open(args.replies, encoding="utf-8") as handle:
            replies = json.load(handle)
    elif shutil.which("claude"):
        replies = {mode: ask(texts[mode], args.reader_model) for mode in ("skim", "full")}
    else:
        print("cold_read: no `claude` CLI here; rerun with --prompts-only, then --replies", file=sys.stderr)
        return 2

    result = grade(spine, replies, args.reader_model)
    result["replies"] = replies
    out = os.path.join(os.path.dirname(os.path.abspath(args.doc)), "cold_read.json")
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
    for r in result["items"]:
        print(f"{'got   ' if r['got'] else 'MISSED'} {r['pass']:4} {r['item']:10} key: {r['key'][:70]}")
    if result["lost"]:
        print(f"reader got lost: {result['lost']}")
    print(f"cold-read: skim {result['skim']}, full {result['full']} - {'pass' if result['pass'] else 'fail'}")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
