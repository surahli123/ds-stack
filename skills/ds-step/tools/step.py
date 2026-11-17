#!/usr/bin/env python3
"""Keep a long data-science project on its aim: one step per session, a state file, and a gate before each run.

    python3 tools/step.py init --aim "<decision this project serves>" --bar "<result that settles it>"
    python3 tools/step.py check                 # is the step card filled in? exit 1 if not
    python3 tools/step.py start [--resume]      # check the card, stamp the start time, print the brief
    python3 tools/step.py brief                 # the short state a session reads first (the SessionStart hook prints it)
    python3 tools/step.py close "<question>" "<answer>" [--evidence <pointer>]
    python3 tools/step.py reopen C3 --reason "<new evidence or contradiction>"
    python3 tools/step.py park "<idea that is not this step>"
    python3 tools/step.py end "<one line: what the step produced>"
    python3 tools/step.py run --decision "<decision it changes>" --if "<result -> choice>" -- <command ...>
    python3 tools/step.py verdict R4 changed|no-change|inconclusive "<one line>"

The state file is DS-STATE.md in the working directory ($DS_STATE overrides). It holds the project's Aim
and Success bar, the current Step card, Frozen files, Closed questions, a Parking lot and a Log. The runs
ledger is .ds-runs.tsv next to it, and each run's full output goes to .ds-runs/R<n>.log; `run` prints
only the summary lines, so row-level output stays out of the agent's context.

The run gate refuses a run when no step is started, when the decision or the expected effect is missing,
when the last run has no verdict yet, or when the last two runs on the same decision were inconclusive
(the noise is larger than the effect; change the design with --new-design, or park the question).

Exit code: 0 done, 1 refused or check failed (the reason is printed), 3 usage error.
"""

import argparse
import datetime as dt
import os
import re
import subprocess
import sys

SECTIONS = ["Aim", "Success bar", "Step", "Frozen", "Closed", "Parking lot", "Log"]
CARD_FIELDS = ["Aim", "Done when", "In scope", "Out of scope", "Budget", "Stop and ask"]
MAX_SCOPE = 5
VERDICTS = ("changed", "no-change", "inconclusive")
LEDGER_HEADER = ["ts", "id", "step", "decision", "if", "command", "exit", "log", "verdict", "note"]
SUMMARY_LINES, SUMMARY_CHARS = 8, 1500

TEMPLATE = """# Project state

Read this first in every session. Change it with `step.py`; the Step card is yours to write before a step starts.

## Aim
{aim}

## Success bar
{bar}

## Step
Aim: <the one thing this step moves toward the project Aim>
Done when: <a check that passes or fails>
In scope:
1. <at most five steps>
Out of scope: <what this step will not touch>
Budget: <minutes, for example 90m>
Stop and ask: <when to stop and ask the owner>

## Frozen

## Closed

## Parking lot

## Log
"""


class Refused(Exception):
    pass


def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def state_path():
    return os.environ.get("DS_STATE") or os.path.join(os.getcwd(), "DS-STATE.md")


def read(path=None):
    path = path or state_path()
    if not os.path.exists(path):
        raise Refused(f"no state file at {path}; run `step.py init` first")
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def write(text, path=None):
    with open(path or state_path(), "w", encoding="utf-8") as handle:
        handle.write(text)


def sections(text):
    """Map each `## Name` heading to its body (text up to the next ## heading)."""
    found, name, lines = {}, None, []
    for line in text.splitlines():
        heading = re.match(r"^## (.+?)\s*$", line)
        if heading:
            if name:
                found[name] = "\n".join(lines).strip("\n")
            name, lines = heading.group(1), []
        elif name:
            lines.append(line)
    if name:
        found[name] = "\n".join(lines).strip("\n")
    return found


def replace_section(text, name, body):
    pattern = re.compile(rf"(^## {re.escape(name)}[ \t]*\n)(.*?)(?=^## |\Z)", re.M | re.S)
    if not pattern.search(text):
        return text.rstrip("\n") + f"\n\n## {name}\n{body.rstrip()}\n"
    return pattern.sub(lambda m: m.group(1) + (body.rstrip() + "\n\n" if body.strip() else "\n"), text, count=1)


def append_line(text, name, line):
    body = sections(text).get(name, "")
    return replace_section(text, name, (body.rstrip() + "\n" if body.strip() else "") + line)


