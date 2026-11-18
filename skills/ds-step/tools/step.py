#!/usr/bin/env python3
"""Keep a long data-science project on its aim: one step per session, closed questions, and a gate before each run.

    step.py init --aim "<decision the project serves>" --bar "<result that settles it>"
    step.py card --aim "..." --done "..." --scope "..." [--scope ...] --out "..." --budget 90m --ask "..." [--freeze <file> ...]
    step.py start                      # check the card, hash it and the frozen files, print the brief
    step.py brief                      # what a session reads first; refuses if state was changed outside step.py
    step.py decide "<question a run will settle>"            # -> D<n>
    step.py run --decision D1 --if "<result -> choice>" [--new-design "..."] -- <command ...>
    step.py verdict R1 changed|no-change|inconclusive "<one line>"   # changed or no-change closes the decision
    step.py close "<question>" "<answer>" [--evidence <pointer>]     # -> C<n>
    step.py reopen C3 --reason "<new evidence>"
    step.py park "<idea that is not this step>"
    step.py end "<what the step produced>" [--abandon]
    step.py render                     # rewrite DS-STATE.md from the event log, discarding hand edits

State lives in .ds-step/events.jsonl at the project root (the first parent folder that has one, as git finds
.git; $DS_STEP_ROOT overrides). It is append-only: every command adds events, none rewrites them.
DS-STATE.md is rendered from it, so an edit made anywhere else (another session, another harness, git pull)
is found at the next brief, run or end. At start the card and each frozen file are hashed; a changed hash
stops run and end until the step is ended with --abandon.

The run gate refuses a run without a started step, an open decision id, or an --if line; while the last run
has no verdict; and after two verdicts in the step that were not `changed`, unless --new-design says what
changed. Each run's output streams to .ds-step/runs/R<n>.log; only its summary lines are printed.

Exit code: 0 done, 1 refused (the reason is printed), 3 usage error.
"""

import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
import re
import subprocess
import sys

MAX_SCOPE = 5
VERDICTS = ("changed", "no-change", "inconclusive")
SUMMARY_LINES, SUMMARY_CHARS = 8, 1500
TOOL = os.path.abspath(__file__)


class Refused(Exception):
    pass


def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def find_root(start=None):
    """The project root: $DS_STEP_ROOT, else the nearest folder at or above start holding .ds-step/events.jsonl."""
    if os.environ.get("DS_STEP_ROOT"):
        return os.path.abspath(os.environ["DS_STEP_ROOT"])
    folder = os.path.abspath(start or os.getcwd())
    while True:
        if os.path.exists(os.path.join(folder, ".ds-step", "events.jsonl")):
            return folder
        parent = os.path.dirname(folder)
        if parent == folder:
            return None
        folder = parent


def paths(root):
    base = os.path.join(root, ".ds-step")
    return {"events": os.path.join(base, "events.jsonl"), "runs": os.path.join(base, "runs"),
            "lock": os.path.join(base, "lock"), "state": os.path.join(root, "DS-STATE.md")}


def sha(path):
    try:
        with open(path, "rb") as handle:
            return hashlib.sha256(handle.read()).hexdigest()
    except OSError:
        return "missing"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def budget_minutes(value):
    match = re.match(r"^\s*(\d+(?:\.\d+)?)\s*(m|min|mins|minutes|h|hr|hrs|hours)\s*$", value or "", re.I)
    if not match:
        return None
    return int(float(match.group(1)) * (60 if match.group(2).lower().startswith("h") else 1))


# --- events and the state they fold into --------------------------------------------------------

