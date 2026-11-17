# Drift and token waste in long data-science work

ds-stack now has `ds-step`, which enforces its working rules in a script and two Claude Code hooks instead of asking the agent to remember them. All three sources studied point the same way: a rule that lives only in a prompt fades over a long run, and a rule built into a tool holds. None of them measures its mechanisms against a baseline, so every rule below rests on practitioner experience and our own retro, not on an experiment.

## The problem

An agent team ran an LLM intent-labeling pilot from 2026-11-09 to 11-17 to rank three search bets. Its retro found five failure modes:

- About ten tuning runs on the same ~100 invented rows, each ending "within noise".
- Ten of eleven instructions revised while the executing agent was running them.
- Twelve decisions in one day on fields the success bar didn't use.
- Five planners at once, with accepted decisions in unmerged branches.
- One executing conversation kept for days, rereading row-level output.

The stopgap rules adopted on 2026-11-17 were right, but each one depended on the agent remembering it.

## pstack

Read on 2026-11-17 from [cursor/plugins/pstack](https://github.com/cursor/plugins/tree/main/pstack):

- [poteto-mode](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) and its [worker.md](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/worker.md)
- the playbooks [hillclimb](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/hillclimb.md), [session-pickup](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/session-pickup.md) and [pause-safely](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/pause-safely.md)
- [figure-it-out](https://github.com/cursor/plugins/blob/main/pstack/skills/figure-it-out/SKILL.md) and [show-me-your-work](https://github.com/cursor/plugins/blob/main/pstack/skills/show-me-your-work/SKILL.md)
- the principles [explain-the-number](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-explain-the-number/SKILL.md), [guard-the-context-window](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-guard-the-context-window/SKILL.md) and [encode-lessons-in-structure](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-encode-lessons-in-structure/SKILL.md)
- [the pitfalls guide](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/10-recipes-and-pitfalls.md)

Mechanisms:

- explain-the-number: "Write the decision before you run. Name the result that would change it, and the noise floor. Stop when the run-to-run spread is larger than the effect."
- hillclimb fixes a "checkable stop predicate" and freezes the measurement harness before the loop. It logs one `decision.tsv` row per attempt and reads that log before each attempt.
- Work goes to fresh agents. A fix round goes to a new agent with "the original brief, every later directive, and the prior agent's report". session-pickup treats the prior trail as "authoritative input. Resist the bias to re-derive it."
- guard-the-context-window keeps "summaries in the main thread, not raw payloads". Agent kickoffs pass "file pointers not inlined context".
- encode-lessons-in-structure: a repeated instruction becomes "a lint, metadata flag, runtime check, or script instead of more text".
- pstack ships no harness hooks. It enforces through skills, agent briefs and committed scripts.

Evidence: none measured. The README rests on the author's experience, and the pitfalls guide gives recipes, not numbers.

Fit:

- ds-stack already took the verify-by-script stance (`verify_readout.py`, `ds_verify.py`) and interrogate's "keep only what a rerun proves".
- Taken now: decision-before-run, the stop rule on noise, and an append-only TSV run ledger.
- Left: the playbook router, model and panel defaults, and swarm and arena fan-out. Those speed up parallel coding, and our failure was too much parallel work.

## Matt Pocock's skills

[github.com/mattpocock/skills](https://github.com/mattpocock/skills), read at commit `5863806`:

- [wayfinder](https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md)
- [handoff](https://github.com/mattpocock/skills/blob/main/skills/productivity/handoff/SKILL.md) and [claude-handoff](https://github.com/mattpocock/skills/blob/main/skills/in-progress/claude-handoff/SKILL.md)
- [implement-spec](https://github.com/mattpocock/skills/blob/main/skills/engineering/implement-spec/SKILL.md)
- [writing-for-agents](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md)
- [git-guardrails-claude-code](https://github.com/mattpocock/skills/blob/main/skills/misc/git-guardrails-claude-code/SKILL.md)

Mechanisms:

- wayfinder keeps one map with a Destination, "Decisions so far" (one line per closed ticket), "Not yet specified" and "Out of scope". Out-of-scope work "never graduates"; it returns only if the destination is redrawn.
- Each ticket is "sized to one 100K token agent session". The rule is "never resolve more than one ticket per session". A session loads "the low-res view, not every ticket body".
- "A decision lives in exactly one place", the tracker, not a branch.
- handoff writes the conversation to a file for a fresh agent and points to existing artifacts instead of copying them. implement-spec says "Start every subagent with a fresh context window".
- writing-for-agents treats always-loaded text as a cost ("context load"). It warns that a vague bound "invites premature completion".
- git-guardrails installs a PreToolUse hook that blocks dangerous git commands.

Evidence: none measured. The README cites "decades of engineering experience".

Fit:

- Taken: one step per session, a low-resolution brief, closed questions stated once, a parking lot kept apart from the decision record, and a PreToolUse hook as the enforcement point.
- Left: the issue-tracker map. A ds-stack project usually lives in one repo, and one file on main can't split across five planners. Grilling is ds-plan's job.

## Anthropic's Claude Code documentation

Read on 2026-11-17:

- the docs pages on [hooks](https://code.claude.com/docs/en/hooks), [skills](https://code.claude.com/docs/en/skills), [sub-agents](https://code.claude.com/docs/en/sub-agents), [memory](https://code.claude.com/docs/en/memory), [costs](https://code.claude.com/docs/en/costs) and [best practices](https://code.claude.com/docs/en/best-practices)
- the engineering posts [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) and [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

Mechanisms:

- Best practices: "If something has to happen every time, make it a hook … CLAUDE.md is for guidelines." Memory calls CLAUDE.md "context, not enforced configuration".
- PreToolUse blocks a call with `permissionDecision: "deny"` and shows the reason to Claude. SessionStart's `additionalContext` is added at session start, including after `compact` and `resume`, capped at 10,000 characters.
- The harness post uses a progress file and a JSON feature list the agent may only flip to passing ("It is unacceptable to remove or edit tests"). It chose JSON because the model rewrites JSON less readily than Markdown. Each session works on "only one feature at a time" and starts with a fixed routine: read the git log and progress file, then pick the next item.
- Saving tokens:
  - `/clear` between tasks, since "stale context wastes tokens on every subsequent message".
  - Hooks that filter output, cutting context "from tens of thousands of tokens to hundreds".
  - Subagents that return summaries of 1,000 to 2,000 tokens.
  - A CLAUDE.md under 200 lines.

Evidence:

- The costs page gives the only figures: about $13 per developer per active day, and about 7x more tokens for agent teams in plan mode.
- The context post cites Chroma's context-rot study.
- The harness post is anecdotal ("dramatically improved performance").

Fit:

- Taken: the hook layer, one item per session, the fixed start routine, protected settled entries, and output filtering.
- Left: a Stop hook that keeps the agent working. Our agents did too much, not too little.
- Left: a JSON state file. The PreToolUse guard answers the rewrite risk and keeps the file readable for the owner.

## What changed

Before this change, ds-stack guarded a single analysis (logged queries, traced numbers, a fixed readout) and had nothing that spanned sessions. Four changes, all in `ds-step`:

| Change | Failure it targets | How it is enforced |
|---|---|---|
| A task card in `DS-STATE.md`, plus Closed, Frozen, a parking lot and a Log | Long conversations, off-path work | `step.py start` refuses an empty field, more than five in-scope items, no time box, or a second open step |
| A run gate: `--decision` and `--if` on every run, a verdict before the next run, a third run blocked after two inconclusive ones | Tuning on noise | `step.py run` refuses. The test replays the ten-run loop, and the gate stops it at run 3 |
| Summary-only output: the log goes to `.ds-runs/R<n>.log`, and only SUMMARY/RESULT/VERDICT lines are printed | Rows read into context | `step.py run` |
| Hooks: SessionStart injects the brief; PreToolUse denies edits that change a closed answer, rewrite a running card or touch a frozen file | Instructions rewritten mid-run, reopened questions, losing the aim after compaction | `hooks/hooks.json`; inactive without `DS-STATE.md` |

`tests/test_ds_step.py` has 14 cases. In a live `claude -p` session, the agent quoted the aim and closed question C1 without reading a file. Its Edit of C1 was denied with the hook's reason, and it did not retry.

Not addressed:

- Too many planners. The skill says one planner writes Step cards and keeps state on main, but no script stops a person from opening five sessions.
- The Bash check is a heuristic.
- `step.py reopen` is open by design, and each reopen leaves a reason in the Log.
- Codex and Cursor get only the script's refusals, not the hooks.

The next evidence: run the next multi-session project under `ds-step` and compare runs per decision, inconclusive streaks, reopened questions and session length with this retro.
