# Drift and token waste in long data-science work

ds-stack now has `ds-step`. It enforces the pilot's working rules in a script and two Claude Code hooks, so the agent doesn't have to remember them. pstack and Anthropic's docs both argue for moving a rule out of prose into a check. Matt Pocock's skills mostly sharpen the wording first and add a hook only for hard guardrails. No source measures its drift mechanisms against a baseline, so the rules below rest on practitioner experience and our own retro.

## The problem

The intent-labeling pilot (2026-11-09 to 11-17) was meant to rank three search bets. Its retro found:

- about ten tuning runs on ~100 invented rows, each ending "within noise";
- ten of eleven instructions revised while an agent ran them;
- twelve decisions in one day on fields the success bar didn't use;
- five planners at once, with accepted decisions in unmerged branches;
- one executing conversation kept open for days, rereading row-level output.

## pstack

Read at [cursor/plugins@e1cc031](https://github.com/cursor/plugins/tree/e1cc031/pstack):

- [poteto-mode](https://github.com/cursor/plugins/blob/e1cc031/pstack/skills/poteto-mode/SKILL.md)
- the playbooks [hillclimb](https://github.com/cursor/plugins/blob/e1cc031/pstack/skills/poteto-mode/playbooks/hillclimb.md), [session-pickup](https://github.com/cursor/plugins/blob/e1cc031/pstack/skills/poteto-mode/playbooks/session-pickup.md) and [pause-safely](https://github.com/cursor/plugins/blob/e1cc031/pstack/skills/poteto-mode/playbooks/pause-safely.md)
- [figure-it-out](https://github.com/cursor/plugins/blob/e1cc031/pstack/skills/figure-it-out/SKILL.md) and [show-me-your-work](https://github.com/cursor/plugins/blob/e1cc031/pstack/skills/show-me-your-work/SKILL.md)
- the principles [explain-the-number](https://github.com/cursor/plugins/blob/e1cc031/pstack/skills/principle-explain-the-number/SKILL.md), [guard-the-context-window](https://github.com/cursor/plugins/blob/e1cc031/pstack/skills/principle-guard-the-context-window/SKILL.md) and [encode-lessons-in-structure](https://github.com/cursor/plugins/blob/e1cc031/pstack/skills/principle-encode-lessons-in-structure/SKILL.md)

Mechanisms:

- "Write the decision before you run. Name the result that would change it, and the noise floor. Stop when the run-to-run spread is larger than the effect." (explain-the-number)
- hillclimb fixes a "checkable stop predicate" and freezes the harness before the loop. It also logs one row per attempt in `decision.tsv` and reads that log before each new attempt.
- Fresh agents get "the original brief, every later directive, and the prior agent's report". session-pickup treats the prior trail as "authoritative input".
- Summaries stay in the main thread, "not raw payloads".
- A repeated instruction becomes "a lint, metadata flag, runtime check, or script instead of more text".
- No harness hooks.

Evidence: none measured. The README rests on the author's experience.

Fit:

- Taken: decision-before-run, the stop rule on noise, an append-only log.
- Left out: the playbook router, the model panels, and swarm and arena fan-out. Our problem was too much parallel work.

## Matt Pocock's skills

Read at [mattpocock/skills@5863806](https://github.com/mattpocock/skills/tree/5863806):

- [wayfinder](https://github.com/mattpocock/skills/blob/5863806/skills/engineering/wayfinder/SKILL.md)
- [handoff](https://github.com/mattpocock/skills/blob/5863806/skills/productivity/handoff/SKILL.md)
- [implement-spec](https://github.com/mattpocock/skills/blob/5863806/skills/engineering/implement-spec/SKILL.md)
- [writing-for-agents](https://github.com/mattpocock/skills/blob/5863806/skills/productivity/writing-for-agents/SKILL.md)
- [git-guardrails-claude-code](https://github.com/mattpocock/skills/blob/5863806/skills/misc/git-guardrails-claude-code/SKILL.md)

Mechanisms:

- wayfinder plans a large effort as a map of decision tickets, not execution steps. The map has a Destination, "Decisions so far", "Not yet specified" and "Out of scope". Out-of-scope work "never graduates".
- "A decision lives in exactly one place", its ticket. The map only gists it and links to it.
- A ticket is "sized to one 100K token agent session". Each session resolves one ticket, with an exception for research tickets.
- handoff writes a file for a fresh agent and points to existing artifacts instead of copying them. implement-spec says "Start every subagent with a fresh context window".
- writing-for-agents counts always-loaded text as "context load". Its first fix for a vague bound is to "sharpen the bound first".
- git-guardrails is a PreToolUse hook for the cases wording can't secure.

Evidence: none measured.

Fit:

- Taken:
  - one item per session;
  - a low-resolution brief;
  - each decision recorded in one place (a Closed entry);
  - a parking lot apart from that record;
  - a PreToolUse hook as the hard stop.
- Left out: the issue-tracker map. A ds-stack project usually lives in one repo, and an event log on main can't split across planners.

## Anthropic's Claude Code documentation

Read on 2026-11-17:

- the docs pages on [hooks](https://code.claude.com/docs/en/hooks), [memory](https://code.claude.com/docs/en/memory), [costs](https://code.claude.com/docs/en/costs) and [best practices](https://code.claude.com/docs/en/best-practices)
- the engineering posts [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) and [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

Mechanisms:

- "If something has to happen every time, make it a hook … CLAUDE.md is for guidelines." Memory describes CLAUDE.md as "context, not enforced configuration".
- PreToolUse can deny a call and show Claude the reason. SessionStart context is injected again after `compact` and `resume`.
- A hook sees only its own session's tool calls.
- The harness post keeps a progress file and a JSON feature list. It chose JSON because "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files". The agent works on "only one feature at a time", and each session starts by reading the git log and the progress file.
- Two token rules: `/clear` between tasks, because "stale context wastes tokens", and filter output so it costs "hundreds" of tokens rather than "tens of thousands".

Evidence, all qualitative except the cost figures:

- The context post says sub-agent architectures "showed a substantial improvement over single-agent systems on complex research tasks", citing Anthropic's multi-agent research post.
- The harness post says testing tools "dramatically improved performance". That is about browser testing, not the progress file.
- The costs page gives about $13 per developer per active day, and about 7x more tokens for agent teams in plan mode.

Fit:

- Taken: the hooks, one item per session, the fixed start routine and output filtering. State is now a JSON event log, with Markdown only as the rendered view.
- Left out: a Stop hook that keeps the agent working. Our agents did too much, not too little.

## What changed

| Change | Failure it targets | Enforced by |
|---|---|---|
| Card, frozen files, closed questions and parking lot in an append-only event log rendered as `DS-STATE.md`; start-time hashes of the card and frozen files | Instructions rewritten mid-run, off-path work | `brief`, `run` and `end` refuse on any changed hash or hand-edited view, whatever wrote it |
| Run gate keyed to decision ids; a conclusive verdict closes the decision; two runs in a step that changed nothing block a third | Tuning on noise | `run`. The replay test mixes verdicts and rewords the decisions, and is stopped at run 3 |
| Output streamed to `.ds-step/runs/R<n>.log`, with only summary lines printed | Rows read into context | `run` |
| SessionStart brief and session stamp; PreToolUse deny on file edits to state and frozen files | Losing the aim after compaction; a second step in one session | `hooks/hooks.json`, which does nothing without `.ds-step/` |

`tests/test_ds_step.py` has 19 cases.

Not addressed:

- Five planners at once. The rule is written down, but no script stops a person from opening five sessions.
- A verdict rewritten in the event log by a shell command. The PR diff shows it.
- In Codex and Cursor, only the script's refusals apply, because those harnesses don't run the hooks.

Next: run the next multi-session project under `ds-step` and compare runs per decision and reopened questions with this retro.
