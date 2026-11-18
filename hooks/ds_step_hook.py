#!/usr/bin/env python3
"""Claude Code hooks for ds-step. They do nothing unless a .ds-step/ folder is found.

    ds_step_hook.py session-start   # put the brief in context; stamp the session id for step.py
    ds_step_hook.py pre-tool-use    # Write|Edit|MultiEdit|NotebookEdit: deny edits to .ds-step/ and
                                    # DS-STATE.md, and to frozen files while a step runs

The project root is found by walking up from the edited file, then the session's cwd, then
$CLAUDE_PROJECT_DIR. The hook sees only its own session's file tools; step.py's start-time hashes catch
every other write. A hook error never blocks the agent.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": f"ds-step: {reason}"}}))


def pre_tool_use(step, payload):
    tool_input = payload.get("tool_input") or {}
    if payload.get("tool_name") not in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        return
    given = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    target = os.path.realpath(os.path.join(payload.get("cwd") or os.getcwd(), given))
    root = step.find_root(os.path.dirname(target), payload.get("cwd"), os.environ.get("CLAUDE_PROJECT_DIR"))
    if not root:
        return
    rel = os.path.relpath(target, os.path.realpath(root))
    if rel == "DS-STATE.md" or rel.split(os.sep)[0] == ".ds-step":
        return deny(f"{rel} is written by step.py only; use its commands (card, decide, park, verdict, ...)")
    s = step.fold(step.load(root))
    if s["step"] and rel in s["card"]["frozen"]:
        deny(f"{rel} is frozen while step {s['step']['n']} runs. Changing instructions mid-run resets the work: "
             "park the change (`step.py park`) for the next step's card")


def session_start(step, payload):
    root = step.find_root(payload.get("cwd"), os.environ.get("CLAUDE_PROJECT_DIR"))
    if not root:
        return
    if os.environ.get("CLAUDE_ENV_FILE") and payload.get("session_id"):
        with open(os.environ["CLAUDE_ENV_FILE"], "a") as handle:
            handle.write(f"export DS_SESSION_ID={payload['session_id']}\n")
    try:
        body = step.brief(root, step.fold(step.load(root)))
    except step.Refused as refusal:
        body = f"ds-step can't read its state: {refusal}"
    lines = ["ds-step project. Discussion, review and questions need nothing more. A session that runs an eval, "
             "labeling pass or prompt variant, or changes frozen instructions, works inside a started step "
             "(`step.py card ...`, `step.py start`) and runs through `step.py run`.", body]
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                             "additionalContext": "\n".join(lines)}}))


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(HERE), "skills", "ds-step", "tools"))
        import step

        payload = json.loads(sys.stdin.read() or "{}")
        {"session-start": session_start, "pre-tool-use": pre_tool_use}[argv[0]](step, payload)
    except Exception as error:  # a broken hook must not stop the agent
        print(f"ds-step hook error, allowing: {error}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
