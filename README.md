# ds-stack

A small, pstack-style plugin for data-science work. It doesn't make agents faster. It makes their numbers more trustworthy: before an agent reports a number, scripts check the mechanics, the agent rules alternative explanations in or out with evidence, and it writes a readout a person can act on.

> If you want to go fast, go deep first. — poteto, [pstack](https://github.com/cursor/plugins/tree/main/pstack)

This repo is v0 of the plan in the owner's notes (`ds-stack-brainstorm-design-v2-2026-10-08.md`). It holds only the **generic core**. Company facts live in a private overlay outside any repo (see [`overlay.example/`](overlay.example/README.md)).

## What's in it

| Path | What it is | Portable? |
|---|---|---|
| `skills/ds-mode/SKILL.md` | The thin method skill: restate, check the data, size and decompose, rule alternatives in or out, write the readout | Yes: plain SKILL.md |
| `skills/ds-mode/checks/` | Four check scripts on aggregates, using only the Python standard library: `completeness`, `fanout`, `mix_shift`, `srm` | Yes: Python 3.10+, no dependencies |
| `skills/ds-mode/checks/registry.json` | The evidence behind each check. Only `mix_shift` is "evidenced" so far; the others are provisional until real incidents back them | n/a |
| `safety/` | The reference guarded query runner and its startup self-test (the safety envelope) | The contract is portable; adapters live in the overlay |
| `hooks/`, `.githooks/` | A pre-commit and pre-push hook that blocks terms from the overlay's denylist. It is fail-closed | git + bash |
| `eval/` | Seeded synthetic fixtures with gold answers, a three-arm runner (`claude -p` in clean profiles), a script grader, and the pre-registered pass rule | Claude Code CLI |
| `tests/` | Unit tests. Each check must fail on its planted mistake | pytest |

## Install the skill

Copy the one folder `skills/ds-mode/` to wherever your tool looks for skills:

| Tool | Location | Status |
|---|---|---|
| Claude Code | `~/.claude/skills/ds-mode/` or `<project>/.claude/skills/ds-mode/` | tested here in the three-arm eval |
| Cursor | `~/.cursor/skills/ds-mode/` or `<project>/.cursor/skills/ds-mode/` | not yet smoke-loaded |
| Codex | your Codex skills folder | not yet smoke-loaded |

Then type `/ds-mode <your question>`, or let the skill's description trigger it.

## How a run works

1. The agent restates the question and names the decision it feeds.
2. It computes aggregates, then runs the checks that apply, for example `python3 checks/run.py mix_shift --json '{...}'`. Each check prints one JSON line and appends it to `.ds-checks.log`, so a grader reads what actually ran instead of trusting the agent's report.
3. A failed check must change the answer, or the readout must show why it doesn't. A check that applies but can't run means the headline is `can't tell`.
4. The final reply is the fixed readout: Answer (with a `Headline:` line), what it means for the decision, the alternatives ruled in or out with measured, inferred or guess labels, the checks run, and the caveats.

## Develop

```bash
make test        # unit tests
make selftest    # safety envelope
make hooks       # enable the denylist hook (needs DS_OVERLAY_DIR or DS_DENYLIST)
make fixtures    # regenerate fixtures and gold (deterministic)
make eval        # 5 fixtures x 3 arms x 3 runs via claude -p (uses model credits)
make grade RUN=eval/results/<dir>
```

## Honest status

- The fixtures are **synthetic** and number 5. The pass rule needs at least 15 held-out fixtures before it will issue a verdict, so every eval here reports `INSUFFICIENT_N`. That makes it a smoke test of the harness, not proof that v0 works.
- Three of the four checks are **provisional**. They need real incidents from the wrong-number archive (plan Stage 1) before they count as evidenced.
- The method in `SKILL.md` is a **draft** based on the owner's earlier search-metric work. The owner replaces it with their own first five moves (plan Stage 2).
- The skill has not yet been smoke-loaded in Cursor or Codex.