def card(text):
    """Parse the Step card into its fields; In scope is a list of the numbered items."""
    fields, current = {}, None
    for line in sections(text).get("Step", "").splitlines():
        field = re.match(r"^([A-Z][A-Za-z ]+):\s*(.*)$", line)
        if field and field.group(1) in CARD_FIELDS + ["Started"]:
            current = field.group(1)
            fields[current] = [] if current == "In scope" else field.group(2).strip()
            if current == "In scope" and field.group(2).strip():
                fields[current].append(field.group(2).strip())
        elif current == "In scope" and re.match(r"^\s*(\d+[.)]|[-*])\s+\S", line):
            fields[current].append(re.sub(r"^\s*(\d+[.)]|[-*])\s+", "", line).strip())
    return fields


def budget_minutes(value):
    match = re.match(r"^\s*(\d+(?:\.\d+)?)\s*(m|min|mins|minutes|h|hr|hrs|hours)\b", value or "", re.I)
    if not match:
        return None
    amount = float(match.group(1))
    return int(amount * 60) if match.group(2).lower().startswith("h") else int(amount)


def card_problems(text):
    fields, problems = card(text), []
    state = sections(text)
    for name in ("Aim", "Success bar"):
        if not state.get(name, "").strip() or "<" in state.get(name, ""):
            problems.append(f"the project {name} is empty; write it once, at init")
    for name in CARD_FIELDS:
        value = fields.get(name)
        if not value or any("<" in v for v in (value if isinstance(value, list) else [value])):
            problems.append(f"Step card: {name} is not filled in")
    scope = fields.get("In scope") or []
    if len(scope) > MAX_SCOPE:
        problems.append(f"Step card: {len(scope)} in-scope steps; at most {MAX_SCOPE}. Split the step")
    if fields.get("Budget") and "<" not in fields["Budget"] and budget_minutes(fields["Budget"]) is None:
        problems.append("Step card: Budget must be a time box such as 90m or 2h")
    return problems


def closed_entries(text):
    """The closed questions as (id, line), in file order. Lines look like `- C3: question -> answer (...)`."""
    return re.findall(r"^(- (C\d+): .*)$", sections(text).get("Closed", ""), re.M)


def frozen_paths(text):
    return [re.sub(r"^\s*[-*]\s+", "", line).strip().strip("`")
            for line in sections(text).get("Frozen", "").splitlines() if re.match(r"^\s*[-*]\s+\S", line)]


def started(text):
    value = card(text).get("Started")
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None
    except ValueError:
        return None


def set_started(text, stamp):
    body = sections(text).get("Step", "")
    body = "\n".join(line for line in body.splitlines() if not line.startswith("Started:"))
    if stamp:
        body = body.rstrip() + f"\nStarted: {stamp}"
    return replace_section(text, "Step", body)


