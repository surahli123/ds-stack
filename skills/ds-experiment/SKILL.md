---
name: ds-experiment
description: >-
  Use to read out an A/B experiment, especially search ranking tests on a
  Statsig-style scorecard: checks validity, makes the launch call from the
  pre-registration in code, explains why metrics moved and which cuts to run
  next, says whether the result is ready for triage, and renders a one-screen
  readout plus a triage prep sheet. Also runs on /ds-experiment.
---

# ds-experiment

The launch call comes from code, not from reading 60 metrics. A call compares one interval with one pre-registered threshold. `decide.py` makes it and names the metric or check that decided it. Your job is to feed it correctly, explain the mechanism and say what would change the call. You can disagree, but only in a separate line.

## Steps

`<overlay>` below is `$DS_OVERLAY_DIR`, the private overlay. If it's unset, leave out `--standards`: the defaults apply and the readout says so. Don't search the filesystem for an overlay or for example files.

1. **Collect the inputs:**
   - the scorecard: the Statsig `pulse_results` response, or a CSV export
   - the experiment config and its audit log
   - the team's pre-registration

   Save what the results were requested with (CUPED, confidence level, corrections) as `request.json`, because the response doesn't say.
2. **Normalize:**
   ```
   python3 <dir>/tools/normalize.py --pulse pulse.json --request request.json --experiment experiment.json --audit audit_logs.json
   ```
   For a CSV export use `--csv export.csv --map <overlay>/scorecard_map.json`. If it reports unknown settings, find them; don't assume.
3. **Write `prereg.json`** from the team's pre-registration, following `references/prereg.md`.
   - Copy bars, margins and directions. Never invent them.
   - Leave out what the team didn't write. The overlay's `standards.json` fills it, and the readout says so.
   - Set `"confirmed": false` unless the owner checked it.
4. **Decide:**
   ```
   python3 <dir>/tools/decide.py --scorecard scorecard.json --config config.json --prereg prereg.json --standards <overlay>/standards.json [--daily daily_by_exposure_day.json]
   ```
   The daily series must be by days since first exposure. A calendar-day series mixes day of week with late joiners. Read every line it prints.
   Never edit `scorecard.json`, `config.json` or `decision.json` by hand, and never correct the export's numbers yourself. If a check fails because of how the data was exported, the call is Can't tell. Say in `would_change` how to fix the export. The readout's History line shows every rerun that changed the call.
5. **Explain, and dig before triage:**
   ```
   python3 <dir>/tools/explain.py --decision decision.json --scorecard scorecard.json --prereg prereg.json --config config.json [--evidence evidence.json]
   ```
   It prints the triage readiness, the questions triage will ask with candidate mechanisms (from `references/search_patterns.json` and the overlay's `patterns.json`), and the cuts to run in order. Each cut says what result would support or contradict its mechanism.
   - With data access, run the top cuts through the guarded runner as aggregates. Put the results in `evidence.json` (format in `tools/explain.py`), then rerun: new metrics under `metrics`, splits under `segments` with per-arm units, and outcomes of cuts that aren't either under `cuts`. A cut that supports a candidate confirms it; one that contradicts it removes it. Repeat until the plan is empty or the verdict stops changing.
   - Record every cut you ran, including the ones that found nothing. The count of cuts run is part of the evidence.
   - A "Not ready" verdict names what to do first. Do that before anything else.
   - Patterns found by scanning, and segments not in the pre-registration's `segments`, are exploratory. They can start a rerun or a new test, never a launch.
6. **Write `notes.json`.** It is the only text you write. The schema is in `tools/render.py`.
   - `why_it_moved`: at most 3 bullets, each labelled measured, inferred or guess. Take them from `explain.json`: a mechanism is measured only when a cut you ran supports it.
   - `would_change`: at most 3 bullets, each naming the data or event that would flip the call.
   - `analyst_view`: only when evidence the rule can't see would change the call, with the reason. Never use it to argue with a registered bar or margin, a check that couldn't run, or a secondary metric that didn't survive correction. The classic case is a volume primary (queries, sessions or clicks per user) that rose while success fell or reformulation rose: more searching can mean worse results.
7. **Render:**
   ```
   python3 <dir>/tools/render.py --decision decision.json --scorecard scorecard.json --notes notes.json --explain explain.json
   ```
   It writes `readout.md` for the launch review and `triage_prep.md` for the engineer: the questions, candidate answers and cuts. It refuses notes that use stat-speak, use numbers not in the scorecard, or put call words in "why it moved". Fix the notes and rerun; don't route around it.
8. **Test the read:**
   ```
   python3 <dir>/../doc-tighten/tools/doc_lint.py readout.md --spine spine.json
   python3 <dir>/../cold-read/tools/cold_read.py readout.md --spine spine.json
   ```
   `render.py` writes `spine.json` from the decision. Never edit it.
9. **Reply** with `readout.md` exactly as rendered, starting with its first line, then `triage_prep.md` as rendered, then the lint and cold-read result lines verbatim, and nothing else. Never summarize it or point to the file instead. Add no preamble and no caveats section. A caveat that matters belongs in `would_change` or `why_it_moved`, so rerender. If the cold read fails, say so in one line after the result lines.

## Rules that hold even when they're inconvenient

- Never recompute an interval the platform gave. A two-proportion interval on query-level metrics, when users were randomized, is too narrow.
- Only the primary and the registered guardrails can block. Secondaries are corrected for false discoveries and can't change the call, however red they look.
- A failed check is softened only by an explanation listed in the pre-registration, and then it escalates.
- A flat result is "no effect found" only when the interval rules out the bar. Otherwise the test needs more data, or it was too small to answer.
- A lift measured on triggered traffic is not the overall lift. Set `mass_share` so the call is made on the right population.
- Without `claude` (Cursor, Codex), run the cold read with `--prompts-only` and grade with `--replies`.

## Calls

| Call | Means |
|---|---|
| Ship | the primary clears its bar and every guardrail is within its margin |
| Don't ship | a guardrail is past its margin, or the primary got worse |
| Escalate | a trade-off for triage: a guardrail is unclear, harm sits inside a margin, the win is below the bar, or primaries split |
| Keep running | not enough data yet: before the planned sample, the effect is fading, or one extension would settle it |
| No effect found | enough data, and the interval rules out the bar |
| Can't tell | the test is broken: the sample split, config, scorecard or pre-period check failed |
| Not an A/B test | interleaving or holdout; this rule doesn't apply |
