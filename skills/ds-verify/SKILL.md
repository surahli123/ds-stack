---
name: ds-verify
description: >-
  Use to check a finished ds-mode readout before anyone acts on it: "verify
  this readout", "check this analysis", "is this number right", "review the
  readout before I send it", "帮我核对这个结论", "检查这个分析对不对". Replays
  every logged query on a copy of the data, traces every number, checks the
  estimand, the "ruled in" evidence, the flagged checks and the team's metric
  definitions, and lists what a reviewer must judge, in order. Also runs on
  /ds-verify.
---

# ds-verify

A ds-mode readout says where each number came from. This skill checks that the readout is true to those sources: the queries still return what was logged, the numbers are the ones the sources show, and the words match the evidence. It writes no analysis and changes no file. ds-mode runs it as its last step when this skill sits next to it; a reviewer runs it first, then reads only what it points to.

## Steps

1. Collect the inputs:
   - the readout;
   - the query log (`.ds-queries.log`, or `$DS_QUERIES_LOG`) and the check log (`.ds-checks.log`, or `$DS_CHECKS_LOG`);
   - the database the queries ran on (`--db`, else `$DS_WAREHOUSE`, else `./warehouse.db`);
   - the overlay folder (`$DS_OVERLAY_DIR`);
   - the original request. ds-mode doesn't save it, so write it to `request.md` first.

   A missing input never passes: its checks report `could_not_verify`.
2. Run the script from the analysis directory:

   ```bash
   python3 <skills>/ds-verify/tools/ds_verify.py readout.md --request request.md
   ```

   For an eval run directory, `--run-dir <dir>` reads `result.md`, `queries.log` and `checks.log` from it. `--json report.json` also writes the report as JSON. The private copy of the database goes in `$TMPDIR`; set it to a disk with room for one copy.
3. Read the first line:
   - `ds-verify: pass`: every check passed;
   - `ds-verify: fail`: at least one check failed;
   - `ds-verify: unverified`: nothing failed, but something that matters couldn't be checked, such as a missing input, a pasted result, or a Headline number not found in its source.

   The exit code is 0, 1 or 2 in the same order. Next come the findings, then "Needs a human, in this order".
4. Act on it:
   - Analyst: fix each failure, then run the script again. A failure about a number or a definition is fixed in the analysis, by rerunning the queries; rewording the readout doesn't fix it. Add its first line to Provenance's `- Verified:` line, after the verify_readout.py result. Don't change a check, a log or the request to make a failure go away.
   - Reviewer: work down the "Needs a human" list. It holds the failures and unchecked items, the numbers to check by hand, `[guess]` lines, checks that couldn't run, a missing reconciliation, and the `[given]` numbers to confirm against the request. A readout with a failure goes back to the analyst with the failure's line.
   - An `overlay` failure means the readout and the team's metric definition disagree. Fix the readout. A change to `metrics.json` needs a person's approval; this skill never edits it.

## The checks

| Check | Fails when |
|---|---|
| `trace` | A number has no tag, or a tag names a query or check that didn't run |
| `replay` | A logged query, replayed in order on a private copy of the database, returns different rows or no longer runs |
| `sources` | Never fails. A number missing from the output it cites is a by-hand item; on the Headline it is `could_not_verify` |
| `estimand` | The Headline's unit isn't the one asked for, a causal number has no `from <design>`, the Headline contradicts its estimate line, or it says `can't tell` while Adjusted has a number, the Causal effect is not identified and no completeness, srm or fanout check flagged |
| `alternatives` | No alternative says "ruled in", "ruled out" or "not ruled out", or a hedged "ruled in" has no flagged check behind it |
| `flags` | A check that flagged or failed isn't reported by its tag. A rerun of the same check on the same input makes it a warning |
| `overlay` | The Metric line lacks the overlay's numerator, denominator or filters; the SQL behind the Headline lacks them; the Headline's result column is computed without them; or an estimate gives a number for an unavailable metric |

The overlay check finds a metric by its key in `metrics.json`, by an `aliases` list in its entry (for example `"aliases": ["点击率", "click-through rate"]`), or by its numerator and denominator in the Metric line.

The Metric line's words are easy to change, so the check also reads the runner queries the Headline, Observed and Adjusted lines cite, directly, through a check's `from`, or through the query ids a pasted entry names. Their SQL must use the numerator, the denominator and each filter's column. When one query computes both definitions, the result column that holds the Headline number must be computed from the overlay's numerator and denominator. Each column name is read from the database (`base_columns()`, the second port point), so a ratio of aliases from a CTE is left alone. A Headline computed by hand is left alone too: it is already `unverified`.

## Porting replay to the warehouse

`scratch_copy()` in `tools/ds_verify.py` is the main port point; `base_columns()`, which lists the columns of every table, is the other. In this reference it copies a SQLite file through the backup API on a read-only connection, which includes a WAL file and never writes to the source. It then drops the scratch tables the analysis left, so their `CREATE` statements replay cleanly. A warehouse port replaces that function with a scratch schema it may write to, under the same prefix as `runner.json`. It must never replay into the tables the analysis read.

## What it can't tell you

It checks the readout against its own evidence. It can't tell whether the analysis asked the right question, chose the right comparison, or missed an alternative nobody listed. That is the reviewer's part: `ds-mode/references/review-checklist.md`.

## How it was proved

`eval/verify_eval.py` runs this script on graded eval runs, without gold. The results below are in-sample: the rules were written after reading these runs and an adversarial review of them.

- 68 Claude full-arm runs in the current readout format:
  - It fails all 7 that the grader marks wrong: 5 ignored the overlay in the arm without the overlay step, 1 gave a percent level in pp, and 1 wrote no "ruled in/out" verdicts. None of the 7 is a wrong number caught by replay, because no run had one.
  - Of the 61 marked right, 50 pass and 10 are unverified, for a pasted result or a Headline derived by hand.
  - 1 fails. Its Headline gives a percent level in pp, a unit the grader let through.
- All 381 runner queries replay to the logged rows.
- 2 Codex validation runs: it fails both. The one marked right wrote "ruled in as unresolved possibilities".

The held-out test ran on the 48 full-arm runs of the 2026-11-02 Codex matrix. It failed 9 of 10 wrong runs. It failed 22 of 38 right runs, each for a "ruled in" that meant "not excluded". 7 of the wrong runs were abstentions, which it couldn't yet see. Details: `docs/results.md`.