def brief(text):
    """At most about 25 lines: what a fresh session must know before it does anything."""
    state, fields = sections(text), card(text)
    out = [f"Aim: {state.get('Aim', '').strip()}", f"Success bar: {state.get('Success bar', '').strip()}"]
    begun = started(text)
    if begun:
        used = int((now() - begun).total_seconds() // 60)
        limit = budget_minutes(fields.get("Budget", ""))
        clock = f"{used} of {limit} min used" if limit else f"{used} min in"
        over = " OVER BUDGET: end the step or ask the owner" if limit and used > limit else ""
        out.append(f"Step (started {fields['Started']}, {clock}){over}: {fields.get('Aim', '')}")
    else:
        out.append(f"Step (not started; run `step.py start`): {fields.get('Aim', '')}")
    out.append(f"  Done when: {fields.get('Done when', '')}")
    for i, item in enumerate(fields.get("In scope") or [], 1):
        out.append(f"  {i}. {item}")
    out.append(f"  Out of scope: {fields.get('Out of scope', '')}")
    out.append(f"  Stop and ask: {fields.get('Stop and ask', '')}")
    closed = closed_entries(text)
    if closed:
        out.append(f"Closed ({len(closed)}; settled, do not reopen without new evidence via `step.py reopen`):")
        out.extend("  " + line[2:][:160] for line, _ in closed[-12:])
        if len(closed) > 12:
            out.append(f"  ... {len(closed) - 12} older in DS-STATE.md")
    frozen = frozen_paths(text)
    if frozen:
        out.append("Frozen (no edits while this step runs): " + ", ".join(frozen))
    parked = [ln for ln in state.get("Parking lot", "").splitlines() if ln.strip()]
    if parked:
        out.append(f"Parking lot: {len(parked)} idea(s), not for this step")
    last = ledger_rows()
    if last and not last[-1]["verdict"]:
        out.append(f"Run {last[-1]['id']} has no verdict yet: record it with `step.py verdict` before another run")
    return "\n".join(out)


# --- runs ledger --------------------------------------------------------------------------------

def ledger_path():
    return os.path.join(os.path.dirname(os.path.abspath(state_path())), ".ds-runs.tsv")


def ledger_rows():
    path = ledger_path()
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().splitlines()
    return [dict(zip(LEDGER_HEADER, line.split("\t") + [""] * len(LEDGER_HEADER))) for line in lines[1:] if line]


def write_ledger(rows):
    clean = lambda v: re.sub(r"[\t\r\n]+", " ", str(v))  # noqa: E731
    with open(ledger_path(), "w", encoding="utf-8") as handle:
        handle.write("\t".join(LEDGER_HEADER) + "\n")
        for row in rows:
            handle.write("\t".join(clean(row.get(k, "")) for k in LEDGER_HEADER) + "\n")


def decision_key(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def summarize(output, pattern):
    """The lines worth reading: those matching the summary pattern, else the last few, capped."""
    lines = [ln for ln in output.splitlines() if ln.strip()]
    picked = [ln for ln in lines if re.search(pattern, ln)] if pattern else []
    picked = (picked or lines)[-SUMMARY_LINES:]
    text = "\n".join(ln[:300] for ln in picked)
    return text[-SUMMARY_CHARS:]


def gate(text, decision, expect, new_design):
    if not started(text):
        raise Refused("no step is started; fill in the Step card and run `step.py start`")
    if not decision.strip() or not expect.strip():
        raise Refused("name the decision this run changes (--decision) and what result would change it (--if); "
                      "if no decision depends on it, don't run it")
    rows = ledger_rows()
    if rows and not rows[-1]["verdict"]:
        raise Refused(f"run {rows[-1]['id']} has no verdict; read its summary against its decision and record "
                      f"`step.py verdict {rows[-1]['id']} changed|no-change|inconclusive \"...\"` first")
    same = [r for r in rows if decision_key(r["decision"]) == decision_key(decision)]
    tail = same[-2:]
    if len(tail) == 2 and all(r["verdict"] == "inconclusive" for r in tail) and not new_design:
        raise Refused(f"the last two runs on this decision ({tail[0]['id']}, {tail[1]['id']}) were inconclusive: "
                      "the noise is larger than the effect. Change the design (more rows, a different measure, "
                      "a held-out set) and say how with --new-design, or park the question")


def run(args):
    text = read()
    gate(text, args.decision, args.expect, args.new_design)
    rows = ledger_rows()
    run_id = f"R{len(rows) + 1}"
    folder = os.path.join(os.path.dirname(ledger_path()), ".ds-runs")
    os.makedirs(folder, exist_ok=True)
    log = os.path.join(folder, f"{run_id}.log")
    proc = subprocess.run(args.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    with open(log, "w", encoding="utf-8") as handle:
        handle.write(proc.stdout)
    note = f"new design: {args.new_design}" if args.new_design else ""
    rows.append({"ts": now().isoformat(), "id": run_id, "step": card(text).get("Aim", ""), "decision": args.decision,
                 "if": args.expect, "command": " ".join(args.command), "exit": proc.returncode,
                 "log": os.path.relpath(log, os.path.dirname(ledger_path())), "verdict": "", "note": note})
    write_ledger(rows)
    print(f"{run_id} exit {proc.returncode}; full output in {log} ({len(proc.stdout.splitlines())} lines, not shown)")
    print(f"Decision: {args.decision} | If: {args.expect}")
    print(summarize(proc.stdout, args.summary))
    print(f"Next: `step.py verdict {run_id} changed|no-change|inconclusive \"<one line>\"`")
    return 0


def verdict(args):
    rows = ledger_rows()
    match = [r for r in rows if r["id"] == args.run_id]
    if not match:
        raise Refused(f"no run {args.run_id} in {ledger_path()}")
    if match[0]["verdict"]:
        raise Refused(f"{args.run_id} already has verdict {match[0]['verdict']}; the ledger is append-only")
    match[0]["verdict"] = args.verdict
    match[0]["note"] = "; ".join(x for x in (match[0]["note"], args.note) if x)
    write_ledger(rows)
    text = append_line(read(), "Log", f"- {now().date()} {args.run_id} {args.verdict}: {args.note}")
    write(text)
    print(f"{args.run_id}: {args.verdict}")
    return 0


# --- state commands -----------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd")
    p = sub.add_parser("init")
    p.add_argument("--aim", default="<the decision this project serves, its owner and options>")
    p.add_argument("--bar", default="<the result that settles it, and the fields it uses>")
    sub.add_parser("check")
    p = sub.add_parser("start")
    p.add_argument("--resume", action="store_true", help="continue a step a crashed session left open")
    sub.add_parser("brief")
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
    p = sub.add_parser("run")
    p.add_argument("--decision", default="", help="the decision this run's result changes")
    p.add_argument("--if", dest="expect", default="", help="which result would change it, and to what")
    p.add_argument("--new-design", default="", help="after two inconclusive runs: what changed in the design")
    p.add_argument("--summary", default=r"^(SUMMARY|RESULT|VERDICT)\b",
                   help="regex for the output lines to print (default: lines starting SUMMARY, RESULT or VERDICT)")
    p.add_argument("command", nargs=argparse.REMAINDER)
    p = sub.add_parser("verdict")
    p.add_argument("run_id")
    p.add_argument("verdict", choices=VERDICTS)
    p.add_argument("note")
    args = parser.parse_args(argv)
    if not args.cmd:
        parser.print_usage(sys.stderr)
        return 3
    try:
        return dispatch(args)
    except Refused as refusal:
        print(f"step.py: refused. {refusal}", file=sys.stderr)
        return 1


def dispatch(args):
    if args.cmd == "init":
        if os.path.exists(state_path()):
            raise Refused(f"{state_path()} exists; edit its Step card instead")
        write(TEMPLATE.format(aim=args.aim, bar=args.bar))
        print(f"wrote {state_path()}; fill in the Step card, then `step.py start`")
        return 0
    if args.cmd == "run":
        if args.command[:1] == ["--"]:
            args.command = args.command[1:]
        if not args.command:
            raise Refused("no command after --")
        return run(args)
    if args.cmd == "verdict":
        return verdict(args)
    text = read()
    stamp = now().strftime("%Y-%m-%d %H:%M UTC")
    if args.cmd == "check":
        problems = card_problems(text)
        print("\n".join(problems) if problems else "step card ok")
        return 1 if problems else 0
    if args.cmd == "start":
        problems = card_problems(text)
        if problems:
            raise Refused("the Step card is not ready:\n  " + "\n  ".join(problems))
        if started(text) and not args.resume:
            raise Refused("a step is already started and not ended. One step per session: `step.py end` it, "
                          "or pass --resume if its session crashed")
        if not started(text):
            text = set_started(text, now().isoformat().replace("+00:00", "Z"))
            text = append_line(text, "Log", f"- {stamp} started: {card(text).get('Aim', '')}")
            write(text)
        print(brief(text))
        return 0
    if args.cmd == "brief":
        print(brief(text))
        return 0
    if args.cmd == "close":
        ids = [int(cid[1:]) for _, cid in closed_entries(text)]
        cid = f"C{max(ids, default=0) + 1}"
        evidence = f"; {args.evidence}" if args.evidence else ""
        write(append_line(text, "Closed", f"- {cid}: {args.question} -> {args.answer} ({now().date()}{evidence})"))
        print(cid)
        return 0
    if args.cmd == "reopen":
        entries = dict((cid, line) for line, cid in closed_entries(text))
        if args.closed_id not in entries:
            raise Refused(f"no closed question {args.closed_id}")
        body = "\n".join(ln for ln in sections(text)["Closed"].splitlines() if ln != entries[args.closed_id])
        text = replace_section(text, "Closed", body)
        text = append_line(text, "Log", f"- {stamp} reopened {entries[args.closed_id][2:]} because: {args.reason}")
        write(text)
        print(f"reopened {args.closed_id}; the reason is in the Log")
        return 0
    if args.cmd == "park":
        write(append_line(text, "Parking lot", f"- {now().date()} {args.idea}"))
        print("parked")
        return 0
    if args.cmd == "end":
        begun = started(text)
        if not begun:
            raise Refused("no step is started")
        rows = ledger_rows()
        if rows and not rows[-1]["verdict"]:
            raise Refused(f"run {rows[-1]['id']} has no verdict; record it before ending the step")
        used = int((now() - begun).total_seconds() // 60)
        limit = budget_minutes(card(text).get("Budget", ""))
        over = f", over its {limit} min budget" if limit and used > limit else ""
        text = set_started(text, None)
        text = append_line(text, "Log", f"- {stamp} ended after {used} min{over}: {args.summary}")
        write(text)
        print(f"step ended after {used} min{over}. Write the next Step card before the next session starts.")
        return 0
    return 3


if __name__ == "__main__":
    sys.exit(main())
