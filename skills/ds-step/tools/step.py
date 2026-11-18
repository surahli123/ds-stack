#!/usr/bin/env python3
"""Keep a long data-science project on its aim: one step per session, settled decisions, a gate before each run.

    step.py init --aim "<decision the project serves>" --bar "<result that settles it>"
    step.py card --aim "..." --done "..." --scope "..." [--scope ...] --out "..." --budget 90m --ask "..." [--freeze <file> ...]
    step.py start                      # hash the card and the frozen files, print the brief
    step.py brief                      # what a session reads first, at most about 2,000 characters
    step.py decide "<question>" [--answer "..." --evidence <pointer>]   # opens D-xxxx, or records it settled
    step.py run --decision D-xxxx --if "<result -> choice>" [--new-design "..."] -- <command ...>
    step.py verdict R-xxxx changed|no-change|inconclusive "<one line>"  # changed / no-change settle the decision
    step.py reopen D-xxxx --reason "<new evidence>"
    step.py park "<idea that is not this step>"
    step.py end "<what the step produced>" [--abandon]

State is .ds-step/events.jsonl at the project root (the nearest parent folder that has one; $DS_STEP_ROOT
overrides). Commands only append to it; ids carry a random suffix and the file merges with git's union driver,
so branches can be merged. DS-STATE.md is a view written after every command; it is gitignored.

At start the card and each frozen file are hashed. If either changes while the step runs, by any route,
run and end refuse until the step is ended with --abandon. The run gate refuses a run without a started step,
an open decision, or an --if line; while another run has no verdict; and after two runs in the step that
changed nothing, unless --new-design says what changed. Output streams to .ds-step/runs/<id>.log and only
its summary lines are printed.

Exit code: 0 done, 1 refused (the reason is printed), 3 usage error.
"""

import argparse
import contextlib
import datetime as dt
import hashlib
import json
import os
import re
import secrets
import subprocess
import sys

try:
    import fcntl
except ImportError:  # Windows: no lock, so start one run at a time
    fcntl = None

MAX_SCOPE, BRIEF_CHARS = 5, 2000
SUMMARY_LINES, SUMMARY_CHARS = 8, 1500
TOOL = os.path.abspath(__file__)


class Refused(Exception):
    pass


def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def find_root(*starts):
    """$DS_STEP_ROOT, else the nearest folder at or above any start that holds .ds-step/events.jsonl."""
    if os.environ.get("DS_STEP_ROOT"):
        return os.path.abspath(os.environ["DS_STEP_ROOT"])
    for start in [s for s in starts if s] or [os.getcwd()]:
        folder = os.path.abspath(start)
        while True:
            if os.path.exists(os.path.join(folder, ".ds-step", "events.jsonl")):
                return folder
            if os.path.dirname(folder) == folder:
                break
            folder = os.path.dirname(folder)
    return None


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
    return int(float(match.group(1)) * (60 if match.group(2).lower()[0] == "h" else 1)) if match else None


def minutes_since(ts):
    return int((now() - dt.datetime.fromisoformat(ts)).total_seconds() // 60)


def new_id(prefix):
    return f"{prefix}-{secrets.token_hex(2)}"


def pid_alive(pid):
    if not pid or os.name == "nt":  # os.kill(pid, 0) would terminate the process on Windows
        return False
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ValueError):
        return False


# --- events and the state they fold into --------------------------------------------------------

def events_path(root):
    return os.path.join(root, ".ds-step", "events.jsonl")


