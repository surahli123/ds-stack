# Ranker v7: Ship

Decision: Ship. Successful Search Rate rose 0.81% (+0.41% to +1.21%), which clears the 0.50% bar and every guardrail held.

Ask: Approve the launch to all traffic.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: secondary metric Queries per User got worse after correction.

Triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | estimate at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- Success on triggered queries flat while untriggered carries the lift, or the lift tied to the Queries per User drop, would make the win a counting effect.
- A pre-exposure comparison showing the arms already differed on Successful Search Rate would void the result.
- Segment mix shifting between arms in a per-user cut would explain the segment-versus-total gap.

## Why it moved

- [measured] CTR rose 2.10% mostly through its denominator. Queries per User fell 1.90% while Clicks per User stayed flat (+0.10%): same clicks over fewer searches.
- [inferred] Successful Search Rate rose 0.81%, but Long Click Rate (-0.03%), Reformulation Rate and Abandonment Rate did not improve, so a pure relevance gain is not yet shown.
- [guess] Segment cuts of Successful Search Rate are all flat or negative (Informational -0.89%) though the total rose; search mix may differ between arms.

## Appendix

- Secondary metrics: 52 tested; after a false-discovery correction these moved: CTR (+2.10%), Queries per User (-1.90%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
