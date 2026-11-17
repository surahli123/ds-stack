---
name: ds-step
description: >-
  Use for data-science work that spans several sessions or agents: a pilot, an
  eval loop, prompt tuning, a labeling project, "continue the project", "next
  step", "pick up where we left off", "继续这个项目", "下一步". Keeps one step per
  session against a short state file (DS-STATE.md): a task card filled in before
  work starts, closed questions that stay closed, frozen instructions, and a
  parking lot. Every run must name the decision it changes, and two
  inconclusive runs on one decision stop the loop. Also runs on /ds-step.
---

# ds-step

Long projects drift in the same few ways: runs that change no decision, instructions rewritten while an agent executes them, settled questions reopened, side quests on fields the success bar does not use, and one conversation kept alive for days. This skill makes the working rules against them hard to skip: `tools/step.py` refuses the move, and in Claude Code the plugin's hooks block it.

## The state file

`DS-STATE.md` sits at the project root, in the main branch, so every session and every agent reads the same one. It holds:

- **Aim** and **Success bar**: the decision the project serves, and the result that settles it, with the fields it uses. Written once, at `init`.
- **Step**: the task card for the current step (Aim, Done when, In scope with at most five items, Out of scope, Budget as a time box, Stop and ask). `start` refuses a card with an empty or placeholder field.
- **Frozen**: files that must not change while the step runs, such as the instructions an executing agent is following.
- **Closed**: settled questions, one line each, with the answer and its evidence.
- **Parking lot**: ideas that are not this step.
- **Log**: one line per start, end, run verdict and reopen, written by the script.

Change the file through `step.py`. Write the Step card yourself, between steps.

## Steps

1. At the start of a session, read the brief, not the whole history: `python3 <skills>/ds-step/tools/step.py brief` (in Claude Code the SessionStart hook already put it in context). If there is no state file, run `step.py init --aim "..." --bar "..."`; take the aim from the `Decision:` line of a ds-plan plan when there is one.
2. Fill in the Step card for one step, then run `step.py start`. A step is what one session can finish inside its budget. If the card needs more than five in-scope items, split it.
3. Work only on the step. When something else comes up (a boundary case of a field the success bar does not use, a better prompt idea, a new dataset question), run `step.py park "..."` and go on. When a question gets settled, run `step.py close "<question>" "<answer>" --evidence <pointer>`. Reopen one only with new evidence: `step.py reopen C3 --reason "..."`.
4. Before any run that costs time or tokens (an eval, a labeling pass, a prompt variant), go through the gate:

   ```bash
   python3 <skills>/ds-step/tools/step.py run --decision "<decision it changes>" --if "<result -> choice>" -- <command>
   ```

   If no decision depends on the result, don't run it. The full output goes to `.ds-runs/R<n>.log`; only lines starting `SUMMARY`, `RESULT` or `VERDICT` (else the last eight) are printed, so make the script print its summary that way. Don't read the log into context; open a line range only to check a specific number.
5. Read the summary against the `--if` line and record `step.py verdict R<n> changed|no-change|inconclusive "<one line>"`. The gate refuses the next run until you do. After two inconclusive runs on one decision it refuses a third: the noise is larger than the effect. Change the design (more rows, a held-out set, a different measure) and pass `--new-design "..."`, or park the question and tell the owner.
6. Review once, at the end of the step, against Done when. Then `step.py end "<what the step produced>"` and write the next Step card for the next session. Don't start a second step in the same session; a fresh session reads the brief and costs far less than a long one.

## Rules for several agents

- One planner writes Step cards; executing agents get a card and the Frozen files, never a revised copy mid-run. A change to the instructions waits for the next step.
- Accepted decisions go into Closed on the main branch the same day. A decision that sits in an unmerged branch is not closed.
- Pass pointers (`DS-STATE.md`, `.ds-runs/R4.log`, a query id), not pasted rows.

## What enforces what

| Rule | Enforced by |
|---|---|
| A filled task card before work | `step.py start` refuses; the SessionStart hook says no step is running |
| One step per session | `start` refuses while a step is open; the hook flags a step left open by an earlier session |
| A decision before every run | `step.py run` refuses without `--decision` and `--if` |
| Read each result before the next run | `run` refuses while the last run has no verdict |
| Stop tuning on noise | `run` refuses a third run after two inconclusive ones on the same decision |
| Summary-only reading | `run` writes the full output to a file and prints the summary lines |
| Closed questions stay closed | the PreToolUse hook blocks an edit that changes or drops a Closed line |
| No instruction rewrites mid-run | the hook blocks edits to the Step card and to Frozen files while a step runs |
| Time box | `brief` and `end` report minutes used against Budget |

Outside Claude Code the hooks don't run; the script's refusals still hold. The Bash part of the hook is a heuristic, and `step.py reopen` is a deliberate way through: the point is that every reopen leaves a reason in the Log.