def load(root):
    events = []
    with open(events_path(root), encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if line.strip():
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    raise Refused(f".ds-step/events.jsonl line {number} is not an event (a merge conflict?): "
                                  f"{line.strip()[:60]!r}. Keep both sides' lines and delete the markers")
    return sorted(events, key=lambda e: e["ts"])  # stable: a union merge keeps each side in order


def append(root, event):
    with open(events_path(root), "a", encoding="utf-8") as handle:
        handle.write(json.dumps({"ts": now().isoformat(), **event}, ensure_ascii=False) + "\n")


def fold(events):
    s = {"aim": "", "bar": "", "card": None, "step": None, "steps": 0, "decisions": {}, "parked": [],
         "runs": {}, "ended_sessions": set(), "recent": events[-8:]}

    def known(table, key, what):
        if key not in s[table]:
            raise Refused(f"the event log names {what} {key}, which it never created")
        return s[table][key]

    for e in events:
        kind = e["type"]
        if kind in ("decide", "run") and e["id"] in s["decisions"].keys() | s["runs"].keys():
            raise Refused(f"the event log creates {e['id']} twice; after a merge, rename one of them")
        if kind == "init":
            s["aim"], s["bar"] = e["aim"], e["bar"]
        elif kind == "card":
            s["card"] = e["card"]
        elif kind == "start":
            s["steps"] += 1
            s["step"] = {"n": s["steps"], "ts": e["ts"], "session": e.get("session"), "hashes": e["hashes"]}
        elif kind == "end":
            s["ended_sessions"] |= {x for x in (e.get("session"), (s["step"] or {}).get("session")) if x}
            for r in s["runs"].values():
                if e.get("abandon") and s["step"] and r["step"] == s["step"]["n"] and not r["verdict"]:
                    r["verdict"] = "abandoned"
            s["step"], s["card"] = None, None
        elif kind == "decide":
            s["decisions"][e["id"]] = {"question": e["question"], "answer": e.get("answer"),
                                       "evidence": e.get("evidence", ""), "ts": e["ts"]}
        elif kind == "reopen":
            known("decisions", e["id"], "decision")["answer"] = None
        elif kind == "park":
            s["parked"].append(e)
        elif kind == "run":
            s["runs"][e["id"]] = {**e, "verdict": None, "finished": False, "step": (s["step"] or {}).get("n")}
        elif kind == "finished":
            run = known("runs", e["run"], "run")
            run.update(finished=True, exit=e.get("exit"))
            if e.get("error"):
                run["verdict"] = "failed"
        elif kind == "verdict":
            run = known("runs", e["run"], "run")
            run["verdict"] = e["verdict"]
            if e["verdict"] in ("changed", "no-change"):
                known("decisions", run["decision"], "decision").update(answer=e["note"], evidence=e["run"],
                                                                        ts=e["ts"])
    return s


def drift(root, s):
    """What changed under a running step: the card (in the log) or a frozen file (anywhere)."""
    if not s["step"]:
        return []
    hashes, problems = s["step"]["hashes"], []
    if digest([s["aim"], s["bar"], s["card"]]) != hashes["card"]:
        problems.append("the Aim, Success bar or card changed in the event log since start")
    problems += [f"frozen file {rel} changed since the step started" for rel, recorded in hashes["frozen"].items()
                 if sha(os.path.join(root, rel)) != recorded]
    return problems


def require_clean(root, s):
    problems = drift(root, s)
    if problems:
        raise Refused("; ".join(problems) + ". Instructions must not change mid-step: run "
                      "`step.py end \"...\" --abandon` and write a new card")


@contextlib.contextmanager
def locked(root):
    with open(os.path.join(root, ".ds-step", "lock"), "w") as handle:
        if fcntl:
            fcntl.flock(handle, fcntl.LOCK_EX)
        yield


# --- views --------------------------------------------------------------------------------------

def settled(s):
    return [(d, v) for d, v in s["decisions"].items() if v["answer"]]


def view(s):
    """DS-STATE.md: the full picture for a person. Derived and gitignored; the agent reads the brief."""
    card = s["card"]
    out = ["# Project state", "", "Written by step.py after every command from .ds-step/events.jsonl.", "",
           "## Aim", s["aim"], "", "## Success bar", s["bar"], "", "## Step"]
    if card:
        out += [f"Aim: {card['aim']}", f"Done when: {card['done']}", "In scope:"]
        out += [f"{i}. {item}" for i, item in enumerate(card["scope"], 1)]
        out += [f"Out of scope: {card['out']}", f"Budget: {card['budget']}", f"Stop and ask: {card['ask']}"]
        out += [f"Frozen: {', '.join(card['frozen']) or 'none'}"]
        out += [f"Started: {s['step']['ts']} (step {s['step']['n']})"] if s["step"] else []
    else:
        out.append("No card. Write one with `step.py card ...`.")
    out += ["", "## Open decisions"] + [f"- {d}: {v['question']}" for d, v in s["decisions"].items()
                                        if not v["answer"]]
    out += ["", "## Settled"] + [f"- {d}: {v['question']} -> {v['answer']} ({v['ts'][:10]}"
                                 f"{'; ' + v['evidence'] if v['evidence'] else ''})" for d, v in settled(s)]
    out += ["", "## Parking lot"] + [f"- {e['ts'][:10]} {e['idea']}" for e in s["parked"]]
    out += ["", "## Recent"] + [f"- {e['ts'][:16]} {e['type']} {e.get('id') or e.get('run') or ''}".rstrip()
                                for e in s["recent"]]
    return "\n".join(out) + "\n"


def brief(root, s):
    """Tool line first, then aim, step, open and settled decisions; older entries become counts."""
    head = [f"Tool: python3 {TOOL}"] + [f"WARNING: {p}" for p in drift(root, s)]
    head += [f"Aim: {s['aim']}", f"Success bar: {s['bar']}"]
    card = s["card"]
    if s["step"]:
        used, limit = minutes_since(s["step"]["ts"]), budget_minutes(card["budget"])
        head.append(f"Step {s['step']['n']} running, {used} of {limit} min{' OVER BUDGET' if used > limit else ''}: "
                    f"{card['aim']}")
    else:
        head.append("No step running." + (f" Card ready: {card['aim']}" if card else " No card yet."))
    if card:
        head += [f"  Done when: {card['done']}", f"  In scope: {'; '.join(card['scope'])}",
                 f"  Out of scope: {card['out']}", f"  Stop and ask: {card['ask']}",
                 f"  Frozen: {', '.join(card['frozen']) or 'none'}"]
    head += [f"Run {r['id']} has no verdict yet." for r in s["runs"].values() if not r["verdict"]]
    open_ = [f"  {d}: {v['question'][:120]}" for d, v in s["decisions"].items() if not v["answer"]]
    done = [f"  {d}: {v['question'][:80]} -> {v['answer'][:80]}" for d, v in settled(s)]
    tail = [f"Parking lot: {len(s['parked'])} idea(s) in DS-STATE.md, not for this step."] if s["parked"] else []
    for keep in range(len(done), -1, -1):
        lines = head + ([f"Open decisions ({len(open_)}):"] + open_[:6] if open_ else [])
        lines += [f"Settled ({len(done)}; reopen only with new evidence):"] + done[len(done) - keep:] if done else []
        lines += [f"  ... {len(done) - keep} older in DS-STATE.md"] if keep < len(done) else []
        text = "\n".join(lines + tail)
        if len(text) <= BRIEF_CHARS or keep == 0:
            return text[:BRIEF_CHARS]


# --- commands -----------------------------------------------------------------------------------

def check_card(root, args):
    problems = [f"--{name} is empty" for name in ("aim", "done", "out", "ask") if not getattr(args, name).strip()]
    if not 1 <= len(args.scope) <= MAX_SCOPE:
        problems.append(f"{len(args.scope)} in-scope steps; give 1 to {MAX_SCOPE} (--scope each). Split the step")
    if budget_minutes(args.budget) is None:
        problems.append("--budget must be a time box such as 90m or 2h")
    frozen = [os.path.normpath(p) for p in args.freeze]
    for given, rel in zip(args.freeze, frozen):
        if "\\" in given or os.path.isabs(given) or rel.startswith("..") or not os.path.isfile(os.path.join(root, rel)):
            problems.append(f"frozen path {given!r} is not a file given relative to {root} with /")
    if problems:
        raise Refused("the card is not ready:\n  " + "\n  ".join(problems))
    return {"aim": args.aim, "done": args.done, "scope": args.scope, "out": args.out, "budget": args.budget,
            "ask": args.ask, "frozen": frozen}


def summarize(text, pattern):
    lines = [ln for ln in text.splitlines() if ln.strip()]
    picked = [ln for ln in lines if re.search(pattern, ln)] or lines
    return "\n".join(ln[:300] for ln in picked[-SUMMARY_LINES:])[-SUMMARY_CHARS:]


def gate(s, args):
    if not s["step"]:
        raise Refused("no step is started; write a card and run `step.py start`")
    decision = s["decisions"].get(args.decision)
    if not decision:
        raise Refused(f"no decision {args.decision or '(none given)'}; open one with `step.py decide \"...\"`. "
                      "If no decision depends on the result, don't run it")
    if decision["answer"]:
        raise Refused(f"{args.decision} is settled: {decision['answer']}. Reopen it with new evidence first")
    if not args.expect.strip():
        raise Refused("say which result would change the decision, and to what (--if)")
    pending = [r for r in s["runs"].values() if not r["verdict"]]
    if pending:
        raise Refused(f"run {pending[-1]['id']} has no verdict; read its summary against its --if line and record "
                      f"`step.py verdict {pending[-1]['id']} changed|no-change|inconclusive \"...\"` first")
    runs = [r for r in s["runs"].values() if r["step"] == s["step"]["n"] and r["verdict"] != "failed"]
    since = runs[max([i for i, r in enumerate(runs) if r.get("new_design")], default=0):]
    if len(since) >= 2 and all(r["verdict"] != "changed" for r in since[-2:]) and not args.new_design:
        raise Refused(f"the last two runs in this step ({since[-2]['id']}, {since[-1]['id']}) changed nothing. "
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
        run_id = new_id("R")
        log = os.path.join(root, ".ds-step", "runs", f"{run_id}.log")
        os.makedirs(os.path.dirname(log), exist_ok=True)
        append(root, {"type": "run", "id": run_id, "decision": args.decision, "if": args.expect, "pid": os.getpid(),
                      "command": command, "log": os.path.relpath(log, root), "new_design": args.new_design})
    try:
        with open(log, "wb") as handle:
            code = subprocess.run(command, stdout=handle, stderr=subprocess.STDOUT).returncode
    except OSError as error:
        append(root, {"type": "finished", "run": run_id, "error": str(error)})
        raise Refused(f"{run_id} did not launch: {error}")
    append(root, {"type": "finished", "run": run_id, "exit": code})
    with open(log, encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    print(f"{run_id} exit {code}; full output in {log} ({len(text.splitlines())} lines, not shown)")
    print(f"{args.decision}: {s['decisions'][args.decision]['question']} | If: {args.expect}")
    print(summarize(text, args.summary))
    return f"Next: `step.py verdict {run_id} changed|no-change|inconclusive \"<one line>\"`"


def command(root, s, args):
    session = os.environ.get("DS_SESSION_ID")
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
        if session and session in s["ended_sessions"]:
            raise Refused("this session already ended a step. One step per session: start the next in a fresh one")
        hashes = {"card": digest([s["aim"], s["bar"], s["card"]]),
                  "frozen": {rel: sha(os.path.join(root, rel)) for rel in s["card"]["frozen"]}}
        append(root, {"type": "start", "session": session, "hashes": hashes})
        return brief(root, fold(load(root)))
    if args.cmd == "brief":
        return brief(root, s)
    if args.cmd == "decide":
        did = new_id("D")
        append(root, {"type": "decide", "id": did, "question": args.question, "answer": args.answer,
                      "evidence": args.evidence})
        return did
    if args.cmd == "verdict":
        r = s["runs"].get(args.run_id)
        if not r:
            raise Refused(f"no run {args.run_id}")
        if r["verdict"]:
            raise Refused(f"{args.run_id} already has verdict {r['verdict']}; the log is append-only")
        if not r["finished"] and pid_alive(r.get("pid")):
            raise Refused(f"{args.run_id} is still running; wait for it to finish")
        append(root, {"type": "verdict", "run": args.run_id, "verdict": args.verdict, "note": args.note})
        return f"{args.run_id}: {args.verdict}" + ("" if args.verdict == "inconclusive" else f"; {r['decision']} settled")
    if args.cmd == "reopen":
        if not (s["decisions"].get(args.decision_id) or {}).get("answer"):
            raise Refused(f"{args.decision_id} is not a settled decision")
        if not args.reason.strip():
            raise Refused("give the new evidence or contradiction (--reason)")
        append(root, {"type": "reopen", "id": args.decision_id, "reason": args.reason})
        return f"reopened {args.decision_id}"
    if args.cmd == "park":
        append(root, {"type": "park", "idea": args.idea})
        return "parked"
    if args.cmd == "end":
        if not s["step"]:
            raise Refused("no step is started")
        if not args.abandon:
            require_clean(root, s)
            pending = [r for r in s["runs"].values() if not r["verdict"]]
            if pending:
                raise Refused(f"run {pending[-1]['id']} has no verdict; record it before ending the step")
        used, limit = minutes_since(s["step"]["ts"]), budget_minutes(s["card"]["budget"])
        note = "; ".join(drift(root, s)) if args.abandon else ""
        append(root, {"type": "end", "summary": args.summary, "minutes": used, "session": session,
                      "abandon": args.abandon, "drift": note})
        over = f", over its {limit} min budget" if used > limit else ""
        return f"step ended after {used} min{over}. Write the next card; start it in a fresh session"
    raise Refused(f"unknown command {args.cmd}")


def init(args):
    if find_root():
        raise Refused(f"a project already exists at {find_root()}; run step.py from there or below it")
    if not args.aim.strip() or not args.bar.strip():
        raise Refused("give the project --aim and --bar")
    root = os.getcwd()
    os.makedirs(os.path.join(root, ".ds-step"), exist_ok=True)
    for name, text in ((".gitignore", "runs/\nlock\n"), (".gitattributes", "events.jsonl merge=union\n")):
        with open(os.path.join(root, ".ds-step", name), "w") as handle:
            handle.write(text)
    ignore = os.path.join(root, ".gitignore")
    if "DS-STATE.md" not in (open(ignore).read() if os.path.exists(ignore) else ""):
        with open(ignore, "a") as handle:
            handle.write("DS-STATE.md\n")
    append(root, {"type": "init", "aim": args.aim, "bar": args.bar})
    return root


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
    sub.add_parser("start")
    sub.add_parser("brief")
    p = sub.add_parser("decide")
    p.add_argument("question")
    p.add_argument("--answer", default=None, help="record the decision as already settled")
    p.add_argument("--evidence", default="")
    p = sub.add_parser("run")
    p.add_argument("--decision", default="", help="the open decision (D-xxxx) this run's result settles")
    p.add_argument("--if", dest="expect", default="", help="which result would change it, and to what")
    p.add_argument("--new-design", default="", help="after two runs that changed nothing: what is different now")
    p.add_argument("--summary", default=r"^(SUMMARY|RESULT|VERDICT)\b", help="regex for the output lines to print")
    p.add_argument("command", nargs=argparse.REMAINDER)
    p = sub.add_parser("verdict")
    p.add_argument("run_id")
    p.add_argument("verdict", choices=("changed", "no-change", "inconclusive"))
    p.add_argument("note")
    p = sub.add_parser("reopen")
    p.add_argument("decision_id")
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
    root = None
    try:
        if args.cmd == "init":
            root = init(args)
            print(f"started a project at {root}; write a card with `step.py card ...`")
            return 0
        root = find_root()
        if not root:
            raise Refused("no ds-step project here or above; run `step.py init` at the project root")
        if args.cmd == "run":
            message = run(root, args)
        else:
            with locked(root):
                message = command(root, fold(load(root)), args)
        print(message)
        return 0
    except Refused as refusal:
        print(f"step.py: refused. {refusal}", file=sys.stderr)
        return 1
    finally:
        if root:
            with contextlib.suppress(Refused, OSError):
                with open(os.path.join(root, "DS-STATE.md"), "w", encoding="utf-8") as handle:
                    handle.write(view(fold(load(root))))


if __name__ == "__main__":
    sys.exit(main())
