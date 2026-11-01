---
name: ds-verify
description: >-
  Use to check a finished ds-mode readout before anyone acts on it: "verify
  this readout", "check this analysis", "is this number right", "review the
  readout before I send it", "帮我核对这个结论", "检查这个分析对不对". Replays
  every logged query on a copy of the data, traces every number, checks the
  estimand, the "ruled in" evidence, the flagged checks and the team's metric
  definitions, and lists what a reviewer must look at by hand. Also runs on
  /ds-verify.
---

# ds-verify

A ds-mode readout says where each number came from. This skill checks that the readout is true to those sources: the queries still return what was logged, the numbers are the ones the sources show, and the words match the evidence. It writes no analysis and changes no file. The analyst runs it before replying; a reviewer runs it first, then reads only what it points to.

## Steps

1. Find the inputs. The readout, the query log (`.ds-queries.log` or `$DS_QUERIES_LOG`), the check log (`.ds-checks.log` or `$DS_CHECKS_LOG`), the database the queries ran on, the overlay folder (`$DS_OVERLAY_DIR`), and the original request saved to a file. A missing input makes its checks `could_not_verify`, never `pass`.
2. Run the script from the analysis directory:

   ```bash
   python3 <skills>/ds-verify/tools/ds_verify.py readout.md --db warehouse.db --request request.md
   ```

   It reads the logs and the overlay from the environment, or from `--queries`, `--checks` and `--overlay`. For an eval run directory, `--run-dir <dir>` reads `result.md`, `queries.log` and `checks.log` from it. `--json report.json` also writes the report as JSON.
3. Read the report. The first line is `ds-verify: pass` or `ds-verify: fail` with counts. Then come the failures, the checks it could not do, the warnings, the numbers to check by hand, and the `[given]` numbers to confirm against the request.
4. Act on it:
   - Analyst: fix each failure in the analysis or the readout, run the script again, and put its first line in Provenance as `- Verified: <line>`. Don't change a check, a log or the request to make a failure go away.
   - Reviewer: start with the failures, then the numbers to check by hand, then the `[given]` lines. A readout with a failure goes back to the analyst with the failure's line.
   - A failure on the `overlay` check means the readout and the team's metric definition disagree. Fix the readout. A change to `metrics.json` needs a person's approval; this skill never edits it.

## The checks

| Check | Fails when |
|---|---|
| `trace` | A number has no tag, or a tag names a query or check that didn't run (ds-mode's `verify_readout.py`) |
| `replay` | A logged query, replayed in order on a temporary copy of the database, returns different rows or no longer runs |
| `sources` | Never fails. A point estimate that isn't in the output it cites goes on the "check by hand" list |
| `estimand` | The Headline's unit isn't the one asked for, a Causal effect number names no design, or the Headline matches no estimate line |
| `alternatives` | No alternative says "ruled in" or "ruled out", or a hedged "ruled in" ("unresolved", "possible") has no flagged check behind it |
| `flags` | A check that flagged or failed is missing from the readout |
| `overlay` | The Metric line ignores the overlay's definition, or the Headline gives a number for a metric the overlay marks unavailable |

Replay uses the SQLite reference adapter, like `ds-mode/tools/query.py`. A warehouse port replaces `connect()` in `tools/ds_verify.py` and replays into its own scratch area. It never replays into the tables the analysis read.

## What it can't tell you

It checks the readout against its own evidence. It can't tell whether the analysis asked the right question, chose the right comparison, or missed an alternative nobody listed. That is the reviewer's part: `ds-mode/references/review-checklist.md`.

## How it was proved

`eval/verify_eval.py` runs this script on graded eval runs. It never reads gold. On 68 full-arm runs in the current readout format, it failed all 7 that the grader marked wrong. It also failed 3 of the 61 that the grader marked right; each had a real fault in the readout: two left out a failed check, and one gave a percent level in pp. All 381 runner queries replayed to the logged rows. The rules were written after reading some of those failures, so the next unseen run set is the real test.
