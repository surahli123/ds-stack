## Answer
Headline: 0.0 percentage points (like-for-like, hours 0–9: 27.0% yesterday vs 27.0% in the prior 7 days)
There is no real drop. Yesterday's data stops at hour 9, and the early hours always have lower CTR, so the partial day makes the overall figure look lower. [measured]

## What it means for the CTR drop report to leadership
Don't report a drop. The 27.0% vs 29.8% gap comes from comparing a partial day with full days. Re-check once the full day of 2026-10-07 has loaded.

## Why we believe it
- Alternatives considered:
  - Real CTR decline: ruled out. Hour by hour, yesterday matches the prior days: 24.0% in hours 0–7 and 31.0% in hours 8–9, and the prior week shows the same pattern. [measured]
  - Partial-day artifact: ruled in. Yesterday has only 10 of 24 hourly rows (hours 0–9). Its raw CTR is 27.0% (5,292 / 19,600) against about 29.83% for full days. The prior 7 days restricted to hours 0–9 also come to 27.0% (37,044 / 137,200). [measured]
  - Mix shift across hours: this is what explains the gap. Low-CTR overnight hours make up a larger share of a 10-hour day than of a 24-hour day. [inferred]
  - Data pipeline lag or outage: not ruled out. The data stops at hour 9, and I can't tell from here whether the load is still running or has failed. [guess]
- Checks run:
  - completeness: fail. 2026-10-07 has 10 rows, 42% of the 24-row trailing median, so the day is incomplete.
  - mix_shift: skipped. I did the equivalent hour-matched comparison by hand instead of running the check.
  - fanout: skipped. No joins were used.
  - srm: skipped. This is not an experiment.

## Caveats, and what would change the answer
- Only hours 0–9 of yesterday exist, so the hours from 10 on are unobserved. A real drop could still show up there.
- The hour-matched baseline is the prior 7 days (2026-09-30 to 2026-10-06), which is a small sample.
- Once the full day loads, compare full-day CTR with the 29.83% baseline. A value clearly below that would change this answer.