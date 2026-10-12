# Porting ds-experiment to the work laptop

Run these steps on the work laptop. Each one prints only counts or pass/fail, so its output can be copied home without company data.

1. Overlay. Write `standards.json` from the triage meeting's standards, starting from `overlay.example/standards.json`: margins, what harm inside a margin does, the sample-split alpha. If the internal scorecard exports CSV, copy its header into `scorecard_map.json`.
2. Adapter self-test. Normalize one real scorecard with `normalize.py`, then run `decide.py` on it. The scorecard check must pass. A failure usually means the column map mixes percent and fractions or relative and absolute changes. Fix the map, not the check.
3. Measure the current agent. Run this on its last 20 readouts:
   ```
   python3 audit_readouts.py <dir>
   ```
   It prints median words, stat-speak terms, the line where the call first appears, the number of distinct structures, and lint fails by rule. These counts are the four symptoms in numbers, and the baseline to beat.
4. Backtest the rule. For the last 20 experiments that went to triage, write a row in `cases.csv`: scorecard, config and prereg paths, plus the call triage made. Then run:
   ```
   python3 backtest.py cases.csv --standards <overlay>/standards.json
   ```
   It prints the confusion matrix. Read each disagreement locally with `--show-rows`. Each one means either `standards.json` doesn't yet encode a team rule, or triage made a call the rule would have caught.
5. Use it as a post-processor. Have the work agent call `normalize.py`, `decide.py` and `render.py` instead of writing its own readout. Rerun step 3 on the next 20 readouts and compare.

In Cursor there is no `claude -p`, so run the cold read with `--prompts-only` and `--replies`.
