---
name: ds-experiment
description: >-
  Use to read out an A/B experiment for a launch decision, especially search
  ranking tests on a Statsig-style scorecard: normalizes the scorecard and
  config, checks validity, makes the launch call from the pre-registration in
  code, and renders a one-screen readout for the launch review. The model
  writes only the mechanism and what would change the call. Also runs on
  /ds-experiment.
---

# ds-experiment

The launch call comes from code, not from reading 60 metrics. A call compares one interval with one pre-registered threshold. `decide.py` makes it and names the metric or check that decided it. Your job is to feed it correctly, explain the mechanism and say what would change the call. You can disagree, but only in a separate line.

## Steps

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
   The daily series must be by days since first exposure. A calendar-day series mixes day of week with late joiners. Read every line it prints. Don't edit `decision.json`.
5. **Write `notes.json`.** It is the only text you write. The schema is in `tools/render.py`.
   - `why_it_moved`: at most 3 bullets, each labelled measured, inferred or guess. Use segment cuts in the scorecard when they exist. Otherwise one guess bullet says the mechanism is unknown.
   - `would_change`: at most 3 bullets. Each names the data or event that would flip the call.
   - `analyst_view`: only when you'd make a different call, with the reason. Use it when the evidence contradicts the pre-registration, for example a primary that rose for a bad reason.
6. **Render:**
   ```
   python3 <dir>/tools/render.py --decision decision.json --scorecard scorecard.json --notes notes.json
   ```
   It refuses notes that use stat-speak or numbers that aren't in the scorecard. It also refuses call words in "why it moved". Fix the notes and rerun. Don't route around it.
7. **Test the read:**
   ```
   python3 <dir>/../doc-tighten/tools/doc_lint.py readout.md --spine spine.json
   python3 <dir>/../cold-read/tools/cold_read.py readout.md --spine spine.json
   ```
   `render.py` writes `spine.json` from the decision. Never edit it.
8. **Reply** with `readout.md` exactly as rendered, then the lint and cold-read result lines verbatim, and nothing else. Add no preamble and no caveats section. A caveat that matters belongs in `would_change` or `why_it_moved`, so rerender. If the cold read fails, say so in one line after the result lines.

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
