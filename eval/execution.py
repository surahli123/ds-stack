"""Did an eval run execute? Shared by run_arms.py, grade.py and acceptance.py.

A run executed when the agent got a fair chance at the task: it exited 0 with a reply, or it hit a limit of its
own (the time cap, the turn cap, or an empty final reply), which is graded as the miss it is. A run that the
provider or the harness cut short is an execution failure: rate-limited, at capacity, not isolated, a crash or
an API error. It says nothing about the model or the skill, so it is never graded as a wrong answer. run_arms.py records the outcome in meta.json ("execution"); for runs
made before that field existed, it is worked out the same way from meta.json's exit code, result.md, agent.log
and the transcript's result event.
"""

import json
import os
import re

OK = "ok"
# The agent's own limits: graded as answers (they score as misses), not execution failures.
AGENT_LIMITS = ("timeout", "max_turns", "empty_reply")
# Failures worth retrying after a pause: the provider refused the request, not the agent's work.
RETRYABLE = ("rate_limited", "capacity")
# The line eval/agents/codex.sh prints before it exits without starting the agent (older versions printed it
# and went on). Anchored to that line: Codex echoes the model's prose into its log, and an analysis may well
# say "the effect is not isolated".
ISOLATION = re.compile(r"^ds-stack: .+ is present, so this run is not isolated", re.M)
# Provider refusals are read only from error lines (Codex prints "ERROR: ...") and from an error result the
# agent reported, never from tool output or prose, where "429 rows" or "overloaded servers" can appear.
ERROR_LINE = re.compile(r"^\s*(?:ERROR|Error|error)\b.*$", re.M)
RATE_LIMITED = re.compile(r"\b429\b|too many requests|rate[ _-]?limit|usage limit", re.I)
CAPACITY = re.compile(r"at capacity|overloaded|\b529\b", re.I)
AGENT_MODEL = re.compile(r"^model: *(\S+)", re.M)
REASONING_EFFORT = re.compile(r"^reasoning effort: *(\S+)", re.M)


def classify(code, reply, log, error_text=None):
    """'ok', one of AGENT_LIMITS, or why the run didn't execute: not_isolated, rate_limited, capacity,
    exit_<code> or agent_error. An isolation warning on a run that also failed for another reason gives both,
    e.g. "not_isolated+rate_limited" (only an older wrapper, which warned and went on, can produce that).

    `log` is the agent's stderr: only a wrapper writes there, so an isolation warning is looked for there and
    never in the reply or a transcript. `error_text` is an error result the agent reported (claude -p's
    is_error), or None.
    """
    outcome = _outcome(code, reply, log, error_text)
    if ISOLATION.search(log or ""):
        return "not_isolated" if outcome in (OK, "exit_4") else f"not_isolated+{outcome}"
    return outcome


def _outcome(code, reply, log, error_text):
    if code == 0 and error_text is None and (reply or "").strip():
        return OK
    # claude -p exits 1 on any error result, its turn cap included; the cap is the agent's own limit.
    if error_text is not None and "max_turns" in error_text:
        return "max_turns"
    # Codex retries a 429 itself and may still finish, so these patterns only explain a run that failed.
    errors = "\n".join(ERROR_LINE.findall(log or "") + [error_text or ""])
    if RATE_LIMITED.search(errors):
        return "rate_limited"
    if CAPACITY.search(errors):
        return "capacity"
    if code == "timeout":
        return "timeout"
    if code != 0:
        # A custom agent has no error channel, so a crash for its own reasons can't be told from a provider
        # failure: it counts as a failure, and every rerun it causes is reported.
        return f"exit_{code}"
    return "agent_error" if error_text is not None else "empty_reply"


def executed(kind):
    """True when the run counts: it finished, or stopped at one of the agent's own limits."""
    return kind == OK or kind in AGENT_LIMITS


def claude_result(transcript):
    """(reply, error_text, cost, turns) from claude -p's stream-json; error_text is None unless is_error."""
    reply, error_text, cost, turns = "", None, None, None
    for line in transcript.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if isinstance(event, dict) and event.get("type") == "result":
            reply = event.get("result") or ""
            error_text = (reply or event.get("subtype") or "error") if event.get("is_error") else None
            cost, turns = event.get("total_cost_usd"), event.get("num_turns")
    return reply, error_text, cost, turns


def agent_details(log):
    """The model and reasoning effort an agent printed in its log header (Codex does), if any."""
    details = {}
    for key, pattern in (("agent_model", AGENT_MODEL), ("reasoning_effort", REASONING_EFFORT)):
        found = pattern.search(log or "")
        if found:
            details[key] = found.group(1)
    return details


def _read(path):
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8", errors="replace") as handle:
        return handle.read()


def run_execution(run_dir, meta=None):
    """The recorded outcome of one run, or the same classification applied to an older run's files."""
    if meta is None:
        with open(os.path.join(run_dir, "meta.json")) as handle:
            meta = json.load(handle)
    if meta.get("execution"):
        return meta["execution"]
    error_text = None
    if meta.get("transcript") is not False:
        _, error_text, _, _ = claude_result(_read(os.path.join(run_dir, "transcript.jsonl")))
    # Every meta.json run_arms.py writes has "exit"; a hand-made one without it is taken as a clean exit.
    return classify(meta.get("exit", 0), _read(os.path.join(run_dir, "result.md")),
                    _read(os.path.join(run_dir, "agent.log")), error_text)