def load(root):
    with open(paths(root)["events"], encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def append(root, event):
    event = {"ts": now().isoformat(), **event}
    with open(paths(root)["events"], "a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


def fold(events):
    s = {"aim": "", "bar": "", "card": None, "step": None, "decisions": {}, "closed": {}, "parked": [],
         "runs": {}, "n": {"D": 0, "C": 0, "R": 0, "step": 0}, "ended_sessions": set(), "recent": []}
    for e in events:
        kind = e["type"]
        if kind == "init":
            s["aim"], s["bar"] = e["aim"], e["bar"]
        elif kind == "card":
            s["card"] = e["card"]
        elif kind == "start":
            s["n"]["step"] += 1
            s["step"] = {"n": s["n"]["step"], "ts": e["ts"], "session": e.get("session"), "hashes": e["hashes"]}
        elif kind == "end":
            if s["step"] and s["step"].get("session"):
                s["ended_sessions"].add(s["step"]["session"])
            s["step"], s["card"] = None, None
        elif kind == "decide":
            s["n"]["D"] += 1
            s["decisions"][e["id"]] = {"question": e["question"], "closed_by": None}
        elif kind == "close":
            s["n"]["C"] += 1
            s["closed"][e["id"]] = e
            if e.get("decision"):
                s["decisions"][e["decision"]]["closed_by"] = e["id"]
        elif kind == "reopen":
            entry = s["closed"].pop(e["id"])
            if entry.get("decision"):
                s["decisions"][entry["decision"]]["closed_by"] = None
        elif kind == "park":
            s["parked"].append(e)
        elif kind == "run":
            s["n"]["R"] += 1
            s["runs"][e["id"]] = {**e, "verdict": None, "step": s["step"]["n"] if s["step"] else None}
        elif kind == "verdict":
            s["runs"][e["run"]]["verdict"] = e["verdict"]
        s["recent"].append(e)
    return s


def describe(e):
    kind, day = e["type"], e["ts"][:16].replace("T", " ")
    text = {"init": "project started", "card": f"card written: {e.get('card', {}).get('aim', '')}",
            "start": "step started", "end": f"step ended{' (abandoned)' if e.get('abandon') else ''}: "
            f"{e.get('summary', '')}", "decide": f"{e.get('id')} opened: {e.get('question', '')}",
            "close": f"{e.get('id')} closed", "reopen": f"{e.get('id')} reopened: {e.get('reason', '')}",
            "park": "idea parked", "run": f"{e.get('id')} ran for {e.get('decision')}",
            "verdict": f"{e.get('run')} {e.get('verdict')}: {e.get('note', '')}"}.get(kind, kind)
    return f"- {day} {text}"


def render(s):
    """DS-STATE.md, deterministic, so any change made outside step.py shows as a difference."""
    out = ["# Project state", "", f"Written by `{TOOL}` from .ds-step/events.jsonl. Change it only through "
           "that tool; a hand edit is refused at the next brief, run or end.", "",
           "## Aim", s["aim"], "", "## Success bar", s["bar"], "", "## Step"]
    card = s["card"]
    if not card:
        out.append("No card. Write one with `step.py card ...` before the next step.")
    else:
        out += [f"Aim: {card['aim']}", f"Done when: {card['done']}", "In scope:"]
        out += [f"{i}. {item}" for i, item in enumerate(card["scope"], 1)]
        out += [f"Out of scope: {card['out']}", f"Budget: {card['budget']}", f"Stop and ask: {card['ask']}"]
        if s["step"]:
            out.append(f"Started: {s['step']['ts']} (step {s['step']['n']})")
    out += ["", "## Frozen"] + [f"- {p}" for p in (card or {}).get("frozen", [])]
    out += ["", "## Open decisions"] + [f"- {d}: {v['question']}" for d, v in s["decisions"].items()
                                        if not v["closed_by"]]
    out += ["", "## Closed"]
    for cid, e in s["closed"].items():
        evidence = f"; {e['evidence']}" if e.get("evidence") else ""
        out.append(f"- {cid}: {e['question']} -> {e['answer']} ({e['ts'][:10]}{evidence})")
    parked = s["parked"]
    out += ["", "## Parking lot"] + [f"- {e['ts'][:10]} {e['idea']}" for e in parked[-10:]]
    if len(parked) > 10:
        out.append(f"- ... {len(parked) - 10} older in .ds-step/events.jsonl")
    out += ["", "## Recent"] + [describe(e) for e in s["recent"][-8:]]
    return "\n".join(out) + "\n"


def write_state(root, s):
    with open(paths(root)["state"], "w", encoding="utf-8") as handle:
        handle.write(render(s))


def drift(root, s):
    """What changed outside step.py: DS-STATE.md, and while a step runs, the card or a frozen file."""
    problems = []
    try:
        with open(paths(root)["state"], encoding="utf-8") as handle:
            current = handle.read()
    except OSError:
        current = None
    if current != render(s):
        problems.append("DS-STATE.md was changed outside step.py. Put the change through step.py, or discard it "
                        "with `step.py render`")
    if s["step"]:
        hashes = s["step"]["hashes"]
        if digest([s["aim"], s["bar"], s["card"]]) != hashes["card"]:
            problems.append("the Aim, Success bar or Step card changed in the event log since start")
        for rel, recorded in hashes["frozen"].items():
            if sha(os.path.join(root, rel)) != recorded:
                problems.append(f"frozen file {rel} changed since the step started")
    return problems


def require_clean(root, s):
    problems = drift(root, s)
    if problems:
        tail = (" Instructions must not change mid-step: end it with `step.py end \"...\" --abandon` and start a "
                "new step." if s["step"] else "")
        raise Refused("; ".join(problems) + "." + tail)


@contextlib.contextmanager
def locked(root):
    with open(paths(root)["lock"], "w") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


# --- commands -----------------------------------------------------------------------------------

def brief(root, s):
    lines = render(s).split("\n## Recent")[0].splitlines()[4:]
    if s["step"]:
        used = int((now() - dt.datetime.fromisoformat(s["step"]["ts"])).total_seconds() // 60)
        limit = budget_minutes(s["card"]["budget"])
        over = " OVER BUDGET: end the step or ask the owner." if used > limit else ""
        lines.insert(0, f"Step {s['step']['n']} running: {used} of {limit} min used.{over}")
    else:
        lines.insert(0, "No step running.")
    pending = [r for r in s["runs"].values() if not r["verdict"]]
    if pending:
        lines.insert(1, f"Run {pending[-1]['id']} has no verdict yet; record it before another run.")
    lines.append(f"Tool: python3 {TOOL}")
    return "\n".join(line for line in lines if line.strip())


def check_card(root, args):
    problems = []
    for name in ("aim", "done", "out", "ask"):
        if not getattr(args, name).strip():
            problems.append(f"--{name} is empty")
    if not 1 <= len(args.scope) <= MAX_SCOPE:
        problems.append(f"{len(args.scope)} in-scope steps; give 1 to {MAX_SCOPE} (--scope each). Split the step")
    if budget_minutes(args.budget) is None:
        problems.append("--budget must be a time box such as 90m or 2h")
    frozen = []
    for given in args.freeze:
        rel = os.path.normpath(given)
        if "\\" in given or os.path.isabs(given) or rel.startswith(".."):
            problems.append(f"frozen path {given!r}: give a path relative to the project root, with /")
        elif not os.path.isfile(os.path.join(root, rel)):
            problems.append(f"frozen path {given!r} is not a file under {root}")
        else:
            frozen.append(rel)
    if problems:
        raise Refused("the card is not ready:\n  " + "\n  ".join(problems))
    return {"aim": args.aim, "done": args.done, "scope": args.scope, "out": args.out, "budget": args.budget,
            "ask": args.ask, "frozen": frozen}


def summarize(text, pattern):
    lines = [ln for ln in text.splitlines() if ln.strip()]
    picked = [ln for ln in lines if re.search(pattern, ln)] if pattern else []
    return "\n".join(ln[:300] for ln in (picked or lines)[-SUMMARY_LINES:])[-SUMMARY_CHARS:]


def gate(s, args):
    if not s["step"]:
        raise Refused("no step is started; write a card and run `step.py start`")
    decision = s["decisions"].get(args.decision)
    if not decision:
        raise Refused(f"no decision {args.decision or '(none given)'}; open one with `step.py decide \"...\"`. "
                      "If no decision depends on the result, don't run it")
    if decision["closed_by"]:
        raise Refused(f"{args.decision} is closed by {decision['closed_by']}; reopen it with new evidence first")
    if not args.expect.strip():
        raise Refused("say which result would change the decision, and to what (--if)")
    runs = [r for r in s["runs"].values() if r["step"] == s["step"]["n"]]
    if runs and not runs[-1]["verdict"]:
        raise Refused(f"run {runs[-1]['id']} has no verdict; read its summary against its --if line and record "
                      f"`step.py verdict {runs[-1]['id']} changed|no-change|inconclusive \"...\"` first")
    since = runs
    for i, r in enumerate(runs):
        if r.get("new_design"):
            since = runs[i:]
    judged = [r for r in since if r["verdict"] != "failed"]
    if len(judged) >= 2 and all(r["verdict"] != "changed" for r in judged[-2:]) and not args.new_design:
        raise Refused(f"the last two runs in this step ({judged[-2]['id']}, {judged[-1]['id']}) changed nothing. "
                      "Change the design (more rows, a held-out set, a different measure) and say how with "
                      "--new-design, or end the step and tell the owner")


def run(root, args):
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        raise Refused("no command after --")
    with locked(root):
        s = fold(load(root))
        require_clean(root, s)
        gate(s, args)
        run_id = f"R{s['n']['R'] + 1}"
        os.makedirs(paths(root)["runs"], exist_ok=True)
        log = os.path.join(paths(root)["runs"], f"{run_id}.log")
        append(root, {"type": "run", "id": run_id, "decision": args.decision, "if": args.expect,
                      "command": command, "log": os.path.relpath(log, root), "new_design": args.new_design})
        write_state(root, fold(load(root)))
    try:
        with open(log, "wb") as handle:
            code = subprocess.run(command, stdout=handle, stderr=subprocess.STDOUT).returncode
    except OSError as error:
        with locked(root):
            append(root, {"type": "verdict", "run": run_id, "verdict": "failed", "note": f"did not launch: {error}"})
            write_state(root, fold(load(root)))
        raise Refused(f"{run_id} did not launch: {error}")
    with open(log, encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    print(f"{run_id} exit {code}; full output in {log} ({len(text.splitlines())} lines, not shown)")
    print(f"Decision {args.decision}: {s['decisions'][args.decision]['question']} | If: {args.expect}")
    print(summarize(text, args.summary))
    print(f"Next: `step.py verdict {run_id} changed|no-change|inconclusive \"<one line>\"`")
    return 0


def dispatch(args):
    if args.cmd == "init":
        root = find_root()
        if root:
            raise Refused(f"a project already exists at {root}; run step.py from there or below it")
        root = os.path.abspath(os.getcwd())
        os.makedirs(os.path.join(root, ".ds-step"), exist_ok=True)
        with open(os.path.join(root, ".ds-step", ".gitignore"), "w") as handle:
            handle.write("runs/\nlock\n")
        if not args.aim.strip() or not args.bar.strip():
            raise Refused("give the project --aim and --bar")
        append(root, {"type": "init", "aim": args.aim, "bar": args.bar})
        write_state(root, fold(load(root)))
        print(f"started a project at {root}; write a card with `step.py card ...`")
        return 0
    root = find_root()
    if not root:
        raise Refused("no ds-step project here or above; run `step.py init` at the project root")
    if args.cmd == "run":
        return run(root, args)
    with locked(root):
        s = fold(load(root))
        if args.cmd == "render":
            write_state(root, s)
            print("DS-STATE.md rewritten from the event log")
            return 0
        if args.cmd == "brief":
            require_clean(root, s)
            print(brief(root, s))
            return 0
        if args.cmd == "end" and args.abandon:
            if not s["step"]:
                raise Refused("no step is started")
            reason = "; ".join(drift(root, s)) or "abandoned by request"
            append(root, {"type": "end", "summary": f"{args.summary} ({reason})", "abandon": True})
            write_state(root, fold(load(root)))
            print("step abandoned; write a new card for the next session")
            return 0
        require_clean(root, s)
        message = command(root, s, args)
        write_state(root, fold(load(root)))
        print(message)
        return 0


def command(root, s, args):
    if args.cmd == "card":
        if s["step"]:
            raise Refused("a step is running; its card is frozen until `step.py end`")
        append(root, {"type": "card", "card": check_card(root, args)})
        return "card written; run `step.py start` in the session that does the step"
    if args.cmd == "start":
        if s["step"]:
            raise Refused("a step is already running; end it first. One step per session")
        if not s["card"]:
            raise Refused("no card; write one with `step.py card ...`")
        session = os.environ.get("DS_SESSION_ID")
        if session and session in s["ended_sessions"]:
            raise Refused("this session already ended a step. One step per session: start the next in a fresh one")
        hashes = {"card": digest([s["aim"], s["bar"], s["card"]]),
                  "frozen": {rel: sha(os.path.join(root, rel)) for rel in s["card"]["frozen"]}}
        append(root, {"type": "start", "session": session, "hashes": hashes})
        return brief(root, fold(load(root)))
    if args.cmd == "decide":
        did = f"D{s['n']['D'] + 1}"
        append(root, {"type": "decide", "id": did, "question": args.question})
        return did
    if args.cmd == "verdict":
        r = s["runs"].get(args.run_id)
        if not r:
            raise Refused(f"no run {args.run_id}")
        if r["verdict"]:
            raise Refused(f"{args.run_id} already has verdict {r['verdict']}; the log is append-only")
        append(root, {"type": "verdict", "run": args.run_id, "verdict": args.verdict, "note": args.note})
        if args.verdict == "inconclusive":
            return f"{args.run_id}: inconclusive"
        cid = f"C{s['n']['C'] + 1}"
        append(root, {"type": "close", "id": cid, "question": s["decisions"][r["decision"]]["question"],
                      "answer": args.note, "evidence": args.run_id, "decision": r["decision"]})
        return f"{args.run_id}: {args.verdict}; {r['decision']} closed as {cid}"
    if args.cmd == "close":
        cid = f"C{s['n']['C'] + 1}"
        append(root, {"type": "close", "id": cid, "question": args.question, "answer": args.answer,
                      "evidence": args.evidence})
        return cid
    if args.cmd == "reopen":
        if args.closed_id not in s["closed"]:
            raise Refused(f"no closed question {args.closed_id}")
        if not args.reason.strip():
            raise Refused("give the new evidence or contradiction (--reason)")
        append(root, {"type": "reopen", "id": args.closed_id, "reason": args.reason})
        return f"reopened {args.closed_id}; the reason is in the event log"
    if args.cmd == "park":
        append(root, {"type": "park", "idea": args.idea})
        return "parked"
    if args.cmd == "end":
        if not s["step"]:
            raise Refused("no step is started")
        pending = [r for r in s["runs"].values() if not r["verdict"]]
        if pending:
            raise Refused(f"run {pending[-1]['id']} has no verdict; record it before ending the step")
        used = int((now() - dt.datetime.fromisoformat(s["step"]["ts"])).total_seconds() // 60)
        limit = budget_minutes(s["card"]["budget"])
        over = f", over its {limit} min budget" if used > limit else ""
        append(root, {"type": "end", "summary": args.summary, "minutes": used})
        return f"step ended after {used} min{over}. Write the next card; start it in a fresh session"
    raise Refused(f"unknown command {args.cmd}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd")
    p = sub.add_parser("init")
    p.add_argument("--aim", required=True)
    p.add_argument("--bar", required=True)
    p = sub.add_parser("card")
    for name in ("aim", "done", "out", "ask", "budget"):
        p.add_argument(f"--{name}", required=True)
    p.add_argument("--scope", action="append", default=[])
    p.add_argument("--freeze", action="append", default=[], help="a file the step must not change")
    for name in ("start", "brief", "render"):
        sub.add_parser(name)
    p = sub.add_parser("decide")
    p.add_argument("question")
    p = sub.add_parser("run")
    p.add_argument("--decision", default="", help="the open decision id (D<n>) this run's result settles")
    p.add_argument("--if", dest="expect", default="", help="which result would change it, and to what")
    p.add_argument("--new-design", default="", help="after two runs that changed nothing: what is different now")
    p.add_argument("--summary", default=r"^(SUMMARY|RESULT|VERDICT)\b", help="regex for the output lines to print")
    p.add_argument("command", nargs=argparse.REMAINDER)
    p = sub.add_parser("verdict")
    p.add_argument("run_id")
    p.add_argument("verdict", choices=VERDICTS)
    p.add_argument("note")
    p = sub.add_parser("close")
    p.add_argument("question")
    p.add_argument("answer")
    p.add_argument("--evidence", default="")
    p = sub.add_parser("reopen")
    p.add_argument("closed_id")
    p.add_argument("--reason", required=True)
    p = sub.add_parser("park")
    p.add_argument("idea")
    p = sub.add_parser("end")
    p.add_argument("summary")
    p.add_argument("--abandon", action="store_true", help="end a step whose instructions changed under it")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exit_:
        return 3 if exit_.code else 0
    if not args.cmd:
        parser.print_usage(sys.stderr)
        return 3
    try:
        return dispatch(args)
    except Refused as refusal:
        print(f"step.py: refused. {refusal}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
