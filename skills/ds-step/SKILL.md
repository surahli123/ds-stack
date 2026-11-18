---
name: ds-step
description: >-
  Use for data-science work that spans several sessions or agents: a pilot, an
  eval loop, prompt tuning, a labeling project, "continue the project", "next
  step", "pick up where we left off", "继续这个项目", "下一步". Keeps one step per
  session against an append-only event log rendered as DS-STATE.md: a task card
  written before the step, frozen instructions, closed questions and a parking
  lot. Every run names the decision it settles, and two runs that change nothing
  stop the loop. Also runs on /ds-step.
---

# ds-step

Long projects drift in the same few ways. Runs change no decision. Instructions are rewritten while an agent executes them. Settled questions are reopened. Work goes into fields the success bar doesn't use. One conversation stays open for days. `tools/step.py` refuses these moves, and in Claude Code the plugin's hooks add a second line of defense.

Discussion, review and quick questions need none of this. A step is needed only for a session that runs something (an eval, a labeling pass, a prompt variant) or changes the instructions a run uses.

## Where state lives

`.ds-step/events.jsonl` at the project root holds the state. Every command appends events and none rewrites them, so commit the file on the main branch the same day. `DS-STATE.md` is rendered from the log, so read it, never edit it. An edit made any other way is refused at the next `brief`, `run` or `end`. That covers another session, another harness, a shell command or a `git pull`. `step.py render` discards such an edit. Run the tool from the root or any folder below it.

## Steps

1. Read the brief: `python3 <skills>/ds-step/tools/step.py brief`. In Claude Code the SessionStart hook has already put it in context. For a new project, run `step.py init --aim "..." --bar "..."` and take the aim from the `Decision:` line of a ds-plan plan.
2. Write the card for one step, sized to finish in one session:

   ```bash
   step.py card --aim "..." --done "<a check that passes or fails>" --scope "..." [--scope ... up to 5] \
     --out "..." --budget 90m --ask "<when to stop and ask>" [--freeze prompts/v3.md ...]
   ```

   Freeze every file a run reads its instructions from. Then run `step.py start`. It hashes the card and the frozen files. If either changes before the step ends, `run` and `end` refuse until you run `step.py end "..." --abandon` and write a new card.
3. Stay on the step:
   - When something else comes up, park it with `step.py park "..."`.
   - Record a settled question with `step.py close "<question>" "<answer>" --evidence <pointer>`.
   - Reopen one only with new evidence: `step.py reopen C3 --reason "..."`.
4. Open the decision a run will settle with `step.py decide "<question>"`, then run through the gate:

   ```bash
   step.py run --decision D1 --if "<result -> choice>" -- <command>
   ```

   If no decision depends on the result, don't run it. The output streams to `.ds-step/runs/R<n>.log`. Only lines starting `SUMMARY`, `RESULT` or `VERDICT` are printed (otherwise the last eight), so make the script print its summary that way. Open the log only for a specific line range.
5. Record the verdict: `step.py verdict R<n> changed|no-change|inconclusive "<one line>"`.
   - `changed` and `no-change` close the decision as a Closed entry.
   - The gate refuses the next run until the verdict is in.
   - After two runs in the step that changed nothing, it refuses a third. Change the design (more rows, a held-out set, a different measure) and pass `--new-design "..."`, or end the step and tell the owner.
6. Review once, at the end, against Done when. Then run `step.py end "<what the step produced>"`. It clears the card. Write the next card, and start it in a fresh session.

## Several agents

- One planner writes cards. An executing agent gets a started step and its frozen files, never a revised copy mid-run.
- A decision counts once it is closed in the event log on main. One that sits in an unmerged branch is not closed.
- Pass pointers, not pasted rows: `DS-STATE.md`, `.ds-step/runs/R4.log`, a query id.

## What enforces what

| Rule | Enforced by |
|---|---|
| A card before a step | `start` refuses without one. `card` refuses empty fields, more than five in-scope items, a budget that isn't a time box, and frozen paths that aren't files. |
| No instruction changes mid-step | Start-time hashes: `brief`, `run` and `end` refuse when the card or a frozen file changed, by any route. In Claude Code the PreToolUse hook also denies file-tool edits to frozen files. |
| State changes only through the tool | The rendered `DS-STATE.md` is compared on every check. The hook denies file-tool edits to `DS-STATE.md` and `.ds-step/`. |
| A decision before every run | `run` refuses without an open decision id and an `--if` line. |
| Read each result before the next run | `run` refuses while a run has no verdict. Failed launches and killed runs are recorded too. |
| Stop tuning on noise | `run` refuses a third run after two runs in the step that changed nothing. Rewording a decision doesn't reset the count. |
| Settled stays settled | A conclusive verdict closes its decision, and `run` refuses a closed decision until it is reopened with a reason. |
| One step per session | `end` clears the card. In Claude Code the SessionStart hook stamps the session id, and `start` refuses in a session that already ended a step. Other harnesses get only the cleared card. |
| Summary-only reading | `run` streams the output to a file and prints the summary lines. |

What it doesn't stop: a person or agent editing `.ds-step/events.jsonl` with a shell command. Edits to the card in the log are caught by the start-time hash. A rewritten verdict is not caught; review the diff of the log in the PR.
