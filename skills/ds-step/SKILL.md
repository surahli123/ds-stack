---
name: ds-step
description: >-
  Use for data-science work that spans several sessions or agents: a pilot, an
  eval loop, prompt tuning, a labeling project, "continue the project", "next
  step", "pick up where we left off", "继续这个项目", "下一步". Keeps one step per
  session against an append-only event log: a task card written before the step,
  frozen instructions, settled decisions and a parking lot. Every run names the
  decision it settles, and two runs that change nothing stop the loop. Also runs
  on /ds-step.
---

# ds-step

Long projects drift in the same few ways. Runs change no decision. Instructions are rewritten while an agent executes them. Settled questions are reopened. Work goes into fields the success bar doesn't use. One conversation stays open for days. `tools/step.py` refuses these moves, and in Claude Code the plugin's hooks add a second line of defense.

Discussion, review and quick questions need none of this. A step is needed only for a session that runs something (an eval, a labeling pass, a prompt variant) or changes the instructions a run uses.

## Where state lives

`.ds-step/events.jsonl` at the project root is the state. Commands only append to it, and each id carries a random suffix (`D-3fa2`, `R-91c2`). The file merges across branches with git's union driver, which `init` sets up in `.ds-step/.gitattributes`. Commit it on main the same day. If a merge still leaves conflict markers, step.py names the line; keep both sides and delete the markers.

`DS-STATE.md` is the full view for a person. It is rewritten after every command and gitignored, so editing it changes nothing. Run step.py from the root or any folder below it.

## Steps

1. Read the brief: `python3 <skills>/ds-step/tools/step.py brief`. In Claude Code the SessionStart hook has already put it in context. For a new project, run `step.py init --aim "..." --bar "..."` and take the aim from the `Decision:` line of a ds-plan plan.
2. Write the card for one step, sized to finish in one session:

   ```bash
   step.py card --aim "..." --done "<a check that passes or fails>" --scope "..." [--scope ... up to 5] \
     --out "..." --budget 90m --ask "<when to stop and ask>" [--freeze prompts/v3.md ...]
   ```

   Freeze every file a run reads its instructions from. Then run `step.py start`. It hashes the card and the frozen files. If either changes before the step ends, by any route, `run` and `end` refuse until `step.py end "..." --abandon`. The brief shows the change as a warning, and verdicts can still be recorded.
3. Stay on the step:
   - Park anything else with `step.py park "..."`.
   - Record a question that is already settled with `step.py decide "<question>" --answer "..." --evidence <pointer>`.
   - Reopen a settled decision only with new evidence: `step.py reopen D-3fa2 --reason "..."`.
4. Open the decision a run will settle with `step.py decide "<question>"`, then run through the gate:

   ```bash
   step.py run --decision D-3fa2 --if "<result -> choice>" -- <command>
   ```

   If no decision depends on the result, don't run it. The output streams to `.ds-step/runs/<id>.log`, and only lines starting `SUMMARY`, `RESULT` or `VERDICT` are printed (otherwise the last eight). Make the script print its summary that way. Open the log only for a specific line range.
5. When the run has finished, record `step.py verdict R-91c2 changed|no-change|inconclusive "<one line>"`.
   - `changed` and `no-change` settle the decision.
   - The gate refuses the next run until the verdict is in.
   - After two runs in the step that changed nothing, it refuses a third. Change the design (more rows, a held-out set, a different measure) and pass `--new-design "..."`, or end the step and tell the owner.
6. Review once, at the end, against Done when. Then run `step.py end "<what the step produced>"`. It clears the card. Write the next card, and start it in a fresh session.

## Several agents

- One planner writes cards. An executing agent gets a started step and its frozen files, never a revised copy mid-run.
- A decision counts once it is settled in the event log on main. A decision that sits in an unmerged branch is not settled.
- Pass pointers, not pasted rows: the brief, `.ds-step/runs/R-91c2.log`, a query id.

## What enforces what

| Rule | Enforced by |
|---|---|
| A card before a step | `start` refuses without one. `card` refuses empty fields, more than five in-scope items, a budget that isn't a time box, and frozen paths that aren't files. |
| No instruction changes mid-step | Start-time hashes: `run` and `end` refuse when the card or a frozen file changed, by any route. In Claude Code the PreToolUse hook also denies file-tool edits to frozen files. |
| A decision before every run | `run` refuses without an open decision id and an `--if` line. |
| Read each result before the next run | `run` refuses while a run has no verdict. `verdict` refuses while the run is still going. Failed launches are recorded as `failed`, and runs in an abandoned step as `abandoned`. |
| Stop tuning on noise | `run` refuses a third run after two runs in the step that changed nothing. Rewording a decision doesn't reset the count. |
| Settled stays settled | `run` refuses a settled decision until it is reopened with a reason. |
| One step per session | `end` clears the card. In Claude Code the SessionStart hook stamps the session id, and `start` refuses in a session that started or ended a step. Other harnesses get only the cleared card. |
| Summary-only reading | `run` streams the output to a file and prints the summary lines. The brief is capped at about 2,000 characters. |

What it doesn't stop:

- A verdict rewritten in `.ds-step/events.jsonl` with a shell command. Review the log's diff in the PR.
- `--new-design` with an unchanged command.
- On Windows there is no run lock, so start one run at a time.
