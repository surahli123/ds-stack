## Answer
Headline: can't tell (2026-10-07 is only partly loaded, so there's no valid full-day number yet)

The apparent drop of about 2.8 pp is not a real CTF decline. 2026-10-07 has only hours 0–9, and that partial day over-represents low-CTR night hours.

- Observed: -2.83 pp (-3.47 to -2.20): 27.00% on the partial day vs 29.83% for 2026-09-30 to 2026-10-06 [measured]
- Adjusted: +0.10 pp (-0.61 to +0.81), holding hour-of-day mix fixed (night 0–7 vs day 8–23) [measured]
- Causal effect: not identified (no experiment or intervention here; it would take a full day of data plus a known change to attribute)

## What it means for the leadership update
Don't report a drop. The like-for-like interval of -0.6 to +0.8 pp includes zero. Hours 0–9 are 27.0% on both 2026-10-07 and the prior 7 days. The mix-adjusted interval is wider than the 0.1 pp minimum-effect threshold in the check, so a small real change can't be ruled out. Re-run once 2026-10-07 is fully loaded.

## Why we believe it
- Alternatives considered:
  - Real CTR decline: ruled out for the hours loaded. Hours 0–9 give 27.0% yesterday vs 27.0% over the prior 7 days. Within-segment change is +0.10 pp [measured]
  - Partial-day / mix artifact: ruled in. Mix accounts for -2.93 pp, 97% of the gap [measured]
  - A drop in the not-yet-loaded hours 10–23: can't be excluded [guess]
- Checks run:
  - completeness: fail. 2026-10-07 has 10 of 24 hourly rows, 42% of the trailing median [check:completeness#1]
  - mix_shift: flag. Mix-dominant, with within-segment change +0.10 pp (-0.61 to +0.81) [check:mix_shift#2]
  - fanout and srm: skipped. There are no joins and no experiment in this task.

## Caveats, and what would change the answer
- The intervals assume independent searches. Clustering by user or session would widen them.
- The two-segment split (night/day) is coarse. Hourly rates are flat within each block in the data I saw.
- Any change that appears only after hour 9 would not show up here.
- Comparing hours 0–9 across days is measured. The claim that the full day will match is inferred.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), stated here [guess]. No metrics.json exists in the directory.
- Data: search_hourly, complete through 2026-10-06. 2026-10-07 is partial (hours 0–9).
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: the checks are logged in `.ds-checks.log` (completeness#1, mix_shift#1 and #2). The mix_shift#1 entry is a could-not-run test attempt. The ad-hoc SQLite queries were run inline and not saved.