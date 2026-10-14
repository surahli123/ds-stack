# Acceptance run, Claude column (2026-10-14)

**Result.** Claude Code passes Plumbing, Correctness and Value in both English and Chinese, under the bar fixed in `docs/acceptance.md`. The Chinese Value result overstates the gain, for the format reason explained below. Review hasn't been done yet, and the Codex and Cursor columns are still to run on the owner's machine.

The bar was fixed at commit `4dc834a`. The model is Sonnet, with 8 fixtures × 3 arms × 3 runs per language. Results: `eval/results/2026-10-14-claude-en/` and `-zh/`. The table comes from `eval/acceptance.py`.

| Level | English | Chinese |
|---|---|---|
| Plumbing | PASS: 24 of 24 full-arm runs traced | PASS: 24 of 24 |
| Correctness | PASS: 8 of 8 fixtures right by majority | PASS: 8 of 8 |
| Value | PASS: plain prompting missed 6 of 9 runs on f6–f8; fixtures right: full 3, plain 1 | PASS: plain missed 8 of 9; full 3, plain 0 |
| Review | Not done | Not done |

| Runs right (of 24) | Plain prompting | Checks only | Full ds-mode |
|---|---|---|---|
| English | 13 | 12 | 23 |
| Chinese | 4 | 2 | 23 |

Model spend was $6.76 for English and $7.10 for Chinese.

## How to read it

- **Value in English is the real measure.** Plain prompting missed f6 (it used the obvious CTR definition, about 46% instead of 50.05%) and f7 (it reported add-to-cart as an 8.3% purchase rate). It also missed f1 and f3, where it abstained on the full rollouts. ds-mode got all four right. f8 didn't discriminate, as calibration predicted.
- **Chinese Value is inflated by the format contract.** Of the 20 plain-prompting misses in Chinese, 17 translated "ruled in/out", which only ds-mode is told to keep in English. Ignoring that, 9 of those 17 runs had the right answer. The substantive Chinese misses are the same as in English: f6 0 of 3, plus one f1 abstention.

## Failures in the full arm

| Run | What happened | Layer | Action |
|---|---|---|---|
| English f2 #3 | The right number, but its alternatives lacked "ruled in/out", so it parsed as unreadable | Model, format lapse | None. Counted; the bar is frozen |
| Chinese f2 #1 | Wrote "+54.98 pp" for a rate level that is in percent, so the grader found no number in percent | Model, unit error | None. Counted |

Neither failure changes a fixture's majority. No harness, plumbing or fixture failure occurred, and no skill-text or grader fix was needed in this run.

## Teeth tests

Each ran the full arm with one SKILL.md change, on a scratch branch since deleted. The patch is in each results directory.

| Change | Result | Caught? |
|---|---|---|
| Removed the three-estimate-lines rule | f1 3/3, f3 2/3, f6 3/3 right | No. With the lines gone, nothing prompts an abstention, so the rule isn't what makes f1 and f3 pass |
| Removed the step that reads `metrics.json` from `$DS_OVERLAY_DIR` | f6 0/3, f7 1/3 right | Yes. Both fixtures fail |

So the eval catches the loss of the metric-catalog step, but not the loss of the estimate rule. That rule matters only alongside the three-line format it explains.

## Still open

- The Codex and Cursor columns, which dots runs from `docs/prompts/acceptance-dots.md`.
- Review: a data scientist who didn't build ds-stack checks `eval/results/2026-10-14-claude-en/f6__full__1/` in under 10 minutes, using only `result.md`, `queries.log`, `checks.log` and the review checklist.
- Harder cases for the next round: `docs/eval-candidates.md`.
