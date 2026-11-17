#!/usr/bin/env python3
"""Claude Code hooks for ds-step. They do nothing unless the project has a DS-STATE.md.

    ds_step_hook.py session-start   # SessionStart: put the project brief in the agent's context
    ds_step_hook.py pre-tool-use    # PreToolUse on Write|Edit|MultiEdit|Bash: block edits that
                                    # rewrite a running step's card, change or drop a closed answer,
                                    # or touch a frozen file while a step runs

The state file is $DS_STATE, else DS-STATE.md in $CLAUDE_PROJECT_DIR, else in the hook's cwd.
The legitimate ways through are step.py commands (`end`, `reopen --reason`), which leave a Log line.
The Bash check is a heuristic: it catches redirects, sed -i, tee, cp, mv and rm aimed at a guarded file.
A hook error never blocks the agent; it prints to stderr and allows the call.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "skills", "ds-step", "tools"))

import step  # noqa: E402

WRITERS = r"(>>?|\bsed\s+[^|;&]*-i|\bperl\s+[^|;&]*-i|\btee\b|\bcp\b|\bmv\b|\brm\b|\btruncate\b|\bdd\b)"


def find_state(payload):
    if os.environ.get("DS_STATE"):
        return os.environ["DS_STATE"]
    base = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
    return os.path.join(base, "DS-STATE.md")


def step_card_body(text):
    body = step.sections(text).get("Step", "")
    return "\n".join(line.rstrip() for line in body.splitlines() if not line.startswith("Started:")).strip()


def after_edit(current, tool, tool_input):
    """The state file's text if the edit went through, or None when it can't be worked out."""
    if tool == "Write":
        return tool_input.get("content", "")
    edits = tool_input.get("edits") if tool == "MultiEdit" else [tool_input]
    text = current
    for edit in edits or []:
        old, new = edit.get("old_string", ""), edit.get("new_string", "")
        if old not in text:
            return None
        text = text.replace(old, new) if edit.get("replace_all") else text.replace(old, new, 1)
    return text


def state_edit_problem(current, new):
    lost = [line for line, _ in step.closed_entries(current) if line not in new.splitlines()]
    if lost:
        return (f"this edit changes or removes closed question {lost[0].split(':')[0][2:]}. Closed questions stay "
                "closed. If new evidence contradicts one, run `step.py reopen <id> --reason \"...\"`; "
                "otherwise park the thought with `step.py park`")
    if step.started(current):
        if not step.started(new):
            return "this edit removes the Started stamp of a running step; end it with `step.py end \"...\"`"
        if step_card_body(current) != step_card_body(new):
            return ("the Step card is frozen while its step runs. Finish or end this step (`step.py end`), "
                    "then write the next card; put new ideas in the Parking lot (`step.py park`)")
    return None


def guarded_paths(state_file, text):
    """Frozen files, as absolute paths, while a step runs; none between steps."""
    if not step.started(text):
        return []
    base = os.path.dirname(os.path.abspath(state_file))
    return [os.path.normpath(os.path.join(base, p)) for p in step.frozen_paths(text)]


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": f"ds-step: {reason}"}}))
    return 0


def pre_tool_use(payload):
    state_file = find_state(payload)
    if not os.path.exists(state_file):
        return 0
    with open(state_file, encoding="utf-8") as handle:
        current = handle.read()
    tool, tool_input = payload.get("tool_name", ""), payload.get("tool_input") or {}
    state_abs = os.path.normpath(os.path.abspath(state_file))
    frozen = guarded_paths(state_file, current)
    if tool in ("Write", "Edit", "MultiEdit"):
        target = os.path.normpath(os.path.join(payload.get("cwd") or os.getcwd(), tool_input.get("file_path", "")))
        if target in frozen:
            return deny(f"{os.path.relpath(target, os.path.dirname(state_abs))} is frozen while this step runs. "
                        "Changing instructions mid-run resets the work; end the step first, or park the change")
        if target == state_abs:
            new = after_edit(current, tool, tool_input)
            problem = state_edit_problem(current, new) if new is not None else None
            if problem:
                return deny(problem)
        return 0
    if tool == "Bash":
        command = tool_input.get("command", "")
        if "step.py" in command or not re.search(WRITERS, command):
            return 0
        names = {state_abs: "DS-STATE.md"}
        names.update({p: os.path.relpath(p, os.path.dirname(state_abs)) for p in frozen})
        for path, rel in names.items():
            if os.path.basename(path) in command:
                return deny(f"this command looks like it writes {rel}. Change DS-STATE.md through step.py, "
                            "and leave frozen files alone while the step runs")
    return 0


def session_start(payload):
    state_file = find_state(payload)
    if not os.path.exists(state_file):
        return 0
    with open(state_file, encoding="utf-8") as handle:
        text = handle.read()
    os.environ["DS_STATE"] = state_file
    lines = ["ds-step project state (from DS-STATE.md). Work only on the Step below; settled questions are listed "
             "as Closed; put anything else in the Parking lot with `step.py park`.", step.brief(text)]
    if payload.get("source") == "startup" and step.started(text):
        lines.append("A step started in an earlier session is still open. One step per session: decide with the "
                     "owner whether to `step.py end` it or `step.py start --resume`.")
    elif not step.started(text):
        lines.append("No step is running. Before other work, fill in the Step card in DS-STATE.md and run "
                     "`step.py start`; it refuses an incomplete card.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                             "additionalContext": "\n".join(lines)[:9000]}}))
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        if argv[:1] == ["session-start"]:
            return session_start(payload)
        if argv[:1] == ["pre-tool-use"]:
            return pre_tool_use(payload)
        print("usage: ds_step_hook.py session-start|pre-tool-use", file=sys.stderr)
        return 0
    except Exception as error:  # a broken hook must not stop the agent
        print(f"ds-step hook error, allowing: {error}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
