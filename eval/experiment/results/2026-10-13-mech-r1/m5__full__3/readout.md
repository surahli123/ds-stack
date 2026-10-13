# Ranker v7: Escalate

Decision: Escalate. Successful Search Rate rose 0.68% (+0.28% to +1.08%), but Abandonment Rate rose 2.10% (+1.50% to +2.70%), the wrong way, though inside its 4.00% margin.

Ask: Decide the trade-off at triage.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: secondary metric CTR got worse after correction.

Triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Abandonment Rate | guardrail | +2.10% (+1.50% to +2.70%) | at most 4.00% higher | worse, within margin |
| Successful Search Rate | primary | +0.68% (+0.28% to +1.08%) | estimate at least 0.50% higher | better |
| 1 other guardrail | guardrail | | | within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- If abandonment sits on queries with no answer or rich snippet, or users re-search soon after leaving, the rise is harm and the abandonment trade-off tips against the change.
- If success rises only on queries where the ranking changed, the win is real and larger there; if it is flat there, the overall rise is not from ranking.
- A pre-exposure comparison that shows the arms already differed would make the test unreliable.

## Why it moved

- [inferred] Successful Search Rate rose 0.68% while abandonment went up and CTR fell 1.10%: this fits users getting answers on the page and leaving without a click. No cut has tested it.
- [inferred] Clicks per User fell 1.20% while Queries per User didn't move clearly, which fits fewer clicks per search and no extra searching. It does not show whether those searches were satisfied.
- [guess] The mobile and desktop success rates are both slightly down though overall success is up, so the overall rise is not yet traced to any slice.

## Appendix

- Secondary metrics: 54 tested; after a false-discovery correction these moved: CTR (-1.10%), Clicks per User (-1.20%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms).
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
