# Dialogue evaluation (development only)

This is a small development set, not a holdout. Replay tests responses to explicit user contributions, corrections, scope and finishing. It cannot establish whether useful questions were asked or whether the model elicited a scripted fact. Every scripted turn is a USER contribution regardless of the preceding answer; no turn says that the assistant offered or requested it. No automatic semantic scoring or pass verdict is produced. The old plan evaluation remains separate.

The runner uses `claude -p` with the same tool permissions and clean HOME/Claude config for each arm; each successful turn resumes the same session. No private review rubric or future turns are copied to the workspace. No data is supplied. Raw per-turn stdout/stderr, user/assistant transcript, exit/session/usage/cost/time, installed skill file hashes, and routing evidence are written to a new result directory. Unknown usage or cost remains null; a total is null if any constituent is unknown. A failure, empty answer, missing/changed session or timeout stops the conversation and marks it incomplete. No retry occurs. Results can contain model-generated text and should be inspected before sharing.

Choose model and runs only with authorization; the examples do not imply approval to spend. Use the same model, case and timeout across arms. Specify a commit for the current arm, which is extracted from git rather than an installed cache; provide a candidate skills directory containing `ds-plan/` and `ds-mode/` (the latter is required for mode-entry). Each result path must be new:

```sh
python3 eval/dialogue/run_dialogue.py --case retro-3p --arm baseline --model MODEL --out /tmp/dialogue-baseline
python3 eval/dialogue/run_dialogue.py --case retro-3p --arm current --current-ref COMMIT --model MODEL --out /tmp/dialogue-current
python3 eval/dialogue/run_dialogue.py --case retro-3p --arm candidate --skill-source /path/to/skills --model MODEL --out /tmp/dialogue-candidate
```

Repeat with `company-correction`, `one-shot`, and `mode-entry`. Direct cases point to ds-plan. For mode-entry both skill arms install ds-mode and ds-plan and CLAUDE.md directs ds-mode only. `routing: observed` requires successful Read tool results for this run's installed ds-mode followed by ds-plan; paths in other installations do not count. Otherwise routing is unverified, even if the answer mentions the skills. Read events show what was loaded, not whether instructions were followed. Check the raw logs and content before drawing conclusions.

## Manual adaptive walkthrough

Use the same clean profile, source versions, tool permissions and initial user turn as replay. Continue each arm in the same session. The fact bank is the USER turns in `cases.json`; provide a fact only when relevant, as an explicit user statement. If asked outside the bank, answer "unknown" or apply the same predeclared response across arms. Record each assistant question verbatim and the exact subsequent user fact or proposal, its source, turn number, and whether it answered that question. Never claim a fact was elicited when it was independently volunteered. Do not accept a model proposal unless it was actually offered; record any acceptance explicitly. Apply the same response rules to each arm and disclose differences in user paths. This manual mode assesses question usefulness, but is not an automated or controlled replay. Keep private fact bank and rubric outside the agent workspace.

## Manual review template

For each judgment record turn number, exact assistant quote, user contribution and rationale; mark unsupported or not observable when appropriate. Review the whole final body and earlier responses, not just headings or closing lines. Record:

- Scope and outcome definition, including 3p clicks vs citations, and whether corrections persist throughout the body.
- Whether the current question was answered, especially the mathematical expression; any repeated questions and why they matter.
- Facts vs user proposals vs unverified assumptions, including who introduced each, and the status of P80, randomization, records and observed results.
- Pre-treatment grouping and later activation; company assignment vs salesperson target; implications of the dependency correction.
- Whether the response finishes when asked, identifies actionable checks and remaining decisions, and avoids unauthorized execution or invented results.
- For adaptive walkthroughs only, question → fact/proposal provenance and whether each question changes a decision.
- Execution status, routing evidence, usage/cost/time, and the turns needed to reach a user-confirmed candidate; do not compare incomplete runs as completed dialogues.

Calibration negative example: a final paragraph says "assignment was by company; target is the salesperson; dependency is unresolved," while the body groups people by login frequency and treats them as independently randomized. A reviewer should flag the body contradiction with quotations even though the closing paragraph looks correct. This is a manual calibration example, not a claim of automatic detection. Future untouched cases and predeclared judgments are required before making general efficacy or win-rate claims.
