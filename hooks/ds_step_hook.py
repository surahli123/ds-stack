#!/usr/bin/env python3
"""Claude Code hooks for ds-step. They do nothing unless the project has a .ds-step/ folder.

    ds_step_hook.py session-start   # put the project brief in context; stamp the session id for step.py
    ds_step_hook.py pre-tool-use    # Write|Edit|MultiEdit|NotebookEdit: deny edits to DS-STATE.md and
                                    # .ds-step/, and to frozen files while a step runs

The hook sees only its own session's file tools. Writes it can't see (shell commands, another session or
harness, a git pull) are caught by step.py itself, which hashes the card and frozen files at start and
refuses brief, run and end when one changed. A hook error never blocks the agent.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "skills", "ds-step", "tools"))

import step  # noqa: E402

FILE_TOOLS = ("Write", "Edit", "MultiEdit", "NotebookEdit")


def project_root(payload):
    return step.find_root(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd())


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": f"ds-step: {reason}"}}))
    return 0


def pre_tool_use(payload):
    root = project_root(payload)
    tool_input = payload.get("tool_input") or {}
    if not root or payload.get("tool_name") not in FILE_TOOLS:
        return 0
    given = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    target = os.path.realpath(os.path.join(payload.get("cwd") or os.getcwd(), given))
    real_root = os.path.realpath(root)
    rel = os.path.relpath(target, real_root)
    if rel == "DS-STATE.md" or rel == ".ds-step" or rel.startswith(".ds-step" + os.sep):
        return deny(f"{rel} is written by step.py only; use its commands (card, close, park, verdict, ...)")
    s = step.fold(step.load(root))
    if s["step"] and rel in s["card"]["frozen"]:
        return deny(f"{rel} is frozen while step {s['step']['n']} runs. Changing instructions mid-run resets the "
                    "work: park the change (`step.py park`) for the next step's card")
    return 0


def session_start(payload):
    root = project_root(payload)
    if not root:
        return 0
    env_file = os.environ.get("CLAUDE_ENV_FILE")
    if env_file and payload.get("session_id"):
        with open(env_file, "a") as handle:
            handle.write(f"export DS_SESSION_ID={payload['session_id']}\n")
    s = step.fold(step.load(root))
    try:
        step.require_clean(root, s)
        body = step.brief(root, s)
    except step.Refused as refusal:
        body = f"ds-step refuses to brief: {refusal}"
    lines = ["ds-step project state. Discussion, review and questions need nothing more. A session that runs "
             "an eval, labeling pass or prompt variant, or changes frozen instructions, works inside a started "
             "step: `step.py card ...`, then `step.py start`, and each run through `step.py run`.", body]
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
